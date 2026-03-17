---
name: survey-analyzer
description: Analyze survey responses with Likert scale analysis, cross-tabulations, sentiment scoring, and frequency distributions with visualizations.
---

# Survey Analyzer

Comprehensive survey data analysis with Likert scales, cross-tabs, and sentiment analysis.

## Features

- **Likert Scale Analysis**: Agreement scale scoring and visualization
- **Cross-Tabulation**: Relationship analysis between categorical variables
- **Frequency Analysis**: Response distributions and percentages
- **Sentiment Scoring**: Text response sentiment analysis
- **Open-Ended Analysis**: Theme extraction from text responses
- **Statistical Tests**: Chi-square, correlations, significance testing
- **Visualizations**: Bar charts, heatmaps, word clouds, distribution plots
- **Report Generation**: Comprehensive PDF/HTML reports

## Quick Start

```python
from survey_analyzer import SurveyAnalyzer

analyzer = SurveyAnalyzer()

# Load survey data
analyzer.load_csv('survey_responses.csv')

# Analyze Likert scale question
results = analyzer.likert_analysis('satisfaction', scale_type='agreement')
print(f"Mean score: {results['mean_score']:.2f}")

# Cross-tabulation
crosstab = analyzer.crosstab('age_group', 'product_preference')
print(crosstab)

# Generate report
analyzer.generate_report('survey_report.pdf')
```

## CLI Usage

```bash
# Analyze Likert scale
python survey_analyzer.py --data survey.csv --likert satisfaction --output results.pdf

# Cross-tabulation
python survey_analyzer.py --data survey.csv --crosstab age_group product --output crosstab.png

# Sentiment analysis
python survey_analyzer.py --data survey.csv --sentiment comments --output sentiment.html

# Full report
python survey_analyzer.py --data survey.csv --report --output full_report.pdf
```

## API Reference

### SurveyAnalyzer Class

```python
class SurveyAnalyzer:
    def __init__(self)

    # Data Loading
    def load_csv(self, filepath, **kwargs) -> 'SurveyAnalyzer'
    def load_data(self, data: pd.DataFrame) -> 'SurveyAnalyzer'

    # Likert Scale Analysis
    def likert_analysis(self, column, scale_type='agreement') -> Dict
    def likert_comparison(self, columns: List[str]) -> pd.DataFrame
    def plot_likert(self, column, output, scale_type='agreement') -> str

    # Frequency Analysis
    def frequency_table(self, column) -> pd.DataFrame
    def multiple_choice(self, column, delimiter=',') -> pd.DataFrame
    def plot_frequencies(self, column, output, top_n=None) -> str

    # Cross-Tabulation
    def crosstab(self, row_var, col_var, normalize=None) -> pd.DataFrame
    def chi_square_test(self, row_var, col_var) -> Dict
    def plot_crosstab(self, row_var, col_var, output) -> str

    # Sentiment Analysis
    def sentiment_analysis(self, column) -> pd.DataFrame
    def sentiment_summary(self, column) -> Dict
    def plot_sentiment(self, column, output) -> str

    # Open-Ended Analysis
    def word_frequency(self, column, top_n=20) -> pd.DataFrame
    def word_cloud(self, column, output) -> str
    def extract_themes(self, column, n_themes=5) -> List[str]

    # Statistics
    def satisfaction_score(self, columns: List[str]) -> Dict
    def response_rate(self) -> Dict
    def demographics_summary(self, columns: List[str]) -> pd.DataFrame

    # Reporting
    def generate_report(self, output, format='pdf') -> str
    def summary(self) -> str
```

## Likert Scale Analysis

### Standard Scales

```python
# 5-point agreement scale
analyzer.likert_analysis('satisfaction', scale_type='agreement')
# 1=Strongly Disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly Agree

# 5-point frequency scale
analyzer.likert_analysis('usage', scale_type='frequency')
# 1=Never, 2=Rarely, 3=Sometimes, 4=Often, 5=Always

# Custom scale
analyzer.likert_analysis('rating', scale_type='custom',
                        labels=['Poor', 'Fair', 'Good', 'Excellent'])
```

### Results

```python
results = analyzer.likert_analysis('satisfaction')
# {
#     'mean_score': 4.2,
#     'median': 4,
#     'mode': 5,
#     'distribution': {1: 2, 2: 5, 3: 15, 4: 40, 5: 38},
#     'percentages': {1: 2%, 2: 5%, 3: 15%, 4: 40%, 5: 38%},
#     'top_2_box': 78%,  # % Agree + Strongly Agree
#     'bottom_2_box': 7%  # % Disagree + Strongly Disagree
# }
```

### Visualization

```python
# Stacked bar chart
analyzer.plot_likert('satisfaction', 'likert_chart.png')

# Compare multiple questions
analyzer.likert_comparison(['quality', 'value', 'service'])
analyzer.plot_likert_comparison(['quality', 'value', 'service'],
                               'comparison.png')
```

## Frequency Analysis

### Single Choice

```python
freq = analyzer.frequency_table('age_group')
#          Count  Percentage
# 18-24      45      22.5%
# 25-34      78      39.0%
# 35-44      52      26.0%
# 45+        25      12.5%

# Plot
analyzer.plot_frequencies('age_group', 'age_distribution.png')
```

### Multiple Choice

For questions allowing multiple selections:

```python
# Data format: "Option A, Option B, Option C"
results = analyzer.multiple_choice('features_liked', delimiter=',')
#                Count  Percentage
# Price            120      60%
# Quality           95      47.5%
# Design            80      40%
# Durability        70      35%

analyzer.plot_frequencies('features_liked', 'features.png', top_n=10)
```

## Cross-Tabulation

### Basic Cross-Tab

```python
crosstab = analyzer.crosstab('age_group', 'satisfaction')
#           Satisfied  Neutral  Dissatisfied
# 18-24          30       10           5
# 25-34          60       15           3
# 35-44          40        8           4
# 45+            18        5           2

# With percentages
crosstab_pct = analyzer.crosstab('age_group', 'satisfaction',
                                 normalize='index')  # Row percentages
```

### Statistical Testing

```python
result = analyzer.chi_square_test('age_group', 'satisfaction')
# {
#     'statistic': 12.45,
#     'p_value': 0.014,
#     'significant': True,
#     'interpretation': 'There is a significant relationship between
#                        age_group and satisfaction (p=0.014)'
# }
```

### Visualization

```python
# Heatmap
analyzer.plot_crosstab('age_group', 'satisfaction', 'crosstab_heatmap.png')
```

## Sentiment Analysis

Analyze open-ended text responses:

```python
# Analyze all comments
sentiment_df = analyzer.sentiment_analysis('comments')
#      comment                          polarity  sentiment
# 0    "Great product!"                  0.8      Positive
# 1    "Could be better"                 0.1      Neutral
# 2    "Very disappointed"              -0.6      Negative

# Summary
summary = analyzer.sentiment_summary('comments')
# {
#     'positive': 65%,
#     'neutral': 20%,
#     'negative': 15%,
#     'avg_polarity': 0.35
# }

# Visualize
analyzer.plot_sentiment('comments', 'sentiment_distribution.png')
```

## Open-Ended Analysis

### Word Frequency

```python
words = analyzer.word_frequency('comments', top_n=20)
#        Word   Frequency
# 0     great       45
# 1   quality       38
# 2     price       32
# ...
```

### Word Cloud

```python
analyzer.word_cloud('comments', 'wordcloud.png')
```

### Theme Extraction

```python
themes = analyzer.extract_themes('feedback', n_themes=5)
# ['product quality', 'customer service', 'pricing',
#  'delivery speed', 'user experience']
```

## Satisfaction Metrics

### Net Promoter Score (NPS)

```python
nps = analyzer.nps_score('recommendation')  # 0-10 scale
# {
#     'promoters': 65%,   # 9-10
#     'passives': 25%,    # 7-8
#     'detractors': 10%,  # 0-6
#     'nps': 55
# }
```

### Overall Satisfaction

```python
satisfaction = analyzer.satisfaction_score([
    'product_quality',
    'customer_service',
    'value_for_money',
    'ease_of_use'
])
# {
#     'overall_score': 4.3,
#     'category_scores': {...},
#     'satisfaction_rate': 86%  # % scoring 4-5
# }
```

## Demographics Analysis

```python
demographics = analyzer.demographics_summary([
    'age_group',
    'gender',
    'location',
    'income_range'
])

# Returns frequency tables for each demographic variable
```

## Response Rate Analysis

```python
response_rate = analyzer.response_rate()
# {
#     'total_respondents': 200,
#     'completion_rate': 85%,
#     'average_time': '5m 30s',
#     'dropout_points': {
#         'question_5': 8%,
#         'question_12': 5%
#     }
# }
```

## Report Generation

### Comprehensive Report

```python
analyzer.generate_report('survey_report.pdf', format='pdf')
```

Report includes:
- Executive summary
- Response rate and demographics
- Question-by-question analysis
- Likert scale visualizations
- Cross-tabulations
- Sentiment analysis
- Key findings and recommendations

### Custom Report Sections

```python
analyzer.set_report_sections([
    'executive_summary',
    'demographics',
    'likert_questions',
    'cross_tabs',
    'sentiment',
    'recommendations'
])
```

## Advanced Features

### Filter by Segment

```python
# Analyze subset of responses
analyzer.filter('age_group', '25-34')
results = analyzer.likert_analysis('satisfaction')
analyzer.clear_filter()
```

### Compare Segments

```python
comparison = analyzer.compare_segments(
    segment_col='age_group',
    metric_col='satisfaction'
)
# Shows how different segments scored the metric
```

### Trend Analysis

For longitudinal surveys:

```python
trends = analyzer.trend_analysis(
    metric='satisfaction',
    time_col='survey_date',
    period='month'
)
analyzer.plot_trends(trends, 'satisfaction_trend.png')
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
- scipy>=1.10.0
- textblob>=0.17.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
- wordcloud>=1.9.0
- reportlab>=4.0.0
