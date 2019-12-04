# 主要解决cve搜索时出现多个记录的情况下，需要人工设定cve于cnnvd的对应关系，然后爬取数据
import re

from selenium.common.exceptions import TimeoutException

from parseCNNVD import get_more_CN_describe

if __name__ == "__main__":
    cnnvd = dict()
    with open('cnnvd_remain.txt') as fp:
        for line in fp:
            r = re.search(r'CVE-(\d+\-\d+),(CNNVD-\d+\-\d+)', line)
            if r:
                cnnvd[r.group(1)] = r.group(2)
    # print(cnnvd)
    for cve, cnnvd in cnnvd.items():
        print(cve, cnnvd)
        try:
            buffer = get_more_CN_describe(cnnvd)
        except TimeoutException as e:
            print('ERROR @ {}'.format(cnnvd))
            buffer.close()
            continue
        cve_file = open(r'D:\work\data\CVE-{}.txt'.format(cve), 'w', encoding='utf-8')
        cve_file.write(buffer.getvalue())
        cve_file.close()
        buffer.close()
