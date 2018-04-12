# -*- coding: utf-8 -*-
# @Author: wwbn2753
# @Date:   2018-04-12 15:20:45
# @fileName: behavior_tree.py

"""
行为树
行为树=树+条件节点+行为节点+组合节点

树：是由节点通过指针拼接起来的
组合节点：顺序节点（and），选择节点（or）
条件节点与行为节点的逻辑不同，但是代码是基本一样的，除非扩展新功能
编辑器：腾讯的行为树编辑器，自己项目使用的编辑器（类似思维导图的树形结构）

暂时不考虑持续性的节点返回值

应用：使用到AI中，通过特定情况下执行AI，产生特定行为，驱动状态机。
"""


BT_NODE_RUN_RESULT_FAIL = 0
BT_NODE_RUN_RESULT_SUCCESS = 1

class TreeNode(object):
	def __init__(self, subject, parent = None, params = None):
		self._children = []
		self._parent = parent
		self._params = params
		self._subject = subject

	def addChild(self, childNode):
		self._children.append(childNode)

	def getChildren(self):
		return self._children

	def getParent(self):
		return self._parent

	#节点的特定接口
	def run(self):
		return BT_NODE_RUN_RESULT_FAIL

#条件节点
class ConditionNode(TreeNode):
	def run(self):
		funcName, args = self._params
		func = getattr(self._subject, funcName, None)
		if func:
			ret = func(*args)
			if not ret:
				return BT_NODE_RUN_RESULT_FAIL
			else:
				return BT_NODE_RUN_RESULT_SUCCESS

		return BT_NODE_RUN_RESULT_FAIL

#行为节点
class ActionNode(TreeNode):
	def run(self):
		funcName, args = self._params
		func = getattr(self._subject, funcName, None)
		if func:
			ret = func(*args)
			if not ret:
				return BT_NODE_RUN_RESULT_FAIL
			else:
				return BT_NODE_RUN_RESULT_SUCCESS

		return BT_NODE_RUN_RESULT_FAIL

#组合节点
class SequenceNode(TreeNode):
	def run(self):
		for childNode in self._children:
			ret = childNode.run()
			if ret == BT_NODE_RUN_RESULT_FAIL:
				return ret

		return BT_NODE_RUN_RESULT_SUCCESS

class SelectNode(TreeNode):
	def run(self):
		for childNode in self._children:
			ret = childNode.run()
			if ret != BT_NODE_RUN_RESULT_FAIL:
				return ret

		return BT_NODE_RUN_RESULT_FAIL


# treeCfg = {
# 	"type" : "SequenceNode",
# 	"child" : [
# 		{
# 			"type" : "ConditionNode",
# 			"params" : ["checkHp", [100]],
# 		},
# 		{
# 			"type" : "ActionNode",
# 			"params" : ["actAttack", []],
# 		},
# 	]
# }
def createBehaviorTree(subject, treeCfg, parent = None):
	#主体是subject，配置是treeCfg,parent是当前节点
	if not treeCfg:
		return

	#创建根节点
	nodeClass = globals()[treeCfg["type"]]
	node = nodeClass(subject, parent, treeCfg.get("params"))
	#创建孩子节点
	for childCfg in treeCfg.get("child", []):
		childNode = createBehaviorTree(subject, childCfg, parent = node)
		if childNode:
			node.addChild(childNode)
	return node




#=======================测试例子==========================
class Unit(object):
	def __init__(self):
		self._hp = 150
		self._aiObj = None

	def getHp(self):
		return self._hp

	def setAI(self, aiObj):
		self._aiObj = aiObj

	def runAI(self):
		if self._aiObj:
			self._aiObj.runAI()

class AI(object):
	def __init__(self, unit, treeCfg):
		self._unit = unit
		self._root = createBehaviorTree(self, treeCfg)

	def runAI(self):
		self._root.run()

	#条件
	def checkHp(self, hp):
		return self._unit.getHp() >= hp

	#行为
	def actAttack(self):
		print "攻击敌人"


treeCfg = {
	"type" : "SequenceNode",
	"child" : [
		{
			"type" : "ConditionNode",
			"params" : ["checkHp", [100]],
		},
		{
			"type" : "ActionNode",
			"params" : ["actAttack", []],
		},
	]
}

unit = Unit()
aiObj = AI(unit, treeCfg)

unit.setAI(aiObj)

unit.runAI()