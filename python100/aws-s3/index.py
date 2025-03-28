

import boto3
import logging
from io import BytesIO
from werkzeug.datastructures import FileStorage

# 配置日志记录
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class S3Error(Exception):
    """自定义S3异常类"""
    pass

class S3Handle(object):
    """
    S3处理上传下载文件
    """

    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.service_name = "s3"
        self.bucket_name = bucket_name
        self.client = self.create_client()

    def create_client(self):
        """
        客户端创建
        :return: boto3 S3 客户端
        """
        return boto3.client(
            self.service_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url
        )

    def upload_file(self, file_path, key):
        """
        本地文件上传
        :param file_path: 本地文件路径-绝对
        :param key: S3 对象键
        :raises S3Error: 如果上传失败
        """
        try:
            self.client.upload_file(file_path, self.bucket_name, key)
        except Exception as e:
            logging.error(f"Failed to upload file {file_path} to key {key}: {e}")
            raise S3Error(f"Failed to upload file {file_path} to key {key}")

    def download_file(self, key, file_path):
        """
        下载文件
        :param key: S3 对象键
        :param file_path: 本地文件路径
        :raises S3Error: 如果下载失败
        """
        try:
            self.client.download_file(self.bucket_name, key, file_path)
        except Exception as e:
            logging.error(f"Failed to download file from key {key} to {file_path}: {e}")
            raise S3Error(f"Failed to download file from key {key} to {file_path}")

    def delete_file(self, key):
        """
        删除文件
        :param key: S3 对象键
        :raises S3Error: 如果删除失败
        """
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
        except Exception as e:
            logging.error(f"Failed to delete file with key {key}: {e}")
            raise S3Error(f"Failed to delete file with key {key}")

    def _upload_fileobj(self, fileobj, key):
        """
        上传文件流到S3的私有方法
        :param fileobj: 文件流对象
        :param key: S3 对象键
        :raises S3Error: 如果上传失败
        """
        try:
            self.client.upload_fileobj(fileobj, self.bucket_name, key)
        except Exception as e:
            logging.error(f"Failed to upload fileobj to key {key}: {e}")
            raise S3Error(f"Failed to upload fileobj to key {key}")

    def upload_file_buffer(self, file, key):
        """
        流文件上传
        :param file: 文件对象
        :param key: S3 对象键
        :raises S3Error: 如果上传失败
        """
        with BytesIO(file.read()) as data_stream:
            self._upload_fileobj(data_stream, key)

    def upload_file_buffer_with_name(self, file: FileStorage, key):
        """
        带文件名的流文件上传
        :param file: 文件对象
        :param key: S3 对象键（不含扩展名）
        :raises S3Error: 如果上传失败
        """
        filename = file.filename
        ends = filename.split(".")[-1]
        with BytesIO(file.read()) as data_stream:
            self._upload_fileobj(data_stream, f"{key}.{ends}")

    def download_file_buffer(self, key):
        """
        流下载文件
        :param key: S3 对象键
        :return: 文件内容字节串
        :raises S3Error: 如果下载失败
        """
        data_stream = BytesIO()
        try:
            self.client.download_fileobj(self.bucket_name, key, data_stream)
            return data_stream.getvalue()
        except Exception as e:
            logging.error(f"Failed to download file buffer from key {key}: {e}")
            raise S3Error(f"Failed to download file buffer from key {key}")