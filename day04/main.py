INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

data = list(map(int, lines.split("-")))


def yes(s):
    s = str(s)
    adj = False
    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            adj = True
    if not adj:
        return False
    decreases = False
    for i in range(1, len(s)):
        if int(s[i]) < int(s[i-1]):
            return False
    return True

def yes2(s):
    s = str(s)
    adj = False
    last = None
    for i in range(len(s) - 1):
        if s[i] == last:
            continue
        reps = 0
        while ((i + reps + 1) < len(s)) and (s[i] == s[i + reps + 1]):
            reps += 1
        if reps == 1:
            adj = True
        last = s[i]
    if not adj:
        return False
    decreases = False
    for i in range(1, len(s)):
        if int(s[i]) < int(s[i-1]):
            return False
    return True

print(sum([1 for i in range(data[0], data[1]+1) if yes(i)]))
print(sum([1 for i in range(data[0], data[1]+1) if yes2(i)]))
