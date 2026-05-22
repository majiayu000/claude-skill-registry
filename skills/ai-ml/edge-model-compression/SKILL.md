---
name: Edge Model Compression
description: Model compression techniques including quantization, pruning, and knowledge distillation for edge deployment
---

# Edge Model Compression

## Current Level: Expert (Enterprise Scale)

## Domain: Edge AI & TinyML
## Skill ID: 114

---

## Executive Summary

Edge Model Compression enables deployment of large, accurate machine learning models on resource-constrained edge devices through techniques like quantization, pruning, knowledge distillation, and neural architecture search. This capability is essential for bringing AI capabilities to edge devices with limited memory, compute, and power while maintaining acceptable accuracy.

### Strategic Necessity

- **Resource Constraints**: Deploy models on devices with <512KB RAM
- **Cost Reduction**: Reduce hardware requirements and power consumption
- **Latency Improvement**: Faster inference on edge devices
- **Bandwidth Savings**: Smaller models for faster OTA updates
- **Scalability**: Deploy AI to millions of edge devices

---

## Technical Deep Dive

### Compression Techniques Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Model Compression Pipeline                            │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Original   │    │   Compressed │    │   Optimized   │                  │
│  │   Model      │───▶│   Model      │───▶│   Model       │                  │
│  │   100MB      │    │   10MB       │    │   1MB         │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Compression Techniques                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │ Quantization │  │   Pruning    │  │ Distillation │              │   │
│  │  │  4-32x       │  │  2-10x       │  │  2-5x        │              │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │   │
│  └─────────┼─────────────────┼─────────────────┼─────────────────────────┘   │
│            │                 │                 │                           │
│            ▼                 ▼                 ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Optimization Techniques                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   NAS        │  │   Fusion     │  │   Layer      │              │   │
│  │  │  2-5x        │  │  1.5-3x      │  │   Grouping   │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Quantization

Quantization reduces model size and improves inference speed by reducing numerical precision of weights and activations.

**Quantization Types:**

```python
from enum import Enum
from typing import Dict, Any, Tuple
import numpy as np
import torch

class QuantizationType(Enum):
    """Quantization types"""
    FP32 = "fp32"           # Full precision
    FP16 = "fp16"           # Half precision
    INT8 = "int8"           # 8-bit integer
    INT4 = "int4"           # 4-bit integer
    MIXED = "mixed"         # Mixed precision

class QuantizationStrategy(Enum):
    """Quantization strategies"""
    POST_TRAINING = "post_training"  # Post-training quantization
    QUANTIZATION_AWARE = "quantization_aware"  # Quantization-aware training
    DYNAMIC = "dynamic"  # Dynamic quantization

class ModelQuantizer:
    """Model quantization for edge deployment"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.quantization_type = QuantizationType(
            config.get('quantization_type', 'int8')
        )
        self.strategy = QuantizationStrategy(
            config.get('strategy', 'post_training')
        )
        self.calibration_data = None
        
    def quantize_model(self, model: torch.nn.Module) -> torch.nn.Module:
        """Quantize model based on strategy"""
        if self.strategy == QuantizationStrategy.POST_TRAINING:
            return self._post_training_quantization(model)
        elif self.strategy == QuantizationStrategy.QUANTIZATION_AWARE:
            return self._quantization_aware_training(model)
        elif self.strategy == QuantizationStrategy.DYNAMIC:
            return self._dynamic_quantization(model)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
    
    def _post_training_quantization(
        self, 
        model: torch.nn.Module
    ) -> torch.nn.Module:
        """Post-training quantization"""
        # Calibrate with representative data
        self._calibrate_model(model)
        
        # Apply quantization
        if self.quantization_type == QuantizationType.INT8:
            quantized_model = torch.quantization.quantize_dynamic(
                model,
                {torch.nn.Linear, torch.nn.Conv2d},
                dtype=torch.qint8
            )
        elif self.quantization_type == QuantizationType.FP16:
            quantized_model = model.half()
        else:
            raise ValueError(f"Unsupported type: {self.quantization_type}")
        
        return quantized_model
    
    def _quantization_aware_training(
        self, 
        model: torch.nn.Module
    ) -> torch.nn.Module:
        """Quantization-aware training"""
        # Prepare model for QAT
        model.qconfig = torch.quantization.get_default_qat_qconfig(
            'fbgemm'
        )
        model_prepared = torch.quantization.prepare_qat(model)
        
        # Train model (caller's responsibility)
        # model_prepared = train_model(model_prepared, data)
        
        # Convert to quantized model
        quantized_model = torch.quantization.convert(model_prepared)
        
        return quantized_model
    
    def _dynamic_quantization(
        self, 
        model: torch.nn.Module
    ) -> torch.nn.Module:
        """Dynamic quantization"""
        quantized_model = torch.quantization.quantize_dynamic(
            model,
            {torch.nn.Linear, torch.nn.LSTM, torch.nn.GRU},
            dtype=torch.qint8
        )
        return quantized_model
    
    def _calibrate_model(self, model: torch.nn.Module):
        """Calibrate model with representative data"""
        if self.calibration_data is None:
            raise ValueError("Calibration data not set")
        
        # Prepare model for calibration
        model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
        model_prepared = torch.quantization.prepare(model)
        
        # Run calibration
        with torch.no_grad():
            for data in self.calibration_data:
                model_prepared(data)
    
    def set_calibration_data(self, data: torch.utils.data.DataLoader):
        """Set calibration data for post-training quantization"""
        self.calibration_data = data
    
    def compute_quantization_metrics(
        self, 
        original: torch.nn.Module,
        quantized: torch.nn.Module,
        test_data: torch.utils.data.DataLoader
    ) -> Dict[str, float]:
        """Compute quantization metrics"""
        original_accuracy = self._evaluate_model(original, test_data)
        quantized_accuracy = self._evaluate_model(quantized, test_data)
        
        original_size = self._get_model_size(original)
        quantized_size = self._get_model_size(quantized)
        
        return {
            'original_accuracy': original_accuracy,
            'quantized_accuracy': quantized_accuracy,
            'accuracy_drop': original_accuracy - quantized_accuracy,
            'original_size_mb': original_size,
            'quantized_size_mb': quantized_size,
            'compression_ratio': original_size / quantized_size,
            'speedup': self._measure_speedup(original, quantized, test_data)
        }
    
    def _evaluate_model(
        self, 
        model: torch.nn.Module,
        test_data: torch.utils.data.DataLoader
    ) -> float:
        """Evaluate model accuracy"""
        model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in test_data:
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        return correct / total
    
    def _get_model_size(self, model: torch.nn.Module) -> float:
        """Get model size in MB"""
        param_size = 0
        buffer_size = 0
        
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        size_mb = (param_size + buffer_size) / 1024 / 1024
        return size_mb
    
    def _measure_speedup(
        self, 
        original: torch.nn.Module,
        quantized: torch.nn.Module,
        test_data: torch.utils.data.DataLoader
    ) -> float:
        """Measure inference speedup"""
        import time
        
        # Measure original
        original.eval()
        start = time.time()
        with torch.no_grad():
            for inputs, _ in test_data:
                _ = original(inputs)
        original_time = time.time() - start
        
        # Measure quantized
        quantized.eval()
        start = time.time()
        with torch.no_grad():
            for inputs, _ in test_data:
                _ = quantized(inputs)
        quantized_time = time.time() - start
        
        return original_time / quantized_time
```

### 2. Pruning

Pruning removes less important weights from the model to reduce size and computation.

```python
class PruningType(Enum):
    """Pruning types"""
    MAGNITUDE = "magnitude"  # Magnitude-based pruning
    STRUCTURED = "structured"  # Structured pruning
    GRADIENT = "gradient"  # Gradient-based pruning
    RANDOM = "random"  # Random pruning

class ModelPruner:
    """Model pruning for edge deployment"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pruning_type = PruningType(config.get('pruning_type', 'magnitude'))
        self.sparsity = config.get('sparsity', 0.5)
        self.iterative = config.get('iterative', True)
        self.iterations = config.get('iterations', 10)
        
    def prune_model(self, model: torch.nn.Module) -> torch.nn.Module:
        """Prune model based on strategy"""
        if self.iterative:
            return self._iterative_pruning(model)
        else:
            return self._one_shot_pruning(model)
    
    def _one_shot_pruning(self, model: torch.nn.Module) -> torch.nn.Module:
        """One-shot pruning"""
        if self.pruning_type == PruningType.MAGNITUDE:
            return self._magnitude_pruning(model, self.sparsity)
        elif self.pruning_type == PruningType.STRUCTURED:
            return self._structured_pruning(model, self.sparsity)
        elif self.pruning_type == PruningType.GRADIENT:
            return self._gradient_pruning(model, self.sparsity)
        else:
            raise ValueError(f"Unknown pruning type: {self.pruning_type}")
    
    def _iterative_pruning(self, model: torch.nn.Module) -> torch.nn.Module:
        """Iterative pruning"""
        current_sparsity = 0.0
        sparsity_step = self.sparsity / self.iterations
        
        for i in range(self.iterations):
            current_sparsity += sparsity_step
            
            # Prune model
            model = self._magnitude_pruning(model, current_sparsity)
            
            # Fine-tune model (caller's responsibility)
            # model = fine_tune(model, data)
        
        return model
    
    def _magnitude_pruning(
        self, 
        model: torch.nn.Module,
        sparsity: float
    ) -> torch.nn.Module:
        """Magnitude-based pruning"""
        parameters_to_prune = []
        
        for name, module in model.named_modules():
            if isinstance(module, (torch.nn.Linear, torch.nn.Conv2d)):
                parameters_to_prune.append((module, 'weight'))
        
        # Apply pruning
        torch.nn.utils.prune.global_unstructured(
            parameters_to_prune,
            pruning_method=torch.nn.utils.prune.L1Unstructured,
            amount=sparsity
        )
        
        # Make pruning permanent
        for module, name in parameters_to_prune:
            torch.nn.utils.prune.remove(module, name)
        
        return model
    
    def _structured_pruning(
        self, 
        model: torch.nn.Module,
        sparsity: float
    ) -> torch.nn.Module:
        """Structured pruning (prune entire filters/neurons)"""
        for module in model.modules():
            if isinstance(module, torch.nn.Conv2d):
                # Prune filters based on L2 norm
                weights = module.weight.data
                filter_norms = torch.norm(weights.view(weights.size(0), -1), dim=1)
                
                # Determine number of filters to prune
                num_filters = module.out_channels
                num_to_prune = int(sparsity * num_filters)
                
                # Get indices of filters to prune
                _, indices = torch.sort(filter_norms)
                prune_indices = indices[:num_to_prune]
                
                # Zero out pruned filters
                for idx in prune_indices:
                    module.weight.data[idx] = 0.0
                    if module.bias is not None:
                        module.bias.data[idx] = 0.0
        
        return model
    
    def _gradient_pruning(
        self, 
        model: torch.nn.Module,
        sparsity: float
    ) -> torch.nn.Module:
        """Gradient-based pruning"""
        # This requires gradients from training
        # Caller should provide gradients or train model first
        
        for name, param in model.named_parameters():
            if 'weight' in name and param.grad is not None:
                # Prune based on gradient magnitude
                grad_magnitude = torch.abs(param.grad)
                threshold = torch.quantile(grad_magnitude, sparsity)
                
                mask = grad_magnitude > threshold
                param.data = param.data * mask.float()
        
        return model
    
    def compute_pruning_metrics(
        self, 
        original: torch.nn.Module,
        pruned: torch.nn.Module,
        test_data: torch.utils.data.DataLoader
    ) -> Dict[str, float]:
        """Compute pruning metrics"""
        original_accuracy = self._evaluate_model(original, test_data)
        pruned_accuracy = self._evaluate_model(pruned, test_data)
        
        original_size = self._get_model_size(original)
        pruned_size = self._get_model_size(pruned)
        
        actual_sparsity = self._compute_sparsity(pruned)
        
        return {
            'original_accuracy': original_accuracy,
            'pruned_accuracy': pruned_accuracy,
            'accuracy_drop': original_accuracy - pruned_accuracy,
            'original_size_mb': original_size,
            'pruned_size_mb': pruned_size,
            'compression_ratio': original_size / pruned_size,
            'actual_sparsity': actual_sparsity,
            'flops_reduction': self._compute_flops_reduction(original, pruned)
        }
    
    def _compute_sparsity(self, model: torch.nn.Module) -> float:
        """Compute actual sparsity of model"""
        total_params = 0
        zero_params = 0
        
        for param in model.parameters():
            total_params += param.numel()
            zero_params += (param == 0).sum().item()
        
        return zero_params / total_params if total_params > 0 else 0.0
    
    def _compute_flops_reduction(
        self, 
        original: torch.nn.Module,
        pruned: torch.nn.Module
    ) -> float:
        """Compute FLOPs reduction"""
        # Simplified FLOPs estimation
        original_flops = self._estimate_flops(original)
        pruned_flops = self._estimate_flops(pruned)
        
        return 1.0 - (pruned_flops / original_flops) if original_flops > 0 else 0.0
    
    def _estimate_flops(self, model: torch.nn.Module) -> int:
        """Estimate model FLOPs"""
        flops = 0
        
        for module in model.modules():
            if isinstance(module, torch.nn.Conv2d):
                # Conv2D: kernel_size * in_channels * out_channels * output_size
                kernel_size = module.kernel_size[0] * module.kernel_size[1]
                in_channels = module.in_channels
                out_channels = module.out_channels
                output_size = 1  # Simplified
                flops += kernel_size * in_channels * out_channels * output_size
            elif isinstance(module, torch.nn.Linear):
                # Linear: in_features * out_features
                flops += module.in_features * module.out_features
        
        return flops
```

### 3. Knowledge Distillation

Knowledge distillation transfers knowledge from a large teacher model to a smaller student model.

```python
class KnowledgeDistiller:
    """Knowledge distillation for model compression"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.temperature = config.get('temperature', 5.0)
        self.alpha = config.get('alpha', 0.5)  # Weight for distillation loss
        self.beta = 1.0 - self.alpha  # Weight for hard loss
        
    def distill(
        self, 
        teacher: torch.nn.Module,
        student: torch.nn.Module,
        train_data: torch.utils.data.DataLoader,
        epochs: int = 10
    ) -> torch.nn.Module:
        """Distill knowledge from teacher to student"""
        # Freeze teacher
        teacher.eval()
        for param in teacher.parameters():
            param.requires_grad = False
        
        # Setup optimizer
        optimizer = torch.optim.Adam(student.parameters(), lr=0.001)
        criterion = torch.nn.CrossEntropyLoss()
        
        # Training loop
        student.train()
        for epoch in range(epochs):
            total_loss = 0.0
            
            for inputs, labels in train_data:
                optimizer.zero_grad()
                
                # Forward pass
                with torch.no_grad():
                    teacher_outputs = teacher(inputs)
                
                student_outputs = student(inputs)
                
                # Compute losses
                distillation_loss = self._compute_distillation_loss(
                    teacher_outputs,
                    student_outputs
                )
                
                hard_loss = criterion(student_outputs, labels)
                
                # Combined loss
                loss = self.alpha * distillation_loss + self.beta * hard_loss
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_data):.4f}")
        
        return student
    
    def _compute_distillation_loss(
        self,
        teacher_outputs: torch.Tensor,
        student_outputs: torch.Tensor
    ) -> torch.Tensor:
        """Compute knowledge distillation loss"""
        # Soften outputs with temperature
        teacher_soft = torch.nn.functional.softmax(
            teacher_outputs / self.temperature,
            dim=1
        )
        student_soft = torch.nn.functional.log_softmax(
            student_outputs / self.temperature,
            dim=1
        )
        
        # KL divergence loss
        loss = torch.nn.functional.kl_div(
            student_soft,
            teacher_soft,
            reduction='batchmean'
        )
        
        # Scale by temperature squared
        loss = loss * (self.temperature ** 2)
        
        return loss
    
    def compute_distillation_metrics(
        self, 
        teacher: torch.nn.Module,
        student: torch.nn.Module,
        test_data: torch.utils.data.DataLoader
    ) -> Dict[str, float]:
        """Compute distillation metrics"""
        teacher_accuracy = self._evaluate_model(teacher, test_data)
        student_accuracy = self._evaluate_model(student, test_data)
        
        teacher_size = self._get_model_size(teacher)
        student_size = self._get_model_size(student)
        
        return {
            'teacher_accuracy': teacher_accuracy,
            'student_accuracy': student_accuracy,
            'accuracy_retention': student_accuracy / teacher_accuracy,
            'teacher_size_mb': teacher_size,
            'student_size_mb': student_size,
            'compression_ratio': teacher_size / student_size,
            'parameter_reduction': 1.0 - (student_size / teacher_size)
        }
```

### 4. Neural Architecture Search (NAS)

```python
class NeuralArchitectureSearch:
    """Neural architecture search for edge-optimized models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.search_space = config.get('search_space', 'default')
        search_method = config.get('search_method', 'darts')
        
        if search_method == 'darts':
            self.searcher = DARTSSearcher(config)
        elif search_method == 'nasnet':
            self.searcher = NASNetSearcher(config)
        else:
            raise ValueError(f"Unknown search method: {search_method}")
    
    def search(
        self,
        input_shape: Tuple[int, ...],
        num_classes: int,
        train_data: torch.utils.data.DataLoader,
        epochs: int = 50
    ) -> torch.nn.Module:
        """Search for optimal architecture"""
        return self.searcher.search(
            input_shape,
            num_classes,
            train_data,
            epochs
        )

class DARTSSearcher:
    """Differentiable Architecture Search (DARTS)"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.num_nodes = config.get('num_nodes', 4)
        self.num_ops = config.get('num_ops', 8)
        
    def search(
        self,
        input_shape: Tuple[int, ...],
        num_classes: int,
        train_data: torch.utils.data.DataLoader,
        epochs: int
    ) -> torch.nn.Module:
        """Search for optimal architecture using DARTS"""
        # Initialize architecture
        model = self._initialize_network(input_shape, num_classes)
        
        # Setup optimizer
        optimizer_w = torch.optim.SGD(
            model.weights_parameters(),
            lr=0.025,
            momentum=0.9,
            weight_decay=3e-4
        )
        optimizer_alpha = torch.optim.Adam(
            model.arch_parameters(),
            lr=3e-4,
            betas=(0.5, 0.999),
            weight_decay=1e-3
        )
        
        # Search loop
        for epoch in range(epochs):
            # Train architecture parameters
            self._train_architecture(model, train_data, optimizer_alpha)
            
            # Train network weights
            self._train_weights(model, train_data, optimizer_w)
        
        # Derive final architecture
        final_model = self._derive_architecture(model)
        
        return final_model
    
    def _initialize_network(
        self,
        input_shape: Tuple[int, ...],
        num_classes: int
    ) -> torch.nn.Module:
        """Initialize DARTS network"""
        # Simplified implementation
        # In practice, this would create a search space
        # with mixed operations and architecture parameters
        pass
    
    def _train_architecture(
        self,
        model: torch.nn.Module,
        data: torch.utils.data.DataLoader,
        optimizer: torch.optim.Optimizer
    ):
        """Train architecture parameters"""
        pass
    
    def _train_weights(
        self,
        model: torch.nn.Module,
        data: torch.utils.data.DataLoader,
        optimizer: torch.optim.Optimizer
    ):
        """Train network weights"""
        pass
    
    def _derive_architecture(
        self,
        model: torch.nn.Module
    ) -> torch.nn.Module:
        """Derive final architecture from search"""
        pass
```

---

## Tooling & Tech Stack

### Compression Frameworks
- **TensorFlow Model Optimization Toolkit**: Quantization, pruning, clustering
- **PyTorch Quantization**: Native quantization support
- **ONNX Runtime**: Cross-platform optimization
- **TensorRT**: NVIDIA GPU optimization

### NAS Frameworks
- **AutoKeras**: Automated neural architecture search
- **NVIDIA NVAutoML**: AutoML for edge
- **FBNetV3**: Facebook's NAS framework
- **Once-for-All**: Train once, deploy anywhere

### Development Tools
- **Python 3.9+**: Primary language
- **PyTorch/TensorFlow**: ML frameworks
- **TensorBoard**: Visualization
- **Netron**: Model visualization

### Hardware Platforms
- **NVIDIA Jetson**: Edge AI devices
- **Intel Neural Compute Stick**: Edge inference
- **Google Coral**: Edge TPU
- **ARM Ethos**: NPU optimization

---

## Configuration Essentials

### Compression Configuration

```yaml
# config/compression_config.yaml
quantization:
  enabled: true
  type: "int8"  # fp32, fp16, int8, int4, mixed
  strategy: "post_training"  # post_training, quantization_aware, dynamic
  calibration_samples: 100
  per_channel: true

pruning:
  enabled: true
  type: "magnitude"  # magnitude, structured, gradient, random
  sparsity: 0.5
  iterative: true
  iterations: 10
  fine_tune_epochs: 5

distillation:
  enabled: false
  temperature: 5.0
  alpha: 0.5
  beta: 0.5
  epochs: 10

nas:
  enabled: false
  search_method: "darts"  # darts, nasnet, enas
  search_space: "default"
  num_nodes: 4
  search_epochs: 50

optimization:
  target_device: "edge_mcu"  # edge_mcu, edge_gpu, cloud
  max_size_mb: 1.0
  max_latency_ms: 100
  min_accuracy: 0.90
  target_flops: 1000000  # 1M FLOPs

output:
  format: "tflite"  # tflite, onnx, torchscript
  optimize_for: "latency"  # latency, size, accuracy
  include_metadata: true
```

---

## Code Examples

### Good: Complete Compression Pipeline

```python
# compression/pipeline.py
from typing import Dict, Any, Tuple
import torch
import logging

from compression.quantization import ModelQuantizer
from compression.pruning import ModelPruner
from compression.distillation import KnowledgeDistiller
from compression.nas import NeuralArchitectureSearch
from compression.metrics import CompressionMetrics

logger = logging.getLogger(__name__)

class ModelCompressionPipeline:
    """Complete model compression pipeline"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize components
        if config['quantization']['enabled']:
            self.quantizer = ModelQuantizer(config['quantization'])
        
        if config['pruning']['enabled']:
            self.pruner = ModelPruner(config['pruning'])
        
        if config['distillation']['enabled']:
            self.distiller = KnowledgeDistiller(config['distillation'])
        
        if config['nas']['enabled']:
            self.nas = NeuralArchitectureSearch(config['nas'])
        
        self.metrics = CompressionMetrics()
    
    def compress_model(
        self,
        model: torch.nn.Module,
        train_data: torch.utils.data.DataLoader,
        test_data: torch.utils.data.DataLoader
    ) -> Tuple[torch.nn.Module, Dict[str, Any]]:
        """Compress model using configured techniques"""
        logger.info("Starting model compression pipeline...")
        
        # Store original metrics
        original_metrics = self.metrics.compute_baseline(
            model, test_data
        )
        logger.info(f"Original model: {original_metrics}")
        
        current_model = model
        
        # Step 1: NAS (if enabled)
        if self.config['nas']['enabled']:
            logger.info("Running Neural Architecture Search...")
            current_model = self.nas.search(
                input_shape=self._get_input_shape(train_data),
                num_classes=self._get_num_classes(train_data),
                train_data=train_data,
                epochs=self.config['nas']['search_epochs']
            )
            logger.info("NAS completed")
        
        # Step 2: Knowledge Distillation (if enabled)
        if self.config['distillation']['enabled']:
            logger.info("Running Knowledge Distillation...")
            # Create student model (smaller architecture)
            student_model = self._create_student_model(current_model)
            
            current_model = self.distiller.distill(
                teacher=current_model,
                student=student_model,
                train_data=train_data,
                epochs=self.config['distillation']['epochs']
            )
            logger.info("Distillation completed")
        
        # Step 3: Pruning (if enabled)
        if self.config['pruning']['enabled']:
            logger.info("Running Model Pruning...")
            current_model = self.pruner.prune_model(current_model)
            
            # Fine-tune after pruning
            if self.config['pruning']['iterative']:
                current_model = self._fine_tune(
                    current_model,
                    train_data,
                    epochs=self.config['pruning']['fine_tune_epochs']
                )
            
            logger.info("Pruning completed")
        
        # Step 4: Quantization (if enabled)
        if self.config['quantization']['enabled']:
            logger.info("Running Model Quantization...")
            
            # Set calibration data for post-training quantization
            if self.config['quantization']['strategy'] == 'post_training':
                self.quantizer.set_calibration_data(train_data)
            
            current_model = self.quantizer.quantize_model(current_model)
            logger.info("Quantization completed")
        
        # Compute final metrics
        final_metrics = self.metrics.compute_baseline(
            current_model, test_data
        )
        logger.info(f"Compressed model: {final_metrics}")
        
        # Compute compression summary
        summary = self._compute_summary(
            original_metrics,
            final_metrics
        )
        logger.info(f"Compression summary: {summary}")
        
        # Validate against targets
        self._validate_targets(summary)
        
        return current_model, summary
    
    def _get_input_shape(
        self, 
        data: torch.utils.data.DataLoader
    ) -> Tuple[int, ...]:
        """Get input shape from data loader"""
        for inputs, _ in data:
            return tuple(inputs.shape[1:])
        return (224, 224, 3)  # Default
    
    def _get_num_classes(
        self, 
        data: torch.utils.data.DataLoader
    ) -> int:
        """Get number of classes from data loader"""
        for _, labels in data:
            return len(torch.unique(labels))
        return 10  # Default
    
    def _create_student_model(
        self, 
        teacher: torch.nn.Module
    ) -> torch.nn.Module:
        """Create student model from teacher"""
        # Simplified: create smaller version
        # In practice, this would use a predefined student architecture
        student = type(teacher)(
            in_channels=teacher.in_channels,
            num_classes=teacher.num_classes,
            width_multiplier=0.5  # 50% of teacher size
        )
        return student
    
    def _fine_tune(
        self,
        model: torch.nn.Module,
        data: torch.utils.data.DataLoader,
        epochs: int
    ) -> torch.nn.Module:
        """Fine-tune model after pruning"""
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        criterion = torch.nn.CrossEntropyLoss()
        
        model.train()
        for epoch in range(epochs):
            total_loss = 0.0
            for inputs, labels in data:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            logger.info(f"Fine-tune epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(data):.4f}")
        
        return model
    
    def _compute_summary(
        self,
        original: Dict[str, float],
        final: Dict[str, float]
    ) -> Dict[str, Any]:
        """Compute compression summary"""
        return {
            'original_size_mb': original['size_mb'],
            'final_size_mb': final['size_mb'],
            'compression_ratio': original['size_mb'] / final['size_mb'],
            'size_reduction_percent': (1 - final['size_mb'] / original['size_mb']) * 100,
            'original_accuracy': original['accuracy'],
            'final_accuracy': final['accuracy'],
            'accuracy_drop': original['accuracy'] - final['accuracy'],
            'accuracy_retention_percent': (final['accuracy'] / original['accuracy']) * 100,
            'original_latency_ms': original['latency_ms'],
            'final_latency_ms': final['latency_ms'],
            'speedup': original['latency_ms'] / final['latency_ms'],
            'latency_reduction_percent': (1 - final['latency_ms'] / original['latency_ms']) * 100
        }
    
    def _validate_targets(self, summary: Dict[str, Any]):
        """Validate compression against targets"""
        targets = self.config['optimization']
        
        # Check size
        if summary['final_size_mb'] > targets['max_size_mb']:
            logger.warning(
                f"Size {summary['final_size_mb']}MB exceeds target {targets['max_size_mb']}MB"
            )
        
        # Check latency
        if summary['final_latency_ms'] > targets['max_latency_ms']:
            logger.warning(
                f"Latency {summary['final_latency_ms']}ms exceeds target {targets['max_latency_ms']}ms"
            )
        
        # Check accuracy
        if summary['final_accuracy'] < targets['min_accuracy']:
            logger.warning(
                f"Accuracy {summary['final_accuracy']} below target {targets['min_accuracy']}"
            )
    
    def export_model(
        self,
        model: torch.nn.Module,
        output_path: str,
        format: str = 'tflite'
    ):
        """Export compressed model"""
        if format == 'tflite':
            self._export_tflite(model, output_path)
        elif format == 'onnx':
            self._export_onnx(model, output_path)
        elif format == 'torchscript':
            self._export_torchscript(model, output_path)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def _export_tflite(self, model: torch.nn.Module, output_path: str):
        """Export to TensorFlow Lite format"""
        # Convert PyTorch to TensorFlow first, then to TFLite
        # This is a simplified example
        logger.info(f"Exporting model to TFLite: {output_path}")
        # Implementation would use torch.onnx or similar
        pass
    
    def _export_onnx(self, model: torch.nn.Module, output_path: str):
        """Export to ONNX format"""
        logger.info(f"Exporting model to ONNX: {output_path}")
        dummy_input = torch.randn(1, 3, 224, 224)
        torch.onnx.export(
            model,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output']
        )
    
    def _export_torchscript(self, model: torch.nn.Module, output_path: str):
        """Export to TorchScript format"""
        logger.info(f"Exporting model to TorchScript: {output_path}")
        dummy_input = torch.randn(1, 3, 224, 224)
        traced_model = torch.jit.trace(model, dummy_input)
        traced_model.save(output_path)
```

### Bad: Anti-pattern Example

```python
# BAD: No validation
def bad_compression(model):
    # Compresses without checking accuracy
    quantized = quantize(model)
    pruned = prune(quantized)
    return pruned

# BAD: No fine-tuning
def bad_pruning(model):
    # Prunes without fine-tuning
    pruned = prune(model, sparsity=0.5)
    return pruned

# BAD: Wrong order
def bad_pipeline(model):
    # Quantizes before pruning (wrong order)
    quantized = quantize(model)
    pruned = prune(quantized)
    return pruned

# BAD: No calibration
def bad_quantization(model):
    # Quantizes without calibration
    return quantize(model)

# BAD: No metrics
def bad_compression(model):
    # Doesn't measure impact
    compressed = compress(model)
    return compressed
```

---

## Standards, Compliance & Security

### Industry Standards
- **ONNX**: Open Neural Network Exchange format
- **TensorFlow Lite**: Edge deployment standard
- **OpenVINO**: Intel optimization standard
- **NVIDIA TensorRT**: GPU optimization standard

### Security Best Practices
- **Model Encryption**: Protect model IP
- **Secure Deployment**: Verify model integrity
- **Access Control**: Control model distribution
- **Audit Logging**: Track model versions

### Compliance Requirements
- **Model Versioning**: Track model provenance
- **Performance Monitoring**: Track accuracy drift
- **Documentation**: Document compression process
- **Validation**: Validate compressed models

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/example/edge-model-compression.git
cd edge-model-compression

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy example config
cp config/compression_config.yaml.example config/compression_config.yaml

# Edit configuration
vim config/compression_config.yaml
```

### 3. Compress Model

```python
from compression.pipeline import ModelCompressionPipeline
import torch

# Load model
model = torch.load('model.pth')

# Load data
train_data = torch.load('train_data.pth')
test_data = torch.load('test_data.pth')

# Create pipeline
pipeline = ModelCompressionPipeline(config)

# Compress model
compressed_model, summary = pipeline.compress_model(
    model,
    train_data,
    test_data
)

# Export model
pipeline.export_model(compressed_model, 'compressed_model.tflite')
```

### 4. Evaluate Results

```python
print(f"Compression ratio: {summary['compression_ratio']:.2f}x")
print(f"Accuracy retention: {summary['accuracy_retention_percent']:.2f}%")
print(f"Speedup: {summary['speedup']:.2f}x")
```

---

## Production Checklist

### Model Compression
- [ ] Quantization applied correctly
- [ ] Pruning applied correctly
- [ ] Fine-tuning completed
- [ ] Calibration data representative
- [ ] Model validated on test set

### Export & Deployment
- [ ] Model exported in correct format
- [ ] Model optimized for target device
- [ ] Model signed/encrypted
- [ ] Deployment package created
- [ ] OTA update configured

### Validation
- [ ] Accuracy meets requirements
- [ ] Latency meets requirements
- [ ] Size meets requirements
- [ ] Power consumption measured
- [ ] Stress testing completed

### Documentation
- [ ] Compression process documented
- [ ] Model metadata recorded
- [ ] Performance metrics documented
- [ ] Known limitations documented
- [ ] User guide created

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Validation**
   ```python
   # BAD: Compresses without checking
   compressed = quantize(model)
   ```

2. **No Fine-tuning**
   ```python
   # BAD: Prunes without recovery
   pruned = prune(model, sparsity=0.5)
   ```

3. **Wrong Order**
   ```python
   # BAD: Quantizes before pruning
   quantized = quantize(model)
   pruned = prune(quantized)
   ```

4. **No Calibration**
   ```python
   # BAD: Quantizes without calibration
   return quantize(model)
   ```

5. **No Metrics**
   ```python
   # BAD: Doesn't measure impact
   compressed = compress(model)
   ```

### ✅ Follow These Practices

1. **Validate Accuracy**
   ```python
   # GOOD: Checks accuracy
   compressed = quantize(model)
   if accuracy(compressed) < threshold:
       adjust_parameters()
   ```

2. **Fine-tune After Pruning**
   ```python
   # GOOD: Recovers accuracy
   pruned = prune(model, sparsity=0.5)
   fine_tuned = fine_tune(pruned, data)
   ```

3. **Correct Order**
   ```python
   # GOOD: Prunes before quantizing
   pruned = prune(model, sparsity=0.5)
   quantized = quantize(pruned)
   ```

4. **Calibrate Quantization**
   ```python
   # GOOD: Uses calibration data
   quantizer.set_calibration_data(data)
   quantized = quantizer.quantize(model)
   ```

5. **Measure Metrics**
   ```python
   # GOOD: Tracks all metrics
   metrics = evaluate(compressed, original)
   log_metrics(metrics)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Development**: 120-200 hours
- **Pipeline Development**: 80-120 hours
- **Testing & Validation**: 60-100 hours
- **Total**: 260-420 hours

### Operational Costs
- **Compute Resources**: $200-1000/month
- **Storage**: $50-200/month
- **Monitoring**: $50-150/month
- **Support**: 10-20 hours/month

### ROI Metrics
- **Model Size Reduction**: 80-95%
- **Latency Improvement**: 2-10x
- **Power Savings**: 50-80%
- **Hardware Cost Reduction**: 30-60%

### KPI Targets
- **Compression Ratio**: > 10x
- **Accuracy Retention**: > 95%
- **Latency Reduction**: > 50%
- **Power Reduction**: > 50%
- **Deployment Success Rate**: > 99%

---

## Integration Points / Related Skills

### Upstream Skills
- **91. Feature Store Implementation**: Feature extraction
- **92. Drift Detection and Retraining**: Model drift monitoring
- **93. Model Registry and Versioning**: Model lifecycle

### Parallel Skills
- **111. TinyML Microcontroller AI**: Edge inference
- **112. Hybrid Inference Architecture**: Cloud-edge coordination
- **113. On-Device Model Training**: Federated learning
- **115. Edge AI Development Workflow**: End-to-end pipeline

### Downstream Skills
- **101. High Performance Inference**: Inference optimization
- **102. Model Optimization and Quantization**: Model compression
- **103. Serverless Inference**: Cloud fallback
- **116. Agentic AI Frameworks**: Agent-based AI

### Cross-Domain Skills
- **14. Monitoring and Observability**: Metrics and tracing
- **15. DevOps Infrastructure**: Deployment automation
- **81. SaaS FinOps Pricing**: Cost optimization
- **84. Compliance AI Governance**: Regulatory compliance

---

## References & Resources

### Documentation
- [TensorFlow Model Optimization](https://www.tensorflow.org/model_optimization)
- [PyTorch Quantization](https://pytorch.org/docs/stable/quantization.html)
- [ONNX Runtime](https://onnxruntime.ai/)
- [TensorRT](https://developer.nvidia.com/tensorrt)

### NAS Frameworks
- [AutoKeras](https://autokeras.com/)
- [NVIDIA NVAutoML](https://developer.nvidia.com/nvidia-tao-toolkit)
- [FBNetV3](https://github.com/facebookresearch/FBNetV3)
- [Once-for-All](https://github.com/mit-han-lab/once-for-all)

### Papers & Research
- [Quantization and Training of Neural Networks](https://arxiv.org/abs/1712.05877)
- [Pruning Filters for Efficient ConvNets](https://arxiv.org/abs/1608.08710)
- [Distilling Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)
- [DARTS: Differentiable Architecture Search](https://arxiv.org/abs/1806.09055)
