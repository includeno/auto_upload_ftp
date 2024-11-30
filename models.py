# models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class SyncConfig(Base):
    __tablename__ = 'sync_configs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prefix = Column(String, nullable=True)
    suffix = Column(String, nullable=True)
    date_match = Column(DateTime, nullable=True)
    scan_directory = Column(String)
    subdirectory_levels = Column(Integer, default=0)
    skip_suffixes = Column(String, nullable=True)  # 逗号分隔的后缀列表
    enabled = Column(Boolean, default=True)

    tasks = relationship("SyncTask", back_populates="config")

class SyncTask(Base):
    __tablename__ = 'sync_tasks'

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="Pending")
    progress = Column(Float, default=0.0)
    config_id = Column(Integer, ForeignKey('sync_configs.id'))

    config = relationship("SyncConfig", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task")

class TaskLog(Base):
    __tablename__ = 'task_logs'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('sync_tasks.id'))
    timestamp = Column(DateTime)
    message = Column(Text)
    level = Column(String)

    task = relationship("SyncTask", back_populates="logs")

class FileRecord(Base):
    __tablename__ = 'file_records'

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    destination = Column(String)
    last_modified = Column(DateTime)
    last_uploaded = Column(DateTime, nullable=True)
    status = Column(String, default="Pending")
    config_id = Column(Integer, ForeignKey('sync_configs.id'))

class GlobalConfig(Base):
    __tablename__ = 'global_config'

    id = Column(Integer, primary_key=True, index=True)
    skip_suffixes = Column(String, nullable=True)  # 逗号分隔的后缀列表
