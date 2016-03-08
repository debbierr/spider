# coding:utf-8


#网页下载器
#根据给出的URL进行下载，其中如果需要代理或其他，需要对opener进行改写
#更新时间：2016/3/8
#创建时间：2016/3/2
#作者：debbie

import urllib2
import cookielib

class HtmlDownloader(object):
	
	#发送HTTP请求并存储响应的HTML文档
	def download(self,url):
		if url is None:
			return None
		#添加cookie信息
		# cookie=cookielib.CookieJar()
		# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		# urllib2.install_opener(opener)
		# request = urllib2.Request(url)
		#包装头部信息
		request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
		response = urllib2.urlopen(request)
		if response.getcode() !=200:
			return None
		return response.read()
