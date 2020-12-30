INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
lower, upper = map(int, raw.strip().split("-"))
passwords = tuple(map(str, range(lower, upper + 1)))

from itertools import groupby
from typing import Callable
def valid(group_size_rule: Callable[[int], bool], password: str) -> bool:
	nondecreasing = all(a <= b for a, b in zip(password, password[1:]))
	has_valid_group = any(
		group_size_rule(sum(1 for _ in group))
		for _, group in groupby(password)
	)
	return nondecreasing and has_valid_group

print(sum(1 for p in passwords if valid(lambda s: s > 1, p)))
print(sum(1 for p in passwords if valid(lambda s: s == 2, p)))
