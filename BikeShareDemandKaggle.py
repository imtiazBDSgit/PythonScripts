# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:34:42 2017

@author: imtiaz.a.khan
"""
#Kaggle Bike share demand regression Problem
# Compare Algorithms
import numpy
from pandas import read_csv,DatetimeIndex,DataFrame,to_csv
from matplotlib import pyplot
import seaborn as sns
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor

# load dataset
url = 'https://raw.githubusercontent.com/imtiazBDSgit/PythonScripts/master/bikesharedemand.csv'
train_df =read_csv(url)
temp = DatetimeIndex(train_df['datetime'])
train_df['hour']=temp.hour
train_df['day']=temp.day
train_df['season']=train_df['season'].astype('category')
train_df['holiday']=train_df['holiday'].astype('category')
train_df['workingday']=train_df['workingday'].astype('category')
train_df['hour']=train_df['hour'].astype('category')
train_df['day']=train_df['day'].astype('category')
corr = train_df.corr()

#correlation plot
corr = train_df.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)

X_train=train_df.drop(['casual','registered','count','datetime'],axis=1)
Y_train=train_df["count"]
# prepare models
models = []
models.append(('LR', LinearRegression()))
models.append(('Ridge', Ridge()))
models.append(('Lasso', Lasso()))
models.append(('ElasticNet', ElasticNet()))
models.append(('DTR', DecisionTreeRegressor()))
models.append(('KNN', KNeighborsRegressor()))
models.append(('SVM', SVR()))
# evaluate each model in turn
results = []
names = []
scoring = 'mean_squared_error'
for name, model in models:
    kfold = KFold(n=10886,n_folds=10, random_state=7)
    cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
# boxplot algorithm comparison
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(names)
pyplot.show()

# From the above analysis we can see , decision tree regressor is giving less value of mean squared error.
ensemblemodels = []
ensemblemodels.append(('ADB', AdaBoostRegressor()))
ensemblemodels.append(('BG', BaggingRegressor()))
ensemblemodels.append(('ET', ExtraTreesRegressor()))
ensemblemodels.append(('GB', GradientBoostingRegressor()))
ensemblemodels.append(('RF', RandomForestRegressor()))
scoring = 'mean_squared_error'
for name, model in ensemblemodels:
    kfold = KFold(n=10886,n_folds=10, random_state=7)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
 

fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(names)
pyplot.show()

#Clearly from the above ensembles RF wins the race , fixing the RF and building the model
#Model building using RF
rf = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=7)
rf.fit(X_train, Y_train)

#Testing the test set
#Loading the test set
test_df=read_csv('https://raw.githubusercontent.com/imtiazBDSgit/PythonScripts/master/bikesharedemandTest.csv')
temp_t = DatetimeIndex(test_df['datetime'])
test_df['hour']=temp_t.hour
test_df['day']=temp_t.day
test_ts = test_df.set_index('datetime')  
X_test=test_df.drop(['datetime'],axis=1)
X_test['season']=test_df['season'].astype('category')
X_test['holiday']=test_df['holiday'].astype('category')
X_test['workingday']=test_df['workingday'].astype('category')
X_test['hour']=test_df['hour'].astype('category')
X_test['day']=test_df['day'].astype('category')

#prediction

counts = rf.predict(X_test)

d = {'count': numpy.round(counts)}
submission = DataFrame(data=d,index=test_ts.index)
submission.to_csv("C:\\users\\imtiaz.a.khan\\submission.csv")



