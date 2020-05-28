import numpy as np
import cv2
import os
import datetime
import random

def make_image():
    class_name = input("enter the class you want to make -> ")
    class_image_path = "Images/"+class_name
    class_annotation_path = "Annotation/"+class_name
    cap = cv2.VideoCapture(1)  # カメラ番号は多分0か1
    if cap.isOpened():
        print("successfully opened")
        print("make "+class_name)

        #ディレクトリの存在確認
        if not os.path.exists(class_image_path):
            os.makedirs(class_image_path)
            os.makedirs(class_annotation_path)
        class_text = open(class_annotation_path+"/"+class_name+".txt", 'a+')
        size = len(os.listdir(class_image_path))+10000  # 初期値をずらしてコンフリクトを避ける
        size2 = size

        _, frame = cap.read()
        h = frame.shape[0]
        w = frame.shape[1]
        xmin, ymin, xmax, ymax = w//2-200, h//2-200, w//2+200, h//2+200

        takeSS = 2  # 10*x[ms]に一回更新
        takeSS_flag = False
        count = 0

        while True:

            # 枠の操作
            r = random.randint(-2, 2)
            key = cv2.waitKey(10)
            if key == ord('a') and xmin >= 10:  # 左
                xmin -= 8+r
                xmax -= 8+r
            elif key == ord('s') and ymax < h-10:  # 下
                ymin += 8+r
                ymax += 8+r
            elif key == ord('d') and xmax < w-10:  # 右
                xmin += 8+r
                xmax += 8+r
            elif key == ord('w') and ymin >= 10:  # 上
                ymin -= 8+r
                ymax -= 8+r
            elif key == ord('n') and xmax-xmin > 10:  # 縮小
                xmin += 3+r
                ymin += 3+r
                xmax -= 3+r
                ymax -= 3+r
            elif key == ord('m') and ymin >= 5 and xmax < w-5 and ymax < h-5 and xmin >= 5:  # 拡大
                xmin -= 3+r
                ymin -= 3+r
                xmax += 3+r
                ymax += 3+r
            elif key == ord('x'):
                takeSS_flag = not takeSS_flag
            elif key == ord('q'):
                if size2 > size+1:
                    #更新内容を追加
                    class_text.write("更新時刻:")
                    class_text.write(str(datetime.datetime.now()))
                    class_text.write(" 更新内容:")
                    class_text.write(str(size+1))
                    class_text.write("から")
                    class_text.write(str(size2))
                    class_text.write("を追加\n")
                    class_text.close()
                cv2.destroyWindow("window")
                break

            #画面の更新
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame_copy = frame.copy()
            if takeSS_flag:
                cv2.rectangle(frame_copy, (xmin, ymin), (xmax, ymax), (0, 0, 255))
            else:
                cv2.rectangle(frame_copy, (xmin, ymin), (xmax, ymax), (0, 255, 0))

            cv2.putText(frame_copy, str(size2), (0, h//3), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), thickness=2)
            cv2.imshow("window", frame_copy)

            #画面を保存
            if count%takeSS == 0 and takeSS_flag:
                #書き出し
                size2 += 1
                cv2.imwrite(class_image_path+"/img"+str(size2)+".jpg", frame)
                with open(class_annotation_path+"/img"+str(size2)+".txt", "w") as f:
                    f.write(str(xmin))
                    f.write(",")
                    f.write(str(ymin))
                    f.write(",")
                    f.write(str(xmax))
                    f.write(",")
                    f.write(str(ymax))
                    f.write("\n")

            count += 1

        cap.release()
    else:
        print("failed to open camera")
        return

    a = input("continue to make images?(y/n) -> ")
    if a == "y":
        make_image()
    else:
        return

def delete_image():
    print("作り途中")

def save_image(c, img):
    pass

def main():
    s = input("make or delete? -> ")
    if s == "make":
        make_image()
    elif s == "delete":
        delete_image()
    else:
        print("invalid input")

if __name__ == '__main__':
    main()
