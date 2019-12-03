INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

changes = [int(l) for l in lines.split()]
print(sum(changes))


freqs = set()
current = 0
i = 0
while True:
    current += changes[i]
    if current in freqs:
        break
    freqs.add(current)
    i = (i + 1) % len(changes)

print(current)
