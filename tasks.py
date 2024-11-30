# tasks.py

import threading
import time
from database import SessionLocal
from models import SyncConfig, SyncTask, FileRecord, TaskLog, GlobalConfig
from datetime import datetime
import os

def scheduler():
    while True:
        db = SessionLocal()
        configs = db.query(SyncConfig).filter(SyncConfig.enabled == True).all()
        for config in configs:
            threading.Thread(target=run_sync_task, args=(config.id,)).start()
        db.close()
        time.sleep(60)  # 每隔60秒检查一次

def run_sync_task(config_id: int):
    db = SessionLocal()
    config = db.query(SyncConfig).get(config_id)
    task = SyncTask(
        start_time=datetime.utcnow(),
        status="Running",
        progress=0.0,
        config_id=config_id
    )
    db.add(task)
    db.commit()
    try:
        files = scan_files(config)
        total_files = len(files)
        for idx, file_path in enumerate(files):
            # 上传文件
            upload_file(file_path, config)
            task.progress = (idx + 1) / total_files * 100
            db.commit()
        task.status = "Completed"
    except Exception as e:
        task.status = "Failed"
        log = TaskLog(
            task_id=task.id,
            timestamp=datetime.utcnow(),
            message=str(e),
            level="ERROR"
        )
        db.add(log)
    finally:
        task.end_time = datetime.utcnow()
        db.commit()
        db.close()

def scan_files(config: SyncConfig):
    matched_files = []

    skip_suffixes_global = get_global_skip_suffixes()
    skip_suffixes_config = config.skip_suffixes.split(',') if config.skip_suffixes else []

    def should_skip(file_name):
        suffix = os.path.splitext(file_name)[1]
        if suffix in skip_suffixes_config:
            return True
        if suffix in skip_suffixes_global:
            return True
        return False

    for root, dirs, files in os.walk(config.scan_directory):
        depth = root[len(config.scan_directory):].count(os.sep)
        if depth > config.subdirectory_levels:
            continue
        for file_name in files:
            if should_skip(file_name):
                continue
            if config.prefix and not file_name.startswith(config.prefix):
                continue
            if config.suffix and not file_name.endswith(config.suffix):
                continue
            file_path = os.path.join(root, file_name)
            if config.date_match:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < config.date_match:
                    continue
            matched_files.append(file_path)
    return matched_files

def upload_file(file_path: str, config: SyncConfig):
    # 调用 ftp_uploader.py 中的上传函数
    pass

def get_global_skip_suffixes():
    db = SessionLocal()
    global_config = db.query(GlobalConfig).first()
    db.close()
    if global_config and global_config.skip_suffixes:
        return global_config.skip_suffixes.split(',')
    else:
        return []
