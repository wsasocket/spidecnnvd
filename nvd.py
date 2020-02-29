import requests
import re
import json
from bs4 import BeautifulSoup


def parse_html(html):

    soup = BeautifulSoup(html, 'html.parser')
    CPEs = list()
    CWEs = list()
    CVSS = list()

    CPE_rows = soup.find_all('tr', attrs={'class': 'vulnerable'})
    for r in CPE_rows:
        CPEs.append(parse_CPE(get_CPE_from_html(r)))

    pattern = re.compile(r'vuln-CWEs-row-(\d)+')
    CWEs_rows = soup.find_all('tr', attrs={'data-testid': pattern})

    for r in CWEs_rows:
        CWEs.append(parse_CWE(get_CWE_from_html(r)))

    pattern = re.compile(r'tooltipCvss(2|3){1}NistMetrics')
    CVSS_Element = soup.find('span',
                             attrs={'class': pattern})

    CVSS = parse_CVSS(get_CVSS_from_html(CVSS_Element))

    return {'CPEs':CPEs,'CWEs':CWEs,'CVSS':CVSS}



def get_CPE_from_html(html):
    """从 html 中获取 CPE的相关信息，包括CPE串，from/upto（可能为空）"""
    # <b data-testid = "vuln-software-cpe-2-0-0" >
    cpe = list()
    rows = html.find_all('td')
    for r in rows:
        cpe.append(r.find('b').text)
    return cpe


def parse_CPE(cpe):
    """解析 CPE 字符串，返回需要的信息字典
    {'CPE':'','FROM':'','UPTO':''}
    CPE(Common Platform Enumeration )的格式有两种：
    cpe:2.3:a:mozilla:persona:*:*:*:*:*:drupal:*:*', 'From (including)7.x-1.0', 'Up to (excluding)7.x-1.11
    cpe:/o:siemens:siprotec_5_firmware:::~~~~~cp300', 'Up to (excluding)7.91'
    """
    tmp = {'CPE': '', 'FROM': '', 'UPTO': ''}
    tmp['CPE'] = cpe[0]
    if len(cpe) > 1:
        for i in cpe[1:]:
            if 'From ' in i:
                tmp['FROM'] = i[16:]
            elif 'Up to ' in i:
                tmp['UPTO'] = i[17:]
    return tmp


def get_CWE_from_html(html):
    """从 html 中获取 CWE的相关信息，包括CWE串 """
    rows = html.find_all('td')
    cwe = list()
    for r in rows:
        cwe.append(r.text.strip())
    return cwe


def parse_CWE(cwe):
    """解析 CWE 字符串，返回需要的信息字典
    {'CODE':'','DESC':'','SOURCE':''}
    原始格式：
    'CWE-352', 'Cross-Site Request Forgery (CSRF)', 'NIST'
    """
    tmp = {'CODE': '', 'DESC': '', 'SOURCE': ''}
    tmp['CODE'] = cwe[0]
    tmp['DESC'] = cwe[1]
    tmp['SOURCE'] = cwe[2]

    return tmp


def get_CVSS_from_html(html):
    """从 html 中获取 CVSS3.0的字符串"""
    return html.text


def parse_CVSS(cvss):
    """解析 CVSS结构，暂时不返回评分
        {'VSESION':'','CVSS':'','SCORE':0}
    """
    tmp={'VERSION':'','CVSS':'','SCORE':0}
    if (r := re.match(r'^CVSS:(\d+\.\d+)\/(AV:*.+)',cvss)):
        tmp['VERSION'] = r.group(1)
        tmp['CVSS'] = r.group(2)
    else:
        tmp['VERSION'] = '2.0'
        tmp['CVSS'] = cvss[1:-1]
    return tmp


if __name__ == "__main__":
    url_telplate = 'https://nvd.nist.gov/vuln/detail/{CVE}#vulnConfigurationsArea'
    cves = ['CVE-2013-4227','CVE-2008-4250','CVE-2019-12265']
    for cve in cves:
        r = requests.get(url_telplate.format(CVE=cve))
        print(json.dumps({'CVE':cve,'NIST':parse_html(r.text)}))

