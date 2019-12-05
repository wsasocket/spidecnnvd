from io import StringIO
import re

import requests
from bs4 import BeautifulSoup


def get_more_CN_describe(cnnvd):
    buff = StringIO()
    CNNVD_URI = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD={}'.format(cnnvd)
    ret = requests.get(url=CNNVD_URI)
    soup = BeautifulSoup(ret.text, 'html.parser')
    buff.writelines('漏洞信息详情\n')
    memo = soup.find('div', attrs={'class': 'detail_xq w770'})
    buff.writelines(memo.h2.text + '\n')
    lis = memo.ul.find_all('li')
    for i in lis:
        buff.writelines(i.span.text)
        if 'CNNVD' in i.span.text:
            buff.writelines('\n')
            continue
        try:
            x = i.a.stripped_strings
            for c in x:
                buff.writelines(c + '\n')
        except:
            pass

    buff.writelines('漏洞简介' + '\n')
    desc = soup.find('div', attrs={'class': 'd_ldjj'})
    pp = desc.find_all('p')
    for i in pp:
        for c in i.stripped_strings:
            buff.writelines(c + '\n')

    bulletin = soup.find('div', attrs={'class': 'd_ldjj m_t_20'}).stripped_strings
    for c in bulletin:
        buff.writelines(c + '\n')

    buff.writelines('参考网址' + '\n')
    reference = soup.find_all('p', attrs={'class': 'ckwz'})
    for h in reference:
        r = re.search(r'http(s*)://[\w\d\.\-\_/]+', h.text)
        if r:
            buff.writelines(r.group(0) + '\n')
    buff.writelines('受影响实体' + '\n')
    affect = soup.find('div', attrs={'class': "vulnerability_list"})

    lis = affect.ul.find_all('li')
    if lis:
        for l in lis:
            try:
                li = l.select('a')
                if len(li) > 0:
                    for i in l.stripped_strings:
                        buff.writelines(i + '\n')
            except:
                pass
    else:
        buff.writelines('暂无' + '\n')
    return buff
