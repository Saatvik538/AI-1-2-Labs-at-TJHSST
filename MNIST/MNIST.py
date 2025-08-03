#saatvik kesarwani, pd 1, 2026
import sys; args = sys.argv[1:]
import time, math, random
train_images_fp, train_labels_fp, test_images_fp, test_labels_fp = args[:4]

#IDX file loaders
def load_idx_images(path):
    with open(path, 'rb') as f: #rb is binary read mode
        #read the first 4 bytes to get the magic number
        #converts those bytes to an integer
        m = int.from_bytes(f.read(4))
        #next 4 bytes: how many images are in the file
        size = int.from_bytes(f.read(4))
        #next 4 bytes: number of rows per image (should be 28 for MNIST)
        rows = int.from_bytes(f.read(4))
        #next 4 bytes: number of columns per image (should be 28 for MNIST)
        cols = int.from_bytes(f.read(4))
        #this returns a single bytes object of length rows*cols*size
        buf = f.read(rows * cols * size)

    #store our normalized images here
    imgs = []

    for i in range(size):
        #calculate the start position in the buffer for image i
        start = i * rows * cols
        #slice out exactly rows*cols bytes for this image
        chunk = buf[start : start + rows * cols]

        #'chunk' is a bytes like sequence of pixel values 0–255.
        #the result is a list of floats of length rows*cols.
        imgs.append([b / 255.0 for b in chunk])

    #return the list of all images as flat float lists
    return imgs

def load_idx_labels(path):
    with open(path, 'rb') as f:
        magic = int.from_bytes(f.read(4))
        size = int.from_bytes(f.read(4))
        buf  = f.read(size)
    return [b for b in buf]

print("Loading MNIST data:")
train_images = load_idx_images(train_images_fp)
train_labels = load_idx_labels(train_labels_fp)
test_images = load_idx_images(test_images_fp)
test_labels = load_idx_labels(test_labels_fp)
print(f"-> {len(train_images)} train samples, {len(test_images)} test samples")

#one hot encoder makes all qualitative lables into numbers
def to_one_hot(lbl, classes=10):
    v = [0.0]*classes
    v[lbl] = 1.0
    return v #makes a list of 0.0's with a 1.0 at the index of the label

#assemble into (input, label_vector) pairs
train_data = list(zip(train_images, [to_one_hot(l) for l in train_labels]))
test_data  = list(zip(test_images,  [to_one_hot(l) for l in test_labels ]))

#network architecture  and hyperparams
#input_size = pixels + bias
input_size = len(train_images[0]) + 1 #784 + 1
h1,h2,h3,o = 128,64,10,10 #h3 == o required by no dot‐product last layer
layer_counts = [input_size, h1, h2, h3, o]
initial_alpha = 0.1
max_epochs = 10 #only one epoch needed for this task
random.seed(0)
#weight matrices
W1 = [[random.uniform(-0.5,0.5) for _ in range(input_size)] for _ in range(h1)]
W2 = [[random.uniform(-0.5,0.5) for _ in range(h1)] for _ in range(h2)]
W3 = [[random.uniform(-0.5,0.5) for _ in range(h2)] for _ in range(h3)]
W4 = [[random.uniform(-0.5,0.5)] for _ in range(o)] #one weight per output unit

def dot_product(a,b): return sum(x*y for x,y in zip(a,b))
def logistic(z):
    try: return 1.0/(1.0+math.exp(-z))
    except OverflowError: return 0.0 if z<0 else 1.0
def logistic_derivative(a): return a*(1.0-a)

#forward, backprop, train & test functions
def forward_pass(x):
    xa = x + [1.0]  #append bias
    z1 = [dot_product(W1[i], xa)  for i in range(h1)];  a1 = [logistic(z) for z in z1]
    z2 = [dot_product(W2[i], a1) for i in range(h2)];  a2 = [logistic(z) for z in z2]
    z3 = [dot_product(W3[i], a2) for i in range(h3)];  a3 = [logistic(z) for z in z3]
    #last layer: elementwise multiply
    out = [W4[i][0] * a3[i] for i in range(o)]
    return xa, a1, a2, a3, out

#full test accuracy on entire test set
def test_accuracy(dataset):
    correct = 0
    total = len(dataset)
    for x,y_true in dataset:
        _, _, _, _, out = forward_pass(x)
        pred = out.index(max(out))
        truec = y_true.index(1.0)
        if pred == truec:
            correct += 1
    return correct / total

data = train_data  #for backprop

def train_epoch(alpha):
    global W1,W2,W3,W4
    total_err = 0.0
    test_counts=[]
    test_accs=[]
    seen=0
    for x, y_true in data:
        xa,a1,a2,a3,out = forward_pass(x)
        #backprop deltas
        delta4 = [(y_true[i] - out[i]) for i in range(o)]
        delta3 = [W4[k][0]*delta4[k]*logistic_derivative(a3[k]) for k in range(h3)]
        delta2 = [sum(W3[k][j]*delta3[k] for k in range(h3))*logistic_derivative(a2[j]) for j in range(h2)]
        delta1 = [sum(W2[k][i]*delta2[k] for k in range(h2))*logistic_derivative(a1[i]) for i in range(h1)]
        #update
        for i in range(h1):
            for j in range(input_size):
                W1[i][j] += alpha * delta1[i] * xa[j]
        for i in range(h2):
            for j in range(h1):
                W2[i][j] += alpha * delta2[i] * a1[j]
        for i in range(h3):
            for j in range(h2):
                W3[i][j] += alpha * delta3[i] * a2[j]
        for i in range(o):
            W4[i][0] += alpha * delta4[i] * a3[i]
        #accumulate mean squared error
        total_err += sum(0.5 * (out[i]-y_true[i])**2 for i in range(o))
        seen+=1
        if seen%5000==0:
            acc=test_accuracy(test_data)
            test_counts.append(seen)
            test_accs.append(acc*100.0)
    return total_err/len(data),test_counts,test_accs

#training loop
start = time.time()
alpha = initial_alpha
best_err = float('inf')
best_W = None

print(f"training on {len(data)} samples, architecture {layer_counts}")
for epoch in range(1, max_epochs+1):
    epoch_start = time.time()
    err,counts,accs = train_epoch(alpha)
    epoch_time = time.time() - epoch_start
    print(f"Epoch {epoch} took {epoch_time:.2f} seconds")
    alpha = initial_alpha * math.sqrt(err)

    #after epoch check 90% test accuracy
    final_acc=test_accuracy(test_data)
    print(f"Test accuracy after epoch {epoch}: {final_acc*100:.2f}%")
    if final_acc>=0.90:
        print("reached >=90% test accuracy so stopping early")
        break
total_time = time.time() - start
print(f"Total training time: {total_time:.2f} seconds")
#plotting accuracy vs train count
#STORING VALUES to graph on sheets
with open('accuracy_vs_traincount.txt', 'w') as f:
    f.write('train_count\taccuracy_percent\n')  #tab separated header
    for count, acc in zip(counts, accs):
        f.write(f"{count}\t{acc}\n")  #tab separated values
print("saved test accuracy vs train count to accuracy_vs_traincount.txt")

#save final weights to file and report size
with open('final_weights.txt','w') as f:
    for M in (W1,W2,W3,W4):
        for row in M:
            f.write(" ".join(str(w) for w in row)+"\n")
with open('final_weights.txt','rb') as f:
    f.seek(0,2) #.seek to end of file
    #.tell() returns the current position in the file
    size_bytes=f.tell() #get size in bytes
    size_kb=size_bytes/1024 #convert to KB
print(f"final weights file size: {size_kb:.2f} KB")

wc1 = sum(len(row) for row in W1)   #h1 * input_size
wc2 = sum(len(row) for row in W2)   #h2 * h1
wc3 = sum(len(row) for row in W3)   #h3 * h2
wc4 = sum(len(row) for row in W4)   #o  * 1
print("Weight counts per layer:", wc1, wc2, wc3, wc4)

#saatvik kesarwani, pd 1, 2026