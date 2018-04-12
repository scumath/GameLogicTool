# -*- coding: utf-8 -*-
# @Author: scumath
# @Date:   2018-04-12 17:01:44
# @fileName: profile_tool.py

"""
主要是了解一些监控并优化python运行速度，内存占用的工具
运行速度：profile，pstats
命令行方式：python -m profile singleton.py


内存：memory_profiler 
python -m memory_profiler del3.py 运行查看每一行的内存变化
mprof run test.py 生成随时间变化的内存曲线

内存泄露和循环引用：gc，objgraph,graphviz,heapy
http://python.jobbole.com/88827/
http://www.techweb.com.cn/network/system/2017-06-24/2540834.shtml
sys.getrefcount(obj)对象可以获得一个对象的引用数目，返回值是真实引用数目加1（加1的原因是obj被当做参数传入了getrefcount函数）
objgraph:objgraph.show_growth(),
objgraph.show_backrefs(a, max_depth=5, filename = "indirect.png")
用 heapy 查看分配对象随时间增长的差异，heapy能够显示对象持有的最大内存等;用Objgraph找backref链(例如：前4节)，尝试获取它们不能被释放的原因。
"""

#profile的使用
def foo():
	sum = 0
	for i in range(10000):
		sum += i
	return sum

from memory_profiler import profile
@profile
def memoryFoo():
	x = range(1000)
	y = range(20000)
	z = x + y

def refObj():
	x = "500"
	import sys
	print sys.getrefcount(x)

if __name__ == "__main__":
	
	#1. 直接将函数耗时显示到控制台
	import profile
	profile.run("foo()")

	#2. 将profile写到文件，然后使用pstats分析
	import profile
	profile.run("foo()", "profile.txt")
	import pstats
	p = pstats.Stats("profile.txt")
	p.sort_stats("time").print_stats()

	#3. 使用hotshot进行监控
	import hotshot
	import hotshot.stats
	prof = hotshot.Profile("hs_prof.txt", 1)
	prof.runcall(foo)
	prof.close()
	p = hotshot.stats.load("hs_prof.txt")
	p.print_stats()


	#4. 内存
	memoryFoo()

	#5. 引用
	refObj()