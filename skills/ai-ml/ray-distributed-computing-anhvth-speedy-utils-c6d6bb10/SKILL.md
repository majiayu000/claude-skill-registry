---
title: Ray - Distributed Computing for AI and Python Applications
description: Comprehensive guide to using Ray for scalable distributed computing, including Ray Core, Data, Train, Tune, Serve, and RLlib with practical examples
category: distributed-systems
tags:
  - ray
  - distributed-computing
  - machine-learning
  - parallel-processing
  - ai-infrastructure
  - reinforcement-learning
  - model-serving
  - hyperparameter-tuning
version: 1.0.0
created: 2026-01-06
---

# Ray - Distributed Computing for AI and Python Applications

## Overview

Ray is an open-source unified framework for scaling AI and Python applications. It provides the compute layer for parallel processing so that you don't need to be a distributed systems expert. Ray minimizes the complexity of running distributed individual workflows and end-to-end machine learning workflows.

### What Ray Provides

- **Scalable libraries** for common machine learning tasks (data preprocessing, distributed training, hyperparameter tuning, reinforcement learning, and model serving)
- **Pythonic distributed computing primitives** for parallelizing and scaling Python applications
- **Integrations and utilities** for deploying on Kubernetes, AWS, GCP, and Azure

## Installation

### Basic Installation
```bash
pip install -U ray
```

### With Specific Libraries
```bash
# Ray Data for data processing
pip install -U "ray[data]"

# Ray Train for distributed training
pip install -U "ray[train]"

# Ray Tune for hyperparameter tuning
pip install -U "ray[tune]"

# Ray Serve for model serving
pip install -U "ray[serve]"

# RLlib for reinforcement learning
pip install -U "ray[rllib]" torch

# All libraries
pip install -U "ray[all]"
```

## Ray Framework Architecture

Ray's unified compute framework consists of three layers:

1. **Ray AI Libraries** – Scalable and unified toolkit for ML applications
2. **Ray Core** – General purpose distributed computing library
3. **Ray Clusters** – Worker nodes connected to a common head node

## 1. Ray Core - Distributed Computing Primitives

### Initializing Ray
```python
import ray

# Initialize Ray
ray.init()

# Or Ray auto-initializes on first remote API call
```

### Tasks - Parallel Functions

Tasks are stateless functions that execute in parallel:

```python
import ray

# Define a remote task
@ray.remote
def square(x):
    return x * x

# Launch four parallel square tasks
futures = [square.remote(i) for i in range(4)]

# Retrieve results
results = ray.get(futures)
print(results)  # [0, 1, 4, 9]
```

### Actors - Stateful Workers

Actors maintain internal state between method calls:

```python
import ray

# Define a Counter actor
@ray.remote
class Counter:
    def __init__(self):
        self.i = 0
    
    def get(self):
        return self.i
    
    def incr(self, value):
        self.i += value

# Create a Counter actor
c = Counter.remote()

# Submit calls to the actor
for _ in range(10):
    c.incr.remote(1)

# Retrieve final actor state
print(ray.get(c.get.remote()))  # 10
```

### Passing Objects

Ray's distributed object store efficiently manages data:

```python
import ray
import numpy as np

# Define a task that sums the values in a matrix
@ray.remote
def sum_matrix(matrix):
    return np.sum(matrix)

# Call with a literal argument
result = ray.get(sum_matrix.remote(np.ones((100, 100))))
print(result)  # 10000.0

# Put a large array into the object store
matrix_ref = ray.put(np.ones((1000, 1000)))

# Call with the object reference
result = ray.get(sum_matrix.remote(matrix_ref))
print(result)  # 1000000.0
```

## 2. Ray Data - Scalable Data Processing for AI

### Overview

Ray Data provides flexible and performant APIs for batch inference, data preprocessing, and data loading for ML training. It features a streaming execution engine for efficiently processing large datasets.

### Basic Usage

```python
import ray
import pandas as pd

class ClassificationModel:
    def __init__(self):
        from transformers import pipeline
        self.pipe = pipeline("text-classification")
    
    def __call__(self, batch: pd.DataFrame):
        results = self.pipe(list(batch["text"]))
        result_df = pd.DataFrame(results)
        return pd.concat([batch, result_df], axis=1)

# Read data
ds = ray.data.read_text("s3://anonymous@ray-example-data/sms_spam_collection_subset.txt")

# Apply batch transformation
ds = ds.map_batches(
    ClassificationModel,
    compute=ray.data.ActorPoolStrategy(size=2),
    batch_size=64,
    batch_format="pandas",
    # num_gpus=1  # Enable for GPU workers
)

# Show results
ds.show(limit=1)
```

### Key Features

- **Faster for deep learning**: Streams data between CPU preprocessing and GPU inference/training
- **Framework friendly**: Integrates with vLLM, PyTorch, HuggingFace, TensorFlow
- **Multi-modal data**: Supports Parquet, Lance, images, JSON, CSV, audio, video
- **Scalable by default**: Runs unchanged from laptop to hundreds of nodes

## 3. Ray Train - Distributed Model Training

### Overview

Ray Train is a scalable machine learning library for distributed training and fine-tuning. It supports PyTorch, PyTorch Lightning, HuggingFace Transformers, TensorFlow, Keras, XGBoost, LightGBM, and more.

### Supported Frameworks

| PyTorch Ecosystem | More Frameworks |
|-------------------|-----------------|
| PyTorch | TensorFlow |
| PyTorch Lightning | Keras |
| Hugging Face Transformers | Horovod |
| Hugging Face Accelerate | XGBoost |
| DeepSpeed | LightGBM |

### Example: Distributed Training

```python
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer

def train_func(config):
    # Your training logic here
    import torch
    import torch.nn as nn
    
    model = nn.Linear(10, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    
    # Training loop
    for epoch in range(10):
        # Training code
        pass

# Configure trainer
trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(
        num_workers=4,
        use_gpu=True
    )
)

# Run training
result = trainer.fit()
```

## 4. Ray Tune - Hyperparameter Tuning

### Overview

Ray Tune is a Python library for experiment execution and hyperparameter tuning at any scale. It supports PyTorch, XGBoost, TensorFlow, Keras, and state-of-the-art algorithms like Population Based Training (PBT) and HyperBand/ASHA.

### Basic Example

```python
from ray import tune

def objective(config):
    # Objective function to minimize
    score = config["a"] ** 2 + config["b"]
    return {"score": score}

# Define search space
search_space = {
    "a": tune.grid_search([0.001, 0.01, 0.1, 1.0]),
    "b": tune.choice([1, 2, 3]),
}

# Create and run tuner
tuner = tune.Tuner(objective, param_space=search_space)
results = tuner.fit()

# Get best result
best_result = results.get_best_result(metric="score", mode="min")
print(best_result.config)
```

### Advanced Features

- **Population Based Training**: Dynamic hyperparameter optimization
- **HyperBand/ASHA**: Early stopping for efficient resource allocation
- **Integration with**: Ax, BayesOpt, BOHB, Nevergrad, Optuna

## 5. Ray Serve - Scalable Model Serving

### Overview

Ray Serve is a scalable model serving library for building online inference APIs. It's framework-agnostic and particularly well-suited for model composition and multi-model serving.

### Basic Deployment

```python
import requests
from starlette.requests import Request
from typing import Dict
from ray import serve

# Define a Ray Serve application
@serve.deployment
class MyModelDeployment:
    def __init__(self, msg: str):
        # Initialize model state
        self._msg = msg
    
    def __call__(self, request: Request) -> Dict:
        return {"result": self._msg}

app = MyModelDeployment.bind(msg="Hello world!")

# Deploy the application locally
serve.run(app, route_prefix="/")

# Query the application
response = requests.get("http://localhost:8000/")
print(response.json())  # {'result': 'Hello world!'}
```

### Model Composition

```python
import requests
import starlette
from typing import Dict
from ray import serve
from ray.serve.handle import DeploymentHandle

@serve.deployment
class Adder:
    def __init__(self, increment: int):
        self.increment = increment
    
    def add(self, inp: int):
        return self.increment + inp

@serve.deployment
class Combiner:
    def average(self, *inputs) -> float:
        return sum(inputs) / len(inputs)

@serve.deployment
class Ingress:
    def __init__(
        self,
        adder1: DeploymentHandle,
        adder2: DeploymentHandle,
        combiner: DeploymentHandle,
    ):
        self._adder1 = adder1
        self._adder2 = adder2
        self._combiner = combiner
    
    async def __call__(self, request: starlette.requests.Request) -> Dict[str, float]:
        input_json = await request.json()
        final_result = await self._combiner.average.remote(
            self._adder1.add.remote(input_json["val"]),
            self._adder2.add.remote(input_json["val"]),
        )
        return {"result": final_result}

# Build and deploy the application
app = Ingress.bind(
    Adder.bind(increment=1),
    Adder.bind(increment=2),
    Combiner.bind()
)
serve.run(app)

# Query the application
response = requests.post("http://localhost:8000/", json={"val": 100.0})
print(response.json())  # {"result": 101.5}
```

## 6. RLlib - Reinforcement Learning

### Overview

RLlib is an open-source library for reinforcement learning, offering support for production-level, highly scalable, and fault-tolerant RL workloads with simple and unified APIs.

### Quick Start Example

```python
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.connectors.env_to_module import FlattenObservations
from pprint import pprint

# Configure the algorithm
config = (
    PPOConfig()
    .environment("Taxi-v3")
    .env_runners(
        num_env_runners=2,
        # Observations are discrete (ints) -> flatten (one-hot) them
        env_to_module_connector=lambda env: FlattenObservations(),
    )
    .evaluation(evaluation_num_env_runners=1)
)

# Build the algorithm
algo = config.build_algo()

# Train for 5 iterations
for _ in range(5):
    pprint(algo.train())

# Evaluate
pprint(algo.evaluate())

# Release resources
algo.stop()
```

### Key Features

- **Scalable and fault-tolerant**: Built on Ray for production workloads
- **Multi-agent RL (MARL)**: Support for multi-agent environments
- **Offline RL**: Train from historical data
- **External environments**: Connect to external simulators

## 7. Ray Clusters - Deployment and Scaling

### Cluster Deployment Options

Ray supports deployment on:

- **Cloud Providers**: AWS, GCP, Azure (via Ray on VMs)
- **Kubernetes**: Via KubeRay project
- **Anyscale**: Fully managed Ray platform
- **On-premise**: Manual deployment

### Cluster Concepts

- **Head Node**: Coordinates the cluster and schedules tasks
- **Worker Nodes**: Execute tasks and actors
- **Autoscaling**: Dynamically adjusts resources based on workload
- **Job Submission**: Deploy applications to existing clusters

## Common Use Cases

### 1. Batch Inference

Process large batches of data through ML models efficiently:

```python
import ray

@ray.remote
class ModelInference:
    def __init__(self):
        # Load model
        self.model = load_model()
    
    def predict(self, batch):
        return self.model.predict(batch)

# Create actors
actors = [ModelInference.remote() for _ in range(4)]

# Distribute work
batches = split_data_into_batches(data)
futures = [actor.predict.remote(batch) for actor, batch in zip(actors, batches)]

# Collect results
results = ray.get(futures)
```

### 2. Distributed Training

```python
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_func(config):
    # Distributed training logic
    pass

trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=8, use_gpu=True)
)
result = trainer.fit()
```

### 3. Hyperparameter Tuning

```python
from ray import tune

def training_function(config):
    # Training with hyperparameters from config
    accuracy = train_model(lr=config["lr"], batch_size=config["batch_size"])
    return {"accuracy": accuracy}

analysis = tune.run(
    training_function,
    config={
        "lr": tune.loguniform(1e-4, 1e-1),
        "batch_size": tune.choice([32, 64, 128])
    },
    num_samples=10
)

best_config = analysis.get_best_config(metric="accuracy", mode="max")
```

### 4. Model Serving

```python
from ray import serve

@serve.deployment
class ModelServer:
    def __init__(self):
        self.model = load_model()
    
    async def __call__(self, request):
        data = await request.json()
        predictions = self.model.predict(data["input"])
        return {"predictions": predictions.tolist()}

serve.run(ModelServer.bind())
```

## Best Practices

### 1. Resource Management

```python
# Specify resources for tasks
@ray.remote(num_cpus=2, num_gpus=1)
def gpu_task(data):
    return process_on_gpu(data)

# Specify resources for actors
@ray.remote(num_cpus=1, num_gpus=0.5)
class Model:
    pass
```

### 2. Object Store Management

```python
# Use ray.put() for large objects
large_data = np.random.rand(1000000)
data_ref = ray.put(large_data)

# Pass reference instead of data
@ray.remote
def process(data_ref):
    data = ray.get(data_ref)
    return compute(data)
```

### 3. Error Handling

```python
import ray

@ray.remote
def may_fail(x):
    if x < 0:
        raise ValueError("Negative input")
    return x * 2

# Handle failures
try:
    result = ray.get(may_fail.remote(-1))
except ray.exceptions.RayTaskError as e:
    print(f"Task failed: {e}")
```

### 4. Monitoring

```python
# Access Ray dashboard
# Default at http://localhost:8265

# Get cluster resources
resources = ray.cluster_resources()
print(resources)

# Get task/actor status
from ray import state
actors = state.list_actors()
tasks = state.list_tasks()
```

## Performance Tips

1. **Batch Operations**: Group small tasks into larger batches to reduce overhead
2. **Object Serialization**: Use NumPy arrays or Arrow tables for efficient serialization
3. **Avoid Returning Large Objects**: Use `ray.put()` and object references
4. **Use Actors for State**: Actors are better than tasks for stateful computations
5. **Configure Resources Properly**: Match task/actor resources to actual needs

## Advanced Features

### Custom Resources

```python
# Start Ray with custom resources
ray.init(resources={"special_hardware": 4})

@ray.remote(resources={"special_hardware": 1})
def specialized_task():
    pass
```

### Placement Groups

```python
from ray.util.placement_group import placement_group

# Create a placement group for co-located tasks
pg = placement_group([{"CPU": 2}, {"CPU": 2}], strategy="STRICT_PACK")

@ray.remote
def task():
    pass

# Schedule tasks in the placement group
ray.get([task.options(placement_group=pg).remote() for _ in range(4)])
```

## Troubleshooting

### Common Issues

1. **Out of Memory**: Reduce batch sizes or use object spilling
2. **Slow Performance**: Check resource utilization and network bandwidth
3. **Task Failures**: Enable retries or implement error handling
4. **Connection Issues**: Verify firewall settings and network configuration

### Debugging

```python
# Enable verbose logging
ray.init(logging_level="debug")

# Use ray.timeline() for performance analysis
ray.timeline(filename="timeline.json")
```

## Resources

- **Documentation**: https://docs.ray.io/
- **GitHub**: https://github.com/ray-project/ray
- **Community**: https://discuss.ray.io/
- **Slack**: https://www.ray.io/join-slack
- **Examples**: https://docs.ray.io/en/latest/ray-overview/examples.html

## Example Projects

### Complete ML Pipeline

```python
import ray
from ray import tune, serve
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

# 1. Data preprocessing with Ray Data
ds = ray.data.read_parquet("s3://bucket/data.parquet")
ds = ds.map_batches(preprocess_function)

# 2. Model training with Ray Train
def train_func(config):
    # Training logic
    pass

trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True)
)
result = trainer.fit()

# 3. Hyperparameter tuning with Ray Tune
tuner = tune.Tuner(
    trainer,
    param_space={"train_loop_config": {"lr": tune.loguniform(1e-4, 1e-1)}}
)
tuning_results = tuner.fit()

# 4. Model serving with Ray Serve
@serve.deployment
class PredictionService:
    def __init__(self):
        self.model = load_best_model(tuning_results)
    
    async def __call__(self, request):
        data = await request.json()
        return {"prediction": self.model.predict(data)}

serve.run(PredictionService.bind())
```

## Conclusion

Ray provides a comprehensive framework for distributed computing and AI workloads. Its unified API makes it easy to:

- **Scale Python applications** from laptop to cluster
- **Build end-to-end ML pipelines** with integrated libraries
- **Deploy production-grade ML services** with minimal code changes
- **Handle complex distributed systems** without expert knowledge

Start with Ray Core for general distributed computing, then leverage specialized libraries (Data, Train, Tune, Serve, RLlib) for ML-specific workloads.
