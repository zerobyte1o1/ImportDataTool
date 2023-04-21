## 导入数据创建脚本
> 结合faker库创建数据

###  使用方法 
  - pip install -r requirements.txt 
  - 将导入模板文件放在ImportDataTool 目录下
  - 将data_rules.yaml跟随模板文件重置： 
    python generated_yaml
    
  - 按照规则填写data_rules.yaml文件
  - 创建数据脚本，命令行执行： 
    python create_data 10000

### data_rules.yaml文件填写规则
```
# 如下为data_rules.yaml文件填写规则
- name: 工厂
  content: [2000,5000]
  length:
- name: 供应商编码
  content: _number
  length: 10
- name: 发放版本号
  content: _number
  length: 6
- name: 库存地点编码
  content: _number
  length: 8
  
# name为表名，content为填写内容，length为字段长度

  ```
> name: 无需修改，执行generated_yaml.py脚本后自动生成

> content:
> 1. content 内容有部分随机参数：
> - _text 随机length长度的文字
> -  _letters 随机length长度的字母
> - _number 随机length长度的数字
> - _phone 随机手机号码（中国）该参数下length不生效
> - _email 随机邮箱 该参数下length不生效
> - _conn 数据库查询结果列举 length填写内容：[sql, host, database, username, password]
> 2. content 参数的枚举：
> - 可以使用列表，如[2000,5000],脚本会在列表范围内进行单选（目前不支持多选），length参数不生效
> 3. content 直接输入：
> - 生成的数据中该字段内容均为content的内容

> length: 在部分参数下生效，随机数据时做长度限制