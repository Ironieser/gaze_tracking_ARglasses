import dlib
import cv2
from sklearn.externals import joblib
import pandas as pd


class WorldDetect(object):
    def __init__(self):
        self.clf_world_x = joblib.load("model/world_x.pkl")
        self.clf_world_y = joblib.load("model/world_y.pkl")


    def detect(self,df):
        # 得到待预测的目标值
        self.world_x = self.clf_world_x.predict(df)
        self.world_y = self.clf_world_y.predict(df)
        print(self.world_x)
        print(self.world_y)


    def show(self,frame):
        b, g, r = cv2.split(frame)
        frame = cv2.merge([r, g, b])

        cv2.circle(frame, (self.world_x, self.world_y), 30, (0, 255, 0), 5)

        # 画十字标
        color = (255, 255, 0)

        cv2.line(frame, (self.world_x - 10, self.world_y), (self.world_x + 10, self.world_y), color, thickness=5)
        cv2.line(frame, (self.world_x, self.world_y - 10), (self.world_x, self.world_y + 10), color, thickness=5)

        return frame
