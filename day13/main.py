INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

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
            inp = getinput()
            if len(instruct) >= 3 and instruct[-3] == "2":
                p[self.base + p[pos+1]] = inp
            else:
                p[p[pos+1]] = inp
            self.pos += 2
            return None
            #return True
        elif opcode == "04":
            self.pos += 2
            #print(arg1)
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

data[0] = 2

A = Program(data)

screen = dict()
def stringifyscreen(scr):
    rows = [[]]
    for k, v in scr.items():
        while k[1] > (len(rows)-1):
            rows.append([])
        while k[0] > (len(rows[k[1]])-1):
            rows[k[1]].append(" ")
        if v == 0:
            tile = " "
        elif v == 1:
            tile = "W"
        elif v == 2:
            tile = "#"
        elif v == 3:
            tile = "+"
        elif v == 4:
            tile = "0"
        else:
            tile = "?"
        rows[k[1]][k[0]] = tile
    out = ""
    for row in rows:
        out += "".join(row) + "\n"
    return out

prevballmove = (1, 1)
prevballpos = None
def getmove(scr):
    global prevballmove
    global prevballpos
    scrstr = stringifyscreen(scr).split("\n")
    ballpos = None
    for i, row in enumerate(scrstr):
        for j, tile in enumerate(row):
            if tile == "0":
                ballpos = (i, j)
                break
    if ((prevballpos is not None) and
        (ballpos != (prevballpos[0]+prevballmove[0],prevballpos[1]+prevballmove[1]))):
        print("bad!")
        while input() != "!":
            pass
    prevballpos = ballpos
    
    yourpos = None
    for i, row in enumerate(scrstr):
        for j, tile in enumerate(row):
            if tile == "+":
                yourpos = (i, j)
                break
    
    ballmove = prevballmove
    #print(scrstr[ballpos[0]+prevballmove[0]][ballpos[1]])
    #print(prevballmove)
    if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
            ballmove = (-ballmove[0], -ballmove[1])
            if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] == "#":
                scrstr[ballpos[0]] = list(scrstr[ballpos[0]])
                scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] = " "
                scrstr[ballpos[0]] = "".join(scrstr[ballpos[0]])
            if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] == "#":
                scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
                scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] = " "
                scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
        else:
            ballmove =(-ballmove[0], ballmove[1])
            if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] == "#":
                scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
                scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] = " "
                scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
    elif scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] == "#":
            scrstr[ballpos[0]] = list(scrstr[ballpos[0]])
            scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] = " "
            scrstr[ballpos[0]] = "".join(scrstr[ballpos[0]])
        ballmove = (ballmove[0], -ballmove[1])
    elif scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] == "#":
            scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
            scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] = " "
            scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
        ballmove = (-ballmove[0], -ballmove[1])
    prevballmove = ballmove
    if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
            ballmove = (-ballmove[0], -ballmove[1])
            if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] == "#":
                scrstr[ballpos[0]] = list(scrstr[ballpos[0]])
                scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] = " "
                scrstr[ballpos[0]] = "".join(scrstr[ballpos[0]])
            if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] == "#":
                scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
                scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] = " "
                scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
        else:
            ballmove =(-ballmove[0], ballmove[1])
            if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] == "#":
                scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
                scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] = " "
                scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
    elif scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] == "#":
            scrstr[ballpos[0]] = list(scrstr[ballpos[0]])
            scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] = " "
            scrstr[ballpos[0]] = "".join(scrstr[ballpos[0]])
        ballmove = (ballmove[0], -ballmove[1])
    elif scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] == "#":
            scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
            scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] = " "
            scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
        ballmove = (-ballmove[0], -ballmove[1])
    prevballmove = ballmove
    if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
            ballmove = (-ballmove[0], -ballmove[1])
            if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] == "#":
                scrstr[ballpos[0]] = list(scrstr[ballpos[0]])
                scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] = " "
                scrstr[ballpos[0]] = "".join(scrstr[ballpos[0]])
            if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] == "#":
                scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
                scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] = " "
                scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
        else:
            ballmove =(-ballmove[0], ballmove[1])
            if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] == "#":
                scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
                scrstr[ballpos[0]+prevballmove[0]][ballpos[1]] = " "
                scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
    elif scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] == "#":
            scrstr[ballpos[0]] = list(scrstr[ballpos[0]])
            scrstr[ballpos[0]][ballpos[1]+prevballmove[1]] = " "
            scrstr[ballpos[0]] = "".join(scrstr[ballpos[0]])
        ballmove = (ballmove[0], -ballmove[1])
    elif scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] in ("+", "#", "W"):
        if scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] == "#":
            scrstr[ballpos[0]+prevballmove[0]] = list(scrstr[ballpos[0]+prevballmove[0]])
            scrstr[ballpos[0]+prevballmove[0]][ballpos[1]+prevballmove[1]] = " "
            scrstr[ballpos[0]+prevballmove[0]] = "".join(scrstr[ballpos[0]+prevballmove[0]])
        ballmove = (-ballmove[0], -ballmove[1])
    prevballmove = ballmove
    
    if ballpos[0]+ballmove[0] == yourpos[0]:
        ballmove = (-ballmove[0], ballmove[1])

    prevballmove = ballmove

    horidiff = (ballpos[1]+ballmove[1]) - yourpos[1]
    if (ballpos[0] == (yourpos[0]-1)) and (ballpos[1] == yourpos[1]):
        horidiff = 0
    move = 0
    if horidiff > 0:
        move = 1
    elif horidiff < 0:
        move = -1
    #print(ballmove)
    #print(yourpos[1], "vs", ballpos[1], ballmove[1])
    #print(horidiff, move)
    #input()
    return move
    
    

def getinput():
    global screen
    inp = getmove(screen)
    while False:
        inp = input("Move: ")
        if inp == "q":
            inp = -1
            break
        elif inp == "e":
            inp = 1
            break
        elif inp == "w":
            inp = 0
            break
        elif inp == "":
            inp = getmove(screen)
            break
    return inp

while True:
    x = A.get()
    if x is False:
        break
    y = A.get()
    tile = A.get()
    if (x, y) == (-1, 0):
        print("Score:", tile)        
    else:
        print("")
        screen[(x, y)] = tile
    print(stringifyscreen(screen))




