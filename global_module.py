# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 16:02:52
# @fileName: global_module.py

"""
探讨了__builtin__，__builtins__，builtins的联系与区别
https://www.cnblogs.com/jasonzeng888/p/6477752.html

内置模块：python2  __builtin__,python3 builtins
__builtins__：在__main__中是__builtin__的应用，在非__main__中是__builtin__.__dict__真傻逼。（__main__是指这个py文件作为程序入口）
游戏内入口函数一般不会做builtin的事情，所以通常使用__builtins__[key]没问题。
"""

def initModules():
	import __builtin__
	import math
	__builtin__.__dict__["math"] = math

def initModules2():
	import math
	__builtins__["math"] = math

def initModules3():
	import math
	__builtins__.__dict__["math"] = math

def main():
	print math

initModules()
main()






