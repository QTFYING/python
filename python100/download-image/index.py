import os
import requests
from PIL import Image


def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        if os.path.getsize(save_path) > 0:  # 检查文件是否为空
            try:
                image = Image.open(save_path)
                width, height = image.size
                file_size = len(response.content)
                print(f"图片分辨率为：{width}x{height}")
                print(f"图片体积大小为：{file_size} 字节")
            except Exception as e:
                print(f"打开图片时出错: {e}")
        else:
            print("文件为空或未下载正确")
    else:
        print(f"请求失败，状态码: {response.status_code}")


url = 'https://p6-passport.byteacctimg.com/img/user-avatar/f4812c3351ed4e02775a671dda83168b~180x180.awebp'
save_path = './image.jpg'  # 你可以修改保存的文件名和路径

download_image(url, save_path)
