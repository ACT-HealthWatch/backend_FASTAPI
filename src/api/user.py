from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

from src.database.user.user import *
from src.database.user.crud import *
from src.service.middleware import *

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
    
@app.get("/api/v1/user/list", description="유저 리스트", status_code=status.HTTP_200_OK, tags=["user"])
async def login(id: str, pw: str):
    try:
        with sessionFix() as session:
            result = UserCommands().read(session, UserTable, id, pw)
            if result == None:
                raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")
            return result
    except Exception as e:
        return {"message": str(e)}