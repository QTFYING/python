import pandas as pd

# 读取文件
df = pd.read_csv('city_list.csv')

# 按照city进行分组，并按照date升序排列
new_df = df.sort_values(['date']).groupby('city')

# 取出结果中的每一行拼接成新的dataframe
data_list = [pd.DataFrame(row) for head, row in new_df]
res_df = pd.concat(data_list)

print(res_df)

# 自定义city排序
res_df['city'] = pd.Categorical(df['city'], ["广宁", "广州", "南京", "杭州", "北京", "上海"])
res = res_df.sort_values('city')
print(res)