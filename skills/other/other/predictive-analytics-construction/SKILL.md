---
name: "predictive-analytics-construction"
description: "Forecast project outcomes using historical data: cost overruns, schedule delays, risk probabilities. Machine learning models for construction prediction."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📈", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Predictive Analytics for Construction

## Overview

Use historical project data to predict future outcomes: cost overruns, schedule delays, quality issues, and risks. Apply machine learning models tailored for construction industry patterns.

## Business Case

Predictive analytics enables proactive project management:
- **Early Warning**: Identify projects likely to overrun before it happens
- **Resource Optimization**: Allocate resources based on predicted needs
- **Risk Mitigation**: Focus on high-risk areas early
- **Better Estimates**: Learn from historical accuracy

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

@dataclass
class PredictionResult:
    prediction: float
    confidence: float
    prediction_type: str
    features_used: List[str]
    feature_importance: Dict[str, float]
    comparable_projects: List[str]
    risk_factors: List[str]

@dataclass
class ModelMetrics:
    model_name: str
    accuracy: float
    mae: float
    feature_importance: Dict[str, float]
    training_samples: int
    last_trained: datetime

class ConstructionPredictiveAnalytics:
    """Predictive analytics for construction projects."""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.encoders: Dict[str, LabelEncoder] = {}
        self.metrics: Dict[str, ModelMetrics] = {}
        self.feature_columns: Dict[str, List[str]] = {}

    def prepare_features(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features for model training."""
        # Separate numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Remove target from features
        if target_col in numeric_cols:
            numeric_cols.remove(target_col)
        if target_col in categorical_cols:
            categorical_cols.remove(target_col)

        # Encode categorical variables
        df_encoded = df.copy()
        for col in categorical_cols:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                df_encoded[col] = self.encoders[col].fit_transform(df[col].astype(str))
            else:
                df_encoded[col] = self.encoders[col].transform(df[col].astype(str))

        feature_cols = numeric_cols + categorical_cols
        X = df_encoded[feature_cols].fillna(0)
        y = df[target_col]

        return X, y, feature_cols

    def train_cost_overrun_model(self, historical_data: pd.DataFrame) -> ModelMetrics:
        """Train model to predict cost overrun percentage."""
        # Expected columns: project_type, original_estimate, gross_area, duration_months,
        # num_change_orders, complexity_score, contractor_experience, final_cost

        required_cols = ['original_estimate', 'final_cost']
        if not all(col in historical_data.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")

        # Calculate overrun percentage
        df = historical_data.copy()
        df['overrun_pct'] = ((df['final_cost'] - df['original_estimate']) / df['original_estimate']) * 100

        # Prepare features
        feature_cols = [col for col in df.columns if col not in ['final_cost', 'overrun_pct', 'project_id', 'project_name']]
        X, y, used_features = self.prepare_features(df[feature_cols + ['overrun_pct']], 'overrun_pct')

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)

        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='neg_mean_absolute_error')

        # Feature importance
        importance = dict(zip(used_features, model.feature_importances_))

        # Store model
        self.models['cost_overrun'] = model
        self.scalers['cost_overrun'] = scaler
        self.feature_columns['cost_overrun'] = used_features

        metrics = ModelMetrics(
            model_name='cost_overrun',
            accuracy=1 - (mae / df['overrun_pct'].std()),
            mae=mae,
            feature_importance=importance,
            training_samples=len(X_train),
            last_trained=datetime.now()
        )
        self.metrics['cost_overrun'] = metrics

        return metrics

    def train_schedule_delay_model(self, historical_data: pd.DataFrame) -> ModelMetrics:
        """Train model to predict schedule delay probability."""
        df = historical_data.copy()

        # Binary classification: was project delayed?
        df['was_delayed'] = (df['actual_duration'] > df['planned_duration']).astype(int)

        feature_cols = [col for col in df.columns
                       if col not in ['actual_duration', 'was_delayed', 'project_id', 'project_name']]

        X, y, used_features = self.prepare_features(df[feature_cols + ['was_delayed']], 'was_delayed')

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train_scaled, y_train)

        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        importance = dict(zip(used_features, model.feature_importances_))

        self.models['schedule_delay'] = model
        self.scalers['schedule_delay'] = scaler
        self.feature_columns['schedule_delay'] = used_features

        metrics = ModelMetrics(
            model_name='schedule_delay',
            accuracy=accuracy,
            mae=0,
            feature_importance=importance,
            training_samples=len(X_train),
            last_trained=datetime.now()
        )
        self.metrics['schedule_delay'] = metrics

        return metrics

    def predict_cost_overrun(self, project_data: Dict) -> PredictionResult:
        """Predict cost overrun for a new project."""
        if 'cost_overrun' not in self.models:
            raise ValueError("Cost overrun model not trained. Call train_cost_overrun_model first.")

        model = self.models['cost_overrun']
        scaler = self.scalers['cost_overrun']
        features = self.feature_columns['cost_overrun']

        # Prepare input
        input_df = pd.DataFrame([project_data])

        # Encode categorical
        for col in input_df.select_dtypes(include=['object']).columns:
            if col in self.encoders:
                input_df[col] = self.encoders[col].transform(input_df[col].astype(str))

        # Ensure all features present
        for feat in features:
            if feat not in input_df.columns:
                input_df[feat] = 0

        X = input_df[features].fillna(0)
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]

        # Get feature importance for this prediction
        importance = dict(zip(features, model.feature_importances_))
        top_features = sorted(importance.items(), key=lambda x: -x[1])[:5]

        # Identify risk factors
        risk_factors = []
        if prediction > 10:
            risk_factors.append(f"High overrun risk: {prediction:.1f}%")
        for feat, imp in top_features[:3]:
            risk_factors.append(f"Key factor: {feat} (importance: {imp:.2%})")

        return PredictionResult(
            prediction=prediction,
            confidence=0.8,  # Could calculate from model uncertainty
            prediction_type='cost_overrun_percentage',
            features_used=features,
            feature_importance=dict(top_features),
            comparable_projects=[],
            risk_factors=risk_factors
        )

    def predict_delay_probability(self, project_data: Dict) -> PredictionResult:
        """Predict probability of schedule delay."""
        if 'schedule_delay' not in self.models:
            raise ValueError("Schedule delay model not trained.")

        model = self.models['schedule_delay']
        scaler = self.scalers['schedule_delay']
        features = self.feature_columns['schedule_delay']

        input_df = pd.DataFrame([project_data])

        for col in input_df.select_dtypes(include=['object']).columns:
            if col in self.encoders:
                input_df[col] = self.encoders[col].transform(input_df[col].astype(str))

        for feat in features:
            if feat not in input_df.columns:
                input_df[feat] = 0

        X = input_df[features].fillna(0)
        X_scaled = scaler.transform(X)

        probability = model.predict_proba(X_scaled)[0][1]
        prediction = model.predict(X_scaled)[0]

        importance = dict(zip(features, model.feature_importances_))
        top_features = sorted(importance.items(), key=lambda x: -x[1])[:5]

        risk_factors = []
        if probability > 0.7:
            risk_factors.append(f"High delay probability: {probability:.1%}")
        elif probability > 0.4:
            risk_factors.append(f"Moderate delay probability: {probability:.1%}")

        return PredictionResult(
            prediction=probability,
            confidence=probability if prediction == 1 else 1 - probability,
            prediction_type='delay_probability',
            features_used=features,
            feature_importance=dict(top_features),
            comparable_projects=[],
            risk_factors=risk_factors
        )

    def find_similar_projects(self, project_data: Dict, historical_data: pd.DataFrame,
                             n: int = 5) -> pd.DataFrame:
        """Find similar projects from historical data."""
        from sklearn.neighbors import NearestNeighbors

        numeric_cols = historical_data.select_dtypes(include=[np.number]).columns.tolist()
        exclude = ['final_cost', 'actual_duration', 'overrun_pct']
        feature_cols = [c for c in numeric_cols if c not in exclude]

        X = historical_data[feature_cols].fillna(0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Prepare new project
        new_project = pd.DataFrame([project_data])[feature_cols].fillna(0)
        new_scaled = scaler.transform(new_project)

        # Find neighbors
        nn = NearestNeighbors(n_neighbors=min(n, len(X)), metric='euclidean')
        nn.fit(X_scaled)
        distances, indices = nn.kneighbors(new_scaled)

        similar = historical_data.iloc[indices[0]].copy()
        similar['similarity_score'] = 1 / (1 + distances[0])

        return similar

    def generate_prediction_report(self, project_data: Dict, historical_data: pd.DataFrame) -> str:
        """Generate comprehensive prediction report."""
        lines = ["# Project Prediction Report", ""]
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Project:** {project_data.get('project_name', 'New Project')}")
        lines.append("")

        # Cost prediction
        if 'cost_overrun' in self.models:
            cost_pred = self.predict_cost_overrun(project_data)
            lines.append("## Cost Overrun Prediction")
            lines.append(f"**Predicted Overrun:** {cost_pred.prediction:.1f}%")
            lines.append(f"**Confidence:** {cost_pred.confidence:.1%}")
            lines.append("")
            lines.append("**Key Factors:**")
            for feat, imp in list(cost_pred.feature_importance.items())[:5]:
                lines.append(f"- {feat}: {imp:.2%}")
            lines.append("")

        # Schedule prediction
        if 'schedule_delay' in self.models:
            delay_pred = self.predict_delay_probability(project_data)
            lines.append("## Schedule Delay Prediction")
            lines.append(f"**Delay Probability:** {delay_pred.prediction:.1%}")
            lines.append("")

        # Similar projects
        lines.append("## Similar Historical Projects")
        similar = self.find_similar_projects(project_data, historical_data, n=5)
        for _, row in similar.iterrows():
            name = row.get('project_name', 'Project')
            overrun = row.get('overrun_pct', 0)
            similarity = row.get('similarity_score', 0)
            lines.append(f"- **{name}**: {overrun:.1f}% overrun (similarity: {similarity:.1%})")

        # Risk summary
        lines.append("")
        lines.append("## Risk Summary")
        all_risks = []
        if 'cost_overrun' in self.models:
            all_risks.extend(cost_pred.risk_factors)
        if 'schedule_delay' in self.models:
            all_risks.extend(delay_pred.risk_factors)

        for risk in all_risks:
            lines.append(f"- ⚠️ {risk}")

        return "\n".join(lines)
```

## Quick Start

```python
import pandas as pd

# Load historical data
historical = pd.read_excel("historical_projects.xlsx")

# Initialize analytics
analytics = ConstructionPredictiveAnalytics()

# Train models
cost_metrics = analytics.train_cost_overrun_model(historical)
print(f"Cost model MAE: {cost_metrics.mae:.2f}%")

delay_metrics = analytics.train_schedule_delay_model(historical)
print(f"Delay model accuracy: {delay_metrics.accuracy:.1%}")

# Predict for new project
new_project = {
    'project_type': 'Office',
    'original_estimate': 5000000,
    'gross_area': 50000,
    'duration_months': 18,
    'complexity_score': 7,
    'contractor_experience': 15
}

cost_prediction = analytics.predict_cost_overrun(new_project)
print(f"Predicted overrun: {cost_prediction.prediction:.1f}%")

delay_prediction = analytics.predict_delay_probability(new_project)
print(f"Delay probability: {delay_prediction.prediction:.1%}")

# Generate report
report = analytics.generate_prediction_report(new_project, historical)
print(report)
```

## Dependencies

```bash
pip install pandas numpy scikit-learn
```

## Resources

- **ML for Construction**: Research on predictive models
- **Feature Engineering**: Construction-specific features
