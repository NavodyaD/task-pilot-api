from pydantic import BaseModel, EmailStr

class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr