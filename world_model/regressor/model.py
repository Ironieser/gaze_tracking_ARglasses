from sklearn.linear_model import SGDRegressor as SGDR
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor as GBR
from sklearn.externals import joblib
import pandas as pd


# 读取数据
point = pd.read_csv("../../csv_data/test.csv")
world_x = point["world_x"]
world_y = point["world_y"]

# 读取数据中的标签列
eye_x = point["eye_x"]
eye_y = point["eye_y"]
eye = pd.concat([eye_x, eye_y], axis=1)

# clf = SGDR(loss='huber',penalty='l2',alpha=0.01,max_iter=1000)
clf = GBR(max_depth=10)
clf.fit(eye, world_x)
joblib.dump(clf, "world_x.pkl")
print('得分：',clf.score(eye, world_x))

clf.fit(eye, world_y)
joblib.dump(clf, "world_y.pkl")
print('得分：',clf.score(eye, world_y))


# print('回归系数：',clf.coef_)
# print('偏差：',clf.intercept_)
