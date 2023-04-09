from fastapi import FastAPI

# import uvicorn
from game_query.routes import rawg

app = FastAPI()

app.include_router(router=rawg.router, prefix="/api")

@app.get("/")
def root_ping():
    return {"hello": "from vercel"}
