---
name: attribution-analysis-modeling
description: Perform multi-touch attribution analysis using Markov chains, Shapley values, and custom attribution models. Use when you need to analyze marketing channel effectiveness, calculate conversion attribution, optimize marketing budgets, or understand customer journey paths. Supports channel transition analysis, ROI calculation, and marketing optimization insights with Chinese language support.
allowed-tools: Read, Write, Bash, Glob
---

# Marketing Attribution Analysis & Modeling

A comprehensive attribution analysis skill that evaluates marketing channel effectiveness using advanced statistical models, helping optimize marketing spend and understand customer journey patterns.

## Instructions

### 1. Data Loading and Preparation
When users provide marketing touchpoint data:
- Load and validate channel interaction data
- Parse customer journey paths and touchpoint sequences
- Handle different data formats (CSV, JSON, Excel)
- Support both user-level and session-level attribution analysis
- Process timestamp data for chronological path analysis

### 2. Customer Journey Analysis
- Reconstruct customer journey paths from touchpoint data
- Calculate path lengths and conversion patterns
- Identify common conversion paths and bottlenecks
- Analyze channel sequencing and order effects
- Support both online and offline channel attribution

### 3. Attribution Model Implementation
- **Markov Chain Attribution**: Build transition probability matrices and calculate removal effects
- **Shapley Value Attribution**: Calculate fair channel contributions using game theory
- **First-Touch Attribution**: Assign full credit to the first channel in the path
- **Last-Touch Attribution**: Assign full credit to the last channel before conversion
- **Linear Attribution**: Distribute credit equally across all channels
- **Time-Decay Attribution**: Weight channels based on recency
- **Position-Based Attribution**: Weight first and last touches more heavily

### 4. Channel Performance Analysis
- Calculate conversion rates by channel and channel combinations
- Compute ROI and cost-per-acquisition (CPA) for each channel
- Analyze channel synergy and interaction effects
- Identify underperforming and overperforming channels
- Generate channel contribution percentages

### 5. Visualization and Reporting
- Create attribution weight distribution charts
- Generate customer journey path visualizations
- Build channel transition heatmaps and network graphs
- Produce ROI analysis and budget allocation recommendations
- Generate comprehensive attribution reports

## Usage Examples

### Marketing Channel Attribution
```
Analyze the effectiveness of our marketing channels:
[CSV with columns: user_id, timestamp, channel, conversion_status, conversion_value]
```

### Digital Campaign Attribution
```
Calculate attribution for our digital marketing campaigns:
[Marketing touchpoint data with campaign, channel, timestamp, and conversion data]
```

### E-commerce Conversion Attribution
```
Perform attribution analysis for e-commerce customer journeys:
[Customer path data showing touchpoints before purchase]
```

### Budget Optimization
```
Help optimize our marketing budget based on attribution results:
[Channel performance data with spend and conversion metrics]
```

## Key Features

### Advanced Attribution Models
- **Markov Chain Analysis**: Probabilistic model for channel transition analysis
- **Shapley Values**: Game theory-based fair attribution calculation
- **Custom Models**: Flexible framework for custom attribution logic
- **Model Comparison**: Compare different attribution models side-by-side

### Customer Journey Analysis
- **Path Reconstruction**: Automatically build conversion paths from raw data
- **Touchpoint Sequencing**: Analyze order and timing effects
- **Conversion Funnels**: Identify drop-off points in customer journeys
- **Multi-path Analysis**: Handle customers with multiple conversion paths

### Channel Performance Metrics
- **Attribution Weights**: Calculate each channel's contribution to conversions
- **ROI Analysis**: Compute return on investment for each channel
- **Synergy Effects**: Measure how channels work together
- **Incremental Impact**: Estimate additional value from channel combinations

### Business Intelligence
- **Budget Optimization**: Recommend optimal budget allocation
- **Channel Recommendations**: Suggest best channel combinations
- **Performance Benchmarks**: Compare channel performance against baselines
- **Trend Analysis**: Track attribution changes over time

## File Requirements

### Standard Touchpoint Data Format
```csv
user_id,timestamp,channel,conversion_status,conversion_value,cost
USER001,2024-01-15T10:30:00Z,paid_search,0,0,50
USER001,2024-01-16T14:20:00Z,social_media,0,0,30
USER001,2024-01-18T09:15:00Z,email,1,1000,10
```

### Required Fields:
- **user_id**: Unique customer identifier
- **timestamp**: Touchpoint timestamp (ISO format preferred)
- **channel**: Marketing channel or touchpoint
- **conversion_status**: Binary indicator of conversion (0/1)
- **conversion_value**: Monetary value of conversion (optional)
- **cost**: Marketing cost for touchpoint (optional, for ROI analysis)

### Supported Channel Types:
- Digital: paid_search, organic_search, social_media, email, display, video
- Traditional: tv, radio, print, outdoor, direct_mail
- E-commerce: marketplace, affiliate, referral
- Custom: Any channel name can be used

## Output Files Generated

- **attribution_results.csv**: Complete attribution analysis with channel weights
- **channel_performance.csv**: Channel metrics including ROI and CPA
- **customer_paths.csv**: Reconstructed customer journey paths
- **transition_matrix.csv**: Markov chain transition probability matrix
- **attribution_dashboard.png**: Comprehensive visualization dashboard
- **attribution_report.md**: Detailed analysis report and recommendations

## Dependencies

- **Core Analytics**: pandas, numpy, scipy
- **Visualization**: matplotlib, seaborn, networkx (for path graphs)
- **Statistical Models**: scikit-learn (optional, for advanced models)
- **Data Processing**: Standard Python libraries for file operations

## Attribution Models Explained

### Markov Chain Attribution
Uses probability transition matrices to model customer journey behavior:
- Calculates removal effect of each channel
- Considers channel transition probabilities
- Handles complex multi-path customer journeys
- Provides incremental value assessment

### Shapley Value Attribution
Applies cooperative game theory for fair attribution:
- Calculates marginal contribution of each channel
- Considers all possible channel combinations
- Provides theoretically optimal attribution
- Handles channel interaction effects

### Custom Attribution Models
Flexible framework for business-specific attribution:
- Configurable weighting rules
- Time-based decay functions
- Position-based weighting
- Custom business logic integration

## Business Applications

### Marketing Budget Optimization
- Allocate budget based on true channel contribution
- Identify underutilized high-performing channels
- Reduce spend on low-impact channels
- Test new channel opportunities

### Campaign Performance Analysis
- Evaluate multi-channel campaign effectiveness
- Understand channel synergy effects
- Optimize campaign sequencing and timing
- Measure incremental lift from channel combinations

### Customer Journey Optimization
- Identify optimal channel sequences
- Remove friction points in conversion paths
- Enhance high-performing channel combinations
- Personalize channel selection by customer segment

## Advanced Features

### Real-time Attribution
- Process streaming touchpoint data
- Update attribution weights dynamically
- Provide real-time channel performance insights
- Support live campaign optimization

### Multi-Conversion Analysis
- Handle multiple conversion types
- Analyze different conversion values separately
- Compare attribution across conversion types
- Optimize for specific conversion goals

### Segmentation Analysis
- Perform attribution by customer segment
- Compare channel effectiveness across segments
- Optimize channel mix by segment
- Personalize marketing strategies

## Best Practices

### Data Quality
- Ensure consistent user identification across touchpoints
- Maintain accurate timestamp data
- Include cost data for ROI analysis
- Handle data gaps and missing values appropriately

### Model Selection
- Choose attribution model based on business goals
- Compare multiple models for validation
- Consider customer journey complexity
- Validate results with business stakeholders

### Implementation
- Start with simpler models before advancing to complex ones
- Test attribution results against known business outcomes
- Implement gradual changes based on attribution insights
- Monitor attribution model performance over time

---

*This skill transforms complex attribution analysis into actionable marketing insights, helping businesses optimize their marketing spend and understand true channel effectiveness.*