import sys; args = sys.argv[1:]
import time
import math
import random

def dot_product(a, b):
    return sum(x*y for x, y in zip(a, b))

def logistic(x):
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def logistic_derivative(y):
    return y * (1.0 - y)
data = []
with open(args[0]) as f:
    for line in f:
        line = line.strip()
        if not line or '=>' not in line:
            continue
        left, right = line.split('=>')
        x = [float(v) for v in left.split()]
        y = [float(v) for v in right.split()]
        data.append((x, y))

n_inputs = len(data[0][0])
n_outputs = len(data[0][1])

input_size = n_inputs + 1
h1 = 4 if n_outputs == 2 else 2
h2 = n_outputs
o = n_outputs

alpha = 1.5
max_epochs = 10000
err_thresh = 0.1

random.seed(0)
w1 = [[random.uniform(-1, 1) for _ in range(input_size)] for _ in range(h1)]
w2 = [[random.uniform(-1, 1) for _ in range(h1)] for _ in range(h2)]
w3 = [[random.uniform(-1, 1)] for _ in range(o)]

def train():
    global w1, w2, w3
    for epoch in range(max_epochs):
        for x, y_true in data:
            xa = x + [1.0]
            z1 = [dot_product(w1[i], xa) for i in range(h1)]
            a1 = [logistic(z) for z in z1]
            z2 = [dot_product(w2[i], a1) for i in range(h2)]
            a2 = [logistic(z) for z in z2]
            out = [w3[i][0] * a2[i] for i in range(o)]

            delta3 = [(y_true[i] - out[i]) for i in range(o)]
            delta2 = [
                w3[k][0] * delta3[k] * logistic_derivative(a2[k]) for k in range(o)
            ]
            delta1 = [
                (sum(w2[k][i] * delta2[k] for k in range(h2))) * logistic_derivative(a1[i])
                for i in range(h1)
            ]

            for i in range(h1):
                for j in range(input_size):
                    w1[i][j] += alpha * delta1[i] * xa[j]
            for i in range(h2):
                for j in range(h1):
                    w2[i][j] += alpha * delta2[i] * a1[j]
            for i in range(o):
                w3[i][0] += alpha * delta3[i] * a2[i]

def calculate_total_error():
    total_error = 0.0
    for x, y_true in data:
        xa = x + [1.0]
        z1 = [dot_product(w1[i], xa) for i in range(h1)]
        a1 = [logistic(z) for z in z1]
        z2 = [dot_product(w2[i], a1) for i in range(h2)]
        a2 = [logistic(z) for z in z2]
        out = [w3[i][0] * a2[i] for i in range(o)]
        total_error += sum(0.5 * (out[i] - y_true[i])**2 for i in range(o))
    return total_error

while True:
    train()
    err = calculate_total_error()
    if err < err_thresh:
        break
    w1 = [[random.uniform(-1, 1) for _ in range(input_size)] for _ in range(h1)]
    w2 = [[random.uniform(-1, 1) for _ in range(h1)] for _ in range(h2)]
    w3 = [[random.uniform(-1, 1)] for _ in range(o)]

layers = [input_size, h1, h2, o]
print(f"Layer counts: {layers[0]} {layers[1]} {layers[2]} {layers[3]}")
for m in (w1, w2, w3):
    print(" ".join(str(w) for row in m for w in row))