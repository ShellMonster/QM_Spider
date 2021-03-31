"""
@FileName：pymysql_py.py\n
@Description：\n
@Author：道长\n
@Time：2021/3/26 16:01\n
@Department：运营部\n
@Website：www.geekaso.com.com\n
@Copyright：©2019-2021 七麦数据
"""
import pymysql

# 连接MYSQL数据库
class Login_SQL:
    def __init__(self, host, user, passowrd, db, port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.password = passowrd
        self.db = db
        self.port = port
        self.charset = charset

    def login_mysql(self):
        """
            * 使用pymysql方法连接数据库；
        """
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, charset=self.charset)
        print('连接 %s 地址的 %s 数据库成功' %(self.host, self.db))
        conn = db.cursor()  # 获取指针以操作数据库
        conn.execute('set names utf8')
        return db

    def login_mongdb(self):
        """
            * 尚未写完；
        """
        pass