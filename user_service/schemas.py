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


class PathDataOrg(BaseModel):
    path: str
    op: str
    value: str


class Manager(BaseModel):
    email: str
    password: str
    role: int
    medcentreId: str
    firstName: str
    lastName: str
    phone: str
    avatarUrl: str
    status: str


class PathManager(BaseModel):
    patchUserDoc: list
    patchManagerDoc:list
