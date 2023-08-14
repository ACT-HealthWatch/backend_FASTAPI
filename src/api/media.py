import random
import string
import os

from datetime import date
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status, UploadFile, File, Depends
from typing_extensions import Annotated

from src.database.user.user import *
from src.database.user.crud import *
from src.service.middleware import *
from src.service.hash import *

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

@app.post(
        "/api/v1/upload/test/image", description="영상 업로드 테스트",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["media"]
    )
async def image_test(file: UploadFile):
    DIR = "static/images/"
    try:
        content = await file.read()
        fileName = f"{file.filename}"

        with open(os.path.join(DIR, fileName), "wb") as fp:
            fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)
        
        # 경로 + 파일 반환
        return {
            "filename": fileName,
            "path": os.path.join(DIR, fileName)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post(
        "/api/v1/upload/video", description="영상 업로드",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["media"]
    )
async def video(file: UploadFile, sessionUID: Annotated[str, Depends(get_authenticated_user)]):
    DIR = "static/videos/"
    try:
        content = await file.read()
        user_id = sessionUID
        extension = os.path.splitext(file.filename)[-1]
        # 파일명 
        fileName = f"{user_id}_videos_{date.today().strftime('%Y%m%d')}{extension}"

        with open(os.path.join(DIR, fileName), "wb") as fp:
            fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)
        
        # 경로 + 파일 반환
        return JSONResponse(status_code=200, content={
            "filename": fileName,
            "path": os.path.join(DIR, fileName)
        })
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    
@app.post(
        "/api/v1/upload/image", description="이미지 업로드",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["media"]
    )
async def video(file: UploadFile, sessionUID: Annotated[str, Depends(get_authenticated_user)]):
    DIR = "static/images/"
    try:
        content = await file.read()
        user_id = sessionUID
        extension = os.path.splitext(file.filename)[-1]
        # 파일명 
        fileName = f"{user_id}_videos_{date.today().strftime('%Y%m%d')}{extension}"

        with open(os.path.join(DIR, fileName), "wb") as fp:
            fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)
        
        # 경로 + 파일 반환
        return JSONResponse(status_code=200, content={
            "filename": fileName,
            "path": os.path.join(DIR, fileName)
        })
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})