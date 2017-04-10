# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 07:43:43 2017

@author: imtiaz.a.khan
"""
#Package used for association and frequent pattern mining
from orangecontrib.associate.fpgrowth import *
import pandas as pd

#enumerating all frequent itemsets with support greater than two transactions
DrugStoreData=pd.read_excel('C:/Users/imtiaz.a.khan/Desktop/datamining assignment 2/dataminingassignment2datasets/Cosmetics.xlsx',1)
DrugStoreData.head()
DrugStoreData.shape

#Association Mining 
X=DrugStoreData.ix[:,'Bag':].values==1
itemsets = dict(frequent_itemsets(X, .003))
rules = association_rules(itemsets, .90)
StatisticsOfRules=list(rules_stats(rules, itemsets, 14))
len(StatisticsOfRules)
OutputValues=[(a,b,c,d,g) for a,b,c,d,e,f,g,h in StatisticsOfRules]

namesOutput=['atecedent','consequent','support','confidence','lift']
OutputDataFrame=pd.DataFrame(OutputValues,columns=namesOutput)
OutputDataFrame=OutputDataFrame.sort(['lift'],ascending=False).reset_index(drop=True)
OutputDataFrame=OutputDataFrame.head(20)
OutputDataFrame['atecedentValues']='blank'
OutputDataFrame['consequentValues']='blank'

for index,t in OutputDataFrame['atecedent'].iteritems():
    p=[i for i in list(t)]
    OutputDataFrame['atecedentValues'][index]=list(DrugStoreData.columns[1:][p])

for index,t in OutputDataFrame['consequent'].iteritems():
    p=[i for i in list(t)]
    OutputDataFrame['consequentValues'][index]=list(DrugStoreData.columns[1:][p])    
   

sum(OutputDataFrame['lift']>1)
OutputDataFrame=OutputDataFrame.sort(['lift'],ascending=False).reset_index(drop=True)
OutputDataFrame.head(20)

OutputDataFrame.to_excel('CosmeticsAssociationMiningResults.xlsx')
