from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.database.conn import Session
from contextlib import contextmanager

hashCode = "Hello_neighbor"
oauth2Schema = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")
tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users",
    },
    {
        "name": "media",
        "description": "Operations with media",
    }
]

app = FastAPI(
    title="Document for healthwatch API",
    version="1.0",
    license_info={
        "name": "GPL-2.0",
        "url": "https://opensource.org/license/gpl-2-0/",
    }, openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(SessionMiddleware, secret_key=hashCode)

@contextmanager
def sessionFix():
    """
    오퍼레이션 도중 세션 생성 발생 시 세션 변경
    """
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()