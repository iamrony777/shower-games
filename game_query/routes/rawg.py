from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from ..lib.rawg import Rawg

router = APIRouter(prefix="/rawg")


@router.get("/")
def return_result(query: str):
    rawg = Rawg()
    return JSONResponse(
        rawg.games(query),
    )
