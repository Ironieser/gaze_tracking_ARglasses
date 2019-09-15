import os
import cv2
import glob
import dlib

detector_world = dlib.simple_object_detector("world.svm")

test_folder = "../img_data/world/"

# 定义编解码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('predict.avi',fourcc, 20.0, (640,480))

for f in glob.glob(test_folder+'*.jpg'):
    print("Processing file: {}".format(f))
    img = cv2.imread(f, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)
    img2 = cv2.merge([r, g, b])
    dets_world = detector_world(img2)
    print("Number of worlds detected: {}".format(len(dets_world)))
    for index, world in enumerate(dets_world):
        print(dets_world)
        print('world {}; left {}; top {}; right {}; bottom {}'.format(index, world.left(), world.top(), world.right(), world.bottom()))

        left = world.left()
        top = world.top()
        right = world.right()
        bottom = world.bottom()

        world_x = int((right+left)/2)
        world_y = int((top + bottom) / 2)

        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)

        # 画十字标
        color = (100, 255, 0)

        cv2.line(img, (world_x - 30, world_y), (world_x + 30, world_y), color, thickness=2)
        cv2.line(img, (world_x, world_y - 30), (world_x, world_y + 30), color, thickness=2)

    # 保存当前帧
    out.write(img)

    cv2.imshow("detect", img)
    cv2.waitKey(0)

k = cv2.waitKey(0)
cv2.destroyAllWindows()