import wave
import struct
from matplotlib import pyplot as plt

#Составление словаря декода
codmorze = {'a': '•—', 'b': '—•••', 'c': '—•—•', 'd': '—••',
         'e': '•', 'f': '••—•', 'g': '——•', 'h': '••••',
         'i': '••', 'j': '•———', 'k': '—•—', 'l': '•—••',
         'm': '——', 'n': '—•', 'o': '———', 'p': '•——•',
         'q': '——•—', 'r': '•—•', 's': '•••', 't': '—',
         'u': '••—', 'v': '•••—', 'w': '•——', 'x': '—••—',
         'y': '—•——', 'z': '——••', ' ': '_'}

#Странный алгоритм по отчистке ненужных прорех тишины в массиве, который надо разбирать отдельно (0-тишина или отсутствие сигнала)
# def foo(ls, d, m):
#     x, y = ls
#     if y - x < 10:
#         del d[x - m:y - m]
#         return (y - x)+m
#     else:
#         return m

#Открываем файл, который нужно декодировать
source=wave.open("morze.wav", "rb")

#Создаем файл-дурак, для проверки правильности отчистки ненужного шума и устанавливаем параметры от родительского
dest=wave.open("morze_update.wav", "wb")
dest.setparams(source.getparams())
print(source.getparams())
frames=source.getnframes()
data=source.readframes(frames)

#Декод данных bin --> dec
data=struct.unpack("<" + str(frames*source.getnchannels()) + "h", data)
data_updated=list(data)

#Процесс зануления шума
for i in range(len(data_updated)):
    if 0<data_updated[i]<5000 or 0>data_updated[i]>(-5000):
        data_updated[i]=0
# print(data_updated) проверочный принт

#кодируем массив обратно dec --> bin и записываем в файл
updated_frames=struct.pack("<" + str(len(data_updated)) + "h", *data_updated)
dest.writeframes(updated_frames)

source.close()
dest.close()

# открываем отчищенный от шума файл (отчищали для того, чтобы не путаться между сигналом . или - и шумом)
dest = wave.open("morze_update.wav", "rb")
print(dest.getparams())
frames = dest.getnframes()
frame_rate=dest.getframerate()
data = dest.readframes(frames)

#Декод данных bin --> dec
data = struct.unpack("<" + str(frames*dest.getnchannels()) + "h", data)

#ебнутая фишка для ускорения работы(могу объянить отдельно)
end=int((frames/frame_rate))
data2 = list(data[::end])

#Алгоритм по удалению прорех в сигналах
check_list = []
cheker = []
for x in range(len(data2)):

    if data2[x] == 0 and len(cheker) == 0:
        cheker.append(x)

    if data2[x] != 0 and len(cheker) != 0:
        cheker.append(x)
        check_list.append(cheker)
        cheker = []

cheker.append(len(data2))
check_list.append(cheker)
c = 0


#алгоритм по разделению сигналов в последовательность буквы и их разделению(чтобы ...(s) и ---(o) не декодилось как ...- и т.п.)
# ls_of_words=[]
ls_of_spaces=[]
counter=0
for x in data2:
    if x!=0:
        if counter<0:
            ls_of_spaces.append(abs(counter))
            counter=0
        counter+=1

    if x==0:
        if counter>0:
            # ls_of_words.append(counter)
            counter=0
        counter-=1
ls_of_spaces.append(abs(counter))

# авг для понимания разности длинны короткого и длинного сигнала, короткого и длинного участка тишины
# avg_of_words=sum(ls_of_words)/len(ls_of_words)
avg_of_spaces=sum(ls_of_spaces)/len(ls_of_spaces)

def avger(n):
    mi = axyet(ls_of_spaces)
    if n>mi+10:
        return "•"
    else:
        return '—'
    
def axyet(ls):
    counter=0
    l=[]
    for i in ls:
        if i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            counter+=1
        else:
            l.append(counter)
            counter=0
    l.remove(0)
    return min(l)

    
# print(len(ls_of_words), ls_of_words, avg_of_words)
# print(len(ls_of_spaces), ls_of_spaces, avg_of_spaces)
counter=0
symbols=''
ans=''
for i in range(1, len(ls_of_spaces)):
    if 10<ls_of_spaces[i]<400:        
        symbols+=avger(counter)
        counter=0
    elif ls_of_spaces[-1]<=ls_of_spaces[i]:
        symbols+=avger(counter)
        ans+=symbols+" "
        counter=0
        symbols=''
        ans+=" _ "
    elif 400<=ls_of_spaces[i]<ls_of_spaces[-1]:
        symbols+=avger(counter)
        ans+=symbols+" "
        counter=0
        symbols=''
    else:
        counter+=1
print(ans)
#кодировка в код морзе
# ans=''
# for symbol in range(len(ls_of_words)):
#     if ls_of_spaces[symbol] > avg_of_spaces:
#         ans += ' '

#     if ls_of_words[symbol]>avg_of_words:
#         ans+='•'
#     else:
#         ans+='—'

# декод из кода морзе
decod=ans.split()
decoded_string=''
for word in decod[:-1]:
    for key, value in codmorze.items():
        if word==value:
            decoded_string+=key

#не помню зачем это делал
#decoded_string=decoded_string[:-2:]

print(decod)
print(decoded_string)

plt.plot(data2)
plt.show()

