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
	score: int
	auto: bool
	tile_to_char: ClassVar[Dict[int, str]] = {
		0: " ",
		1: "|",
		2: "#",
		3: "_",
		4: "o"
	}
	char_to_joystick: ClassVar[Dict[str, int]] = {
		"a": -1,
		"s": 0,
		"d": 1
	}
	def __init__(self, program: Iterable[int], auto: bool = True) -> None:
		self.ico = Ico(program)
		self.ico.cal = self
		self.index = 0
		self.screen = defaultdict(int)
		self.score = 0
		self.auto = auto
	def __call__(self) -> int:
		self.consume_log()
		if self.auto:
			return 0
		else:
			return self.prompt_joystick()
	def __str__(self) -> str:
		indexes, jndexes = zip(*self.screen)
		return "\n".join(
			"".join(
				self.tile_to_char[self.screen[i, j]]
				for j in range(min(jndexes), max(jndexes) + 1)
			)
			for i in range(min(indexes), max(indexes) + 1)
		)
	def run(self) -> None:
		self.ico.run()
		self.consume_log()
	def consume_log(self) -> None:
		while self.index < len(self.ico.log):
			j, i, value = self.ico.log[self.index: self.index + 3]
			if (j, i) == (-1, 0): self.score = value
			else:                 self.screen[i, j] = value
			self.index += 3
	def prompt_joystick(self) -> int:
		print(self)
		msg = f"<{'|'.join(self.char_to_joystick)}>: "
		while (j := self.char_to_joystick.get(input(msg))) is None: pass
		return j

demo = ArcadeCabinet(program)
demo.run()
print(sum(1 for tile in demo.screen.values() if tile == 2))

game = ArcadeCabinet((2,) + program[1:], False)
game.run()
print(game.score)
