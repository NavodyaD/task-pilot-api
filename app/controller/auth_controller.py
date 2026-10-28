from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, get_db, hash_password, verify_password
from app.models.user_model import User
from app.schemas.auth_request import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    role = data.role.upper()
    if role not in {"TEACHER", "STUDENT"}:
        raise HTTPException(status_code=400, detail="Role must be TEACHER or STUDENT")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": {"id": user.id, "name": user.name, "role": user.role}}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
