# 检查爬取的数据文件，修正部分格式上及数据上的问题，并插入到数据库中

import os
import re
from datetime import datetime
from io import StringIO
from shutil import move
from sqlite3 import connect, IntegrityError

keywords = ['漏洞信息详情', 'CNNVD编号：', '危害等级：', 'CVE编号：', '漏洞类型：', '发布时间：',
            '威胁类型：', '更新时间：', '厂       商：', '漏洞来源：', '漏洞简介', '漏洞公告', '参考网址', '受影响实体']


def get_cve_list(path):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file() and entry.name.startswith('CVE'):
                yield entry.name


def more_key_words_in_one_line(line):
    line = line.strip('\n\r ')
    kw = list()
    for k in keywords:
        if k in line:
            kw.append(k)
    if len(kw) > 0:
        for k in kw:
            line = line.replace(k, '', 1)
        if len(line) > 0:
            return kw, line
        else:
            return kw, None
    else:
        return None, line


def init_cve_db(db_file):
    DDL = '''CREATE TABLE IF NOT EXISTS [info](
  [cve] CHAR(32) PRIMARY KEY ON CONFLICT FAIL NOT NULL ON CONFLICT FAIL UNIQUE ON CONFLICT FAIL, 
  [cnnvd] CHAR(32) UNIQUE ON CONFLICT FAIL, 
  [describe] CHAR(256) NOT NULL ON CONFLICT FAIL, 
  [level] CHAR(16), 
  [vuln_type] CHAR(32), 
  [threaten_type] CHAR(32), 
  [manufacturer] CHAR(64), 
  [source] CHAR(256), 
  [brief] CHAR(256), 
  [bulletin] CHAR(512), 
  [reference] CHAR(512), 
  [affect] CHAR(512), 
  [expose_date] DATE, 
  [reflash_date] DATE);'''
    conn = connect(db_file)
    cur = conn.cursor()
    cur.execute(DDL)
    return conn, cur


def parse_data_struct(raw_data):
    if not isinstance(raw_data, StringIO):
        raise TypeError
    if not raw_data.readable():
        raise IOError

    data_struct = dict()
    current_key = None
    print(raw_data.getvalue())
    # key_line = False
    for line in raw_data.readlines():
        key_line = False
        for k in keywords:
            if k in line:
                current_key = k
                if '更新时间' in line or '发布时间' in line:
                    date_string = line.replace(current_key, '').strip('\n')
                    r = re.match(r'(20(16|17|18|19))-(\d{2})-(\d{2})', date_string)
                    # if not r:
                    #     print(date_string)
                    #     exit(1)
                    if r:
                        data_struct[current_key] = datetime.strptime(date_string, '%Y-%m-%d')
                    else:
                        r = re.match(r'CNNVD-(20(\d{2}))(\d{2})-(\d{2,4})', data_struct['CNNVD编号：'])
                        if not r:
                            print('Can not get correct date')
                            print(line)
                            exit(1)
                        else:
                            date_string = '{}-{}-{}'.format(r.group(1), r.group(3), '01')
                            data_struct[current_key] = datetime.strptime(date_string, '%Y-%m-%d')
                else:
                    data_struct[current_key] = line.replace(current_key, '')
                key_line = True
                break
        if not key_line:
            data_struct[current_key] += line
    return data_struct


# file = r'D:\work\data\CVE-2016-0008.txt'
if __name__ == '__main__':
    db_connection, db_cursor = init_cve_db(os.path.join('.', 'cve.db'))
    ROOT = r'D:\work\data\CNNVD'
    for f in get_cve_list(ROOT):
        buffer = StringIO()
        file = os.path.join(ROOT, f)
        with open(file, encoding='utf-8') as fp:
            for line in fp:
                k, v = more_key_words_in_one_line(line)
                if k is None:  # info no keyword
                    # print(v)
                    buffer.writelines(v + '\n')
                    continue
                if len(k) > 1:  # more keyword in one line
                    for kk in k[:-1]:
                        if '：' in kk:
                            # print('{}{}'.format(kk,'N/A'))
                            buffer.writelines('{}{}\n'.format(kk, 'N/A'))
                        else:
                            # print(kk)
                            buffer.writelines(kk + '\n')
                    if '：' in k[-1] and v is not None:
                        buffer.writelines('{}{}\n'.format(k[-1], v))
                        continue
                    if '：' in k[-1] and v is None:
                        buffer.writelines('{}{}\n'.format(k[-1], 'N/A'))
                        continue
                    buffer.writelines(k[-1] + '\n')
                    if v is not None:
                        # print(v)
                        buffer.writelines(v + '\n')
                    continue
                if len(k) == 1:
                    if v is None:
                        # print(k[0])
                        buffer.writelines(k[0] + '\n')
                    else:
                        # print('{}{}'.format(k[0],v))
                        buffer.writelines('{}{}\n'.format(k[0], v))
        buffer.seek(0)
        x = parse_data_struct(buffer)
        if f[:-4] != x['CVE编号：'].strip('\n'):
            print(f[:-4])
            print(x['CVE编号：'])
            exit(1)
        SQL = 'INSERT INTO INFO(describe,cnnvd,level,cve,vuln_type,expose_date,threaten_type, \
        reflash_date,manufacturer,source,brief,bulletin,reference,affect) VALUES(:1,:2,:3,:4,:5, \
        :6,:7,:8,:9,:10,:11,:12,:13,:14)'
        SQL_VALUE = list()
        for k, v in x.items():
            if isinstance(v, str):
                SQL_VALUE.append(v.strip('\n'))
            if isinstance(v, datetime):
                SQL_VALUE.append(v.strftime('%Y-%m-%d'))
        # print(SQL_VALUE)
        try:
            db_cursor.execute(SQL, SQL_VALUE)
        except IntegrityError as e:
            print(SQL_VALUE)
            exit(1)
        buffer.close()
        move(os.path.join(r'D:\work\data\CNNVD', f), os.path.join(r'D:\work\data\CNNVD_OK', f))
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
