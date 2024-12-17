import pandas as pd
import openpyxl

# 加载Excel工作簿
file_path = 'movie_list_less.xlsx'
wb = openpyxl.load_workbook(file_path, data_only=False)  # data_only=False 以确保能够读取超链接对象
ws = wb.active

# 使用pandas读取Excel文件的电影名称（但不包括超链接）
# 假设电影名称在第一行第一列开始的区域，且第一行为标题行
df = pd.read_excel(file_path, usecols=[0], header=0, names=['电影名称'])

# 创建一个字典来存储电影名称和对应的网盘链接
movie_links = {}

# 遍历工作表中的每个单元格，检查超链接
for row in ws.iter_rows(min_row=2, values_only=False):  # values_only=False 以获取单元格对象
    movie_cell = row[0]  # 假设电影名称在第一列
    baidu_cell = row[1]  # 假设百度网盘链接在第二列
    kuake_cell = row[2]  # 假设夸克网盘链接在第三列
    xunlei_cell = row[3]  # 假设迅雷云盘链接在第四列

    movie_name = movie_cell.value  # 获取电影名称

    # 检查并提取超链接
    baidu_link = baidu_cell.hyperlink.target if baidu_cell.hyperlink else None
    kuake_link = kuake_cell.hyperlink.target if kuake_cell.hyperlink else None
    xunlei_link = xunlei_cell.hyperlink.target if xunlei_cell.hyperlink else None

    # 将电影名称和链接添加到字典中
    movie_links[movie_name] = {
        '百度网盘': baidu_link,
        '夸克网盘': kuake_link,
        '迅雷云盘': xunlei_link
    }

# 由于我们已经有了电影名称和链接的完整信息，现在不需要再使用pandas的DataFrame了
# 直接遍历字典，打印每部电影及其网盘链接
for movie, links in movie_links.items():
    print(f"电影名称: {movie}")
    if links['百度网盘']:
        print(f"百度网盘: {links['百度网盘']}")
    if links['夸克网盘']:
        print(f"夸克网盘: {links['夸克网盘']}")
    if links['迅雷云盘']:
        print(f"迅雷云盘: {links['迅雷云盘']}")
    print("-" * 40)