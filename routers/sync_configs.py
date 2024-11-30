# routers/sync_configs.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SyncConfig
from schemas import SyncConfigCreate, SyncConfig
from typing import Optional, List

router = APIRouter(prefix="/configs", tags=["sync_configs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SyncConfig)
def create_sync_config(config: SyncConfigCreate, db: Session = Depends(get_db)):
    db_config = SyncConfig(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.get("/", response_model=List[SyncConfig])
def read_sync_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    configs = db.query(SyncConfig).offset(skip).limit(limit).all()
    return configs
