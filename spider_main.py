# coding:utf-8

#
#该程序是一个简单的轻量级的爬虫程序。
#可以针对一般的不需要登录不需要代理的网页进行爬取。
#程序给出了两个情况：
#1.爬取的内容是有HTML网页同步的直接呈现的，可以用DOM结构里面提取
#2.爬取的内容是异步的，由后台异步传JSON给前台的，需要从网页结构里面提取其JSON数据路径
#针对不同的网页结构和不同的爬取数据需要自定义其匹配关键词，为保护项目隐私已经隐去相关的URL
#和正则匹配项。其中有关URL的均以http://baidu.com代替，有关匹配项的分别以subName，subString
#和className代替，需要根据实际爬虫需要进行替换。
#
#------------------------------------------------------------------------------------
#爬虫主程序
#四个子模块，URL管理器、网页下载器、网页解析器、数据存储器
#爬虫基本逻辑：从URL管理器中取出URL送入网页下载器进行网页下载，
#下载好的网页送入网页解析器提取感兴趣的内容，并用数据存储器进行存储。
#更新时间：2016/3/8
#创建时间：2016/3/2
#作者：debbie

from spider import url_manager,html_downloader,html_parser,html_outputer

class SpiderMain(object):

	def __init__(self):
		self.urls=url_manager.UrlManager()
		self.downloader=html_downloader.HtmlDownloader()
		self.parser=html_parser.HtmlParser()
		self.outputer=html_outputer.HtmlOutputer()

#针对可以直接在HTML的DOM树中找到的数据的情况
	def craw(self,root_url):
		#爬取的页面数
		count=1
		self.urls.add_new_url(root_url)
		while self.urls.has_new_url():
			try:
				new_url=self.urls.get_new_url()
				#记录爬虫过程，可以写到>一个log里面，方便查看
				print 'craw %d : %s'%(count,new_url)
				html_cont=self.downloader.download(new_url)
				new_urls, new_data = self.parser.parse(new_url,html_cont)
				self.urls.add_new_urls(new_urls)
				#每次爬取都进行数据的汇总
				self.outputer.collect_data(new_data)
				if count==1000:
					break
				count=count+1
			except:
				print 'craw failed'
		#爬取完成后，再进行数据的存储
		self.outputer.output_html()


#针对由数据后台异步传JSON数据给前端页面展示的情况
#需要从下载的页面中找出JSON数据源的地址
#然后根据这个地址下载出JSON字符串
#解析字符串，获取URL和数据内容

	#根据根页面提取url，并存入url列表
	def craw_all(self,root_url):		
		#要爬取的数据条数
		size=1000;
		html_cont=self.downloader.download(root_url)
		data_link=self.parser.get_topic_data(html_cont,size)
		data_cont=self.downloader.download(data_link)
		#print data_cont
		topic_urls, topic_data = self.parser.parse_topic(data_cont)
		self.urls.add_new_urls(topic_urls)
		#如果根页面有需要存储的数据时，需要进行collect
		#self.outputer.collect_topic(topic_data)

	#根据URL列表中逐次进行单个页面进行爬取
	def craw_each(self):
		#爬取的页面数
		count=0
		while self.urls.has_new_url():
			count = count+1
			try:
				size=500
				new_url=self.urls.get_new_url()
				#记录爬虫过程，可以写到>一个log里面，方便查看
				print 'craw %d : %s'%(count,new_url)
				#print new_url
				html_cont=self.downloader.download(new_url)
				#print html_cont
				data_link = self.parser.get_comment_data(new_url,html_cont,size)
				data_cont=self.downloader.download(data_link)
				comment_data = self.parser.parse_comment(data_cont)
				#self.urls.add_new_urls(new_urls)
				#每爬一URL，就进行存储
				self.outputer.collect_data(comment_data,new_url)				
			except:
				print 'craw failed'
			#测试用
			# if count==5:
			# 		break
		##爬取完成后，再进行数据的存储
		#self.outputer.output_html()
if __name__ == '__main__':

#针对可以直接在HTML的DOM树中找到的数据的情况
	#以下网址仅供样例用
	root_url="http://baidu.com"
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)

#针对由数据后台异步传JSON数据给前端页面展示的情况
	#以下网址仅供样例用
	root_url="http://baidu.com"
	obj_spider = SpiderMain()
	obj_spider.craw_all(root_url)
	obj_spider.craw_each()