# -*- coding = utf-8
import sys
from bs4 import BeautifulSoup #网页解析，获取数据
import re   #正则表达式，进行文字匹配
import urllib.request,urllib.error#制定url，获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行sqlite数据库操作


def main():
	print("start...")
	baseurl = "https://movie.douban.com/top250?start="
	#爬取网页
	dataList = getData(baseurl)
	savepath = r'/Users/randallstresure/Desktop/爬虫/data' 
	#保存数据
	#storeData(savepath)
	askURL("https://movie.douban.com/top250?start=")
	
	


#爬取网页
def getData(baseurl):
	dataList = []
	for i in range (0,10): #调用获取页面信息的函数10次
		url = baseurl + str(i * 25)
		html = askURL(url) #保存获取到的网页源码
	#逐一解析数据
		
	return dataList 


#得到指定一个URL的网页内容

def askURL(url):
	#make yourself like a real user （estimate head）
	head = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
	}
	request = urllib.request.Request(url,headers = head)
	html = ""
	try:
		response = urllib.request.urlopen(request)
		html = response.read().decode("utf-8")
		print(html)

	except urllib.error.URLError as e:
		if hasattr(e,"code"):
			print(e.code)
		if hasattr(e,"reason"):
			print(e.reason)

	return html















#保存数据
#def storeData(dbpath):


if __name__ == "__main__":
#调用函数
	main()
