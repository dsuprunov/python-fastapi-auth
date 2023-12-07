import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = APIRouter(prefix='/auth', tags=['Auth'])

security = HTTPBasic()

usernames_to_passwords = {
    'admin': 'admin',
    'user': 'user',
    'john': 'password',
}


def get_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    exc_unauthed = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid user name or password',
        headers={'WWW-Authenticate': 'Basic'}
    )
    if credentials.username not in usernames_to_passwords:
        raise exc_unauthed

    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        usernames_to_passwords.get(credentials.username, '').encode('utf-8')
    ):
        raise exc_unauthed

    return credentials.username


@router.get('/basic/')
def basic(
        auth_username: str = Depends(get_username)
):
    return {
        'message': f'Hi {auth_username}'
    }
