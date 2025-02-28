import requests
from bs4 import BeautifulSoup
import csv

 # 定义请求的 URL 和 headers
url = "https://movie.douban.com/top250"
headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # 设置编码方式
html_content = response.text  # 获取网页的 HTML 内容
print("网页内容加载成功！")

soup = BeautifulSoup(html_content, 'html.parser')
# 提取电影名称、描述、评分和评价人数
movies = []

for item in soup.find_all('div', class_='item'):
    title = item.find('span', class_='title').get_text()  # 电影名称
    description = item.find('span', class_='inq')  # 电影描述
    rating = item.find('span', class_='rating_num').get_text()  # 评分
    votes = item.find('div', class_='star').find_all('span')[3].get_text()  # 评价人数
    # 如果没有描述，将其置为空字符串
    if description:
       description = description.get_text()
    else:
        description = ''

    movie = {
        "title": title,
        "description": description,
        "rating": rating,
        "votes": votes.replace('人评价', '').strip()
    }

    movies.append(movie)

print("数据提取成功", movies)

# 将数据保存到 CSV 文件
with open('douban_top250.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'description', 'rating', 'votes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for movie in movies:
        writer.writerow(movie)

print("数据保存成功")


