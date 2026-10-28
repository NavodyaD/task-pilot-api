from pydantic import BaseModel, Field


class ClassroomCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)


class EnrolStudentRequest(BaseModel):
    student_id: int = Field(gt=0)


class SubjectCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class AssessmentCreateRequest(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    assessment_type: str = Field(min_length=2, max_length=50)
    max_marks: float = Field(gt=0)


class MarkCreateRequest(BaseModel):
    student_id: int = Field(gt=0)
    score: float = Field(ge=0)
