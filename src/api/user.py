from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends
from typing_extensions import Annotated

from src.database.user.user import *
from src.database.user.crud import *
from src.service.middleware import *
from src.service.hash import *

@app.post(
        "/api/v1/user/register", description="유저 등록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def create(user: User):
    try:
        with sessionFix() as session:
            new_user = UserTable(
                user_name=user.user_name,
                user_id=user.user_id,
                user_pw=user.user_pw,
            )
            result = UserCommands().create(session, new_user)
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/v1/user/login", description="유저 로그인", status_code=status.HTTP_200_OK, tags=["user"])
async def login(id: str, pw: str):
    try:
        with sessionFix() as session:
            result = UserCommands().read(session, UserTable, id, pw)
            if result == None:
                raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")
            return result
    except Exception as e:
        return {"message": str(e)}
    
@app.post(
        "/api/v1/user/token", description="유저 토큰 조회",
        tags=["user"]
    )
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        with sessionFix() as session:
            user = UserCommands().read(session, UserTable, id=form_data.username)
            if user is None:
                return {"message": "유저가 존재하지 않습니다."}
            isUser = hashData.verify_password(form_data.password, user.user_pw)
            if isUser:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = hashData.create_user_token(
                    data={"sub": user.user_id}, expires_delta=access_token_expires
                )
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                return {"message": "비밀번호가 일치하지 않습니다."}
    except Exception:
        return {"message": "로그인에 실패했습니다."}