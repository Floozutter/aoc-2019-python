INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

def getdata(filepath):
    with open(filepath) as ifile:
        lines = ifile.read()
    return [int(l) for l in lines.split(",")]

program = getdata(INPUTPATH)


def run(initial, inputlist):
    p = initial.copy()
    pos = 0
    inputindex = 0
    while True:
        
        instruct = str(p[pos])
        if len(instruct) == 1:
            opcode = "0" + instruct
        else:
            opcode = instruct[-2:]
        
        if len(instruct) >= 3 and instruct[-3] == "1":
            arg1 = p[pos+1]
        else:
            arg1 = p[p[pos+1]]
        if opcode in ["01", "02"]:
            if len(instruct) >= 4 and instruct[-4] == "1":
                arg2 = p[pos+2]
            else:
                arg2 = p[p[pos+2]]
            if len(instruct) >= 5 and instruct[-5] == "1":
                arg3 = p[pos+3]
            else:
                arg3 = p[p[pos+3]]
        if opcode == "99":
            break
        elif opcode == "01":
            p[p[pos+3]] = arg1 + arg2
            pos += 4
        elif opcode == "02":
            p[p[pos+3]] = arg1 * arg2
            pos += 4
        elif opcode == "03":
            p[p[pos+1]] = inputlist[inputindex]
            inputindex += 0
            pos += 2
        elif opcode == "04":
            if arg1 != 0:
                print("bad diag: " + str(arg1))
                return
            print(arg1)
            pos += 2
        else:
            assert False, "bad"
    return

def run2(initial, inputlist):
    p = initial.copy()
    pos = 0
    inputindex = 0
    while True:
        
        instruct = str(p[pos])   
        if len(instruct) == 1:
            opcode = "0" + instruct
        else:
            opcode = instruct[-2:]
        print(p, pos, opcode)
        if len(instruct) >= 3 and instruct[-3] == "1":
            arg1 = p[pos+1]
        else:
            arg1 = p[p[pos+1]]
        if opcode in ["01", "02", "05", "06", "07", "08"]:
            if len(instruct) >= 4 and instruct[-4] == "1":
                arg2 = p[pos+2]
            else:
                arg2 = p[p[pos+2]]
            if opcode in ["01", "02", "07", "08"]:
                if len(instruct) >= 5 and instruct[-5] == "1":
                    arg3 = p[pos+3]
                else:
                    arg3 = p[p[pos+3]]
        if opcode == "99":
            break
        elif opcode == "01":
            p[p[pos+3]] = arg1 + arg2
            pos += 4
        elif opcode == "02":
            p[p[pos+3]] = arg1 * arg2
            pos += 4
        elif opcode == "03":
            p[p[pos+1]] = inputlist[inputindex]
            inputindex += 0
            pos += 2
        elif opcode == "04":
            if arg1 != 0:
                print("bad diag: " + str(arg1))
                return
            print(arg1)
            pos += 2
        elif opcode == "05":
            if arg1 != 0:
                pos = arg2
            else:
                pos += 3
        elif opcode == "06":
            if arg1 == 0:
                pos = arg2
            else:
                pos += 3
        elif opcode == "07":
            p[p[pos+3]] = 0
            if arg1 < arg2:
                p[p[pos+3]] = 1
            pos += 4
        elif opcode == "08":
            p[p[pos+3]] = 0
            if arg1 == arg2:
                p[p[pos+3]] = 1
            pos += 4
        else:
            assert False, "bad"
    return

run(program, [1])
run2(program, [5])

