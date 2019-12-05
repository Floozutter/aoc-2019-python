import re
from collections import defaultdict

INPUTPATH = "input.txt"
INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

records = [l for l in lines.split("\n") if l]
    

def sleepiest(records):
    sleeps = dict()
    guard = None
    waketime = None
    t = None
    for line in records:
        t = line[12:12+5]
        shiftmatch = re.search("#(\d+)", line)
        if shiftmatch:
            guard = int(shiftmatch.group(1))
            waketime = t
        elif "falls" in line:
            pass

sleepiest(records)
