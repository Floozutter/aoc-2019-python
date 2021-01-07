INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
from typing import Tuple
def line_to_pos(line: str) -> Tuple[int, int, int]:
	filtered = "".join(c for c in line if c.isdigit() or c in {"-", ","})
	return tuple(map(int, filtered.split(",")))
start_positions = tuple(map(line_to_pos, raw.strip().split("\n")))

from itertools import combinations
from typing import List, Iterable
class System:
	poss: List[List[int]]
	vels: List[List[int]]
	def __init__(self, poss: Iterable[Iterable[int]]) -> None:
		self.poss = [list(pos) for pos in poss]
		self.vels = [[0] * len(pos) for pos in self.poss]
	def __eq__(self, other) -> bool:
		return self.poss == other.poss and self.vels == other.vels
	def step(self, n: int) -> None:
		for _ in range(n):
			for i, j in combinations(range(len(self.poss)), 2):
				for ax, (a, b) in enumerate(zip(self.poss[i], self.poss[j])):
					if a < b:
						self.vels[i][ax] += 1
						self.vels[j][ax] -= 1
					elif a > b:
						self.vels[i][ax] -= 1
						self.vels[j][ax] += 1
			for pos, vel in zip(self.poss, self.vels):
				for i in range(len(pos)):
					pos[i] += vel[i]
	def total_energy(self) -> int:
		return sum(
			sum(map(abs, pos)) * sum(map(abs, vel))
			for pos, vel in zip(self.poss, self.vels)
		)

system = System(start_positions)
system.step(1000)
print(system.total_energy())

tort = System(start_positions)
tort.step(1)
hare = System(start_positions)
hare.step(2)
steps = 1
from time import time
t = time()
while tort != hare:
	if steps % 100_000 == 0: print(f"Steps: {steps:,}")
	tort.step(1)
	hare.step(2)
	steps += 1
print(f"Time Elapsed: {time() - t}")
print(steps)
