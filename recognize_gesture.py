import sys
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from kerasyolo3.yolo import YOLO

cap = cv2.VideoCapture(1)
if cap.isOpened():
    yolo = YOLO()
    while True:
        _, frame = cap.read()
        #result, label, box = yolo.detect_image(frame)
        #cv2.imshow("result", result)
        cv2.imshow("result", frame)
        """
        label, boxを処理してジェスチャーを認識する
        """

        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            cap.release()
            break
