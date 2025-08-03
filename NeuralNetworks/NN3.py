import sys; args = sys.argv[1:]
import time, math, random, re

ineq = args[0] if args else "x*x+y*y>=1.0"
m = re.match(r'(x\*x\+y\*y)\s*([<>]=?)\s*([\d.]+)', ineq)
op = m.group(2)
r2 = float(m.group(3))

def label(x, y):
    d2 = x*x + y*y
    if   op == '<':  return 1.0 if d2 <  r2 else 0.0
    elif op == '<=': return 1.0 if d2 <= r2 else 0.0
    elif op == '>':  return 1.0 if d2 >  r2 else 0.0
    else:            return 1.0 if d2 >= r2 else 0.0

data = []
for _ in range(2000):
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    data.append(([x, y], [label(x, y)]))

layer_counts = [3, 8, 5, 1, 1]

input_size, h1, h2, h3, o = layer_counts

initial_alpha = 0.1
max_epochs    = 1000
time_limit    = 99

random.seed(0)

w1 = [[random.uniform(-0.5, 0.5) for _ in range(input_size)] for _ in range(h1)]
w2 = [[random.uniform(-0.5, 0.5) for _ in range(h1)]         for _ in range(h2)]
w3 = [[random.uniform(-0.5, 0.5) for _ in range(h2)]         for _ in range(h3)]
w4 = [[random.uniform(-0.5, 0.5)] for _ in range(o)]

def dot_product(a, b):
    return sum(x*y for x, y in zip(a, b))

def logistic(z):
    try:
        return 1.0 / (1.0 + math.exp(-z))
    except OverflowError:
        return 0.0 if z < 0 else 1.0

def logistic_derivative(a):
    return a * (1.0 - a)

def forward_pass(x):
    xa = x + [1.0]
    z1 = [dot_product(w1[i], xa) for i in range(h1)]
    a1 = [logistic(z) for z in z1]
    z2 = [dot_product(w2[i], a1) for i in range(h2)]
    a2 = [logistic(z) for z in z2]
    z3 = [dot_product(w3[i], a2) for i in range(h3)]
    a3 = [logistic(z) for z in z3]
    out = [w4[i][0] * a3[i] for i in range(o)]
    return xa, a1, a2, a3, out

def train_epoch(alpha):
    global w1, w2, w3, w4
    total_err = 0.0
    for x, y_true in data:
        xa, a1, a2, a3, out = forward_pass(x)
        delta4 = [(y_true[i] - out[i]) for i in range(o)]
        delta3 = [ w4[k][0] * delta4[k] * logistic_derivative(a3[k])
                   for k in range(h3) ]
        delta2 = [ (sum(w3[k][j] * delta3[k] for k in range(h3)))
                   * logistic_derivative(a2[j])
                   for j in range(h2) ]
        delta1 = [ (sum(w2[k][i] * delta2[k] for k in range(h2)))
                   * logistic_derivative(a1[i])
                   for i in range(h1) ]
        for i in range(h1):
            for j in range(input_size):
                w1[i][j] += alpha * delta1[i] * xa[j]
        for i in range(h2):
            for j in range(h1):
                w2[i][j] += alpha * delta2[i] * a1[j]
        for i in range(h3):
            for j in range(h2):
                w3[i][j] += alpha * delta3[i] * a2[j]
        for i in range(o):
            w4[i][0] += alpha * delta4[i] * a3[i]
        total_err += sum(0.5 * (out[i] - y_true[i])**2 for i in range(o))
    return total_err / len(data)

def test_accuracy(n=100000):
    correct = 0
    for _ in range(n):
        x, y_true = random.choice(data)
        heyyyyyyyyyy, heyyyyyyyyy, heyyyyyyyy, heyyyyy, out = forward_pass(x)
        pred = 1 if out[0] > 0.5 else 0
        if pred == int(y_true[0]):
            correct += 1
    return correct / n

start_time = time.time()
alpha = initial_alpha
best_err = float('inf')
best_w = None

print(f"training on {len(data)} points, inequality: {ineq}")

for epoch in range(1, max_epochs+1):
    avg_err = train_epoch(alpha)
    alpha = initial_alpha * math.sqrt(avg_err)

    if epoch % 100 == 0:
        acc = test_accuracy(10000)
        print(f"epoch {epoch}, err {avg_err:.6f}, acc {acc:.4f}, alpha is {alpha:.6f}")
        if avg_err < best_err:
            best_err = avg_err
            best_w = ( [row[:] for row in w1],
                         [row[:] for row in w2],
                         [row[:] for row in w3],
                         [row[:] for row in w4] )
        if acc >= 0.991:
            print("reached greater than 99.1 accuracy so its stopping early")
            print("layer counts:", *layer_counts)
            for M in (w1, w2, w3, w4):
                print(" ".join(str(w) for row in M for w in row))
            break

    if time.time() - start_time > time_limit:
        print("time limit reached; stopping")
        print("layer counts:", *layer_counts)
        for M in (w1, w2, w3, w4):
            print(" ".join(str(w) for row in M for w in row))
        break

if best_w:
    w1, w2, w3, w4 = best_w

final_acc = test_accuracy()
print(f"final accuracy: {final_acc:.4f}, best error: {best_err:.6f}")

print("layer counts:", *layer_counts)
for M in (w1, w2, w3, w4):
    print(" ".join(str(w) for row in M for w in row))
