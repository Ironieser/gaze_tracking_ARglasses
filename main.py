import os
import cv2
import glob
import pandas as pd
import numpy as np
from eye_detect import EyeDetect
from world_detect import WorldDetect
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from PIL import Image
import time


test_folder = "img_data/origin"
detect_eye = EyeDetect()
detect_world = WorldDetect()

# 定义编解码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('detect.avi',fourcc, 20.0, (1280,480))

df = pd.DataFrame(np.zeros((1, 6)), columns=[
    'eye_x', 'eye_y', 'pipil_x', 'pupil_y', 'pupil_w', 'pupil_h'])

file_list = os.listdir(test_folder)
num = len(file_list)
count = 0


for files in file_list:
    img_dir = os.path.join(test_folder, files)
    print("Processing file: {}".format(img_dir))
    print("这是第" + str(count+1) + "张图片, 共有" + str(num) + "张图片")
    frame = cv2.imread(img_dir, cv2.IMREAD_COLOR)

    world = frame[:, 0:640]
    frame = frame[:, 640:1280]

    detect_eye.detect(frame)
    detect_eye.show(frame)
    # out.write(frame)

    # cv2.namedWindow("detect_eye", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("detect_eye", frame)

    df.iloc[0, 0], df.iloc[0, 1], df.iloc[0, 2], df.iloc[0, 3], df.iloc[0, 4], \
    df.iloc[0, 5] = detect_eye.eye_x, detect_eye.eye_y, detect_eye.pupil_x, \
                    detect_eye.pupil_y, detect_eye.pupil_w, detect_eye.pupil_h


    detect_world.detect(df)
    world = detect_world.show(world)

    # cv2.namedWindow("detect_world", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("detect_world", world)

    output = np.hstack((world, frame))

    cv2.namedWindow("detect", cv2.WINDOW_AUTOSIZE)
    out.write(output)
    cv2.imshow("detect", output)

    cv2.waitKey(1)

    count+=1


k = cv2.waitKey(0)
cv2.destroyAllWindows()