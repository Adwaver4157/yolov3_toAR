import sys
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from kerasyolo3.yolo import YOLO

cap = cv2.VideoCapture(1)
if cap.isOpened():
    #yolo = YOLO()

    count = 0
    while True:
        cv2.waitKey(1)
        _, frame = cap.read()
        image = Image.fromarray(frame)
        #image, label, box = yolo.detect_image(image)
        result = np.asarray(image)
        cv2.imshow("result", result)

        """
        label, boxを処理してジェスチャーを認識する
        """

        count += 1        
        if count == 100:
            cv2.destroyAllWindows()
            cap.release()
            break
