# -*- coding: utf-8 -*-
"""
	基于贪心算法的旅行商问题解法Python源码
	
	Author:	Greatpan
	Date:	2018.9.30
"""
import pandas #导入pandas库,用于读取数据
import numpy as np 
import math
import matplotlib.pyplot as plt #导入matplotlib库,用于绘图

class Node:
	"""
	类名：Node
	其他说明：无
	"""
	def __init__(self,CityNum):
		"""
		函数名：__init__()
		函数功能：	初始化类Node
			输入	self：类本身,即Node,包含以下属性
					CityNum：城市数量
			输出	无
		其他说明：无
		"""
		self.visited=[False]*CityNum    #记录城市是否走过
		self.start=0                    #起点城市
		self.end=0                      #目标城市
		self.current=0                  #当前所处城市
		self.num=0                      #走过的城市数量
		self.pathsum=0                  #走过的总路程
		self.lb=0                       #当前结点的下界
		self.listc=[]                   #记录依次走过的城市

def GetData(datapath):
	"""
	函数名：GetData()
	函数功能：	从外界读取城市数据并处理
		输入	无
		输出	1 Position：各个城市的位置矩阵
			2 CityNum：城市数量
			3 Dist：城市间距离矩阵
	其他说明：无
	"""
	dataframe = pandas.read_csv(datapath,sep=" ",header=None) #读取数据
	Cities = dataframe.iloc[:,1:3]			#Cities:城市坐标矩阵
	Position= np.array(Cities)				#从城市A到B的距离矩阵
	CityNum=Position.shape[0]				#CityNum:代表城市数量
	Dist = np.zeros((CityNum,CityNum))		#Dist(i,j)：城市i与城市j间的距离

	#计算距离矩阵
	for i in range(CityNum): #计算距离矩阵
		for j in range(CityNum):
			if i==j:
				Dist[i,j] = math.inf #城市i到城市j的距离为无穷大
			else:
				Dist[i,j] = math.sqrt(np.sum((Position[i,:]-Position[j,:])**2)) #城市i到城市j的距离
	return Position,CityNum,Dist #返回城市位置矩阵，城市数量，城市间距离矩阵

def ResultShow(Min_Path,BestPath,CityNum,string):
	"""
	函数名：ResultShow()
	函数功能：	将结果输出到屏幕上
		输入	1 Min_Path：最短路径长度
			2 BestPath：最短路径
			3 CityNum：城市数量
			4 string：算法名称
		输出	无
	其他说明：无
	"""
	print("基于"+string+"求得的旅行商最短路径为：") #输出最短路径
	for m in range(CityNum):
		print(str(BestPath[m])+"—>",end="")
	print(BestPath[CityNum]) 
	print("总路径长为："+str(Min_Path)) #输出最短路径长度
	print() 

def draw(BestPath,Position,title):
	"""
	函数名：draw(BestPath,Position,title)
	函数功能：	通过最优路径将旅行商依次经过的城市在图表上绘制出来
		输入	1 	BestPath：最优路径
			2	Position：各个城市的位置矩阵
			3	title:图表的标题
		输出	无
	其他说明：无
	"""
	plt.title(title) #图表标题
	plt.plot(Position[:,0],Position[:,1],'bo') #绘制城市的位置
	for i,city in enumerate(Position): #绘制城市的编号
		plt.text(city[0], city[1], str(i)) #城市编号
	plt.plot(Position[BestPath, 0], Position[BestPath, 1], color='red') #绘制旅行商的路径
	plt.show() #显示图表
