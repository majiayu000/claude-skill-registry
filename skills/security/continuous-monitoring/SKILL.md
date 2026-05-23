---
name: continuous-monitoring
version: "2.0.0"
description: Real-time monitoring and detection of adversarial attacks and model drift in production
sasmp_version: "1.3.0"
bonded_agent: 05-defense-strategy-developer
bond_type: SECONDARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [monitoring_type]
  properties:
    monitoring_type:
      type: string
      enum: [input_anomaly, output_quality, model_drift, security_events, all]
    alert_threshold:
      type: number
      default: 0.8
output_schema:
  type: object
  properties:
    alerts:
      type: array
    metrics:
      type: object
    recommendations:
      type: array
# Framework Mappings
owasp_llm_2025: [LLM10, LLM02]
nist_ai_rmf: [Measure, Manage]
---

# Continuous Monitoring

Implement **real-time detection** of adversarial attacks and model degradation in production AI systems.

## Quick Reference

```yaml
Skill:       continuous-monitoring
Agent:       05-defense-strategy-developer
OWASP:       LLM10 (Unbounded Consumption), LLM02 (Sensitive Disclosure)
NIST:        Measure, Manage
Use Case:    Detect attacks and drift in production
```

## Monitoring Architecture

```
User Input → [Input Monitor] → [Model] → [Output Monitor] → Response
                  ↓                              ↓
            [Anomaly Detection]          [Quality Check]
                  ↓                              ↓
            [Alert System] ←←←←←←←←←←←←←←←←←←←←←←
                  ↓
            [Incident Response]
```

## Detection Categories

### 1. Input Anomaly Detection

```yaml
Category: input_anomaly
Latency Impact: 10-20ms
Detection Rate: 85-95%
```

```python
class InputAnomalyDetector:
    def __init__(self, training_distribution):
        self.mean = training_distribution.mean
        self.cov = training_distribution.covariance
        self.threshold = 3.0  # Standard deviations

    def detect(self, input_embedding):
        # Mahalanobis distance from training distribution
        diff = input_embedding - self.mean
        distance = np.sqrt(diff.T @ np.linalg.inv(self.cov) @ diff)

        if distance > self.threshold:
            return AnomalyAlert(
                type="out_of_distribution",
                score=distance,
                severity=self._classify_severity(distance)
            )
        return None

    def detect_injection(self, text_input):
        # Pattern-based injection detection
        injection_patterns = [
            r'ignore\s+(previous|all)\s+instructions',
            r'system\s*:\s*',
            r'(admin|developer)\s+mode',
        ]
        for pattern in injection_patterns:
            if re.search(pattern, text_input, re.I):
                return AnomalyAlert(type="injection_attempt", severity="HIGH")
        return None
```

### 2. Output Quality Monitoring

```yaml
Category: output_quality
Metrics: [confidence, coherence, toxicity, latency]
```

```python
class OutputQualityMonitor:
    def __init__(self, config):
        self.confidence_threshold = config.get('confidence', 0.5)
        self.toxicity_threshold = config.get('toxicity', 0.1)
        self.latency_threshold_ms = config.get('latency', 5000)

    def check(self, response, metadata):
        alerts = []

        # Low confidence check
        if metadata.confidence < self.confidence_threshold:
            alerts.append(Alert("low_confidence", metadata.confidence))

        # Toxicity check
        toxicity_score = self.toxicity_classifier(response)
        if toxicity_score > self.toxicity_threshold:
            alerts.append(Alert("high_toxicity", toxicity_score))

        # Latency check
        if metadata.latency_ms > self.latency_threshold_ms:
            alerts.append(Alert("high_latency", metadata.latency_ms))

        # Coherence check
        coherence = self.coherence_scorer(response)
        if coherence < 0.7:
            alerts.append(Alert("low_coherence", coherence))

        return alerts
```

### 3. Model Drift Detection

```yaml
Category: model_drift
Types: [data_drift, concept_drift, prediction_drift]
```

```python
class DriftDetector:
    def __init__(self, baseline_window=1000):
        self.baseline_window = baseline_window
        self.baseline_inputs = []
        self.baseline_outputs = []

    def detect_data_drift(self, current_inputs):
        """Detect drift in input distribution"""
        if len(self.baseline_inputs) < self.baseline_window:
            self.baseline_inputs.extend(current_inputs)
            return None

        # KL divergence between distributions
        baseline_dist = self._estimate_distribution(self.baseline_inputs)
        current_dist = self._estimate_distribution(current_inputs)
        kl_div = self._kl_divergence(baseline_dist, current_dist)

        if kl_div > 0.1:
            return DriftAlert("data_drift", kl_div)
        return None

    def detect_concept_drift(self, predictions, ground_truth):
        """Detect drift in model performance"""
        # Track accuracy over sliding windows
        recent_accuracy = self._compute_accuracy(predictions, ground_truth)
        baseline_accuracy = self._baseline_accuracy()

        if baseline_accuracy - recent_accuracy > 0.05:
            return DriftAlert("concept_drift", recent_accuracy)
        return None
```

### 4. Security Event Monitoring

```yaml
Category: security_events
Events: [extraction_attempt, jailbreak, rate_abuse]
```

```python
class SecurityMonitor:
    def __init__(self):
        self.query_history = defaultdict(list)
        self.extraction_patterns = []

    def detect_extraction(self, user_id, queries):
        """Detect model extraction attempts"""
        history = self.query_history[user_id]
        history.extend(queries)

        # Check for systematic querying patterns
        if len(history) > 1000:  # High volume
            diversity = self._query_diversity(history)
            if diversity > 0.9:  # Very diverse
                return SecurityAlert("extraction_attempt", user_id)

        return None

    def detect_abuse(self, user_id, request_timestamps):
        """Detect rate limit abuse"""
        window = 60  # 1 minute
        recent = [t for t in request_timestamps if time.time() - t < window]

        if len(recent) > 100:  # Too many requests
            return SecurityAlert("rate_abuse", user_id, len(recent))
        return None
```

## Alert Configuration

```yaml
Alert Thresholds:
  input_anomaly:
    warning: 2.5  # standard deviations
    critical: 4.0

  output_toxicity:
    warning: 0.3
    critical: 0.7

  model_drift:
    warning: 0.05  # 5% accuracy drop
    critical: 0.10

  extraction_queries:
    warning: 500/hour
    critical: 1000/hour
```

## Dashboard Metrics

```
┌──────────────────────────────────────────────────────────┐
│ REAL-TIME MONITORING DASHBOARD                           │
├──────────────────────────────────────────────────────────┤
│ Input Anomalies (1hr):  ████░░░░ 12 (2.4%)              │
│ Output Toxicity (1hr):  █░░░░░░░  3 (0.6%)              │
│ Model Latency P99:      ████████ 2.3s                   │
│ Drift Score:            ██░░░░░░ 0.02 (OK)              │
│ Security Alerts:        ░░░░░░░░ 0                       │
└──────────────────────────────────────────────────────────┘
```

## Troubleshooting

```yaml
Issue: Too many false positive alerts
Solution: Tune thresholds, add allowlists, improve baseline

Issue: Missing attack detection
Solution: Expand detection patterns, lower thresholds

Issue: High monitoring latency
Solution: Use sampling, async processing, optimize detectors
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 05 | Configures monitoring |
| Agent 08 | CI/CD integration |
| /report | Monitoring reports |
| Prometheus/Grafana | Metrics visualization |

---

**Detect attacks and drift with real-time AI monitoring.**
