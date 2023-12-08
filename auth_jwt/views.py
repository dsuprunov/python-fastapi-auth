from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

import auth_jwt.auth_utils as auth_utils
from auth_jwt.user import User, users_db
from auth_jwt.token import Token


http_bearer = HTTPBearer()


router = APIRouter(prefix='/jwt', tags=['JWT'])


def validate_auth_user(
        username: str = Form(),
        password: str = Form()
):
    exc_unauthed = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid user name or password'
    )

    if not (user := users_db.get(username)):
        raise exc_unauthed

    if not auth_utils.validate_password(password, user.password):
        raise exc_unauthed

    return user


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    try:
        payload = auth_utils.jwt_decode(
            token=token
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

    return payload


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
) -> User:
    username: str | None = payload.get('sub')
    if user := users_db.get(username):
        return user

    # ToDo in real world remove 'user not found'
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token (user not found)',
    )


def get_current_active_auth_user(
        user: User = Depends(get_current_auth_user)
) -> User:
    return user


@router.post('/login/', response_model=Token)
def login(
        user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
    }
    token = auth_utils.jwt_encode(jwt_payload)
    return Token(
        access_token=token,
        token_type='Bearer',
    )


@router.get('/check/')
def check(
        user: User = Depends(get_current_active_auth_user)
):
    return {
        'username': user.username,
    }
