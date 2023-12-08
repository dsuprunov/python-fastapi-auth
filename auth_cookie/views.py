import uuid
from typing import Any
from time import time
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie


router = APIRouter(prefix='/cookie', tags=['Cookie'])

header_to_username = {
    'qwerty': 'admin',
    'asdfgh': 'user'
}

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'web-app-session-id'


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    return COOKIES[session_id]


def get_username(
        static_token: str = Header(alias='x-auth-token')
) -> str:
    if username := header_to_username.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token'
    )


@router.post('/login/')
def set_cookie(
        response: Response,
        username: str = Depends(get_username)
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)

    return {
        'result': 'ok'
    }

@router.get('/check/')
def check_cookie(
        user_session_data: dict = Depends(get_session_data)
):
    return {
        'message': f"Hello {user_session_data['username']}",
        **user_session_data
    }


@router.get('/logout/')
def del_cookie(
        response: Response,
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
        user_session_data: dict = Depends(get_session_data)
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)

    return {
        'message': f"Bye {user_session_data['username']}"
    }
