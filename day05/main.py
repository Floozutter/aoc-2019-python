INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
prg = tuple(map(int, raw.strip().split(",")))

from enum import Enum
class Mde(Enum):
	POS = 0
	IMM = 1
from itertools import chain, repeat, islice
from operator import methodcaller
from typing import List, Dict, Callable, Iterable, ClassVar
class Ico:
	liv: bool
	ptr: int
	mem: List[int]
	cal: Callable[[], int]
	log: List[int]
	def __init__(self, prg: Iterable[int], cal: Callable[[], int]) -> None:
		self.liv = True
		self.ptr = 0
		self.mem = list(prg)
		self.cal = cal
		self.log = list()
	def get(self, mde: Mde) -> int:
		if   mde == Mde.POS: idx = self.mem[self.ptr]
		elif mde == Mde.IMM: idx = self.ptr
		self.ptr += 1
		return idx
	def ste(self) -> None:
		val = self.mem[self.get(Mde.IMM)]
		opc = val % 100
		mds = map(Mde, chain(map(int, reversed(str(val // 100))), repeat(0)))
		opr = self.ops[opc]
		opr(self, *map(self.get, islice(mds, opr.__code__.co_argcount - 1)))
	def run(self) -> List[int]:
		while self.liv:
			self.ste()
		return self.log
	def add(self, idx: int, jdx: int, kdx: int) -> None:
		self.mem[kdx] = self.mem[idx] + self.mem[jdx]
	def mul(self, idx: int, jdx: int, kdx: int) -> None:
		self.mem[kdx] = self.mem[idx] * self.mem[jdx]
	def inp(self, idx: int) -> None:
		self.mem[idx] = self.cal()
	def out(self, idx: int) -> None:
		self.log.append(self.mem[idx])
	def jit(self, idx: int, jdx: int) -> None:
		if self.mem[idx]: self.ptr = self.mem[jdx]
	def jif(self, idx: int, jdx: int) -> None:
		if not self.mem[idx]: self.ptr = self.mem[jdx]
	def les(self, idx: int, jdx: int, kdx: int) -> None:
		self.mem[kdx] = int(self.mem[idx] < self.mem[jdx])
	def equ(self, idx: int, jdx: int, kdx: int) -> None:
		self.mem[kdx] = int(self.mem[idx] == self.mem[jdx])
	def hal(self) -> None:
		self.liv = False
	ops: ClassVar[Dict[int, Callable[..., None]]] = {
		 1: add,
		 2: mul,
		 3: inp,
		 4: out,
		 5: jit,
		 6: jif,
		 7: les,
		 8: equ,
		99: hal
	}

print(Ico(prg, lambda: 1).run()[-1])
print(Ico(prg, lambda: 5).run()[-1])
