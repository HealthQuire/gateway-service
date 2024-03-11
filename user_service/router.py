from fastapi import APIRouter, Header

from rabbit import router
from user_service.schemas import Login, Register, Organization

user_router = APIRouter()


@router(fastapi_router=user_router.post, method="POST", path="/user/login", json_data=["login"])
async def login_user(login: Login,
                     access_token: str | None = Header(default=None),
                     refresh_token: str | None = Header(default=None),
                     email: str | None = Header(default=None),
                     password: str | None = Header(default=None)):
    pass


@router(fastapi_router=user_router.post, method="POST", path="/user/register",
        json_data=["register"])
async def register_user(register: Register,
                        access_token: str | None = Header(default=None),
                        refresh_token: str | None = Header(default=None),
                        email: str | None = Header(default=None),
                        password: str | None = Header(default=None)):
    pass


@router(fastapi_router=user_router.get, method="GET", path="/user/Organizations", role=1)
async def register_user(access_token: str | None = Header(default=None),
                        refresh_token: str | None = Header(default=None),
                        email: str | None = Header(default=None),
                        password: str | None = Header(default=None)):
    pass


@router(fastapi_router=user_router.get, method="GET", path="/user/Organizations/{id}", role=1,
        path_param="id")
async def register_user(id: str,
                        access_token: str | None = Header(default=None),
                        refresh_token: str | None = Header(default=None),
                        email: str | None = Header(default=None),
                        password: str | None = Header(default=None)):
    pass


@router(fastapi_router=user_router.post, method="POST", path="/user/Organizations", role=6,
        json_data=["organization"])
async def register_user(organization: Organization,
                        access_token: str | None = Header(default=None),
                        refresh_token: str | None = Header(default=None),
                        email: str | None = Header(default=None),
                        password: str | None = Header(default=None)):
    pass


@router(fastapi_router=user_router.delete, method="DELETE", path="/user/Organizations/{id}", role=6,
        path_param="id")
async def register_user(id: str,
                        access_token: str | None = Header(default=None),
                        refresh_token: str | None = Header(default=None),
                        email: str | None = Header(default=None),
                        password: str | None = Header(default=None)):
    pass
