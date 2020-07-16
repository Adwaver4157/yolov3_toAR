# coding:utf-8
"""
学習済yoloを用いてlocalでwebカメラのリアルタイム推論を行う

Args:
    --model   : 学習済モデルの相対パス       (default : modeldata/yolov3_final.h5)
    --anchors : yolo_anchors.txtの相対パス (default : model_data/yolo_anchors.txt)
    --classes : class_name.txtの相対パス   (default : model_data/class_name.txt)
    ex) Main.py --model_path kerasyolo3/model_data/tiny_yolov3_prog.h5
                --anchors_path kerasyolo3/model_data/tiny_yolo_anchors.txt
                --classes_path kerasyolo3/model_data/class_name.txt
                --gestures_path kerasyolo3/model_data/gestures.txt
"""

import cv2
import os
from kerasyolo3.yolo import YOLO
from RecognizeGesture import RecognizeGesture
import argparse


def main():
    cap = cv2.VideoCapture(1)
    if cap.isOpened():
        while True:
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)

            # # # # # # # your process # # # # # # #

            result, mClass, mBox = yolo.detect_image(frame)

            if mClass is not None:
                cv2.rectangle(result, (mBox[1], mBox[0]),
                              (mBox[3], mBox[2]), (0, 0, 255))

            gesture = rg.recogniseGesture(result)

            if gesture != -1:
                pass

            # # # # # # # your process # # # # # # #

            cv2.imshow("window", result)

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
    current_path = os.getcwd()
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' +
        YOLO.get_defaults("model_path")
    )
    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' +
        YOLO.get_defaults("anchors_path")
    )
    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' +
        YOLO.get_defaults("classes_path")
    )
    parser.add_argument(
        '--gestures_path', type=str,
        help='path to gesture definition, default ' +
        'kerasyolo3/model_data/gestures.txt'
    )
    FLAGS = vars(parser.parse_args())
    for arg in FLAGS:
        FLAGS[arg] = os.path.join(current_path, FLAGS[arg])
    print(FLAGS)

    gestures_path = FLAGS.pop("gestures_path")

    # YOLO(画像認識クラス)生成
    yolo = YOLO(**FLAGS)

    # RecognizeGesture(ジェスチャー認識クラス)生成
    rg = RecognizeGesture(gestures_path)
    rg.showGesture()

    main()