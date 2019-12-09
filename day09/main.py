INPUTPATH = "input.txt"
INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

data = [int(l) for l in lines.strip().split(",")]



class Program:
    def __init__(self, initial):
        self.state = initial.copy()
        self.pos = 0
        self.base = 0
        self.halted = False
    def next(self, inp):
        if self.halted:
            return False
        p = self.state
        pos = self.pos
        instruct = str(p[pos])   
        if len(instruct) == 1:
            opcode = "0" + instruct
        else:
            opcode = instruct[-2:]
        if opcode == "99":
            self.halted = True
            return False
        if len(instruct) >= 3 and instruct[-3] == "1":
            arg1 = p[pos+1]
        elif len(instruct) >= 3 and instruct[-3] == "2":
            arg1 = p[self.base + p[pos+1]]
        else:
            arg1 = p[p[pos+1]]
        if opcode in ["01", "02", "05", "06", "07", "08"]:
            if len(instruct) >= 4 and instruct[-4] == "1":
                arg2 = p[pos+2]
            elif len(instruct) >= 4 and instruct[-4] == "2":
                arg2 = p[self.base + p[pos+2]]
            else:
                arg2 = p[p[pos+2]]
            if opcode in ["01", "02", "07", "08"]:  
                if len(instruct) >= 5 and instruct[-5] == "1":
                    arg3 = p[pos+3]
                elif len(instruct) >= 5 and instruct[-5] == "2":
                    arg3 = p[self.base + p[pos+3]]
                else:
                    arg3 = p[p[pos+3]]
        if opcode == "01":
            if len(instruct) >= 5 and instruct[-5] == "2":
                p[self.base + p[pos+3]] = arg1 + arg2
            else:
                p[p[pos+3]] = arg1 + arg2
            self.pos += 4
        elif opcode == "02":
            if len(instruct) >= 5 and instruct[-5] == "2":
                p[self.base + p[pos+3]] = arg1 * arg2
            else:
                p[p[pos+3]] = arg1 * arg2
            self.pos += 4
        elif opcode == "03":
            if len(instruct) >= 3 and instruct[-3] == "2":
                p[self.base + p[pos+1]] = inp
            else:
                p[p[pos+1]] = inp
            #inputindex += 1
            self.pos += 2
            return True
        elif opcode == "04":
            self.pos += 2
            print(arg1)
            return arg1
        elif opcode == "05":
            if arg1 != 0:
                self.pos = arg2
            else:
                self.pos += 3
        elif opcode == "06":
            if arg1 == 0:
                self.pos = arg2
            else:
                self.pos += 3
        elif opcode == "07":
            if len(instruct) >= 5 and instruct[-5] == "2":
                p[self.base + p[pos+3]] = 0
            else:
                p[p[pos+3]] = 0
            if arg1 < arg2:
                if len(instruct) >= 5 and instruct[-5] == "2":
                    p[self.base + p[pos+3]] = 1
                else:
                    p[p[pos+3]] = 1
            self.pos += 4
        elif opcode == "08":
            if len(instruct) >= 5 and instruct[-5] == "2":
                p[self.base + p[pos+3]] = 0
            else:
                p[p[pos+3]] = 0
            if arg1 == arg2:
                if len(instruct) >= 5 and instruct[-5] == "2":
                    p[self.base + p[pos+3]] = 1
                else:
                    p[p[pos+3]] = 1
            self.pos += 4
        elif opcode == "09":
            self.base += arg1
            self.pos += 2
        else:
            assert False, "bad"
        return None
    def put(self, inp):
        while True:
            out = self.next(inp)
            if isinstance(out, bool):
                return
    def get(self):
        while True:
            out = self.next(None)
            if isinstance(out, int) or isinstance(out, bool):
                return out


for i in range(1000):
    data.append(0)

A = Program(data)

while True:
    x = A.next(2)
    if x is False:
        break

