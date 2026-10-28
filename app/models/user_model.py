from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="STUDENT")

    classrooms_taught = relationship("Classroom", back_populates="teacher", foreign_keys="Classroom.teacher_id")
    enrolled_classrooms = relationship("ClassroomStudent", back_populates="student", cascade="all, delete-orphan")
    marks = relationship("Mark", back_populates="student", cascade="all, delete-orphan")
