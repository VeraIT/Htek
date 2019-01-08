import requests


class Phone():
	"""构建一个类用来表示话机"""
	def __init__(self, info_dict):
		"""初始化话机的IP地址和MAC地址"""
		self.ip = info_dict['ip']
		self.mac = info_dict['mac']
		self.web_username = info_dict['web_username']
		self.web_password = info_dict['web_password']
		self.sip_ip = info_dict['sip_ip']
		self.user_id = info_dict['user_id']
		self.password = info_dict['password']
		self.sip_keywords = {'P1': '0', 'P47': self.sip_ip}
		self.account_keywords = {
			'P24082': self.sip_keywords['P1'],
			'P35': self.user_id,
			'P36': self.user_id,
			'P34': self.password
		}

	def make_url(self, web_title):
		"""根据话机的基本信息创建要访问的话机页面的URL"""
		url = "http://"+self.web_username+':'+self.web_password+'@'+self.ip+'/'+web_title+'.htm'
		return url

	def get_webpage(self):
		"""获取话机的网页"""
		url = "http://"+self.web_username+':'+self.web_password+'@'+self.ip+self.home
		try:
			#判断获取网页异常
			r = requests.get(url, timeout=10)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			print("话机"+self.ip+"网页获取失败，请手动检查")




