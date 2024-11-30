from ftplib import FTP
from file_transfer_protocol import FileTransferProtocol
from typing import List

class FTPTransfer(FileTransferProtocol):
    def __init__(self):
        self.ftp = None

    def connect(self, host: str, username: str, password: str, port: int = 21):
        """连接到 FTP 服务器"""
        self.ftp = FTP()
        self.ftp.connect(host, port)
        self.ftp.login(username, password)
        print(f"Connected to FTP server {host}:{port}")

    def upload(self, local_file: str, remote_file: str):
        """上传文件到 FTP 服务器"""
        with open(local_file, "rb") as f:
            self.ftp.storbinary(f"STOR {remote_file}", f)
        print(f"Uploaded {local_file} to {remote_file}")

    def download(self, remote_file: str, local_file: str):
        """从 FTP 下载文件"""
        with open(local_file, "wb") as f:
            self.ftp.retrbinary(f"RETR {remote_file}", f.write)
        print(f"Downloaded {remote_file} to {local_file}")

    def list_files(self, remote_dir: str) -> List[str]:
        """列出 FTP 服务器上的文件"""
        return self.ftp.nlst(remote_dir)

    def close(self):
        """关闭 FTP 连接"""
        if self.ftp:
            self.ftp.quit()
            print("FTP connection closed")
