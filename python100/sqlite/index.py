import sqlite3
from datetime import datetime

# 1.连接数据库（如果数据库文件不存在，则会自动创建一个）
conn = sqlite3.connect('/Users/mayapeng/SQLite/my_sqlite.db')

#2. 创建一个游标对象，用于执行SQL语句
cursor = conn.cursor()

# 删除已有的users表（如果存在）
cursor.execute("DROP TABLE IF EXISTS USERS")
cursor.execute("""
CREATE TABLE USERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

#3. 使用for循环插入100,000条数据
current_timestamp_start = datetime.now()
print("开始时间:", current_timestamp_start)

for i in range(100):
  # 生成用户名，例如：User_1, User_2, ...User_100000
    name = f"User_{i+1}"
    age = i % 100 + 1
    cursor.execute("INSERT INTO USERS(name, age) values(?, ?)", (name, age))

    # 每插入10条记录后提交一次，避免过多数据积累在内存中
    if (i + 1) % 10 == 0:
        conn.commit()

current_timestamp_end = datetime.now()
print("结束时间:", current_timestamp_end)
print("耗时时间:", current_timestamp_end - current_timestamp_start)


# 4. 关闭游标和链接
cursor.close()
conn.close()