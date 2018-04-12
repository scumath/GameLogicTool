# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 14:11:26
# @fileName: singleton.py


"""
目的：单例的多种实现方式
参考：https://www.cnblogs.com/huchong/p/8244279.html
第一种：构造一个单例的基类，修改__new__的实现，然后通过继承来获得单例功能，或者增加getInstance接口
第二种：使用metaclass，修改metaclass在__call__时的逻辑
第三种：全局变量的形式
第四种：使用装饰器对cls进行装饰
"""

#第一种，new
class Singleton(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = object.__new__(cls)  
		return cls._instance


class Examp1(Singleton):
	pass

a = Examp1()
b = Examp1()
print a is b

#第二种，metaclass(metaclass是用来创建类的，类是用来创建对象的)
class Singleton(type):
	def __init__(self, *args, **kwargs):
		self._instance = None
		super(Singleton, self).__init__(*args, **kwargs)
	
	def __call__(cls, *args, **kwargs):
		if not cls._instance:
			obj = cls.__new__(cls, *args, **kwargs)
			obj.__init__(*args, **kwargs)
			cls._instance = obj
		return cls._instance


class Examp2(object):
	__metaclass__ = Singleton

a = Examp2()
b = Examp2()
print a is b


#第三种：全局变量
class __SingletonClass(object):
	pass

singletonClassObj = __SingletonClass()
#外界只能使用singletonClassObj，不能使用__SingletonClass
a = singletonClassObj
b = singletonClassObj
print a is b


#第四种：装饰器，统一管理所有的单例(类进行__call__时调用相当于执行的_singleton)

def singletonDec(cls):
	clsMap = {}
	def _singleton(*args, **kwargs):
		if cls not in clsMap:
			clsMap[cls] = cls(*args, **kwargs)
		return clsMap[cls]

	return _singleton

@singletonDec
class Examp3(object):
	pass

a = Examp3()
b = Examp3()
print a is b

