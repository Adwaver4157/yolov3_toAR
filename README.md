# keras-yolo3 のチュートリアル

以下の colab をコピーして学習、テストすることができます
https://colab.research.google.com/drive/1pi7Iskwi2G_nYMithtQFPoyqWzQ6BFmp?usp=sharing


# ディレクトリ構成
```
yolov3_toAR/
  ┝ README.md
  ┝ kears-yolov3
  |
  ┝ resize.py
  ┝ datasets      　  ┐
  ┝ class_name.txt 　 ├  この三つはresize.pyで作られる
  ┝ train.txt       　┘
  |
  ┝ manage_data.py <- ImagesとAnnotationを作成する
  |
  ┝ Images
  |   ┝ class01 <-クラス名はなんでもいい
  |   |   ┝ class01.txt <- クラス内の画像の総数や、更新情報
  |   |   ┝ img1.jpg
  |   |   ...
  |   |   └ img1000.jpg
  |   ┝ class02
  |   |   ┝ class02.txt
  |   |   ┝ img1.jpg
  |   |   ...
  |   |   └ img1000.jpg
  |   ...
  |
  └ Annotation
      ┝ class01 <-Images内のディレクトリに対応する名前
      |   ┝ img1.txt <- Images内の同名画像のannotation(書式は下)
      |   ...
      |   └ img1000.txt
      ┝ class02
      |   ┝ img1.txt
      |   ...
      |   └ img1000.txt
      ...
```
