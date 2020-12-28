INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
masses = list(map(int, raw.strip().split()))

print(sum(mass // 3 - 2 for mass in masses))

def fuel_requirement(mass: int) -> int:
	fuel = mass // 3 - 2
	return fuel + fuel_requirement(fuel) if fuel > 0 else 0
print(sum(map(fuel_requirement, masses)))
