---
name: aiops
description: Generic AIOps (AI for IT Operations) patterns and best practices for 2025. Provides comprehensive implementation strategies for intelligent monitoring, automation, incident response, and observability across any infrastructure. Framework-agnostic approach supporting multiple monitoring platforms, cloud providers, and automation tools.
license: MIT
---

# AIOps - AI for IT Operations

This skill provides comprehensive patterns for implementing AIOps strategies in 2025, including intelligent monitoring, automated incident response, predictive analytics, and observability best practices. The patterns are designed to be framework-agnostic and applicable across different infrastructure platforms.

## When to Use This Skill

Use this skill when you need to:
- Implement AIOps strategies for modern infrastructure
- Build intelligent monitoring and alerting systems
- Create automated incident response workflows
- Deploy predictive maintenance solutions
- Implement self-healing capabilities
- Build observability platforms with AI/ML
- Optimize multi-cloud operations
- Create chaos engineering practices
- Implement generative AI for operations
- Build digital twins for infrastructure

## 1. AIOps Architecture Patterns

### Core AIOps Platform Architecture

```python
# aiops/core/architecture.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class IncidentStatus(str, Enum):
    """Incident status"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class Metric:
    """Metric data point"""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    source: str = ""
    unit: str = ""

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: datetime
    level: str
    message: str
    service: str
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    stack_trace: Optional[str] = None

@dataclass
class Trace:
    """Distributed trace data"""
    trace_id: str
    spans: List[Dict[str, Any]]
    duration: timedelta
    service_map: Dict[str, List[str]]
    error_count: int = 0

@dataclass
class Alert:
    """Alert representation"""
    id: str
    name: str
    severity: AlertSeverity
    status: IncidentStatus
    description: str
    source: str
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    fingerprint: str = ""
    related_entities: List[str] = field(default_factory=list)

class DataSource(ABC):
    """Abstract data source interface"""

    @abstractmethod
    async def collect_metrics(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Metric]:
        """Collect metrics from data source"""
        pass

    @abstractmethod
    async def query_logs(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100
    ) -> List[LogEntry]:
        """Query logs from data source"""
        pass

    @abstractmethod
    async def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get trace data"""
        pass

class AIOpsEngine:
    """Core AIOps processing engine"""

    def __init__(self):
        self.data_sources: List[DataSource] = []
        self.alert_processors: List[AlertProcessor] = []
        self.ml_models: Dict[str, Any] = {}
        self.knowledge_base: KnowledgeBase = KnowledgeBase()
        self.automation_engine = AutomationEngine()

    def register_data_source(self, data_source: DataSource) -> None:
        """Register a data source"""
        self.data_sources.append(data_source)
        logger.info(f"Registered data source: {type(data_source).__name__}")

    def register_alert_processor(self, processor: 'AlertProcessor') -> None:
        """Register an alert processor"""
        self.alert_processors.append(processor)
        logger.info(f"Registered alert processor: {type(processor).__name__}")

    async def process_alert(self, alert: Alert) -> Dict[str, Any]:
        """Process incoming alert through AIOps pipeline"""
        logger.info(f"Processing alert: {alert.id} - {alert.name}")

        # 1. Enrich alert with context
        enriched_alert = await self._enrich_alert(alert)

        # 2. Run through ML models for classification and prediction
        analysis = await self._analyze_alert(enriched_alert)

        # 3. Determine appropriate response
        response_plan = await self._generate_response_plan(enriched_alert, analysis)

        # 4. Execute automated actions if applicable
        if response_plan.get("auto_execute", False):
            await self._execute_response(enriched_alert, response_plan)

        # 5. Update knowledge base
        await self.knowledge_base.update_from_alert(enriched_alert, analysis, response_plan)

        return {
            "alert_id": alert.id,
            "status": "processed",
            "analysis": analysis,
            "response_plan": response_plan
        }

    async def _enrich_alert(self, alert: Alert) -> Alert:
        """Enrich alert with additional context"""
        # Get related metrics
        for source in self.data_sources:
            try:
                metrics = await source.collect_metrics(
                    query=f"{alert.name}[5m]",
                    start_time=alert.timestamp - timedelta(minutes=5),
                    end_time=alert.timestamp
                )

                # Add metrics to alert annotations
                alert.annotations[f"metrics_{type(source).__name__}"] = json.dumps([
                    {"name": m.name, "value": m.value} for m in metrics
                ])
            except Exception as e:
                logger.error(f"Failed to enrich alert with metrics: {e}")

        # Get related logs
        for source in self.data_sources:
            try:
                logs = await source.query_logs(
                    query=f"service:{alert.source} level:error",
                    start_time=alert.timestamp - timedelta(minutes=5),
                    end_time=alert.timestamp,
                    limit=10
                )

                # Add logs to alert context
                alert.annotations["recent_errors"] = json.dumps([
                    {"timestamp": l.timestamp.isoformat(), "message": l.message}
                    for l in logs
                ])
            except Exception as e:
                logger.error(f"Failed to enrich alert with logs: {e}")

        return alert

    async def _analyze_alert(self, alert: Alert) -> Dict[str, Any]:
        """Analyze alert using ML models"""
        analysis = {
            "classification": None,
            "severity_score": 0.0,
            "predicted_impact": "low",
            "recommendations": [],
            "related_incidents": []
        }

        # Classification model
        if "classification" in self.ml_models:
            features = self._extract_features(alert)
            analysis["classification"] = self.ml_models["classification"].predict([features])[0]

        # Severity prediction
        if "severity" in self.ml_models:
            features = self._extract_features(alert)
            analysis["severity_score"] = self.ml_models["severity"].predict_proba([features])[0][1]

        # Impact prediction
        if "impact" in self.ml_models:
            features = self._extract_features(alert)
            analysis["predicted_impact"] = self.ml_models["impact"].predict([features])[0]

        # Find related incidents from knowledge base
        analysis["related_incidents"] = await self.knowledge_base.find_similar_incidents(alert)

        return analysis

    async def _generate_response_plan(
        self,
        alert: Alert,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate automated response plan"""
        plan = {
            "priority": alert.severity,
            "actions": [],
            "escalation_rules": [],
            "auto_execute": False,
            "estimated_resolution_time": None
        }

        # Determine if auto-execution is safe
        if (analysis["classification"] in ["known_issue", "false_positive"] and
            alert.severity in [AlertSeverity.LOW, AlertSeverity.MEDIUM]):
            plan["auto_execute"] = True

        # Generate actions based on classification
        classification = analysis.get("classification")

        if classification == "resource_exhaustion":
            plan["actions"].append({
                "type": "scale",
                "target": alert.source,
                "params": {"replicas": "+20%"}
            })
            plan["actions"].append({
                "type": "notify",
                "channel": "devops",
                "message": f"Resource exhaustion detected in {alert.source}"
            })

        elif classification == "known_issue":
            # Apply known fix
            known_fix = await self.knowledge_base.get_known_fix(alert.name)
            if known_fix:
                plan["actions"].append(known_fix)

        elif classification == "false_positive":
            plan["actions"].append({
                "type": "suppress",
                "duration": "1h",
                "reason": "False positive detected"
            })

        # Add escalation rules
        if alert.severity == AlertSeverity.CRITICAL:
            plan["escalation_rules"].append({
                "condition": "no_response_5m",
                "action": "escalate_to_oncall",
                "timeout": 300
            })

        return plan

    def _extract_features(self, alert: Alert) -> List[float]:
        """Extract features for ML models"""
        # Simple feature extraction - in production, use more sophisticated methods
        features = [
            float(alert.severity == AlertSeverity.CRITICAL),
            float(alert.severity == AlertSeverity.HIGH),
            float(alert.severity == AlertSeverity.MEDIUM),
            len(alert.description),
            len(alert.labels),
            alert.timestamp.hour / 24.0,
            alert.timestamp.weekday() / 7.0
        ]
        return features

    async def _execute_response(
        self,
        alert: Alert,
        response_plan: Dict[str, Any]
    ) -> None:
        """Execute automated response actions"""
        for action in response_plan.get("actions", []):
            try:
                await self.automation_engine.execute(action)
                logger.info(f"Executed action for alert {alert.id}: {action['type']}")
            except Exception as e:
                logger.error(f"Failed to execute action: {e}")
```

### Monitoring Platform Integrations

```python
# aiops/integrations/monitoring.py
import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.architecture import DataSource, Metric, LogEntry, Trace, Alert

class PrometheusDataSource(DataSource):
    """Prometheus metrics integration"""

    def __init__(self, url: str):
        self.url = url.rstrip("/")
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def collect_metrics(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Metric]:
        """Query Prometheus for metrics"""
        session = await self._get_session()

        params = {
            "query": query,
            "start": start_time.timestamp(),
            "end": end_time.timestamp(),
            "step": "15s"
        }

        url = f"{self.url}/api/v1/query_range"

        async with session.get(url, params=params) as response:
            data = await response.json()
            metrics = []

            if data["status"] == "success":
                result = data["data"]
                if result["resultType"] == "matrix":
                    for series in result["result"]:
                        labels = series["metric"]
                        values = series["values"]

                        for timestamp, value in values:
                            metrics.append(Metric(
                                name=query,
                                value=float(value),
                                timestamp=datetime.fromtimestamp(float(timestamp)),
                                labels=labels,
                                source="prometheus"
                            ))

            return metrics

    async def query_logs(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100
    ) -> List[LogEntry]:
        """Prometheus doesn't store logs - use Loki integration"""
        return []

    async def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Prometheus doesn't store traces - use Jaeger/Tempo integration"""
        return None

class LokiDataSource(DataSource):
    """Loki log aggregation integration"""

    def __init__(self, url: str):
        self.url = url.rstrip("/")
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def collect_metrics(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Metric]:
        """Loki doesn't store metrics"""
        return []

    async def query_logs(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100
    ) -> List[LogEntry]:
        """Query Loki for logs"""
        session = await self._get_session()

        params = {
            "query": query,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "limit": str(limit)
        }

        url = f"{self.url}/loki/api/v1/query_range"

        async with session.get(url, params=params) as response:
            data = await response.json()
            logs = []

            if data["status"] == "success":
                result = data["data"]
                for series in result["result"]:
                    stream = series["stream"]
                    for timestamp, line in series["values"]:
                        logs.append(LogEntry(
                            timestamp=datetime.fromtimestamp(float(timestamp) / 1e9),
                            level=stream.get("level", "info"),
                            message=line,
                            service=stream.get("service", "unknown"),
                            labels=stream
                        ))

            return logs

    async def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Loki doesn't store traces"""
        return None

class JaegerDataSource(DataSource):
    """Jaeger distributed tracing integration"""

    def __init__(self, url: str):
        self.url = url.rstrip("/")
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def collect_metrics(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Metric]:
        """Jaeger doesn't store metrics"""
        return []

    async def query_logs(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100
    ) -> List[LogEntry]:
        """Jaeger doesn't store logs"""
        return []

    async def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get trace from Jaeger"""
        session = await self._get_session()

        url = f"{self.url}/api/traces/{trace_id}"

        async with session.get(url) as response:
            data = await response.json()

            if data["data"] and data["data"][0]["spans"]:
                spans = data["data"][0]["spans"]
                service_map = {}
                error_count = 0

                for span in spans:
                    service = span["process"]["serviceName"]
                    if service not in service_map:
                        service_map[service] = []
                    service_map[service].append(span["spanID"])

                    if span.get("tags"):
                        for tag in span["tags"]:
                            if tag.get("key") == "error" and tag.get("value"):
                                error_count += 1

                return Trace(
                    trace_id=trace_id,
                    spans=spans,
                    duration=timedelta(
                        microseconds=data["data"][0]["duration"]
                    ),
                    service_map=service_map,
                    error_count=error_count
                )

            return None

class DatadogDataSource(DataSource):
    """Datadog APM integration"""

    def __init__(self, api_key: str, app_key: str, site: str = "datadoghq.com"):
        self.api_key = api_key
        self.app_key = app_key
        self.site = site
        self.base_url = f"https://api.{site}"
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            headers = {
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key
            }
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session

    async def collect_metrics(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Metric]:
        """Query Datadog metrics"""
        session = await self._get_session()

        params = {
            "query": query,
            "from": int(start_time.timestamp()),
            "to": int(end_time.timestamp())
        }

        url = f"{self.base_url}/api/v1/query"

        async with session.get(url, params=params) as response:
            data = await response.json()
            metrics = []

            if "series" in data:
                for series in data["series"]:
                    for point in series["pointlist"]:
                        metrics.append(Metric(
                            name=series["metric"],
                            value=point[1],
                            timestamp=datetime.fromtimestamp(point[0]),
                            labels={k: str(v) for k, v in series["tag_set"].items()},
                            source="datadog",
                            unit=series.get("unit", "")
                        ))

            return metrics

    async def query_logs(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100
    ) -> List[LogEntry]:
        """Query Datadog logs"""
        session = await self._get_session()

        payload = {
            "query": query,
            "time": {
                "from": start_time.isoformat(),
                "to": end_time.isoformat()
            },
            "limit": limit
        }

        url = f"{self.base_url}/api/v2/logs/events/search"

        async with session.post(url, json=payload) as response:
            data = await response.json()
            logs = []

            for log in data.get("data", []):
                attributes = log.get("attributes", {})

                logs.append(LogEntry(
                    timestamp=datetime.fromisoformat(attributes["timestamp"]),
                    level=attributes.get("status", "info"),
                    message=attributes.get("message", ""),
                    service=attributes.get("service", "unknown"),
                    trace_id=attributes.get("trace_id"),
                    labels=attributes.get("tags", [])
                ))

            return logs

    async def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get trace from Datadog"""
        session = await self._get_session()

        url = f"{self.base_url}/api/v1/trace/{trace_id}"

        async with session.get(url) as response:
            data = await response.json()

            # Parse Datadog trace format
            # Implementation depends on Datadog API response structure
            return None
```

## 2. Machine Learning for Operations

### Anomaly Detection Models

```python
# aiops/ml/anomaly_detection.py
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import asyncio
from collections import deque

class AnomalyDetector:
    """Generic anomaly detection for metrics and logs"""

    def __init__(self, model_type: str = "isolation_forest"):
        self.model_type = model_type
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.is_trained: Dict[str, bool] = {}
        self.feature_history: Dict[str, deque] = {}

    async def detect_metric_anomaly(
        self,
        metric_name: str,
        current_value: float,
        historical_values: List[float],
        window_size: int = 100
    ) -> Tuple[bool, float]:
        """Detect anomalies in time series metrics"""
        if metric_name not in self.models:
            await self._train_metric_model(metric_name, historical_values)

        # Prepare features
        features = self._extract_time_series_features(
            current_value,
            historical_values,
            window_size
        )

        # Scale features
        if metric_name in self.scalers:
            features = self.scalers[metric_name].transform([features])

        # Predict anomaly
        model = self.models[metric_name]
        anomaly_score = model.decision_function([features])[0]
        is_anomaly = model.predict([features])[0] == -1

        return is_anomaly, float(anomaly_score)

    async def detect_log_anomaly(
        self,
        log_entries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in log patterns"""
        # Extract log features
        features = []
        for entry in log_entries:
            features.append([
                len(entry.get("message", "")),
                entry.get("level_numeric", 0),
                entry.get("hour_of_day", 0),
                entry.get("day_of_week", 0)
            ])

        features = np.array(features)

        # Train or use existing model
        model_name = "log_patterns"
        if model_name not in self.models:
            self.models[model_name] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            self.models[model_name].fit(features)

        # Predict anomalies
        predictions = self.models[model_name].predict(features)
        scores = self.models[model_name].decision_function(features)

        # Return anomalous logs
        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Anomaly
                anomalies.append({
                    "log_index": i,
                    "log_entry": log_entries[i],
                    "anomaly_score": float(score),
                    "reason": "Unusual log pattern detected"
                })

        return anomalies

    async def detect_performance_anomaly(
        self,
        metrics: Dict[str, List[float]],
        threshold: float = 0.1
    ) -> Dict[str, Dict[str, Any]]:
        """Detect performance anomalies across multiple metrics"""
        results = {}

        for metric_name, values in metrics.items():
            if len(values) < 10:
                continue

            # Calculate statistical anomalies
            mean_val = np.mean(values)
            std_val = np.std(values)
            recent_values = values[-5:]

            for i, value in enumerate(recent_values):
                z_score = abs(value - mean_val) / (std_val + 1e-8)

                if z_score > 3:  # Statistical outlier
                    if metric_name not in results:
                        results[metric_name] = {
                            "anomalies": [],
                            "severity": "medium"
                        }

                    results[metric_name]["anomalies"].append({
                        "value": value,
                        "z_score": z_score,
                        "index": i,
                        "type": "statistical"
                    })

        return results

    async def _train_metric_model(
        self,
        metric_name: str,
        values: List[float]
    ) -> None:
        """Train anomaly detection model for a metric"""
        if len(values) < 30:
            # Not enough data for training
            return

        # Prepare training data
        training_features = []
        for i in range(10, len(values)):
            # Create window of previous values
            window = values[i-10:i]
            features = [
                np.mean(window),
                np.std(window),
                values[i],  # Current value
                (values[i] - np.mean(window)) / (np.std(window) + 1e-8),  # Z-score
                max(window) - min(window),  # Range
            ]
            training_features.append(features)

        training_features = np.array(training_features)

        # Scale features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(training_features)
        self.scalers[metric_name] = scaler

        # Train model
        if self.model_type == "isolation_forest":
            model = IsolationForest(
                contamination=0.05,
                random_state=42
            )
            model.fit(scaled_features)
        else:
            # Add other model types as needed
            model = IsolationForest(contamination=0.05, random_state=42)
            model.fit(scaled_features)

        self.models[metric_name] = model
        self.is_trained[metric_name] = True

    def _extract_time_series_features(
        self,
        current_value: float,
        historical_values: List[float],
        window_size: int
    ) -> List[float]:
        """Extract features from time series data"""
        if len(historical_values) < window_size:
            window = historical_values
        else:
            window = historical_values[-window_size:]

        features = [
            np.mean(window),
            np.std(window),
            min(window),
            max(window),
            current_value,
            (current_value - np.mean(window)) / (np.std(window) + 1e-8),
            len([v for v in window if v > np.mean(window)]) / len(window),  # Percentage above mean
        ]

        return features

class PredictiveAnalyzer:
    """Predictive analytics for capacity planning and incident prediction"""

    def __init__(self):
        self.models: Dict[str, Any] = {}

    async def predict_capacity_needs(
        self,
        metric_history: Dict[str, List[float]],
        forecast_horizon: int = 7
    ) -> Dict[str, Dict[str, Any]]:
        """Predict future resource needs"""
        predictions = {}

        for metric_name, values in metric_history.items():
            if len(values) < 30:
                continue

            # Simple linear trend prediction (use more sophisticated models in production)
            x = np.arange(len(values))
            coeffs = np.polyfit(x, values, 1)

            # Predict future values
            future_x = np.arange(len(values), len(values) + forecast_horizon * 24)
            future_values = np.polyval(coeffs, future_x)

            # Calculate growth rate
            growth_rate = (future_values[-1] - values[-1]) / values[-1] * 100

            predictions[metric_name] = {
                "current": values[-1],
                "predicted_peak": float(max(future_values)),
                "predicted_average": float(np.mean(future_values)),
                "growth_rate": growth_rate,
                "recommendation": self._get_capacity_recommendation(growth_rate),
                "confidence": 0.75  # Should be calculated based on model accuracy
            }

        return predictions

    async def predict_incidents(
        self,
        alert_history: List[Dict[str, Any]],
        system_metrics: Dict[str, List[float]]
    ) -> Dict[str, Any]:
        """Predict likelihood of future incidents"""
        # Feature engineering
        features = self._extract_incident_features(alert_history, system_metrics)

        # Simplified risk score calculation
        risk_factors = {
            "error_rate_trend": self._calculate_trend(
                system_metrics.get("error_rate", [])
            ),
            "cpu_utilization_avg": np.mean(
                system_metrics.get("cpu_utilization", [0])
            ),
            "memory_utilization_avg": np.mean(
                system_metrics.get("memory_utilization", [0])
            ),
            "recent_incident_count": len([
                a for a in alert_history[-24:]
                if a.get("severity") == "critical"
            ]),
        }

        # Calculate risk score (0-100)
        risk_score = min(100, max(0, (
            risk_factors["error_rate_trend"] * 30 +
            risk_factors["cpu_utilization_avg"] * 25 +
            risk_factors["memory_utilization_avg"] * 25 +
            risk_factors["recent_incident_count"] * 20
        )))

        return {
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "contributing_factors": risk_factors,
            "recommendations": self._get_mitigation_recommendations(risk_factors)
        }

    def _extract_incident_features(
        self,
        alert_history: List[Dict[str, Any]],
        system_metrics: Dict[str, List[float]]
    ) -> List[float]:
        """Extract features for incident prediction"""
        features = []

        # Alert patterns
        recent_alerts = alert_history[-24:] if len(alert_history) >= 24 else alert_history
        features.append(len(recent_alerts))
        features.append(len([a for a in recent_alerts if a.get("severity") == "critical"]))

        # System metrics
        for metric_name in ["cpu", "memory", "disk", "network"]:
            values = system_metrics.get(f"{metric_name}_utilization", [0])
            features.append(np.mean(values[-12:]) if values else 0)
            features.append(np.std(values[-12:]) if values else 0)

        return features

    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend coefficient (positive = increasing)"""
        if len(values) < 2:
            return 0.0

        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, 1)
        return coeffs[0]

    def _get_capacity_recommendation(self, growth_rate: float) -> str:
        """Get capacity recommendation based on growth rate"""
        if growth_rate > 50:
            return "Immediate scaling required - consider 2x current capacity"
        elif growth_rate > 20:
            return "Plan for scaling within next week - recommend 1.5x capacity"
        elif growth_rate > 0:
            return "Monitor growth - consider 25% buffer"
        else:
            return "Capacity adequate - no immediate action needed"

    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level from risk score"""
        if risk_score >= 80:
            return "critical"
        elif risk_score >= 60:
            return "high"
        elif risk_score >= 40:
            return "medium"
        else:
            return "low"

    def _get_mitigation_recommendations(
        self,
        risk_factors: Dict[str, float]
    ) -> List[str]:
        """Get mitigation recommendations based on risk factors"""
        recommendations = []

        if risk_factors["cpu_utilization_avg"] > 80:
            recommendations.append("Scale CPU resources or optimize CPU usage")

        if risk_factors["memory_utilization_avg"] > 80:
            recommendations.append("Increase memory allocation or check for memory leaks")

        if risk_factors["error_rate_trend"] > 0:
            recommendations.append("Investigate and fix increasing error rate")

        if risk_factors["recent_incident_count"] > 3:
            recommendations.append("Review recent incidents for root cause analysis")

        return recommendations

class AILogAnalyzer:
    """AI-powered log analysis and pattern detection"""

    def __init__(self):
        self.patterns: Dict[str, List[str]] = {}
        self.embeddings: Dict[str, np.ndarray] = {}

    async def analyze_logs(
        self,
        logs: List[LogEntry]
    ) -> Dict[str, Any]:
        """Analyze logs for patterns and anomalies"""
        analysis = {
            "total_logs": len(logs),
            "error_rate": 0.0,
            "patterns": [],
            "anomalies": [],
            "trending_topics": [],
            "recommendations": []
        }

        # Calculate error rate
        error_count = len([l for l in logs if l.level.lower() in ["error", "critical"]])
        analysis["error_rate"] = error_count / len(logs) * 100

        # Extract patterns using regex and ML
        analysis["patterns"] = await self._extract_patterns(logs)

        # Find anomalies
        analysis["anomalies"] = await self._detect_log_anomalies(logs)

        # Identify trending topics/errors
        analysis["trending_topics"] = await self._identify_trending_topics(logs)

        # Generate recommendations
        analysis["recommendations"] = self._generate_log_recommendations(analysis)

        return analysis

    async def _extract_patterns(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Extract common patterns from logs"""
        # Simplified pattern extraction
        # In production, use more sophisticated NLP techniques
        patterns = []

        # Group logs by service
        service_logs = {}
        for log in logs:
            if log.service not in service_logs:
                service_logs[log.service] = []
            service_logs[log.service].append(log)

        # Find error patterns
        for service, service_log_list in service_logs.items():
            error_logs = [l for l in service_log_list if l.level.lower() == "error"]
            if len(error_logs) > 0:
                # Find common substrings in error messages
                common_errors = {}
                for log in error_logs:
                    # Simplified - use actual pattern matching in production
                    for word in log.message.split():
                        if len(word) > 5:  # Only consider longer words
                            common_errors[word] = common_errors.get(word, 0) + 1

                if common_errors:
                    most_common = max(common_errors, key=common_errors.get)
                    patterns.append({
                        "service": service,
                        "type": "error_pattern",
                        "pattern": most_common,
                        "count": common_errors[most_common],
                        "percentage": common_errors[most_common] / len(error_logs) * 100
                    })

        return patterns

    async def _detect_log_anomalies(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Detect anomalies in logs"""
        anomalies = []

        # Check for unusual error spikes
        error_by_minute = {}
        for log in logs:
            if log.level.lower() in ["error", "critical"]:
                minute = log.timestamp.replace(second=0, microsecond=0)
                error_by_minute[minute] = error_by_minute.get(minute, 0) + 1

        if error_by_minute:
            avg_errors = np.mean(list(error_by_minute.values()))
            for minute, count in error_by_minute.items():
                if count > avg_errors * 3:  # 3x spike
                    anomalies.append({
                        "type": "error_spike",
                        "timestamp": minute.isoformat(),
                        "value": count,
                        "baseline": avg_errors,
                        "severity": "high"
                    })

        return anomalies

    async def _identify_trending_topics(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Identify trending topics in logs"""
        # Simplified trending detection
        word_count = {}
        for log in logs[-100:]:  # Last 100 logs
            for word in log.message.lower().split():
                if len(word) > 5 and word.isalpha():
                    word_count[word] = word_count.get(word, 0) + 1

        # Get top trending words
        trending = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]

        return [
            {"topic": word, "count": count}
            for word, count in trending
        ]

    def _generate_log_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on log analysis"""
        recommendations = []

        if analysis["error_rate"] > 5:
            recommendations.append(
                f"High error rate ({analysis['error_rate']:.1f}%) detected - investigate immediately"
            )

        if len(analysis["anomalies"]) > 0:
            recommendations.append(
                f"Found {len(analysis['anomalies'])} anomalies - review and address"
            )

        for pattern in analysis["patterns"][:3]:
            if pattern["percentage"] > 30:
                recommendations.append(
                    f"Common error pattern in {pattern['service']}: {pattern['pattern']}"
                )

        return recommendations
```

## 3. Automation and Self-Healing

### Automation Engine

```python
# aiops/automation/engine.py
import asyncio
import subprocess
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ActionType(str, Enum):
    """Types of automation actions"""
    SCALE = "scale"
    RESTART = "restart"
    PATCH = "patch"
    NOTIFY = "notify"
    SUPPRESS = "suppress"
    ISOLATE = "isolate"
    FAILBACK = "failback"

@dataclass
class Action:
    """Automation action definition"""
    type: ActionType
    target: str
    params: Dict[str, Any]
    conditions: List[str] = None
    timeout: int = 300
    retries: int = 3

class AutomationEngine:
    """Automation engine for executing remediation actions"""

    def __init__(self):
        self.actions: Dict[str, Action] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.action_handlers: Dict[ActionType, Callable] = {
            ActionType.SCALE: self._handle_scale,
            ActionType.RESTART: self._handle_restart,
            ActionType.PATCH: self._handle_patch,
            ActionType.NOTIFY: self._handle_notify,
            ActionType.SUPPRESS: self._handle_suppress,
            ActionType.ISOLATE: self._handle_isolate,
            ActionType.FAILBACK: self._handle_failback
        }

    def register_action(self, action: Action) -> None:
        """Register an automation action"""
        self.actions[action.target] = action
        logger.info(f"Registered action: {action.type} for {action.target}")

    async def execute(self, action: Action) -> Dict[str, Any]:
        """Execute an automation action"""
        execution_id = f"{action.type}_{action.target}_{int(datetime.utcnow().timestamp())}"

        logger.info(f"Executing action {execution_id}: {action.type} on {action.target}")

        execution = {
            "id": execution_id,
            "action": action,
            "status": "running",
            "started_at": datetime.utcnow(),
            "result": None,
            "error": None
        }

        try:
            # Check conditions
            if action.conditions and not await self._check_conditions(action.conditions):
                execution["status"] = "skipped"
                execution["error"] = "Conditions not met"
                return execution

            # Execute action with retries
            result = await self._execute_with_retries(action)

            execution["status"] = "success"
            execution["result"] = result
            logger.info(f"Action {execution_id} completed successfully")

        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)
            logger.error(f"Action {execution_id} failed: {e}")

        finally:
            execution["completed_at"] = datetime.utcnow()
            execution["duration"] = (execution["completed_at"] - execution["started_at"]).total_seconds()
            self.execution_history.append(execution)

        return execution

    async def _execute_with_retries(self, action: Action) -> Any:
        """Execute action with retry logic"""
        last_exception = None

        for attempt in range(action.retries + 1):
            try:
                handler = self.action_handlers.get(action.type)
                if not handler:
                    raise ValueError(f"No handler for action type: {action.type}")

                # Execute with timeout
                return await asyncio.wait_for(
                    handler(action),
                    timeout=action.timeout
                )

            except asyncio.TimeoutError:
                last_exception = TimeoutError(f"Action timed out after {action.timeout}s")
                if attempt < action.retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise last_exception

            except Exception as e:
                last_exception = e
                if attempt < action.retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise last_exception

    async def _check_conditions(self, conditions: List[str]) -> bool:
        """Check if action conditions are met"""
        # Implement condition checking logic
        # For example, check cluster health, time windows, etc.
        return True

    async def _handle_scale(self, action: Action) -> Dict[str, Any]:
        """Handle scale action"""
        params = action.params
        command = [
            "kubectl", "scale",
            f"--replicas={params.get('replicas', '+1')}",
            f"deployment/{action.target}"
        ]

        if "namespace" in params:
            command.insert(1, f"-n={params['namespace']}")

        result = await self._run_command(command)
        return {"scaled": True, "result": result}

    async def _handle_restart(self, action: Action) -> Dict[str, Any]:
        """Handle restart action"""
        params = action.params
        command = ["kubectl", "rollout", "restart", f"deployment/{action.target}"]

        if "namespace" in params:
            command.insert(2, f"-n={params['namespace']}")

        result = await self._run_command(command)
        return {"restarted": True, "result": result}

    async def _handle_patch(self, action: Action) -> Dict[str, Any]:
        """Handle patch action"""
        params = action.params

        # Build patch command
        command = ["kubectl", "patch"]

        if "namespace" in params:
            command.extend(["-n", params["namespace"]])

        resource_type = params.get("type", "deployment")
        command.extend([f"{resource_type}/{action.target}"])

        patch_type = params.get("patch_type", "strategic")
        command.extend(["--type", patch_type])

        patch_data = params.get("patch", {})
        command.extend(["-p", json.dumps(patch_data)])

        result = await self._run_command(command)
        return {"patched": True, "result": result}

    async def _handle_notify(self, action: Action) -> Dict[str, Any]:
        """Handle notification action"""
        params = action.params
        channel = params.get("channel", "default")
        message = params.get("message", f"AAction executed: {action.type} on {action.target}")

        # Implement notification logic (Slack, Teams, Email, etc.)
        # This is a placeholder for actual notification implementation
        notification = {
            "channel": channel,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "sent": True
        }

        # Example: Send to Slack
        if channel == "slack":
            webhook_url = params.get("webhook_url")
            if webhook_url:
                slack_payload = {
                    "text": message,
                    "attachments": [{
                        "color": "warning",
                        "fields": [{
                            "title": "Action",
                            "value": f"{action.type} on {action.target}",
                            "short": True
                        }, {
                            "title": "Timestamp",
                            "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                            "short": True
                        }]
                    }]
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(webhook_url, json=slack_payload) as response:
                        if response.status != 200:
                            raise Exception(f"Slack notification failed: {response.status}")

        return notification

    async def _handle_suppress(self, action: Action) -> Dict[str, Any]:
        """Handle alert suppression"""
        params = action.params
        duration = params.get("duration", "1h")
        reason = params.get("reason", "Automated suppression")

        # Implement alert suppression logic
        # This depends on your alerting system (Prometheus, AlertManager, etc.)
        suppression = {
            "target": action.target,
            "duration": duration,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }

        return {"suppressed": True, "suppression": suppression}

    async def _handle_isolate(self, action: Action) -> Dict[str, Any]:
        """Handle service isolation"""
        params = action.params
        namespace = params.get("namespace", "default")

        # Implement isolation logic
        # For example, update service to point to maintenance page
        command = [
            "kubectl", "patch", "service", action.target,
            "-n", namespace,
            "-p", '{"spec": {"selector": {"app": "maintenance"}}}'
        ]

        result = await self._run_command(command)
        return {"isolated": True, "result": result}

    async def _handle_failback(self, action: Action) -> Dict[str, Any]:
        """Handle failback to primary"""
        params = action.params
        namespace = params.get("namespace", "default")

        # Implement failback logic
        # Restore traffic to primary service
        command = [
            "kubectl", "patch", "service", action.target,
            "-n", namespace,
            "-p", '{"spec": {"selector": {"app": "' + action.target + '"}}}'
        ]

        result = await self._run_command(command)
        return {"failed_back": True, "result": result}

    async def _run_command(self, command: List[str]) -> str:
        """Run shell command"""
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Command failed: {stderr.decode()}")

        return stdout.decode()

class SelfHealingManager:
    """Manages self-healing policies and execution"""

    def __init__(self, automation_engine: AutomationEngine):
        self.automation_engine = automation_engine
        self.healing_policies: Dict[str, Dict[str, Any]] = {}
        self.active_healings: Dict[str, Dict[str, Any]] = {}

    def register_healing_policy(
        self,
        service_name: str,
        policy: Dict[str, Any]
    ) -> None:
        """Register a self-healing policy for a service"""
        self.healing_policies[service_name] = policy
        logger.info(f"Registered healing policy for {service_name}")

    async def trigger_healing(
        self,
        service_name: str,
        incident: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Trigger self-healing for a service"""
        if service_name not in self.healing_policies:
            return {"error": "No healing policy registered"}

        policy = self.healing_policies[service_name]
        healing_id = f"healing_{service_name}_{int(datetime.utcnow().timestamp())}"

        logger.info(f"Triggering self-healing {healing_id} for {service_name}")

        healing_record = {
            "id": healing_id,
            "service": service_name,
            "incident": incident,
            "policy": policy,
            "status": "running",
            "actions": [],
            "started_at": datetime.utcnow()
        }

        self.active_healings[healing_id] = healing_record

        try:
            # Execute healing actions based on policy
            for action_def in policy.get("actions", []):
                action = Action(
                    type=ActionType(action_def["type"]),
                    target=action_def.get("target", service_name),
                    params=action_def.get("params", {}),
                    timeout=action_def.get("timeout", 300)
                )

                result = await self.automation_engine.execute(action)
                healing_record["actions"].append({
                    "action": action_def,
                    "result": result
                })

                # Check if healing was successful
                if result["status"] != "success":
                    healing_record["status"] = "failed"
                    break
            else:
                healing_record["status"] = "success"

        except Exception as e:
            healing_record["status"] = "error"
            healing_record["error"] = str(e)
            logger.error(f"Self-healing failed: {e}")

        finally:
            healing_record["completed_at"] = datetime.utcnow()
            healing_record["duration"] = (
                healing_record["completed_at"] - healing_record["started_at"]
            ).total_seconds()

        return healing_record

    async def check_healing_status(self, healing_id: str) -> Optional[Dict[str, Any]]:
        """Get status of an active healing process"""
        return self.active_healings.get(healing_id)
```

## 4. Observability and Monitoring Best Practices

### Unified Observability Platform

```python
# aiops/observability/platform.py
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class ServiceHealth:
    """Service health status"""
    service_name: str
    status: str  # healthy, degraded, unhealthy
    latency_p99: float
    error_rate: float
    throughput: float
    last_check: datetime
    dependencies: List[str] = field(default_factory=list)
    sla_status: str = "within_sla"

class ObservabilityPlatform:
    """Unified observability platform for AIOps"""

    def __init__(self, data_sources: List[DataSource]):
        self.data_sources = data_sources
        self.service_health: Dict[str, ServiceHealth] = {}
        self.slo_compliance: Dict[str, Dict[str, Any]] = {}
        self.dashboard_configs: Dict[str, Dict[str, Any]] = {}

    async def get_service_overview(self) -> Dict[str, Any]:
        """Get comprehensive service overview"""
        overview = {
            "total_services": len(self.service_health),
            "healthy_services": 0,
            "degraded_services": 0,
            "unhealthy_services": 0,
            "services": {}
        }

        for service_name, health in self.service_health.items():
            overview["services"][service_name] = {
                "status": health.status,
                "latency_p99": health.latency_p99,
                "error_rate": health.error_rate,
                "throughput": health.throughput,
                "sla_status": health.sla_status
            }

            if health.status == "healthy":
                overview["healthy_services"] += 1
            elif health.status == "degraded":
                overview["degraded_services"] += 1
            else:
                overview["unhealthy_services"] += 1

        return overview

    async def check_slo_compliance(
        self,
        service_name: str,
        slo_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check SLO compliance for a service"""
        now = datetime.utcnow()
        window = timedelta(days=30)  # 30-day rolling window

        # Collect metrics for SLO calculation
        metrics = []
        for source in self.data_sources:
            try:
                source_metrics = await source.collect_metrics(
                    query=slo_config["metric_query"],
                    start_time=now - window,
                    end_time=now
                )
                metrics.extend(source_metrics)
            except Exception as e:
                logger.error(f"Failed to collect metrics from {type(source).__name__}: {e}")

        if not metrics:
            return {"error": "No metrics available"}

        # Calculate SLO compliance
        total_requests = sum(m.value for m in metrics if m.name.endswith("_total"))
        good_requests = sum(m.value for m in metrics if m.name.endswith("_success"))

        if total_requests == 0:
            return {"error": "No requests in time window"}

        actual_availability = (good_requests / total_requests) * 100
        target_availability = slo_config["target"]

        compliance = {
            "service": service_name,
            "slo_name": slo_config["name"],
            "target_availability": target_availability,
            "actual_availability": actual_availability,
            "compliance": actual_availability >= target_availability,
            "error_budget": target_availability - actual_availability,
            "time_window": window.days,
            "total_requests": total_requests,
            "good_requests": good_requests,
            "calculated_at": now.isoformat()
        }

        self.slo_compliance[f"{service_name}_{slo_config['name']}"] = compliance
        return compliance

    async def generate_incident_report(
        self,
        incident_id: str,
        start_time: datetime,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive incident report"""
        if not end_time:
            end_time = datetime.utcnow()

        report = {
            "incident_id": incident_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_hours": (end_time - start_time).total_seconds() / 3600,
            "affected_services": [],
            "metrics_impact": {},
            "error_rate_impact": {},
            "user_impact": {},
            "timeline": [],
            "root_cause_analysis": {},
            "action_items": []
        }

        # Collect data for affected services
        for service_name, health in self.service_health.items():
            if health.last_check >= start_time and health.last_check <= end_time:
                report["affected_services"].append(service_name)

                # Collect metrics impact
                for source in self.data_sources:
                    try:
                        metrics = await source.collect_metrics(
                            query=f"rate(http_requests_total[5m])",
                            start_time=start_time,
                            end_time=end_time
                        )
                        if metrics:
                            report["metrics_impact"][service_name] = [
                                {"timestamp": m.timestamp.isoformat(), "value": m.value}
                                for m in metrics
                            ]
                    except Exception as e:
                        logger.error(f"Failed to collect metrics for {service_name}: {e}")

        return report

    async def create_dashboard(
        self,
        dashboard_name: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new observability dashboard"""
        dashboard = {
            "name": dashboard_name,
            "description": config.get("description", ""),
            "panels": config.get("panels", []),
            "time_range": config.get("time_range", "1h"),
            "refresh_interval": config.get("refresh_interval", "5m"),
            "created_at": datetime.utcnow().isoformat()
        }

        self.dashboard_configs[dashboard_name] = dashboard
        return dashboard

    async def get_dashboard_data(
        self,
        dashboard_name: str,
        time_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get data for a specific dashboard"""
        if dashboard_name not in self.dashboard_configs:
            return {"error": "Dashboard not found"}

        dashboard = self.dashboard_configs[dashboard_name]
        now = datetime.utcnow()

        # Parse time range
        if time_range:
            end_time = now
            if time_range.endswith("h"):
                start_time = now - timedelta(hours=int(time_range[:-1]))
            elif time_range.endswith("d"):
                start_time = now - timedelta(days=int(time_range[:-1]))
            else:
                start_time = now - timedelta(hours=1)
        else:
            start_time = now - timedelta(hours=1)
            end_time = now

        dashboard_data = {
            "name": dashboard_name,
            "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
            "panels": []
        }

        # Collect data for each panel
        for panel in dashboard["panels"]:
            panel_data = {
                "title": panel["title"],
                "type": panel["type"],
                "data": []
            }

            try:
                # Collect metrics based on panel query
                for source in self.data_sources:
                    metrics = await source.collect_metrics(
                        query=panel["query"],
                        start_time=start_time,
                        end_time=end_time
                    )
                    panel_data["data"].extend([
                        {"timestamp": m.timestamp.isoformat(), "value": m.value}
                        for m in metrics
                    ])
            except Exception as e:
                panel_data["error"] = str(e)

            dashboard_data["panels"].append(panel_data)

        return dashboard_data

# SLO and SLA Management
class SLOManager:
    """Manages Service Level Objectives and Service Level Agreements"""

    def __init__(self):
        self.slos: Dict[str, Dict[str, Any]] = {}
        self.slas: Dict[str, Dict[str, Any]] = {}

    def define_slo(
        self,
        service_name: str,
        slo_name: str,
        target: float,
        time_window: str,
        alerting_burn_rate: float = 2.0
    ) -> Dict[str, Any]:
        """Define a Service Level Objective"""
        slo = {
            "service_name": service_name,
            "slo_name": slo_name,
            "target": target,
            "time_window": time_window,
            "alerting_burn_rate": alerting_burn_rate,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }

        self.slos[f"{service_name}_{slo_name}"] = slo
        return slo

    def define_sla(
        self,
        service_name: str,
        sla_name: str,
        availability_target: float,
        performance_targets: Dict[str, float],
        penalties: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Define a Service Level Agreement"""
        sla = {
            "service_name": service_name,
            "sla_name": sla_name,
            "availability_target": availability_target,
            "performance_targets": performance_targets,
            "penalties": penalties or {},
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }

        self.slas[f"{service_name}_{sla_name}"] = sla
        return sla

    def calculate_error_budget(
        self,
        service_name: str,
        slo_name: str,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Calculate error budget for an SLO"""
        slo_key = f"{service_name}_{slo_name}"
        if slo_key not in self.slos:
            return {"error": "SLO not found"}

        slo = self.slos[slo_key]
        target_availability = slo["target"]

        # Calculate error budget
        period_hours = period_days * 24
        error_budget = (100 - target_availability) / 100 * period_hours

        return {
            "service": service_name,
            "slo": slo_name,
            "period_days": period_days,
            "target_availability": target_availability,
            "error_budget_hours": error_budget,
            "error_budget_percentage": 100 - target_availability,
            "remaining_error_budget": error_budget,  # Would be calculated from actual metrics
            "burn_rate": 0.0  # Would be calculated from actual metrics
        }
```

This comprehensive AIOps skill provides production-ready patterns for implementing AI-powered operations in 2025, including intelligent monitoring, anomaly detection, predictive analytics, automation, and self-healing capabilities.

`★ Insight ─────────────────────────────────────`
The AIOps patterns shown here emphasize several key 2025 best practices:
1. **Data Source Abstraction**: Generic interfaces allow integration with any monitoring platform (Prometheus, Datadog, New Relic, etc.)
2. **ML-Driven Operations**: Anomaly detection, predictive analytics, and pattern recognition using proven ML models
3. **Automation with Safety**: Retry logic, timeout handling, and condition checking ensure safe automated remediation
4. **Observability First**: Unified platform approach to metrics, logs, and traces for comprehensive visibility
5. **SLO-Driven**: Focus on business outcomes through Service Level Objectives and error budget management

These patterns ensure your AIOps implementation is intelligent, automated, and aligned with business objectives.
`─────────────────────────────────────────────────`