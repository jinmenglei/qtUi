import sqlite3
from third_party.config import get_value_by_key
import os


class DataBase(object):
    def __init__(self, database_name='u_database.db'):
        database_path = get_value_by_key('database', 'DATA_PATH')
        print('Database get path: ' + str(database_path))
        if database_path is None:
            database_path = os.path.curdir
        self.connect = sqlite3.connect(os.path.join(database_path, str(database_name)), check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cursor.execute("PRAGMA synchronous = 2;")

    def create_table(self, table_name='u_config'):
        if not self.check_table_by_name(table_name):
            print('DataBase create a new table: ' + str(table_name))
            create_table = 'CREATE TABLE ' + str(table_name) + ' (key VARCHAR PRIMARY KEY UNIQUE, value VARCHAR);'
            self.cursor.execute(create_table)
            self.connect.commit()
        else:
            print('DataBase ' + str(table_name) + ' table is already existed')

    def get_key_by_table_name(self, table_name='u_config'):
        get_key_sql = 'SELECT key FROM ' + str(table_name)
        self.cursor.execute(get_key_sql)
        return self.cursor.fetchall()

    def check_key_existed(self, key):
        res = self.get_key_by_table_name()
        for index in res:
            if str(key) in index:
                print('DataBase ' + str(key) + ' this key is already existed!!')
                return True
        return False

    def get_value_by_key(self, key, table_name='u_config'):
        select_sql = "SELECT value FROM %s WHERE key='%s'"%(table_name, key)
        self.cursor.execute(select_sql)
        res = self.cursor.fetchall()
        if len(res) > 0:
            if len(res[0]) > 0:
                return res[0][0]
        return None

    def delete_key(self, key, table_name='u_config'):
        delete_sql = "DELETE FROM  %s WHERE key='%s'"%(table_name, key)
        self.cursor.execute(delete_sql)
        self.connect.commit()

    def update_key_value(self, key, value, table_name='u_config'):
        if not self.check_table_by_name(table_name):
            print('DataBase ' + str(table_name) + ' table is not existed , create table')
            self.create_table(table_name)
        if self.check_key_existed(key):
            print('DataBase update key:' + str(key) + ' value :' + str(value) + ' in table :' + str(table_name))
            update_sql = "UPDATE %s SET value='%s' WHERE key='%s'"%(str(table_name), str(value), str(key))
            self.cursor.execute(update_sql)
            self.connect.commit()
        else:
            print('DataBase key :' + str(key) + ' is not existed, insert it')
            self.insert_key_value(key, value, table_name)

    def insert_key_value(self, key, value, table_name='u_config'):
        if not self.check_table_by_name(table_name):
            print('DataBase ' + str(table_name) + ' table is not existed , create table')
            self.create_table(table_name)
        if not self.check_key_existed(key):
            print('DataBase insert key :' + str(key) + ' value :' + str(value) + ' in table :' + str(table_name))
            insert_sql = 'INSERT INTO ' \
                         + str(table_name) + ' (key, value) VALUES(\'' + str(key) + '\',\'' + str(value) + '\');'
            self.cursor.execute(insert_sql)
            self.connect.commit()
        else:
            print('DataBase key :' + str(key) + 'is already existed! update!!!')
            self.update_key_value(key, value, table_name)

    def get_all_data(self, table_name='u_config'):
        select_sql = 'SELECT * FROM ' + str(table_name)

        res = self.cursor.execute(select_sql)
        print('DataBase res' + str(res))
        print(self.cursor.fetchall())

        for x in res:
            print(x)

    def check_table_by_name(self, table_name='u_config'):
        gettable_sql = 'SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name;'
        self.cursor.execute(gettable_sql)
        res = self.cursor.fetchall()

        for index in res:
            if table_name in index:
                return True
        return False


# test code
if __name__ == '__main__':
    print('test sqlite3')
    sql = DataBase()

    sql.create_table()

    sql.insert_key_value('test', 'test_value_11')
    print(sql.get_value_by_key('test'))
    # sql.delete_key('test')
    sql.get_all_data()
