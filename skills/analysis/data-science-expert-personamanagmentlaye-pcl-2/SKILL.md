---
name: data-science-expert
version: 1.0.0
description: Expert-level data science, analytics, visualization, and statistical modeling
category: ai
tags: [data-science, analytics, visualization, statistics, pandas, numpy]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# Data Science Expert

Expert guidance for data science, analytics, statistical modeling, and data visualization.

## Core Concepts

### Data Analysis
- Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing
- Feature engineering
- Statistical inference
- Time series analysis
- A/B testing

### Machine Learning
- Supervised learning (classification, regression)
- Unsupervised learning (clustering, PCA)
- Model selection and validation
- Feature importance
- Hyperparameter tuning
- Ensemble methods

### Data Visualization
- Matplotlib, Seaborn, Plotly
- Statistical plots
- Interactive dashboards
- Storytelling with data
- Best practices for visualization
- Color theory and accessibility

## Data Cleaning and EDA

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List

class DataCleaner:
    """Clean and preprocess data"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.cleaning_log = []

    def handle_missing_values(self, strategy: str = 'drop',
                             fill_value=None) -> pd.DataFrame:
        """Handle missing values"""
        missing_before = self.df.isnull().sum().sum()

        if strategy == 'drop':
            self.df = self.df.dropna()
        elif strategy == 'fill':
            if fill_value is not None:
                self.df = self.df.fillna(fill_value)
            else:
                # Fill numeric with median, categorical with mode
                for col in self.df.columns:
                    if self.df[col].dtype in ['float64', 'int64']:
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                    else:
                        self.df[col].fillna(self.df[col].mode()[0], inplace=True)

        missing_after = self.df.isnull().sum().sum()
        self.cleaning_log.append(f"Missing values: {missing_before} -> {missing_after}")

        return self.df

    def remove_duplicates(self) -> pd.DataFrame:
        """Remove duplicate rows"""
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)

        self.cleaning_log.append(f"Duplicates removed: {before - after}")
        return self.df

    def remove_outliers(self, columns: List[str],
                       method: str = 'iqr',
                       threshold: float = 1.5) -> pd.DataFrame:
        """Remove outliers"""
        before = len(self.df)

        for col in columns:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1

                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR

                self.df = self.df[(self.df[col] >= lower) & (self.df[col] <= upper)]

            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(self.df[col]))
                self.df = self.df[z_scores < threshold]

        after = len(self.df)
        self.cleaning_log.append(f"Outliers removed: {before - after}")

        return self.df

class EDA:
    """Exploratory Data Analysis"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def summary_stats(self) -> pd.DataFrame:
        """Generate summary statistics"""
        return self.df.describe(include='all').T

    def correlation_analysis(self, method: str = 'pearson') -> pd.DataFrame:
        """Calculate correlation matrix"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_cols].corr(method=method)

    def plot_distributions(self, columns: List[str] = None):
        """Plot distributions of numeric columns"""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns

        n_cols = len(columns)
        n_rows = (n_cols + 2) // 3

        fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5*n_rows))
        axes = axes.flatten()

        for idx, col in enumerate(columns):
            sns.histplot(self.df[col], kde=True, ax=axes[idx])
            axes[idx].set_title(f'Distribution of {col}')

        plt.tight_layout()
        return fig

    def plot_correlation_heatmap(self):
        """Plot correlation heatmap"""
        corr = self.correlation_analysis()

        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1)
        plt.title('Correlation Heatmap')
        return plt.gcf()
```

## Feature Engineering

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

class FeatureEngineer:
    """Engineer features for machine learning"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.transformers = {}

    def create_interaction_features(self, col1: str, col2: str) -> pd.Series:
        """Create interaction features"""
        self.df[f'{col1}_x_{col2}'] = self.df[col1] * self.df[col2]
        return self.df[f'{col1}_x_{col2}']

    def create_polynomial_features(self, col: str, degree: int = 2) -> pd.DataFrame:
        """Create polynomial features"""
        for d in range(2, degree + 1):
            self.df[f'{col}_pow_{d}'] = self.df[col] ** d
        return self.df

    def bin_numeric_feature(self, col: str, n_bins: int = 5,
                           strategy: str = 'quantile') -> pd.Series:
        """Bin numeric features"""
        self.df[f'{col}_binned'] = pd.qcut(self.df[col], q=n_bins,
                                           labels=False, duplicates='drop')
        return self.df[f'{col}_binned']

    def encode_categorical(self, col: str, method: str = 'onehot') -> pd.DataFrame:
        """Encode categorical variables"""
        if method == 'label':
            le = LabelEncoder()
            self.df[f'{col}_encoded'] = le.fit_transform(self.df[col])
            self.transformers[col] = le

        elif method == 'onehot':
            dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
            self.df = pd.concat([self.df, dummies], axis=1)

        return self.df

    def scale_features(self, columns: List[str],
                      method: str = 'standard') -> pd.DataFrame:
        """Scale numeric features"""
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()

        self.df[columns] = scaler.fit_transform(self.df[columns])
        self.transformers['scaler'] = scaler

        return self.df

    def select_features(self, X: pd.DataFrame, y: pd.Series,
                       k: int = 10,
                       method: str = 'f_classif') -> List[str]:
        """Select top k features"""
        if method == 'f_classif':
            scorer = f_classif
        elif method == 'mutual_info':
            scorer = mutual_info_classif

        selector = SelectKBest(scorer, k=k)
        selector.fit(X, y)

        selected_features = X.columns[selector.get_support()].tolist()
        return selected_features
```

## Time Series Analysis

```python
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

class TimeSeriesAnalyzer:
    """Analyze time series data"""

    def __init__(self, data: pd.Series, freq: str = 'D'):
        self.data = data
        self.freq = freq

    def decompose(self, model: str = 'additive'):
        """Decompose time series"""
        result = seasonal_decompose(self.data, model=model, period=30)

        return {
            'trend': result.trend,
            'seasonal': result.seasonal,
            'residual': result.resid
        }

    def test_stationarity(self) -> dict:
        """Test for stationarity using Augmented Dickey-Fuller"""
        result = adfuller(self.data.dropna())

        return {
            'adf_statistic': result[0],
            'p_value': result[1],
            'critical_values': result[4],
            'is_stationary': result[1] < 0.05
        }

    def make_stationary(self, method: str = 'diff') -> pd.Series:
        """Make series stationary"""
        if method == 'diff':
            return self.data.diff().dropna()
        elif method == 'log':
            return np.log(self.data)
        elif method == 'log_diff':
            return np.log(self.data).diff().dropna()

    def fit_arima(self, order: tuple = (1, 1, 1)):
        """Fit ARIMA model"""
        model = ARIMA(self.data, order=order)
        fitted_model = model.fit()

        return {
            'model': fitted_model,
            'aic': fitted_model.aic,
            'bic': fitted_model.bic,
            'summary': fitted_model.summary()
        }

    def forecast(self, model, steps: int = 30) -> pd.Series:
        """Generate forecast"""
        return model.forecast(steps=steps)
```

## A/B Testing

```python
from scipy import stats

class ABTest:
    """Conduct A/B tests"""

    def __init__(self, control: np.ndarray, treatment: np.ndarray):
        self.control = control
        self.treatment = treatment

    def ttest(self) -> dict:
        """Two-sample t-test"""
        statistic, p_value = stats.ttest_ind(self.control, self.treatment)

        # Calculate confidence interval for difference
        diff_mean = self.treatment.mean() - self.control.mean()
        se_diff = np.sqrt(self.control.var()/len(self.control) +
                         self.treatment.var()/len(self.treatment))
        ci_lower = diff_mean - 1.96 * se_diff
        ci_upper = diff_mean + 1.96 * se_diff

        return {
            't_statistic': statistic,
            'p_value': p_value,
            'mean_control': self.control.mean(),
            'mean_treatment': self.treatment.mean(),
            'difference': diff_mean,
            'ci_95': (ci_lower, ci_upper),
            'significant': p_value < 0.05
        }

    def proportion_test(self, conversions_control: int,
                       conversions_treatment: int) -> dict:
        """Test difference in proportions"""
        n_control = len(self.control)
        n_treatment = len(self.treatment)

        p_control = conversions_control / n_control
        p_treatment = conversions_treatment / n_treatment

        p_pooled = (conversions_control + conversions_treatment) / (n_control + n_treatment)

        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
        z = (p_treatment - p_control) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

        return {
            'conversion_rate_control': p_control,
            'conversion_rate_treatment': p_treatment,
            'lift': (p_treatment - p_control) / p_control * 100,
            'z_statistic': z,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
```

## Best Practices

### Data Analysis
- Always explore data before modeling
- Check data quality and missing values
- Understand variable distributions
- Look for correlations and relationships
- Document data cleaning steps
- Validate assumptions

### Feature Engineering
- Create domain-specific features
- Test feature importance
- Avoid data leakage
- Use cross-validation for validation
- Document feature transformations
- Keep features interpretable

### Visualization
- Choose appropriate plot types
- Use clear labels and titles
- Consider color accessibility
- Avoid chartjunk
- Tell a story with data
- Make visualizations reproducible

## Anti-Patterns

❌ Not exploring data before modeling
❌ Ignoring data quality issues
❌ Data leakage in feature engineering
❌ Over-engineering features
❌ Misleading visualizations
❌ Not documenting analysis steps
❌ Ignoring business context

## Resources

- Pandas: https://pandas.pydata.org/
- NumPy: https://numpy.org/
- Scikit-learn: https://scikit-learn.org/
- Seaborn: https://seaborn.pydata.org/
- Plotly: https://plotly.com/python/
