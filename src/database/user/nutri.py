from pydantic import BaseModel
from sqlalchemy import Column, String, inspect, INTEGER, DateTime
from datetime import datetime
import pytz

from src.database.conn import *


class nutriTable(Base):  # 유저 테이블
    __tablename__ = 'nutrient'  # 테이블 이름
    user_id = Column(String(50), nullable=False)  # 아이디
    kcal = Column(INTEGER, nullable=False)  # 칼로리
    carbohydrate = Column(INTEGER, nullable=False)  # 탄수화물
    protein = Column(INTEGER, nullable=False)  # 단백질
    fat = Column(INTEGER, nullable=False)  # 지방
    generated_time = Column(DateTime, primary_key=True, default=datetime.now(
        pytz.timezone('Asia/Seoul')))  # 생성시간


class nutriData(BaseModel):  # 유저
    kcal: int
    carbohydrate: int
    protein: int
    fat: int


inspector = inspect(conn.engineData())
if not inspector.has_table('nutrient'):
    nutriTable.__table__.create(bind=conn.engineData())
