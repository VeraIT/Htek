"""引入库文件"""
import requests
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import configuration as con

# 设置日志级别
# logging.basicConfig(
# 	level=logging.DEBUG,
# 	format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
# 	datefmt='%Y-%m-%d %H:%M:%S %a %p',
# 	filename='syslog.log',
# 	filemode='a')

logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)
file_handler = logging.FileHandler('syslog.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s [%(funcName)s]')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_phone_webpage(url):
	"""根据给定的URL获取话机web网页
	url：需要获取网页内容的url
	"""
	try:
		# 判断获取网页异常
		r = requests.get(url, timeout=1)
		r.encoding = r.apparent_encoding
		logger.debug(url + "网页获取成功")
		return r.text
	except:
		logger.debug(url+"网页获取失败，请检查")



def check_network_phone(network_segment, start, end, phone_list):
	"""查找某一网段的Htek话机并返回IP地址
	network_segment：需要查找的话机的网络地址段前3位
	start：同一网络地址段的第四位开始查找地址
	end：同一网络地址段的第四位结束查找地址
	phone_list：搜索出来的Htek话机IP地址列表
	"""
	while start < end:
		url = network_segment + str(start)+'/index.htm'
		web_index = get_phone_webpage(url)
		match_success = re.search(r'IP Phone', str(web_index))
		if match_success is not None:
			phone_list.append(network_segment+str(start))
		start += 1
	return phone_list


def phone_register(phone):
	"""话机向SIP server注册函数"""
	logger.debug(phone.ip+"：话机开始注册")
	#话机的profile页面URL
	url_profile = "http://user:1234@"+phone.ip+"/account_profile1.htm"
	#选择哪一个profile以及注册的profile地址信息
	sip_keywords = phone.sip_keywords
	#话机的account页面URL
	url_account = "http://user:1234@"+phone.ip+"/account.htm"
	#话机注册的账号，密码信息
	account_keywords = phone.account_keywords
	try:
		# 向profile页面提交sip server信息
		r_profile = requests.post(url_profile, data=sip_keywords)
		print(r_profile.raise_for_status())
		# 向Account页面提交注册信息
		r_account = requests.post(url_account, data=account_keywords)
		logger.debug(phone.ip+'：提交账号：'+account_keywords['P35']+"信息成功")
	except:
		logger.debug(phone.ip+"：话机提交账号信息失败，请手动检查")


def check_register_state(phone):
	"""检查话机是否注册成功，注册成功，程序继续运行，注册失败，退出程序
	url_account：话机的account页面URL
	"""
	# 话机的account页面URL
	url_account = "http://user:1234@" + phone.ip + "/account.htm"
	web_account = get_phone_webpage(url_account)
	#通过正则表达式判断话机是否注册成功
	match_success = re.search(r'Registered|registered', web_account)
	if match_success is not None:
		logger.debug(match_success.group(0)+'：注册成功')

	match_fail = re.search(r'Register Failed|register_failed', web_account)
	if match_fail is not None:
		logger.debug(match_fail.group(0)+'：注册失败')


def check_pbx_state(phone):
	"""检查PBX是否可达"""
	try:
		url_pbx = "https://"+ phone.sip_ip +":5001"
		web_pbx = requests.get(url_pbx)
	except:
		logger.debug(phone.sip_ip+"异常，请检查")


def check_phone_register_info(phone):
	driver = webdriver.Chrome()
	url_pbx = "https://" + phone.sip_ip + ":5001/#/login"
	driver.get(url_pbx)
	driver.find_element_by_css_selector('[ng-model="user.user"]').send_keys('HTekadmin')
	driver.find_element_by_css_selector('[ng-model="user.password"]').send_keys('HTekadmin123')
	driver.find_element_by_css_selector('[type="submit"]').click()






def check_phone_state(phone):
	"""检查话机当前状态"""
	check_url = "http://user:1234@"+phone.ip+"/AutoTest&autoverify=STATE=0"
	r = requests.get(check_url)
	split = re.split('\n', r.text)
	callctl = split[3][11:28]
	for name in con.phone_states.keys():
		if name == callctl:
			return con.phone_states[name]

def A_call_B(phone_a, phone_b):
	"""2路基本通话"""
	phone_a_state = str(check_phone_state(phone_a))
	print(phone_a_state)
	if phone_a_state == '空闲态':
		logging.debug(phone_a.ip + ":话机状态正常，处于空闲态")
	else:
		logging.debug(phone_a.ip + ":话机状态异常处于" + phone_a_state)

	url_a = "http://" + phone_a.web_username + ':' + phone_a.web_password + '@' + phone_a.ip + '/Phone_ActionURL&Command=1&Number=' + phone_b.user_id +'&Account=1'
	url_b = "http://" + phone_b.web_username + ':' + phone_b.web_password + '@' + phone_b.ip + '/Phone_ActionURL&Command=3&key=OK'
	time.sleep(3)
	requests.get(url_a)
	logger.debug(phone_a.ip + '：呼出成功')
	check_phone_state(phone_a)
	time.sleep(3)
	# 判断获取网页异常
	requests.get(url_b)
	logger.debug(phone_b.ip + '：接听成功')
	time.sleep(3)
	check_phone_state(phone_b)
	check_phone_state(phone_a)


def phone_screen_saver(dut_setting_url, dut_tool_url):
	driver = webdriver.Chrome()
	driver.get(dut_setting_url)
	Select(driver.find_element_by_name('P8940')).select_by_value('0')
	driver.find_element_by_id('button1').click()
	driver.get(dut_tool_url)
	print('开始截图')
	driver.find_element_by_id('printscr').click()
	print('结束截图')
	time.sleep(10)




