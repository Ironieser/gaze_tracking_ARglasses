# coding:utf-8
#  imageai下载地址：https://github.com/OlafenwaMoses/ImageAI
#  resnet50_coco_best_v2.1.0.h5 模型下载地址：https://github.com/fizyr/keras-retinanet/releases/
from imageai.Detection import ObjectDetection  # 导入了 ImageAI 目标检测类
import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import matplotlib.pyplot as plt

def targetDetection(imgArray,model_path):
    """
    :param imgArray: 图片数据，类型为ndarray
    :param model_path: retinanet模型路径
    :return:
    """
    path = os.path.abspath(model_path)
    detector = ObjectDetection()  # 定义了目标检测类
    detector.setModelTypeAsRetinaNet()  # 模型的类型设置为 RetinaNet
    detector.setModelPath(path)  # 将模型路径设置为 RetinaNet 模型的路径
    detector.loadModel()  # 模型加载到的目标检测类
    # 调用目标检测函数，解析输入的和输出的图像路径。
    detections = detector.detectObjectsFromImage(input_image=imgArray,
                                                 input_type='array',output_type='array')
    return detections

# data = plt.imread('./imgData/avenue.jpg')
# model_path = ('./imgData/resnet50_coco_best_v2.0.1.h5')
# imgInfo = targetDetection(data,model_path)
# plt.imshow(imgInfo[0])
# plt.show()


if __name__=='__main__':
    # 获取摄像头0表示第一个摄像头
    model_path = ('../model/resnet50_coco_best_v2.0.1.h5')
    cap = cv2.VideoCapture(0)
    while (True):  # 逐帧显示
        ret, img = cap.read() # 强调img是ndarray类型的。
        imgData=targetDetection(img,model_path)
        cv2.imshow('image',imgData[0])
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 释放窗口资源

打开本地摄像头进行实时检测