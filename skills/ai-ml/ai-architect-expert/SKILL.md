---
name: ai-architect-expert
version: 1.0.0
description: Expert-level AI system design, MLOps, architecture patterns, and AI infrastructure
category: ai
tags: [ai-architecture, mlops, system-design, ai-infrastructure, scalability]
allowed-tools:
  - Read
  - Write
  - Edit
---

# AI Architect Expert

Expert guidance for designing AI systems, MLOps architecture, scalable ML infrastructure, and AI platform engineering.

## Core Concepts

### AI System Architecture
- Model serving architectures
- Real-time vs batch inference
- Feature stores
- Model registries
- Training pipelines
- Data versioning

### MLOps Infrastructure
- CI/CD for ML
- Model monitoring and observability
- A/B testing frameworks
- Model retraining automation
- Resource orchestration
- Cost optimization

### Scalability Patterns
- Distributed training
- Model parallelism
- Data parallelism
- Inference optimization
- Caching strategies
- Load balancing

## ML Platform Architecture

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class ModelStage(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"

@dataclass
class ModelMetadata:
    name: str
    version: str
    framework: str
    stage: ModelStage
    metrics: Dict[str, float]
    created_at: str
    updated_at: str

class ModelRegistry:
    """Central model registry for ML platform"""

    def __init__(self):
        self.models: Dict[str, List[ModelMetadata]] = {}

    def register_model(self, model: ModelMetadata) -> str:
        """Register new model version"""
        if model.name not in self.models:
            self.models[model.name] = []

        self.models[model.name].append(model)
        return f"{model.name}:{model.version}"

    def promote_model(self, name: str, version: str, stage: ModelStage):
        """Promote model to different stage"""
        for model in self.models.get(name, []):
            if model.version == version:
                model.stage = stage
                return True
        return False

    def get_production_model(self, name: str) -> Optional[ModelMetadata]:
        """Get current production model"""
        for model in self.models.get(name, []):
            if model.stage == ModelStage.PRODUCTION:
                return model
        return None

class FeatureStore:
    """Feature store for ML features"""

    def __init__(self):
        self.features: Dict[str, Dict] = {}
        self.feature_groups: Dict[str, List[str]] = {}

    def register_feature(self, name: str, dtype: str, description: str,
                        transformation: Optional[str] = None):
        """Register feature definition"""
        self.features[name] = {
            "dtype": dtype,
            "description": description,
            "transformation": transformation
        }

    def create_feature_group(self, group_name: str, feature_names: List[str]):
        """Create feature group for reuse"""
        self.feature_groups[group_name] = feature_names

    def get_features(self, entity_id: str, feature_names: List[str]) -> Dict:
        """Retrieve feature values for entity"""
        # In production, this would query online/offline stores
        return {name: self._fetch_feature(entity_id, name)
                for name in feature_names}
```

## Training Pipeline Architecture

```python
from abc import ABC, abstractmethod
import torch.distributed as dist

class TrainingPipeline(ABC):
    """Base training pipeline"""

    def __init__(self, config: Dict):
        self.config = config
        self.experiment_tracker = None
        self.checkpointer = None

    @abstractmethod
    def prepare_data(self):
        """Data preparation step"""
        pass

    @abstractmethod
    def train(self):
        """Training step"""
        pass

    @abstractmethod
    def evaluate(self):
        """Evaluation step"""
        pass

    def run(self):
        """Execute full pipeline"""
        self.prepare_data()
        self.train()
        metrics = self.evaluate()
        self.log_metrics(metrics)
        return metrics

class DistributedTrainingPipeline(TrainingPipeline):
    """Distributed training with DDP"""

    def __init__(self, config: Dict, world_size: int, rank: int):
        super().__init__(config)
        self.world_size = world_size
        self.rank = rank
        self.setup_distributed()

    def setup_distributed(self):
        """Initialize distributed training"""
        dist.init_process_group(
            backend='nccl',
            world_size=self.world_size,
            rank=self.rank
        )

    def prepare_data(self):
        """Distribute data across workers"""
        from torch.utils.data.distributed import DistributedSampler

        self.sampler = DistributedSampler(
            self.dataset,
            num_replicas=self.world_size,
            rank=self.rank
        )

    def train(self):
        """Distributed training loop"""
        from torch.nn.parallel import DistributedDataParallel as DDP

        model = DDP(self.model, device_ids=[self.rank])

        for epoch in range(self.config['epochs']):
            self.sampler.set_epoch(epoch)

            for batch in self.dataloader:
                loss = self.train_step(model, batch)

                if self.rank == 0:
                    self.log_loss(loss)
```

## Model Serving Architecture

```python
from fastapi import FastAPI, BackgroundTasks
from prometheus_client import Counter, Histogram
import asyncio

# Metrics
prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')

class ModelServer:
    """Production model serving"""

    def __init__(self, model_registry: ModelRegistry):
        self.registry = model_registry
        self.loaded_models = {}
        self.prediction_cache = {}

    async def load_model(self, name: str, version: str = "production"):
        """Load model into memory"""
        if version == "production":
            model_metadata = self.registry.get_production_model(name)
        else:
            model_metadata = self.registry.get_model(name, version)

        if not model_metadata:
            raise ValueError(f"Model {name}:{version} not found")

        # Load model from storage
        model = await self._load_from_storage(model_metadata)
        self.loaded_models[f"{name}:{version}"] = model

        return model

    @prediction_latency.time()
    async def predict(self, model_name: str, features: Dict) -> Dict:
        """Make prediction with caching"""
        prediction_counter.inc()

        # Check cache
        cache_key = self._generate_cache_key(model_name, features)
        if cache_key in self.prediction_cache:
            return self.prediction_cache[cache_key]

        # Get model
        model = self.loaded_models.get(model_name)
        if not model:
            model = await self.load_model(model_name)

        # Predict
        result = await self._run_inference(model, features)

        # Cache result
        self.prediction_cache[cache_key] = result

        return result

    async def predict_batch(self, model_name: str,
                           batch_features: List[Dict]) -> List[Dict]:
        """Batch prediction for efficiency"""
        tasks = [self.predict(model_name, features)
                for features in batch_features]
        return await asyncio.gather(*tasks)

app = FastAPI()
model_server = ModelServer(model_registry=ModelRegistry())

@app.post("/predict/{model_name}")
async def predict_endpoint(model_name: str, features: Dict):
    return await model_server.predict(model_name, features)
```

## Monitoring and Observability

```python
from dataclasses import dataclass
from datetime import datetime
import numpy as np

@dataclass
class PredictionLog:
    timestamp: datetime
    model_name: str
    model_version: str
    features: Dict
    prediction: any
    latency_ms: float
    input_hash: str

class ModelMonitor:
    """Monitor model performance in production"""

    def __init__(self):
        self.logs: List[PredictionLog] = []
        self.metrics = {}

    def log_prediction(self, log: PredictionLog):
        """Log prediction for monitoring"""
        self.logs.append(log)

        # Update metrics
        self.update_latency_metrics(log)
        self.check_data_drift(log)

    def update_latency_metrics(self, log: PredictionLog):
        """Track prediction latency"""
        model_key = f"{log.model_name}:{log.model_version}"

        if model_key not in self.metrics:
            self.metrics[model_key] = {
                "latencies": [],
                "predictions": 0
            }

        self.metrics[model_key]["latencies"].append(log.latency_ms)
        self.metrics[model_key]["predictions"] += 1

    def check_data_drift(self, log: PredictionLog):
        """Detect data drift in input features"""
        # Compare current feature distributions with training data
        # Alert if significant drift detected
        pass

    def get_model_health(self, model_name: str) -> Dict:
        """Get model health metrics"""
        model_metrics = self.metrics.get(model_name, {})

        latencies = model_metrics.get("latencies", [])

        return {
            "total_predictions": model_metrics.get("predictions", 0),
            "avg_latency_ms": np.mean(latencies) if latencies else 0,
            "p95_latency_ms": np.percentile(latencies, 95) if latencies else 0,
            "p99_latency_ms": np.percentile(latencies, 99) if latencies else 0
        }
```

## Best Practices

### Architecture Design
- Separate training and serving infrastructure
- Use feature stores for consistency
- Implement model versioning from day one
- Design for horizontal scalability
- Plan for model rollback capability
- Build monitoring into the architecture

### MLOps
- Automate model retraining pipelines
- Implement CI/CD for models
- Version everything (data, code, models)
- Monitor model performance metrics
- Track data drift and model decay
- Implement gradual rollout (canary/blue-green)

### Infrastructure
- Use GPU efficiently (batching, mixed precision)
- Implement caching for repeated predictions
- Consider model compression (quantization, pruning)
- Plan for disaster recovery
- Optimize costs (spot instances, autoscaling)
- Use managed services where appropriate

## Anti-Patterns

❌ No model versioning or registry
❌ Training and serving environment mismatch
❌ No monitoring or alerting
❌ Manual model deployment process
❌ Ignoring data drift
❌ No rollback strategy
❌ Over-engineering for initial MVP

## Resources

- MLflow: https://mlflow.org/
- Kubeflow: https://www.kubeflow.org/
- Seldon Core: https://www.seldon.io/
- BentoML: https://www.bentoml.com/
- Weights & Biases: https://wandb.ai/
