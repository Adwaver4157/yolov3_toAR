# coding:utf-8


class RecognizeGesture:
    def __init__(self, path):
        self.path = path
        self.dict = {}  # name of gesture and rule
        self.arr = []  # FIFOqueue of signs
        self.step = 0
        self.criteria = [None, self.step, 0]
        txt = open(self.path)
        while True:
            gesture = txt.readline()
            if not gesture:
                break
            gesture = gesture.strip().split(' ')
            assert len(gesture) == 2, 'format of gesturess.txt is wrong'
            name, definition = gesture[0], gesture[1]
            definition = definition.split(',')
            self.dict[name] = list(map(int, definition))

    def recognizeGesture(self, image, box, mClass, score):
        self.step += 1
        h, w = image.shape[0], image.shape[1]
        # ↓試験導入
        """
        print(box)
        # 大きさチェック
        x, y = box[2]-box[0], box[3]-box[1]
        if max(x, y)/min(x, y) > 3 or max(x, y) > max(h//2, w//2):
            mClass = None
        # 可能性チェック
        if self.step-self.criteria[2] > 10:
            self.criteria = [None, self.step]
        mClass = self.checkClass(box, mClass, score)
        """
        if mClass is None:
            return None

        # サインの追加
        cx = (box[0] + box[2]) // 2
        cy = (box[1] + box[3]) // 2
        quadrant = 0
        if cx <= h // 2:
            if cy <= w // 2:
                quadrant = 1
            else:
                quadrant = 2
        else:
            if cy <= w // 2:
                quadrant = 4
            else:
                quadrant = 3
        if (len(self.arr) == 0) or (self.arr[-1] != [quadrant, mClass]):
            self.arr.append([quadrant, mClass])

        return self.patternMatch()

    def patternMatch(self):
        if len(self.arr) < 4:
            return None
        for ges in self.dict:
            flag = True
            length = len(self.dict[ges]) // 2
            for i in range(length):
                flag &= (self.dict[ges][2*i:2*(i+1)] == self.arr[-length+i])
            if flag:
                return ges
        return None

    def checkClass(self, box, mClass, score):

        if score > 0.3:
            self.criteria = [box, self.step, 3]
            return mClass

        if self.criteria[0] is None:
            return None
        else:
            dice = self.calcDice(box, self.criteria[0])
            if dice < 0.5:  # 要調整
                return None
            else:
                if score > 0.1:
                    self.criteria = [box, self.step, self.criteria[2]]
                else:
                    if self.criteria[2] != 1:
                        self.criteria = [box, self.step, self.criteria[2]-1]
                return mClass

    def calcDice(box, box2):
        h = max(min(box[2], box2[2])-max(box[0], box2[0]), 0)
        w = max(min(box[3], box2[3])-max(box[1], box2[1]), 0)
        s1 = (box[2]-box[0])*(box[3]-box[1])
        s2 = (box2[2]-box2[0])*(box2[3]-box2[1])
        return 2*h*w/(s1+s2)

    def showGesture(self):
        for ges in self.dict:
            print("ジェスチャー[" + ges + "] : ", end='')
            for j in range(len(self.dict[ges]) // 2):
                print(str(self.dict[ges][j * 2]) + "象限, サイン" +
                      str(self.dict[ges][j * 2 + 1]), end='')
                if((j + 1) * 2 == len(self.dict[ges])):
                    print()
                else:
                    print(" -> ", end='')
