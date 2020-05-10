# -*- coding = utf-8
import sys
from bs4 import BeautifulSoup #网页解析，获取数据
import re   #正则表达式，进行文字匹配
import urllib.error urllib.request #制定url，获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行sqlite数据库操作


def main();
	print("start...")
	baseurl = "https://movie.douban.com/top250?start="
	#爬取网页
	dataList = getData(baseurl)
	savepath = r'/Users/randallstresure/Desktop/爬虫/data' 
	#保存数据
	
	


#爬取网页
def getData(baseurl):
	dataList = []
	#逐一解析数据
	return dataList 














#保存数据
def storeData(dbpath):



if __name__ == "__main__":
#调用函数
	main()
