import sys; args = sys.argv[1:]
import math

def transfer_t1(x):
    return x

def transfer_t2(x):
    return x if x > 0 else 0

def transfer_t3(x):
    return 1/(1+math.exp(-x))

def transfer_t4(x):
    return 2/(1+math.exp(-x)) - 1

tf_spec = args[1]
if tf_spec == "T1":
    transfer = transfer_t1
elif tf_spec == "T2":
    transfer = transfer_t2
elif tf_spec == "T3":
    transfer = transfer_t3
elif tf_spec == "T4":
    transfer = transfer_t4

with open(args[0]) as f:
    lines = [line.strip() for line in f if line.strip()]
weights_layers = [list(map(float, line.split())) for line in lines]

input_layer = list(map(float, args[2:]))

def dot_product(lst1, lst2):
    return sum(a * b for a, b in zip(lst1, lst2))

#process the network according to the number of weight layers
if len(weights_layers) == 1:
    weights = weights_layers[0]
    num_inputs = len(input_layer)
    if len(weights) == num_inputs:
        outputs = [input_layer[i] * weights[i] for i in range(num_inputs)]
    else:
        num_outputs = len(weights) // num_inputs
        outputs = []
        for j in range(num_outputs):
            chunk = weights[j*num_inputs:(j+1)*num_inputs]
            outputs.append(transfer(dot_product(input_layer, chunk)))
else:
    output_weights = weights_layers[-1]
    current_layer = input_layer
    for layer in weights_layers[:-1]:
        num_inputs = len(current_layer)
        next_layer = []
        for j in range(0, len(layer), num_inputs):
            chunk = layer[j:j+num_inputs]
            next_layer.append(transfer(dot_product(current_layer, chunk)))
        current_layer = next_layer
    if len(output_weights) == len(current_layer):
        outputs = [current_layer[i] * output_weights[i] for i in range(len(current_layer))]
    else:
        num_inputs = len(current_layer)
        num_outputs = len(output_weights) // num_inputs
        outputs = []
        for j in range(num_outputs):
            chunk = output_weights[j*num_inputs:(j+1)*num_inputs]
            outputs.append(transfer(dot_product(current_layer, chunk)))

print(" ".join(map(str, outputs)))
