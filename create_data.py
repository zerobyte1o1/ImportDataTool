import os
import random
import sys
import yaml
from openpyxl import load_workbook
from faker import Faker
import psycopg2

fake = Faker(locale='zh_CN')
file_list = os.listdir()
for file in file_list:
    if '.xlsx' in file:
        file_name = file


def write_data(data: list):
    wb = load_workbook(file_name)
    ws = wb['Sheet1']
    for data_line in data:
        ws.append(data_line)
    wb.save(file_name)
    print(f'数据生成成功，已存入文件——{file_name}')


class Conn_res:
    res = []
    colu = 0

    @classmethod
    def exe_sql(cls, sql, host, database, username, password):
        if not cls.res:
            conn=cls.conn_postgres(host, database, username, password)
            cursor = conn.cursor()
            cursor.execute(sql)
            cls.res = cursor.fetchall()

    @classmethod
    def conn_postgres(cls, host, database, username, password):
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password
        )
        return conn


def create_data(total):
    with open('data_rules.yaml', 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    result_data = []
    for i in range(total):
        list_data = []
        for j, item in enumerate(data):
            if item['content'] == '_text':
                value = fake.sentence(nb_words=item['length'], variable_nb_words=True, ext_word_list=None)
            elif item['content'] == '_letters':
                value = fake.pystr(min_chars=None, max_chars=item['length'])
            elif item['content'] == '_number':
                value = fake.random_number(digits=item['length'])
            elif item['content'] == '_phone':
                value = fake.phone_number()
            elif item['content'] == '_email':
                value = fake.email()
            elif type(item['content']) is list:
                value = random.choice(item['content'])
            elif type(item['content']) is None:
                value = ''
            elif item['content'] == '_conn':
                value = Conn_res.exe_sql(item['length'][4], item['length'][0], item['length'][1], item['length'][2],
                                         item['length'][3])
                Conn_res.colu = j
                value = ''
            else:
                value = item['content']
            list_data.append(value)
        result_data.append(list_data)
        for k, item_ in enumerate(Conn_res.res):
            result_data[k][Conn_res.colu] = item_

    return result_data


param = sys.argv

if len(param) != 2:
    print('请输入正确的参数')
    sys.exit()

data = create_data(int(param[1]))
write_data(data)
