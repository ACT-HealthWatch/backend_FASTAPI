from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database.conn import Session
from contextlib import contextmanager

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users",
    }
]

app = FastAPI(
    title="Document for healthwatch API",
    version="1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }, openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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