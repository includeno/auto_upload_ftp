# schemas.py

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class SyncConfigBase(BaseModel):
    name: str
    scan_directory: str
    subdirectory_levels: int = 0
    enabled: bool = True
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    date_match: Optional[datetime] = None
    skip_suffixes: Optional[str] = None

class SyncConfigCreate(SyncConfigBase):
    pass

class SyncConfig(SyncConfigBase):
    id: int

    class Config:
        from_attributes = True

class SyncTaskBase(BaseModel):
    config_id: int

class SyncTaskCreate(SyncTaskBase):
    pass

class SyncTask(SyncTaskBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    progress: float

    class Config:
        from_attributes = True

class FileRecord(BaseModel):
    id: int
    path: str
    destination: str
    last_modified: datetime
    last_uploaded: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True
