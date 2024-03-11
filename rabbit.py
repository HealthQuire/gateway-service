import aio_pika
import requests
from os import environ
from aio_pika.patterns import RPC
from functools import wraps
from fastapi import status, HTTPException, Header
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

if environ.get("AUTHORIZATION_URL") is None:
    load_dotenv()
CONNECTION_STR = environ.get("CONNECTION_STR")
AUTHORIZATION_URL = environ.get("AUTHORIZATION_URL")


async def _try_decode_token(access: str | None) -> int:
    if access is None:
        return 0
    res = requests.post(AUTHORIZATION_URL + "/decode_token", headers={"access-token": access})
    if res.status_code == status.HTTP_401_UNAUTHORIZED:
        return 0
    data = res.json()
    return data["user_role"]


async def _try_refresh_token(access: str | None, refresh: str | None):
    if access is None or refresh is None:
        return None, None
    res = requests.post(AUTHORIZATION_URL + "/refresh_token",
                        headers={"access-token": access, "refresh-token": refresh})
    if res.status_code == status.HTTP_401_UNAUTHORIZED:
        return None, None
    data = res.json()
    return data["access_token"], data["refresh_token"]


async def _try_get_tokens(email: str | None, password: str | None):
    if email is None or password is None:
        return None, None
    res = requests.post(AUTHORIZATION_URL + "/create_token",
                        headers={"login": email, "password": password})
    if res.status_code == status.HTTP_200_OK:
        data = res.json()
        return data["access_token"], data["refresh_token"]
    return None, None


async def _check_tokens(access: str | None, refresh: str | None, email: str | None,
                        password: str | None) -> tuple:
    role = await _try_decode_token(access)
    if role != 0:
        return role, access, refresh

    access_try, refresh_try = await _try_refresh_token(access, refresh)
    role = await _try_decode_token(access_try)
    if role != 0:
        return role, access_try, refresh_try

    access_try, refresh_try = await _try_get_tokens(email, password)
    return await _try_decode_token(access_try), access_try, refresh_try


async def send_request_to_queue(message: dict) -> tuple[dict, int]:
    print(CONNECTION_STR)
    connection = await aio_pika.connect_robust(CONNECTION_STR)

    async with connection:
        channel = await connection.channel()
        rpc = await RPC.create(channel)
        result, status_code = await rpc.proxy.resolve(**message)
        print(result, status_code)
        return result, status_code


def router(fastapi_router,
           method: str,
           path: str,
           status_code: int = status.HTTP_200_OK,
           json_data: list = None,
           role: int = 0):
    fastapi_router = fastapi_router(path, status_code=status_code)

    def wrapper(endpoint):
        @fastapi_router
        @wraps(endpoint)
        async def decorator(access_token: str | None = Header(default=None),
                            refresh_token: str | None = Header(default=None),
                            email: str | None = Header(default=None),
                            password: str | None = Header(default=None),
                            **kwargs):
            if path == "/user/register":
                role_check: int = kwargs["register"].dict()["role"] + 1
                if role_check == 2:
                    role_check = 0
            else:
                role_check = role

            if role_check != 0:
                user_role, new_access_token, new_refresh_token = await _check_tokens(access_token,
                                                                                     refresh_token,
                                                                                     email,
                                                                                     password)
                access_token = new_access_token
                refresh_token = new_refresh_token
                print(user_role)
                if user_role < role_check:
                    resp_code = status.HTTP_401_UNAUTHORIZED if user_role == 0 \
                        else status.HTTP_403_FORBIDDEN
                    if access_token is None:
                        access_token = ''
                    if refresh_token is None:
                        refresh_token = ''
                    return JSONResponse({"details": "Update token"},
                                        status_code=resp_code,
                                        headers={"access_token": access_token,
                                                 "refresh-token": refresh_token})

            message = {"method": method, "path": path}
            if json_data is not None:
                message["json_data"] = dict()
                for json_name in json_data:
                    for key, val in kwargs[json_name].dict().items():
                        message["json_data"][key] = val
            response_data, response_status_code = await send_request_to_queue(message)

            if response_status_code >= status.HTTP_400_BAD_REQUEST:
                raise HTTPException(
                    status_code=response_status_code, detail=response_data
                )
            if access_token is None:
                access_token = ''
            if refresh_token is None:
                refresh_token = ''
            resp_header = {"access-token": access_token,
                           "refresh_token": refresh_token}
            return JSONResponse(response_data, headers=resp_header)

    return wrapper


if __name__ == '__main__':
    print(_check_tokens(None, None, None, None))
