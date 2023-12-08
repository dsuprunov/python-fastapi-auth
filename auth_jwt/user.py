from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
)

import auth_jwt.auth_utils as auth_utils


class User(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes


users_db: dict[str, User] = {
    'admin': User(username='admin', password=auth_utils.hash_password('qwerty')),
    'user': User(username='user', password=auth_utils.hash_password('qwerty')),
}
