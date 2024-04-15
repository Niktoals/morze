import wave
import struct
from matplotlib import pyplot as plt

#Поиск и вычленение нужных звуков сигналов с полледующей декодировкой (bin --> dec)и записью в файлы dot, dash, space
#ЭТА ХУЙНЯ НАСТРАИВАЕТСЯ ВРУЧНУЮ, НЕ ТРОГАЙ ЕЕ, ОНО ТЕБЯ СОЖРЕТ
# source=wave.open("sos.wav", "rb")
# frames=source.getnframes()
# data=source.readframes(frames)
# framerate=source.getframerate()
#
# data=struct.unpack("<" + str(frames*source.getnchannels()) + "h", data)
# data_updated=list(data[int(framerate*1.85):framerate*2:])
#
# for i in range(len(data_updated)):
#     if 0<data_updated[i]<5000 or 0>data_updated[i]>(-5000):
#         data_updated[i]=0
# # print(data_updated)
#
# dash=open("dash.txt", "w")
# dash.write(str(data_updated))
# dash.close()
#
# source.close()
# plt.plot(data_updated)
# plt.show()

codmorze = {'a': '•—', 'b': '—•••', 'c': '—•—•', 'd': '—••',
         'e': '•', 'f': '••—•', 'g': '——•', 'h': '••••',
         'i': '••', 'j': '•———', 'k': '—•—', 'l': '•—••',
         'm': '——', 'n': '—•', 'o': '———', 'p': '•——•',
         'q': '——•—', 'r': '•—•', 's': '•••', 't': '—',
         'u': '••—', 'v': '•••—', 'w': '•——', 'x': '—••—',
         'y': '—•——', 'z': '——••'}


#Создание звукового файла, в который потом запишем произвольную звуковую последовательность
dest=wave.open("morze.wav", "wb")

# Считывание масивов значений фреймов сигналов
dot=open("dot.txt", "r").read()
space=open("space.txt", "r").read()
dash=open("dash.txt", "r").read()

# counter=0
# for i in dot:
#     if i != '0':
#         counter+=1
# print(counter)
# counter=0    Проверка разности сигналов . и _ (надо, чтобы удостовериться в точности различий короткого и длинного сигнала)
# for i in dash:
#     if i != '0':
#         counter+=1
# print(counter)
input_data=input()
decoded_string=''
for word in input_data:
    if word==" ":
        decoded_string+=" "
        continue
    decoded_string+=codmorze[word]
    decoded_string+=" "


#Считывание произвольной последовательности из инпута
sound=space
input_data=decoded_string
for sigh in input_data:
    if sigh=='•':
        sound+=dot
    if sigh=='—':
        sound+=dash
    if sigh==' ':
        sound+=space
sound+=space

#форматирование массива данных str --> int
sound=list(map(lambda x: int(x), sound.split(", ")))


#Установка частоты дискретизации и прочих обязательных значений формата звукового файла
dest.setnchannels(1)
dest.setsampwidth(2)
dest.setframerate(44100)

#обратная кодировка dec --> bin
updated_frames=struct.pack("<" + str(len(sound)) + "h", *sound)
dest.writeframes(updated_frames)

#Вывод графической составляющей
plt.plot(sound)
plt.show()

