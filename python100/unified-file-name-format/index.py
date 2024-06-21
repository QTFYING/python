'''
批量修改mocks文件夹下，命名不规范的文件，统一为xx-xx-xx.xx格式
'''

import os
import re


def camel_to_snake(camel_str):
    # 将大驼峰命名转换为小写下划线命名，再转换为短横线命名
    snake_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    snake_str = re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_str).lower()
    return snake_str.replace("_", "-")

def is_already_formatted(filename):
    # 检查文件名是否已经是正确的 xx-xx-xx.xx 格式，或者以下划线开头
    base_name, extension = os.path.splitext(filename)
    parts = base_name.split('-')
    if filename.startswith('_'):
        return True
    if all(part.islower() for part in parts) and len(parts) >= 1:
        return True
    return False

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if not is_already_formatted(filename):
                base_name, extension = os.path.splitext(filename)
                new_base_name = camel_to_snake(base_name)
                new_filename = f"{new_base_name}{extension}"
                new_filepath = os.path.join(directory, new_filename)
                os.rename(filepath, new_filepath)

def process_directories(base_dir):
    for root, dirs, files in os.walk(base_dir):
        rename_files_in_directory(root)

if __name__ == "__main__":
    base_directory = "mocks"
    process_directories(base_directory)