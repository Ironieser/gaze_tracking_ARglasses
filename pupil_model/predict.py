import os
import cv2
import glob
import dlib

detector_pupil = dlib.simple_object_detector("pupil.svm")
detector_frame = dlib.simple_object_detector("frame.svm")

test_folder = "../img_data/eyes/"

# 定义编解码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('predict.avi',fourcc, 20.0, (640,480))

for f in glob.glob(test_folder+'*.jpg'):
    print("Processing file: {}".format(f))
    img = cv2.imread(f, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)
    img2 = cv2.merge([r, g, b])
    dets_pupil = detector_pupil(img2)
    dets_frame = detector_frame(img2)
    print("Number of pupils detected: {}".format(len(dets_pupil)))
    for index, pupil in enumerate(dets_pupil):
        print(dets_pupil)
        print('pupil {}; left {}; top {}; right {}; bottom {}'.format(index, pupil.left(), pupil.top(), pupil.right(), pupil.bottom()))

        left = pupil.left()
        top = pupil.top()
        right = pupil.right()
        bottom = pupil.bottom()

        pupil_x = int((right+left)/2)
        pupil_y = int((top + bottom) / 2)

        cv2.rectangle(img, (left, top), (right, bottom), (255, 255, 0), 3)

        # 画十字标
        color = (0, 255, 0)

        cv2.line(img, (pupil_x - 30, pupil_y), (pupil_x + 30, pupil_y), color, thickness=2)
        cv2.line(img, (pupil_x, pupil_y - 30), (pupil_x, pupil_y + 30), color, thickness=2)

    print("Number of frames detected: {}".format(len(dets_frame)))
    for index, frame in enumerate(dets_frame):
        print(dets_frame)
        print('frame {}; left {}; top {}; right {}; bottom {}'.format(index, frame.left(), frame.top(), frame.right(), frame.bottom()))

        left = frame.left()
        top = frame.top()
        right = frame.right()
        bottom = frame.bottom()

        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)

    cv2.namedWindow("detect", cv2.WINDOW_AUTOSIZE)

    # 保存当前帧
    out.write(img)

    cv2.imshow("detect", img)
    cv2.waitKey(0)

k = cv2.waitKey(0)
cv2.destroyAllWindows()