import os
import sys
import dlib
import cv2
import glob

detector = dlib.simple_object_detector("detector.svm")

current_path = os.getcwd()
test_folder = current_path + '/last/data/'

for f in glob.glob(test_folder+'*.jpg'):
    print("Processing file: {}".format(f))
    img = cv2.imread(f, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)
    img2 = cv2.merge([r, g, b])
    dets = detector(img2)
    print("Number of faces detected: {}".format(len(dets)))
    for index, face in enumerate(dets):
        print(dets)
        print('face {}; left {}; top {}; right {}; bottom {}'.format(index, face.left(), face.top(), face.right(), face.bottom()))

        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
        cv2.namedWindow("detect", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("detect", img)
        cv2.waitKey(0)

k = cv2.waitKey(0)
cv2.destroyAllWindows()