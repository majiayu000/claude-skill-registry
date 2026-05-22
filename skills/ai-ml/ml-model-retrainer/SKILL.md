---
name: "ml-model-retrainer"
description: "Automated pipeline for retraining ML models with new construction data. Monitor model drift, trigger retraining, and validate model performance."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🤖", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# ML Model Retrainer for Construction

## Overview

Automated pipeline for keeping construction ML models up-to-date. Monitor for data drift, trigger retraining when needed, validate performance, and manage model versions.

## Business Case

ML models degrade over time as:
- Market conditions change (material prices, labor rates)
- New construction methods emerge
- Project complexity evolves
- Regional factors shift

Continuous retraining ensures predictions remain accurate.

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import pickle
import hashlib
import json
import os

@dataclass
class ModelVersion:
    version_id: str
    model_name: str
    created_at: datetime
    training_samples: int
    metrics: Dict[str, float]
    feature_columns: List[str]
    hyperparameters: Dict[str, Any]
    data_hash: str
    is_active: bool = False

@dataclass
class DriftReport:
    checked_at: datetime
    data_drift_detected: bool
    performance_drift_detected: bool
    drift_score: float
    affected_features: List[str]
    recommendation: str

@dataclass
class RetrainingResult:
    success: bool
    new_version: Optional[ModelVersion]
    old_metrics: Dict[str, float]
    new_metrics: Dict[str, float]
    improvement: Dict[str, float]
    validation_passed: bool
    notes: List[str]

class MLModelRetrainer:
    """Automated ML model retraining for construction predictions."""

    def __init__(self, model_dir: str = "./models"):
        self.model_dir = model_dir
        self.models: Dict[str, Any] = {}
        self.versions: Dict[str, List[ModelVersion]] = {}
        self.active_versions: Dict[str, ModelVersion] = {}
        self.drift_thresholds = {
            'performance_degradation': 0.15,  # 15% degradation triggers retrain
            'data_drift_score': 0.3,
            'min_new_samples': 50,
        }

        os.makedirs(model_dir, exist_ok=True)

    def register_model(self, model_name: str, model: Any,
                       feature_columns: List[str],
                       hyperparameters: Dict = None) -> ModelVersion:
        """Register a new model for management."""
        version = ModelVersion(
            version_id=f"{model_name}-v{datetime.now().strftime('%Y%m%d%H%M%S')}",
            model_name=model_name,
            created_at=datetime.now(),
            training_samples=0,
            metrics={},
            feature_columns=feature_columns,
            hyperparameters=hyperparameters or {},
            data_hash="",
            is_active=True
        )

        self.models[model_name] = model
        if model_name not in self.versions:
            self.versions[model_name] = []
        self.versions[model_name].append(version)
        self.active_versions[model_name] = version

        return version

    def calculate_data_hash(self, data: pd.DataFrame) -> str:
        """Calculate hash of training data for change detection."""
        data_str = data.to_json()
        return hashlib.md5(data_str.encode()).hexdigest()

    def detect_data_drift(self, model_name: str,
                          reference_data: pd.DataFrame,
                          current_data: pd.DataFrame) -> DriftReport:
        """Detect data drift between reference and current data."""

        drift_scores = {}
        affected_features = []

        # Compare distributions for each feature
        for col in reference_data.select_dtypes(include=[np.number]).columns:
            if col in current_data.columns:
                ref_mean = reference_data[col].mean()
                ref_std = reference_data[col].std()
                cur_mean = current_data[col].mean()
                cur_std = current_data[col].std()

                # Normalized difference
                if ref_std > 0:
                    mean_drift = abs(cur_mean - ref_mean) / ref_std
                    std_drift = abs(cur_std - ref_std) / ref_std
                    drift_scores[col] = (mean_drift + std_drift) / 2

                    if drift_scores[col] > 0.5:
                        affected_features.append(f"{col} (drift: {drift_scores[col]:.2f})")

        avg_drift = np.mean(list(drift_scores.values())) if drift_scores else 0
        data_drift_detected = avg_drift > self.drift_thresholds['data_drift_score']

        recommendation = "No action needed"
        if data_drift_detected:
            recommendation = "Data drift detected - consider retraining"
        elif avg_drift > self.drift_thresholds['data_drift_score'] * 0.7:
            recommendation = "Minor drift detected - monitor closely"

        return DriftReport(
            checked_at=datetime.now(),
            data_drift_detected=data_drift_detected,
            performance_drift_detected=False,
            drift_score=avg_drift,
            affected_features=affected_features,
            recommendation=recommendation
        )

    def evaluate_model_performance(self, model_name: str,
                                   test_data: pd.DataFrame,
                                   target_col: str) -> Dict[str, float]:
        """Evaluate current model performance on new data."""

        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not registered")

        model = self.models[model_name]
        version = self.active_versions[model_name]

        # Prepare features
        X = test_data[version.feature_columns].fillna(0)
        y = test_data[target_col]

        # Predict
        y_pred = model.predict(X)

        # Calculate metrics
        metrics = {
            'mae': mean_absolute_error(y, y_pred),
            'rmse': np.sqrt(mean_squared_error(y, y_pred)),
            'r2': r2_score(y, y_pred),
            'mape': np.mean(np.abs((y - y_pred) / y.replace(0, 1))) * 100,
        }

        return metrics

    def check_performance_drift(self, model_name: str,
                                 baseline_metrics: Dict[str, float],
                                 current_metrics: Dict[str, float]) -> DriftReport:
        """Check if model performance has degraded."""

        # Calculate degradation for each metric
        degradation = {}
        for metric in ['mae', 'rmse']:
            if metric in baseline_metrics and metric in current_metrics:
                # Higher is worse for these metrics
                change = (current_metrics[metric] - baseline_metrics[metric]) / baseline_metrics[metric]
                degradation[metric] = change

        for metric in ['r2']:
            if metric in baseline_metrics and metric in current_metrics:
                # Lower is worse for R2
                change = (baseline_metrics[metric] - current_metrics[metric]) / abs(baseline_metrics[metric])
                degradation[metric] = change

        avg_degradation = np.mean(list(degradation.values())) if degradation else 0
        performance_drift = avg_degradation > self.drift_thresholds['performance_degradation']

        affected = [f"{m}: {d:+.1%}" for m, d in degradation.items() if d > 0.1]

        recommendation = "No action needed"
        if performance_drift:
            recommendation = "Performance degraded - retraining recommended"
        elif avg_degradation > self.drift_thresholds['performance_degradation'] * 0.5:
            recommendation = "Performance declining - monitor closely"

        return DriftReport(
            checked_at=datetime.now(),
            data_drift_detected=False,
            performance_drift_detected=performance_drift,
            drift_score=avg_degradation,
            affected_features=affected,
            recommendation=recommendation
        )

    def retrain_model(self, model_name: str,
                      training_data: pd.DataFrame,
                      target_col: str,
                      model_class: type,
                      hyperparameters: Dict = None,
                      validation_data: pd.DataFrame = None) -> RetrainingResult:
        """Retrain model with new data."""

        if model_name not in self.active_versions:
            raise ValueError(f"Model {model_name} not found")

        old_version = self.active_versions[model_name]
        old_metrics = old_version.metrics.copy()

        notes = []

        # Check minimum samples
        if len(training_data) < self.drift_thresholds['min_new_samples']:
            notes.append(f"Warning: Only {len(training_data)} samples (minimum: {self.drift_thresholds['min_new_samples']})")

        # Prepare data
        X = training_data[old_version.feature_columns].fillna(0)
        y = training_data[target_col]

        # Train new model
        hyperparams = hyperparameters or old_version.hyperparameters
        new_model = model_class(**hyperparams)
        new_model.fit(X, y)

        # Evaluate on validation data
        if validation_data is not None:
            X_val = validation_data[old_version.feature_columns].fillna(0)
            y_val = validation_data[target_col]
            y_pred = new_model.predict(X_val)

            new_metrics = {
                'mae': mean_absolute_error(y_val, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_val, y_pred)),
                'r2': r2_score(y_val, y_pred),
            }
        else:
            # Cross-validation
            cv_scores = cross_val_score(new_model, X, y, cv=5, scoring='neg_mean_absolute_error')
            new_metrics = {
                'mae': -cv_scores.mean(),
                'mae_std': cv_scores.std(),
            }
            new_model.fit(X, y)  # Refit on full data

        # Calculate improvement
        improvement = {}
        for metric in new_metrics:
            if metric in old_metrics:
                if metric in ['mae', 'rmse']:
                    imp = (old_metrics[metric] - new_metrics[metric]) / old_metrics[metric]
                else:
                    imp = (new_metrics[metric] - old_metrics[metric]) / abs(old_metrics[metric])
                improvement[metric] = imp

        # Validation check
        validation_passed = True
        if 'mae' in improvement and improvement['mae'] < -0.1:
            validation_passed = False
            notes.append("New model performs worse - not deploying")

        if validation_passed:
            # Create new version
            new_version = ModelVersion(
                version_id=f"{model_name}-v{datetime.now().strftime('%Y%m%d%H%M%S')}",
                model_name=model_name,
                created_at=datetime.now(),
                training_samples=len(training_data),
                metrics=new_metrics,
                feature_columns=old_version.feature_columns,
                hyperparameters=hyperparams,
                data_hash=self.calculate_data_hash(training_data),
                is_active=True
            )

            # Deactivate old version
            old_version.is_active = False

            # Update registries
            self.models[model_name] = new_model
            self.versions[model_name].append(new_version)
            self.active_versions[model_name] = new_version

            notes.append(f"Model updated: {old_version.version_id} -> {new_version.version_id}")

            return RetrainingResult(
                success=True,
                new_version=new_version,
                old_metrics=old_metrics,
                new_metrics=new_metrics,
                improvement=improvement,
                validation_passed=True,
                notes=notes
            )
        else:
            return RetrainingResult(
                success=False,
                new_version=None,
                old_metrics=old_metrics,
                new_metrics=new_metrics,
                improvement=improvement,
                validation_passed=False,
                notes=notes
            )

    def save_model(self, model_name: str, path: str = None):
        """Save model to disk."""
        if path is None:
            version = self.active_versions[model_name]
            path = os.path.join(self.model_dir, f"{version.version_id}.pkl")

        model_data = {
            'model': self.models[model_name],
            'version': self.active_versions[model_name],
        }

        with open(path, 'wb') as f:
            pickle.dump(model_data, f)

        return path

    def load_model(self, path: str) -> str:
        """Load model from disk."""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)

        model_name = model_data['version'].model_name
        self.models[model_name] = model_data['model']
        self.active_versions[model_name] = model_data['version']

        if model_name not in self.versions:
            self.versions[model_name] = []
        self.versions[model_name].append(model_data['version'])

        return model_name

    def get_model_history(self, model_name: str) -> pd.DataFrame:
        """Get version history for a model."""
        if model_name not in self.versions:
            return pd.DataFrame()

        history = []
        for v in self.versions[model_name]:
            history.append({
                'version_id': v.version_id,
                'created_at': v.created_at,
                'training_samples': v.training_samples,
                'mae': v.metrics.get('mae'),
                'r2': v.metrics.get('r2'),
                'is_active': v.is_active
            })

        return pd.DataFrame(history)

    def run_maintenance_check(self, model_name: str,
                               reference_data: pd.DataFrame,
                               current_data: pd.DataFrame,
                               target_col: str) -> Dict:
        """Run complete maintenance check for a model."""

        results = {
            'model_name': model_name,
            'checked_at': datetime.now(),
            'actions_needed': []
        }

        # Check data drift
        data_drift = self.detect_data_drift(model_name, reference_data, current_data)
        results['data_drift'] = {
            'detected': data_drift.data_drift_detected,
            'score': data_drift.drift_score,
            'affected_features': data_drift.affected_features
        }

        if data_drift.data_drift_detected:
            results['actions_needed'].append("Retrain due to data drift")

        # Check performance
        baseline_metrics = self.active_versions[model_name].metrics
        current_metrics = self.evaluate_model_performance(model_name, current_data, target_col)

        perf_drift = self.check_performance_drift(model_name, baseline_metrics, current_metrics)
        results['performance_drift'] = {
            'detected': perf_drift.performance_drift_detected,
            'score': perf_drift.drift_score,
            'metrics_affected': perf_drift.affected_features
        }

        if perf_drift.performance_drift_detected:
            results['actions_needed'].append("Retrain due to performance degradation")

        # Overall recommendation
        if results['actions_needed']:
            results['recommendation'] = "Retraining recommended"
        else:
            results['recommendation'] = "Model performing well - no action needed"

        return results

    def generate_report(self, model_name: str) -> str:
        """Generate model status report."""
        lines = [f"# Model Status Report: {model_name}", ""]
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        if model_name in self.active_versions:
            version = self.active_versions[model_name]
            lines.append("")
            lines.append("## Active Version")
            lines.append(f"- **Version:** {version.version_id}")
            lines.append(f"- **Created:** {version.created_at.strftime('%Y-%m-%d')}")
            lines.append(f"- **Training Samples:** {version.training_samples:,}")
            lines.append("")
            lines.append("## Performance Metrics")
            for metric, value in version.metrics.items():
                lines.append(f"- **{metric}:** {value:.4f}")

        # Version history
        lines.append("")
        lines.append("## Version History")
        history = self.get_model_history(model_name)
        if not history.empty:
            lines.append(history.to_markdown(index=False))

        return "\n".join(lines)
```

## Quick Start

```python
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

# Load data
historical = pd.read_excel("historical_projects.xlsx")
new_data = pd.read_excel("recent_projects.xlsx")

# Initialize retrainer
retrainer = MLModelRetrainer("./models")

# Train initial model
features = ['gross_area', 'contract_value', 'planned_duration', 'num_subcontractors']
X = historical[features]
y = historical['delay_days']

model = GradientBoostingRegressor(n_estimators=100)
model.fit(X, y)

# Register model
version = retrainer.register_model(
    "schedule_delay",
    model,
    features,
    {'n_estimators': 100}
)

# Run maintenance check
check = retrainer.run_maintenance_check(
    "schedule_delay",
    historical,
    new_data,
    "delay_days"
)
print(f"Recommendation: {check['recommendation']}")

# Retrain if needed
if check['actions_needed']:
    result = retrainer.retrain_model(
        "schedule_delay",
        pd.concat([historical, new_data]),
        "delay_days",
        GradientBoostingRegressor,
        {'n_estimators': 100}
    )
    print(f"Retraining {'successful' if result.success else 'failed'}")
    for note in result.notes:
        print(f"  - {note}")

# Save model
retrainer.save_model("schedule_delay")

# Generate report
print(retrainer.generate_report("schedule_delay"))
```

## Dependencies

```bash
pip install pandas numpy scikit-learn
```
