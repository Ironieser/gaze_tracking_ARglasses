import os
import time

import cv2
import numpy as np
import pandas as pd

from app.pupil_master.library.eye_detect import EyeDetect
from app.pupil_master.library.world_detect import WorldDetect


class PupilTrack(object):
    def __init__(self):
        # self.data_video_origin = "app/pupil_master/Data/data_video/test.avi"
        self.data_video_record = "app/pupil_master/Data/data_video/main_cam_d.avi"

        # self.cap = cv2.VideoCapture(self.data_video_origin)  # 参数为视频文件目录

        self.webcam1 = cv2.VideoCapture(0)  # world
        self.webcam2 = cv2.VideoCapture(1)  # eye

        self.detect_eye = EyeDetect()
        self.detect_world = WorldDetect()

        # 定义编解码器并创建 VideoWriter 对象
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(self.data_video_record, fourcc, 20.0, (1280, 480))

        self.df = pd.DataFrame(
            np.zeros((1, 6)),
            columns=["eye_x", "eye_y", "pipil_x", "pupil_y", "pupil_w", "pupil_h"],
        )

    def draw_circle(self):
        cv2.circle(
            self.world,
            (self.detect_world.world_x, self.detect_world.world_y),
            30,
            (0, 255, 0),
            5,
        )
        # 画十字标
        cv2.line(
            self.world,
            (self.detect_world.world_x - 10, self.detect_world.world_y),
            (self.detect_world.world_x + 10, self.detect_world.world_y),
            (255, 255, 0),
            thickness=5,
        )
        cv2.line(
            self.world,
            (self.detect_world.world_x, self.detect_world.world_y - 10),
            (self.detect_world.world_x, self.detect_world.world_y + 10),
            (255, 255, 0),
            thickness=5,
        )

        cv2.rectangle(
            self.eye,
            (self.detect_eye.pupil_x, self.detect_eye.pupil_y),
            (
                self.detect_eye.pupil_x + self.detect_eye.pupil_w,
                self.detect_eye.pupil_y + self.detect_eye.pupil_h,
            ),
            (150, 255, 0),
            3,
        )
        cv2.rectangle(
            self.eye,
            (self.detect_eye.eye_x, self.detect_eye.eye_y),
            (
                self.detect_eye.eye_x + self.detect_eye.eye_w,
                self.detect_eye.eye_y + self.detect_eye.eye_h,
            ),
            (0, 255, 0),
            3,
        )
        # 画十字标
        cv2.line(
            self.eye,
            (self.detect_eye.pupil_c_x - 30, self.detect_eye.pupil_c_y),
            (self.detect_eye.pupil_c_x + 30, self.detect_eye.pupil_c_y),
            (255, 255, 0),
            thickness=2,
        )
        cv2.line(
            self.eye,
            (self.detect_eye.pupil_c_x, self.detect_eye.pupil_c_y - 30),
            (self.detect_eye.pupil_c_x, self.detect_eye.pupil_c_y + 30),
            (255, 255, 0),
            thickness=2,
        )

        return self.world, self.eye

    def load(self):
        (
            self.df.iloc[0, 0],
            self.df.iloc[0, 1],
            self.df.iloc[0, 2],
            self.df.iloc[0, 3],
            self.df.iloc[0, 4],
            self.df.iloc[0, 5],
        ) = (
            self.detect_eye.eye_x,
            self.detect_eye.eye_y,
            self.detect_eye.pupil_x,
            self.detect_eye.pupil_y,
            self.detect_eye.pupil_w,
            self.detect_eye.pupil_h,
        )

    def display(self):
        os.system("cls")
        print("Pupil Smart console")
        print("eye_x:", round(self.detect_eye.eye_x, 1), end="   ")
        print("eye_y:", round(self.detect_eye.eye_y, 1))
        print("----------------------------")
        print("pupil_x:", round(self.detect_eye.pupil_x, 1), end="   ")
        print("pupil_y:", round(self.detect_eye.pupil_y, 1))
        print("pupil_w:", round(self.detect_eye.pupil_w, 1), end="   ")
        print("pupil_h:", round(self.detect_eye.pupil_h, 1))
        print("----------------------------")
        print("word_x:", round(self.world_x[0], 1), end="   ")
        print("word_y:", round(self.world_y[0], 1))
        print("----------------------------")
        print(" ")

    def track(self):
        # ret, frame = self.cap.read()
        ret, frame1 = self.webcam1.read()
        ret, frame2 = self.webcam2.read()

        if ret is False:
            print("采集结束")
            output = 255 * np.ones([480, 1280, 3], np.uint8)
            return ret, output
        else:
            self.world = cv2.resize(frame1, (640, 480))
            self.eye = cv2.resize(frame2, (640, 480))
            # self.world = frame[:, 0:640]
            # self.eye = frame[:, 640:1280]

            self.detect_eye.detect(self.eye)
            self.load()
            self.world_x, self.world_y = self.detect_world.detect(self.df)
            self.display()
            self.world, self.eye = self.draw_circle()

            output = np.hstack((self.world, self.eye))
            self.out.write(output)

            return ret, output

