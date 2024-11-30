from protocols.FTP import FTPTransfer
from protocols.SFTP import SFTPTransfer
from file_transfer_protocol import FileTransferProtocol

class FileTransferFactory:
    @staticmethod
    def get_transfer_protocol(protocol: str) -> FileTransferProtocol:
        """
        根据协议类型返回相应的传输对象(FTP或SFTP)
        :param protocol: 协议类型，'ftp' 或 'sftp'
        :return: 对应的文件传输对象
        """
        if protocol == "ftp":
            return FTPTransfer()
        elif protocol == "sftp":
            return SFTPTransfer()
        else:
            raise ValueError("Unsupported protocol. Please choose 'ftp' or 'sftp'.")
