INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

def getdata(filepath):
    with open(filepath) as ifile:
        lines = ifile.read()
    return [int(l) for l in lines.split()]

x = getdata(INPUTPATH)
