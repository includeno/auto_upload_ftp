# routers/sync_tasks.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SyncTask
from schemas import SyncTask, SyncTaskCreate
from typing import List
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["sync_tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SyncTask)
def create_sync_task(task: SyncTaskCreate, db: Session = Depends(get_db)):
    db_task = SyncTask(**task.dict(), start_time=datetime.now(datetime.timezone.utc))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[SyncTask])
def read_sync_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(SyncTask).offset(skip).limit(limit).all()
    return tasks
