# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 20:10:39
# @fileName: log.py

import time

class Log(object):
	def info(self, key, msg):
		#可以考虑把日志写到控制台，或者文件，或者sa
		print "%s %s %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), key, msg)

	def error(self, key, msg):
		print "%s %s %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), key, msg)

class LogMgr(object):
	def __init__(self):
		self._logs = {}

	def getLog(self, logName):
		if logName not in  self._logs:
			self._logs[logName] = Log()
		return self._logs[logName]

logMgr = LogMgr()

log = logMgr.getLog("test")
log.info("moduleName", "detail desc")











