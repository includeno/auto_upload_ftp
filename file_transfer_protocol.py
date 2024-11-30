from abc import ABC, abstractmethod
from typing import List

class FileTransferProtocol(ABC):
    @abstractmethod
    def connect(self, host: str, username: str, password: str, port: int = 21):
        """连接到FTP或SFTP服务器"""
        pass

    @abstractmethod
    def upload(self, local_file: str, remote_file: str):
        """上传文件到远程服务器"""
        pass

    @abstractmethod
    def download(self, remote_file: str, local_file: str):
        """从远程服务器下载文件"""
        pass

    @abstractmethod
    def list_files(self, remote_dir: str) -> List[str]:
        """列出远程目录中的文件"""
        pass

    @abstractmethod
    def close(self):
        """关闭连接"""
        pass


