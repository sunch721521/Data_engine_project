#项目B
from efficient_apriori import apriori
import pandas as pd
data = pd.read_csv('订单表.csv',encoding='gbk').sort_values(by=['客户ID'])
orders_series = data.set_index('客户ID')['产品名称']
transactions = []
temp_index = 0
for i, v in orders_series.items():
	if i != temp_index:
		temp_set = set()
		temp_index = i
		temp_set.add(v)
		transactions.append(temp_set)
	else:
		temp_set.add(v)      
itemsets, rules = apriori(transactions, min_support=0.02,  min_confidence=0.5
print('频繁项集：',itemsets)
print('关联规则: ',rules)