import sys; args = sys.argv[1:]
import math
import re

ineq = args[1]

m = re.match(r'(x\*x\+y\*y)\s*([<>]=?)\s*([\d.]+)', ineq)
op = m.group(2)
r2 = float(m.group(3))
r = math.sqrt(r2)

sign = -1.0 if op in ("<", "<=") else 1.0

numeric_layers = []
with open(args[0]) as f:
    for line in f:
        if re.search(r"[A-Za-z]", line):
            continue
        nums = re.findall(r"[+-]?\d*\.\d+|[+-]?\d+\.\d*|[+-]?\d+", line)
        if nums:
            numeric_layers.append([float(x) for x in nums])

orig_layer_counts = [2]
for i, layer in enumerate(numeric_layers):
    prev = orig_layer_counts[-1]
    cnt = len(layer)
    orig_layer_counts.append(cnt // prev)

hidden_counts = orig_layer_counts[1:-1]

comp_layer_counts = [3] + [h*2 for h in hidden_counts] + [1, 1]

comp_numeric_layers = []
LAY = len(numeric_layers)

for i in range(LAY):
    orig = numeric_layers[i]
    rows = orig_layer_counts[i+1]
    cols = orig_layer_counts[i]
    grid = [orig[r*cols:(r+1)*cols] for r in range(rows)]

    if i == 0:
        layer = []
        for w in grid:
            w_in, w_bias = w
            w_in_scaled = sign * w_in / r        
            layer += [w_in_scaled, 0.0, w_bias]
        for w in grid:
            w_in, w_bias = w
            w_in_scaled = sign * w_in / r        
            layer += [0.0, w_in_scaled, w_bias]
        comp_numeric_layers.append(layer)

    elif i < LAY - 1:
        prev_sz = orig_layer_counts[i]
        layer = []
        for w in grid:
            layer += w + [0.0] * prev_sz
        for w in grid:
            layer += [0.0] * prev_sz + w
        comp_numeric_layers.append(layer)

    else:
        layer = [sign * w for w in orig] + [sign * w for w in orig]
        comp_numeric_layers.append(layer)

if op in (">", ">="):
    w_final = (1 + math.e) / (2 * math.e)
else:
    w_final = (1 + math.e) / 2
comp_numeric_layers.append([w_final])

print("layer counts:", *comp_layer_counts)
for layer in comp_numeric_layers:
    print(" ".join(str(w) for w in layer))
