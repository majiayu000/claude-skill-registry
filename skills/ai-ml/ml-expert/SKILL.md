---
name: ml-expert
version: 1.0.0
description: Expert-level machine learning, deep learning, model training, and MLOps
category: ai
tags: [machine-learning, deep-learning, neural-networks, mlops, data-science]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# Machine Learning Expert

Expert guidance for machine learning systems, deep learning, model training, deployment, and MLOps practices.

## Core Concepts

### Machine Learning Fundamentals
- Supervised learning (classification, regression)
- Unsupervised learning (clustering, dimensionality reduction)
- Reinforcement learning
- Feature engineering
- Model evaluation and validation
- Hyperparameter tuning

### Deep Learning
- Neural networks (CNNs, RNNs, Transformers)
- Transfer learning
- Fine-tuning pre-trained models
- Attention mechanisms
- GANs (Generative Adversarial Networks)
- Autoencoders

### MLOps
- Model versioning and tracking
- Experiment management
- Model deployment and serving
- Monitoring and retraining
- CI/CD for ML pipelines
- A/B testing for models

## Supervised Learning

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

class MLPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.feature_names = None

    def prepare_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2):
        """Split and scale data"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.feature_names = X.columns.tolist()

        return X_train_scaled, X_test_scaled, y_train, y_test

    def train_classifier(self, X_train, y_train, n_estimators: int = 100):
        """Train random forest classifier"""
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_train, y_train)

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)

        return {
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "feature_importance": dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }

    def evaluate(self, X_test, y_test) -> dict:
        """Evaluate model performance"""
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)

        return {
            "predictions": y_pred,
            "probabilities": y_proba,
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "classification_report": classification_report(y_test, y_pred, output_dict=True)
        }

    def save_model(self, path: str):
        """Save model and scaler"""
        joblib.dump({
            "model": self.model,
            "scaler": self.scaler,
            "feature_names": self.feature_names
        }, path)
```

## Deep Learning with PyTorch

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

class NeuralNetwork(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, num_classes: int):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, num_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

class Trainer:
    def __init__(self, model, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = model.to(device)
        self.device = device
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(model.parameters(), lr=0.001)

    def train_epoch(self, dataloader: DataLoader) -> float:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0

        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(self.device), target.to(self.device)

            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)

            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(dataloader)

    def evaluate(self, dataloader: DataLoader) -> dict:
        """Evaluate model"""
        self.model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in dataloader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()

        return {
            "accuracy": 100 * correct / total,
            "total_samples": total
        }

    def train(self, train_loader: DataLoader, val_loader: DataLoader,
              epochs: int = 10):
        """Full training loop"""
        history = {"train_loss": [], "val_acc": []}

        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_metrics = self.evaluate(val_loader)

            history["train_loss"].append(train_loss)
            history["val_acc"].append(val_metrics["accuracy"])

            print(f"Epoch {epoch+1}/{epochs} - Loss: {train_loss:.4f} - Val Acc: {val_metrics['accuracy']:.2f}%")

        return history
```

## Model Deployment

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str

class ModelServer:
    def __init__(self, model_path: str):
        self.model_data = joblib.load(model_path)
        self.model = self.model_data["model"]
        self.scaler = self.model_data["scaler"]
        self.version = "1.0.0"

    def predict(self, features: np.ndarray) -> dict:
        """Make prediction"""
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))

        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0].max()

        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "model_version": self.version
        }

# Global model instance
model_server = ModelServer("model.pkl")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        features = np.array(request.features)
        result = model_server.predict(features)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": model_server.version}
```

## MLOps with MLflow

```python
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

class MLflowExperiment:
    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()

    def log_training_run(self, model, X_train, y_train, X_test, y_test,
                        params: dict):
        """Log training run with MLflow"""
        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(params)

            # Train model
            model.fit(X_train, y_train)

            # Evaluate
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)

            # Log metrics
            mlflow.log_metric("train_accuracy", train_score)
            mlflow.log_metric("test_accuracy", test_score)

            # Log model
            mlflow.sklearn.log_model(model, "model")

            # Log feature importance
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(enumerate(model.feature_importances_))
                mlflow.log_dict(feature_importance, "feature_importance.json")

            run_id = mlflow.active_run().info.run_id
            return run_id

    def register_model(self, run_id: str, model_name: str):
        """Register model in MLflow model registry"""
        model_uri = f"runs:/{run_id}/model"
        mlflow.register_model(model_uri, model_name)

    def promote_to_production(self, model_name: str, version: int):
        """Promote model version to production"""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production"
        )
```

## Best Practices

### Data Preparation
- Handle missing values appropriately
- Scale/normalize features
- Encode categorical variables properly
- Split data before any preprocessing
- Use stratified splits for imbalanced data
- Create validation set for hyperparameter tuning

### Model Training
- Start with simple baselines
- Use cross-validation
- Monitor training and validation metrics
- Implement early stopping
- Save best model checkpoints
- Track experiments systematically

### Deployment
- Version models and datasets
- Monitor model performance in production
- Implement model A/B testing
- Set up retraining pipelines
- Log predictions for analysis
- Implement fallback mechanisms

## Anti-Patterns

❌ Training on test data (data leakage)
❌ No validation set for hyperparameter tuning
❌ Ignoring class imbalance
❌ Not scaling features
❌ Overfitting to training data
❌ No model versioning
❌ Missing monitoring in production

## Resources

- Scikit-learn: https://scikit-learn.org/
- PyTorch: https://pytorch.org/
- TensorFlow: https://www.tensorflow.org/
- MLflow: https://mlflow.org/
- Hugging Face: https://huggingface.co/
