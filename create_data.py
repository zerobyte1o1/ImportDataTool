import os
import random
import sys
import yaml
from openpyxl import load_workbook
from faker import Faker

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


def create_data(total):
    with open('data_rules.yaml', 'r') as file:
        data = yaml.safe_load(file)
    result_data = []
    for i in range(total):
        list_data = []
        for item in data:
            if item['content'] == '_text':
                value = fake.sentence(nb_words=item['length'], variable_nb_words=True, ext_word_list=None)
            elif item['content'] == '_letters':
                value = fake.pystr(min_chars=None, max_chars=item['length'])
            elif item['content'] == '_number':
                value = fake.random_number(digits=item['length'])
            elif item['content'] == '_phone':
                value = fake.phone_number
            elif item['content'] == '_email':
                value = fake.email()
            elif type(item['content']) is list:
                value = random.choice(item['content'])
            else:
                value = item['content']
            list_data.append(value)
        result_data.append(list_data)

    return result_data

param=sys.argv

if len(param) !=2:
    print('请输入正确的参数')
    sys.exit()
try:
    data = create_data(int(param[1]))
    write_data(data)
except:
    print("参数请输入数字")