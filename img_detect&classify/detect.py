# coding:utf-8
#  imageai下载地址：https://github.com/OlafenwaMoses/ImageAI
#  resnet50_coco_best_v2.1.0.h5 模型下载地址：https://github.com/fizyr/keras-retinanet/releases/
from imageai.Detection import ObjectDetection  # 导入了 ImageAI 目标检测类
import cv2
import os
import time
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

data = plt.imread('../img_classify/05-30.jpg')
model_path = ('../model/resnet50_coco_best_v2.1.0.h5')
t1 = time.time()
imgInfo = targetDetection(data,model_path)
t2 = time.time()
print(t2-t1)
plt.imshow(imgInfo[0])
plt.show()