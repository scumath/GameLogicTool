# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 20:28:28
# @fileName: network.py


"""
https://www.cnblogs.com/jiu0821/p/6275685.html
1. 使用urlretrieve下载文件到本地文件中
2. 使用urllib的urlopen下载文件 
3. 使用requests下载文件
"""

url = 'http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2'
#1. 使用urlretrieve下载文件到本地文件中
def downloadFile(url):
	import urllib
	urllib.urlretrieve(url, "test0.zip", downCallback)

def downCallback(blocknum, blocksize, totalsize):
	'''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
	return	
	print "downCallback ", blocknum, blocksize, totalsize

downloadFile(url)

# 2. 使用urllib的urlopen下载文件 
def downloadFile2(url):
	import urllib2
	f = urllib2.urlopen(url)
	data = f.read()
	with open("test.zip", "wb") as code:
		code.write(data)

downloadFile2(url)

# 3. 使用requests下载文件
def downloadFile3(url):
	import requests
	f = requests.get(url)
	data = f.content
	with open("test1.zip", "wb") as code:
		code.write(data)

downloadFile3(url)