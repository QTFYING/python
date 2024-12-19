import requests
from bs4 import BeautifulSoup
def scrape_data(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设置正确的编码

    soup = BeautifulSoup(response.text, 'html.parser')
    # 从网站提取相关数据的代码在此处
    return soup

# 使用示例
url = 'http://47.116.193.173:9156'
soup = scrape_data(url)
print(soup.prettify())