"""
Images, Annotation内にある画像をリサイズする

** datasetsディレクトリがないときerrorとなる **

Args:
    -p,--project_name       : リサイズしたい画像のプロジェクト名
    -W,--width              : リサイズ後の横の長さ(32の倍数)
    -H,--height             : リサイズ後の縦の長さ(32の倍数、Widthと同じ時省略できる)
    -n,--number_of_classes  : 使用したいクラス数(0の時、全てのクラスを使う)
    ex) Handプロジェクトの画像を2クラス分だけ640*320にリサイズしたい -> python resize.py -p Hand -w 640 -n 2

"""
import glob
import sys
import os
from PIL import Image
import argparse

def main(**kwargs):
    width = kwargs['width']
    height = kwargs['height']
    if width%32 != 0 or height%32 != 0:
        print('Width and Height must be multiple of 32')
    else:
        project_name = kwargs['project_name']
        class_num_limit = kwargs['number_of_classes']
        class_directories = glob.glob(os.path.join(project_name, "Images", "*"))
        class_name_txt = open(os.path.join(project_name, "class_name.txt"), "w")
        train_txt = open(os.path.join(project_name, "train.txt"), "w")

        img_num = 1
        class_num = 0
        try:
            os.mkdir(os.path.join(project_name, "datasets"))
        except Exception:
            print("'datasets' directory already exists. Make sure that the directory is empty and delete it.")
            return

        for class_path in class_directories:
            class_name = os.path.basename(class_path)

            #class_name.txtへの書き込み(クラス名)
            class_name_txt.write(class_name)
            class_name_txt.write("\n")

            img_files = glob.glob(os.path.join(class_path, "*"))

            for img_path in img_files:
                img_name = os.path.basename(img_path)

                #画像のリサイズ
                img = Image.open(img_path)
                w = width/img.width
                h = height/img.height
                img_resize = img.resize((width, height))
                try:
                    img_resize.save(os.path.join(project_name, "datasets", "image"+str(img_num)+".jpg"))
                except Exception as e:
                    print(e)
                    continue

                #犬↓
                """
                text = open(os.path.join(project_name, "Annotation", class_name, os.path.splitext(img_name)[0]))
                for i in range(18):
                    text.readline()
                line = [0]*4
                for i in range(4):
                    s = text.readline().strip()[6:-7]
                    line[i] = int(s)
                for i in range(3):
                    a = text.readline().strip()
                if "object" in a:  # 複数の犬がいるのは使わない
                    continue
                """
                #犬↑
                #普段使う方↓

                text = open(os.path.join(project_name, "Annotation", class_name, os.path.splitext(img_name)[0]+'.txt'))
                line = list(map(int, text.readline().split(",")))

                #普段使う方↑

                #train.txtへの書き込み(annotation)
                train_txt.write(os.path.join(project_name, "datasets", "image"+str(img_num)+".jpg"))
                train_txt.write(str(int(line[0]*w)))
                train_txt.write(",")
                train_txt.write(str(int(line[1]*h)))
                train_txt.write(",")
                train_txt.write(str(int(line[2]*w)))
                train_txt.write(",")
                train_txt.write(str(int(line[3]*h)))
                train_txt.write(",")
                train_txt.write(str(class_num))
                train_txt.write("\n")

                img_num += 1

            class_num += 1
            if class_num == class_num_limit:
                break

        train_txt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--project_name',
        type=str,
        default='sample',
        help='リサイズしたい画像のプロジェクト名 default:sample'
    )
    parser.add_argument(
        '-W', '--width',
        type=int,
        default=320,
        help='リサイズ後の横の長さ default:320'
    )
    parser.add_argument(
        '-H', '--height',
        type=int,
        default=320,
        help='リサイズ後の縦の長さ default:320'
    )
    parser.add_argument(
        '-n', '--number_of_classes',
        type=int,
        default=0,
        help='使うクラスの数(全て使うなら0) default:0'
    )
    FLAGS = vars(parser.parse_args())
    print(FLAGS)
    main(**FLAGS)
