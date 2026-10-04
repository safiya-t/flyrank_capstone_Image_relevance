from fastapi import FastAPI

from src.api import router

app = FastAPI(title="FlyRank API")
app.include_router(router)
