#Saatvik Kesarwani, pd 1, 2026
import os
import tensorflow as tf
import time
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.losses import CategoricalCrossentropy

def load_idx_images(path):
#loads idx images into a list of length n images each flattened to 784 floats normalizes pixels to 01
    with open(path,'rb') as f:
        m=int.from_bytes(f.read(4))
        size=int.from_bytes(f.read(4))
        rows=int.from_bytes(f.read(4))
        cols=int.from_bytes(f.read(4))
        buf=f.read(rows*cols*size)
    imgs=[]
    for i in range(size):
        start=i*rows*cols
        chunk=buf[start:start+rows*cols]
        imgs.append([b/255.0 for b in chunk])
    return imgs

def load_idx_labels(path):
#loads idx labels into a list of length n ints
    with open(path,'rb') as f:
        m=int.from_bytes(f.read(4))
        size=int.from_bytes(f.read(4))
        buf=f.read(size)
    return [b for b in buf]

def to_one_hot(lbl,classes=10):
#converts integer label to a onehot list of length classes
    v=[0.0]*classes
    v[lbl]=1.0
    return v
train_images_fp = 'train-images.idx3-ubyte'
train_labels_fp = 'train-labels.idx1-ubyte'
test_images_fp  = 't10k-images.idx3-ubyte'
test_labels_fp  = 't10k-labels.idx1-ubyte'

print("loading mnist data")
train_images=load_idx_images(train_images_fp)
train_labels=load_idx_labels(train_labels_fp)
test_images=load_idx_images(test_images_fp)
test_labels=load_idx_labels(test_labels_fp)
print("->",len(train_images),"train samples",len(test_images),"test samples")
overall_start = time.time()
epoch_times = []   # will hold how many seconds each epoch took
test_acc_list = []   # will hold test accuracy after each epoch
#prepare data as Python lists for keras
x_train = np.array(train_images, dtype='float32')  # shape (60000, 784)
x_test  = np.array(test_images,  dtype='float32')  # shape (10000, 784)
y_train = np.array([to_one_hot(l) for l in train_labels], dtype='float32')
y_test  = np.array([to_one_hot(l) for l in test_labels],  dtype='float32')

input_dim=28*28
hidden_1=128
hidden_2=64
hidden_3=10
output_dim=10
learning_rate=0.1
#W4 = tf.Variable(initial_value=tf.random.uniform([output_dim], -0.5, 0.5), trainable=True, name='w4')
#layers.Lambda(lambda x: x * W4, name='dense_out')
model=keras.Sequential([layers.Input(shape=(input_dim,)),layers.Dense(hidden_1,activation='sigmoid',name='dense_h1'),layers.Dense(hidden_2,activation='sigmoid',name='dense_h2'),layers.Dense(hidden_3,activation='sigmoid',name='dense_h3'),layers.Dense(output_dim,activation=None,name='dense_out')])#sequential stacks layers in order

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate),loss=CategoricalCrossentropy(from_logits=True),metrics=['accuracy']) #compile configures model for training with sgd optimizer crossentropy loss and accuracy metric
model.summary() #prints model architecture

batch_size=64
max_epochs=1000
for epoch in range(max_epochs):
    print(f"Epoch {epoch+1}/{max_epochs}")
    t0 = time.time()
    history = model.fit(
        x_train, y_train,
        validation_data=(x_test, y_test),
        batch_size=batch_size,
        epochs=1,
        verbose=2
    )
    epoch_dur = time.time() - t0
    epoch_times.append(epoch_dur)

    # capture validation accuracy (== test accuracy here)
    val_acc = history.history['val_accuracy'][0]
    test_acc_list.append(val_acc)

    if val_acc >= 0.95:
        print(f"\nreached >=95% validation accuracy at epoch {epoch+1} stopping")
        break

#evaluate returns loss and accuracy on test data
test_loss,test_acc=model.evaluate(x_test,y_test,verbose=0)
print("\nfinal test accuracy",test_acc*100,"%")

total_training_time = time.time() - overall_start
print(f"Total training time: {total_training_time:.2f} seconds")

os.makedirs('/content/mnist2_saved',exist_ok=True) #creates directory if not exists

# dump final weights to txt
txt_path='/content/mnist2_saved/final_weights.txt'
with open(txt_path,'w') as f:
    weights=model.get_weights()
    for w_array in weights:
        flat=[]
        for row in w_array.tolist():
            if isinstance(row,list):
                for v in row:
                    flat.append(v)
            else:
                flat.append(row)
        f.write(" ".join(str(float(v)) for v in flat)+"\n")
print("saved final weights to",txt_path)

size_bytes=os.path.getsize(txt_path)
size_kb=size_bytes/1024.0
print("final weights file size:",size_kb,"KB")

# architecture of the nn (layer counts)
print("Architecture of the NN (layer counts):",input_dim,hidden_1,hidden_2,hidden_3,output_dim)

# weight counts per layer
weights=model.get_weights()
weight_counts=[w_array.size for idx,w_array in enumerate(weights) if idx%2==0]
print("Weight counts per layer:",*weight_counts)
with open(txt_path, 'r') as f:
    data = f.read()
    print("last 32 characters of weight file:", data[-32:])
from google.colab import files
files.download(txt_path)
#Saatvik Kesarwani, pd 1, 2026