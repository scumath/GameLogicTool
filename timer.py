# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 10:18:58
# @fileName: timer.py



"""
设计目标：
游戏的逻辑循环一般来说只是对定时器进行update，具体逻辑在定时器中实现，所以定时调度器是非常重要的工具。
在设计调度器时需要考虑：
（1）不同定时器如果有依赖会怎么样（游戏的逻辑应该保证定时器之间没有依赖），代码强制让早的定时器先update
（2）在同一帧，同时多次创建和删除定时器，应该满足时序问题，比如先加再删应该删掉此定时器。
（3）同一个函数，理论上应该只存在一个定时器中（也就是新的定时器会覆盖此函数的旧的定时器）

为解决这两个问题
（1）使用列表来管理定时器解决时序问题
（2）使用init和delete标记来解决同一帧多次创建和删除的问题
（3）为了加速定时器的查找，维护了多个字典方便快速查找
"""

import time
import uuid

class Timer(object):
	def __init__(self, interval, callback, times = 1):
		#每个interval时间，调用times次callback
		self._id = uuid.uuid1()
		self.init(interval, callback, times)

	def init(self, interval, callback, times):
		self._interval = interval
		self._callback = callback
		self._times = times
		self._leftTime = self._interval

		self._isInit = True
		self.isDelete = False

	def getId(self):
		return self._id

	def reloadTimer(self, interval, callback, times):
		self.init(interval, callback, times)

	def getCallback(self):
		return self._callback

	def update(self, dt):
		if self.isDelete:
			return

		if self._isInit:
			self._isInit = False
			return

		self._leftTime -= dt
		if self._leftTime <= 0:
			if self._times > 0:
				self._times -= 1
			if self._callback:
				self._callback()

			if self._times == 0:
				self.isDelete = True
			else:
				self._leftTime = self._interval


#需要支持快速通过id或者callback找到timer的功能
class Schedule(object):
	def __init__(self):
		self._timersById = {}
		self._timerQueue = []
		self._timersByCallback = {}
		self._lastUpdateTime = time.time()

	def addTimer(self, interval, callback, times = 1):
		self.delTimerByCallback(callback)

		timer = Timer(interval, callback, times)
		self._timerQueue.append(timer)
		self._timersById[timer.getId()] = timer
		if timer.getCallback() not in self._timersByCallback:
			self._timersByCallback[timer.getCallback()] = []

		self._timersByCallback[timer.getCallback()].append(timer.getId())

		return timer.getId()

	def delTimerById(self, timerId):
		if timerId in self._timersById:
			timer = self._timersById[timerId]
			timer.isDelete = True

	def delTimerByCallback(self, callback):
		timerIds = self.findTimersByCallback(callback)
		for timerId in timerIds or []:
			self.delTimerById(timerId)

	def findTimersByCallback(self, callback):
		return self._timersByCallback.get(callback)

	def update(self):
		#_timerQueue变量只可能增加不可能减少
		iterIndex = 0
		curTime = time.time()
		dt = curTime - self._lastUpdateTime
		self._lastUpdateTime = curTime
		while  iterIndex < len(self._timerQueue):
			timer = self._timerQueue[iterIndex]
			try:
				timer.update(dt)
			except:
				print "timer error callback=%s" % timer.getCallback()
				timer.isDelete = True
				pass
			iterIndex += 1

		#处理要删除的定时器
		for index in range(len(self._timerQueue) -1, -1, -1):
			timer = self._timerQueue[index]
			if timer.isDelete:
				del self._timerQueue[index]
				del self._timersById[timer.getId()]

				self._timersByCallback[timer.getCallback()].remove(timer.getId())
				if not self._timersByCallback[timer.getCallback()]:
					del self._timersByCallback[timer.getCallback()]

if __name__ == '__main__':
	scheduleObj = Schedule()

	def call1():
		print "call1"
		scheduleObj.addTimer(3, call2, 2)


	def call2():
		print "call2"
		scheduleObj.addTimer(4, call3, -1)

	def call3():
		print "call3"
		#触发异常，停止定时器的执行（结果未知）
		x = 1/0

	scheduleObj.addTimer(2, call1, 1)

	#简陋的游戏循环（1s1次）
	while True:
		scheduleObj.update()
		time.sleep(1)
