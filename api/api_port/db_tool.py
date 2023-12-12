import pymysql as sql

class sql_tool:
    def __init__(self, password: str, db_name: str, table_name: str):
        """
        初始化
        password: mysql密码, db_name: 数据库名, table_name: 表名
        """
        self.conn = sql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd=password,
            charset="utf8",
            db=db_name,
        )

        self.cursor = self.conn.cursor()
        self.table_name = table_name

    def save(self):
        "保存当前变更"
        self.conn.commit()

    def insert(self, columns: list):
        "插入一列数据, 要求个数匹配"
        insert_content = ""
        for i in columns:
            if type(i) is str:
                i = sql.converters.escape_string(i)
            insert_content += f"'{i}',"
        insert_content = insert_content[:-1]  # delete last ','
        cmd = f"INSERT INTO {self.table_name} VALUES ({insert_content})"
        self.cursor.execute(cmd)

    def fetch_specific(self, item_name: str, item_content: str) -> tuple:
        """
        选中item_name字段下内容为item_content的记录
        返回二维tuple
        """
        item_name = sql.converters.escape_string(item_name)
        item_content = sql.converters.escape_string(item_content)
        cmd = f"SELECT * FROM {self.table_name} WHERE {item_name}='{item_content}'"
        self.cursor.execute(cmd)
        temp = self.cursor.fetchall()
        if temp is None:
            return ()
        else:
            return temp

    def fetch_all(self) -> tuple:
        """
        选中所有记录
        返回二维tuple
        """
        cmd = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(cmd)
        temp = self.cursor.fetchall()
        if temp is None:
            return ()
        else:
            return temp

    def setTable(self, table_name: str):
        "设置表名，即切换当前表"
        self.table_name = table_name

    def fetch_file(file_name):
        ''''''


if __name__ == "__main__":
    # for debug
    s = sql_tool("ADMINROOT", "testdb", "test_table")
    print(s.fetch_specific("ID", "2"))
    s.insert([4, "David", "D not D"])
    s.save()
    print(s.fetch_all())
