from pydantic import BaseModel
import redis

from passlib.hash import oracle10
from datetime import datetime, timedelta, timezone
from typing import Union
from typing_extensions import Annotated
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from src.service.middleware import *
from src.database.user.user import *
from src.database.user.crud import *

secret_key = os.environ.get("SECRET_KEY")
hashCode = "Hello_neighbor"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


class TokenData(BaseModel):
    access_token: str
    token_type: str


class UserToken(BaseModel):
    username: Union[str, None] = None
    access_token: Union[str, None] = None


class SessionManager():
    @staticmethod
    def create_user_session(user_id: str, token: str):
        try:
            redisController.set(user_id, token)
        except Exception as e:
            print(e)

    @staticmethod
    def delete_user_session(user_id: str):
        try:
            redisController.delete(user_id)
        except Exception as e:
            print(e)

    @staticmethod
    def get_user_session(user_id: str):
        data = redisController.get(user_id)
        print(data)
        if data is None:
            return None
        return data.decode('utf-8')


class hashData():
    @staticmethod
    def verify_password(plain, hashed):
        return oracle10.verify(hashCode, hashed, plain)

    @staticmethod
    def get_password_hash(password):
        return oracle10.hash(hashCode, password)

    @staticmethod
    def create_user_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            # timezone seoul
            expire = datetime.now(timezone(timedelta(hours=9))) + expires_delta
        else:
            expire = datetime.now(
                timezone(timedelta(hours=9))) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: Annotated[str, Depends(oauth2Schema)]):
        with sessionFix() as session:
            credentialsException = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
                user_id: str = payload.get("sub")
                if user_id is None:
                    raise credentialsException
                token_data = UserToken(username=user_id, access_token=token)
            except JWTError:
                print('JWTError')
                raise credentialsException

            user = UserCommands().read(session, UserTable, id=user_id)
            if user is None:
                print('2')
                raise credentialsException
            return token_data


async def get_authenticated_user(token: Annotated[UserToken, Depends(hashData().verify_token)]):
    user_id = token.username
    stored_token = SessionManager.get_user_session(user_id)

    if stored_token is None:
        print('3')
        return {
            "message": "token is not valid"
        }
    return user_id
