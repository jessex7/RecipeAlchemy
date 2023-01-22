from fastapi import FastAPI

from .routers import recipes

app = FastAPI()
app.include_router(recipes.router)

@app.get("/")
async def read_root():
    return {"message": "Hello there!"}