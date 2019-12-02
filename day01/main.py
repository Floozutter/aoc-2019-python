INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

def getdata(filepath):
    with open(filepath) as ifile:
        lines = ifile.read()
    return [int(l) for l in lines.split()]

masses = getdata(INPUTPATH)
total = sum(m // 3 - 2 for m in masses)
print(total)

def get_req2(mass):
    req = 0
    extra = mass // 3 - 2
    while extra > 0:
        req += extra
        extra = extra // 3 - 2
    return req


total2 = sum(get_req2(m) for m in masses)
print(total2)
