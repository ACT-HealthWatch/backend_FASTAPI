import json

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status, Depends
from typing_extensions import Annotated

from src.database.user.user import *
from src.database.user.crud import *

from src.database.user.nutri import *
from src.database.user.crud_nutri import *

from src.service.middleware import *
from src.service.hash import *


@app.get(
    "/api/v1/user/nutrient/all", description="유저별 영양소 조회",
    response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"}
    }, tags=["nutrient"]
)
async def nutirentAll(sessionUID: Annotated[str, Depends(get_authenticated_user)]):
    with sessionFix() as session:
        result = NutriCommands().read(session, nutriTable, user_id=sessionUID)
        return result


@app.get(
    "/api/v1/user/nutrient/weekly", description="유저별 주간 영양소 조회",
    response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"}
    }, tags=["nutrient"]
)
async def nutirentWeekly(sessionUID: Annotated[str, Depends(get_authenticated_user)]):
    with sessionFix() as session:
        results = NutriCommands().read(session, nutriTable,
                                       user_id=sessionUID, generated_time=7)
        json_results = [
            {
                'date': result.date.isoformat(),
                'total_kcal': float(result.total_kcal),
                'total_carbs': float(result.total_carbs),
                'total_protein': float(result.total_protein),
                'total_fat': float(result.total_fat)
            }
            for result in results
        ]

        return JSONResponse(content=json_results)


@app.post(
    "/api/v1/user/nutrient/add", description="해당 시간의 영양소 데이터 추가",
    status_code=status.HTTP_200_OK, response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"}
    }, tags=["nutrient"]
)
async def create(data: nutriData, sessionUID: Annotated[str, Depends(get_authenticated_user)]):
    try:
        with sessionFix() as session:
            newData = nutriTable(
                user_id=sessionUID,
                kcal=data.kcal,
                carbohydrate=data.carbohydrate,
                protein=data.protein,
                fat=data.fat,
            )
            result = NutriCommands().create(session, newData)
            return {"message": result}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
