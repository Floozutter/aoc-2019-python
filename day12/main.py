INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
from typing import Tuple
def line_to_pos(line: str) -> Tuple[int, int, int]:
	filtered = "".join(c for c in line if c.isdigit() or c in {"-", ","})
	return tuple(map(int, filtered.split(",")))
starts = tuple(zip(*map(line_to_pos, raw.strip().split("\n"))))

from itertools import combinations
from typing import List, Iterable
class Axis:
	poss: List[int]
	vels: List[int]
	def __init__(self, poss: Iterable[int]) -> None:
		self.poss = list(poss)
		self.vels = [0] * len(self.poss)
	def __eq__(self, other) -> bool:
		return self.poss == other.poss and self.vels == other.vels
	def step(self, n: int) -> None:
		for _ in range(n):
			for i, j in combinations(range(len(self.poss)), 2):
				a, b = self.poss[i], self.poss[j]
				diff = 1 if a < b else -1 if a > b else 0
				self.vels[i] += diff
				self.vels[j] -= diff
			for i, vel in enumerate(self.vels):
				self.poss[i] += vel

system = tuple(map(Axis, starts))
for axis in system:
	axis.step(1000)
moon_poss = zip(*(axis.poss for axis in system))
moon_vels = zip(*(axis.vels for axis in system))
print(sum(
	sum(map(abs, pos)) * sum(map(abs, vel))
	for pos, vel in zip(moon_poss, moon_vels)
))

def detect_cycle(poss: Iterable[int]) -> Tuple[int, int]:
	tort = Axis(poss)
	hare = Axis(tort.poss)
	tort.step(1)
	hare.step(2)
	first_repeat = 1
	while tort != hare:
		tort.step(1)
		hare.step(2)
		first_repeat += 1
	hare.step(1)
	period = 1
	while hare != tort:
		hare.step(1)
		period += 1
	return first_repeat - period, period
system_mu = 0
system_period = 1
from math import lcm
for mu, period in map(detect_cycle, starts):
	while system_mu % period != mu:
		system_mu += system_period
	system_period = lcm(system_period, period)
print(system_mu + system_period)
