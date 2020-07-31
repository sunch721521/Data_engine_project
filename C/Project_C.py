from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
data = pd.read_csv('CarPrice_Assignment.csv')#载入数据
train_x = data.drop(['car_ID'],axis=1)#去除无列
# 使用LabelEncoder
from sklearn.preprocessing import LabelEncoder
columns = ['CarName','fueltype','aspiration','doornumber','carbody','drivewheel','enginelocation','enginetype','cylindernumber','fuelsystem']#待转化字段
le = LabelEncoder()
for column in columns:
    train_x[column] = le.fit_transform(train_x[column])
# 将数据归化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
# 使用K-Means 手肘法
import matplotlib.pyplot as plt
sse = []
for k in range(1, 20):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 20)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()
#由手肘法可取K=8
kmeans = KMeans(n_clusters=8)#尝试将数据分为8类
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u'聚类结果'},axis=1,inplace=True)
result.to_csv('CarPrice_Assignment_cluster_results.csv',index=False)
VWs=['vokswagen rabbit','volkswagen 1131 deluxe sedan','volkswagen model 111','volkswagen type 3','volkswagen 411 (sw)','volkswagen super beetle','volkswagen dasher','vw dasher','vw rabbit','volkswagen rabbit','volkswagen rabbit custom']
#找出VW车型竞品车型
for VW in VWs:
	Num = result[result['CarName'].isin([VW])]['聚类结果'].tolist()
	Cars = result.loc[result['聚类结果']==int(Num[0])]['CarName']
	Cars_list=[]
	for car in Cars:
		if car != VW:
			Cars_list.append(car)
	print(VW+'的竞品车型：')
	print(Cars_list)
	

    
	

