"""
boto3==1.28.78
Werkzeug==2.1.2
"""

import boto3
import traceback
from io import BytesIO
from werkzeug.datastructures import FileStorage

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
        :return:
        """
        client = boto3.client(
            self.service_name,
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            endpoint_url = self.endpoint_url,
        )

        return client

    def upload_file(self, file_path,key):
        """
        本地文件上传
        :param file_path: 本地文件路径-绝对
        :param key: key
        :return: 对象key
        """
        try:
            self.client.upload_file(file_path, self.bucket_name, key)
            return True, key
        except Exception as e:
            print(traceback.format_exc())
            return False, None

    def download_file(self, key, file_path):
        """
        下载文件
        :param key: 对象key
        :param file_path: 文件路径
        :return:
        """
        try:
            self.client.download_file(self.bucket_name, key, file_path)
            return True
        except Exception as e:
            print(traceback.format_exc())
            return False

    def delete_file(self, key):
        """
        删除文件
        :param key: 对象 key
        :return:
        """
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            return True, key
        except Exception as e:
            print(traceback.format_exc())
            return False, None

    def upload_file_buffer(self, file, key):
        """
        流文件上传
        :param file: 文件
        :param key: key
        :return: 对象key
        """
        try:
            data_stream = BytesIO(file.read())
            # 上传流文件到S3存储桶
            self.client.upload_fileobj(data_stream, self.bucket_name, key)
            return True, key
        except Exception as e:
            print(traceback.format_exc())
            return False, None

    def upload_file_buffer_with_name(self, file: FileStorage, key):
        """
        流文件上传
        :param file: 文件
        :param key: key
        :return: 对象key
        """
        try:
            filename = file.filename
            ends = filename.split(".")[-1]
            data_stream = BytesIO(file.read())
            # 上传流文件到S3存储桶
            self.client.upload_fileobj(data_stream, self.bucket_name, f"{key}.{ends}")
            return True, f"{key}.{ends}"
        except Exception as e:
            print(traceback.format_exc())
            return False, None

    def download_file_buffer(self, key):
        """
        流下载文件
        :param key: 对象key
        :return: 文件流
        """
        try:
            # 创建一个BytesIO流对象来保存下载的数据
            data_stream = BytesIO()
            # 下载S3对象到流文件
            self.client.download_fileobj(self.bucket_name, key, data_stream)
            # 将流文件的内容读取到一个变量中
            downloaded_data = data_stream.getvalue()
            return True, downloaded_data
        except Exception as e:
            print(traceback.format_exc())
            return False, None