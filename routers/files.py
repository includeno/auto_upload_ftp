# routers/files.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
#from models import FileRecord
from typing import List

router = APIRouter(prefix="/files", tags=["files"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.FileRecord])
def search_files(prefix: str = "", suffix: str = "", limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(schemas.FileRecord)
    if prefix:
        query = query.filter(schemas.FileRecord.path.startswith(prefix))
    if suffix:
        query = query.filter(schemas.FileRecord.path.endswith(suffix))
    files = query.limit(limit).all()
    return files
