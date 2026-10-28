from fastapi import FastAPI
from app.config.database import engine, Base

# Import models
from app.models.user_model import User
from app.models.classroom_model import Classroom, ClassroomStudent
from app.models.academic_model import Subject, Assessment, Mark

# Import controllers
from app.controller.user_controller import router as user_router
from app.controller.auth_controller import router as auth_router
from app.controller.classroom_controller import router as classroom_router
from app.controller.academic_controller import router as academic_router

app = FastAPI(title="Classroom Management API", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

# register routes
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(classroom_router)
app.include_router(academic_router)

@app.get("/")
def home():
    return {"message": "FastAPI running successfully"}
