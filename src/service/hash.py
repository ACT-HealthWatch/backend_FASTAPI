from os import urandom
from pydantic import BaseModel

from passlib.hash import oracle10
from datetime import datetime, timedelta, timezone
from typing import Union
from typing_extensions import Annotated
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status, JSONResponse
from src.service.middleware import *
from src.database.user.user import *
from src.database.user.crud import *

secret_key = urandom(32)
hashCode = "Hello_neighbor"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class TokenData(BaseModel):
    access_token: str
    token_type: str

class UserToken(BaseModel):
    username: Union[str, None] = None
    is_valid: Union[bool, None] = True

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
            expire = datetime.now(timezone(timedelta(hours=9))) + timedelta(minutes=15)
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
                token_data = UserToken(username=user_id)
            except JWTError:
                raise credentialsException
            
            user = UserCommands().read(session, UserTable, id=user_id)
            if user is None:
                raise credentialsException
            return token_data
        
async def getCurrentUser(
        token: Annotated[User, Depends(hashData().verify_token)]
    ):
    if token.is_valid:
        return token
    else:
        return JSONResponse(status_code=400, content={"message": "invalid credentials"})