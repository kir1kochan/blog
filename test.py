# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# 设置Chrome浏览器驱动路径
chrome_driver_path =r'C:\chromedriver.exe'

# 配置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


# 设置循环次数
num_iterations = int(input("请输入一循环次数（整数）\n"))

for _ in range(num_iterations):
    # 创建浏览器驱动
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    try:
        # 打开网页
        driver.get("https://idolhorse-audition2024.com/")

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 清除所有Cookies
        driver.delete_all_cookies()

        # 刷新页面
        driver.refresh()

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 获取 Cookie
        cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    finally:
        # 关闭浏览器驱动
        driver.quit()

    # POST 请求的数据
    url = 'https://idolhorse-audition2024.com/thanks.php'
    form_data = {
        'q1': '',  # 日文字符
        'q2': '',
        'q3': '',
        'q4': '',
        'q5': '',
        'q6': '',
        'q7': '',
        'q8': '',
        'q20': '1',
        'audition': '1',
        'step': '1'
    }

    # 自定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # 发送POST请求
    response = requests.post(url, data=form_data, headers=headers, cookies=cookies_dict)

    # 打印响应状态码和内容
    print(f"Iteration {_ + 1}:")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

