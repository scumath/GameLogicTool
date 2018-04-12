# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 14:38:06
# @fileName: listener.py


"""
监听者模式：
常见的用途是：逻辑或者界面去监听数据的变化，当数据改变时刷新界面的显示。

"""

#监听者和被监听者的协议
class EventProtocal(object):
	def __init__(self):
		#自己被哪些对象监听的map(用于事件的派发)
		self._listenedMap = {}
		#自己监听了哪些对象（用于自己销毁时自动清理自己监听的事件）
		self._listenMap = {}

	def listenMsg(self, dispatcher, msg, func):
		#自己监听dispatcher的消息
		
		if msg not in self._listenMap:
			self._listenMap[msg] = {}

		if dispatcher not in self._listenMap[msg]:
			self._listenMap[msg][dispatcher] = {}

		self._listenMap[msg][dispatcher][func] = True

		#dispatcher记录哪些对象监听了他
		dispatcher.__listenedMsg(self, msg, func)
	
	def __listenedMsg(self, listener, msg, func):
		#自己被listener监听
		if msg not in self._listenedMap:
			self._listenedMap[msg] = {}
		if listener not in self._listenedMap[msg]:
			self._listenedMap[msg][listener] = {}
		self._listenedMap[msg][listener][func] = True

	def dispatchMsg(self, msg, *args, **kwargs):
		if msg not in self._listenedMap:
			return

		for funcMap in self._listenedMap[msg].values():
			for func in funcMap.keys():
				if func:
					func(*args, **kwargs)

	def unlistenMsg(self, dispatcher, msg):
		if msg in self._listenMap:
			if dispatcher in self._listenMap[msg]:
				del self._listenMap[msg][dispatcher]

		dispatcher.__unlistenedMsg(self, msg)

	def __unlistenedMsg(self, listener, msg):
		if msg in self._listenedMap:
			if listener in self._listenedMap[msg]:
				del self._listenedMap[msg][listener]

	def clearListenMsg(self):
		#监听的消息清理
		for msg, dispatchers in self._listenMap.items():
			for dispatcher in dispatchers.keys():
				self.unlistenMsg(dispatcher, msg)
		# self._listenMap = {}

	def clearListenedMsg(self):
		#被监听的消息清理
		for msg, listeners in self._listenedMap.items():
			for listener in listeners.keys():
				listener.unlistenMsg(self, msg)
		# self._listenedMap = {}

	def release(self):
		self.clearListenMsg()
		self.clearListenedMsg()


#被监听者（数据）
class Data(EventProtocal):
	def __init__(self):
		super(Data, self).__init__()
		self._data = {}

	def changeData(self, key, value):
		self._data[key] = value
		self.dispatchMsg("DATA_CHANGED", key, value)

#监听数据变化的UI
class UI(EventProtocal):
	def __init__(self):
		super(UI, self).__init__()

	def onDataChanged(self, key, value):
		print "数据改变，UI收到数据改变的通知，利用数据刷新界面。", key, value

dispatcher = Data()
listener = UI()

listener.listenMsg(dispatcher, "DATA_CHANGED", listener.onDataChanged)
dispatcher.changeData("name", "scu")
dispatcher.changeData("name", "math")

dispatcher.release()
listener.release()
