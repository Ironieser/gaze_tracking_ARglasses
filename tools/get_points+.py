import numpy as np
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from PIL import Image
import os
import time


count_l, count_r = 0, 0
count, num = 0, 0
df = pd.read_csv("../csv_data/points.csv")
print(df)
if df.empty == 1:
    print("empty")
    df = pd.DataFrame(np.zeros((1, 4)), columns=['world_x', 'world_y', 'eye_x', 'eye_y'])
    first = 1
    update = 1
    df_new = pd.DataFrame(np.zeros((1, 4)), columns=['world_x', 'world_y', 'eye_x', 'eye_y'])
else:
    first = 0
    update = 1
    df_new = pd.DataFrame(np.zeros((1, 4)), columns=['world_x', 'world_y', 'eye_x', 'eye_y'])


def on_press(event):
    global count_l, count_r, count, df, num, first, update, df_new
    print(event.button)

    if update == 1:
        df_new = pd.DataFrame(np.zeros((1, 4)), columns=['world_x', 'world_y', 'eye_x', 'eye_y'])
        print(update)

    if event.button == 1:
        update = 0
        count_l = 1
        df_new.iloc[0, 0] = int(event.xdata)
        df_new.iloc[0, 1] = int(event.ydata)
        print("左：", df_new.iloc[0, 0], df_new.iloc[0, 1])
    elif event.button == 3:
        update = 0
        count_r = 1
        df_new.iloc[0, 2] = int(event.xdata)-640
        df_new.iloc[0, 3] = int(event.ydata)
        print("右：", df_new.iloc[0, 2], df_new.iloc[0, 3])
    else:
        update = 0
        print("请点击关键点")

    if count_l == 1 and count_r == 1:
        count_l, count_r = 0, 0
        update = 1
        print(df_new)
        if first == 1:
            df = df_new
            first = 0
        else:
            df = pd.concat([df, df_new], axis=0, ignore_index=True)

        df.to_csv("../csv_data/points.csv")
        time.sleep(0.5)
        plt.close(1)
    else:
        pass


def get_point():
    global count, num, df, first
    path = input("请输入图片所在路径：")
    # path = "../test"
    file_list = os.listdir(path)
    num = len(file_list)
    # df = pd.DataFrame(np.zeros((num, 4)), columns=['world_x', 'world_y', 'eye_x', 'eye_y'])
    if first == 1:
        i = len(df.index)
    else:
        i = len(df.index) + 1
    print("从第"+str(i)+"张图片开始！")
    print("")
    for files in file_list:
        count += 1
        if count >= i:
            print("这是第"+str(count)+"张图片, 共有"+str(num)+"张图片")

            img_dir = os.path.join(path, files)

            fig = plt.figure(figsize=(12, 6))
            img = Image.open(img_dir)
            plt.title(files, fontsize=25)

            plt.imshow(img, animated=True)
            fig.canvas.mpl_connect('button_press_event', on_press)
            plt.show()
        else:
            pass


get_point()
print(df)
df.to_csv("../csv_data/points.csv")

