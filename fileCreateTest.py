file = open("test.txt", "w")
s= ''
for i in range(0,100000000):
    s += str(i)
file.write(s)
fileObj.close()
