from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    email: str
    role: int
    phone: str
    avatarUrl: str
    status: str


class Register(BaseModel):
    email: str
    password: str
    role: int
    phone: str
    avatarUrl: str
    status: str


class Organization(BaseModel):
    ownerId: str
    name: str
    status: str
