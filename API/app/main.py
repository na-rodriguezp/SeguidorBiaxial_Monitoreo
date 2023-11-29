from fastapi import FastAPI
from app import router

app = FastAPI()

@app.get("/")
async def Home():
    return "Welcome to the Solar Biaxial System Monitoring API of Uniandes"

app.include_router(router.router)