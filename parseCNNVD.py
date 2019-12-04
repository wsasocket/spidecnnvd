from io import StringIO
import re

import requests
from bs4 import BeautifulSoup


def get_more_CN_describe(cnnvd):
    buff = StringIO()
    CNNVD_URI = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD={}'.format(cnnvd)
    ret = requests.get(url=CNNVD_URI)
    soup = BeautifulSoup(ret.text, 'html.parser')
    # print('漏洞信息详情')
    buff.writelines('漏洞信息详情\n')
    memo = soup.find('div', attrs={'class': 'detail_xq w770'})
    # print(memo.h2.text)
    buff.writelines(memo.h2.text + '\n')
    lis = memo.ul.find_all('li')
    for i in lis:
        # print(i.span.text,end='')
        buff.writelines(i.span.text)
        # print(buff.getvalue())
        if 'CNNVD' in i.span.text:
            # print('\n')
            buff.writelines('\n')
            continue
        try:
            x = i.a.stripped_strings
            for c in x:
                # print(c)
                buff.writelines(c + '\n')
        except:
            pass
    # print('漏洞简介')
    buff.writelines('漏洞简介' + '\n')
    desc = soup.find('div', attrs={'class': 'd_ldjj'})
    pp = desc.find_all('p')
    for i in pp:
        for c in i.stripped_strings:
            # print(c)
            buff.writelines(c + '\n')

    bulletin = soup.find('div', attrs={'class': 'd_ldjj m_t_20'}).stripped_strings
    for c in bulletin:
        # print(c)
        buff.writelines(c + '\n')

    # print('参考网址')
    buff.writelines('参考网址' + '\n')
    reference = soup.find_all('p', attrs={'class': 'ckwz'})
    for h in reference:
        r = re.search(r'http(s*)://[\w\d\.\-\_/]+', h.text)
        if r:
            # print(r.group(0))
            buff.writelines(r.group(0) + '\n')
    # print('受影响实体')
    buff.writelines('受影响实体' + '\n')
    affect = soup.find('div', attrs={'class': "vulnerability_list"})

    lis = affect.ul.find_all('li')
    if lis:
        for l in lis:
            try:
                li = l.select('a')
                if len(li) > 0:
                    for i in l.stripped_strings:
                        # print(i)
                        buff.writelines(i + '\n')
            except:
                pass

    else:
        # print('暂无')
        buff.writelines('暂无' + '\n')
    return buff
