INPUTPATH, W, H = "input.txt", 25, 6
#INPUTPATH, W, H = "input-test.txt", 2, 2
with open(INPUTPATH) as ifile:
	raw = ifile.read()
pixels = tuple(map(int, raw.strip()))

layers = tuple(pixels[i: i + W * H] for i in range(0, len(pixels), W * H))
fewest_zeros = min(layers, key = lambda layer: layer.count(0))
print(fewest_zeros.count(1) * fewest_zeros.count(2))

flat = tuple(next(filter(lambda p: p != 2, stack)) for stack in zip(*layers))
image = tuple(
	"".join(map(lambda p: " " if p == 0 else "#", flat[i: i + W]))
	for i in range(0, len(flat), W)
)
print("\n".join(image))
