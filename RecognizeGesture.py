# coding:utf-8


class RecognizeGesture:
    def __init__(self, path):
        self.path = path
        self.dict = {}  # name of gesture and rule
        self.arr = []  # FIFOqueue of signs
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

    def recognizeGesture(self, image, box, mClass):
        if mClass is None:
            return None
        img = image.copy()
        h, w = img.shape[0], img.shape[1]
        x = (box[0] + box[2]) // 2
        y = (box[1] + box[3]) // 2
        quadrant = 0
        if x <= h // 2:
            if y <= w // 2:
                quadrant = 1
            else:
                quadrant = 2
        else:
            if y <= w // 2:
                quadrant = 4
            else:
                quadrant = 3
        if (len(self.arr) == 0) or (self.arr[-1] != [quadrant, mClass]):
            self.arr.append([quadrant, mClass])
        return self.patternMatch()

    def patternMatch(self):
        for ges in self.dict:
            flag = True
            length = len(self.dict[ges]) // 2
            for i in range(length):
                flag &= (self.dict[ges][2 * i:2 * (i + 1)] == self.arr[-length + i])
            if flag:
                return ges
        return None

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
