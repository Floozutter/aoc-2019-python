from itertools import permutations

INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

def getdata(filepath):
    with open(filepath) as ifile:
        lines = ifile.read()
    return [int(l) for l in lines.split(",")]

program = getdata(INPUTPATH)

"""
def run2(initial, inputlist):
    return


highest = 0
for perm in permutations(range(5)):
    A = run2(program, [perm[0], 0])
    B = run2(program, [perm[1], A])
    C = run2(program, [perm[2], B])
    D = run2(program, [perm[3], C])
    E = run2(program, [perm[4], D])
    print(perm, A, B, C, D, E)
    if E > highest:
        highest = E
"""

class Program:
    def __init__(self, initial):
        self.state = initial.copy()
        self.pos = 0
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
        if opcode == "01":
            p[p[pos+3]] = arg1 + arg2
            self.pos += 4
        elif opcode == "02":
            p[p[pos+3]] = arg1 * arg2
            self.pos += 4
        elif opcode == "03":
            p[p[pos+1]] = inp
            #inputindex += 1
            self.pos += 2
            return True
        elif opcode == "04":
            self.pos += 2
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
            p[p[pos+3]] = 0
            if arg1 < arg2:
                p[p[pos+3]] = 1
            self.pos += 4
        elif opcode == "08":
            p[p[pos+3]] = 0
            if arg1 == arg2:
                p[p[pos+3]] = 1
            self.pos += 4
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



def runperm(perm):
    A = Program(program)
    B = Program(program)
    C = Program(program)
    D = Program(program)
    E = Program(program)
    A.put(perm[0])
    B.put(perm[1])
    C.put(perm[2])
    D.put(perm[3])
    E.put(perm[4])
    Eouts = []
    A.put(0)
    while True:
        binp = A.get()
        if binp is False:
            return Eouts[-1]
        B.put(binp)
        cinp = B.get()
        if cinp is False:
            return Eouts[-1]
        C.put(cinp)
        dinp = C.get()
        if dinp is False:
            return Eouts[-1]
        D.put(dinp)
        einp = D.get()
        if einp is False:
            return Eouts[-1]
        E.put(einp)
        ainp = E.get()
        Eouts.append(ainp)
        if ainp is False:
            return Eouts[-1]
        A.put(ainp)

highest = 0
for perm in permutations(range(5, 10)):
    out = runperm(perm)
    if highest < out:
        highest = out
print(highest)
