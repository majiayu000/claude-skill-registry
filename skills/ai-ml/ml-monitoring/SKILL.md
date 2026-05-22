---
name: ml-monitoring
description: Production-grade ML model monitoring, drift detection, and observability
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 06-monitoring-observability
bond_type: PRIMARY_BOND

input_schema:
  type: object
  required:
    - monitoring_type
  properties:
    monitoring_type:
      type: string
      enum: [drift_detection, performance_monitoring, alerting, ab_testing, root_cause_analysis]
    model_type:
      type: string
      enum: [classification, regression, ranking, recommendation, nlp, cv]
    drift_config:
      type: object
      properties:
        reference_window_days:
          type: integer
          default: 30
        detection_method:
          type: string
          enum: [ks_test, psi, wasserstein, chi_square, js_divergence]
        threshold:
          type: number
          default: 0.1

output_schema:
  type: object
  properties:
    status:
      type: string
      enum: [healthy, degraded, critical, unknown]
    drift_results:
      type: object
    alerts:
      type: array
      items:
        type: object
    recommendations:
      type: array
      items:
        type: string
    next_steps:
      type: array
      items:
        type: string

validation:
  pre_conditions:
    - model_deployed_and_serving
    - metrics_endpoint_accessible
    - baseline_data_available
  post_conditions:
    - monitoring_dashboard_updated
    - alerts_configured
    - drift_report_generated

error_handling:
  common_errors:
    - type: insufficient_baseline_data
      recovery: extend_reference_window
    - type: metrics_collection_failure
      recovery: fallback_to_cached_metrics
    - type: alert_fatigue
      recovery: adjust_thresholds_dynamically
---

# ML Monitoring

Production-grade ML model monitoring, drift detection, and observability skill.

## Learning Objectives

By mastering this skill, you will be able to:
- Implement comprehensive data and model drift detection
- Build production alerting systems with actionable notifications
- Design and analyze A/B tests for model comparison
- Create observability dashboards for ML systems
- Perform root cause analysis on model degradation

---

## Module 1: Data Drift Detection

### Concept Overview

Data drift occurs when the statistical properties of model inputs change over time, potentially degrading model performance.

### Drift Detection Methods

| Method | Best For | Sensitivity | Compute Cost |
|--------|----------|-------------|--------------|
| KS Test | Continuous features | High | Low |
| PSI | Categorical features | Medium | Low |
| Wasserstein | Distribution shape | High | Medium |
| Chi-Square | Categorical | Medium | Low |
| JS Divergence | Probability distributions | High | Medium |

### Implementation: Evidently AI Drift Detection

```python
"""
Production-ready drift detection with Evidently AI.
"""
import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import (
    DataDriftTable,
    DatasetDriftMetric,
    ColumnDriftMetric
)
from typing import Dict, Any, Optional
import json
from datetime import datetime

class DriftDetector:
    """Enterprise drift detection system."""

    def __init__(
        self,
        reference_data: pd.DataFrame,
        column_mapping: Optional[ColumnMapping] = None,
        drift_threshold: float = 0.1
    ):
        self.reference_data = reference_data
        self.column_mapping = column_mapping or ColumnMapping()
        self.drift_threshold = drift_threshold
        self.drift_history = []

    def detect_drift(
        self,
        current_data: pd.DataFrame,
        include_target: bool = True
    ) -> Dict[str, Any]:
        """
        Detect drift between reference and current data.

        Args:
            current_data: Current production data
            include_target: Whether to check target drift

        Returns:
            Drift detection results with actionable insights
        """
        # Build report with metrics
        metrics = [
            DatasetDriftMetric(),
            DataDriftTable()
        ]

        report = Report(metrics=metrics)
        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )

        # Extract results
        result_dict = report.as_dict()

        drift_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "dataset_drift": result_dict["metrics"][0]["result"]["dataset_drift"],
            "drift_share": result_dict["metrics"][0]["result"]["drift_share"],
            "drifted_columns": [],
            "severity": "healthy",
            "recommendations": []
        }

        # Analyze column-level drift
        column_results = result_dict["metrics"][1]["result"]["drift_by_columns"]
        for col_name, col_data in column_results.items():
            if col_data["drift_detected"]:
                drift_result["drifted_columns"].append({
                    "column": col_name,
                    "drift_score": col_data["drift_score"],
                    "stattest_name": col_data["stattest_name"]
                })

        # Determine severity
        drift_share = drift_result["drift_share"]
        if drift_share > 0.5:
            drift_result["severity"] = "critical"
            drift_result["recommendations"].append(
                "URGENT: Major drift detected. Consider model retraining."
            )
        elif drift_share > 0.2:
            drift_result["severity"] = "degraded"
            drift_result["recommendations"].append(
                "WARNING: Moderate drift. Investigate drifted features."
            )

        # Store history
        self.drift_history.append(drift_result)

        return drift_result

    def generate_html_report(
        self,
        current_data: pd.DataFrame,
        output_path: str
    ) -> str:
        """Generate interactive HTML drift report."""
        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )
        report.save_html(output_path)
        return output_path


# Usage Example
if __name__ == "__main__":
    # Load reference data (from training period)
    reference_df = pd.read_parquet("data/reference_baseline.parquet")

    # Load current production data
    current_df = pd.read_parquet("data/production_latest.parquet")

    # Configure column mapping
    column_mapping = ColumnMapping(
        target="label",
        prediction="prediction",
        numerical_features=["feature_1", "feature_2", "feature_3"],
        categorical_features=["category_a", "category_b"]
    )

    # Initialize detector
    detector = DriftDetector(
        reference_data=reference_df,
        column_mapping=column_mapping,
        drift_threshold=0.1
    )

    # Run drift detection
    results = detector.detect_drift(current_df)
    print(json.dumps(results, indent=2))
```

### Exercise 1.1: Custom Drift Detection

**Task**: Implement a custom drift detector for a specific feature type.

```python
# Implement multivariate drift detection using MMD
from sklearn.metrics.pairwise import rbf_kernel
import numpy as np

def maximum_mean_discrepancy(
    X: np.ndarray,
    Y: np.ndarray,
    gamma: float = 1.0
) -> float:
    """
    Calculate MMD between two distributions.

    TODO: Implement
    1. Calculate K_XX (kernel of X with itself)
    2. Calculate K_YY (kernel of Y with itself)
    3. Calculate K_XY (cross kernel)
    4. Return MMD = mean(K_XX) + mean(K_YY) - 2*mean(K_XY)
    """
    pass

# Test with synthetic data
np.random.seed(42)
X_ref = np.random.normal(0, 1, (1000, 5))
X_drift = np.random.normal(0.5, 1.2, (1000, 5))  # Drifted
X_nodrift = np.random.normal(0.02, 1.01, (1000, 5))  # Stable

# mmd_drift = maximum_mean_discrepancy(X_ref, X_drift)
# mmd_nodrift = maximum_mean_discrepancy(X_ref, X_nodrift)
# Assert: mmd_drift >> mmd_nodrift
```

---

## Module 2: Model Performance Monitoring

### Key Performance Indicators

```yaml
classification_metrics:
  primary:
    - accuracy
    - f1_score
    - auc_roc
  secondary:
    - precision
    - recall
    - log_loss
  business:
    - false_positive_cost
    - false_negative_cost

regression_metrics:
  primary:
    - rmse
    - mae
    - r2_score
  secondary:
    - mape
    - quantile_loss
  business:
    - prediction_interval_coverage
    - business_value_captured
```

### Implementation: Prometheus Metrics Exporter

```python
"""
Production metrics exporter for ML models.
"""
from prometheus_client import (
    Counter, Gauge, Histogram, Summary,
    CollectorRegistry, generate_latest
)
from typing import Dict, Any, List
import time
from functools import wraps
import numpy as np

class MLMetricsExporter:
    """Export ML metrics to Prometheus."""

    def __init__(self, model_name: str, model_version: str):
        self.registry = CollectorRegistry()
        self.model_name = model_name
        self.model_version = model_version

        # Prediction metrics
        self.prediction_counter = Counter(
            'ml_predictions_total',
            'Total number of predictions',
            ['model_name', 'model_version', 'status'],
            registry=self.registry
        )

        self.prediction_latency = Histogram(
            'ml_prediction_latency_seconds',
            'Prediction latency in seconds',
            ['model_name', 'model_version'],
            buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
            registry=self.registry
        )

        self.prediction_confidence = Histogram(
            'ml_prediction_confidence',
            'Prediction confidence distribution',
            ['model_name', 'model_version', 'predicted_class'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99],
            registry=self.registry
        )

        # Feature metrics
        self.feature_value = Summary(
            'ml_feature_value',
            'Feature value distribution',
            ['model_name', 'feature_name'],
            registry=self.registry
        )

        # Performance metrics (updated via ground truth)
        self.model_accuracy = Gauge(
            'ml_model_accuracy',
            'Current model accuracy',
            ['model_name', 'model_version', 'window'],
            registry=self.registry
        )

        self.model_f1 = Gauge(
            'ml_model_f1_score',
            'Current model F1 score',
            ['model_name', 'model_version', 'window'],
            registry=self.registry
        )

        # Drift metrics
        self.drift_score = Gauge(
            'ml_drift_score',
            'Current drift score',
            ['model_name', 'drift_type', 'feature'],
            registry=self.registry
        )

    def track_prediction(self, func):
        """Decorator to track prediction metrics."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                latency = time.time() - start_time

                # Track successful prediction
                self.prediction_counter.labels(
                    model_name=self.model_name,
                    model_version=self.model_version,
                    status='success'
                ).inc()

                self.prediction_latency.labels(
                    model_name=self.model_name,
                    model_version=self.model_version
                ).observe(latency)

                # Track confidence if available
                if isinstance(result, dict) and 'confidence' in result:
                    predicted_class = str(result.get('class', 'unknown'))
                    self.prediction_confidence.labels(
                        model_name=self.model_name,
                        model_version=self.model_version,
                        predicted_class=predicted_class
                    ).observe(result['confidence'])

                return result

            except Exception as e:
                self.prediction_counter.labels(
                    model_name=self.model_name,
                    model_version=self.model_version,
                    status='error'
                ).inc()
                raise

        return wrapper

    def update_performance_metrics(
        self,
        accuracy: float,
        f1_score: float,
        window: str = "1h"
    ):
        """Update performance metrics from ground truth."""
        self.model_accuracy.labels(
            model_name=self.model_name,
            model_version=self.model_version,
            window=window
        ).set(accuracy)

        self.model_f1.labels(
            model_name=self.model_name,
            model_version=self.model_version,
            window=window
        ).set(f1_score)

    def update_drift_score(
        self,
        drift_type: str,
        feature: str,
        score: float
    ):
        """Update drift metrics."""
        self.drift_score.labels(
            model_name=self.model_name,
            drift_type=drift_type,
            feature=feature
        ).set(score)

    def get_metrics(self) -> bytes:
        """Get metrics in Prometheus format."""
        return generate_latest(self.registry)


# FastAPI integration
from fastapi import FastAPI, Response

app = FastAPI()
metrics_exporter = MLMetricsExporter(
    model_name="fraud_detector",
    model_version="v2.1.0"
)

@app.get("/metrics")
async def metrics():
    return Response(
        content=metrics_exporter.get_metrics(),
        media_type="text/plain"
    )

@app.post("/predict")
@metrics_exporter.track_prediction
async def predict(request: dict):
    # Your prediction logic here
    return {"class": 1, "confidence": 0.92}
```

---

## Module 3: Alerting System Design

### Alert Severity Matrix

```yaml
critical_alerts:
  conditions:
    - model_accuracy_drop > 15%
    - prediction_latency_p99 > 2s
    - error_rate > 5%
    - data_drift_score > 0.5
  response_time: immediate
  notification: pagerduty + slack

warning_alerts:
  conditions:
    - model_accuracy_drop > 5%
    - prediction_latency_p95 > 500ms
    - error_rate > 1%
    - data_drift_score > 0.2
  response_time: 1_hour
  notification: slack

info_alerts:
  conditions:
    - feature_distribution_shift
    - traffic_pattern_change
    - new_category_detected
  response_time: 24_hours
  notification: email
```

### Implementation: Intelligent Alerting

```python
"""
Intelligent alerting system with noise reduction.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import json

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Alert:
    """Alert data structure."""
    id: str
    severity: AlertSeverity
    title: str
    description: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)
    runbook_url: Optional[str] = None

@dataclass
class AlertRule:
    """Define an alert rule."""
    name: str
    metric_name: str
    condition: Callable[[float], bool]
    severity: AlertSeverity
    description_template: str
    runbook_url: Optional[str] = None
    cooldown_minutes: int = 15
    consecutive_failures: int = 3

class AlertManager:
    """Manage alerts with noise reduction."""

    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.failure_counts: Dict[str, int] = {}
        self.last_alert_time: Dict[str, datetime] = {}
        self.notification_handlers: Dict[AlertSeverity, List[Callable]] = {
            AlertSeverity.INFO: [],
            AlertSeverity.WARNING: [],
            AlertSeverity.CRITICAL: []
        }

    def add_rule(self, rule: AlertRule):
        """Register an alert rule."""
        self.rules[rule.name] = rule
        self.failure_counts[rule.name] = 0

    def add_notification_handler(
        self,
        severity: AlertSeverity,
        handler: Callable[[Alert], None]
    ):
        """Add notification handler for severity level."""
        self.notification_handlers[severity].append(handler)

    def evaluate_metric(
        self,
        metric_name: str,
        value: float,
        labels: Dict[str, str] = None
    ):
        """Evaluate metric against all matching rules."""
        for rule_name, rule in self.rules.items():
            if rule.metric_name != metric_name:
                continue

            if rule.condition(value):
                self._handle_failure(rule, value, labels or {})
            else:
                self._handle_recovery(rule)

    def _handle_failure(
        self,
        rule: AlertRule,
        value: float,
        labels: Dict[str, str]
    ):
        """Handle rule failure."""
        self.failure_counts[rule.name] += 1

        # Check consecutive failures threshold
        if self.failure_counts[rule.name] < rule.consecutive_failures:
            return

        # Check cooldown
        last_time = self.last_alert_time.get(rule.name)
        if last_time:
            cooldown = timedelta(minutes=rule.cooldown_minutes)
            if datetime.utcnow() - last_time < cooldown:
                return

        # Create alert
        alert = Alert(
            id=f"{rule.name}_{datetime.utcnow().timestamp()}",
            severity=rule.severity,
            title=f"Alert: {rule.name}",
            description=rule.description_template.format(
                value=value,
                metric=rule.metric_name
            ),
            metric_name=rule.metric_name,
            current_value=value,
            threshold=0,  # Would be set from rule
            labels=labels,
            runbook_url=rule.runbook_url
        )

        # Store and notify
        self.active_alerts[rule.name] = alert
        self.alert_history.append(alert)
        self.last_alert_time[rule.name] = datetime.utcnow()

        self._send_notifications(alert)

    def _handle_recovery(self, rule: AlertRule):
        """Handle rule recovery."""
        self.failure_counts[rule.name] = 0

        if rule.name in self.active_alerts:
            del self.active_alerts[rule.name]

    def _send_notifications(self, alert: Alert):
        """Send notifications for alert."""
        handlers = self.notification_handlers[alert.severity]
        for handler in handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Notification handler failed: {e}")


# Notification handlers
def slack_notification(alert: Alert):
    """Send Slack notification."""
    import requests

    color_map = {
        AlertSeverity.INFO: "#36a64f",
        AlertSeverity.WARNING: "#ff9900",
        AlertSeverity.CRITICAL: "#ff0000"
    }

    payload = {
        "attachments": [{
            "color": color_map[alert.severity],
            "title": alert.title,
            "text": alert.description,
            "fields": [
                {"title": "Metric", "value": alert.metric_name, "short": True},
                {"title": "Value", "value": str(alert.current_value), "short": True}
            ],
            "footer": "ML Monitoring System",
            "ts": int(alert.timestamp.timestamp())
        }]
    }

    # requests.post(SLACK_WEBHOOK_URL, json=payload)
    print(f"[SLACK] {alert.severity.value}: {alert.title}")


def pagerduty_notification(alert: Alert):
    """Send PagerDuty notification for critical alerts."""
    import requests

    payload = {
        "routing_key": "YOUR_ROUTING_KEY",
        "event_action": "trigger",
        "dedup_key": alert.id,
        "payload": {
            "summary": alert.title,
            "severity": "critical",
            "source": "ml-monitoring",
            "custom_details": {
                "metric": alert.metric_name,
                "value": alert.current_value,
                "description": alert.description
            }
        },
        "links": [{
            "href": alert.runbook_url,
            "text": "Runbook"
        }] if alert.runbook_url else []
    }

    # requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)
    print(f"[PAGERDUTY] Critical: {alert.title}")


# Usage
alert_manager = AlertManager()

# Add rules
alert_manager.add_rule(AlertRule(
    name="high_error_rate",
    metric_name="prediction_error_rate",
    condition=lambda x: x > 0.05,
    severity=AlertSeverity.CRITICAL,
    description_template="Error rate {value:.2%} exceeds 5% threshold",
    runbook_url="https://wiki.company.com/ml-runbooks/high-error-rate",
    consecutive_failures=3
))

alert_manager.add_rule(AlertRule(
    name="model_accuracy_degradation",
    metric_name="model_accuracy",
    condition=lambda x: x < 0.85,
    severity=AlertSeverity.WARNING,
    description_template="Model accuracy dropped to {value:.2%}",
    consecutive_failures=5
))

# Register handlers
alert_manager.add_notification_handler(AlertSeverity.CRITICAL, slack_notification)
alert_manager.add_notification_handler(AlertSeverity.CRITICAL, pagerduty_notification)
alert_manager.add_notification_handler(AlertSeverity.WARNING, slack_notification)
```

---

## Module 4: A/B Testing for ML Models

### Statistical Framework

```yaml
experiment_design:
  minimum_detectable_effect: 0.02  # 2% improvement
  statistical_power: 0.80
  significance_level: 0.05

  sample_size_calculation:
    formula: "2 * (z_alpha + z_beta)^2 * variance / MDE^2"

  traffic_allocation:
    control: 50%
    treatment: 50%

  guardrail_metrics:
    - latency_p99_ms < 200
    - error_rate < 0.01
```

### Implementation: A/B Testing Framework

```python
"""
Statistical A/B testing framework for ML models.
"""
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

@dataclass
class ExperimentConfig:
    """A/B experiment configuration."""
    experiment_id: str
    control_model: str
    treatment_model: str
    traffic_split: float = 0.5
    min_sample_size: int = 1000
    significance_level: float = 0.05
    guardrails: Dict[str, Tuple[float, float]] = None

@dataclass
class ExperimentResult:
    """A/B experiment results."""
    experiment_id: str
    control_mean: float
    treatment_mean: float
    control_std: float
    treatment_std: float
    sample_size_control: int
    sample_size_treatment: int
    p_value: float
    confidence_interval: Tuple[float, float]
    lift: float
    is_significant: bool
    recommendation: str

class ABTestingFramework:
    """Statistical A/B testing for ML models."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.control_metrics: List[float] = []
        self.treatment_metrics: List[float] = []
        self.guardrail_violations: Dict[str, List[float]] = {}

    def assign_variant(self, user_id: str) -> str:
        """
        Deterministically assign user to variant.
        Uses consistent hashing for stable assignment.
        """
        hash_input = f"{self.config.experiment_id}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        normalized = (hash_value % 10000) / 10000

        if normalized < self.config.traffic_split:
            return "control"
        else:
            return "treatment"

    def record_metric(
        self,
        variant: str,
        metric_value: float,
        guardrail_metrics: Dict[str, float] = None
    ):
        """Record metric observation for variant."""
        if variant == "control":
            self.control_metrics.append(metric_value)
        else:
            self.treatment_metrics.append(metric_value)

        # Check guardrails
        if guardrail_metrics and self.config.guardrails:
            for metric_name, value in guardrail_metrics.items():
                if metric_name in self.config.guardrails:
                    min_val, max_val = self.config.guardrails[metric_name]
                    if value < min_val or value > max_val:
                        if metric_name not in self.guardrail_violations:
                            self.guardrail_violations[metric_name] = []
                        self.guardrail_violations[metric_name].append(value)

    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        power: float = 0.8,
        significance_level: float = 0.05
    ) -> int:
        """Calculate required sample size per variant."""
        z_alpha = stats.norm.ppf(1 - significance_level / 2)
        z_beta = stats.norm.ppf(power)

        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)

        pooled_p = (p1 + p2) / 2

        n = (2 * pooled_p * (1 - pooled_p) * (z_alpha + z_beta) ** 2) / \
            ((p1 - p2) ** 2)

        return int(np.ceil(n))

    def analyze(self) -> ExperimentResult:
        """Perform statistical analysis of experiment."""
        control = np.array(self.control_metrics)
        treatment = np.array(self.treatment_metrics)

        # Basic statistics
        control_mean = np.mean(control)
        treatment_mean = np.mean(treatment)
        control_std = np.std(control, ddof=1)
        treatment_std = np.std(treatment, ddof=1)

        # Welch's t-test (unequal variances)
        t_stat, p_value = stats.ttest_ind(
            treatment, control, equal_var=False
        )

        # Confidence interval for difference
        n1, n2 = len(control), len(treatment)
        se = np.sqrt(control_std**2/n1 + treatment_std**2/n2)
        z = stats.norm.ppf(1 - self.config.significance_level/2)
        diff = treatment_mean - control_mean
        ci = (diff - z*se, diff + z*se)

        # Lift calculation
        lift = (treatment_mean - control_mean) / control_mean if control_mean != 0 else 0

        # Significance
        is_significant = p_value < self.config.significance_level

        # Recommendation
        if len(control) < self.config.min_sample_size:
            recommendation = "CONTINUE: Insufficient sample size"
        elif self.guardrail_violations:
            recommendation = f"STOP: Guardrail violations detected: {list(self.guardrail_violations.keys())}"
        elif is_significant and lift > 0:
            recommendation = f"SHIP: Treatment wins with {lift:.2%} lift (p={p_value:.4f})"
        elif is_significant and lift < 0:
            recommendation = f"REVERT: Control wins, treatment shows {lift:.2%} regression"
        else:
            recommendation = "NO DECISION: Results not statistically significant"

        return ExperimentResult(
            experiment_id=self.config.experiment_id,
            control_mean=control_mean,
            treatment_mean=treatment_mean,
            control_std=control_std,
            treatment_std=treatment_std,
            sample_size_control=len(control),
            sample_size_treatment=len(treatment),
            p_value=p_value,
            confidence_interval=ci,
            lift=lift,
            is_significant=is_significant,
            recommendation=recommendation
        )

    def run_sequential_analysis(
        self,
        alpha_spending_function: str = "obrien_fleming"
    ) -> Dict[str, any]:
        """
        Sequential analysis for early stopping.
        Uses alpha spending to control false positive rate.
        """
        current_n = len(self.control_metrics) + len(self.treatment_metrics)
        max_n = self.config.min_sample_size * 2
        information_fraction = current_n / max_n

        # O'Brien-Fleming spending function
        if alpha_spending_function == "obrien_fleming":
            alpha_spent = 2 * (1 - stats.norm.cdf(
                stats.norm.ppf(1 - self.config.significance_level/2) /
                np.sqrt(information_fraction)
            ))
        else:
            alpha_spent = self.config.significance_level * information_fraction

        result = self.analyze()

        return {
            "can_stop_early": result.p_value < alpha_spent,
            "alpha_spent": alpha_spent,
            "information_fraction": information_fraction,
            "current_p_value": result.p_value,
            "result": result
        }


# Usage Example
config = ExperimentConfig(
    experiment_id="model_v2_vs_v1_conversion",
    control_model="fraud_detector_v1",
    treatment_model="fraud_detector_v2",
    traffic_split=0.5,
    min_sample_size=5000,
    guardrails={
        "latency_p99_ms": (0, 200),
        "error_rate": (0, 0.01)
    }
)

ab_test = ABTestingFramework(config)

# Simulate recording metrics
np.random.seed(42)
for i in range(10000):
    user_id = f"user_{i}"
    variant = ab_test.assign_variant(user_id)

    # Simulate conversion rates
    if variant == "control":
        converted = np.random.binomial(1, 0.10)  # 10% baseline
    else:
        converted = np.random.binomial(1, 0.11)  # 11% treatment (10% lift)

    ab_test.record_metric(
        variant=variant,
        metric_value=converted,
        guardrail_metrics={"latency_p99_ms": np.random.normal(100, 20)}
    )

# Analyze results
result = ab_test.analyze()
print(f"Recommendation: {result.recommendation}")
print(f"Lift: {result.lift:.2%}")
print(f"P-value: {result.p_value:.4f}")
print(f"95% CI: [{result.confidence_interval[0]:.4f}, {result.confidence_interval[1]:.4f}]")
```

---

## Module 5: Root Cause Analysis

### Decision Tree: Model Degradation

```
Model Performance Degraded?
├── YES
│   ├── Check Data Drift
│   │   ├── Drift Detected
│   │   │   ├── Feature drift → Investigate upstream data sources
│   │   │   ├── Target drift → Market/behavior shift
│   │   │   └── Concept drift → Retrain with recent data
│   │   └── No Drift
│   │       ├── Check Infrastructure
│   │       │   ├── Latency spike → Scale resources
│   │       │   ├── Memory pressure → Optimize batch size
│   │       │   └── GPU utilization low → Check data loading
│   │       └── Check Model
│   │           ├── Feature engineering bug → Review pipeline
│   │           ├── Model config changed → Audit deployment
│   │           └── Dependency version → Check requirements
│   └── Check Traffic Patterns
│       ├── Traffic spike → Scale horizontally
│       └── New user segment → Evaluate model coverage
└── NO
    └── Continue monitoring
```

### Automated Root Cause Analysis

```python
"""
Automated root cause analysis for ML systems.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum
import pandas as pd

class RootCause(Enum):
    DATA_DRIFT = "data_drift"
    TARGET_DRIFT = "target_drift"
    CONCEPT_DRIFT = "concept_drift"
    INFRASTRUCTURE = "infrastructure"
    MODEL_BUG = "model_bug"
    TRAFFIC_PATTERN = "traffic_pattern"
    UNKNOWN = "unknown"

@dataclass
class DiagnosticResult:
    """Result of diagnostic check."""
    check_name: str
    passed: bool
    details: Dict
    severity: str
    remediation: str

@dataclass
class RCAReport:
    """Root cause analysis report."""
    primary_cause: RootCause
    confidence: float
    diagnostics: List[DiagnosticResult]
    recommended_actions: List[str]
    timeline: List[Dict]

class RootCauseAnalyzer:
    """Automated root cause analysis."""

    def __init__(self):
        self.diagnostics: List[Callable] = []
        self.results: List[DiagnosticResult] = []

    def add_diagnostic(self, diagnostic_fn: Callable):
        """Register diagnostic check."""
        self.diagnostics.append(diagnostic_fn)

    def run_analysis(
        self,
        metrics_df: pd.DataFrame,
        drift_results: Dict,
        infra_metrics: Dict
    ) -> RCAReport:
        """Run all diagnostics and determine root cause."""

        self.results = []

        # Run all diagnostics
        for diagnostic in self.diagnostics:
            result = diagnostic(metrics_df, drift_results, infra_metrics)
            self.results.append(result)

        # Determine primary cause
        primary_cause, confidence = self._determine_cause()

        # Generate recommendations
        recommendations = self._generate_recommendations(primary_cause)

        # Build timeline
        timeline = self._build_timeline(metrics_df)

        return RCAReport(
            primary_cause=primary_cause,
            confidence=confidence,
            diagnostics=self.results,
            recommended_actions=recommendations,
            timeline=timeline
        )

    def _determine_cause(self) -> tuple[RootCause, float]:
        """Determine most likely root cause."""
        failed_checks = [r for r in self.results if not r.passed]

        if not failed_checks:
            return RootCause.UNKNOWN, 0.0

        # Priority-based cause determination
        cause_priority = {
            "data_drift": RootCause.DATA_DRIFT,
            "target_drift": RootCause.TARGET_DRIFT,
            "infrastructure": RootCause.INFRASTRUCTURE,
            "model_validation": RootCause.MODEL_BUG,
            "traffic": RootCause.TRAFFIC_PATTERN
        }

        for check_prefix, cause in cause_priority.items():
            matching = [r for r in failed_checks if check_prefix in r.check_name.lower()]
            if matching:
                severity_score = sum(
                    {"critical": 3, "warning": 2, "info": 1}.get(r.severity, 0)
                    for r in matching
                )
                confidence = min(0.95, 0.5 + severity_score * 0.15)
                return cause, confidence

        return RootCause.UNKNOWN, 0.3

    def _generate_recommendations(self, cause: RootCause) -> List[str]:
        """Generate remediation recommendations."""
        recommendations = {
            RootCause.DATA_DRIFT: [
                "1. Identify drifted features using drift report",
                "2. Investigate upstream data source changes",
                "3. Consider retraining with recent data window",
                "4. Implement feature monitoring alerts"
            ],
            RootCause.TARGET_DRIFT: [
                "1. Analyze target distribution shift",
                "2. Check for seasonality or market changes",
                "3. Update training data with recent labels",
                "4. Consider online learning approach"
            ],
            RootCause.INFRASTRUCTURE: [
                "1. Check resource utilization (CPU/GPU/Memory)",
                "2. Review recent deployment changes",
                "3. Scale resources if needed",
                "4. Check for dependency version conflicts"
            ],
            RootCause.MODEL_BUG: [
                "1. Review recent model/pipeline changes",
                "2. Validate feature engineering logic",
                "3. Check model artifact integrity",
                "4. Run model validation tests"
            ],
            RootCause.TRAFFIC_PATTERN: [
                "1. Analyze traffic distribution changes",
                "2. Check for new user segments",
                "3. Validate model coverage for edge cases",
                "4. Consider segment-specific models"
            ],
            RootCause.UNKNOWN: [
                "1. Review all system logs",
                "2. Check recent changes across stack",
                "3. Engage cross-functional team",
                "4. Consider manual investigation"
            ]
        }
        return recommendations.get(cause, recommendations[RootCause.UNKNOWN])

    def _build_timeline(self, metrics_df: pd.DataFrame) -> List[Dict]:
        """Build timeline of events."""
        # Simplified timeline - would use actual metrics in production
        return [
            {"timestamp": "T-24h", "event": "Baseline metrics normal"},
            {"timestamp": "T-12h", "event": "First anomaly detected"},
            {"timestamp": "T-6h", "event": "Performance degradation confirmed"},
            {"timestamp": "T-0h", "event": "RCA initiated"}
        ]


# Diagnostic functions
def check_data_drift(
    metrics_df: pd.DataFrame,
    drift_results: Dict,
    infra_metrics: Dict
) -> DiagnosticResult:
    """Check for data drift."""
    drift_score = drift_results.get("drift_share", 0)

    return DiagnosticResult(
        check_name="data_drift_check",
        passed=drift_score < 0.2,
        details={"drift_score": drift_score, "drifted_features": drift_results.get("drifted_columns", [])},
        severity="critical" if drift_score > 0.5 else "warning" if drift_score > 0.2 else "info",
        remediation="Investigate drifted features and consider retraining"
    )

def check_infrastructure(
    metrics_df: pd.DataFrame,
    drift_results: Dict,
    infra_metrics: Dict
) -> DiagnosticResult:
    """Check infrastructure health."""
    cpu_util = infra_metrics.get("cpu_utilization", 0)
    memory_util = infra_metrics.get("memory_utilization", 0)
    latency_p99 = infra_metrics.get("latency_p99_ms", 0)

    issues = []
    if cpu_util > 90:
        issues.append(f"High CPU: {cpu_util}%")
    if memory_util > 90:
        issues.append(f"High Memory: {memory_util}%")
    if latency_p99 > 500:
        issues.append(f"High Latency: {latency_p99}ms")

    return DiagnosticResult(
        check_name="infrastructure_check",
        passed=len(issues) == 0,
        details={"cpu": cpu_util, "memory": memory_util, "latency_p99": latency_p99, "issues": issues},
        severity="critical" if len(issues) > 1 else "warning" if issues else "info",
        remediation="Scale resources or optimize model serving"
    )


# Usage
analyzer = RootCauseAnalyzer()
analyzer.add_diagnostic(check_data_drift)
analyzer.add_diagnostic(check_infrastructure)

# Run analysis
# report = analyzer.run_analysis(metrics_df, drift_results, infra_metrics)
```

---

## Troubleshooting Guide

### Common Issues

#### Issue: High False Positive Rate in Drift Detection

**Symptoms**:
- Frequent drift alerts without actual model degradation
- Alert fatigue from monitoring system

**Diagnosis**:
```bash
# Check drift threshold settings
grep -r "drift_threshold" config/

# Review historical drift scores
SELECT date, drift_score, model_accuracy
FROM ml_metrics
WHERE date > NOW() - INTERVAL '7 days'
ORDER BY date;
```

**Resolution**:
1. Increase drift threshold from 0.1 to 0.15
2. Implement consecutive failure requirement (3+ failures)
3. Use statistical significance testing before alerting
4. Add cooldown periods between alerts

#### Issue: Delayed Ground Truth Labels

**Symptoms**:
- Performance metrics unavailable for hours/days
- Cannot detect model degradation quickly

**Diagnosis**:
```python
# Check label delay distribution
label_delays = df['label_timestamp'] - df['prediction_timestamp']
print(f"Median delay: {label_delays.median()}")
print(f"P95 delay: {label_delays.quantile(0.95)}")
```

**Resolution**:
1. Implement proxy metrics (confidence scores, prediction distribution)
2. Use weak supervision for faster labeling
3. Create synthetic ground truth from business rules
4. Deploy shadow models for comparison

#### Issue: A/B Test Shows No Significance

**Symptoms**:
- P-value stuck above significance level
- Experiment running longer than expected

**Diagnosis**:
```python
# Check statistical power
from statsmodels.stats.power import TTestIndPower
power_analysis = TTestIndPower()
required_n = power_analysis.solve_power(
    effect_size=0.1,
    power=0.8,
    alpha=0.05
)
print(f"Required sample size per group: {required_n}")
```

**Resolution**:
1. Verify minimum detectable effect is realistic
2. Increase traffic allocation to experiment
3. Extend experiment duration
4. Consider alternative metrics with higher signal

### Debug Checklist

```yaml
monitoring_debug_checklist:
  metrics_collection:
    - [ ] Metrics endpoint returning 200
    - [ ] Prometheus scraping successfully
    - [ ] No gaps in time series data
    - [ ] Labels correctly applied

  drift_detection:
    - [ ] Reference data loaded correctly
    - [ ] Feature columns match between ref and current
    - [ ] Statistical tests appropriate for data types
    - [ ] Threshold values reasonable

  alerting:
    - [ ] Alert rules syntax valid
    - [ ] Notification channels configured
    - [ ] Cooldown periods appropriate
    - [ ] Runbooks linked and accessible

  ab_testing:
    - [ ] Traffic split working correctly
    - [ ] User assignment deterministic
    - [ ] Metrics tracking both variants
    - [ ] Guardrails configured
```

---

## Quick Reference

### Essential Commands

```bash
# Check Evidently drift report
python -m evidently.ui.app --project-path ./evidently_workspace

# Prometheus metrics query
curl -s localhost:9090/api/v1/query?query=ml_prediction_latency_seconds

# Start monitoring stack
docker-compose -f monitoring-stack.yml up -d

# Run drift detection job
python scripts/run_drift_detection.py --date $(date +%Y-%m-%d)
```

### Metric Naming Conventions

```yaml
prometheus_naming:
  format: "{domain}_{metric}_{unit}"
  examples:
    - ml_prediction_latency_seconds
    - ml_model_accuracy_ratio
    - ml_drift_score_ratio
    - ml_feature_value_total
```

### Integration Points

```yaml
upstream_dependencies:
  - feature_store: feast
  - model_registry: mlflow
  - data_warehouse: snowflake

downstream_consumers:
  - alerting: pagerduty, slack
  - visualization: grafana
  - analytics: datadog
```
