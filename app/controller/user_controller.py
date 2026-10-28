from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_request import UserCreateRequest
from app.service.implementation.user_service_impl import UserServiceImpl
from app.auth import get_db, require_roles

router = APIRouter()

user_service = UserServiceImpl()

@router.post("/users")
def create_user(user: UserCreateRequest, db: Session = Depends(get_db), _=Depends(require_roles("TEACHER"))):
    if user_service.user_repo.find_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    return user_service.create_user(db, user)


@router.get("/users")
def get_users(db: Session = Depends(get_db), _=Depends(require_roles("TEACHER"))):
    return user_service.get_all_users(db)
