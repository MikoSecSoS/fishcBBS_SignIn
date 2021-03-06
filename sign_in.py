# -*- coding: utf-8 -*-

import re
import time
import datetime
import threading
import configparser

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By  

browser = webdriver.PhantomJS()
# browser = webdriver.Chrome()


class SignIn(object):
	"""docstring for SignIn"""

	def signIn(self):
		nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print("开始签到，当前时间:", nowTime)

		startTime = time.time()
		browser.get("https://fishc.com.cn/")
		try:
			WebDriverWait(browser,10).until(lambda x: x.find_element_by_xpath("//*[@id=\"ls_username\"]")).send_keys(self.username)
			WebDriverWait(browser,10).until(lambda x: x.find_element_by_xpath("//*[@id=\"ls_password\"]")).send_keys(self.password)
			browser.find_element_by_xpath("//*[@id=\"lsform\"]/div/div[1]/table/tbody/tr[2]/td[3]/button/em").click()
			print("输入账密完成...")
			time.sleep(1)
		except Exception as e:
			print("当前为登录状态")

		browser.get("https://fishc.com.cn/plugin.php?id=k_misign:sign")
		try:
			WebDriverWait(browser,5).until(lambda x: x.find_element_by_xpath("//*[@id=\"JD_sign\"]")).click()
			print("签到成功...")
			time.sleep(1)
		except Exception as e:
			print("未登录或已签到")

		html = WebDriverWait(browser,5).until(lambda x: x.find_element_by_xpath("//*[@id=\"wp\"]/div[2]/div[1]/div[1]/div/div[1]")).get_attribute("outerHTML")

		flag = html.find("您的签到排名")

		if flag:
			top = "您的签到排名: " + re.search("\d+", html).group(0)
			print(top)
			with open("access.txt", "a+") as f:
				f.write("[ " + nowTime + " ]\t" + top + "\r\n")
		else:
			print("签到失败")
			with open("签到失败源码.txt", "w") as f:
				f.write(html)

		# browser.quit() # 关闭浏览器

		endTime = time.time()

		useTime = endTime-startTime

		print("[签到用时]", useTime)

		try:
			timer = threading.Timer(86400-useTime, self.signIn)
			timer.start()
		except KeyboardInterrupt as e:
			print("Bye~~~")

	def loadConfig(self):
		print("Load Config...")
		config = configparser.ConfigParser()
		config.read("config.ini")
		self.username = config.get("user", "username")
		self.password = config.get("user", "password")

def main():
	now_time = datetime.datetime.now()

	next_time = now_time + datetime.timedelta(days=+1)
	next_year = next_time.date().year
	next_month = next_time.date().month
	next_day = next_time.date().day

	next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 00:00:00", "%Y-%m-%d %H:%M:%S")

	last_time = now_time + datetime.timedelta(days=-1)

	timer_start_time = (next_time - now_time).total_seconds()
	print(timer_start_time, "秒后签到...")

	signin = SignIn()

	signin.loadConfig()

	signin.signIn()

	timer = threading.Timer(timer_start_time, signin.signIn)
	timer.start()

if __name__ == '__main__':
	main()
