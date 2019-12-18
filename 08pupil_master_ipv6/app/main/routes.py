#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import login_required

from flask import jsonify

from importlib import import_module
import os
from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap


# from app.main.camera import Camera
from app.main.pedestrian_detection import PedestrianDetection, BacksubTractor

# 使用摄像头
# from app.main.main_cam_d import PupilTrack
# 使用本地视频
from app.main.main_video_d import PupilTrack

import cv2 as cv2

pupil = PupilTrack()

main = Blueprint('main', __name__)
x = 0
    
@main.route('/')
@main.route('/index')
@login_required
def index():
    title = "Pupil Smart"

    """ home page."""
    return render_template('main/index.html', object=pupil, title=title)


def gen():
    """Video streaming generator function."""
    # detector = BacksubTractor()
    while True:
        # frame = camera.get_frame()
        # cv2.imshow("", img)
        # cv2.waitKey(10)
        
        # 图像处理
        # ret, img = detector.detect(frame, is_save=True)
        # frame = self.detector_pedestrian.detect(image)            
        ret, img = pupil.track()

        # # 编码jpg图像并返回
        img = cv2.imencode('.jpg', img)[1].tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


@main.route('/index/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # cap = Camera()
    # cap.set_video_source(0)
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    
@main.route('/index/a')  
def a():
    global x
    # return Response(x)   
    return jsonify({'x':x})