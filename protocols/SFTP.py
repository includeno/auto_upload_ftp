import paramiko
from file_transfer_protocol import FileTransferProtocol
from typing import List

class SFTPTransfer(FileTransferProtocol):
    def __init__(self):
        self.sftp = None
        self.client = None

    def connect(self, host: str, username: str, password: str, port: int = 22):
        """连接到 SFTP 服务器"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=username, password=password, port=port)
        self.sftp = self.client.open_sftp()
        print(f"Connected to SFTP server {host}:{port}")

    def upload(self, local_file: str, remote_file: str):
        """上传文件到 SFTP 服务器"""
        self.sftp.put(local_file, remote_file)
        print(f"Uploaded {local_file} to {remote_file}")

    def download(self, remote_file: str, local_file: str):
        """从 SFTP 下载文件"""
        self.sftp.get(remote_file, local_file)
        print(f"Downloaded {remote_file} to {local_file}")

    def list_files(self, remote_dir: str) -> List[str]:
        """列出 SFTP 服务器上的文件"""
        return self.sftp.listdir(remote_dir)

    def close(self):
        """关闭 SFTP 连接"""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        print("SFTP connection closed")
