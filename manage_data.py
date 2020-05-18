import numpy as np
import cv2
import os

def make_image():
    class_name = input("enter the class you want to make -> ")
    class_image_path = "Images/"+class_name
    class_annotation_path = "Annotation/"+class_name
    cap = cv2.VideoCapture(1)  # カメラ番号は多分0か1
    if cap.isOpened():
        print("your camera successfully opened")
        print("make "+class_name)

        if not os.path.exists(class_image_path):
            os.makedirs(class_image_path)
            os.makedirs(class_annotation_path)
            class_text = open(class_image_path+"/"+class_name+".txt", 'a+')
            class_text.write("0\n")
        else:
            class_text = open(class_image_path+"/"+class_name+".txt", 'a+')
        class_text.seek(0)
        class_text_array = class_text.readlines()
        size = int(class_text_array[0])

        while True:
            _, frame = cap.read()
            cv2.imshow("window", frame)
            




            key = cv2.waitKey(1)
            if key == ord('q'):
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
