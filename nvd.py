import requests
import re
from bs4 import BeautifulSoup
nvdurl = r'https://nvd.nist.gov/vuln/detail/CVE-2019-12265?cpeVersion=2.2#vulnConfigurationsArea'
# r = requests.get(nvdurl)


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    CPEs = list()
    CWEs = list()
    CVSS = list()
    CVSS = None
    CPE_rows = soup.find_all('tr', attrs={'class': 'vulnerable'})
    print(len(CPE_rows))
    for r in CPE_rows:
        CPEs.append(parse_CPE(get_CPE_from_html(r)))
    CWE_rows = soup.find_all('tr', attrs={'data-testid': "vuln-CWEs-row-0"})
    for r in CWE_rows:
        CWEs.append(parse_CWE(get_CWE_from_html(r)))

    CVSS_Element = soup.find('span', attrs={
                             'data-testid': 'vuln-cvss3-nist-vector', 'class': 'tooltipCvss3NistMetrics'})
    CVSS = parse_CVSS(get_CVSS_from_html(CVSS_Element))
    print(CPEs)
    print(CWEs)
    print(CVSS)


def get_CPE_from_html(html):
    """从 html 中获取 CPE的相关信息，包括CPE串，from/upto（可能为空）"""
    # <b data-testid = "vuln-software-cpe-2-0-0" >
    cpe = html.find('b')
    if cpe:
        return cpe.text
    return None


def parse_CPE(CPEs):
    """解析 CPE 字符串，返回需要的信息字典
    {'OS':'','APP':'','VER','FROM_I','UPTO_I','FROM_E','UPTO_E'}
    """
    return CPEs


def get_CWE_from_html(html):
    """从 html 中获取 CWE的相关信息，包括CWE串 """
    cwe = html.find('td', attrs={'data-testid': 'vuln-CWEs-link-0'})
    if cwe:
        return cwe.text
    return None


def parse_CWE(CWEs):
    """解析 CWE 字符串，返回需要的信息字典列表
    [{'CODE':'','NAME':'','SOURCE':''}]
    """
    return CWEs


def get_CVSS_from_html(html):
    """从 html 中获取 CVSS3.0的字符串"""
    return html.text


def parse_CVSS(cvss):
    """解析 CVSS结构，暂时不返回评分"""
    return cvss


if __name__ == "__main__":
    # demo = 'nvddemo.html'
    # with open(demo) as fp:
    #     h = fp.read()
    #     parse_html(h)
    r = requests.get(nvdurl)
    parse_html(r.text)
