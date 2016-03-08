# coding:utf-8


#网页解析器
#对下载好的HTML文档进行解析，提取出感兴趣的内容
#更新时间：2016/3/8
#创建时间：2016/3/2
#作者：debbie

from bs4 import BeautifulSoup
import re,urlparse,json

class HtmlParser(object):
	
#针对可以直接在HTML的DOM树中找到的数据的情况
	#从下载的网页中提取URL
	def _get_new_urls(self,page_url,soup):
		new_urls=set()
		links=soup.find_all('a',href=re.compile(r"/subName/\w+"))
		for link in links:
			new_url = link['href']
			new_full_url=urlparse.urljoin(page_url,new_url)
			new_urls.add(new_full_url)
		return new_urls

	#从下载的网页中提取数据信息
	def _get_new_data(self,page_url,soup):
		res_data=[]
		contents=soup.find_all('div',class_='className')
		for content in contents:
			item=[]
			usr_node=content.find('a',href=re.compile(r"/subName/\w+"))
			usr=usr_node.get_text()
			cont_node=content.find('span',class_='className')
			cont=cont_node.get_text()
			item.append(usr)
			item.appned(cont)
			res_data.appned(item)
		return res_data

	#从下载网页中提取URL和数据信息
	def parse(self,page_url,html_cont):
		if page_url is None or html_cont is None:
			return 
		soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
		new_urls=self._get_new_urls(page_url,soup)
		new_data=self._get_new_data(page_url,soup)
		return new_urls,new_data

#针对由数据后台异步传JSON数据给前端页面展示的情况

	#解析根目录网页，提取存放json数据源的url信息
	def get_topic_data(self,html_cont,size):
		if html_cont is None:
			return 
		soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
		link=soup.find(text=re.compile(r"subString"))
		url = re.split('\"',link)		
		#url[1] =url[1].encode("UTF-8") 
		#x = str(url[1])
		full_url="http://baidu.com"+url[1]+"?size="+str(size)
		#print full_url
		return full_url

	#解析获得的JSON格式，提取其中有用的值
	def parse_topic(self,data_cont):
		#print type(data_cont)
		topic_urls=set()
		topic_data=[]
		#data_cont=data_cont.encode("utf8") 
		data=json.loads(data_cont)		
		for x in data["items"]:
			item=[]
			item.append(str(x["id"]))
			item.append(x["title"])
			url="http://www.baidu.com"+x["url"]
			topic_urls.add(url)			
			item.append(url)
			topic_data.append(item)
		#print topic_urls
		#print ','.join(topic_data[0])
		return topic_urls,topic_data

	#从每个字页面中找出存放json数据源的url信息
	def get_comment_data(self,page_url,html_cont,size):
		if page_url is None or html_cont is None:
			return 
		soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
		link=soup.find(text=re.compile(r"subString"))
		#print link
		url = re.split('\"',link)
		for x in url:
			if(re.search(r"/subName/",x)):
				full_url="http://baidu.com"+x+"?size="+str(size)
		#print url
		#new_urls=self._get_new_urls(page_url,soup)
		#new_data=self._get_new_data(page_url,soup)
		#print full_url
		return full_url

	#从得到的JSON格式的数据网页中，提取得到有用数据
	def parse_comment(self,data_cont):
		comment_data=[]
		data=json.loads(data_cont)
		for x in data["items"]:
			item=[]
			item.append(str(x["userId"]))
			item.append(x["time"])
			item.append(x["content"])
			comment_data.append(item)
		return comment_data

	