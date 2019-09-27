import cv2
import time
from eye_detect import EyeDetect


webcam = cv2.VideoCapture(1)


def draw_circle(eye,detect_eye):
    """[summary]

    Arguments:
        world {[type]} -- [description]q
        eye {[type]} -- [description]
        detect_world {[type]} -- [description]
        detect_eye {[type]} -- [description]
        recognize_area {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    cv2.rectangle(
        eye,
        (detect_eye.pupil_x, detect_eye.pupil_y),
        (
            detect_eye.pupil_x + detect_eye.pupil_w,
            detect_eye.pupil_y + detect_eye.pupil_h,
        ),
        (150, 255, 0),
        3,
    )
    cv2.rectangle(
        eye,
        (detect_eye.eye_x, detect_eye.eye_y),
        (detect_eye.eye_x + detect_eye.eye_w, detect_eye.eye_y + detect_eye.eye_h),
        (0, 255, 0),
        3,
    )
    # 画十字标
    cv2.line(
        eye,
        (detect_eye.pupil_c_x - 30, detect_eye.pupil_c_y),
        (detect_eye.pupil_c_x + 30, detect_eye.pupil_c_y),
        (255, 255, 0),
        thickness=2,
    )
    cv2.line(
        eye,
        (detect_eye.pupil_c_x, detect_eye.pupil_c_y - 30),
        (detect_eye.pupil_c_x, detect_eye.pupil_c_y + 30),
        (255, 255, 0),
        thickness=2,
    )

    return eye

# 定义编解码器并创建 VideoWriter 对象
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('data/example.avi',fourcc, 20.0, (640,480))

detect_eye = EyeDetect()
while True:
    # 我们从网络摄像头中得到一个新的画面
    _, frame = webcam.read()

    # eye = frame
    # detect_eye.detect(eye)
    # frame = draw_circle(eye,detect_eye)

    if cv2.waitKey(10) == ord('s'):
        name = "eyes/" + str(time.time())+ ".jpg"
        cv2.imwrite(name, frame)

    # 保存当前帧
    # out.write(frame)
    cv2.imshow("Demo", frame)

    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
