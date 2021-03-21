def fontList(i):
    file = open("./font.txt","r",encoding='UTF8')
    arr = []
    line = file.readline()
    arr.append(line.rstrip('\n').split(","))
    while line:
        line = file.readline()
        arr.append(line.rstrip('\n').split(","))
    file.close()
    return arr[i]



def numfont(d, s):
    result = ""
    st = fontList(s)
    for i in str(d):
        try:
            result += st[int(i)]
        except:
            if i == "." and s < 8:
                result += "."
            elif s == 8:
                if i == ".":
                    result += st[10]
                elif i == "%":
                    result += st[11]
                elif i == "/":
                    result += st[12]
                
    return result
