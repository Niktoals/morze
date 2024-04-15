dot=open("space.txt", "r")
dot2=open("space2.txt", "a")
for i in dot.readline():
    if i!=",":
        dot2.write(i)
dot.close()
dot2.close()