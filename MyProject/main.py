import pickle

LAMBDA1 = 0.001
LAMBDA2 = 0.001
LAMBDA3 = 0.001

print('loading')

with open('pinyin_list.pkl', 'rb') as f:
    pinyin_list = pickle.load(f)

with open('CharFreq.pkl', 'rb') as f:
    CharFreq = pickle.load(f)

with open('WordFreq.pkl', 'rb') as f:
    WordFreq = pickle.load(f)

with open('TriWordFreq.pkl', 'rb') as f:
    TriWordFreq = pickle.load(f)
print('ready')


def GetCharFreq(pinyin, char):
    if char in CharFreq[pinyin]:
        return CharFreq[pinyin][char]
    else:
        return 0


def GetWordFreq(last_char, pinyin, char):
    if last_char in WordFreq and char in WordFreq[last_char]:
        return WordFreq[last_char][char]
    else:
        return LAMBDA1 * GetCharFreq(pinyin, char)


def GetTriWordFreq(last2_chars, pinyin, char):
    if last2_chars in TriWordFreq and char in TriWordFreq[last2_chars]:
        return TriWordFreq[last2_chars][char]
    p = 0
    q = 0
    if last2_chars[1] in WordFreq and char in WordFreq[last2_chars[1]]:
        p = WordFreq[last2_chars[1]][char]
    if char in CharFreq[pinyin]:
        q = CharFreq[pinyin][char]
    return LAMBDA2 * p + LAMBDA3 * q


class Node:
    def __init__(self):
        self.char = ''
        self.max = 0
        self.last = -1
        self.llast = -1

    def set_max(self, _max):
        self.max = _max

    def set_last(self, _last):
        self.last = _last

    def set_llast(self, _llast):
        self.llast = _llast

    def set_char(self, _char):
        self.char = _char


def optimize(line, mode):
    pys = line.split(' ')
    output = ''
    layers = []
    if mode == 2 or len(pys) < 3:
        layer = []
        for char in pinyin_list[pys[0]]:
            temp = Node()
            temp.set_char(char)
            temp.set_max(GetCharFreq(pys[0], char))
            layer.append(temp)
        layers.append(layer)
        for i in range(1, len(pys)):
            layer = []
            for char in pinyin_list[pys[i]]:
                temp = Node()
                temp.set_char(char)
                for j, last_char in enumerate(pinyin_list[pys[i - 1]]):
                    if (layers[i - 1][j].max * GetWordFreq(last_char, pys[i], char)) > temp.max:
                        temp.set_max(layers[i - 1][j].max * GetWordFreq(last_char, pys[i], char))
                        temp.set_last(j)
                layer.append(temp)
            layers.append(layer)
        temp = layers[-1][0]
        for node in layers[-1][1:]:
            if node.max > temp.max:
                temp = node
        output = temp.char
        for i in range(len(pys) - 1):
            temp = layers[len(pys) - 2 - i][temp.last]
            output += temp.char
    elif mode == 3:
        layer = []
        for char in pinyin_list[pys[0]]:
            temp = Node()
            temp.set_char(char)
            temp.set_max(GetCharFreq(pys[0], char))
            layer.append(temp)
        layers.append(layer)
        layer = []
        for char in pinyin_list[pys[1]]:
            temp = Node()
            temp.set_char(char)
            for j, last_char in enumerate(pinyin_list[pys[0]]):
                if (layers[0][j].max * GetWordFreq(last_char, pys[1], char)) > temp.max:
                    temp.set_max(layers[0][j].max * GetWordFreq(last_char, pys[1], char))
                    temp.set_last(j)
            layer.append(temp)
        layers.append(layer)
        for i in range(2, len(pys)):
            layer = []
            for char in pinyin_list[pys[i]]:
                temp = Node()
                temp.set_char(char)
                for k, llast_char in enumerate(pinyin_list[pys[i - 2]]):
                    for j, last_char in enumerate(pinyin_list[pys[i - 1]]):
                        if GetTriWordFreq(llast_char + last_char, pys[i], char) * GetTriWordFreq(layers[i - 3][layers[i - 2][k].last].char + llast_char, pys[i - 1],last_char) * layers[i - 2][k].max > temp.max:
                            temp.set_max(GetTriWordFreq(llast_char + last_char, pys[i], char) * GetTriWordFreq(layers[i - 3][layers[i - 2][k].last].char + llast_char, pys[i - 1],last_char) * layers[i - 2][k].max)
                            temp.set_llast(k)
                            temp.set_last(j)
                layer.append(temp)
            layers.append(layer)
        temp = layers[-1][0]
        for node in layers[-1][1:]:
            if node.max > temp.max:
                temp = node
        output = temp.char + layers[-2][temp.last].char + layers[-3][temp.llast].char
        for i in range(len(pys) - 1):
            if temp.llast != -1:
                temp = layers[len(pys) - 3 - 2 * i][temp.llast]
            else:
                break
            if temp.last != -1:
                output += layers[len(pys) - 4 - 2 * i][temp.last].char
            if temp.llast != -1:
                output += layers[len(pys) - 5 - 2 * i][temp.llast].char
    return output[::-1]


def Realtime_test():
    while True:
        str = input()
        print('2', optimize(str, mode=2))
        print('3', optimize(str, mode=3))


def output_as_text(src, mode):
    with open(src, 'r') as f:
        lines = f.readlines()
    with open('outputs/output' + src[12:], 'w') as f:
        output = ''
        for line in lines:
            output += optimize(line[:-1], mode=mode) + '\n'
        f.write(output)



#Realtime_test()
output_as_text('out.txt', mode=3)
