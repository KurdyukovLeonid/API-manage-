from fastapi import FastAPI
from fastapi.routing import APIRouter
from routers.task import router as task_router
from routers.user import router as user_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task_router)
app.include_router(user_router)