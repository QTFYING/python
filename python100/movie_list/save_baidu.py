import pandas as pd

# 读取Excel文件，文件名为movie_list.xlsx
df = pd.read_excel('movie_list.xlsx')

# 根据网盘类型进行分组
grouped_df = df.groupby('网盘类型')

# 创建字典，用于存储每个分组的HTML表格
html_dict = {}
for name, group in grouped_df:
    html_dict[name] = group.to_html()