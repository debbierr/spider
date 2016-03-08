# coding:utf-8

#数据存储器
#对提取的数据进行整理和存储
#更新时间：2016/3/8
#创建时间：2016/3/2
#作者：debbie

import urllib2
import cookielib

class HtmlOutputer(object):
	def __init__(self):
		self.datas=[]

	#存储得到的根页面数据
	def collect_topic(self,topic_data):
		if topic_data is None:
			return
		fout=open('data.dat','w')		
		for item in topic_data:
			for x in item:
				x=x.encode("utf8") 
				fout.write(x)
				fout.write(' ')
			fout.write('\n')
		fout.close()	
			
	#存储得到的数据
	def collect_data(self,comment_data,url):
		if comment_data is None:
			return
		#self.datas.extend(data)
		arr_url=url.split('/')
		fname=arr_url[len(arr_url)-1]
		#单个进行存储时，存储文件用URL的文件路径命名
		fout=open('./data/'+fname+'.dat','w')		
		for item in comment_data:
			for x in item:
				x=x.encode("utf8") 
				fout.write(x)
				fout.write(' ')
			fout.write('\n')
		fout.close()

	#适用于不需要每个页面单独存储，而是爬取完成后汇总存储
	def output_html(self):
		fout=open('output.dat','w')
		fout.close()