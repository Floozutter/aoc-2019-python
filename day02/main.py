INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
program = tuple(map(int, raw.strip().split(",")))

from operator import add, mul
from typing import Iterable
def run(program: Iterable[int], noun: int, verb: int) -> int:
	m = list(program)
	m[1], m[2] = noun, verb
	p = 0
	while (opcode := m[p]) != 99:
		m[m[p + 3]] = (add if opcode == 1 else mul)(m[m[p + 1]], m[m[p + 2]])
		p += 4
	return m[0]

print(run(program, 12, 2))

from itertools import product
print(next(
	100 * noun + verb
	for noun, verb in product(range(100), repeat = 2)
	if run(program, noun, verb) == 19690720
))
