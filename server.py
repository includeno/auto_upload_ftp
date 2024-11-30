# main.py

from fastapi import FastAPI
from database import engine
from models import Base
from routers import sync_configs, sync_tasks, files
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(sync_configs.router)
app.include_router(sync_tasks.router)
app.include_router(files.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
