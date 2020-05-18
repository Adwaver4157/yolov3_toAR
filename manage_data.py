import numpy as np
import cv2
import os
import datetime

def make_image():
    class_name = input("enter the class you want to make -> ")
    class_image_path = "Images/"+class_name
    class_annotation_path = "Annotation/"+class_name
    cap = cv2.VideoCapture(1)  # カメラ番号は多分0か1
    if cap.isOpened():
        print("your camera successfully opened")
        print("make "+class_name)

        #ディレクトリの存在確認
        if not os.path.exists(class_image_path):
            os.makedirs(class_image_path)
            os.makedirs(class_annotation_path)
        class_text = open(class_image_path+"/"+class_name+".txt", 'a+')
        size = len(os.listdir(class_image_path))-1
        size2 = size


        a, b = 25, 5 # aは描画するフレーム数、bは記録するフレーム数 (gcd(a,b)=b)
        c = 1
        while True:
            _, frame = cap.read()
            cv2.imshow("window", frame)

            if c%(a//b) == 0:

                #
                #未完成
                #

                #書き出し
                size2 += 1
                cv2.imwrite(class_image_path+"/img"+str(size2)+".jpg", frame)
                with open(class_annotation_path+"/img"+str(size2)+".txt", "w") as f:
                    f.write(str(0))
                    f.write(",")
                    f.write(str(0))
                    f.write(",")
                    f.write(str(0))
                    f.write(",")
                    f.write(str(0))
                    f.write("\n")
            c += 1

            key = cv2.waitKey(1000//a)
            if key == ord('q'):
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
