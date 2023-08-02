from fastapi.responses import JSONResponse
from fastapi import HTTPException, status, UploadFile, File

from src.database.user.user import *
from src.database.user.crud import *
from src.service.middleware import *

@app.post(
        "/api/v1/upload/video", description="영상 업로드",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["media"]
    )
async def video(in_files: List[UploadFile] = File(...)):
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
    
@app.post(
        "/api/v1/upload/image", description="이미지 업로드",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def image(user: User):
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