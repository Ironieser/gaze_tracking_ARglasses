from sklearn.externals import joblib
import pandas as pd


# 读取数据
point = pd.read_csv("../../csv_data/result.csv")
eye_x = point["eye_x"]
eye_y = point["eye_y"]
eye = pd.concat([eye_x, eye_y], axis=1)

# 导入模型
clf_world_x = joblib.load("world_x.pkl")
clf_world_y = joblib.load("world_y.pkl")
world_x = []
world_y = []

# 得到待预测的目标值
list = clf_world_x.predict(eye)
point["world_x_p"] = list
list = clf_world_y.predict(eye)
point["world_y_p"] = list
point.to_csv("../../csv_data/result.csv", encoding="utf-8")
print("success")


