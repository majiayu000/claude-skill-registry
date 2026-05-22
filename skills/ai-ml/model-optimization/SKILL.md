---
name: Model Optimization
description: Comprehensive guide for ML model optimization techniques including quantization, pruning, knowledge distillation, and inference optimization.
---

# Model Optimization

## Overview

Model optimization is the process of improving machine learning models for production deployment by reducing model size, improving inference speed, and maintaining accuracy. This skill covers quantization, pruning, knowledge distillation, model compression, architecture optimization, inference optimization, ONNX optimization, TensorRT integration, and benchmarking tools.

## Prerequisites

- Understanding of PyTorch and deep learning
- Knowledge of model architecture and training
- Familiarity with model deployment concepts
- Understanding of precision (FP32, FP16, INT8)
- Basic knowledge of model serving

## Key Concepts

### Quantization

- **Dynamic Quantization**: Weights quantized on-the-fly during inference
- **Static Quantization**: Pre-quantized weights with calibration data
- **Quantization-Aware Training (QAT)**: Training with quantization awareness
- **Per-Channel Quantization**: Separate quantization per output channel
- **INT8/FP16**: Reduced precision formats for efficiency

### Pruning

- **Structured Pruning**: Remove entire channels/filters
- **Unstructured Pruning**: Remove individual weights based on magnitude
- **Global vs Local Pruning**: Pruning scope across the model
- **Iterative Pruning**: Gradual pruning with fine-tuning

### Knowledge Distillation

- **Teacher-Student**: Large teacher model training smaller student
- **Soft Targets**: Using teacher's softened outputs as targets
- **Feature Distillation**: Matching intermediate representations
- **Self-Distillation**: Model teaching itself (EMA)

### Model Compression

- **Weight Sharing**: K-means clustering for shared weights
- **Low-Rank Factorization**: SVD-based layer decomposition
- **Architecture Design**: Efficient architectures (MobileNet, etc.)

### Inference Optimization

- **Batching**: Processing multiple inputs together
- **Caching**: Repeated computation results
- **GPU Optimization**: cuDNN, half precision, kernel fusion
- **ONNX/TensorRT**: Hardware-specific optimization

## Implementation Guide

### Quantization

#### Post-Training Quantization

**Dynamic Quantization:**

```python
import torch
import torch.nn as nn

# Dynamic quantization - weights quantized, activations computed in float
def apply_dynamic_quantization(model, layers_to_quantize=[nn.Linear, nn.LSTM]):
    """Apply dynamic quantization to model."""
    quantized_model = torch.quantization.quantize_dynamic(
        model,
        layers_to_quantize,
        dtype=torch.qint8
    )
    return quantized_model

# Example
model = MyModel()
quantized_model = apply_dynamic_quantization(model)

# Save quantized model
torch.save(quantized_model.state_dict(), "quantized_model.pth")

# Load and use
quantized_model = MyModel()
quantized_model.load_state_dict(torch.load("quantized_model.pth"))
quantized_model.eval()

# Compare sizes
original_size = get_model_size(model)
quantized_size = get_model_size(quantized_model)
print(f"Original size: {original_size:.2f} MB")
print(f"Quantized size: {quantized_size:.2f} MB")
print(f"Reduction: {(1 - quantized_size/original_size)*100:.1f}%")

def get_model_size(model):
    """Get model size in MB."""
    param_size = 0
    for param in model.parameters():
        param_size += param.nelement() * param.element_size()
    buffer_size = 0
    for buffer in model.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()
    return (param_size + buffer_size) / 1024**2
```

**Static Quantization:**

```python
import torch
from torch.quantization import prepare, convert, get_default_qconfig

def apply_static_quantization(model, calibration_dataloader):
    """Apply static quantization with calibration."""
    model.eval()

    # Set quantization configuration
    model.qconfig = get_default_qconfig('fbgemm')

    # Prepare model for quantization
    prepared_model = prepare(model)

    # Calibrate with representative data
    print("Calibrating model...")
    with torch.no_grad():
        for inputs, _ in calibration_dataloader:
            prepared_model(inputs)

    # Convert to quantized model
    quantized_model = convert(prepared_model)

    return quantized_model

# Usage
model = MyModel()
calibration_loader = get_calibration_loader()
quantized_model = apply_static_quantization(model, calibration_loader)
```

**Per-Channel Quantization:**

```python
def apply_per_channel_quantization(model):
    """Apply per-channel quantization for better accuracy."""
    model.eval()

    # Per-channel quantization configuration
    model.qconfig = torch.quantization.get_default_qconfig('fbgemm')

    # For Conv2d and Linear layers, use per-channel quantization
    for name, module in model.named_modules():
        if isinstance(module, (nn.Conv2d, nn.Linear)):
            module.qconfig = torch.quantization.QConfig(
                activation=torch.quantization.MinMaxObserver.with_args(
                    dtype=torch.qint8
                ),
                weight=torch.quantization.PerChannelMinMaxObserver.with_args(
                    dtype=torch.qint8,
                    qscheme=torch.per_channel_symmetric
                )
            )

    prepared_model = prepare(model)
    # Calibrate...
    quantized_model = convert(prepared_model)

    return quantized_model
```

#### Quantization-Aware Training (QAT)

```python
import torch
import torch.nn as nn
from torch.quantization import prepare_qat, convert, get_default_qat_qconfig

def quantization_aware_training(model, train_loader, val_loader, epochs=10, lr=0.001):
    """Train model with quantization awareness."""
    model.train()

    # Set QAT configuration
    model.qconfig = get_default_qat_qconfig('fbgemm')

    # Prepare model for QAT
    model_prepared = prepare_qat(model, inplace=True)

    # Setup optimizer
    optimizer = torch.optim.Adam(model_prepared.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    # Training loop
    for epoch in range(epochs):
        model_prepared.train()
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model_prepared(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        # Validate
        model_prepared.eval()
        val_loss = 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                outputs = model_prepared(inputs)
                val_loss += criterion(outputs, targets).item()

        print(f"Epoch {epoch}, Val Loss: {val_loss/len(val_loader):.4f}")

    # Convert to quantized model
    model_prepared.eval()
    quantized_model = convert(model_prepared)

    return quantized_model

# Usage
model = MyModel()
quantized_model = quantization_aware_training(model, train_loader, val_loader)
```

#### INT8 and FP16

**INT8 Quantization:**

```python
def int8_quantization(model, calibration_loader):
    """Quantize model to INT8."""
    model.eval()

    # INT8 configuration
    model.qconfig = torch.quantization.QConfig(
        activation=torch.quantization.MinMaxObserver.with_args(
            dtype=torch.qint8
        ),
        weight=torch.quantization.MinMaxObserver.with_args(
            dtype=torch.qint8
        )
    )

    prepared_model = prepare(model)

    # Calibrate
    with torch.no_grad():
        for inputs, _ in calibration_loader:
            prepared_model(inputs)

    quantized_model = convert(prepared_model)
    return quantized_model
```

**FP16 (Half Precision):**

```python
def convert_to_fp16(model):
    """Convert model to FP16."""
    model = model.half()
    return model

# Usage
model = MyModel()
model = convert_to_fp16(model)

# Inference with FP16
model.eval()
with torch.no_grad():
    inputs = inputs.half()  # Convert input to FP16
    outputs = model(inputs)
```

**Mixed Precision Training:**

```python
from torch.cuda.amp import autocast, GradScaler

def mixed_precision_training(model, train_loader, epochs=10, lr=0.001):
    """Train with mixed precision (FP16)."""
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    scaler = GradScaler()

    for epoch in range(epochs):
        for inputs, targets in train_loader:
            optimizer.zero_grad()

            with autocast():
                outputs = model(inputs)
                loss = criterion(outputs, targets)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

    return model
```

### Pruning

#### Structured Pruning

**Channel Pruning:**

```python
import torch.nn.utils.prune as prune

def structured_prune_channels(model, prune_ratio=0.3):
    """Prune entire channels from convolutional layers."""
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            # Prune 30% of output channels
            prune.ln_structured(
                module,
                name='weight',
                amount=prune_ratio,
                n=2,
                dim=0  # Prune along output channel dimension
            )

    return model

# Make pruning permanent
def make_pruning_permanent(model):
    """Remove pruning reparameterization."""
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            prune.remove(module, 'weight')

    return model

# Usage
model = MyModel()
model = structured_prune_channels(model, prune_ratio=0.3)
model = make_pruning_permanent(model)
```

**Filter Pruning:**

```python
def filter_pruning(model, dataloader, prune_ratio=0.3):
    """Prune filters based on L1 norm."""
    # Calculate filter norms
    filter_norms = {}
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            # Calculate L1 norm for each filter
            filter_norm = module.weight.data.abs().sum(dim=(1, 2, 3))
            filter_norms[name] = filter_norm

    # Determine filters to prune
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            filter_norm = filter_norms[name]
            num_filters = filter_norm.size(0)
            num_prune = int(num_filters * prune_ratio)

            # Get indices of filters to prune (lowest norm)
            _, prune_indices = torch.topk(filter_norm, num_prune, largest=False)

            # Create pruning mask
            mask = torch.ones(num_filters)
            mask[prune_indices] = 0

            # Apply pruning
            prune.custom_from_mask(module, name='weight', mask=mask.unsqueeze(1).unsqueeze(2).unsqueeze(3))

    return model
```

#### Unstructured Pruning

**L1 Unstructured Pruning:**

```python
def unstructured_prune(model, prune_ratio=0.2):
    """Apply unstructured L1 pruning."""
    for name, module in model.named_modules():
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            prune.l1_unstructured(
                module,
                name='weight',
                amount=prune_ratio
            )

    return model

# Usage
model = MyModel()
model = unstructured_prune(model, prune_ratio=0.2)
```

**Global Unstructured Pruning:**

```python
def global_unstructured_prune(model, prune_ratio=0.2):
    """Prune globally across all layers."""
    parameters_to_prune = []

    for name, module in model.named_modules():
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            parameters_to_prune.append((module, 'weight'))

    prune.global_unstructured(
        parameters_to_prune,
        pruning_method=prune.L1Unstructured,
        amount=prune_ratio
    )

    return model
```

#### Iterative Pruning

```python
def iterative_pruning(model, train_loader, val_loader,
                     num_iterations=5, prune_ratio=0.2,
                     fine_tune_epochs=5):
    """Iteratively prune and fine-tune model."""
    criterion = nn.CrossEntropyLoss()

    for iteration in range(num_iterations):
        print(f"\nPruning iteration {iteration + 1}/{num_iterations}")

        # Prune
        model = global_unstructured_prune(model, prune_ratio)

        # Fine-tune
        optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
        model.train()

        for epoch in range(fine_tune_epochs):
            for inputs, targets in train_loader:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()

        # Evaluate
        model.eval()
        val_accuracy = evaluate(model, val_loader)
        print(f"Val accuracy after pruning: {val_accuracy:.2f}%")

    # Make pruning permanent
    for name, module in model.named_modules():
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            prune.remove(module, 'weight')

    return model
```

### Knowledge Distillation

#### Basic Knowledge Distillation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DistillationLoss(nn.Module):
    """Knowledge distillation loss."""
    def __init__(self, alpha=0.5, temperature=3.0):
        super().__init__()
        self.alpha = alpha
        self.temperature = temperature
        self.kl_div = nn.KLDivLoss(reduction='batchmean')

    def forward(self, student_logits, teacher_logits, targets):
        # Hard loss (cross-entropy with true labels)
        hard_loss = F.cross_entropy(student_logits, targets)

        # Soft loss (KL divergence with teacher)
        soft_loss = self.kl_div(
            F.log_softmax(student_logits / self.temperature, dim=1),
            F.softmax(teacher_logits / self.temperature, dim=1)
        ) * (self.temperature ** 2)

        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss

def knowledge_distillation(teacher_model, student_model,
                           train_loader, val_loader,
                           epochs=50, lr=0.001,
                           alpha=0.5, temperature=3.0):
    """Train student model with knowledge distillation."""
    teacher_model.eval()
    student_model.train()

    optimizer = torch.optim.Adam(student_model.parameters(), lr=lr)
    criterion = DistillationLoss(alpha=alpha, temperature=temperature)

    for epoch in range(epochs):
        student_model.train()
        total_loss = 0

        for inputs, targets in train_loader:
            optimizer.zero_grad()

            # Get teacher outputs (no gradients)
            with torch.no_grad():
                teacher_outputs = teacher_model(inputs)

            # Get student outputs
            student_outputs = student_model(inputs)

            # Compute distillation loss
            loss = criterion(student_outputs, teacher_outputs, targets)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        # Evaluate
        student_model.eval()
        val_acc = evaluate(student_model, val_loader)

        print(f"Epoch {epoch}, Loss: {total_loss/len(train_loader):.4f}, Val Acc: {val_acc:.2f}%")

    return student_model
```

#### Feature-Based Distillation

```python
class FeatureDistillationLoss(nn.Module):
    """Feature-based distillation loss."""
    def __init__(self, feature_weights=None):
        super().__init__()
        self.feature_weights = feature_weights or [1.0, 1.0, 1.0]
        self.mse_loss = nn.MSELoss()

    def forward(self, student_features, teacher_features):
        """Compute feature distillation loss."""
        total_loss = 0

        for i, (s_feat, t_feat) in enumerate(zip(student_features, teacher_features)):
            weight = self.feature_weights[i] if i < len(self.feature_weights) else 1.0
            total_loss += weight * self.mse_loss(s_feat, t_feat)

        return total_loss

def feature_distillation(teacher_model, student_model,
                         train_loader, val_loader,
                         epochs=50, lr=0.001):
    """Train student with feature distillation."""
    teacher_model.eval()
    student_model.train()

    optimizer = torch.optim.Adam(student_model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    feature_criterion = FeatureDistillationLoss()

    for epoch in range(epochs):
        student_model.train()
        total_loss = 0
        total_cls_loss = 0
        total_feat_loss = 0

        for inputs, targets in train_loader:
            optimizer.zero_grad()

            # Get features and outputs
            with torch.no_grad():
                teacher_features, teacher_outputs = teacher_model.forward_features(inputs)

            student_features, student_outputs = student_model.forward_features(inputs)

            # Compute losses
            cls_loss = criterion(student_outputs, targets)
            feat_loss = feature_criterion(student_features, teacher_features)
            loss = cls_loss + 0.1 * feat_loss

            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_cls_loss += cls_loss.item()
            total_feat_loss += feat_loss.item()

        print(f"Epoch {epoch}, Loss: {total_loss/len(train_loader):.4f}")

    return student_model
```

#### Self-Distillation

```python
def self_distillation(model, train_loader, val_loader,
                   epochs=50, lr=0.001, temperature=3.0):
    """Train model with self-distillation."""
    model.train()

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = DistillationLoss(alpha=0.5, temperature=temperature)

    # Create an EMA copy of model
    ema_model = create_ema_model(model)

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for inputs, targets in train_loader:
            optimizer.zero_grad()

            # Get EMA outputs
            with torch.no_grad():
                ema_outputs = ema_model(inputs)

            # Get current outputs
            current_outputs = model(inputs)

            # Compute distillation loss
            loss = criterion(current_outputs, ema_outputs, targets)

            loss.backward()
            optimizer.step()

            # Update EMA model
            update_ema_model(model, ema_model, decay=0.99)

            total_loss += loss.item()

        print(f"Epoch {epoch}, Loss: {total_loss/len(train_loader):.4f}")

    return model

def create_ema_model(model):
    """Create EMA copy of model."""
    ema_model = type(model)(**model.__dict__)
    ema_model.load_state_dict(model.state_dict())
    ema_model.eval()
    return ema_model

def update_ema_model(model, ema_model, decay=0.99):
    """Update EMA model parameters."""
    with torch.no_grad():
        for ema_param, param in zip(ema_model.parameters(), model.parameters()):
            ema_param.data.mul_(decay).add_(param.data, alpha=1 - decay)
```

### Model Compression

#### Weight Sharing

```python
def apply_weight_sharing(model, num_clusters=16):
    """Apply weight sharing (k-means clustering)."""
    for name, module in model.named_modules():
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            weight = module.weight.data

            # Flatten weight for clustering
            weight_flat = weight.view(-1, 1).numpy()

            # K-means clustering
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
            labels = kmeans.fit_predict(weight_flat)
            centroids = kmeans.cluster_centers_

            # Replace weights with centroids
            weight_shared = torch.tensor(centroids[labels].reshape(weight.shape),
                                        dtype=weight.dtype, device=weight.device)
            module.weight.data = weight_shared

    return model
```

#### Low-Rank Factorization

```python
def low_rank_factorization_conv(conv_layer, rank):
    """Factorize convolutional layer using SVD."""
    # Get weight: (out_channels, in_channels, kH, kW)
    weight = conv_layer.weight.data

    # Reshape to 2D: (out_channels, in_channels * kH * kW)
    weight_2d = weight.view(conv_layer.out_channels, -1)

    # SVD
    U, S, V = torch.svd(weight_2d)

    # Truncate
    U_r = U[:, :rank]
    S_r = torch.diag(S[:rank])
    V_r = V[:, :rank]

    # Create two layers
    layer1 = nn.Conv2d(
        conv_layer.in_channels,
        rank,
        conv_layer.kernel_size,
        stride=conv_layer.stride,
        padding=conv_layer.padding,
        bias=False
    )

    layer2 = nn.Conv2d(
        rank,
        conv_layer.out_channels,
        kernel_size=1,
        bias=conv_layer.bias is not None
    )

    # Set weights
    layer1.weight.data = V_r.t().view(rank, conv_layer.in_channels,
                                         conv_layer.kernel_size[0], conv_layer.kernel_size[1])
    layer2.weight.data = (U_r @ S_r).t().view(conv_layer.out_channels, rank, 1, 1)

    if conv_layer.bias is not None:
        layer2.bias.data = conv_layer.bias.data

    return nn.Sequential(layer1, layer2)
```

### Architecture Optimization

#### Depthwise Separable Convolution

```python
class DepthwiseSeparableConv(nn.Module):
    """Depthwise separable convolution for efficient models."""
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super().__init__()

        self.depthwise = nn.Conv2d(
            in_channels,
            in_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            groups=in_channels,
            bias=False
        )

        self.pointwise = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=1,
            bias=False
        )

        self.bn1 = nn.BatchNorm2d(in_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.depthwise(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.pointwise(x)
        x = self.bn2(x)
        x = self.relu(x)
        return x

# Replace standard conv with depthwise separable
def replace_with_depthwise(model):
    """Replace Conv2d layers with DepthwiseSeparableConv."""
    for name, module in list(model.named_children()):
        if isinstance(module, nn.Conv2d):
            if module.kernel_size == (1, 1):
                # Keep 1x1 conv as is (pointwise)
                continue

            # Replace with depthwise separable
            depthwise_conv = DepthwiseSeparableConv(
                module.in_channels,
                module.out_channels,
                kernel_size=module.kernel_size[0],
                stride=module.stride[0],
                padding=module.padding[0]
            )

            setattr(model, name, depthwise_conv)

    return model
```

#### MobileNet Block

```python
class MobileNetBlock(nn.Module):
    """Inverted residual block from MobileNetV2."""
    def __init__(self, in_channels, out_channels, stride, expand_ratio):
        super().__init__()

        hidden_dim = in_channels * expand_ratio

        layers = []

        # Expansion
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(in_channels, hidden_dim, 1, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True)
            ])

        # Depthwise
        layers.extend([
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride=stride,
                       padding=1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True)
        ])

        # Pointwise (linear)
        layers.append(nn.Conv2d(hidden_dim, out_channels, 1, bias=False))
        layers.append(nn.BatchNorm2d(out_channels))

        self.conv = nn.Sequential(*layers)

        # Skip connection
        self.use_skip = (stride == 1 and in_channels == out_channels)

    def forward(self, x):
        out = self.conv(x)
        if self.use_skip:
            return x + out
        return out
```

### Inference Optimization

#### Batching

```python
from collections import deque
import threading
import time

class BatchInference:
    """Batch inference for improved throughput."""
    def __init__(self, model, max_batch_size=32, max_wait_time=0.1):
        self.model = model
        self.model.eval()
        self.max_batch_size = max_batch_size
        self.max_wait_time = max_wait_time
        self.batch_queue = deque()
        self.results = {}
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        """Start batch processing thread."""
        self.running = True
        self.thread = threading.Thread(target=self._process_batches)
        self.thread.start()

    def stop(self):
        """Stop batch processing."""
        self.running = False
        self.thread.join()

    def predict(self, input_data):
        """Add input to batch queue."""
        request_id = id(input_data)
        with self.lock:
            self.batch_queue.append((request_id, input_data))
        return request_id

    def get_result(self, request_id, timeout=10):
        """Get prediction result."""
        start_time = time.time()
        while request_id not in self.results:
            if time.time() - start_time > timeout:
                raise TimeoutError("Prediction timeout")
            time.sleep(0.01)
        return self.results.pop(request_id)

    def _process_batches(self):
        """Process batches."""
        while self.running:
            batch = []
            start_time = time.time()

            with self.lock:
                while len(batch) < self.max_batch_size and \
                      (time.time() - start_time) < self.max_wait_time:
                    if self.batch_queue:
                        batch.append(self.batch_queue.popleft())
                    else:
                        time.sleep(0.001)

            if batch:
                request_ids, inputs = zip(*batch)
                batch_tensor = torch.stack(inputs)

                with torch.no_grad():
                    outputs = self.model(batch_tensor)

                with self.lock:
                    for req_id, output in zip(request_ids, outputs):
                        self.results[req_id] = output
```

#### Caching

```python
from functools import lru_cache
import hashlib
import pickle

class ModelCache:
    """Cache model predictions."""
    def __init__(self, cache_size=1000):
        self.cache_size = cache_size
        self.cache = {}

    def _get_key(self, input_data):
        """Generate cache key from input."""
        if isinstance(input_data, torch.Tensor):
            input_hash = hashlib.md5(input_data.numpy().tobytes()).hexdigest()
        else:
            input_hash = hashlib.md5(pickle.dumps(input_data)).hexdigest()
        return input_hash

    def get(self, input_data):
        """Get cached prediction."""
        key = self._get_key(input_data)
        return self.cache.get(key)

    def set(self, input_data, output):
        """Cache prediction."""
        key = self._get_key(input_data)

        # Evict oldest if cache is full
        if len(self.cache) >= self.cache_size:
            self.cache.pop(next(iter(self.cache)))

        self.cache[key] = output

    def clear(self):
        """Clear cache."""
        self.cache.clear()

# Usage
cache = ModelCache(cache_size=1000)

def predict_with_cache(model, input_data):
    """Predict with caching."""
    # Check cache
    cached_output = cache.get(input_data)
    if cached_output is not None:
        return cached_output

    # Run inference
    with torch.no_grad():
        output = model(input_data)

    # Cache result
    cache.set(input_data, output)

    return output
```

#### GPU Optimization

```python
import torch

def optimize_for_gpu(model):
    """Optimize model for GPU inference."""
    # Enable cuDNN benchmark for optimal convolution algorithms
    torch.backends.cudnn.benchmark = True

    # Disable deterministic mode for better performance
    torch.backends.cudnn.deterministic = False

    # Use half precision if supported
    if torch.cuda.is_available():
        model = model.half()

    return model

def optimize_inference(model, input_shape):
    """Optimize model for inference."""
    model.eval()

    # Optimize with torch.compile (PyTorch 2.0+)
    if hasattr(torch, 'compile'):
        model = torch.compile(model)

    # Add dummy input for tracing
    dummy_input = torch.randn(*input_shape)
    if torch.cuda.is_available():
        dummy_input = dummy_input.cuda()
        model = model.cuda()

    # Warm up
    with torch.no_grad():
        for _ in range(10):
            _ = model(dummy_input)

    return model
```

### ONNX Optimization

#### ONNX Export and Optimization

```python
import torch
import onnx
import onnxruntime as ort

def export_to_onnx(model, input_shape, output_path="model.onnx"):
    """Export PyTorch model to ONNX."""
    model.eval()

    dummy_input = torch.randn(*input_shape)

    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )

    # Verify model
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)

    return output_path

def optimize_onnx_model(onnx_path, optimized_path="model_optimized.onnx"):
    """Optimize ONNX model."""
    from onnxoptimizer import optimize

    onnx_model = onnx.load(onnx_path)

    # Apply optimizations
    optimized_model = optimize(
        onnx_model,
        passes=[
            'eliminate_unused_initializer',
            'fuse_add_bias_into_conv',
            'fuse_bn_into_conv',
            'fuse_consecutive_concats',
            'fuse_consecutive_reduce_unsqueeze',
            'fuse_consecutive_squeezes',
            'fuse_consecutive_transposes',
            'fuse_matmul_add_bias_into_gemm',
            'fuse_pad_into_conv',
            'fuse_transpose_into_gemm',
            'eliminate_nop_transpose',
            'eliminate_nop_pad',
            'eliminate_identity',
            'eliminate_deadend',
            'fuse_add_conv_into_conv',
            'fuse_consecutive_transposes',
            'fuse_transpose_into_gemm',
            'eliminate_nop_transpose',
            'eliminate_nop_pad',
            'eliminate_identity',
            'eliminate_deadend',
            'fuse_add_conv_into_conv',
            'fuse_consecutive_squeezes',
            'fuse_consecutive_transposes',
            'fuse_matmul_add_bias_into_gemm',
            'fuse_pad_into_conv',
            'fuse_transpose_into_gemm',
            'eliminate_nop_transpose',
            'eliminate_nop_pad',
            'eliminate_identity',
            'eliminate_deadend',
            'fuse_add_conv_into_conv',
            'fuse_consecutive_transposes',
            'fuse_transpose_into_gemm',
            'eliminate_nop_transpose',
            'eliminate_nop_pad',
            'eliminate_identity',
            'eliminate_deadend',
        ]
    )

    onnx.save(optimized_model, optimized_path)
    return optimized_path

# Usage
model = MyModel()
export_to_onnx(model, (1, 3, 224, 224))
optimize_onnx_model("model.onnx")
```

#### ONNX Runtime Optimization

```python
def create_optimized_onnx_session(onnx_path, providers=['CUDAExecutionProvider']):
    """Create optimized ONNX Runtime session."""
    sess_options = ort.SessionOptions()

    # Enable graph optimization
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    # Enable memory arena
    sess_options.enable_mem_pattern = True
    sess_options.enable_cpu_mem_arena = True

    # Set execution mode
    sess_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

    # Create session
    session = ort.InferenceSession(
        onnx_path,
        sess_options=sess_options,
        providers=providers
    )

    return session

# Usage
session = create_optimized_onnx_session("model.onnx")

# Run inference
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
outputs = session.run([output_name], {input_name: input_data})
```

### TensorRT Integration

#### TensorRT Conversion

```python
import torch
from torch2trt import TRTModule

def convert_to_tensorrt(model, input_shape, fp16_mode=True):
    """Convert PyTorch model to TensorRT."""
    model.eval()
    model = model.cuda()

    # Create dummy input
    x = torch.ones(input_shape).cuda()

    # Convert to TensorRT
    model_trt = torch2trt.torch2trt(
        model,
        [x],
        fp16_mode=fp16_mode,
        max_workspace_size=1 << 30  # 1GB
    )

    return model_trt

# Usage
model = MyModel()
model_trt = convert_to_tensorrt(model, (1, 3, 224, 224))

# Save TensorRT model
torch.save(model_trt.state_dict(), 'model_trt.pth')

# Load TensorRT model
model_trt = TRTModule()
model_trt.load_state_dict(torch.load('model_trt.pth'))
```

#### TensorRT with ONNX

```python
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

def build_tensorrt_engine(onnx_path, engine_path="model.trt", fp16=True):
    """Build TensorRT engine from ONNX model."""
    logger = trt.Logger(trt.Logger.WARNING)

    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)

    # Parse ONNX model
    with open(onnx_path, 'rb') as model:
        parser.parse(model.read())

    # Build configuration
    config = builder.create_builder_config()
    config.max_workspace_size = 1 << 30  # 1GB

    if fp16 and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)

    # Build engine
    engine = builder.build_engine(network, config)

    # Save engine
    with open(engine_path, 'wb') as f:
        f.write(engine.serialize())

    return engine

# Usage
engine = build_tensorrt_engine("model.onnx", fp16=True)
```

### Benchmarking Tools

#### Model Profiling

```python
import torch
import time
import numpy as np

class ModelProfiler:
    """Profile model performance."""
    def __init__(self, model, input_shape, device='cuda'):
        self.model = model
        self.input_shape = input_shape
        self.device = device
        self.model.eval()

        if device == 'cuda':
            self.model = self.model.cuda()

    def profile_inference(self, num_runs=100, warmup=10):
        """Profile inference latency."""
        dummy_input = torch.randn(*self.input_shape).to(self.device)

        # Warmup
        with torch.no_grad():
            for _ in range(warmup):
                _ = self.model(dummy_input)

        # Benchmark
        latencies = []
        with torch.no_grad():
            for _ in range(num_runs):
                if self.device == 'cuda':
                    torch.cuda.synchronize()

                start = time.perf_counter()
                _ = self.model(dummy_input)

                if self.device == 'cuda':
                    torch.cuda.synchronize()

                end = time.perf_counter()
                latencies.append((end - start) * 1000)  # ms

        return {
            'mean_ms': np.mean(latencies),
            'std_ms': np.std(latencies),
            'min_ms': np.min(latencies),
            'max_ms': np.max(latencies),
            'p50_ms': np.percentile(latencies, 50),
            'p95_ms': np.percentile(latencies, 95),
            'p99_ms': np.percentile(latencies, 99)
        }

    def profile_memory(self):
        """Profile GPU memory usage."""
        if self.device != 'cuda':
            return {'error': 'GPU memory profiling requires CUDA'}

        dummy_input = torch.randn(*self.input_shape).cuda()

        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()

        with torch.no_grad():
            _ = self.model(dummy_input)

        return {
            'allocated_mb': torch.cuda.max_memory_allocated() / 1024 / 1024,
            'reserved_mb': torch.cuda.max_memory_reserved() / 1024 / 1024
        }

    def profile_throughput(self, duration_seconds=10):
        """Profile inference throughput."""
        dummy_input = torch.randn(*self.input_shape).to(self.device)

        start_time = time.time()
        num_inferences = 0

        with torch.no_grad():
            while time.time() - start_time < duration_seconds:
                _ = self.model(dummy_input)
                num_inferences += 1

        elapsed = time.time() - start_time
        throughput = num_inferences / elapsed

        return {
            'duration_seconds': elapsed,
            'num_inferences': num_inferences,
            'throughput_per_second': throughput
        }

# Usage
profiler = ModelProfiler(model, (1, 3, 224, 224), device='cuda')
latency = profiler.profile_inference()
memory = profiler.profile_memory()
throughput = profiler.profile_throughput()

print(f"Latency: {latency['p95_ms']:.2f} ms (p95)")
print(f"Memory: {memory['allocated_mb']:.2f} MB")
print(f"Throughput: {throughput['throughput_per_second']:.2f} inferences/sec")
```

#### Model Comparison

```python
def compare_models(models, input_shape, device='cuda'):
    """Compare multiple models."""
    results = {}

    for name, model in models.items():
        print(f"\nProfiling {name}...")

        profiler = ModelProfiler(model, input_shape, device)

        latency = profiler.profile_inference()
        memory = profiler.profile_memory()
        throughput = profiler.profile_throughput()

        # Count parameters
        num_params = sum(p.numel() for p in model.parameters())

        results[name] = {
            'parameters': num_params,
            'latency_p95_ms': latency['p95_ms'],
            'memory_mb': memory['allocated_mb'],
            'throughput_per_sec': throughput['throughput_per_second']
        }

    # Print comparison
    print("\n" + "=" * 80)
    print(f"{'Model':<20} {'Params':>12} {'Latency (ms)':>15} {'Memory (MB)':>12} {'Throughput':>12}")
    print("=" * 80)
    for name, metrics in results.items():
        print(f"{name:<20} {metrics['parameters']:>12,} "
              f"{metrics['latency_p95_ms']:>15.2f} "
              f"{metrics['memory_mb']:>12.2f} "
              f"{metrics['throughput_per_sec']:>12.2f}")

    return results

# Usage
models = {
    'Original': original_model,
    'Quantized': quantized_model,
    'Pruned': pruned_model
}

compare_models(models, (1, 3, 224, 224))
```

## Best Practices

1. **Start Simple**
   - Begin with basic optimizations (FP16)
   - Gradually apply more aggressive techniques
   - Monitor accuracy after each optimization
   - Use baseline for comparison

2. **Measure Before Optimizing**
   - Profile model before optimization
   - Record baseline metrics (latency, memory, throughput)
   - Use realistic input data
   - Test on target hardware

3. **Use Appropriate Optimization Techniques**
   - Quantization for size reduction
   - Pruning for speed improvement
   - Distillation for model compression
   - Architecture design for efficiency

4. **Maintain Accuracy**
   - Set acceptable accuracy drop threshold
   - Use calibration data for quantization
   - Fine-tune after pruning
   - Validate on representative dataset

5. **Test on Target Hardware**
   - Optimize for production hardware
   - Test on actual deployment environment
   - Consider GPU/CPU constraints
   - Profile memory usage

6. **Handle Edge Cases**
   - Handle variable input sizes
   - Handle batch size 1
   - Handle different data types
   - Test with real-world data

7. **Version Control**
   - Keep original model backup
   - Document optimization steps
   - Track model versions
   - Maintain reproducibility

8. **Monitor in Production**
   - Track inference latency
   - Monitor memory usage
   - Set up alerts for anomalies
   - Log optimization metrics

9. **Use Production Frameworks**
   - ONNX for cross-platform deployment
   - TensorRT for NVIDIA GPUs
   - OpenVINO for Intel CPUs
   - TFLite for mobile deployment

10. **Iterative Improvement**
   - A/B test different optimization strategies
   - Collect production metrics
   - Continuously optimize based on data
   - Stay updated with new techniques

## Related Skills

- [`05-ai-ml-core/model-training`](05-ai-ml-core/model-training/SKILL.md)
- [`05-ai-ml-core/data-augmentation`](05-ai-ml-core/data-augmentation/SKILL.md)
- [`05-ai-ml-core/data-preprocessing`](05-ai-ml-core/data-preprocessing/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`06-ai-ml-production/llm-local-deployment`](06-ai-ml-production/llm-local-deployment/SKILL.md)
