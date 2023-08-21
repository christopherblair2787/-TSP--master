# -*- coding: utf-8 -*-
"""
	基于回溯法的旅行商问题解法Python源码
	#回溯法的思想是：从初始解出发，以深度优先的方式搜索解空间树，当搜索到某一节点时，先判断该节点是否包含问题的解
 	如果包含，就从该节点出发继续搜索下去，如果不包含，就跳过该节点，继续搜索其他的节点。
	下界：在回溯法中，用贪心算法求得的下界作为剪枝条件，即当当前路径长大于下界时，就不再继续搜索。
  	回溯法在用来求问题的所有解时，要回溯到根，且根节点的所有可行的子树都要已被搜索遍才结束。
	Author:	Greatpan
	Date:	2018.10.10
"""

import numpy as np
import time
from MyFuncTool import GetData,ResultShow,draw
import Greedy #导入贪心算法，用于求解下界，作为剪枝条件

def CalcPath_sum(layer,i):
	"""
		函数名：CalcPath_sum(layer,i)
		函数功能：计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离
			输入	1: layer 回溯所处的层数，也即所遍历的城市数
				2: i 当前层数下接下来要访问的子节点，即要访问的下一个城市
			输出	1: Path_sum 求的的是当前递归所处的层数的累积路径值+到下一个节点的距离
		其他说明：无
	"""
	#计算从初始城市到第layer层
	Path_sum = sum([Dist[city1][city2] for city1,city2 in zip(Curpath[:layer], Curpath[1:layer+1])]) #计算从初始城市到第layer层所经历的总距离,这里的layer是从0开始的，所以要+1

	#计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离
	Path_sum += Dist[Curpath[i-1]][i]

	return Path_sum #返回从初始城市到第layer层再到接下来的第i个城市所经历的总距离


def IsPrun(layer,i): 
	"""
	函数名：IsPrun(layer,i)
	函数功能：判断是否符合剪枝条件，符合则返回True,不符合则返回False
		输入	1: layer 回溯所处的层数，也即所遍历的城市数
			2: i 当前层数下接下来要访问的子节点，即要访问的下一个城市
		输出	1: 是——返回True，否——返回False
	其他说明：Path_sum 求的的是当前递归所处的层数的累积路径值+到下一个节点的距离
	"""
	Path_sum=CalcPath_sum(layer,i) #计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离,这里的layer是从0开始的，所以要+1

	# Path_sum值大于当前所求得的最小距离时则进行剪枝(True),否则不减枝(False)
	if Path_sum >= Cur_Min_Path:
		return True
	else:
		return False


def BackTrackingMethod(Dist,CityNum,layer):
	"""
	函数名：BackTrackingMethod(Dist,CityNum,layer)
	函数功能： 动态规划算法的程序入口
		输入	1 CityNum：城市数量
			2 Dist：城市间距离矩阵
            3 layer:旅行商所处层数，也即遍历的城市数
		输出	：无
	其他说明：无
	"""
	global Path_sum,Cur_Min_Path,Min_Path,BestPath #全局变量,用于存储最短路径值，最短路径，最优路径
	if(layer==CityNum): #当遍历到最后一个城市时，计算回到初始城市的路径长度
		Path_sum=CalcPath_sum(layer,0) #计算从初始城市到第layer层再到接下来的第i个城市所经历的总距离,这里的layer是从0开始的，所以要+1
		if(Path_sum<=Cur_Min_Path): #如果当前路径小于当前最小路径，则更新最小路径值，最小路径，最优路径
			Cur_Min_Path=Path_sum #更新当前最小路径值
			Min_Path=Cur_Min_Path #更新最小路径值
			BestPath=Curpath.tolist() #更新最优路径
			BestPath.append(0) #将最优路径的最后一个城市设置为初始城市,这里的0是城市的编号，不是城市的坐标
	else:
		for i in range(layer,CityNum):
			#判断是否符合剪枝条件，不符合则继续执行
			if IsPrun(layer,i): #如果符合剪枝条件，则跳过当前循环，继续下一次循环
				continue
			else:
				Curpath[i],Curpath[layer] = Curpath[layer],Curpath[i]  # 路径交换一下
				BackTrackingMethod(Dist, CityNum, layer+1) #递归调用,遍历下一层
				Curpath[i],Curpath[layer] = Curpath[layer],Curpath[i]  # 路径交换回来

##############################程序入口#########################################
if __name__ == "__main__":
	Position,CityNum,Dist = GetData("./data/TSP10cities.tsp") #获取数据
	Curpath = np.arange(CityNum) #初始化当前路径
	Min_Path=0 #最小路径值
	BestPath=[] #最优路径
	Cur_Min_Path = Greedy.GreedyMethond(CityNum,Dist)[0] #当前最小路径值,初始值为贪心算法的最小路径值，用于剪枝，若当前路径大于当前最小路径值，则进行剪枝

	start = time.clock()				#程序计时开始
	BackTrackingMethod(Dist,CityNum,1)	#调用回溯法
	end = time.clock()					#程序计时结束

	print()
	ResultShow(Min_Path,BestPath,CityNum,"回溯法") 
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"BackTracking Method")

"""
结果：
回溯法求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：0.245802962
"""
