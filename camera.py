import cv2
import time


webcam = cv2.VideoCapture(0)

# 定义编解码器并创建 VideoWriter 对象
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('data/example.avi',fourcc, 20.0, (640,480))

while True:
    # 我们从网络摄像头中得到一个新的画面
    _, frame = webcam.read()

    if cv2.waitKey(1) == ord('s'):
        name = "eyes/" + str(time.time())+ ".jpg"
        cv2.imwrite(name, frame)

    # 保存当前帧
    # out.write(frame)
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()