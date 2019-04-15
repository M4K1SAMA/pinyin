from pypinyin import lazy_pinyin
import sys

path = sys.argv[1]

def is_Chinese(word):
    if '\u4e00' <= word <= '\u9fa5':
        return True
    else:
        return False

str = ''
tmp = ''

with open(path, 'r') as f:
    str = f.read()
    for char in str:
        if not is_Chinese(char):
            if tmp[-1] != '\n':
                tmp += '\n'
        else:
            tmp += char

with open(path, 'w') as f:
   f.write(tmp)

lines = tmp.split('\n')
tmp = ''
for line in lines:
    tmp += ' '.join(lazy_pinyin(line)) + '\n'

with open('py' + path[3:], 'w') as f:
    f.write(tmp[:-1])
