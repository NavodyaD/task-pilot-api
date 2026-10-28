from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_db, require_roles
from app.controller.classroom_controller import get_owned_classroom
from app.models.academic_model import Assessment, Mark, Subject
from app.models.classroom_model import ClassroomStudent
from app.models.user_model import User
from app.schemas.classroom_request import AssessmentCreateRequest, MarkCreateRequest, SubjectCreateRequest

router = APIRouter(tags=["Subjects, Assessments and Marks"])


def get_owned_subject(subject_id: int, teacher: User, db: Session) -> Subject:
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    get_owned_classroom(subject.classroom_id, teacher, db)
    return subject


def get_owned_assessment(assessment_id: int, teacher: User, db: Session) -> Assessment:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    get_owned_subject(assessment.subject_id, teacher, db)
    return assessment


@router.post("/classrooms/{classroom_id}/subjects", status_code=status.HTTP_201_CREATED)
def create_subject(classroom_id: int, data: SubjectCreateRequest, db: Session = Depends(get_db), teacher: User = Depends(require_roles("TEACHER"))):
    get_owned_classroom(classroom_id, teacher, db)
    subject = Subject(name=data.name, classroom_id=classroom_id)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("/classrooms/{classroom_id}/subjects")
def list_subjects(classroom_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "TEACHER":
        get_owned_classroom(classroom_id, user, db)
    elif not db.query(ClassroomStudent).filter_by(classroom_id=classroom_id, student_id=user.id).first():
        raise HTTPException(status_code=403, detail="You are not enrolled in this classroom")
    return db.query(Subject).filter(Subject.classroom_id == classroom_id).all()


@router.post("/subjects/{subject_id}/assessments", status_code=status.HTTP_201_CREATED)
def create_assessment(subject_id: int, data: AssessmentCreateRequest, db: Session = Depends(get_db), teacher: User = Depends(require_roles("TEACHER"))):
    get_owned_subject(subject_id, teacher, db)
    assessment = Assessment(**data.model_dump(), subject_id=subject_id)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


@router.get("/subjects/{subject_id}/assessments")
def list_assessments(subject_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    if user.role == "TEACHER":
        get_owned_subject(subject_id, user, db)
    elif not db.query(ClassroomStudent).filter_by(classroom_id=subject.classroom_id, student_id=user.id).first():
        raise HTTPException(status_code=403, detail="You are not enrolled in this classroom")
    return db.query(Assessment).filter(Assessment.subject_id == subject_id).all()


@router.post("/assessments/{assessment_id}/marks", status_code=status.HTTP_201_CREATED)
def record_mark(assessment_id: int, data: MarkCreateRequest, db: Session = Depends(get_db), teacher: User = Depends(require_roles("TEACHER"))):
    assessment = get_owned_assessment(assessment_id, teacher, db)
    if data.score > assessment.max_marks:
        raise HTTPException(status_code=400, detail="Score cannot be greater than maximum marks")
    if not db.query(ClassroomStudent).filter_by(classroom_id=assessment.subject.classroom_id, student_id=data.student_id).first():
        raise HTTPException(status_code=400, detail="Student is not enrolled in this classroom")
    mark = db.query(Mark).filter_by(assessment_id=assessment_id, student_id=data.student_id).first()
    if mark:
        mark.score = data.score
    else:
        mark = Mark(assessment_id=assessment_id, student_id=data.student_id, score=data.score)
        db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


@router.get("/assessments/{assessment_id}/marks")
def list_marks(assessment_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if user.role == "TEACHER":
        get_owned_assessment(assessment_id, user, db)
        return db.query(Mark).filter(Mark.assessment_id == assessment_id).all()
    mark = db.query(Mark).filter_by(assessment_id=assessment_id, student_id=user.id).first()
    return [mark] if mark else []
