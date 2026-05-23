---
slug: "risk-assessment-ml"
display_name: "Risk Assessment ML"
description: "Apply machine learning for construction project risk assessment. Predict schedule delays, cost overruns, and safety incidents using historical data and project characteristics."
---

# Risk Assessment with Machine Learning

## Overview

This skill implements ML-based risk assessment for construction projects. Predict potential risks before they occur and prioritize mitigation strategies based on data-driven insights.

**Risk Categories:**
- **Schedule Risk**: Delays, critical path impacts
- **Cost Risk**: Budget overruns, change orders
- **Safety Risk**: Incident probability, hazard identification
- **Quality Risk**: Defects, rework probability

## Quick Start

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load historical project data
projects = pd.read_csv("project_history.csv")

# Features for risk prediction
features = ['project_size_m2', 'budget_usd', 'duration_days',
            'complexity_score', 'team_size', 'similar_projects_exp']

X = projects[features]
y_delay = projects['had_delay']  # Binary: 1=delay, 0=on-time

# Train risk model
X_train, X_test, y_train, y_test = train_test_split(X, y_delay, test_size=0.2)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict risk for new project
new_project = [[5000, 2000000, 365, 3, 50, 5]]
risk_probability = model.predict_proba(new_project)[0][1]
print(f"Delay Risk: {risk_probability:.1%}")
```

## Comprehensive Risk Model

### Risk Assessment Framework

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score
from dataclasses import dataclass
from typing import Dict, List, Optional
import joblib

@dataclass
class RiskPrediction:
    category: str
    probability: float
    severity: str
    impact_days: Optional[float]
    impact_cost: Optional[float]
    confidence: float
    contributing_factors: List[str]
    recommended_actions: List[str]

class ConstructionRiskAssessor:
    """ML-based construction risk assessment"""

    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_importance = {}

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for training/prediction"""
        features = df.copy()

        # Encode categorical variables
        categorical_cols = features.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                features[col] = self.encoders[col].fit_transform(features[col].astype(str))
            else:
                features[col] = self.encoders[col].transform(features[col].astype(str))

        # Handle missing values
        features = features.fillna(features.median())

        return features

    def train_delay_model(self, df: pd.DataFrame, target_col: str = 'delay_days'):
        """Train schedule delay prediction model"""
        features = self.prepare_features(df.drop(columns=[target_col]))
        target = df[target_col]

        # Binary classification: delay or not
        target_binary = (target > 0).astype(int)

        # Scale features
        self.scalers['delay'] = StandardScaler()
        X_scaled = self.scalers['delay'].fit_transform(features)

        # Train model
        self.models['delay_classifier'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.models['delay_classifier'].fit(X_scaled, target_binary)

        # Train regression for delay magnitude
        delayed_mask = target > 0
        if delayed_mask.sum() > 10:
            self.models['delay_regressor'] = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            self.models['delay_regressor'].fit(
                X_scaled[delayed_mask],
                target[delayed_mask]
            )

        # Store feature importance
        self.feature_importance['delay'] = dict(zip(
            features.columns,
            self.models['delay_classifier'].feature_importances_
        ))

        return self._evaluate_model('delay_classifier', X_scaled, target_binary)

    def train_cost_overrun_model(self, df: pd.DataFrame,
                                  target_col: str = 'cost_overrun_pct'):
        """Train cost overrun prediction model"""
        features = self.prepare_features(df.drop(columns=[target_col]))
        target = df[target_col]

        # Binary: overrun or not
        target_binary = (target > 0).astype(int)

        self.scalers['cost'] = StandardScaler()
        X_scaled = self.scalers['cost'].fit_transform(features)

        self.models['cost_classifier'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.models['cost_classifier'].fit(X_scaled, target_binary)

        # Regression for magnitude
        overrun_mask = target > 0
        if overrun_mask.sum() > 10:
            self.models['cost_regressor'] = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            self.models['cost_regressor'].fit(
                X_scaled[overrun_mask],
                target[overrun_mask]
            )

        self.feature_importance['cost'] = dict(zip(
            features.columns,
            self.models['cost_classifier'].feature_importances_
        ))

        return self._evaluate_model('cost_classifier', X_scaled, target_binary)

    def train_safety_model(self, df: pd.DataFrame,
                           target_col: str = 'incident_occurred'):
        """Train safety incident prediction model"""
        features = self.prepare_features(df.drop(columns=[target_col]))
        target = df[target_col]

        self.scalers['safety'] = StandardScaler()
        X_scaled = self.scalers['safety'].fit_transform(features)

        self.models['safety_classifier'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            class_weight='balanced',  # Handle imbalanced data
            random_state=42
        )
        self.models['safety_classifier'].fit(X_scaled, target)

        self.feature_importance['safety'] = dict(zip(
            features.columns,
            self.models['safety_classifier'].feature_importances_
        ))

        return self._evaluate_model('safety_classifier', X_scaled, target)

    def _evaluate_model(self, model_name: str, X: np.ndarray, y: np.ndarray) -> Dict:
        """Evaluate model with cross-validation"""
        model = self.models[model_name]
        scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

        return {
            'model': model_name,
            'accuracy_mean': scores.mean(),
            'accuracy_std': scores.std()
        }

    def predict_risks(self, project_data: Dict) -> List[RiskPrediction]:
        """Predict all risks for a project"""
        df = pd.DataFrame([project_data])
        features = self.prepare_features(df)
        predictions = []

        # Schedule risk
        if 'delay_classifier' in self.models:
            X_delay = self.scalers['delay'].transform(features)
            delay_prob = self.models['delay_classifier'].predict_proba(X_delay)[0][1]

            delay_days = None
            if delay_prob > 0.5 and 'delay_regressor' in self.models:
                delay_days = self.models['delay_regressor'].predict(X_delay)[0]

            predictions.append(RiskPrediction(
                category='Schedule',
                probability=delay_prob,
                severity=self._get_severity(delay_prob),
                impact_days=delay_days,
                impact_cost=delay_days * project_data.get('daily_cost', 10000) if delay_days else None,
                confidence=0.85,
                contributing_factors=self._get_top_factors('delay', features.iloc[0]),
                recommended_actions=self._get_delay_actions(delay_prob)
            ))

        # Cost risk
        if 'cost_classifier' in self.models:
            X_cost = self.scalers['cost'].transform(features)
            cost_prob = self.models['cost_classifier'].predict_proba(X_cost)[0][1]

            overrun_pct = None
            if cost_prob > 0.5 and 'cost_regressor' in self.models:
                overrun_pct = self.models['cost_regressor'].predict(X_cost)[0]

            predictions.append(RiskPrediction(
                category='Cost',
                probability=cost_prob,
                severity=self._get_severity(cost_prob),
                impact_days=None,
                impact_cost=project_data.get('budget', 0) * overrun_pct / 100 if overrun_pct else None,
                confidence=0.80,
                contributing_factors=self._get_top_factors('cost', features.iloc[0]),
                recommended_actions=self._get_cost_actions(cost_prob)
            ))

        # Safety risk
        if 'safety_classifier' in self.models:
            X_safety = self.scalers['safety'].transform(features)
            safety_prob = self.models['safety_classifier'].predict_proba(X_safety)[0][1]

            predictions.append(RiskPrediction(
                category='Safety',
                probability=safety_prob,
                severity=self._get_severity(safety_prob),
                impact_days=None,
                impact_cost=None,
                confidence=0.75,
                contributing_factors=self._get_top_factors('safety', features.iloc[0]),
                recommended_actions=self._get_safety_actions(safety_prob)
            ))

        return predictions

    def _get_severity(self, probability: float) -> str:
        if probability >= 0.7:
            return 'High'
        elif probability >= 0.4:
            return 'Medium'
        else:
            return 'Low'

    def _get_top_factors(self, risk_type: str, project_features: pd.Series) -> List[str]:
        """Get top contributing factors for risk"""
        importance = self.feature_importance.get(risk_type, {})
        sorted_factors = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        return [f[0] for f in sorted_factors[:5]]

    def _get_delay_actions(self, probability: float) -> List[str]:
        actions = []
        if probability > 0.7:
            actions.extend([
                'Add buffer to critical path activities',
                'Increase resource allocation',
                'Implement daily progress monitoring'
            ])
        elif probability > 0.4:
            actions.extend([
                'Review schedule with contractors',
                'Identify potential fast-track opportunities'
            ])
        else:
            actions.append('Standard schedule monitoring')
        return actions

    def _get_cost_actions(self, probability: float) -> List[str]:
        actions = []
        if probability > 0.7:
            actions.extend([
                'Increase contingency reserve',
                'Lock in material prices',
                'Review scope with stakeholders'
            ])
        elif probability > 0.4:
            actions.extend([
                'Monitor change order frequency',
                'Implement value engineering review'
            ])
        else:
            actions.append('Standard cost tracking')
        return actions

    def _get_safety_actions(self, probability: float) -> List[str]:
        actions = []
        if probability > 0.7:
            actions.extend([
                'Conduct safety stand-down',
                'Increase safety personnel',
                'Review high-risk activities'
            ])
        elif probability > 0.4:
            actions.extend([
                'Increase safety inspections',
                'Refresh safety training'
            ])
        else:
            actions.append('Maintain standard safety protocols')
        return actions

    def save_models(self, path: str):
        """Save trained models"""
        joblib.dump({
            'models': self.models,
            'scalers': self.scalers,
            'encoders': self.encoders,
            'feature_importance': self.feature_importance
        }, path)

    def load_models(self, path: str):
        """Load trained models"""
        data = joblib.load(path)
        self.models = data['models']
        self.scalers = data['scalers']
        self.encoders = data['encoders']
        self.feature_importance = data['feature_importance']
```

## Feature Engineering

### Project Risk Features

```python
def engineer_risk_features(project_data: pd.DataFrame) -> pd.DataFrame:
    """Create features for risk prediction"""
    df = project_data.copy()

    # Size and complexity metrics
    df['cost_per_sqm'] = df['budget'] / df['area_sqm']
    df['duration_per_sqm'] = df['duration_days'] / df['area_sqm']

    # Team metrics
    df['workers_per_1000sqm'] = df['peak_workers'] / (df['area_sqm'] / 1000)

    # Weather exposure
    df['outdoor_work_pct'] = df['outdoor_activities'] / df['total_activities']

    # Contract complexity
    df['subcontractor_ratio'] = df['num_subcontractors'] / df['total_contractors']

    # Experience factors
    df['team_avg_experience'] = df['total_team_years'] / df['team_size']

    # Season risk
    df['winter_months'] = df.apply(
        lambda r: count_winter_months(r['start_date'], r['end_date']), axis=1
    )

    # Location risk
    df['urban_complexity'] = df['location_type'].map({
        'rural': 1, 'suburban': 2, 'urban': 3, 'downtown': 4
    })

    return df

def count_winter_months(start_date, end_date):
    """Count winter months in project duration"""
    winter_months = [11, 12, 1, 2, 3]
    months = pd.date_range(start_date, end_date, freq='M')
    return sum(1 for m in months if m.month in winter_months)
```

## Risk Report Generation

```python
def generate_risk_report(assessor: ConstructionRiskAssessor,
                        project_data: Dict,
                        output_path: str):
    """Generate comprehensive risk assessment report"""
    predictions = assessor.predict_risks(project_data)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary
        summary = pd.DataFrame([{
            'Category': p.category,
            'Risk Level': p.severity,
            'Probability': f"{p.probability:.1%}",
            'Impact Days': p.impact_days,
            'Impact Cost': p.impact_cost,
            'Top Factor': p.contributing_factors[0] if p.contributing_factors else ''
        } for p in predictions])
        summary.to_excel(writer, sheet_name='Summary', index=False)

        # Detailed recommendations
        actions = []
        for p in predictions:
            for action in p.recommended_actions:
                actions.append({
                    'Category': p.category,
                    'Risk Level': p.severity,
                    'Recommended Action': action
                })
        pd.DataFrame(actions).to_excel(writer, sheet_name='Actions', index=False)

    return output_path
```

## Quick Reference

| Risk Type | Key Features | Model Type |
|-----------|--------------|------------|
| Schedule | Duration, complexity, weather | Random Forest |
| Cost | Budget, scope changes, market | Gradient Boosting |
| Safety | Work type, team experience | Random Forest |
| Quality | Supervision, materials | Logistic Regression |

## Resources

- **Scikit-learn**: https://scikit-learn.org
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `cost-prediction` for detailed cost modeling
- See `4d-simulation` for schedule analysis
- See `data-visualization` for risk dashboards
