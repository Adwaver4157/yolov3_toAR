"""
学習済yoloを用いてlocalでwebカメラのリアルタイム推論を行う

Args:
        --model     : 学習済モデルのパス      (defaultは /content/yolov3_toAR/kerasyolo3/logs/000/trained_weights_stage_1.h5 であるがローカル利用なら必ず適切なパスを指定)
        --anchors   : anchorsのパス         (defaultは model_data/yolo_anchors.txt であるがWDが違うのでこれも指定必須)
        --classes   : class_name.txtのパス  (defaultは /content/yolov3_toAR/class_name.txt これも指定必須)
        ex) recognoze_gesture_local.py --model aaa --anchors bbb --classes ccc

"""
import cv2
import numpy as np
from PIL import Image
from kerasyolo3.yolo import YOLO
import argparse

def main():
    cap = cv2.VideoCapture(1)  # カメラ番号は多分0か1
    if cap.isOpened():
        while True:
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow("window", frame)

            #############your process###############




            #############your process###############

            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
        cap.release()
    else:
        print("failed to open camera")
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )
    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )
    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )
    FLAGS = parser.parse_args()
    yolo = YOLO(**vars(FLAGS))

    main()
