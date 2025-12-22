from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: str
    role: str = "student"
