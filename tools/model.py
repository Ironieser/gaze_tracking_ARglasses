import os
import sys
import glob
import dlib

options = dlib.simple_object_detector_training_options()
# 单个眼睛不是1q2w3e4r
# 左右对称的
# options.add_left_right_image_flips = True
# 支持向量机的C参数，通常默认取为5.自己适当更改参数以达到最好的效果
options.C = 5
# 线程数，你电脑有4核的话就填4
options.num_threads = 4
options.be_verbose = True


# training_xml_path = "sz.xml"
# dlib.train_simple_object_detector(training_xml_path, "sz.svm", options)
# print("")
# print("Training accuracy: {}".format(
#     dlib.test_simple_object_detector(training_xml_path, "sz.svm")))

# training_xml_path = "cz.xml"
# dlib.train_simple_object_detector(training_xml_path, "cz.svm", options)
# print("")
# print("Training accuracy: {}".format(
#     dlib.test_simple_object_detector(training_xml_path, "cz.svm")))
#
# training_xml_path = "dp.xml"
# dlib.train_simple_object_detector(training_xml_path, "dp.svm", options)
# print("")
# print("Training accuracy: {}".format(
#     dlib.test_simple_object_detector(training_xml_path, "dp.svm")))
#
# training_xml_path = "pb.xml"
# dlib.train_simple_object_detector(training_xml_path, "pb.svm", options)
# print("")
# print("Training accuracy: {}".format(
#     dlib.test_simple_object_detector(training_xml_path, "pb.svm")))

# training_xml_path = "zb.xml"
# dlib.train_simple_object_detector(training_xml_path, "zb.svm", options)
# print("")
# print("Training accuracy: {}".format(
#     dlib.test_simple_object_detector(training_xml_path, "zb.svm")))

training_xml_path = "mf.xml"
dlib.train_simple_object_detector(training_xml_path, "mf.svm", options)
print("")
print("Training accuracy: {}".format(
    dlib.test_simple_object_detector(training_xml_path, "mf.svm")))









