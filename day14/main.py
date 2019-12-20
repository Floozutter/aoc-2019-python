from collections import Counter
from math import ceil

INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    data = ifile.read()

def parse_reactions(inputstring):
    reactionsdict = dict()
    for line in inputstring.strip().split("\n"):
        reactants, product = line.split("=>")
        pcount, pname = product.strip().split(" ")
        pcount = int(pcount)
        reactantlist = list()
        for reactant in reactants.strip().split(", "):
            rcount, rname = reactant.strip().split(" ")
            rcount = int(rcount)
            reactantlist.append( (rcount, rname) )
        reactionsdict[pname] = (pcount, tuple(reactantlist))
    return reactionsdict

def ore_requirement(reactionsdict, product, quantity):
    reqdict = Counter({product: quantity})
    extras = Counter()
    while not all(k == "ORE" or v == 0 for k, v in reqdict.items()):
        # break when requirements are only ore
        for k in list(reqdict.keys()):
            if k == "ORE" or reqdict[k] == 0:
                continue
            if extras[k] >= reqdict[k]:
                extras[k] -= reqdict[k]
                reqdict[k] = 0
                continue
            else:
                reqdict[k] -= extras[k]
                extras[k] = 0
            products_per_reaction, reactant_reqs = reactionsdict[k]
            reactions = ceil(reqdict[k] / products_per_reaction)
            products = reactions * products_per_reaction
            extras[k] += products - reqdict[k]
            reqdict[k] = 0
            for rr in reactant_reqs:
                rcount, rname = rr
                reqdict[rname] += rcount * reactions
    return reqdict["ORE"]

reactions = parse_reactions(data)
print(ore_requirement(reactions, "FUEL", 1))


def addfueluntilnomoreore(reactionsdict, available_ore, log=False):
    fuel = 0
    reqdict = Counter()
    extras = Counter()
    while True:
        if all(k == "ORE" or v == 0 for k, v in reqdict.items()):
            if log and (fuel % 1000 == 0):
                print("FUEL:", fuel, "| ORE:", f'{reqdict["ORE"]:,}')
            if reqdict["ORE"] > available_ore:
                return fuel - 1
            fuel += 1
            reqdict["FUEL"] += 1
        for k in list(reqdict.keys()):
            if k == "ORE" or reqdict[k] == 0:
                continue
            if extras[k] >= reqdict[k]:
                extras[k] -= reqdict[k]
                reqdict[k] = 0
                continue
            else:
                reqdict[k] -= extras[k]
                extras[k] = 0
            products_per_reaction, reactant_reqs = reactionsdict[k]
            reactions = ceil(reqdict[k] / products_per_reaction)
            products = reactions * products_per_reaction
            extras[k] += products - reqdict[k]
            reqdict[k] = 0
            for rr in reactant_reqs:
                rcount, rname = rr
                reqdict[rname] += rcount * reactions
    print("How did you get here?")

print(addfueluntilnomoreore(reactions, 1000000000000, True))
