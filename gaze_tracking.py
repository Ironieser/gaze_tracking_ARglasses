import cv2
import numpy as np


class GazeTracking(object):

    def __init__(self, frame, average_iris_size = 0.20):
        self.frame = frame
        self.average_iris_size = average_iris_size

    @staticmethod
    def pupil_size(iris_frame):
        """
        返回虹膜占据眼睛的表面空间的百分比。
        """
        height, width = iris_frame.shape[:2]
        nb_pixels = height * width
        nb_blacks = nb_pixels - cv2.countNonZero(iris_frame)  # 虹膜像素数
        return nb_blacks / nb_pixels

    @staticmethod
    def image_processing(frame, threshold):
        # 双边滤波 邻域直径:10，空间高斯函数标准差:15，灰度值相似性高斯函数标准差:15
        new_frame = cv2.bilateralFilter(frame, 10, 15, 15)

        # 腐蚀
        # iteration的值越高，模糊程度(腐蚀程度)就越高呈正相关关系
        # 感觉不用 腐蚀 的话，识别度跟高
        # kernel = np.ones((3, 3), np.uint8)
        # new_frame = cv2.erode(new_frame, kernel, iterations=3)
        # cv2.imwrite("data/eye_frame_bilateralFilter_erode.jpg", new_frame)

        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1]

        return new_frame

    def find_best_threshold(self, frame):
        trials = {}

        for threshold in range(30, 100, 2):
            iris_frame = self.image_processing(frame, threshold)
            trials[threshold] = self.pupil_size(iris_frame)

        # 以 abs(iris_size - average_iris_size) 为关键，求最小项
        best_threshold, iris_size = min(trials.items(), key=(lambda p: abs(p[1] - self.average_iris_size)))

        return best_threshold

    def pretreat(self):
        # 裁切图片
        height, width = self.frame.shape[:2]
        self.frame = self.frame[100:height-100, 100:width-50]

        # 缩小尺寸
        self.frame = cv2.resize(self.frame, (int(width / 10), int(height / 10)))

        # 灰度化，双边滤波
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        new_frame = cv2.bilateralFilter(gray, 10, 15, 15)
        cv2.imshow("bilateralFilter", new_frame)
        return new_frame

    @staticmethod
    def add_border(new_frame):
        # 加白边
        height, width = new_frame.shape[:2]
        white_l = 255 * np.ones((height, 2), np.uint8)  # 白底左右
        white_t = 255 * np.ones((2, width + 4), np.uint8)  # 白底上下

        new_frame = np.concatenate((new_frame, white_l), axis=1)
        new_frame = np.concatenate((white_l, new_frame), axis=1)
        new_frame = np.concatenate((new_frame, white_t), axis=0)
        new_frame = np.concatenate((white_t, new_frame), axis=0)

        return new_frame

    @staticmethod
    def find_iris_cnt(new_frame):
        # 从二值化虹膜图像中找出轮廓
        _, contours, _ = cv2.findContours(new_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # 将找出的轮廓按面积排序
        contours = sorted(contours, key=cv2.contourArea)
        # 虹膜即为面积第二大的
        iris_cnt = contours[-2]

        # 提取轮廓面积前2大的
        iris_frame = cv2.cvtColor(new_frame.copy(), cv2.COLOR_BAYER_GR2BGR)
        imag_2 = cv2.drawContours(iris_frame.copy(), [contours[-2]], 0, (0, 255, 0), 2)
        imag_1 = cv2.drawContours(iris_frame.copy(), [contours[-1]], 0, (255, 0, 0), 2)
        cv2.imshow("contours_2", imag_2)
        # cv2.imshow("contours_1", imag_1)

        return iris_cnt

    def detect_iris(self, iris_cnt):
        self.x, self.y = 0, 0
        # 计算质心
        try:
            # 提取轮廓几何特征，计算质心
            moments = cv2.moments(iris_cnt)
            self.x = int(moments['m10'] / moments['m00']) - 2
            self.y = int(moments['m01'] / moments['m00']) + 2
        except (IndexError, ZeroDivisionError):
            pass

        # 画十字标
        color = (0, 255, 0)

        cv2.line(self.frame, (self.x - 3, self.y), (self.x + 3, self.y), color, thickness=2)
        cv2.line(self.frame, (self.x, self.y - 3), (self.x, self.y + 3), color, thickness=2)
        cv2.imshow("target", self.frame)

    def analyze(self):
        new_frame = self.pretreat()
        best_threshold = self.find_best_threshold(new_frame)
        print("best_threshold:", best_threshold)

        new_frame = cv2.threshold(new_frame, best_threshold, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow("binary image", new_frame)

        new_frame = self.add_border(new_frame)
        iris_cnt = self.find_iris_cnt(new_frame)
        self.detect_iris(iris_cnt)


if __name__ == '__main__':
    frame = cv2.imread("eyes/eye5.jpg")

    gaze = GazeTracking(frame)
    gaze.analyze()
    print(gaze.x, gaze.y)

    cv2.waitKey(0)
    cv2.destroyAllWindows()