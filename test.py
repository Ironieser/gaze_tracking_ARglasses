from sklearn.linear_model import SGDRegressor
from sklearn.externals import joblib
import pandas as pd

point = pd.read_csv("csv_data/test.csv")
# 读取数据

eye_x = point["eye_x"]
eye_y = point["eye_y"]
eye = pd.concat([eye_x, eye_y], axis=1)
print(eye)

# 导入模型
clf_world_x = joblib.load("model/world_x.pkl")
world_x = []
# 得到待预测的目标值
list = clf_world_x.predict(eye)
point["world_x_p"] = list
point.to_csv("tools/points_result.csv", encoding="utf-8")

