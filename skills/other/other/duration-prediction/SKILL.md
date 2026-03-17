---
name: "duration-prediction"
description: "Predict project duration using k-NN and regression. Estimate timeline based on similar historical projects."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🤖", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Duration Prediction

## Business Case

### Problem Statement
Project duration estimation challenges:
- Subjective expert estimates
- Lack of historical benchmarking
- Inaccurate early-stage predictions
- Difficulty comparing similar projects

### Solution
Machine learning-based duration prediction using k-Nearest Neighbors and regression models trained on historical project data.

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
import math


class ModelType(Enum):
    KNN = "knn"
    LINEAR_REGRESSION = "linear_regression"
    WEIGHTED_KNN = "weighted_knn"


class ProjectType(Enum):
    OFFICE = "office"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"
    RETAIL = "retail"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"


@dataclass
class ProjectFeatures:
    project_id: str
    project_type: ProjectType
    size_sf: float
    floors: int
    complexity: int  # 1-5
    location_factor: float  # Cost adjustment factor
    has_basement: bool = False
    is_renovation: bool = False
    actual_duration: Optional[int] = None  # Days


@dataclass
class PredictionResult:
    predicted_duration: int
    confidence_interval: Tuple[int, int]
    similar_projects: List[str]
    model_used: ModelType
    features_importance: Dict[str, float]


class DurationPredictor:
    """Predict project duration using ML techniques."""

    def __init__(self):
        self.training_data: List[ProjectFeatures] = []
        self.feature_weights: Dict[str, float] = {
            'size_sf': 0.30,
            'floors': 0.15,
            'complexity': 0.25,
            'location_factor': 0.10,
            'has_basement': 0.10,
            'is_renovation': 0.10
        }
        self.type_baseline_days: Dict[ProjectType, Dict[str, float]] = {
            ProjectType.OFFICE: {'base': 300, 'per_1000sf': 0.5},
            ProjectType.RESIDENTIAL: {'base': 240, 'per_1000sf': 0.4},
            ProjectType.INDUSTRIAL: {'base': 180, 'per_1000sf': 0.3},
            ProjectType.RETAIL: {'base': 200, 'per_1000sf': 0.35},
            ProjectType.HEALTHCARE: {'base': 400, 'per_1000sf': 0.6},
            ProjectType.EDUCATION: {'base': 320, 'per_1000sf': 0.45}
        }

    def add_training_project(self, project: ProjectFeatures):
        """Add project to training dataset."""
        if project.actual_duration is not None:
            self.training_data.append(project)

    def load_training_data(self, df: pd.DataFrame):
        """Load training data from DataFrame."""

        for _, row in df.iterrows():
            project = ProjectFeatures(
                project_id=str(row['project_id']),
                project_type=ProjectType(row['project_type'].lower()),
                size_sf=float(row['size_sf']),
                floors=int(row['floors']),
                complexity=int(row['complexity']),
                location_factor=float(row.get('location_factor', 1.0)),
                has_basement=bool(row.get('has_basement', False)),
                is_renovation=bool(row.get('is_renovation', False)),
                actual_duration=int(row['actual_duration'])
            )
            self.add_training_project(project)

    def _extract_features(self, project: ProjectFeatures) -> np.ndarray:
        """Extract feature vector from project."""

        return np.array([
            project.size_sf / 10000,  # Normalize to 10k SF
            project.floors,
            project.complexity,
            project.location_factor,
            1 if project.has_basement else 0,
            1 if project.is_renovation else 0
        ])

    def _calculate_distance(self, features1: np.ndarray,
                            features2: np.ndarray) -> float:
        """Calculate weighted Euclidean distance."""

        weights = np.array(list(self.feature_weights.values()))
        diff = (features1 - features2) ** 2
        weighted_diff = diff * weights
        return math.sqrt(np.sum(weighted_diff))

    def _find_k_nearest(self, target: ProjectFeatures, k: int = 5,
                        same_type: bool = True) -> List[Tuple[ProjectFeatures, float]]:
        """Find k nearest neighbors."""

        target_features = self._extract_features(target)
        distances = []

        for project in self.training_data:
            if same_type and project.project_type != target.project_type:
                continue

            proj_features = self._extract_features(project)
            distance = self._calculate_distance(target_features, proj_features)
            distances.append((project, distance))

        distances.sort(key=lambda x: x[1])
        return distances[:k]

    def predict_knn(self, target: ProjectFeatures, k: int = 5) -> PredictionResult:
        """Predict duration using k-NN."""

        nearest = self._find_k_nearest(target, k)

        if not nearest:
            # Fall back to baseline
            return self._predict_baseline(target)

        # Simple average of k nearest
        durations = [p.actual_duration for p, _ in nearest]
        predicted = int(np.mean(durations))

        # Confidence interval (using std dev)
        std = np.std(durations)
        lower = int(predicted - 1.96 * std)
        upper = int(predicted + 1.96 * std)

        return PredictionResult(
            predicted_duration=predicted,
            confidence_interval=(max(1, lower), upper),
            similar_projects=[p.project_id for p, _ in nearest],
            model_used=ModelType.KNN,
            features_importance=self.feature_weights
        )

    def predict_weighted_knn(self, target: ProjectFeatures, k: int = 5) -> PredictionResult:
        """Predict duration using distance-weighted k-NN."""

        nearest = self._find_k_nearest(target, k)

        if not nearest:
            return self._predict_baseline(target)

        # Inverse distance weighting
        total_weight = 0
        weighted_sum = 0

        for project, distance in nearest:
            weight = 1 / (distance + 0.001)  # Add small value to avoid division by zero
            weighted_sum += project.actual_duration * weight
            total_weight += weight

        predicted = int(weighted_sum / total_weight)

        # Confidence interval
        durations = [p.actual_duration for p, _ in nearest]
        std = np.std(durations)
        lower = int(predicted - 1.96 * std)
        upper = int(predicted + 1.96 * std)

        return PredictionResult(
            predicted_duration=predicted,
            confidence_interval=(max(1, lower), upper),
            similar_projects=[p.project_id for p, _ in nearest],
            model_used=ModelType.WEIGHTED_KNN,
            features_importance=self.feature_weights
        )

    def predict_regression(self, target: ProjectFeatures) -> PredictionResult:
        """Predict duration using linear regression."""

        if len(self.training_data) < 3:
            return self._predict_baseline(target)

        # Filter by project type
        same_type = [p for p in self.training_data if p.project_type == target.project_type]

        if len(same_type) < 3:
            same_type = self.training_data

        # Build feature matrix and target vector
        X = np.array([self._extract_features(p) for p in same_type])
        y = np.array([p.actual_duration for p in same_type])

        # Simple linear regression using normal equations
        X_with_intercept = np.column_stack([np.ones(len(X)), X])

        try:
            # beta = (X'X)^-1 X'y
            XtX = X_with_intercept.T @ X_with_intercept
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X_with_intercept.T @ y
        except np.linalg.LinAlgError:
            return self._predict_baseline(target)

        # Predict
        target_features = self._extract_features(target)
        target_with_intercept = np.array([1] + list(target_features))
        predicted = int(target_features @ beta[1:] + beta[0])

        # Calculate residuals for confidence interval
        y_pred = X_with_intercept @ beta
        residuals = y - y_pred
        rmse = math.sqrt(np.mean(residuals ** 2))

        return PredictionResult(
            predicted_duration=max(1, predicted),
            confidence_interval=(max(1, int(predicted - 1.96 * rmse)),
                               int(predicted + 1.96 * rmse)),
            similar_projects=[p.project_id for p in same_type[:5]],
            model_used=ModelType.LINEAR_REGRESSION,
            features_importance=dict(zip(self.feature_weights.keys(),
                                        [abs(b) / sum(abs(beta[1:])) for b in beta[1:]]))
        )

    def _predict_baseline(self, target: ProjectFeatures) -> PredictionResult:
        """Fall back to baseline prediction."""

        baseline = self.type_baseline_days.get(target.project_type,
                                                {'base': 250, 'per_1000sf': 0.4})

        predicted = int(baseline['base'] +
                       (target.size_sf / 1000) * baseline['per_1000sf'] * 30)

        # Adjustments
        if target.complexity > 3:
            predicted = int(predicted * (1 + (target.complexity - 3) * 0.1))
        if target.has_basement:
            predicted = int(predicted * 1.1)
        if target.is_renovation:
            predicted = int(predicted * 1.2)

        predicted = int(predicted * target.location_factor)

        return PredictionResult(
            predicted_duration=predicted,
            confidence_interval=(int(predicted * 0.8), int(predicted * 1.2)),
            similar_projects=[],
            model_used=ModelType.LINEAR_REGRESSION,
            features_importance=self.feature_weights
        )

    def predict(self, target: ProjectFeatures,
                model: ModelType = ModelType.WEIGHTED_KNN,
                k: int = 5) -> PredictionResult:
        """Predict duration using specified model."""

        if model == ModelType.KNN:
            return self.predict_knn(target, k)
        elif model == ModelType.WEIGHTED_KNN:
            return self.predict_weighted_knn(target, k)
        elif model == ModelType.LINEAR_REGRESSION:
            return self.predict_regression(target)

        return self._predict_baseline(target)

    def evaluate_model(self, test_data: List[ProjectFeatures],
                       model: ModelType = ModelType.WEIGHTED_KNN) -> Dict[str, float]:
        """Evaluate model performance."""

        actuals = []
        predictions = []

        for project in test_data:
            if project.actual_duration is None:
                continue

            result = self.predict(project, model)
            actuals.append(project.actual_duration)
            predictions.append(result.predicted_duration)

        if not actuals:
            return {}

        actuals = np.array(actuals)
        predictions = np.array(predictions)

        mae = np.mean(np.abs(actuals - predictions))
        mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
        rmse = math.sqrt(np.mean((actuals - predictions) ** 2))

        return {
            'mae': round(mae, 1),
            'mape': round(mape, 1),
            'rmse': round(rmse, 1),
            'samples': len(actuals)
        }

    def get_similar_projects(self, target: ProjectFeatures, n: int = 10) -> pd.DataFrame:
        """Get most similar projects."""

        nearest = self._find_k_nearest(target, k=n, same_type=False)

        data = [{
            'Project ID': p.project_id,
            'Type': p.project_type.value,
            'Size (SF)': p.size_sf,
            'Floors': p.floors,
            'Complexity': p.complexity,
            'Duration (days)': p.actual_duration,
            'Distance': round(d, 3)
        } for p, d in nearest]

        return pd.DataFrame(data)
```

## Quick Start

```python
# Create predictor
predictor = DurationPredictor()

# Add training data
training_projects = [
    ProjectFeatures("P001", ProjectType.OFFICE, 50000, 10, 3, 1.0, True, False, 365),
    ProjectFeatures("P002", ProjectType.OFFICE, 75000, 15, 4, 1.1, True, False, 450),
    ProjectFeatures("P003", ProjectType.OFFICE, 30000, 5, 2, 0.9, False, False, 280),
    ProjectFeatures("P004", ProjectType.OFFICE, 60000, 12, 3, 1.0, True, False, 390),
]

for p in training_projects:
    predictor.add_training_project(p)

# Predict for new project
new_project = ProjectFeatures(
    project_id="NEW-001",
    project_type=ProjectType.OFFICE,
    size_sf=55000,
    floors=11,
    complexity=3,
    location_factor=1.0,
    has_basement=True,
    is_renovation=False
)

result = predictor.predict(new_project, ModelType.WEIGHTED_KNN)
print(f"Predicted duration: {result.predicted_duration} days")
print(f"Confidence interval: {result.confidence_interval}")
print(f"Similar projects: {result.similar_projects}")
```

## Common Use Cases

### 1. Compare Models
```python
knn_result = predictor.predict(new_project, ModelType.KNN)
weighted_result = predictor.predict(new_project, ModelType.WEIGHTED_KNN)
regression_result = predictor.predict(new_project, ModelType.LINEAR_REGRESSION)

print(f"k-NN: {knn_result.predicted_duration}")
print(f"Weighted k-NN: {weighted_result.predicted_duration}")
print(f"Regression: {regression_result.predicted_duration}")
```

### 2. Model Evaluation
```python
metrics = predictor.evaluate_model(test_data, ModelType.WEIGHTED_KNN)
print(f"MAE: {metrics['mae']} days")
print(f"MAPE: {metrics['mape']}%")
```

### 3. Find Similar Projects
```python
similar = predictor.get_similar_projects(new_project, n=5)
print(similar)
```

## Resources
- **DDC Book**: Chapter 4.5 - Future: Predictions and Machine Learning
- **scikit-learn**: https://scikit-learn.org/
- **Website**: https://datadrivenconstruction.io
