# selenium demo
# 通过cve查询cnnvd的信息，同时爬取相关的中文信息
import os
from random import randint
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from rebuild_cnnvd import parse_data_struct
from parseCNNVD import get_more_CN_describe


class MoreElementsException(Exception):
    def __init__(self, cve):
        self.cve = cve

    def __str__(self):
        return 'CVE-{} find more result.'.format(self.cve)


def get_cnnvd_desc(webDriver, cve):
    sleep(2)
    driver.find_element_by_xpath('//*[@id="qcvCnnvdid"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="qcvCnnvdid"]').clear()
    driver.find_element_by_xpath('//*[@id="qcvCnnvdid"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="qcvCnnvdid"]').send_keys(cve)
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[1]/form/table/tbody/tr[5]/td[2]/a').click()
    # 提交表单后检查返回结果
    result_list_path = r'/html/body/div[4]/div/div[1]/div/div[2]/ul/li'
    while True:
        CNNVD_list = driver.find_elements_by_xpath(result_list_path)
        # print(type(CNNVD_list))
        if len(CNNVD_list) == 1:
            return CNNVD_list[0].find_element_by_xpath('div[1]/p/a[1]').text

        for li in CNNVD_list:
            cnnvd = li.find_element_by_xpath('div[1]/p/a[1]').text
            data = get_more_CN_describe(cnnvd)
            data.seek(0)
            # print(data.getvalue())
            desc = parse_data_struct(data)
            sleep(randint(1, 5))
            if desc['CVE编号：'].strip('\n') == 'CVE-{}'.format(cve):
                return cnnvd
        else:
            page_2 = '/html/body/div[4]/div/div[1]/div/div[3]/a[4]'
            driver.find_element_by_xpath(page_2).click()
            sleep(3)



    # try:
    #     CNNVD = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul/li/div[1]/p/a[1]')
    # except NoSuchElementException:
    #     return None, None
    #
    # try:
    #     CNNVD = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul/li[2]/div[1]/p/a[1]')
    # except NoSuchElementException:
    #     pass
    # else:
    #     raise MoreElementsException(cve)
    #
    # while True:
    #     CNNVD = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul/li/div[1]/p/a[1]')
    #     if CNNVD.is_displayed():
    #         # print(CNNVD.text)
    #         break
    #     print('Searching')
    #     sleep(2)
    # detail = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul/li/div[1]/a')
    # return CNNVD.text, detail.text
    # # print(driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul/li/div[1]/a').text)


if __name__ == "__main__":
    cves = list()
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    driver.get('http://www.cnnvd.org.cn/web/vulnerability/querylist.tag')
    # sleep(2000)
    while True:
        textbox = driver.find_element_by_xpath('//*[@id="qcvCnnvdid"]')
        if textbox.is_displayed():
            break
        print("Loading")
        sleep(2)

    with open(r'D:\work\data\cve.txt') as fp:
        for line in fp:
            cves.append(line.strip('\n\r'))
    print(len(cves))
    # cves=['2016-1062']
    # fp = open (r'D:\work\data\cnnvd.txt','w')
    for cve in cves:
        # print('CVE-{}'.format(cve))
        cnnvd = None
        try:
            cnnvd = get_cnnvd_desc(driver, cve)
        except TimeoutException as e:
            try:
                os.remove(r'D:\work\data\CVE-{}.txt'.format(cve))
            except:
                pass
            print('CVE-{} Searching Time out'.format(cve))
            continue
        except MoreElementsException as e:
            try:
                os.remove(r'D:\work\data\CVE-{}.txt'.format(cve))
            except:
                pass
            print(e)
            continue

        # fp.close()
        # print('\n')
        # get_more_CN_describe(cnnvd)
        # buf = '{},{},{}\n'.format(cve,cnnvd,detail)
        if cnnvd is None:
            print('CVE-{} Not Found Corresponding CNNVD'.format(cve))
            try:
                os.remove(r'D:\work\data\CVE-{}.txt'.format(cve))
            except FileNotFoundError:
                pass
            continue
        print('{},{}'.format(cve, cnnvd))
        # fp.writelines(buf)
        sleep(2 + randint(3, 18))

        try:
            buff = get_more_CN_describe(cnnvd)
        except TimeoutException as e:
            print('ERROR @ {}'.format(cnnvd))
            buff.close()
            continue
        cve_file = open(r'D:\work\data\CVE-{}.txt'.format(cve), 'w', encoding='utf-8')
        cve_file.write(buff.getvalue())
        cve_file.close()
        buff.close()
    # fp.close()
    driver.quit()
