#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 导入类库
from numpy.random import seed
seed(1)

import numpy as np
from numpy import arange
from matplotlib import pyplot
from pandas import read_csv
from pandas import  set_option
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt 
 


# In[2]:


filename = 'data.csv'
names = ['x1', 'x2', 'x3', 'x4', 'x5','x6','x7','x8','x9','y']
dataset = read_csv(filename, names=names)


# In[3]:


# 数据维度
print(dataset.shape)


# In[4]:


# 特征属性的字段类型
print(dataset.dtypes)


# In[5]:


# 查看最开始的10条记录
print(dataset.head(10))


# In[6]:


# 描述性统计信息
set_option('precision', 1)
print(dataset.describe())


# In[7]:


# 关联关系
set_option('precision', 2)
print(dataset.corr(method='pearson'))


# In[8]:


# 密度图
dataset.plot(kind='density', subplots=True, layout=(5,2), sharex=False, fontsize=1)
pyplot.show()


# In[9]:


# 箱线图
dataset.plot(kind='box', subplots=True, layout=(4,3), sharex=False, sharey=False, fontsize=8)
pyplot.show()


# In[10]:


# 相关矩阵图
fig = pyplot.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(dataset.corr(), vmin=-1, vmax=1, interpolation='none')
fig.colorbar(cax)
ticks = np.arange(0, 10, 1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(names)
ax.set_yticklabels(names)
pyplot.show()


# In[11]:


# 分离数据集
array = dataset.values
X = array[:, 0:9]
Y = array[:, 9]
validation_size = 0.2
 
X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y,test_size=validation_size)


# In[12]:


# 评估算法 - 评估标准
num_folds = 10
scoring = 'neg_mean_squared_error'


# In[13]:


# 评估算法 - baseline
models = {}
models['LR'] = LinearRegression()
models['LASSO'] = Lasso()
models['EN'] = ElasticNet()
models['KNN'] = KNeighborsRegressor()
models['CART'] = DecisionTreeRegressor()
models['SVM'] = SVR()
# 评估算法
results = []
for key in models:
    kfold = KFold(n_splits=num_folds )
    cv_result = cross_val_score(models[key], X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_result)
    print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))


# In[14]:


#评估算法 - 箱线图
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(models.keys())
pyplot.show()


# In[15]:


# 评估算法 - 正态化数据
pipelines = {}
pipelines['ScalerLR'] = Pipeline([('Scaler', StandardScaler()), ('LR', LinearRegression())])
pipelines['ScalerLASSO'] = Pipeline([('Scaler', StandardScaler()), ('LASSO', Lasso())])
pipelines['ScalerEN'] = Pipeline([('Scaler', StandardScaler()), ('EN', ElasticNet())])
pipelines['ScalerKNN'] = Pipeline([('Scaler', StandardScaler()), ('KNN', KNeighborsRegressor())])
pipelines['ScalerCART'] = Pipeline([('Scaler', StandardScaler()), ('CART', DecisionTreeRegressor())])
pipelines['ScalerSVM'] = Pipeline([('Scaler', StandardScaler()), ('SVM', SVR())])
results = []
for key in pipelines:
    kfold = KFold(n_splits=num_folds )
    cv_result = cross_val_score(pipelines[key], X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_result)
    print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))


# In[16]:


#评估算法 - 箱线图
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(models.keys())
pyplot.show()


# In[17]:


# 调参改进算法 - CART
scaler = StandardScaler().fit(X_train)
rescaledX = scaler.transform(X_train)
param_grid = { 'max_depth':list((3,6,9)),'min_samples_split': list((2,4,6)),'min_samples_leaf':list((1,2,4))}
model = DecisionTreeRegressor()
kfold = KFold(n_splits=num_folds )
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
grid_result = grid.fit(X=rescaledX, y=Y_train)

print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))
cv_results = zip(grid_result.cv_results_['mean_test_score'],
                 grid_result.cv_results_['std_test_score'],
                 grid_result.cv_results_['params'])
for mean, std, param in cv_results:
    print('%f (%f) with %r' % (mean, std, param))


# In[18]:


# 调参改进算法 - KNN
scaler = StandardScaler().fit(X_train)
rescaledX = scaler.transform(X_train)
param_grid = {'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]}
model = KNeighborsRegressor()
kfold = KFold(n_splits=num_folds )
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
grid_result = grid.fit(X=rescaledX, y=Y_train)

print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))
cv_results = zip(grid_result.cv_results_['mean_test_score'],
                 grid_result.cv_results_['std_test_score'],
                 grid_result.cv_results_['params'])
for mean, std, param in cv_results:
    print('%f (%f) with %r' % (mean, std, param))


# In[19]:


# 集成算法
ensembles = {}
ensembles['AB'] = Pipeline([('Scaler', StandardScaler()), ('AB', AdaBoostRegressor())])
ensembles['AB-KNN'] = Pipeline([('Scaler', StandardScaler()),('ABKNN', AdaBoostRegressor
                                                              (base_estimator=KNeighborsRegressor(n_neighbors=3)))])
ensembles['AB-CART'] = Pipeline([('Scaler', StandardScaler()), ('ABCART', AdaBoostRegressor
                                                                (DecisionTreeRegressor(max_depth= 9, min_samples_leaf=2, min_samples_split=6)))])
ensembles['RFR'] = Pipeline([('Scaler', StandardScaler()), ('RFR', RandomForestRegressor())])
ensembles['ETR'] = Pipeline([('Scaler', StandardScaler()), ('ETR', ExtraTreesRegressor())])
ensembles['GBR'] = Pipeline([('Scaler', StandardScaler()), ('GBR', GradientBoostingRegressor())])

results = []
for key in ensembles:
    kfold = KFold(n_splits=num_folds )
    cv_result = cross_val_score(ensembles[key], X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_result)
    print('%s: %f (%f)' % (key, cv_result.mean(), cv_result.std()))


# In[20]:


# 集成算法 - 箱线图
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(ensembles.keys())
pyplot.show()


# In[21]:


# 集成算法GBR - 调参
scaler = StandardScaler().fit(X_train)
rescaledX = scaler.transform(X_train)
param_grid = {'n_estimators': [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900]}
model = GradientBoostingRegressor()
kfold = KFold(n_splits=num_folds  )
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
grid_result = grid.fit(X=rescaledX, y=Y_train)
print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))


# In[22]:


# 集成算法ET - 调参
scaler = StandardScaler().fit(X_train)
rescaledX = scaler.transform(X_train)
param_grid = {'n_estimators': [5, 10, 20, 30, 40, 50, 60, 70, 80]}
model = ExtraTreesRegressor()
kfold = KFold(n_splits=num_folds )
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
grid_result = grid.fit(X=rescaledX, y=Y_train)
print('最优：%s 使用%s' % (grid_result.best_score_, grid_result.best_params_))


# In[23]:


#训练模型
scaler = StandardScaler().fit(X_train)
rescaledX = scaler.transform(X_train)
gbr = ExtraTreesRegressor(n_estimators=50)
gbr.fit(X=rescaledX, y=Y_train)


# In[24]:


# 评估算法模型
rescaledX_validation = scaler.transform(X_validation)
predictions = gbr.predict(rescaledX_validation)
print('MSE:  %s' % mean_squared_error(Y_validation, predictions))
print('MAE:  %s' % mean_absolute_error(Y_validation, predictions))
print('RMSE: %s' % np.sqrt(mean_squared_error(Y_validation, predictions)))
print('R2:   %s' % r2_score(Y_validation, predictions))


# In[25]:


plt.plot(Y_validation,linestyle=':',linewidth=3)
plt.plot(predictions,color='#666666' )
plt.show()

