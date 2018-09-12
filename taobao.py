import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


USER = 'your username'
PASSWORD = 'your password'

class Crcaktest():
    def __init__(self):
        self.url = 'https://sycm.taobao.com/custom/login.htm?_target=http://sycm.taobao.com/'
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('disable-infobars')
        # self.add_argument(r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default')
        # self.option.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
        self.browser = webdriver.Chrome(chrome_options=self.option)
        self.wait = WebDriverWait(self.browser,20)
        self.user = USER
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def open(self):
        '''
        打开网页输入账号 和 密码
        :return: None
        '''
        self.browser.get(self.url)
        time.sleep(3)
        iframe = self.browser.find_element_by_xpath('//*[@id="app"]/div/section[1]/div/div[1]/iframe')
        self.browser.switch_to_frame(iframe)
        # user = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="TPL_username_1"]')))
        # password = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="TPL_password_1"]')))
        user =self.browser.find_element_by_xpath('//*[@id="TPL_username_1"]')
        user.send_keys(self.user)
        time.sleep(5)
        password = self.browser.find_element_by_xpath('//*[@id="TPL_password_1"]')
        password.send_keys(self.password)


    def get_slider(self):
        '''
        获取滑块
        :return:滑块对象
        '''
        # slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nc_iconfont btn_slide')))
        slider = self.browser.find_element_by_id('nc_1_n1z')
        return slider


    def get_track(self,distance):
        '''
        根据移动偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        '''
        #偏移轨迹
        track = []
        #当前位移
        current = 0
        #减速阈值
        mid = distance * 4/5
        #计算间隔
        t = 0.2
        #初始速度
        v = 0

        while current < distance:
            if current < mid:
                #加速度为2
                a = 2
            else:
                #加速度为-3
                a = -3
            #初始速度v0
            v0 = v
            #当前速度为 v = v0 + at
            v = v0 + a*t
            #位移距离x = v0t + 1/2*at^2
            move = v0 * t + 1/2* a * t * t
            #当前位移
            current += move
            #加入轨迹
            track.append(round(move))
        return track

    # def move_to_gap(self,slider,tracks):
    def move_to_gap(self,slider):
        '''
        拖动滑块到终点
        :param slider:滑块
        :param tracks: 轨迹
        :return:
        '''
        action = ActionChains(self.browser)

        action.drag_and_drop_by_offset(slider, 400, 0).perform()
        time.sleep(2)

        # action.click_and_hold(slider).perform()
        # for x in tracks:
        #     action.move_by_offset(xoffset=x,yoffset=0).perform()
        # time.sleep(2)
        # action.release().perform()

    def login(self):
        '''
        登录
        :return:None
        '''
        # submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'J_Submit')))
        submit = self.browser.find_element_by_class_name('J_Submit')
        submit.click()
        time.sleep(10)
        print('登录成功')

    def run(self):
        # 输入账号 和 密码
        self.open()
        print('打开网页输入账号密码了')
        # // *[ @ id = "nc_1__scale_text"] / span / b 验证通过的文本
        # 判断是否需要验证
        if not self.browser.find_element_by_id('nocaptcha').get_attribute('style'):
            print('不需要滑动验证')
            print(self.browser.find_element_by_id('nocaptcha').get_attribute('style'))
            self.login()
            time.sleep(5)
        else:
            print('需要滑动验证')
            slider = self.get_slider()
            # slider.click()
            # 获取移动轨迹
            # track = self.get_track(206)  # ????
            # print('滑动轨迹', track)
            # 拖动滑块
            self.move_to_gap(slider)
            # self.move_to_gap(slider, track)

            success = self.wait.until(EC.text_to_be_present_in_element((By.ID, 'nc_1__scale_text'), '验证通过'))
            print(success)

            #需要再次输入密码
            password = self.browser.find_element_by_xpath('//*[@id="TPL_password_1"]')
            password.send_keys(self.password)
            # 失败重试
            if not success:
                self.run()
            else:
                self.login()



if __name__ == '__main__':
    crack = Crcaktest()
    crack.run()