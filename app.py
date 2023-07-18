from fastapi.responses import RedirectResponse

from src.api.user import *
from src.database.user.user import *

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")