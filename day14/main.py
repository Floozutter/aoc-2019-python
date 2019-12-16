from collections import Counter

INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

reqs = dict()
for line in lines.strip().split("\n"):
    recipe, thing = line.split("=>")
    thingcount, thing = thing.strip().split(" ")
    thingcount = int(thingcount)
    comps = set()
    for part in recipe.strip().split(", "):
        compcount, compthing = part.strip().split(" ")
        comps.add( (compthing, int(compcount.strip())) )
    reqs[thing] = (thingcount, comps)

def orecount(reqdict, thing):
    reqlist = [thing]
    extras = []
    def oresonly(reqlist):
        for req in reqlist:
            if req != "ORE":
                return False
        return True
    while not oresonly(reqlist):
        newreqs = []
        for req in reqlist:
            if req == "ORE":
                newreqs.append(req)
                continue
            elif req in extras:
                extras.remove(req)
                continue
            outputcount, reqs4req = reqdict[req]
            for i in range(outputcount - 1):
                extras.append(req)
            for reqreq, reqcount in reqs4req:
                for i in range(reqcount):
                    if reqreq in extras:
                        extras.remove(reqreq)
                    else:
                        newreqs.append(reqreq)
        reqlist = newreqs[:]
    return len(reqlist)

#print(orecount(reqs, "FUEL"))

def orecount(reqdict, thing, amount):
    reqcounter = Counter({thing: amount})
    extras = Counter()
    def oresonly(reqcounter):
        for k, v in reqcounter.items():
            if k != "ORE" and v > 0:
                return False
        return True

    while not oresonly(reqcounter):
        newreqcounter = Counter()
        for k, v in reqcounter.items():
            if k == "ORE":
                newreqcounter["ORE"] += v
                continue
            for i in range(v):
                if extras[k] > 0:
                    extras[k] -= 1
                    continue
                outputcount, reqs4req = reqdict[k]
                extras[k] += outputcount-1
                for reqreq, reqcount in reqs4req:
                    for j in range(reqcount):
                        if extras[reqreq] > 0:
                            extras[reqreq] -= 1
                        else:
                            newreqcounter[reqreq] += 1
        reqcounter = Counter(newreqcounter)
    return reqcounter["ORE"]

print(orecount(reqs, "FUEL", 1))

def addfueluntilnotenoughore(reqdict, oreamount):
    fuel = 1
    reqcounter = Counter({"FUEL": 1})
    extras = Counter()
    def oresonly(reqcounter):
        for k, v in reqcounter.items():
            if k != "ORE" and v > 0:
                return False
        return True

    while True:
        if oresonly(reqcounter):
            print(fuel, reqcounter["ORE"])
            if reqcounter["ORE"] > oreamount:
                return fuel
            fuel += 1
            reqcounter["FUEL"] += 1
        newreqcounter = Counter()
        for k, v in reqcounter.items():
            if k == "ORE":
                newreqcounter["ORE"] += v
                continue
            for i in range(v):
                if extras[k] > 0:
                    extras[k] -= 1
                    continue
                outputcount, reqs4req = reqdict[k]
                extras[k] += outputcount-1
                for reqreq, reqcount in reqs4req:
                    for j in range(reqcount):
                        if extras[reqreq] > 0:
                            extras[reqreq] -= 1
                        else:
                            newreqcounter[reqreq] += 1
        reqcounter = Counter(newreqcounter)

print(addfueluntilnotenoughore(reqs, 1000000000000))
