import requests
import re
nvdurl = r'https://nvd.nist.gov/vuln/detail/CVE-2019-12265?cpeVersion=2.2#vulnConfigurationsArea'

r = requests.get(nvdurl)
# print(r.text)
# if r'cpe:/' in r.text:
#     print('OK')
# cpes = re.findall(r'>(cpe:/(.*?))<', r.text)
# for r in cpes:
#     print(r)


def get_CPE_from_html(html):
    """从 html 中获取 CPE的相关信息，包括CPE串，from/upto（可能为空）"""
    pass


def parse_CPE(CPEs):
    """解析 CPE 字符串，返回需要的信息字典列表
    [{'OS':'','APP':'','VER','FROM_I','UPTO_I','FROM_E','UPTO_E'}]
    """
    pass


def get_CWE_from_html(html):
    """从 html 中获取 CWE的相关信息，包括CWE串 """

    pass


def parse_CWE(CWEs):
    """解析 CWE 字符串，返回需要的信息字典列表
    [{'CODE':'','NAME':'','SOURCE':''}]
    """
    pass


def get_CVSS_from_html(html):
    """从 html 中获取 CVSS3.0的字符串"""

    pass


def parse_CVSS(cvss):
    """解析 CVSS结构，暂时不返回评分"""
    pass
