from fastapi import APIRouter, Depends, HTTPException, status, Header


router = APIRouter(prefix='/auth', tags=['Auth'])

token_to_username = {
    'qwerty': 'admin',
    'asdfgh': 'user',
}


def get_username(
        static_token: str = Header(alias='x-auth-token')
) -> str:
    if username := token_to_username.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token'
    )


@router.get('/header/')
def header(
        username: str = Depends(get_username)
):
    return {
        'message': f'Hi {username}'
    }
