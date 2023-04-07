from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from ..lib.rawg import Rawg

router = APIRouter(prefix="/search")


@router.get("/")
def search(query: str):
    rawg = Rawg()
    return JSONResponse(
        rawg.games(query),
    )
