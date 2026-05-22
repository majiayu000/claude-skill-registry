---
name: tensorflow-data-pipelines
description: Create efficient data pipelines with tf.data
allowed-tools: [Bash, Read]
---

# TensorFlow Data Pipelines

Build efficient, scalable data pipelines using the tf.data API for optimal training performance. This skill covers dataset creation, transformations, batching, shuffling, prefetching, and advanced optimization techniques to maximize GPU/TPU utilization.

## Dataset Creation

### From Tensor Slices

```python
import tensorflow as tf
import numpy as np

# Create dataset from numpy arrays
x_train = np.random.rand(1000, 28, 28, 1)
y_train = np.random.randint(0, 10, 1000)

# Method 1: from_tensor_slices
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))

# Apply transformations
dataset = dataset.shuffle(buffer_size=1024)
dataset = dataset.batch(32)
dataset = dataset.prefetch(tf.data.AUTOTUNE)

# Iterate through dataset
for batch_x, batch_y in dataset.take(2):
    print(f"Batch shape: {batch_x.shape}, Labels shape: {batch_y.shape}")
```

### From Generator Functions

```python
def data_generator():
    """Generator function for custom data loading."""
    for i in range(1000):
        # Simulate loading data from disk or API
        x = np.random.rand(28, 28, 1).astype(np.float32)
        y = np.random.randint(0, 10)
        yield x, y

# Create dataset from generator
dataset = tf.data.Dataset.from_generator(
    data_generator,
    output_signature=(
        tf.TensorSpec(shape=(28, 28, 1), dtype=tf.float32),
        tf.TensorSpec(shape=(), dtype=tf.int32)
    )
)

dataset = dataset.batch(32).prefetch(tf.data.AUTOTUNE)
```

### From Dataset Range

```python
# Create simple range dataset
dataset = tf.data.Dataset.range(1000)

# Use with custom mapping
dataset = dataset.map(lambda x: (tf.random.normal([28, 28, 1]), x % 10))
dataset = dataset.batch(32)
```

## Data Transformation

### Normalization Pipeline

```python
def normalize(image, label):
    """Normalize pixel values."""
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

# Apply normalization
train_dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .map(normalize, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

### Data Augmentation Pipeline

```python
def augment(image, label):
    """Apply random augmentations."""
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, 0.2)
    image = tf.image.random_contrast(image, 0.8, 1.2)
    return image, label

def normalize(image, label):
    """Normalize pixel values."""
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

# Build complete pipeline
train_dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .map(normalize, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()  # Cache after normalization
    .shuffle(1000)
    .map(augment, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

### Multiple Transformations

```python
def resize_image(image, label):
    """Resize images to target size."""
    image = tf.image.resize(image, [224, 224])
    return image, label

def apply_random_rotation(image, label):
    """Apply random rotation augmentation."""
    angle = tf.random.uniform([], -0.2, 0.2)
    image = tfa.image.rotate(image, angle)
    return image, label

# Chain multiple transformations
dataset = (
    tf.data.Dataset.from_tensor_slices((images, labels))
    .map(resize_image, num_parallel_calls=tf.data.AUTOTUNE)
    .map(normalize, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()
    .shuffle(10000)
    .map(augment, num_parallel_calls=tf.data.AUTOTUNE)
    .map(apply_random_rotation, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(64)
    .prefetch(tf.data.AUTOTUNE)
)
```

## Batching and Shuffling

### Basic Batching Configuration

```python
# Batch size
BATCH_SIZE = 64

# Buffer size to shuffle the dataset
# (TF data is designed to work with possibly infinite sequences,
# so it doesn't attempt to shuffle the entire sequence in memory. Instead,
# it maintains a buffer in which it shuffles elements).
BUFFER_SIZE = 10000

dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
```

### Dynamic Batching

```python
# Variable batch sizes based on sequence length
def batch_by_sequence_length(dataset, batch_size, max_length):
    """Batch sequences by length for efficient padding."""
    def key_func(x, y):
        # Bucket by length
        return tf.cast(tf.size(x) / max_length * 10, tf.int64)

    def reduce_func(key, dataset):
        return dataset.batch(batch_size)

    return dataset.group_by_window(
        key_func=key_func,
        reduce_func=reduce_func,
        window_size=batch_size
    )
```

### Stratified Sampling

```python
def create_stratified_dataset(features, labels, batch_size):
    """Create dataset with balanced class sampling."""
    # Separate by class
    datasets = []
    for class_id in range(num_classes):
        mask = labels == class_id
        class_dataset = tf.data.Dataset.from_tensor_slices(
            (features[mask], labels[mask])
        )
        datasets.append(class_dataset)

    # Sample equally from each class
    balanced_dataset = tf.data.Dataset.sample_from_datasets(
        datasets,
        weights=[1.0/num_classes] * num_classes
    )

    return balanced_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
```

## Performance Optimization

### Caching Strategies

```python
# Cache in memory (for small datasets)
dataset = dataset.cache()

# Cache to disk (for larger datasets)
dataset = dataset.cache('/tmp/dataset_cache')

# Optimal caching placement
dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .map(expensive_preprocessing, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()  # Cache after expensive operations
    .shuffle(buffer_size)
    .map(cheap_augmentation, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(batch_size)
    .prefetch(tf.data.AUTOTUNE)
)
```

### Prefetching

```python
# Automatic prefetching
dataset = dataset.prefetch(tf.data.AUTOTUNE)

# Manual prefetch buffer size
dataset = dataset.prefetch(buffer_size=2)

# Complete optimized pipeline
optimized_dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()
    .shuffle(10000)
    .batch(64)
    .prefetch(tf.data.AUTOTUNE)
)
```

### Parallel Data Loading

```python
# Use num_parallel_calls for CPU-bound operations
dataset = dataset.map(
    preprocessing_function,
    num_parallel_calls=tf.data.AUTOTUNE
)

# Interleave for parallel file reading
def make_dataset_from_file(filename):
    return tf.data.TextLineDataset(filename)

filenames = tf.data.Dataset.list_files('/path/to/data/*.csv')
dataset = filenames.interleave(
    make_dataset_from_file,
    cycle_length=4,
    num_parallel_calls=tf.data.AUTOTUNE
)
```

### Memory Management

```python
# Use take() and skip() for train/val split without loading all data
total_size = 10000
train_size = int(0.8 * total_size)

full_dataset = tf.data.Dataset.from_tensor_slices((x, y))

train_dataset = (
    full_dataset
    .take(train_size)
    .shuffle(1000)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)

val_dataset = (
    full_dataset
    .skip(train_size)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

## Advanced Patterns

### Iterating with For Loops

```python
# Basic iteration
for i in tf.data.Dataset.range(3):
    tf.print('iteration:', i)

# With dataset iterator
for i in iter(tf.data.Dataset.range(3)):
    tf.print('iteration:', i)
```

### Distributed Dataset

```python
# Distribute dataset across devices
for i in tf.distribute.OneDeviceStrategy('cpu').experimental_distribute_dataset(
    tf.data.Dataset.range(3)):
    tf.print('iteration:', i)

# Multi-GPU distribution
strategy = tf.distribute.MirroredStrategy()
distributed_dataset = strategy.experimental_distribute_dataset(dataset)
```

### Training Loop Integration

```python
# Execute training loop over dataset
for images, labels in train_ds:
    if optimizer.iterations > TRAIN_STEPS:
        break
    train_step(images, labels)
```

### Vectorized Operations

```python
def f(args):
    embeddings, index = args
    # embeddings [vocab_size, embedding_dim]
    # index []
    # desired result: [embedding_dim]
    return tf.gather(params=embeddings, indices=index)

@tf.function
def f_auto_vectorized(embeddings, indices):
    # embeddings [num_heads, vocab_size, embedding_dim]
    # indices [num_heads]
    # desired result: [num_heads, embedding_dim]
    return tf.vectorized_map(f, [embeddings, indices])

concrete_vectorized = f_auto_vectorized.get_concrete_function(
    tf.TensorSpec(shape=[None, 100, 16], dtype=tf.float32),
    tf.TensorSpec(shape=[None], dtype=tf.int32))
```

## Model Integration

### Training with tf.data

```python
# Use dataset with model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.fit(train_dataset, epochs=1)
```

### Validation Dataset

```python
# Create separate train and validation datasets
train_dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .shuffle(10000)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)

val_dataset = (
    tf.data.Dataset.from_tensor_slices((x_val, y_val))
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)

# Train with validation
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10
)
```

### Custom Training Loop

```python
@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_fn(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

# Training loop with dataset
for epoch in range(epochs):
    for images, labels in train_dataset:
        loss = train_step(images, labels)
    print(f'Epoch {epoch}, Loss: {loss.numpy():.4f}')
```

## File-Based Datasets

### TFRecord Files

```python
# Reading TFRecord files
def parse_tfrecord(example_proto):
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    parsed = tf.io.parse_single_example(example_proto, feature_description)
    image = tf.io.decode_raw(parsed['image'], tf.float32)
    image = tf.reshape(image, [28, 28, 1])
    label = parsed['label']
    return image, label

# Load TFRecord dataset
tfrecord_dataset = (
    tf.data.TFRecordDataset(['data_shard_1.tfrecord', 'data_shard_2.tfrecord'])
    .map(parse_tfrecord, num_parallel_calls=tf.data.AUTOTUNE)
    .shuffle(10000)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

### CSV Files

```python
# Load CSV dataset
def parse_csv(line):
    columns = tf.io.decode_csv(line, record_defaults=[0.0] * 785)
    label = tf.cast(columns[0], tf.int32)
    features = tf.stack(columns[1:])
    features = tf.reshape(features, [28, 28, 1])
    return features, label

csv_dataset = (
    tf.data.TextLineDataset(['data.csv'])
    .skip(1)  # Skip header
    .map(parse_csv, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

### Image Files

```python
def load_and_preprocess_image(path, label):
    """Load image from file and preprocess."""
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

# Create dataset from image paths
image_paths = ['/path/to/image1.jpg', '/path/to/image2.jpg', ...]
labels = [0, 1, ...]

image_dataset = (
    tf.data.Dataset.from_tensor_slices((image_paths, labels))
    .map(load_and_preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
    .cache()
    .shuffle(1000)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

## Data Validation

### DataLoader Generation

```python
# Generate TensorFlow dataset with batching
def gen_dataset(
    batch_size=1,
    is_training=False,
    shuffle=False,
    input_pipeline_context=None,
    preprocess=None,
    drop_remainder=True,
    total_steps=None
):
    """Generate dataset with specified configuration."""
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))

    if shuffle:
        dataset = dataset.shuffle(buffer_size=10000)

    if preprocess:
        dataset = dataset.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)

    dataset = dataset.batch(batch_size, drop_remainder=drop_remainder)

    if is_training:
        dataset = dataset.repeat()

    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    if total_steps:
        dataset = dataset.take(total_steps)

    return dataset
```

## When to Use This Skill

Use the tensorflow-data-pipelines skill when you need to:

- Load and preprocess large datasets that don't fit in memory
- Implement data augmentation for training robustness
- Optimize data loading to prevent GPU/TPU idle time
- Create custom data generators for specialized formats
- Build multi-modal pipelines with images, text, and audio
- Implement efficient batching strategies for variable-length sequences
- Cache preprocessed data to speed up training
- Handle distributed training across multiple devices
- Parse TFRecord, CSV, or other file formats
- Implement stratified sampling for imbalanced datasets
- Create reproducible data shuffling
- Build real-time data augmentation pipelines
- Optimize memory usage with streaming datasets
- Implement prefetching for pipeline parallelism
- Create validation and test splits efficiently

## Best Practices

1. **Always use prefetch()** - Add .prefetch(tf.data.AUTOTUNE) at the end of pipeline to overlap data loading with training
2. **Use num_parallel_calls=AUTOTUNE** - Let TensorFlow automatically tune parallelism for map operations
3. **Cache after expensive operations** - Place .cache() after preprocessing but before augmentation and shuffling
4. **Shuffle before batching** - Call .shuffle() before .batch() to ensure random batches
5. **Use appropriate buffer sizes** - Shuffle buffer should be >= dataset size for perfect shuffling, or at least several thousand
6. **Normalize data in pipeline** - Apply normalization in map() function for consistency across train/val/test
7. **Batch after transformations** - Apply .batch() after all element-wise transformations for efficiency
8. **Use drop_remainder for training** - Set drop_remainder=True in batch() to ensure consistent batch sizes
9. **Leverage AUTOTUNE** - Use tf.data.AUTOTUNE for automatic performance tuning instead of manual values
10. **Apply augmentation after caching** - Cache deterministic preprocessing, apply random augmentation after
11. **Use interleave for file reading** - Parallel file reading with interleave() for large multi-file datasets
12. **Repeat for infinite datasets** - Use .repeat() for training datasets to avoid dataset exhaustion
13. **Use take/skip for splits** - Efficiently split datasets without loading all data into memory
14. **Monitor pipeline performance** - Use TensorFlow Profiler to identify bottlenecks in data pipeline
15. **Shard data for distribution** - Use shard() for distributed training across multiple workers

## Common Pitfalls

1. **Shuffling after batching** - Shuffles batches instead of individual samples, reducing randomness
2. **Not using prefetch** - GPU sits idle waiting for data, wasting compute resources
3. **Cache in wrong position** - Caching after augmentation prevents randomness, before preprocessing wastes memory
4. **Buffer size too small** - Insufficient shuffle buffer leads to poor randomization and training issues
5. **Not using num_parallel_calls** - Sequential map operations create bottlenecks in data loading
6. **Loading entire dataset to memory** - Use tf.data instead of loading all data with NumPy
7. **Applying augmentation deterministically** - Same augmentations every epoch reduce training effectiveness
8. **Not setting random seeds** - Irreproducible results and debugging difficulties
9. **Ignoring batch remainder** - Variable batch sizes cause errors in models expecting fixed dimensions
10. **Repeating validation dataset** - Validation should not repeat, only training datasets
11. **Not using AUTOTUNE** - Manual tuning is difficult and suboptimal compared to automatic optimization
12. **Caching very large datasets** - Exceeds memory limits and causes OOM errors
13. **Too many parallel operations** - Excessive parallelism causes thread contention and slowdown
14. **Not monitoring data loading time** - Data pipeline can become training bottleneck without monitoring
15. **Applying normalization inconsistently** - Different normalization for train/val/test causes poor performance

## Resources

- [tf.data API Guide](https://www.tensorflow.org/guide/data)
- [Data Pipeline Performance](https://www.tensorflow.org/guide/data_performance)
- [TFRecord Format](https://www.tensorflow.org/tutorials/load_data/tfrecord)
- [Image Data Loading](https://www.tensorflow.org/tutorials/load_data/images)
- [CSV Data Loading](https://www.tensorflow.org/tutorials/load_data/csv)
- [Data Augmentation Guide](https://www.tensorflow.org/tutorials/images/data_augmentation)
- [Preprocessing Layers](https://www.tensorflow.org/guide/keras/preprocessing_layers)
- [Building Input Pipelines](https://www.tensorflow.org/api_docs/python/tf/data/Dataset)
