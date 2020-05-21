# keras-yolo3 のチュートリアル

以下の colab をコピーして学習、テストすることができます
https://colab.research.google.com/drive/1pi7Iskwi2G_nYMithtQFPoyqWzQ6BFmp?usp=sharing


## ディレクトリ構成
```
yolov3_toAR/
  |
  ┝ README.md
  ┝ kears-yolov3
  |
  ┝ resize.py
  ┝ datasets      　  ┐
  ┝ class_name.txt 　 ├  この三つはresize.pyで作られる
  ┝ train.txt       　┘
  |
  ┝ manage_data.py <- ImagesとAnnotationを作成してくれる
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
### annotationの書式
```
x_min,y_min,x_max,y_max
```
対象を囲う最小のboxについてのxの最小、yの最小、、、をカンマ区切りで書く  
（犬のを持ってくるときはそのままで大丈夫、ただしresize.pyの内容の「普段」というところをコメントアウトして、「犬」のところを有効にする）

## manage_data.pyの使い方

### ターミナル上
1. make or delete => データを作成するか削除するかを選ぶ(現状makeのみ)
2. enter the class you want to make =>　作りたいクラス名を入力(新規でも既存でも大丈夫)
3. successfully opend => カメラが開けた failed to open => カメラが開けない、11行目の数字をいじる

### window上
* 緑色の枠に目標物を入れる
* 枠の移動は
```
a:左、s:下、d:右、w:上、n:縮小、m:拡大 
```
* kを押すと枠が赤くなる -> 赤い間は画像が保存される
* もう一度kを押すと緑に戻る
* 止める時はqを押す

### ターミナル上
1. continue to make images?　=> 他のクラスを作りたいならy、そうでないならn
2. yなら上記の操作を繰り返す

### !!注意!!
* datasetsディレクトリがないとeerro
