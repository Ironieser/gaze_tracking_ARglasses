# # import numpy as np

# # a = np.array([1, 2, 3, 4, 5, 6]).reshape([2, 3])
# # print(a)

# import cv2

# user, pwd, ip, channel = "admin", "admin", "192.168.0.102", 81

# # video_stream_path = 0  # local camera (e.g. the front camera of laptop)
# # video_stream_path = 'video.avi'  # the path of video file
# # video_stream_path = "rtsp://%s:%s@%s/h265/ch%s/main/av_stream" % (user, pwd, ip, channel)  # HIKIVISION old version 2015
# # video_stream_path = "rtsp://%s:%s@%s//Streaming/Channels/%d" % (user, pwd, ip, channel)  # HIKIVISION new version 2017
# # video_stream_path = "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" % (user, pwd, ip, channel)  # dahua
# video_stream_path = 'http://admin:admin@192.168.0.103'  
# # video_stream_path = '192.168.0.103:81/stream/'  

# def run_opencv_camera():
#     # video_stream_path = 0  # local camera (e.g. the front camera of laptop)
#     cap = cv2.VideoCapture(video_stream_path)
#     # 设置缓存区的大小
#     cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

#     while cap.isOpened():
#         is_opened, frame = cap.read()
#         cv2.imshow('frame', frame)
        
#         k = cv2.waitKey(1)
#         if k == ord('q'):
#             break

#     cap.release()



# run_opencv_camera()



import cv2
import urllib.request
import numpy as np

host = "192.168.0.100:81" # 在这里记得修改ip，否则是无法调用的，刚刚浏览器输入的地址
hoststr = 'http://' + host + '/stream'
print('Streaming ' + hoststr)

print('Print Esc to quit')
stream=urllib.request.urlopen(hoststr)
bytes=bytes()
while True:
    bytes+=stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    i = 0
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        #flags = 1 for color image
        try:
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
            # print i.shape
            cv2.imshow("wjw",i)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit(0)
        except Exception as e:
            print('保存失败', e)
