INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

def getdata(filepath):
    with open(filepath) as ifile:
        lines = ifile.read()
    return [int(l) for l in lines.split(",")]

program = getdata(INPUTPATH)

def run(initial, noun, verb):
    p = initial.copy()
    p[1] = noun
    p[2] = verb
    pos = 0
    while True:
        if p[pos] == 99:
            break
        elif p[pos] == 1:
            p[p[pos+3]] = p[p[pos+1]] + p[p[pos+2]]
        elif p[pos] == 2:
            p[p[pos+3]] = p[p[pos+1]] * p[p[pos+2]]
        else:
            assert False, "bad"
        pos += 4
    return p[0]

print(run(program, 12, 2))


def guess(initial, expected):
    for i in range(0, 100):
        for j in range(0, 100):
            if run(initial, i, j) == expected:
                return (i, j)

print(guess(program, 19690720))
