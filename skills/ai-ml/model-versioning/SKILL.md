---
name: Model Versioning
description: Comprehensive guide for ML model versioning and management strategies, including model registries, metadata tracking, and deployment workflows.
---

# Model Versioning

## Overview

Model versioning is the practice of tracking and managing different versions of machine learning models throughout their lifecycle. This skill covers versioning strategies, model registries, metadata management, lineage tracking, artifact storage, promotion workflows, A/B testing, and model comparison tools.

## Prerequisites

- Understanding of machine learning model development
- Knowledge of Git and version control systems
- Familiarity with model deployment concepts
- Understanding of data pipelines and workflows
- Basic knowledge of database systems

## Key Concepts

### Versioning Strategies

- **Semantic Versioning**: MAJOR.MINOR.PATCH format for tracking changes
- **Timestamp-Based Versioning**: Using timestamps for unique version identifiers
- **Git-Based Versioning**: Leveraging git commits and tags for versioning

### Model Registry

- **Centralized Storage**: Single source of truth for model versions
- **Stage Management**: Development, Staging, Production, Archived stages
- **Metadata Tracking**: Comprehensive model information storage
- **Model Loading**: Retrieving models by version or stage

### Metadata Management

- **Model Metadata Schema**: Structured information about models
- **Metadata Store**: Database for storing and querying metadata
- **Lineage Tracking**: Tracking model relationships and data sources
- **Artifact Storage**: Managing model files and related artifacts

### Deployment Workflows

- **Promotion Pipeline**: Moving models through stages
- **Rollback Strategy**: Reverting to previous versions
- **A/B Testing**: Comparing model versions in production
- **Model Comparison**: Analyzing performance across versions

## Implementation Guide

### Versioning Strategies

#### Semantic Versioning

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ModelVersion:
    """Model version using semantic versioning."""
    major: int
    minor: int
    patch: int
    pre_release: Optional[str] = None
    build_metadata: Optional[str] = None

    def __str__(self):
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            version += f"-{self.pre_release}"
        if self.build_metadata:
            version += f"+{self.build_metadata}"
        return version

    @staticmethod
    def parse(version_string: str) -> 'ModelVersion':
        """Parse version string."""
        # Parse semantic version
        parts = version_string.split('+')
        version = parts[0]
        build = parts[1] if len(parts) > 1 else None

        parts = version.split('-')
        version = parts[0]
        pre = parts[1] if len(parts) > 1 else None

        major, minor, patch = map(int, version.split('.'))

        return ModelVersion(major, minor, patch, pre, build)

    def increment_major(self):
        """Increment major version (breaking changes)."""
        return ModelVersion(self.major + 1, 0, 0)

    def increment_minor(self):
        """Increment minor version (new features)."""
        return ModelVersion(self.major, self.minor + 1, 0)

    def increment_patch(self):
        """Increment patch version (bug fixes)."""
        return ModelVersion(self.major, self.minor, self.patch + 1)

# Usage
v1 = ModelVersion(1, 0, 0)
print(v1)  # 1.0.0

v2 = v1.increment_minor()
print(v2)  # 1.1.0

v3 = ModelVersion.parse("2.1.3-beta+build123")
print(v3)  # 2.1.3-beta+build123
```

#### Timestamp-Based Versioning

```python
from datetime import datetime
import pytz

class TimestampVersion:
    """Timestamp-based versioning."""

    def __init__(self, timezone='UTC'):
        self.timezone = pytz.timezone(timezone)

    def generate(self) -> str:
        """Generate timestamp-based version."""
        now = datetime.now(self.timezone)
        return now.strftime("%Y%m%d-%H%M%S")

    def generate_with_microseconds(self) -> str:
        """Generate version with microseconds."""
        now = datetime.now(self.timezone)
        return now.strftime("%Y%m%d-%H%M%S-%f")

    def parse(self, version_string: str) -> datetime:
        """Parse timestamp version."""
        # Handle both formats
        if '-' in version_string and version_string.count('-') == 2:
            # With microseconds
            dt_str = version_string.replace('-', '')
            dt_str = dt_str[:-6] + '.' + dt_str[-6:]
        else:
            # Without microseconds
            dt_str = version_string.replace('-', '')

        return datetime.strptime(dt_str, "%Y%m%d%H%M%S")

# Usage
versioner = TimestampVersion()
version = versioner.generate()
print(version)  # 20240114-123045

version_micro = versioner.generate_with_microseconds()
print(version_micro)  # 20240114-123045-123456
```

#### Git-Based Versioning

```python
import subprocess
from typing import Optional

class GitVersion:
    """Git-based versioning."""

    @staticmethod
    def get_commit_hash(short: bool = True) -> Optional[str]:
        """Get current commit hash."""
        try:
            length = 7 if short else None
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            commit_hash = result.stdout.strip()
            return commit_hash[:length] if short else commit_hash
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def get_branch() -> Optional[str]:
        """Get current branch name."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def get_tag() -> Optional[str]:
        """Get current tag."""
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--exact-match'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def generate_version() -> str:
        """Generate version from git info."""
        tag = GitVersion.get_tag()
        if tag:
            return tag

        branch = GitVersion.get_branch()
        commit = GitVersion.get_commit_hash(short=True)

        if branch and commit:
            return f"{branch}-{commit}"
        elif commit:
            return commit
        else:
            return "unknown"

# Usage
version = GitVersion.generate_version()
print(version)  # main-abc1234 or v1.0.0
```

### Model Registry

#### MLflow Model Registry

```python
import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient
from typing import Dict, Any

class MLflowModelRegistry:
    """MLflow model registry wrapper."""

    def __init__(self, tracking_uri: str = None):
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

        self.client = MlflowClient()

    def register_model(
        self,
        model,
        model_name: str,
        version: str,
        description: str = None,
        tags: Dict[str, Any] = None,
        metrics: Dict[str, float] = None
    ):
        """Register model to MLflow."""
        with mlflow.start_run():
            # Log model
            mlflow.pytorch.log_model(model, "model")

            # Log parameters
            if tags:
                mlflow.set_tags(tags)

            # Log metrics
            if metrics:
                mlflow.log_metrics(metrics)

            # Register model
            model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
            registered_model = mlflow.register_model(
                model_uri,
                model_name,
                tags={"version": version}
            )

            # Update description
            if description:
                self.client.update_model_version(
                    name=model_name,
                    version=registered_model.version,
                    description=description
                )

        return registered_model

    def get_model_version(self, model_name: str, version: str = None):
        """Get model version from registry."""
        if version:
            return self.client.get_model_version(model_name, version)
        else:
            # Get latest version
            latest = self.client.get_latest_versions(model_name, stages=["Production"])
            return latest[0] if latest else None

    def load_model(self, model_name: str, version: str = None, stage: str = None):
        """Load model from registry."""
        if stage:
            model_uri = f"models:/{model_name}/{stage}"
        elif version:
            model_uri = f"models:/{model_name}/{version}"
        else:
            model_uri = f"models:/{model_name}/Production"

        return mlflow.pytorch.load_model(model_uri)

    def transition_stage(
        self,
        model_name: str,
        version: str,
        stage: str,
        archive_existing_versions: bool = False
    ):
        """Transition model to a new stage."""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
            archive_existing_versions=archive_existing_versions
        )

    def list_models(self, name_filter: str = None):
        """List all registered models."""
        models = self.client.search_registered_models(filter_string=name_filter)
        return models

    def get_model_history(self, model_name: str):
        """Get version history for a model."""
        versions = self.client.get_model_version_stages(model_name)
        return versions

# Usage
registry = MLflowModelRegistry(tracking_uri="http://localhost:5000")

# Register model
registered = registry.register_model(
    model=my_model,
    model_name="image_classifier",
    version="1.0.0",
    description="Initial model release",
    tags={"framework": "pytorch", "task": "classification"},
    metrics={"accuracy": 0.95, "f1": 0.94}
)

# Transition to production
registry.transition_stage("image_classifier", "1", "Production")

# Load model from production
model = registry.load_model("image_classifier", stage="Production")
```

#### Custom Model Registry

```python
import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import pickle
import torch

class ModelRegistry:
    """Custom model registry."""

    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.registry_path / "index.json"
        self._load_index()

    def _load_index(self):
        """Load model index."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {"models": {}}

    def _save_index(self):
        """Save model index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def _compute_hash(self, file_path: Path) -> str:
        """Compute file hash."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def register(
        self,
        model,
        model_name: str,
        version: str,
        metadata: Dict = None,
        metrics: Dict = None,
        artifacts: Dict = None
    ):
        """Register model."""
        model_path = self.registry_path / model_name / version
        model_path.mkdir(parents=True, exist_ok=True)

        # Save model
        model_file = model_path / "model.pth"
        torch.save(model.state_dict(), model_file)
        model_hash = self._compute_hash(model_file)

        # Save metadata
        metadata = metadata or {}
        metadata.update({
            "version": version,
            "registered_at": datetime.now().isoformat(),
            "model_hash": model_hash,
            "model_path": str(model_file),
            "metrics": metrics or {}
        })

        metadata_file = model_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        # Save artifacts
        if artifacts:
            artifacts_dir = model_path / "artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            for name, artifact in artifacts.items():
                artifact_path = artifacts_dir / name
                if isinstance(artifact, (dict, list)):
                    with open(artifact_path.with_suffix('.json'), 'w') as f:
                        json.dump(artifact, f, indent=2)
                else:
                    with open(artifact_path, 'wb') as f:
                        pickle.dump(artifact, f)

        # Update index
        if model_name not in self.index["models"]:
            self.index["models"][model_name] = {"versions": []}

        self.index["models"][model_name]["versions"].append({
            "version": version,
            "registered_at": metadata["registered_at"],
            "metrics": metrics or {},
            "stage": "Development"
        })

        self._save_index()

        return model_path

    def load(self, model_name: str, version: str = None, stage: str = None):
        """Load model."""
        if version:
            model_path = self.registry_path / model_name / version
        elif stage:
            # Find version with specified stage
            versions = self.index["models"].get(model_name, {}).get("versions", [])
            version_info = next((v for v in versions if v["stage"] == stage), None)
            if not version_info:
                raise ValueError(f"No version found with stage {stage}")
            model_path = self.registry_path / model_name / version_info["version"]
        else:
            # Get latest version
            versions = self.index["models"].get(model_name, {}).get("versions", [])
            if not versions:
                raise ValueError(f"No versions found for {model_name}")
            latest = sorted(versions, key=lambda x: x["registered_at"])[-1]
            model_path = self.registry_path / model_name / latest["version"]

        # Load metadata
        metadata_file = model_path / "metadata.json"
        with open(metadata_file) as f:
            metadata = json.load(f)

        # Load model
        model_file = model_path / "model.pth"
        # Assuming model class is known
        model = MyModel()  # Replace with actual model class
        model.load_state_dict(torch.load(model_file))
        model.eval()

        return model, metadata

    def transition_stage(self, model_name: str, version: str, stage: str):
        """Transition model to a new stage."""
        versions = self.index["models"].get(model_name, {}).get("versions", [])
        for v in versions:
            if v["version"] == version:
                v["stage"] = stage
                break

        self._save_index()

    def list_versions(self, model_name: str):
        """List all versions of a model."""
        return self.index["models"].get(model_name, {}).get("versions", [])

    def list_models(self):
        """List all registered models."""
        return list(self.index["models"].keys())

# Usage
registry = ModelRegistry("./model_registry")

# Register model
registry.register(
    model=my_model,
    model_name="image_classifier",
    version="1.0.0",
    metadata={"framework": "pytorch", "task": "classification"},
    metrics={"accuracy": 0.95, "f1": 0.94}
)

# Transition to production
registry.transition_stage("image_classifier", "1.0.0", "Production")

# Load model
model, metadata = registry.load("image_classifier", stage="Production")
```

### Metadata Management

#### Model Metadata Schema

```python
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json

class ModelStage(Enum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

@dataclass
class ModelMetadata:
    """Comprehensive model metadata."""
    # Basic info
    model_name: str
    version: str
    framework: str
    task: str

    # Training info
    training_data_version: str
    training_start: str
    training_end: str
    training_duration_seconds: float

    # Architecture
    architecture: str
    parameters: int
    model_size_mb: float

    # Performance
    metrics: Dict[str, float]
    test_set: str

    # Deployment
    stage: ModelStage
    deployed_at: Optional[str] = None
    deployment_environment: Optional[str] = None

    # Additional
    tags: List[str] = None
    description: str = ""
    git_commit: Optional[str] = None
    git_branch: Optional[str] = None

    # Lineage
    parent_model: Optional[str] = None
    parent_version: Optional[str] = None
    data_sources: List[str] = None

    # Compliance
    data_retention_days: int = 365
    pii_present: bool = False
    gdpr_compliant: bool = True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['stage'] = self.stage.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'ModelMetadata':
        """Create from dictionary."""
        if 'stage' in data and isinstance(data['stage'], str):
            data['stage'] = ModelStage(data['stage'])
        return cls(**data)

    def to_json(self) -> str:
        """Convert to JSON."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'ModelMetadata':
        """Create from JSON."""
        data = json.loads(json_str)
        return cls.from_dict(data)

# Usage
metadata = ModelMetadata(
    model_name="image_classifier",
    version="1.0.0",
    framework="pytorch",
    task="classification",
    training_data_version="v1.0",
    training_start="2024-01-01T00:00:00",
    training_end="2024-01-02T12:00:00",
    training_duration_seconds=86400.0,
    architecture="resnet50",
    parameters=25600000,
    model_size_mb=98.5,
    metrics={"accuracy": 0.95, "f1": 0.94, "precision": 0.93, "recall": 0.95},
    test_set="test_v1.0",
    stage=ModelStage.PRODUCTION,
    tags=["vision", "classification", "production"],
    description="Initial production model",
    git_commit="abc1234",
    git_branch="main",
    data_sources=["imagenet", "custom_dataset"],
    data_retention_days=730,
    pii_present=False,
    gdpr_compliant=True
)

# Save metadata
with open("model_metadata.json", "w") as f:
    f.write(metadata.to_json())
```

#### Metadata Store

```python
import sqlite3
from typing import List, Optional, Dict
from pathlib import Path

class MetadataStore:
    """SQLite-based metadata store."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                version TEXT NOT NULL,
                framework TEXT NOT NULL,
                task TEXT NOT NULL,
                training_data_version TEXT,
                training_start TEXT,
                training_end TEXT,
                architecture TEXT,
                parameters INTEGER,
                model_size_mb REAL,
                stage TEXT NOT NULL,
                deployed_at TEXT,
                deployment_environment TEXT,
                tags TEXT,
                description TEXT,
                git_commit TEXT,
                git_branch TEXT,
                parent_model TEXT,
                parent_version TEXT,
                data_sources TEXT,
                data_retention_days INTEGER DEFAULT 365,
                pii_present INTEGER DEFAULT 0,
                gdpr_compliant INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(model_name, version)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                FOREIGN KEY (model_id) REFERENCES models (id)
            )
        """)

        conn.commit()
        conn.close()

    def save_metadata(self, metadata: ModelMetadata) -> int:
        """Save model metadata."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Insert model
        cursor.execute("""
            INSERT INTO models (
                model_name, version, framework, task,
                training_data_version, training_start, training_end,
                architecture, parameters, model_size_mb,
                stage, deployed_at, deployment_environment,
                tags, description, git_commit, git_branch,
                parent_model, parent_version, data_sources,
                data_retention_days, pii_present, gdpr_compliant
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metadata.model_name, metadata.version, metadata.framework, metadata.task,
            metadata.training_data_version, metadata.training_start, metadata.training_end,
            metadata.architecture, metadata.parameters, metadata.model_size_mb,
            metadata.stage.value, metadata.deployed_at, metadata.deployment_environment,
            json.dumps(metadata.tags or []), metadata.description, metadata.git_commit, metadata.git_branch,
            metadata.parent_model, metadata.parent_version, json.dumps(metadata.data_sources or []),
            metadata.data_retention_days, 1 if metadata.pii_present else 0, 1 if metadata.gdpr_compliant else 0
        ))

        model_id = cursor.lastrowid

        # Insert metrics
        for metric_name, metric_value in metadata.metrics.items():
            cursor.execute("""
                INSERT INTO metrics (model_id, metric_name, metric_value)
                VALUES (?, ?, ?)
            """, (model_id, metric_name, metric_value))

        conn.commit()
        conn.close()

        return model_id

    def get_metadata(self, model_name: str, version: str) -> Optional[ModelMetadata]:
        """Get model metadata."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM models WHERE model_name = ? AND version = ?
        """, (model_name, version))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        # Get metrics
        cursor.execute("""
            SELECT metric_name, metric_value FROM metrics WHERE model_id = ?
        """, (row[0],))

        metrics = {metric_name: metric_value for metric_name, metric_value in cursor.fetchall()}
        conn.close()

        # Build metadata
        return ModelMetadata(
            model_name=row[1],
            version=row[2],
            framework=row[3],
            task=row[4],
            training_data_version=row[5],
            training_start=row[6],
            training_end=row[7],
            training_duration_seconds=0,  # Not stored
            architecture=row[8],
            parameters=row[9],
            model_size_mb=row[10],
            stage=ModelStage(row[11]),
            deployed_at=row[12],
            deployment_environment=row[13],
            tags=json.loads(row[14]),
            description=row[15],
            git_commit=row[16],
            git_branch=row[17],
            parent_model=row[18],
            parent_version=row[19],
            data_sources=json.loads(row[20]),
            data_retention_days=row[21],
            pii_present=bool(row[22]),
            gdpr_compliant=bool(row[23]),
            metrics=metrics
        )

    def list_models(self, stage: ModelStage = None) -> List[Dict]:
        """List all models."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if stage:
            cursor.execute("""
                SELECT model_name, version, stage, deployed_at FROM models WHERE stage = ?
            """, (stage.value,))
        else:
            cursor.execute("""
                SELECT model_name, version, stage, deployed_at FROM models
            """)

        models = [
            {"model_name": row[0], "version": row[1], "stage": row[2], "deployed_at": row[3]}
            for row in cursor.fetchall()
        ]

        conn.close()
        return models

# Usage
store = MetadataStore("./model_metadata.db")
store.save_metadata(metadata)

# Get metadata
metadata = store.get_metadata("image_classifier", "1.0.0")

# List production models
production_models = store.list_models(stage=ModelStage.PRODUCTION)
```

### Model Lineage Tracking

#### Lineage Graph

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class ModelNode:
    """Node in model lineage graph."""
    model_name: str
    version: str
    node_type: str  # "model", "data", "experiment"

class ModelLineage:
    """Track model lineage."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_model(
        self,
        model_name: str,
        version: str,
        parent_model: Optional[str] = None,
        parent_version: Optional[str] = None,
        data_sources: Optional[List[str]] = None
    ):
        """Add model to lineage."""
        node_id = f"{model_name}:{version}"
        self.graph.add_node(node_id, model_name=model_name, version=version, node_type="model")

        # Add parent edge
        if parent_model and parent_version:
            parent_id = f"{parent_model}:{parent_version}"
            self.graph.add_edge(parent_id, node_id, relation="derived_from")

        # Add data source edges
        if data_sources:
            for data_source in data_sources:
                self.graph.add_node(data_source, node_type="data")
                self.graph.add_edge(data_source, node_id, relation="trained_on")

    def add_experiment(
        self,
        experiment_id: str,
        model_name: str,
        version: str,
        hyperparameters: Dict
    ):
        """Add experiment to lineage."""
        node_id = f"{model_name}:{version}"
        exp_id = f"experiment:{experiment_id}"

        self.graph.add_node(exp_id, node_type="experiment", hyperparameters=hyperparameters)
        self.graph.add_edge(exp_id, node_id, relation="produced")

    def get_ancestors(self, model_name: str, version: str) -> List[Dict]:
        """Get all ancestor models."""
        node_id = f"{model_name}:{version}"
        ancestors = nx.ancestors(self.graph, node_id)

        result = []
        for ancestor_id in ancestors:
            node = self.graph.nodes[ancestor_id]
            result.append({
                "id": ancestor_id,
                "type": node.get("node_type"),
                "data": node
            })

        return result

    def get_descendants(self, model_name: str, version: str) -> List[Dict]:
        """Get all descendant models."""
        node_id = f"{model_name}:{version}"
        descendants = nx.descendants(self.graph, node_id)

        result = []
        for descendant_id in descendants:
            node = self.graph.nodes[descendant_id]
            result.append({
                "id": descendant_id,
                "type": node.get("node_type"),
                "data": node
            })

        return result

    def visualize(self, output_path: str = None):
        """Visualize lineage graph."""
        pos = nx.spring_layout(self.graph)

        # Color nodes by type
        colors = []
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get("node_type", "model")
            if node_type == "model":
                colors.append("lightblue")
            elif node_type == "data":
                colors.append("lightgreen")
            else:
                colors.append("lightyellow")

        plt.figure(figsize=(12, 8))
        nx.draw(self.graph, pos, node_color=colors, with_labels=True, node_size=1000, font_size=8)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='lightblue', label='Model'),
            Patch(facecolor='lightgreen', label='Data'),
            Patch(facecolor='lightyellow', label='Experiment')
        ]
        plt.legend(handles=legend_elements)

        plt.title("Model Lineage")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
        else:
            plt.show()

# Usage
lineage = ModelLineage()

lineage.add_model("base_model", "1.0.0", data_sources=["dataset_v1"])
lineage.add_model("fine_tuned", "1.0.0", parent_model="base_model", parent_version="1.0.0",
                    data_sources=["dataset_v2"])
lineage.add_model("production", "1.0.0", parent_model="fine_tuned", parent_version="1.0.0")

# Get lineage
ancestors = lineage.get_ancestors("production", "1.0.0")
descendants = lineage.get_descendants("base_model", "1.0.0")

# Visualize
lineage.visualize("lineage.png")
```

### Artifact Storage

#### Artifact Manager

```python
import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

class ArtifactManager:
    """Manage model artifacts."""

    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_path / "artifacts.json"
        self._load_index()

    def _load_index(self):
        """Load artifact index."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {"artifacts": {}}

    def _save_index(self):
        """Save artifact index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def _compute_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def store(
        self,
        source_path: str,
        artifact_name: str,
        version: str,
        metadata: Dict = None
    ) -> str:
        """Store artifact."""
        source_path = Path(source_path)
        artifact_hash = self._compute_hash(source_path)

        # Create storage path
        storage_dir = self.storage_path / artifact_name / version
        storage_dir.mkdir(parents=True, exist_ok=True)

        # Copy artifact
        artifact_path = storage_dir / source_path.name
        shutil.copy2(source_path, artifact_path)

        # Store metadata
        artifact_metadata = {
            "name": artifact_name,
            "version": version,
            "hash": artifact_hash,
            "size_bytes": source_path.stat().st_size,
            "stored_at": datetime.now().isoformat(),
            "path": str(artifact_path),
            "metadata": metadata or {}
        }

        # Update index
        key = f"{artifact_name}:{version}"
        self.index["artifacts"][key] = artifact_metadata
        self._save_index()

        return str(artifact_path)

    def retrieve(self, artifact_name: str, version: str, destination: str = None) -> Path:
        """Retrieve artifact."""
        key = f"{artifact_name}:{version}"

        if key not in self.index["artifacts"]:
            raise ValueError(f"Artifact {key} not found")

        artifact_info = self.index["artifacts"][key]
        artifact_path = Path(artifact_info["path"])

        if destination:
            dest_path = Path(destination)
            shutil.copy2(artifact_path, dest_path)
            return dest_path

        return artifact_path

    def list_artifacts(self, artifact_name: str = None) -> List[Dict]:
        """List artifacts."""
        if artifact_name:
            return [
                v for k, v in self.index["artifacts"].items()
                if k.startswith(f"{artifact_name}:")
            ]
        return list(self.index["artifacts"].values())

    def delete(self, artifact_name: str, version: str):
        """Delete artifact."""
        key = f"{artifact_name}:{version}"

        if key not in self.index["artifacts"]:
            raise ValueError(f"Artifact {key} not found")

        artifact_info = self.index["artifacts"][key]
        artifact_path = Path(artifact_info["path"])

        # Delete file
        if artifact_path.exists():
            artifact_path.unlink()

        # Delete empty directories
        artifact_path.parent.rmdir()
        if artifact_path.parent.parent.name == artifact_name:
            artifact_path.parent.parent.rmdir()

        # Update index
        del self.index["artifacts"][key]
        self._save_index()

# Usage
manager = ArtifactManager("./artifacts")

# Store artifact
manager.store(
    source_path="model.pth",
    artifact_name="image_classifier",
    version="1.0.0",
    metadata={"framework": "pytorch", "task": "classification"}
)

# Retrieve artifact
artifact_path = manager.retrieve("image_classifier", "1.0.0", destination="./downloaded_model.pth")
```

### Model Promotion Workflow

#### Promotion Pipeline

```python
from enum import Enum
from typing import Callable, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromotionStage(Enum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

class ModelPromotionPipeline:
    """Manage model promotion through stages."""

    def __init__(self, registry):
        self.registry = registry
        self.pre_promotion_hooks = {}
        self.post_promotion_hooks = {}

    def register_pre_hook(self, stage: PromotionStage, hook: Callable):
        """Register pre-promotion hook."""
        if stage not in self.pre_promotion_hooks:
            self.pre_promotion_hooks[stage] = []
        self.pre_promotion_hooks[stage].append(hook)

    def register_post_hook(self, stage: PromotionStage, hook: Callable):
        """Register post-promotion hook."""
        if stage not in self.post_promotion_hooks:
            self.post_promotion_hooks[stage] = []
        self.post_promotion_hooks[stage].append(hook)

    def promote(
        self,
        model_name: str,
        version: str,
        from_stage: PromotionStage,
        to_stage: PromotionStage,
        force: bool = False
    ):
        """Promote model to next stage."""
        logger.info(f"Promoting {model_name}:{version} from {from_stage} to {to_stage}")

        # Run pre-promotion hooks
        if to_stage in self.pre_promotion_hooks:
            for hook in self.pre_promotion_hooks[to_stage]:
                hook(model_name, version, from_stage, to_stage)

        # Validation checks
        if not force and to_stage == PromotionStage.PRODUCTION:
            self._validate_for_production(model_name, version)

        # Perform promotion
        self.registry.transition_stage(model_name, version, to_stage.value)

        logger.info(f"Successfully promoted {model_name}:{version} to {to_stage}")

        # Run post-promotion hooks
        if to_stage in self.post_promotion_hooks:
            for hook in self.post_promotion_hooks[to_stage]:
                hook(model_name, version, from_stage, to_stage)

    def _validate_for_production(self, model_name: str, version: str):
        """Validate model before production deployment."""
        logger.info(f"Validating {model_name}:{version} for production")

        # Check metrics
        metadata = self.registry.get_metadata(model_name, version)
        if not metadata:
            raise ValueError(f"Model metadata not found")

        # Check minimum accuracy threshold
        min_accuracy = 0.90
        accuracy = metadata.metrics.get("accuracy", 0)
        if accuracy < min_accuracy:
            raise ValueError(
                f"Model accuracy {accuracy} below minimum threshold {min_accuracy}"
            )

        # Check for required tests
        # Add your validation logic here

        logger.info(f"Validation passed for {model_name}:{version}")

# Example hooks
def log_promotion(model_name: str, version: str, from_stage: PromotionStage, to_stage: PromotionStage):
    """Log promotion event."""
    logger.info(f"PROMOTION: {model_name}:{version} {from_stage} -> {to_stage}")

def notify_team(model_name: str, version: str, from_stage: PromotionStage, to_stage: PromotionStage):
    """Notify team about production deployment."""
    if to_stage == PromotionStage.PRODUCTION:
        # Send notification (email, Slack, etc.)
        logger.info(f"NOTIFICATION: {model_name}:{version} deployed to production")

def run_sanity_checks(model_name: str, version: str, from_stage: PromotionStage, to_stage: PromotionStage):
    """Run sanity checks before promotion."""
    if to_stage == PromotionStage.PRODUCTION:
        # Run sanity checks
        logger.info(f"Running sanity checks for {model_name}:{version}")
        # Add your sanity check logic here

# Usage
pipeline = ModelPromotionPipeline(registry)

# Register hooks
pipeline.register_pre_hook(PromotionStage.PRODUCTION, run_sanity_checks)
pipeline.register_post_hook(PromotionStage.PRODUCTION, log_promotion)
pipeline.register_post_hook(PromotionStage.PRODUCTION, notify_team)

# Promote model
pipeline.promote(
    model_name="image_classifier",
    version="1.0.0",
    from_stage=PromotionStage.STAGING,
    to_stage=PromotionStage.PRODUCTION
)
```

#### Rollback Strategy

```python
class ModelRollback:
    """Handle model rollbacks."""

    def __init__(self, registry):
        self.registry = registry
        self.rollback_history = {}

    def create_checkpoint(self, model_name: str, version: str):
        """Create rollback checkpoint."""
        logger.info(f"Creating checkpoint for {model_name}:{version}")

        # Get current production version
        current = self.registry.get_model_version(model_name, stage="Production")

        if current:
            checkpoint = {
                "model_name": model_name,
                "version": current.version,
                "created_at": datetime.now().isoformat(),
                "metadata": self.registry.get_metadata(model_name, current.version)
            }

            key = f"{model_name}:{version}"
            self.rollback_history[key] = checkpoint

            logger.info(f"Checkpoint created: {current.version}")
        else:
            logger.warning(f"No production version found for {model_name}")

    def rollback(self, model_name: str, to_version: str = None):
        """Rollback to previous version."""
        logger.info(f"Rolling back {model_name} to {to_version or 'previous version'}")

        if to_version:
            # Rollback to specific version
            self.registry.transition_stage(model_name, to_version, "Production")
        else:
            # Rollback to last checkpoint
            current_production = self.registry.get_model_version(model_name, stage="Production")
            if current_production:
                key = f"{model_name}:{current_production.version}"
                if key in self.rollback_history:
                    checkpoint = self.rollback_history[key]
                    self.registry.transition_stage(model_name, checkpoint["version"], "Production")
                    logger.info(f"Rolled back to {checkpoint['version']}")
                else:
                    logger.warning(f"No checkpoint found for {key}")

    def get_rollback_history(self, model_name: str) -> List[Dict]:
        """Get rollback history for model."""
        return [
            v for k, v in self.rollback_history.items()
            if k.startswith(f"{model_name}:")
        ]

# Usage
rollback = ModelRollback(registry)

# Create checkpoint before promotion
rollback.create_checkpoint("image_classifier", "1.0.0")

# Promote new version
pipeline.promote("image_classifier", "1.0.0", PromotionStage.STAGING, PromotionStage.PRODUCTION)

# Rollback if needed
rollback.rollback("image_classifier")
```

### A/B Testing Setup

#### A/B Test Manager

```python
from typing import Dict, List
import random
import numpy as np

class ABTestManager:
    """Manage A/B testing for models."""

    def __init__(self, registry):
        self.registry = registry
        self.active_tests = {}

    def create_test(
        self,
        test_name: str,
        model_a: str,
        version_a: str,
        model_b: str,
        version_b: str,
        traffic_split: float = 0.5,
        metrics: List[str] = None
    ):
        """Create A/B test."""
        test_id = f"{test_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        self.active_tests[test_id] = {
            "test_name": test_name,
            "model_a": {"name": model_a, "version": version_a},
            "model_b": {"name": model_b, "version": version_b},
            "traffic_split": traffic_split,
            "metrics": metrics or ["accuracy", "latency"],
            "created_at": datetime.now().isoformat(),
            "results_a": [],
            "results_b": []
        }

        logger.info(f"Created A/B test: {test_id}")
        return test_id

    def route_request(self, test_id: str, request_id: str = None) -> str:
        """Route request to model A or B."""
        if test_id not in self.active_tests:
            raise ValueError(f"Test {test_id} not found")

        test = self.active_tests[test_id]

        # Use request_id for consistent routing
        if request_id:
            hash_val = hash(request_id) % 1000
            rand_val = hash_val / 1000.0
        else:
            rand_val = random.random()

        if rand_val < test["traffic_split"]:
            return "A"
        else:
            return "B"

    def record_result(self, test_id: str, model: str, result: Dict):
        """Record test result."""
        if test_id not in self.active_tests:
            raise ValueError(f"Test {test_id} not found")

        test = self.active_tests[test_id]

        if model == "A":
            test["results_a"].append(result)
        elif model == "B":
            test["results_b"].append(result)

    def get_results(self, test_id: str) -> Dict:
        """Get A/B test results."""
        if test_id not in self.active_tests:
            raise ValueError(f"Test {test_id} not found")

        test = self.active_tests[test_id]

        # Calculate statistics
        results_a = test["results_a"]
        results_b = test["results_b"]

        stats = {
            "test_name": test["test_name"],
            "model_a": test["model_a"],
            "model_b": test["model_b"],
            "traffic_split": test["traffic_split"],
            "samples_a": len(results_a),
            "samples_b": len(results_b)
        }

        # Calculate metrics
        for metric in test["metrics"]:
            values_a = [r.get(metric, 0) for r in results_a]
            values_b = [r.get(metric, 0) for r in results_b]

            stats[f"{metric}_a_mean"] = np.mean(values_a) if values_a else 0
            stats[f"{metric}_b_mean"] = np.mean(values_b) if values_b else 0
            stats[f"{metric}_a_std"] = np.std(values_a) if values_a else 0
            stats[f"{metric}_b_std"] = np.std(values_b) if values_b else 0

        return stats

    def conclude_test(self, test_id: str, winner: str = None) -> Dict:
        """Conclude A/B test and promote winner."""
        results = self.get_results(test_id)

        if winner:
            if winner == "A":
                winner_model = self.active_tests[test_id]["model_a"]
            else:
                winner_model = self.active_tests[test_id]["model_b"]

            # Promote winner
            self.registry.transition_stage(
                winner_model["name"],
                winner_model["version"],
                "Production"
            )

            results["winner"] = winner
            results["winner_model"] = winner_model

        # Archive test
        del self.active_tests[test_id]

        return results

# Usage
ab_test = ABTestManager(registry)

# Create A/B test
test_id = ab_test.create_test(
    test_name="model_comparison",
    model_a="image_classifier",
    version_a="1.0.0",
    model_b="image_classifier",
    version_b="1.1.0",
    traffic_split=0.5,
    metrics=["accuracy", "latency_ms"]
)

# Route requests
for request_id in request_ids:
    model = ab_test.route_request(test_id, request_id)
    result = run_inference(model, request_id)
    ab_test.record_result(test_id, model, result)

# Get results
results = ab_test.get_results(test_id)

# Conclude test
ab_test.conclude_test(test_id, winner="B")
```

### Model Comparison

#### Model Comparison Tool

```python
from typing import Dict, List
import pandas as pd

class ModelComparator:
    """Compare multiple models."""

    def __init__(self, registry):
        self.registry = registry

    def compare_models(
        self,
        models: List[Dict],
        metrics: List[str] = None
    ) -> pd.DataFrame:
        """Compare multiple models."""
        comparison_data = []

        for model_info in models:
            model_name = model_info["name"]
            version = model_info["version"]

            metadata = self.registry.get_metadata(model_name, version)

            row = {
                "Model": f"{model_name}:{version}",
                "Framework": metadata.framework,
                "Architecture": metadata.architecture,
                "Parameters": metadata.parameters,
                "Size (MB)": metadata.model_size_mb,
                "Stage": metadata.stage.value
            }

            # Add metrics
            for metric in (metrics or list(metadata.metrics.keys())):
                row[metric] = metadata.metrics.get(metric, 0)

            comparison_data.append(row)

        return pd.DataFrame(comparison_data)

    def compare_versions(
        self,
        model_name: str,
        versions: List[str]
    ) -> pd.DataFrame:
        """Compare different versions of a model."""
        models = [{"name": model_name, "version": v} for v in versions]
        return self.compare_models(models)

    def find_best_model(
        self,
        model_name: str,
        metric: str,
        maximize: bool = True
    ) -> Dict:
        """Find best model version by metric."""
        versions = self.registry.list_versions(model_name)

        best_version = None
        best_value = float('-inf') if maximize else float('inf')

        for version_info in versions:
            metadata = self.registry.get_metadata(model_name, version_info["version"])
            value = metadata.metrics.get(metric, 0)

            if (maximize and value > best_value) or (not maximize and value < best_value):
                best_value = value
                best_version = version_info["version"]

        return {
            "model_name": model_name,
            "version": best_version,
            "metric": metric,
            "value": best_value
        }

# Usage
comparator = ModelComparator(registry)

# Compare models
comparison = comparator.compare_models([
    {"name": "image_classifier", "version": "1.0.0"},
    {"name": "image_classifier", "version": "1.1.0"},
    {"name": "image_classifier", "version": "2.0.0"}
], metrics=["accuracy", "f1", "latency_ms"])

print(comparison)

# Find best model
best = comparator.find_best_model("image_classifier", "accuracy", maximize=True)
print(f"Best model: {best}")
```

## Best Practices

### Versioning Guidelines

1. **Use Semantic Versioning**
   - MAJOR: Breaking changes
   - MINOR: New features, backward compatible
   - PATCH: Bug fixes, backward compatible

2. **Tag Releases in Git**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **Document Changes in CHANGELOG.md**
   ```markdown
   # Changelog

   ## [1.1.0] - 2024-01-15
   ### Added
   - New feature X
   - New feature Y

   ### Changed
   - Improved performance of model

   ## [1.0.0] - 2024-01-01
   ### Added
   - Initial release
   ```

4. **Use Git Commit Hash for Reproducibility**
   ```python
   metadata = {
       "git_commit": GitVersion.get_commit_hash(),
       "git_branch": GitVersion.get_branch()
   }
   ```

5. **Store Hyperparameters with Model**
   ```python
   hyperparameters = {
       "learning_rate": 0.001,
       "batch_size": 32,
       "epochs": 100,
       "optimizer": "Adam"
   }
   ```

### Registry Best Practices

1. **Always Validate Before Production Deployment**
   ```python
   def validate_model(model, test_loader, thresholds):
       """Validate model meets production thresholds."""
       metrics = evaluate(model, test_loader)

       for metric, threshold in thresholds.items():
           if metrics[metric] < threshold:
               raise ValueError(
                   f"Model {metric} ({metrics[metric]}) below threshold ({threshold})"
               )

       return metrics
   ```

2. **Keep Model Lineage**
   ```python
   lineage = ModelLineage()
   lineage.add_model(
       model_name="model_v2",
       version="1.0.0",
       parent_model="model_v1",
       parent_version="1.0.0"
   )
   ```

3. **Use Consistent Metadata**
   ```python
   metadata = ModelMetadata(
       model_name="my_model",
       version="1.0.0",
       framework="pytorch",
       task="classification",
       # ... all required fields
   )
   ```

4. **Archive Old Models**
   ```python
   def archive_old_models(registry, model_name, keep_versions=5):
       """Archive old model versions."""
       versions = registry.list_versions(model_name)

       # Sort by registered date
       versions.sort(key=lambda x: x["registered_at"])

       # Archive all but latest N versions
       for version_info in versions[:-keep_versions]:
           registry.transition_stage(
               model_name,
               version_info["version"],
               "Archived"
           )
   ```

5. **Monitor Production Models**
   ```python
   def monitor_production_models(registry, alert_thresholds):
       """Monitor production models for issues."""
       production_models = registry.list_models(stage="Production")

       for model_info in production_models:
           model, metadata = registry.load(
               model_info["model_name"],
               model_info["version"]
           )

           # Check model health
           health = check_model_health(model)

           if not health["healthy"]:
               # Send alert
               send_alert(
                   model_name=model_info["model_name"],
                   version=model_info["version"],
                   issue=health["issue"]
               )
   ```

## Related Skills

- [`05-ai-ml-core/model-training`](05-ai-ml-core/model-training/SKILL.md)
- [`05-ai-ml-core/model-optimization`](05-ai-ml-core/model-optimization/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`06-ai-ml-production/llm-local-deployment`](06-ai-ml-production/llm-local-deployment/SKILL.md)
- [`15-devops-infrastructure/ci-cd-pipelines`](15-devops-infrastructure/ci-cd-pipelines/SKILL.md)
