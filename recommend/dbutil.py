#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import logging
class _MySQL(object):   
    def __init__(self, Host, Port, User, Passwd, Db,Charset='utf8'): 
        self.conn = MySQLdb.connect(
                host = Host,#连接MYSQL地址  
                port = Port,#端口
                user = User,#用户 
                passwd = Passwd,#密码
                db = Db,#数据库名 
                charset = Charset)#设置编码
    def get_cursor(self):
        return self.conn.cursor()
    
    def query(self, sql):
        cursor = self.get_cursor()  
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()  
        except Exception, e:
            logging.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return result
    def execute(self, sql, param=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            affected_row = cursor.rowcount
        except Exception, e:
            logging.error("mysql execute error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_row  
    
    def executemany(self, sql, params=None):
        cursor = self.get_cursor()
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
            affected_rows = cursor.rowcount
        except Exception, e:
            logging.error("mysql executemany error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_rows
    
    def close(self):
        try:
            self.conn.close()
        except:
            pass
    def __del__(self):
        self.close()   # 对象销毁时自动调用

#test  
if __name__=="__main__debug": 
    conn=_MySQL('localhost',3306,'root','123456','jol') 
    sql="select max(problem_id) from problem;"
    cnt=conn.query(sql);
    print cnt
    conn.close()
