INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

import string

with open(INPUTPATH) as ifile:
    lines = ifile.read()

ids = lines.split()

def has(boxid, n):
    for c in string.ascii_lowercase:
        if boxid.count(c) == n:
            return True
    return False

ids_any2 = [s for s in ids if has(s, 2)]
ids_any3 = [s for s in ids if has(s, 3)]

print(len(ids_any2) * len(ids_any3))


def common(str1, str2):
    return "".join(a for a, b in zip(str1, str2) if a == b)

for i in ids:
    for j in ids:
        shared = common(i, j)
        if len(shared) + 1 == len(i):
            print(shared)
