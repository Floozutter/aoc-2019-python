INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

claims = list(filter(None, lines.split("\n")))

fabric = dict()

def markclaim(markdict, claim):
    parts = claim.split(" ")
    code = int(parts[0][1:])
    coor = tuple(map(int, parts[2][:-1].split(",")))
    size = tuple(map(int, parts[3].split("x")))
    for i in range(coor[0], coor[0]+size[0]):
        for j in range(coor[1], coor[1]+size[1]):
            if (i, j) not in markdict:
                markdict[(i, j)] = []
            markdict[(i, j)].append(code)
            
for c in claims:
    markclaim(fabric, c)

count = 0
for k, v in fabric.items():
    if len(v) >= 2:
        count += 1
print(count)


def checkclaim(markdict, claim):
    parts = claim.split(" ")
    code = int(parts[0][1:])
    coor = tuple(map(int, parts[2][:-1].split(",")))
    size = tuple(map(int, parts[3].split("x")))
    for i in range(coor[0], coor[0]+size[0]):
        for j in range(coor[1], coor[1]+size[1]):
            if len(markdict[(i, j)]) != 1:
                return False
    return True

for c in claims:
    if checkclaim(fabric, c):
        print(c)
