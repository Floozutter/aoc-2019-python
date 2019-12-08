from collections import defaultdict

INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

data = lines.strip()

# 25, 6 dim

images = defaultdict(list)

for i, d in enumerate(data):
    images[i // (25*6)].append(int(d))

fewest = None
for k, v in images.items():
    if (fewest is None) or (v.count(0) < images[fewest].count(0)):
        fewest = k

print(images[fewest].count(1) * images[fewest].count(2))


decoded = [None] * len(images[0])
for k, v in images.items():
    for i, p in enumerate(v):
        if decoded[i] is None:
            if (p == 1):
                decoded[i] = 1
            elif (p == 0):
                decoded[i] = 0

for i, v in enumerate(decoded):
    if (i % 25) == 0:
        print("")
    if v == 0:
        print(" ", end="")
    else:
        print("#", end="")
