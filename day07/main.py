INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
program = tuple(map(int, raw.strip().split(",")))

from enum import Enum
class Mde(Enum):
	POS = 0
	IMM = 1
from itertools import chain, repeat, islice
from typing import Dict, Callable, List, Iterable, Optional, ClassVar
class Ico:
	liv: bool
	ptr: int
	mem: Dict[int, int]
	cal: Callable[[], int]
	log: List[int]
	def __init__(self, prg: Iterable[int], cal: Callable[[], int]) -> None:
		self.liv = True
		self.ptr = 0
		self.mem = dict(enumerate(prg))
		self.cal = cal
		self.log = list()
	def get(self, mde: Mde) -> int:
		if   mde == Mde.POS: idx = self.mem[self.ptr]
		elif mde == Mde.IMM: idx = self.ptr
		self.ptr += 1
		return idx
	def ste(self) -> int:
		if not self.liv: return 99
		val = self.mem[self.get(Mde.IMM)]
		opc = val % 100
		mds = map(Mde, chain(map(int, reversed(str(val // 100))), repeat(0)))
		opr = self.ops[opc]
		opr(self, *map(self.get, islice(mds, opr.__code__.co_argcount - 1)))
		return opc
	def run(self) -> List[int]:
		while self.liv: self.ste()
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

def thruster_signal(settings: Iterable[int]) -> int:
	class Callback:
		def __init__(self, first: int, second: int) -> None:
			self.first = first
			self.second = second
			self.called = False
		def __call__(self) -> int:
			if not self.called:
				self.called = True
				return self.first
			else:
				return self.second
	signal = 0
	for s in settings:
		signal = Ico(program, Callback(s, signal)).run()[-1]
	return signal
from itertools import permutations
print(max(map(thruster_signal, permutations(range(5)))))

def feedback_thruster_signal(settings: Iterable[int]) -> int:
	class Callback:
		def __init__(self, first: int) -> None:
			self.first = first
			self.log = None
			self.called = False
		def set_log(self, log: List[int]) -> None:
			self.log = log
		def __call__(self) -> int:
			if not self.called:
				self.called = True
				return self.first
			elif not self.log:
				return 0
			else:
				return self.log[-1]
	icos = tuple(Ico(program, Callback(s)) for s in settings)
	for a, b in zip(icos, icos[1:] + (icos[0],)):
		b.cal.set_log(a.log)
	while icos[-1].liv:
		for ico in icos:
			while ico.liv and ico.ste() != 4: pass
	return icos[-1].log[-1]
print(max(map(feedback_thruster_signal, permutations(range(5, 10)))))
