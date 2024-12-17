import json
import pyodbc

def import_json_to_access(json_file_path, db_path):
    """将 JSON 文件导入 Access 数据库。

    Args:
        json_file_path: JSON 文件路径。
        db_path: Access 数据库文件路径。
    """

    try:
        # 连接 Access 数据库
        conn_str = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=" + db_path
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 创建 movies 表 (如果不存在)
        try:
            cursor.execute("""
                CREATE TABLE movies (
                    电影名称 TEXT(255) PRIMARY KEY,
                    百度网盘地址 TEXT(255),
                    夸克网盘地址 TEXT(255),
                    迅雷云盘地址 TEXT(255)
                )
            """)
            conn.commit()
            print("Table 'movies' created successfully.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == 'HY000':
                print("Table 'movies' already exists.")
            else:
                print(f"Error creating table: {ex}")
                return # 创建表失败直接返回，避免后续错误

        # 读取 JSON 文件
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: JSON file not found at {json_file_path}")
            return # 文件未找到直接返回
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {json_file_path}")
            return # json格式错误返回

        # 插入数据
        for movie_name, links in data.items():
            baidu_link = links.get("百度网盘")
            quark_link = links.get("夸克网盘")
            xunlei_link = links.get("迅雷云盘")

            try:
                cursor.execute(
                    "INSERT INTO movies (电影名称, 百度网盘地址, 夸克网盘地址, 迅雷云盘地址) VALUES (?, ?, ?, ?)",
                    movie_name, baidu_link, quark_link, xunlei_link
                )
                conn.commit()
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                if sqlstate == '23000':
                    print(f"发现重复数据，跳过插入: {movie_name}")
                else:
                    print(f"Error inserting data for {movie_name}: {ex}")
                    conn.rollback() # 插入失败回滚事务
        print("Data import complete.")

    except pyodbc.Error as ex:
        print(f"Database connection error: {ex}")
    except Exception as e:
        print(f"其他错误：{e}")
    finally:
        if conn:
            conn.close()


# 使用示例
json_file = "movie_list.json"  # JSON 文件路径
db_file = r"D:\T590\Documents\Access\movie_list.accdb"  # Access 数据库文件路径，请替换成你实际的路径
import_json_to_access(json_file, db_file)