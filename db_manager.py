# -*- coding: utf-8 -*-
import sqlite3
import csv
import os

class SQLiteManager:
    def __init__(self, db_name="data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """创建表，columns 为 '字段 类型' 的字符串"""
        cols = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
        self.cursor.execute(sql)
        self.conn.commit()

    def show_tables(self):
        """显示所有表名并编号"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cursor.fetchall()]
        for idx, table in enumerate(tables, 1):
            print(f"{idx}. {table}")
        return tables

    def show_table_schema(self, table_name):
        """显示表结构"""
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return self.cursor.fetchall()

    def insert_data(self, table_name, values):
        """插入数据"""
        placeholders = ", ".join(["?" for _ in values])
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def select_data(self, table_name, condition=None, limit=1000):
        """查询数据，限制1000条"""
        sql = f"SELECT * FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        sql += f" LIMIT {limit}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update_data(self, table_name, set_clause, condition):
        """更新数据"""
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        """删除数据"""
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, table_name):
        """删除表"""
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(sql)
        self.conn.commit()

    def export_to_csv(self, table_name, csv_file):
        """导出表到 CSV"""
        data = self.select_data(table_name)
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def import_from_csv(self, table_name, csv_file):
        """从 CSV 导入数据"""
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.insert_data(table_name, row)

    def close(self):
        self.conn.close()

def main():
    db_name = "data.db"
    manager = SQLiteManager(db_name)

    while True:
        print("\n==== SQLite 数据库管理系统 ====")
        print("1. 创建数据表")
        print("2. 显示所有表")
        print("3. 显示表结构")
        print("4. 添加数据")
        print("5. 查询数据")
        print("6. 修改数据")
        print("7. 删除数据")
        print("8. 删除表")
        print("9. 导出表到 CSV")
        print("10. 从 CSV 导入数据")
        print("0. 退出")

        choice = input("请选择功能：")

        if choice == "1":
            table_name = input("输入表名：")
            columns = input("输入字段定义（格式：字段 类型，多个用逗号分隔）：").split(",")
            manager.create_table(table_name, columns)
            print("表创建成功")

        elif choice == "2":
            tables = manager.show_tables()
            if not tables:
                print("没有表")

        elif choice == "3":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                schema = manager.show_table_schema(table_name)
                print("表结构：", schema)

        elif choice == "4":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                values = input("输入值（用逗号分隔）：").split(",")
                manager.insert_data(table_name, values)
                print("数据添加成功")

        elif choice == "5":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                condition = input("输入查询条件（可选）：")
                data = manager.select_data(table_name, condition)
                print("查询结果：", data)

        elif choice == "6":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                set_clause = input("输入要更新的字段和值（如：name='new'）：")
                condition = input("输入条件：")
                manager.update_data(table_name, set_clause, condition)
                print("数据更新成功")

        elif choice == "7":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                condition = input("输入删除条件：")
                confirm = input("确定删除吗？(y/n)：")
                if confirm.lower() == 'y':
                    manager.delete_data(table_name, condition)
                    print("数据删除成功")
                else:
                    print("取消删除")

        elif choice == "8":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                confirm = input("确定删除表吗？(y/n)：")
                if confirm.lower() == 'y':
                    manager.drop_table(table_name)
                    print("表删除成功")
                else:
                    print("取消删除")

        elif choice == "9":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                csv_file = input("输入CSV文件名：")
                manager.export_to_csv(table_name, csv_file)
                print("导出成功")

        elif choice == "10":
            tables = manager.show_tables()
            if tables:
                table_idx = int(input("选择表编号：")) - 1
                table_name = tables[table_idx]
                csv_file = input("输入CSV文件名：")
                manager.import_from_csv(table_name, csv_file)
                print("导入成功")

        elif choice == "0":
            manager.close()
            break

if __name__ == "__main__":
    main()
