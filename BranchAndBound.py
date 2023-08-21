# -*- coding: utf-8 -*-
"""
	基于分支限定法的旅行商问题解法Python源码
	分支限定法的思想是：基于广度优先搜索，每次扩展当前路径的下一个节点，直到扩展到叶子节点，然后回溯到上一个节点，继续扩展其余的节点，直到扩展完所有的节点。
 	其中下一个节点的选择是基于贪心算法，即选择当前节点到其余未访问节点的最小路径的节点。
	上界：贪心算法求得的最优路径长，如果大于当前最优路径长，则不再继续扩展当前路径。
	下界：对于当前节点，如果将其余未访问的节点加入到当前路径中，那么得到的路径长度一定小于或等于当前最优路径长度，因此，将当前节点的路径长度加上剩余节点的最小路径长度，即为当前节点的下界。
	Author:	Greatpan
	Date:	2018.10.3
"""

import math
import time
from queue import Queue
import Greedy #导入贪心算法,用于求取目标函数的上界
from MyFuncTool import GetData,ResultShow,draw,Node


def get_up(CityNum,Dist):
	"""
		函数名：get_up(CityNum,Dist)
		函数功能：	通过贪心算法求取目标函数的上界
			输入	1 	CityNum：城市数量
				2	Dist：城市间距离矩阵
			输出	1 Path_Up：分支界限法的上界
		其他说明：无
	"""
	Path_Up=Greedy.GreedyMethond(CityNum,Dist)[0] #贪心算法求取目标函数的上界
	return Path_Up


def get_lb(node):
	"""
		函数名：get_lb(node)
		函数功能：	获取旅行商在走到node（城市）点时，到走完全程最小路程
			输入	1 	node：Node类结构数据，node点记录了旅行商走过城市的路径，
				以及还未遍历的城市的信息。
			输出	1	Min_Path:表示旅行商处于node时，接下来要走完全程不可能低于的
				路程值，即node点的下界。
		其他说明：无
	"""
	Min_Path=node.pathsum*2
	#从起点到未遍历城市中的最近一个城市的距离
	min1=math.inf 
	for i in range(CityNum): #遍历所有城市 
		if node.visited[i]==False and min1>Dist[i][node.start]: #如果该城市未被遍历过，且距离起点最近
			min1=Dist[i][node.start] #更新最小距离，即从起点到未遍历城市中的最近一个城市的距离
	Min_Path=Min_Path+min1 if min1!=math.inf else Min_Path #如果min1不是无穷大，说明有未遍历的城市，更新Min_Path

	#从终点到未遍历城市中的最近一个城市的距离
	min2=math.inf
	for i in range(CityNum): #遍历所有城市
		if node.visited[i]==False and min2>Dist[node.end][i]: #如果该城市未被遍历过，且距离终点最近
			min2=Dist[node.end][i] #更新最小距离，即从终点到未遍历城市中的最近一个城市的距离
	Min_Path=Min_Path+min2 if min2!=math.inf else Min_Path #如果min2不是无穷大，说明有未遍历的城市，更新Min_Path

	#求所有未遍历的城市，去和离开的两个最小距离
	for i in range(CityNum): 
		if node.visited[i]==False: #如果该城市未被遍历过
			min1=min2=math.inf 
			#该循环主要是找到去第i个未遍历的城市的最小距离 
			for j in range(CityNum): 	
				if min1 > Dist[i][j]: #如果第i个未遍历的城市离开的最小距离大于Dist[i][j]即从第i个未遍历的城市离开的最小距离
					min1=Dist[i][j] #更新最小距离
					temp=j #记录下标
			#该循环主要是从第i个未遍历的城市离开的最小距离
			for k in range(CityNum):
				if min2 > Dist[k][i] and k!=temp: #如果第i个未遍历的城市离开的最小距离大于Dist[k][i]即从第i个未遍历的城市离开的最小距离
					min2=Dist[i][k] #更新最小距离
			Min_Path=Min_Path+min1 if min1!=math.inf else Min_Path #如果min1不是无穷大，说明有未遍历的城市，更新Min_Path
			Min_Path=Min_Path+min2 if min2!=math.inf else Min_Path #如果min2不是无穷大，说明有未遍历的城市，更新Min_Path
	return Min_Path/2 #返回旅行商在走到node（城市）点时，到走完全程最小路程，即node点的下界,除以2是因为上面的计算是两倍的路程


def create_node(cur_node,next_city):
	"""
		函数名：create_node(cur_node,next_city)
		函数功能：	根据当前的点构建走向下一个城市的点信息
			输入	1 	cur_node：从出发点到当前城市节点信息
				2	next_city：下一个城市
			输出	1	next_node:表示从出发点到当前城市下一个城市的节点信息
		其他说明：无
	"""
	next_node=Node(CityNum)
	next_node.start=cur_node.start 		#沿着cur_node走到next，起点不变 
	next_node.pathsum=cur_node.pathsum+Dist[cur_node.end][next_city]	#更新当前走过的路程值
	next_node.end=next_city 			#更新最后一个点
	next_node.num=cur_node.num+1		#更新走过的城市数量
	next_node.listc=cur_node.listc.copy() #复制走过的城市的路径
	next_node.listc.append(next_city)	#更新走过的城市的路径
	next_node.visited=cur_node.visited.copy() #复制走过的城市的标记
	next_node.visited[next_city] = True	#将nextcity标为已经走过了
	next_node.lb = get_lb(next_node);	#求目标函数

	return next_node

def BaBMethod(CityNum,Dist):
	"""
		函数名：BaBMethod(CityNum,Dist)
		函数功能：	分支限定算法核心
			输入	1 	CityNum：城市数量
				2	Dist：城市间距离矩阵
			输出	1 Min_Path：最优路径长
				2 cur_node：最优路径
		其他说明：无
	"""
	Path_Up=get_up(CityNum,Dist) #求上界，即最小生成树的两倍，因为旅行商问题的最优解一定小于最小生成树的两倍

	node=Node(CityNum)	#出发城市的节点信息
	node.end=0 			#结束点到0结束(当前路径的结束点)
	node.num+=1 		#遍历过得点数，初始1个
	node.listc.append(0) #将出发点加入路径，初始为0
	node.visited[0]=True #将出发点标记为已经遍历过了
	node.lb=Path_Up 	#初始目标值等于上界
	
	Min_Path=math.inf 	#Min_Path是问题的最终解
	pri_queue = Queue() #创建一个优先队列
	pri_queue.put(node) #将起点加入队列
	while pri_queue.qsize()!=0: #当队列不为空时
		cur_node=pri_queue.get() #取出队列中的第一个元素
		#判断是否将所有城市都遍历完成
		if cur_node.num==CityNum: #如果遍历过的城市数量等于城市数量
			ans=cur_node.pathsum+Dist[cur_node.start][cur_node.end]	 	#总的路径消耗
			Path_Up=min(ans,Path_Up)				#上界更新为更接近目标的ans值
			if(Min_Path>ans): 						#如果ans更小，说明找到了更优解
				Min_Path=ans					#更新最优解
				BestPath=cur_node.listc.copy() 

		#当前点可以向下扩展的点入优先级队列
		for i in range(CityNum):
			if cur_node.visited[i]==False: #如果第i个城市没有被遍历过
				next_node=create_node(cur_node,i) #构建从当前点到第i个城市的节点信息，即下一个节点
				if next_node.lb>=Path_Up: #如果下界大于上界，说明不是最优解，不需要继续扩展
					continue
				pri_queue.put(next_node) #将下一个节点加入优先级队列
	BestPath.append(0) #将起点加入最优路径
	return Min_Path,BestPath #返回最优路径长和最优路径

##############################程序入口#########################################
if __name__ == "__main__": 
	Position,CityNum,Dist = GetData("./data/TSP10cities.tsp") #获取数据
	
	start = time.clock()				#程序计时开始
	Min_Path,BestPath=BaBMethod(CityNum,Dist)	#调用分支限定法
	end = time.clock()					#程序计时结束
	
	print()
	ResultShow(Min_Path,BestPath,CityNum,"分支限定法")
	print("程序的运行时间是：%s"%(end-start))
	draw(BestPath,Position,"Branch And Bound Method")
"""
结果：
贪心法求得最短旅行商经过所有城市回到原城市的最短路径为：
0->4->6->7->1->3->2->5->8->9->0
总路径长为：10127.552143541276

程序的运行时间是：0.10620661
"""
