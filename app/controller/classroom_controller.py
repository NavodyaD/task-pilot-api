from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_db, require_roles
from app.models.classroom_model import Classroom, ClassroomStudent
from app.models.user_model import User
from app.schemas.classroom_request import ClassroomCreateRequest, EnrolStudentRequest

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


def get_owned_classroom(classroom_id: int, teacher: User, db: Session) -> Classroom:
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    if classroom.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="You can manage only your own classrooms")
    return classroom


@router.post("", status_code=status.HTTP_201_CREATED)
def create_classroom(data: ClassroomCreateRequest, db: Session = Depends(get_db), teacher: User = Depends(require_roles("TEACHER"))):
    classroom = Classroom(name=data.name, description=data.description, teacher_id=teacher.id)
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom


@router.get("")
def list_classrooms(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "TEACHER":
        return db.query(Classroom).filter(Classroom.teacher_id == user.id).all()
    return db.query(Classroom).join(ClassroomStudent).filter(ClassroomStudent.student_id == user.id).all()


@router.post("/{classroom_id}/students", status_code=status.HTTP_201_CREATED)
def enrol_student(classroom_id: int, data: EnrolStudentRequest, db: Session = Depends(get_db), teacher: User = Depends(require_roles("TEACHER"))):
    get_owned_classroom(classroom_id, teacher, db)
    student = db.query(User).filter(User.id == data.student_id, User.role == "STUDENT").first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if db.query(ClassroomStudent).filter_by(classroom_id=classroom_id, student_id=data.student_id).first():
        raise HTTPException(status_code=409, detail="Student is already enrolled")
    enrollment = ClassroomStudent(classroom_id=classroom_id, student_id=data.student_id)
    db.add(enrollment)
    db.commit()
    return {"message": "Student enrolled successfully"}


@router.get("/{classroom_id}/students")
def list_students(classroom_id: int, db: Session = Depends(get_db), teacher: User = Depends(require_roles("TEACHER"))):
    get_owned_classroom(classroom_id, teacher, db)
    return db.query(User).join(ClassroomStudent).filter(ClassroomStudent.classroom_id == classroom_id).all()
