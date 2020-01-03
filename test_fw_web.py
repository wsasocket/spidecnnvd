from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains


# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
# wait = WebDriverWait(browser, 10)
# wait.until(EC.presence_of_element_located((By.ID, 'content_left')))  # 等到id为content_left的元素加载完毕,最多等10秒
# browser.switch_to.frame('iframeResult')  # 切换到id为iframeResult的frame
# browser.switch_to.parent_frame()  # 切回父frame,就可以查找到了
# windows_handles 为选项卡
# browser.switch_to_window(browser.window_handles[1])
# browser.switch_to_window(browser.window_handles[0])

def login():
    XPATH_USER = r'//*[@id="txt_name_p"]'
    XPATH_PASS = r'//*[@id="txt_password_p"]'
    XPATH_SUBMIT = r'//*[@id="submitId"]'

    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://10.45.254.9:8888')
    driver.find_element_by_xpath(XPATH_USER).send_keys('administrator')
    driver.find_element_by_xpath(XPATH_PASS).send_keys('XXXXXXXXXXXXXXX!')
    driver.find_element_by_xpath(XPATH_SUBMIT).click()
    return driver


def open_bridge_menu(driver=None):
    XPATH_NET = r'/html/body/div[3]/div/div[2]/div/ul/li[2]'
    XPATH_INTERFACE = r'/html/body/div[3]/div/div[2]/div/ul/li[2]/ul/li[1]/a'
    if driver is None:
        return None
    _net = driver.find_element_by_xpath(XPATH_NET)
    _intface = driver.find_element_by_xpath(XPATH_INTERFACE)
    actions = ActionChains(driver)
    actions.move_to_element(_net).click(_intface).perform()


def show_bridge_frame(driver):
    driver.execute_script('window.scrollBy(0,200)')
    sleep(1)
    XPATH_SHOW_FRAME = r'/html/body/div[5]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/a[2]'
    _show_frame = driver.find_element_by_xpath(XPATH_SHOW_FRAME)
    _show_frame.click()
    # actions = ActionChains(driver)
    # actions.click(_show_frame).perform()

def add_bridge(driver):
    # print(driver.window_handles)
    # for i in driver.window_handles:
    #     print(i)
    # driver.switch_to.frame('subModal38047546')
    XPATH_ADD_BRIDGE = r'/html/body/div[5]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[2]'
    _add_bridge = driver.find_element_by_xpath(XPATH_ADD_BRIDGE)
    driver.execute_script('window.scrollBy(0,200)')
    sleep(1)
    actions = ActionChains(driver)
    actions.click(_add_bridge).perform()
    # driver.execute_script('window.scrollBy(0,200)')
    sleep(1)
    XPATH_BRIDGE_ID = r'//*[@id="id"]'
    _bridge_id = driver.find_element_by_xpath(XPATH_BRIDGE_ID)
    actions = ActionChains(driver)
    actions.move_to_element(_bridge_id).click(_bridge_id).perform()
    _bridge_id.send_keys('10')


def drop_down_list(driver):
    XPATH_TRIGGER = r'/html/body/div[91]/div[2]/form/div[4]/div/div'
    XPATH_INTERFACE = r'/html/body/div[91]/div[2]/form/div[4]/div/div/div/ul'

    sleep(2)
    _drop_down_triggle = driver.find_element_by_xpath(XPATH_TRIGGER)
    actions = ActionChains(driver)
    actions.move_to_element(_drop_down_triggle).click(_drop_down_triggle).perform()
    sleep(1)
    _drop_menu_item = driver.find_element_by_xpath(XPATH_INTERFACE)
    interface_list = _drop_menu_item.find_elements_by_xpath('li')

    for i in interface_list:
        print(i.text)
        # if '2' in i.text:
        #     i.click()
    sleep(1)
    XPATH_SUBMIT = r'/html/body/div[91]/div[3]/button[2]'
    driver.find_element_by_xpath(XPATH_SUBMIT).click()


def remove_bridge_by_name(driver):
    driver.execute_script('window.scrollBy(0,200)')
    XPATH_BRIDGE_TABLE = r'/html/body/div[5]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/table/tbody'
    _table = driver.find_element_by_xpath(XPATH_BRIDGE_TABLE)
    _rows = _table.find_elements_by_xpath('tr')
    # for r in _rows:
    #     _col = r.find_element_by_xpath('td[@key="bridge"]')
    #     print(_col.text)
    #     if len(_col.text) == 0:
    #         break
    _col = None
    for r in _rows:
        _col = r.find_element_by_xpath('td[@key="bridge"]')
        if '10' in _col.text:
            break
    XPATH_REMOVE = r'/html/body/div[5]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[3]'
    if _col is not None:
        _remove = driver.find_element_by_xpath(XPATH_REMOVE)
        actions = ActionChains(driver)
        actions.click(_col).click(_remove).perform()
        sleep(5)
        # alert = driver.switch_to_alert()
        # print(alert.text)
        # alert.dismiss()
        # print(driver.window_handles)
        # driver.switch_to.window(driver.window_handles[0])
        # XPATH_COMFIRM = r'/html/body/div[92]/div[2]/div[2]/ul/li[2]/a'
        div = driver.find_element_by_xpath('//div[@id="tdialog"]')
        div1 = div.find_element_by_xpath('div[@id="content_wrapper"]')
        divs = div1.find_elements_by_xpath('div')
        print("!!!!!!! {} !!!!!!!!!".format(len(divs)))
        bts = divs[1].find_elements_by_xpath('ul/li')
        print(len(bts))
        bts[0].click()


if __name__ == '__main__':
    d = login()
    sleep(5)
    open_bridge_menu(d)
    show_bridge_frame(d)
    # add_bridge(d)
    # sleep(1)
    # drop_down_list(d)
    sleep(1)
    remove_bridge_by_name(d)
