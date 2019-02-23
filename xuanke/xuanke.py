# -*- coding: utf-8 -*-
import os
import time
import traceback

import requests
import requests.cookies
import selenium
from lxml import etree
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from wxpy import *

from config import platform_name, get_driver, data_dir
from info import Info
from validcode import get_validcode

chrome_options = Options()
chrome_options.add_argument('--headless')

# 验证码使用


headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           # "Cookie": "JSESSIONID=NSvFcspQDf0YvgDFjbLPMvXrr5JpZNw6r8vX3W1wbtqds6wDyVTn!-1915155993",
           "Host": "elective.pku.edu.cn",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/72.0.3626.109Safari/537.36"
           }


class Xuanke(object):
    def __init__(self, username, password, listening_course,
                 page_fresh_frequency, course_fresh_frequency,
                 wechat_info=False, info_person=False,
                 auto_select=False):
        self.username = username
        self.password = password
        self.listening_course = listening_course
        self.page_fresh_frequency = page_fresh_frequency
        self.course_fresh_frequency = course_fresh_frequency
        self.wechat_info_flag = wechat_info
        self.info_person_flag = info_person
        self.auto_select = auto_select
        # 非接收参数
        self.driver = get_driver()
        self.run_seconds = 0
        self.info = Info(wechat_info=wechat_info)
        # self.driver.maximize_window()

    def login(self):
        """登录"""
        login_url = ("https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=syllabus&appName="
                     "%E5%AD%A6%E7%94%9F%E9%80%89%E8%AF%BE%E7%B3%BB%E7%BB%9F&redirectUrl="
                     "http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do")
        self.get_page_by_selenium(login_url)
        self.driver.find_element_by_id("user_name").clear()
        self.driver.find_element_by_id("user_name").send_keys(self.username)  # 学号
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys(self.password)  # 密码
        self.driver.find_element_by_id("logon_button").click()

    def get_page_by_selenium(self, url):
        try:
            self.driver.get(url)
        except selenium.common.exceptions.WebDriverException:
            self.driver = get_driver()
            self.driver.get(url)
        content = self.driver.page_source
        return content

    def get_content(self):
        """获取当前页面信息"""
        content = self.driver.page_source
        if "无法访问此网站" in content:
            time.sleep(2 * 60)
            self.driver.refresh()
        while "您尚未登录或者会话超时,请重新登录" in content or "请不要用刷课机刷课，否则会受到学校严厉处分！" in content:
            self.driver.find_element_by_xpath('//a[text()="退  出"]').click()  # 退出
            time.sleep(1)  # 等待网页加载完毕
            self.login()
            time.sleep(1)  # 等待网页加载完毕
            self.driver.find_element_by_xpath('//a[text()="补退选"]').click()
            time.sleep(1)  # 等待网页加载完毕
            content = self.driver.page_source
        return content

    def parse_content(self, content):
        """解析选课详情页"""
        all_class = {}
        # 表一
        xuanke_table1 = etree.HTML(content).xpath('//table[@class="datagrid"]')[0]
        xuanke_trs_even = xuanke_table1.xpath('//tr[@class="datagrid-even"]')
        xuanke_trs_odd = xuanke_table1.xpath('//tr[@class="datagrid-odd"]')
        trs = xuanke_trs_even + xuanke_trs_odd
        th1 = ['课程名', '课程类别', '学分', '周学时', '教师', '班号', '开课单位', '专业', '年级', '上课信息', '授课语言', '限数/已选', '补选']
        for td in trs:
            class_info = td.xpath('.//span/text()')
            if len(class_info) == 12:  # 综合实践课，缺教师
                continue
            dic = dict(zip(th1, class_info))
            all_class[dic["课程名"]] = dic
        # 表二
        xuanke_table2 = etree.HTML(content).xpath('//table[@class="datagrid"]')[1]
        xuanke_trs_even = xuanke_table2.xpath('//tr[@class="datagrid-even"]')
        xuanke_trs_odd = xuanke_table2.xpath('//tr[@class="datagrid-odd"]')
        trs = xuanke_trs_even + xuanke_trs_odd
        th1 = ['课程名', '课程类别', '学分', '周学时', '教师', '班号', '开课单位', '专业', '年级', '上课信息', '限数/已选', '补选']
        for td in trs:
            class_info = td.xpath('.//span/text()')
            dic = dict(zip(th1, class_info))
            all_class[dic["课程名"]] = dic
        return all_class

    def download_code_picture(self, pic_name, code_url):
        """下载验证码"""
        with open(os.path.join(data_dir, pic_name), "wb") as f:
            cookies = self.driver.get_cookies()
            headers["Cookie"] = 'JSESSIONID={}'.format(cookies[0]['value'])
            res = requests.get(code_url, headers=headers)
            f.write(res.content)

    def accept_alert(self):
        """ 弹窗确认"""
        alert_text = ""
        if platform_name == "Linux":
            self.driver.execute_script("window.confirm = function(msg) { return true; }")
        else:  # mac,windows
            alert = self.driver.switch_to.alert  # '''获取alert对话框'''
            time.sleep(2)  # '''添加等待时间'''
            alert_text = alert.text
            print(alert_text)  # 打印警告对话框内容
            alert.accept()  # alert对话框属于警告对话框，我们这里只能接受弹窗
        return alert_text

    def fresh_course(self, course_name):
        """点击刷新按钮 course_name:
        """
        try:
            course = self.driver.find_element_by_xpath(
                "//a[contains(@onclick, 'confirmSelect') and contains(@onclick, '{}')]/span[text()='刷新']".format(
                    course_name))
            course.click()  # 点击刷新
            time.sleep(1)
            self.accept_alert()  # 弹窗确认
            print('{}刷新成功'.format(course_name))
        except:
            time.sleep(1)
        fresh_limit_id = self.driver.find_element_by_xpath(
            "//a[contains(@onclick, 'confirmSelect') and contains(@onclick, '{}')]".format(
                course_name)).get_attribute("id")
        if not fresh_limit_id:
            if self.driver.find_element_by_xpath(
                    "//a[contains(@onclick, 'confirmSelect') and contains(@onclick, '{}')]".format(
                        course_name)).text == "补选":
                selected_count = 0
                all_count = 1
            else:
                print('{}刷新失败\n'.format(course_name))
        else:
            electedNum_id = "electedNum{}".format(fresh_limit_id.replace("refreshLimit", ''))
            selected_bulk = self.driver.find_element_by_xpath('//*[@id="{}"]'.format(electedNum_id)).text
            selected_count = selected_bulk.split("/")[0]
            all_count = selected_bulk.split("/")[1]
            print("** {}（{}）\n\n".format(course_name, selected_bulk))
        return selected_count, all_count

    def select_course(self, course_name):
        """ 补选
        :param course_name: 课程名
        """
        code_url = self.driver.find_element_by_id('imgname').get_attribute("src")
        print("code_url： {}".format(code_url))
        pic_name = "code_pic_wsg.png"
        self.download_code_picture(pic_name, code_url)
        code = get_validcode(data_dir, pic_name)
        print("identifying code: {}".format(code))
        self.driver.find_element_by_id('validCode').clear()
        self.driver.find_element_by_id('validCode').send_keys(code)
        # 补选
        self.driver.find_element_by_xpath(
            "//a[contains(@onclick, 'confirmSelect') and contains(@onclick, '{}')]/span[text()='补选']".format(
                course_name)).click()
        alert_text = self.accept_alert()  # 弹窗确认
        print("** {} 补选成功! alert:{}\n".format(course_name, alert_text))
        return True

    def detail_handle(self):
        """处理详情页，解析详情页后，发通知等"""
        content = self.get_content()
        all_course = self.parse_content(content)
        print("all_course: {}".format(all_course))
        select_status = ""
        info_course = {"有空缺": [], "暂无空缺": []}
        for course_name in self.listening_course:
            num = all_course[course_name].get("限数/已选", "")
            if len(num.split('/')) != 2:
                num = all_course[course_name].get("补选")
            if int(num.split('/')[0]) != int(num.split('/')[1]):
                course_str = "{} ({})".format(course_name, num)
                info_course["有空缺"].append(course_str)
            else:
                info_course["暂无空缺"].append("{} ({})".format(course_name, num))
        info_str = "{}\n有空缺：\n{}\n------\n暂无空缺：\n{}".format(
            select_status, "\n".join(info_course["有空缺"]), "\n".join(info_course["暂无空缺"]))
        if len(info_course["有空缺"]) > 0 and self.info_person_flag:
            self.info.info_person()
        print(info_str)
        if self.wechat_info_flag:  # 是否发微信通知
            self.info.info_wechat(info_str)

    def xuanke_task(self):
        self.login()  # 登录
        time.sleep(2)  # 等待网页加载完毕
        self.driver.find_element_by_xpath('//a[text()="补退选"]').click()
        while True:
            try:
                if self.auto_select:  # 自动选课
                    for course_name in self.listening_course:
                        selected_count, all_count = self.fresh_course(course_name)
                        if selected_count < all_count:
                            self.select_course(course_name)  # 补选
                if self.run_seconds % self.page_fresh_frequency == 0:  # 每page_fresh_frequency刷新一次
                    self.detail_handle()  # 补选页面详情处理，解析详情页后发通知等
                    time.sleep(self.page_fresh_frequency)
                    self.run_seconds += self.page_fresh_frequency
                    self.driver.refresh()  # 整体刷新
                self.run_seconds += self.course_fresh_frequency
                time.sleep(self.course_fresh_frequency)  # 每course_fresh_frequency刷新一次
            except Exception:
                print(traceback.format_exc())
                print("异常，接下来暂停10s")
                time.sleep(10)
                print("确定暂停10s了吗\n")

    def run(self):
        logging.info('process %s start ')
        self.xuanke_task()
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                exit(1)
            except Exception as e:
                logging.error(e)
