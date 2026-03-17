---
name: "schedule-forecaster"
description: "Predict project completion dates using ML models. Forecast schedule delays based on current progress, historical patterns, and risk factors."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🤖", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Schedule Forecaster for Construction

## Overview

Predict project completion dates using machine learning models trained on historical data. Forecast delays based on current progress, weather patterns, resource availability, and project characteristics.

## Business Case

Accurate schedule forecasting enables:
- **Early Warning**: Identify potential delays before they impact milestones
- **Resource Planning**: Adjust staffing based on predicted needs
- **Client Communication**: Provide reliable completion estimates
- **Risk Management**: Proactively address schedule risks

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

@dataclass
class ScheduleForecast:
    project_id: str
    forecast_date: datetime
    predicted_completion: datetime
    confidence_interval: Tuple[datetime, datetime]
    delay_probability: float
    delay_days: int
    key_risk_factors: List[str]
    recommended_actions: List[str]

@dataclass
class ProgressSnapshot:
    date: datetime
    planned_progress: float
    actual_progress: float
    earned_value: float
    planned_value: float
    spi: float  # Schedule Performance Index
    cpi: float  # Cost Performance Index

class ConstructionScheduleForecaster:
    """ML-based schedule forecasting for construction projects."""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.feature_columns: List[str] = []
        self.is_trained = False

    def prepare_training_data(self, historical_projects: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features from historical project data."""

        df = historical_projects.copy()

        # Calculate target: actual delay in days
        df['planned_duration'] = (pd.to_datetime(df['planned_end']) - pd.to_datetime(df['planned_start'])).dt.days
        df['actual_duration'] = (pd.to_datetime(df['actual_end']) - pd.to_datetime(df['actual_start'])).dt.days
        df['delay_days'] = df['actual_duration'] - df['planned_duration']

        # Feature engineering
        features = pd.DataFrame()

        # Project characteristics
        if 'project_type' in df.columns:
            features = pd.concat([features, pd.get_dummies(df['project_type'], prefix='type')], axis=1)

        if 'gross_area' in df.columns:
            features['gross_area'] = df['gross_area']
            features['log_area'] = np.log1p(df['gross_area'])

        if 'contract_value' in df.columns:
            features['contract_value'] = df['contract_value']
            features['value_per_sf'] = df['contract_value'] / df['gross_area'].replace(0, 1)

        if 'planned_duration' in df.columns:
            features['planned_duration'] = df['planned_duration']

        # Complexity indicators
        if 'num_subcontractors' in df.columns:
            features['num_subcontractors'] = df['num_subcontractors']

        if 'num_change_orders' in df.columns:
            features['num_change_orders'] = df['num_change_orders']

        # Historical performance
        if 'contractor_avg_delay' in df.columns:
            features['contractor_avg_delay'] = df['contractor_avg_delay']

        # Seasonal factors
        if 'planned_start' in df.columns:
            start_dates = pd.to_datetime(df['planned_start'])
            features['start_month'] = start_dates.dt.month
            features['start_quarter'] = start_dates.dt.quarter
            features['winter_start'] = ((start_dates.dt.month >= 11) | (start_dates.dt.month <= 2)).astype(int)

        # Location factors
        if 'location_factor' in df.columns:
            features['location_factor'] = df['location_factor']

        self.feature_columns = features.columns.tolist()

        return features.fillna(0), df['delay_days']

    def train_delay_model(self, historical_projects: pd.DataFrame) -> Dict[str, float]:
        """Train model to predict schedule delays."""

        X, y = self.prepare_training_data(historical_projects)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Store model
        self.models['delay'] = model
        self.scalers['delay'] = scaler
        self.is_trained = True

        # Feature importance
        importance = dict(zip(self.feature_columns, model.feature_importances_))

        return {
            'mae': mae,
            'rmse': rmse,
            'training_samples': len(X_train),
            'feature_importance': importance
        }

    def train_progress_model(self, progress_data: pd.DataFrame) -> Dict[str, float]:
        """Train model to predict progress based on current trajectory."""

        df = progress_data.copy()

        # Features: current progress, SPI, historical trend
        features = []
        targets = []

        for project_id in df['project_id'].unique():
            project_data = df[df['project_id'] == project_id].sort_values('date')

            for i in range(len(project_data) - 1):
                current = project_data.iloc[i]
                final = project_data.iloc[-1]

                feature = {
                    'current_progress': current['actual_progress'],
                    'planned_progress': current['planned_progress'],
                    'progress_variance': current['actual_progress'] - current['planned_progress'],
                    'spi': current.get('spi', 1.0),
                    'cpi': current.get('cpi', 1.0),
                    'days_elapsed': i,
                    'days_remaining_planned': len(project_data) - i - 1,
                }
                features.append(feature)
                targets.append(final['actual_progress'] - current['actual_progress'])

        X = pd.DataFrame(features)
        y = pd.Series(targets)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_train_scaled, y_train)

        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)

        self.models['progress'] = model
        self.scalers['progress'] = scaler

        return {'mae': mae, 'training_samples': len(X_train)}

    def forecast_completion(self, project_data: Dict,
                            current_progress: float,
                            current_date: datetime) -> ScheduleForecast:
        """Forecast project completion date."""

        if not self.is_trained:
            raise ValueError("Model not trained. Call train_delay_model first.")

        # Prepare features
        features = pd.DataFrame([project_data])[self.feature_columns].fillna(0)
        features_scaled = self.scalers['delay'].transform(features)

        # Predict delay
        predicted_delay = self.models['delay'].predict(features_scaled)[0]

        # Get prediction interval (using model variance)
        tree_predictions = np.array([
            tree.predict(features_scaled)[0]
            for tree in self.models['delay'].estimators_
        ])
        delay_std = np.std(tree_predictions)

        # Calculate dates
        planned_end = pd.to_datetime(project_data.get('planned_end'))
        predicted_completion = planned_end + timedelta(days=int(predicted_delay))

        confidence_low = planned_end + timedelta(days=int(predicted_delay - 1.96 * delay_std))
        confidence_high = planned_end + timedelta(days=int(predicted_delay + 1.96 * delay_std))

        # Calculate delay probability
        delay_probability = 1 / (1 + np.exp(-predicted_delay / 30))  # Sigmoid transform

        # Identify risk factors
        risk_factors = self._identify_risk_factors(project_data, features_scaled)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            predicted_delay, current_progress, project_data
        )

        return ScheduleForecast(
            project_id=project_data.get('project_id', 'Unknown'),
            forecast_date=current_date,
            predicted_completion=predicted_completion,
            confidence_interval=(confidence_low, confidence_high),
            delay_probability=delay_probability,
            delay_days=int(predicted_delay),
            key_risk_factors=risk_factors,
            recommended_actions=recommendations
        )

    def _identify_risk_factors(self, project_data: Dict, features_scaled: np.ndarray) -> List[str]:
        """Identify key risk factors for the project."""
        risk_factors = []

        importance = dict(zip(self.feature_columns, self.models['delay'].feature_importances_))
        top_features = sorted(importance.items(), key=lambda x: -x[1])[:5]

        for feat, imp in top_features:
            if imp > 0.1:
                value = project_data.get(feat)
                if value:
                    risk_factors.append(f"{feat}: {value} (impact: {imp:.1%})")

        # Add context-specific risks
        if project_data.get('num_change_orders', 0) > 10:
            risk_factors.append("High number of change orders")

        if project_data.get('winter_start'):
            risk_factors.append("Winter start increases weather risk")

        return risk_factors[:5]

    def _generate_recommendations(self, predicted_delay: float,
                                   current_progress: float,
                                   project_data: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if predicted_delay > 30:
            recommendations.append("Consider schedule compression techniques (crashing/fast-tracking)")
            recommendations.append("Evaluate additional resource allocation")

        if predicted_delay > 0 and current_progress < 0.5:
            recommendations.append("Review critical path activities for optimization")

        if project_data.get('spi', 1.0) < 0.9:
            recommendations.append("Schedule Performance Index is low - investigate root causes")

        if project_data.get('num_change_orders', 0) > 5:
            recommendations.append("High change order volume - improve change management process")

        if not recommendations:
            recommendations.append("Project on track - maintain current pace")

        return recommendations

    def update_forecast_with_progress(self, project_id: str,
                                       progress_history: List[ProgressSnapshot],
                                       project_data: Dict) -> ScheduleForecast:
        """Update forecast based on current progress trajectory."""

        if len(progress_history) < 2:
            return self.forecast_completion(project_data, 0, datetime.now())

        # Calculate trends
        recent = progress_history[-5:]
        progress_rates = []
        for i in range(1, len(recent)):
            days = (recent[i].date - recent[i-1].date).days
            if days > 0:
                rate = (recent[i].actual_progress - recent[i-1].actual_progress) / days
                progress_rates.append(rate)

        avg_rate = np.mean(progress_rates) if progress_rates else 0
        current_progress = progress_history[-1].actual_progress

        # Estimate remaining duration
        remaining_progress = 100 - current_progress
        if avg_rate > 0:
            remaining_days = remaining_progress / avg_rate
        else:
            remaining_days = 365  # Fallback

        # Adjust with SPI
        current_spi = progress_history[-1].spi
        if current_spi > 0:
            adjusted_remaining = remaining_days / current_spi
        else:
            adjusted_remaining = remaining_days

        # Get base forecast
        base_forecast = self.forecast_completion(
            project_data, current_progress, datetime.now()
        )

        # Blend predictions
        progress_completion = datetime.now() + timedelta(days=int(adjusted_remaining))

        # Weight recent progress more heavily
        blended_completion = base_forecast.predicted_completion + (
            (progress_completion - base_forecast.predicted_completion) * 0.6
        )

        return ScheduleForecast(
            project_id=project_id,
            forecast_date=datetime.now(),
            predicted_completion=blended_completion,
            confidence_interval=base_forecast.confidence_interval,
            delay_probability=base_forecast.delay_probability,
            delay_days=int((blended_completion - pd.to_datetime(project_data['planned_end'])).days),
            key_risk_factors=base_forecast.key_risk_factors + [f"Current SPI: {current_spi:.2f}"],
            recommended_actions=base_forecast.recommended_actions
        )

    def generate_forecast_report(self, forecast: ScheduleForecast, project_name: str) -> str:
        """Generate forecast report."""
        lines = ["# Schedule Forecast Report", ""]
        lines.append(f"**Project:** {project_name}")
        lines.append(f"**Forecast Date:** {forecast.forecast_date.strftime('%Y-%m-%d')}")
        lines.append("")

        lines.append("## Completion Forecast")
        lines.append(f"**Predicted Completion:** {forecast.predicted_completion.strftime('%Y-%m-%d')}")
        lines.append(f"**Confidence Interval:** {forecast.confidence_interval[0].strftime('%Y-%m-%d')} to {forecast.confidence_interval[1].strftime('%Y-%m-%d')}")
        lines.append(f"**Predicted Delay:** {forecast.delay_days} days")
        lines.append(f"**Delay Probability:** {forecast.delay_probability:.1%}")
        lines.append("")

        lines.append("## Risk Factors")
        for risk in forecast.key_risk_factors:
            lines.append(f"- ⚠️ {risk}")
        lines.append("")

        lines.append("## Recommended Actions")
        for action in forecast.recommended_actions:
            lines.append(f"- {action}")

        return "\n".join(lines)
```

## Quick Start

```python
import pandas as pd
from datetime import datetime

# Load historical data
historical = pd.read_excel("historical_projects.xlsx")

# Initialize forecaster
forecaster = ConstructionScheduleForecaster()

# Train model
metrics = forecaster.train_delay_model(historical)
print(f"Model MAE: {metrics['mae']:.1f} days")

# Forecast for new project
new_project = {
    'project_id': 'PROJ-001',
    'project_type': 'Office',
    'gross_area': 50000,
    'contract_value': 5000000,
    'planned_duration': 365,
    'num_subcontractors': 12,
    'num_change_orders': 3,
    'planned_start': '2026-01-15',
    'planned_end': '2027-01-15',
    'start_month': 1,
    'winter_start': 1
}

forecast = forecaster.forecast_completion(new_project, 25, datetime.now())
print(f"Predicted completion: {forecast.predicted_completion.strftime('%Y-%m-%d')}")
print(f"Delay probability: {forecast.delay_probability:.1%}")

# Generate report
report = forecaster.generate_forecast_report(forecast, "Office Building Project")
print(report)
```

## Dependencies

```bash
pip install pandas numpy scikit-learn
```
