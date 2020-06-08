# kerasyolo3 のチュートリアル

以下の colab をコピーして学習、テストすることができます
https://colab.research.google.com/drive/1pi7Iskwi2G_nYMithtQFPoyqWzQ6BFmp?usp=sharing


## ディレクトリ構成
```
yolov3_toAR/
  |
  ┝ README.md
  ┝ kears-yolov3
  |     |
  |     ┝ model_data
  |          ┝ yolo_anchor.txt
  |          ┝ ~~~~.h5 <- 学習済モデル
  ┝ resize.py
  ┝ manage_data.py <- ImagesとAnnotationを作成してくれる
  |
  sample
  | |
  | ┝ datasets         ┐
  | ┝ class_name.txt   | resize.pyで自動的に作られる
  | ┝ train.txt        ┘
  | |
  | |
  | ┝ Images
  | |   ┝ class01 <-クラス名はなんでもいい
  | |   |   ┝ img1.jpg
  | |   |   ...
  | |   |   └ img1000.jpg
  | |   ┝ class02
  | |   |   ┝ img1.jpg
  | |   |   ...
  | |   |   └ img1000.jpg
  | |   ...
  | |
  | └ Annotation
  |     ┝ class01 <-Images内のディレクトリに対応する名前
  |     |   ┝ class01.txt <- クラス内の画像の総数や、更新情報
  |     |   ┝ img1.txt <- Images内の同名画像のannotation(書式は下)
  |     |   ...
  |     |   └ img1000.txt
  |     ┝ class02
  |     |   ┝ class02.txt
  |     |   ┝ img1.txt
  |     |   ...
  |     |   └ img1000.txt
  |     ...
  |
  Hand <-その他、自分で作ったプロジェクト(sampleと同様の構成)
  | |
  |  ...
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
1. make or delete     => データを作成するか削除するかを選ぶ(現状makeのみ)
2. enter project name => プロジェクト名を入力(kerasyolo3およびsample以外)
3. enter class name   =>　作りたいクラス名を入力(新規でも既存でも大丈夫)
4. successfully opend => カメラが開けた 
   failed to open => カメラが開けない、11行目の数字をいじる

### window上
* 緑色の枠に目標物を入れる
* 枠の移動は
```
a:左、s:下、d:右、w:上、n:縮小、m:拡大 
```
* xを押すと枠が赤くなる -> 赤い間は画像が保存される
* もう一度xを押すと緑に戻る
* 止める時はqを押す

### ターミナル上
1. continue to make images?　=> 他のクラスを作りたいならy、そうでないならn
2. yなら上記の操作を繰り返す

## resize.pyの使い方

### 引数
```
-p,--project_name       : リサイズしたい画像のプロジェクト名
-W,--width              : リサイズ後の横の長さ(32の倍数)
-H,--height             : リサイズ後の縦の長さ(32の倍数、Widthと同じ時省略できる)
-n,--number_of_classess : 使用したいクラス数(0の時、全てのクラスを使う)
```
### !!注意!!
* datasetsディレクトリが存在するとerrorになる => 事前にdatasetsがない状態にする(コンフリクトを避けるため)
