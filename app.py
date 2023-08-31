from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.service.middleware import *
from src.api.user import *
from src.api.media import *
from src.database.user.user import *
from src.api.nutri import *
from src.database.user.nutri import *

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
