# coding:utf8

#URL管理器
#维持两个URL集合，分别为已经爬过的URL和未爬的URL
#更新时间：2016/3/8
#创建时间：2016/3/2
#作者：debbie

class UrlManager(object):

	def __init__(self):
		#待爬取的URL集合
		self.new_urls=set()
		#已爬取的URL集合
		self.old_urls=set()

	#添加一个URL
	def add_new_url(self,url):
		if url==None:
			return
		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)

	#批量添加多个URL
	def add_new_urls(self,urls):
		if urls is None or len(urls)==0:
			return
		for url in urls:
			self.add_new_url(url)

	#判断是否还有需要爬的URL
	def has_new_url(self):
		return len(self.new_urls)!=0

	#取出一个URL待爬
	def get_new_url(self):
		new_url=self.new_urls.pop()
		self.old_urls.add(new_url)
		return new_url
