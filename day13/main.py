INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
program = tuple(map(int, raw.strip().split(",")))

from enum import Enum
class Mde(Enum):
	POS = 0
	IMM = 1
	REL = 2
from itertools import chain, repeat, islice
from collections import defaultdict
from typing import Dict, Callable, List, Iterable, Optional, ClassVar
class Ico:
	liv: bool
	ptr: int
	reb: int
	mem: Dict[int, int]
	cal: Callable[[], int]
	log: List[int]
	def __init__(
		self,
		prg: Iterable[int],
		cal: Callable[[], int] = lambda: 0
	) -> None:
		self.liv = True
		self.ptr = 0
		self.reb = 0
		self.mem = defaultdict(int, enumerate(prg))
		self.cal = cal
		self.log = list()
	def get(self, mde: Mde) -> int:
		if   mde == Mde.POS: idx = self.mem[self.ptr]
		elif mde == Mde.IMM: idx = self.ptr
		elif mde == Mde.REL: idx = self.mem[self.ptr] + self.reb
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
	def adj(self, idx: int) -> None:
		self.reb += self.mem[idx]
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
		 9: adj,
		99: hal
	}

from typing import Tuple
class ArcadeCabinet:
	ico: Ico
	index: int
	screen: Dict[Tuple[int, int], int]
	def __init__(self, program: Iterable[int]) -> None:
		self.ico = Ico(program)
		self.ico.cal = self
		self.index = 0
		self.screen = defaultdict(int)
	def __call__(self) -> int:
		return 0
	def consume_log(self):
		while self.index < len(self.ico.log):
			j, i, tile = self.ico.log[self.index: self.index + 3]
			self.screen[i, j] = tile
			self.index += 3

demo = ArcadeCabinet(program)
demo.ico.run()
demo.consume_log()
print(sum(1 for tile in demo.screen.values() if tile == 2))
