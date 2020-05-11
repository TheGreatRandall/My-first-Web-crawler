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
	savepath = "students.xls"
	#保存数据
	dbPath = "movie.db"
	storeDataToDB(dataList,dbPath)
	storeData(dataList,savepath)
	#askURL("https://movie.douban.com/top250?start=")

findLink = re.compile(r'<a href="(.*?)">') #创建正则表达式对象，表示规则（字符串模式），影片详情的链接的规则
#image of movies
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) #re.S include changing line
#title of movies
findTitle = re.compile(r'<span class="title">(.*)</span>')
#rating of movies
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#number of rated people
findNumber = re.compile(r'<span>(\d*)人评价</span>')
#the  brief intro
findInq = re.compile(r'<span class="inq">(.*)</span>')
#find the bd(actor,actress,director,etc.)
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

	
	


#爬取网页
def getData(baseurl):
	dataList = []
	for i in range (0,10): #调用获取页面信息的函数10次
		url = baseurl + str(i * 25)
		html = askURL(url) #保存获取到的网页源码
	#逐一解析数据
		soup = BeautifulSoup(html,"html.parser")
		for item in soup.find_all('div',class_ = "item"):
			data = [] #保存一部电影的所有信息
			item = str(item)
			#影片详情的链接
			link = re.findall(findLink,item)[0] #re库来通过正则表达式查找指定字符串
			data.append(link)
			imgSrc = re.findall(findImgSrc,item)[0]
			data.append(imgSrc)
			
			Title = re.findall(findTitle,item) #could be only Chinese
			if len(Title) == 2:
				ctitle = Title[0]
				otitle = Title[1].replace("/","")
				data.append(ctitle)
				data.append(otitle)
			else:
				data.append(Title[0])
				data.append('') #占位
			
			rating = re.findall(findRating,item)[0]
			data.append(rating)
			
			number = re.findall(findNumber,item)[0]
			data.append(number)
			
			inq = re.findall(findInq,item)
			if len(inq) != 0:
				inq = inq[0].replace("。","")
				data.append(inq)
			else:
				data.append(" ")

			bd = re.findall(findBd,item)[0]	 
			bd = re.sub('<br(\s+)?/>(\s)?', " ",bd) #去掉br
			data.append(bd.strip()) #去掉前后空格


			dataList.append(data)  #把处理好的一部电影信息放入datalist

	



		
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
		

	except urllib.error.URLError as e:
		if hasattr(e,"code"):
			print(e.code)
		if hasattr(e,"reason"):
			print(e.reason)

	return html















#保存数据
def storeData(datalist,savepath):
	print("saving...")
	book = xlwt.Workbook(encoding="utf-8",style_compression = 0)
	sheet = book.add_sheet('doubanMovieTop250',cell_overwrite_ok=True)
	col = ("电影详情","图片链接","中文名","外文名","评分","评价数","概况","相关信息")
	for i in range(0,8):
		sheet.write(0,i,col[i]) #列名
	for i in range(0,250):
		print("第%d条" %(i+1))
		data = datalist[i]
		for j in range(0,8):
			sheet.write(i+1,j,data[j])

	book.save('students.xls')


def storeDataToDB(datalist,savepath):
	init_db(savepath)
	conn = sqlite3.connect(savepath)
	cur = conn.cursor()

	for data in datalist:
		for index in range(len(data)):
			data[index] = '"'+data[index]+'"'
		sql ='''
				insert into movie250(
				info_link,pic_link,cname,ename,score,rated,introduction,info)
				values(%s)'''%",".join(data)
		print(sql)
		#cur.execute(sql)
		#conn.commit()
	cur.close()
	conn.close()



	


def init_db(dbpath):
	sql = '''
		create table movie250
		(
		id integer primary key autoincrement,
		info_link text,
		pic_link text,
		cname varchar,
		ename varchar,
		score numeric,
		rated numeric,
		introduction text,
		info text
		)



	'''

	 # building data sheet
	conn = sqlite3.connect(dbpath)
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()
	conn.close()





if __name__ == "__main__":
#调用函数
	main()
	
