---
name: hr-analytics
description: "Implement HR analytics and people analytics including predictive modeling, workforce metrics, turnover prediction, hiring analytics, performance forecasting, and data-driven HR decision-making. Use for: building HR dashboards, implementing predictive analytics, forecasting turnover, analyzing workforce trends, measuring HR effectiveness, creating people analytics strategies, and leveraging data for talent decisions."
---

# HR Analytics

Leverage data, statistical methods, and predictive modeling to transform HR from reactive administration to proactive, strategic workforce management.

## Overview

This skill provides comprehensive frameworks for HR analytics, people analytics, predictive modeling, and data-driven decision-making. It covers descriptive, diagnostic, predictive, and prescriptive analytics, key workforce metrics, analytics tools, and implementation strategies.

## Analytics Type Selection

| Scenario | Analytics Type | Purpose | Reference |
|----------|---------------|---------|----------|
| Understanding what happened | Descriptive Analytics | Summarize historical HR data | `/references/hr-metrics.md` |
| Understanding why it happened | Diagnostic Analytics | Investigate root causes | `/references/people-analytics-frameworks.md` |
| Forecasting future outcomes | Predictive Analytics | Anticipate trends and risks | `/references/predictive-modeling.md` |
| Recommending actions | Prescriptive Analytics | Guide HR strategy and decisions | `/references/people-analytics-frameworks.md` |
| Building analytics capability | Implementation Strategy | Develop tools, skills, processes | `/references/analytics-tools.md` |

## Four Types of HR Analytics

### 1. Descriptive Analytics
**What:** Summarizes historical HR data  
**Purpose:** Understand what has already happened  
**Examples:**
- Past turnover rates by department
- Historical performance review scores
- Headcount trends over time
- Diversity demographics

**Tools:** Dashboards, reports, data visualization  
**Value:** Baseline understanding, trend identification

### 2. Diagnostic Analytics
**What:** Investigates reasons behind past events  
**Purpose:** Understand why something happened  
**Examples:**
- Why did turnover increase in Q3?
- Why is engagement lower in engineering?
- What factors correlate with high performance?
- Why are certain demographics underrepresented?

**Tools:** Root cause analysis, correlation studies, drill-down reports  
**Value:** Actionable insights into problems

### 3. Predictive Analytics
**What:** Forecasts future trends and outcomes  
**Purpose:** Anticipate what is likely to happen  
**Examples:**
- Which employees are at risk of leaving?
- What are future hiring needs?
- Who are high-potential future leaders?
- What will engagement be next quarter?

**Tools:** Statistical modeling, machine learning, regression analysis  
**Value:** Proactive interventions, strategic planning

### 4. Prescriptive Analytics
**What:** Recommends specific actions  
**Purpose:** Guide HR strategy and decision-making  
**Examples:**
- Optimal compensation adjustments to reduce turnover
- Targeted retention interventions for at-risk employees
- Personalized development plans based on career trajectory
- Ideal candidate profiles for hiring

**Tools:** Optimization algorithms, simulation models, AI recommendations  
**Value:** Data-driven action plans

## Key Predictive Analytics Use Cases

### 1. Turnover Prediction
**Goal:** Identify employees at risk of leaving  
**Data Sources:**
- Tenure, performance ratings, compensation changes
- Manager relationship scores, engagement survey results
- Promotion history, training completion
- External factors (market conditions, commute)

**Model:** Logistic regression or decision tree  
**Output:** Probability score (0-100%) that each employee will leave in next 6 months  
**Action:** Targeted retention interventions (raises, promotions, role changes, manager coaching)

**Example:** HP's "Project Insight" reduced turnover from 20% to <10%, saving $300M

### 2. Hiring Success Prediction
**Goal:** Forecast candidate's future performance and fit  
**Data Sources:**
- Resume patterns, assessment results, interview scores
- Education, skills, experience
- Hiring source, referral status

**Model:** Machine learning classification  
**Output:** Predicted performance rating, time-to-productivity, retention likelihood  
**Action:** Better hiring decisions, reduced mis-hire costs

**Example:** Google's "Prediction Engine" analyzes job history, education, skills, personality to predict success

### 3. Performance Forecasting
**Goal:** Predict future employee performance  
**Data Sources:**
- Historical performance ratings, goal achievement
- Skill assessments, training completion
- Peer feedback, manager effectiveness

**Model:** Regression or neural network  
**Output:** Predicted future performance rating  
**Action:** Targeted development, succession planning, resource allocation

### 4. Workforce Planning
**Goal:** Anticipate future talent needs and skill gaps  
**Data Sources:**
- Business growth projections, attrition trends
- Internal mobility patterns, market talent availability
- Skills inventory, training data

**Model:** Time series forecasting, scenario modeling  
**Output:** Future headcount needs by role, skill gaps  
**Action:** Proactive hiring, reskilling programs, strategic talent acquisition

**Example:** Cisco uses predictive analytics to anticipate skills gaps and address proactively

### 5. Engagement and Productivity
**Goal:** Forecast engagement levels and productivity trends  
**Data Sources:**
- Engagement surveys, performance metrics
- Collaboration patterns, work-life balance indicators
- Manager effectiveness, team dynamics

**Model:** Regression, sentiment analysis  
**Output:** Predicted engagement scores, productivity trends  
**Action:** Early intervention to boost engagement, optimize team composition

**Example:** Best Buy linked 0.1% engagement increase to $100K revenue increase per store

## Critical Workforce Metrics

### Talent Acquisition
- **Time-to-Hire:** Days from posting to offer acceptance (Target: <30 days)
- **Cost-per-Hire:** Total recruiting costs / hires
- **Quality of Hire:** New hire performance after 6-12 months (Target: 4.0/5.0+)
- **Offer Acceptance Rate:** % of offers accepted (Target: 85%+)
- **Source of Hire Effectiveness:** Performance and retention by source
- **Time-to-Productivity:** Days until full productivity

### Retention and Turnover
- **Voluntary Turnover Rate:** (Voluntary departures / avg headcount) x 100 (Target: <10%)
- **Involuntary Turnover Rate:** Performance management effectiveness indicator
- **Turnover by Segment:** Department, role, tenure, performance, manager
- **Regrettable vs. Non-Regrettable:** % high performers vs. low performers leaving
- **Retention Rate:** (Employees remaining / starting headcount) x 100 (Target: 90%+)
- **Cost of Turnover:** Recruiting + onboarding + lost productivity (50-200% of salary)

### Performance
- **Goal Achievement Rate:** % of goals/OKRs met (Target: 70-80% for stretch goals)
- **Performance Rating Distribution:** % in each tier
- **High Performer Retention:** % of top 20% retained (Target: 95%+)
- **Low Performer Management:** % of bottom 10% exited or improved (Target: 80%+)
- **Time-to-Proficiency:** Days to full productivity (varies by role)
- **Internal Mobility Rate:** % moving to new role internally (Target: 15-20%)

### Engagement
- **Employee Engagement Score:** Average survey rating (Target: 7.5/10 or 4.0/5.0)
- **eNPS (Employee Net Promoter Score):** % promoters - % detractors (Target: 30+)
- **Survey Participation Rate:** % completing survey (Target: 80%+)
- **Manager Effectiveness Score:** Direct report ratings (Target: 4.0/5.0+)
- **Pulse Survey Trends:** Real-time sentiment tracking

### Development
- **Training Completion Rate:** % of assigned training completed (Target: 90%+)
- **Training Hours per Employee:** Annual hours (Target: 40+)
- **Skill Gap Closure:** % reduction in gaps after training (Target: 50%+)
- **Internal Promotion Rate:** % of positions filled internally (Target: 30-40%)
- **High-Potential Identification:** % of workforce (Target: 10-15%)

### Diversity, Equity, Inclusion
- **Workforce Diversity:** % representation by demographics
- **Leadership Diversity:** % in leadership roles
- **Pay Equity:** Compensation parity (Target: <5% unexplained variance)
- **Inclusion Score:** Survey rating on feeling included (Target: 4.0/5.0+)
- **Diverse Candidate Slate:** % of finalist pools with diversity (Target: 50%+)

### Productivity
- **Revenue per Employee:** Total revenue / headcount
- **Profit per Employee:** Total profit / headcount
- **Absenteeism Rate:** % of scheduled days missed (Target: <3%)
- **Overtime Hours:** Average per employee
- **Span of Control:** Direct reports per manager (Target: 5-10)

## Data Requirements for Predictive Analytics

### Data Quality
- **Clean:** Consistent data across all HR systems
- **Standardized:** Common formats and definitions
- **Validated:** Regular audits and quality checks
- **Complete:** Minimal missing values

### Data Volume
- **Minimum:** 2 years of comprehensive employee data
- **Sample Size:** 200+ employees for statistical significance
- **Variables:** Multiple data points across different dimensions
- **Outcomes:** Historical results to train models (who left vs. stayed)

### Data Sources
- **HRIS:** Demographics, tenure, job history, compensation
- **Performance Management:** Ratings, goal achievement, feedback
- **Talent Acquisition:** Hiring source, time-to-hire, interview scores
- **Learning Management:** Training completion, certifications
- **Engagement Surveys:** Satisfaction, manager effectiveness, culture fit
- **Payroll:** Compensation changes, bonuses, equity
- **External Data:** Market conditions, industry trends, competitor intelligence

### Feature Engineering
- Compensation history and changes
- Training records and skill development
- Manager changes and relationship quality
- Peer feedback and collaboration patterns
- Promotion velocity and career progression
- Work-life balance indicators (hours, PTO usage)
- External factors (market conditions, commute distance)

## Analytics Tools and Platforms

### Specialized HR Analytics Platforms
- **Visier:** Comprehensive people analytics, predictive models, dashboards (17x more accurate than guesswork for exit risk)
- **HRBench:** Predictive analytics for 25+ HR metrics, visual forecasts
- **isolved:** All four analytics types, easy dashboards, enterprise-grade
- **Crunchr:** Workforce planning and scenario modeling
- **ChartHop:** Org planning and people analytics

### Business Intelligence Platforms
- **Microsoft Power BI:** Data visualization, integrates with Microsoft ecosystem, predictive analytics
- **Tableau:** Advanced visualization, Salesforce Einstein AI integration
- **Qlik Sense:** Associative analytics, self-service BI
- **Looker (Google):** Cloud-native, real-time dashboards

### All-in-One HRIS with Analytics
- **Workday:** Prism Analytics, predictive insights, benchmarking
- **SAP SuccessFactors:** Workforce Analytics, People Analytics
- **Oracle HCM Cloud:** Analytics Cloud, AI-powered insights
- **BambooHR:** Standard and custom reports, basic analytics

### Machine Learning Algorithms
- **Decision Trees:** Classification (will employee leave?), easy to interpret
- **Logistic Regression:** Binary outcomes (promote/don't promote), probability scores
- **Random Forest:** High accuracy, handles large datasets
- **Neural Networks:** Complex pattern recognition, large data requirements
- **Transformer Neural Networks:** Time series analysis, sequential data
- **Clustering (K-Means):** Segmentation (employee personas, performance groups)
- **Natural Language Processing (NLP):** Text analysis (survey comments, exit interviews)

## Implementation Roadmap

### Phase 1: Descriptive Analytics (Months 1-3)
**Goal:** Build dashboards for key metrics

**Actions:**
- Identify critical metrics to track
- Ensure data quality and integration across systems
- Build dashboards in BI tool (Power BI, Tableau)
- Establish baseline measurements
- Create regular reporting cadence

**Deliverables:**
- HR metrics dashboard (turnover, headcount, time-to-hire, engagement)
- Monthly/quarterly reports
- Data governance and quality standards

### Phase 2: Diagnostic Analytics (Months 4-6)
**Goal:** Understand root causes of trends

**Actions:**
- Conduct correlation analyses
- Segment data for deeper insights (by department, role, demographics)
- Investigate anomalies and trends
- Root cause analysis on key issues (turnover spikes, engagement drops)

**Deliverables:**
- Diagnostic reports on key issues
- Segmented analytics
- Insights and recommendations

### Phase 3: Predictive Analytics (Months 7-12)
**Goal:** Forecast future outcomes

**Actions:**
- Select high-impact use case (e.g., turnover prediction)
- Build and validate predictive model
- Pilot with one department
- Refine model based on feedback
- Scale to organization

**Deliverables:**
- Turnover prediction model
- Risk scores for employees
- Pilot results and learnings
- Scaled predictive analytics

### Phase 4: Prescriptive Analytics (Months 13-18)
**Goal:** Recommend actions

**Actions:**
- Develop recommendation engines
- Automate interventions where appropriate
- Integrate with HR workflows
- Measure impact of recommendations

**Deliverables:**
- Automated retention intervention recommendations
- Personalized development plan suggestions
- Integrated analytics in HR processes

## Best Practices

### 1. Start with Business Questions
- Don't start with data looking for insights
- Start with problems and find data to answer them
- Examples: Why is turnover high? Which candidates will succeed? What drives engagement?

### 2. Ensure Data Quality
- Conduct data audit (completeness, accuracy, consistency)
- Standardize formats and definitions
- Establish data governance
- Regular quality checks and validation

### 3. Build Analytics Capability
- Hire or develop data analysts/scientists
- Train HR team on data literacy
- Partner with IT and data teams
- Consider external consultants for specialized projects

### 4. Start Small and Scale
- Begin with descriptive analytics and dashboards
- Progress to diagnostic, then predictive, then prescriptive
- Pilot predictive models with one use case
- Scale based on results and learnings

### 5. Ensure Privacy and Ethics
- Comply with GDPR, CCPA, and other regulations
- Anonymize data where appropriate
- Audit models for bias (gender, race, age)
- Transparent communication about data usage
- Never use analytics punitively

### 6. Integrate with Decision-Making
- Translate data into clear recommendations
- Embed analytics in existing HR processes
- Provide real-time dashboards for managers
- Enable self-service analytics
- Combine data with human judgment

### 7. Measure and Communicate Impact
- Track ROI of analytics initiatives
- Measure changes in key outcomes (turnover, engagement, productivity)
- Calculate cost savings and revenue impact
- Share results with leadership
- Use storytelling and visualization

## Common Pitfalls to Avoid

1. **Analysis Paralysis:** Don't wait for perfect data, start with what you have
2. **Ignoring Data Quality:** Garbage in, garbage out - prioritize data quality
3. **Lack of Business Context:** Analytics without business understanding is meaningless
4. **Overcomplicating:** Start simple, add complexity as needed
5. **No Action:** Insights without action are wasted - ensure recommendations are implemented
6. **Ignoring Privacy:** Data privacy violations can be catastrophic
7. **Algorithmic Bias:** Models can perpetuate existing biases - audit regularly
8. **Replacing Human Judgment:** Analytics informs, doesn't replace human decision-making

## Real-World Examples

**HP - Project Insight:**
- Predicted employee turnover with high accuracy
- Reduced turnover from 20% to <10% (2009-2011)
- Saved estimated $300M
- Enabled proactive manager interventions

**Google - Prediction Engine:**
- Analyzes job history, education, skills, personality to predict candidate success
- Improved hiring quality and reduced mis-hires
- Project Aristotle identified elements of effective teams

**Best Buy - Engagement-Revenue Link:**
- Linked 0.1% engagement increase to $100K revenue per store
- Measured engagement more frequently
- Implemented targeted interventions

**Cisco - Workforce Planning:**
- Predictive analytics for skills gap forecasting
- Proactive reskilling and hiring
- Reduced time to fill critical roles

**American Express - Remote Work Transition:**
- Predicted when employees would need IT support
- Proactive support deployment
- Smooth transition to remote work

**Unilever + HireVue - Video Interview Analysis:**
- Machine learning analysis of video interviews
- 90% faster hiring process
- £1M annual cost savings

## Using the Reference Files

### When to Read Each Reference

**`/references/people-analytics-frameworks.md`** — Read when developing overall people analytics strategy, understanding analytics maturity models, or designing analytics governance. Covers strategic frameworks, organizational readiness, and analytics program design.

**`/references/predictive-modeling.md`** — Read when building predictive models for turnover, hiring, performance, or other HR outcomes. Includes detailed modeling techniques, algorithms, validation methods, and implementation guidance.

**`/references/hr-metrics.md`** — Read when defining which metrics to track, building HR dashboards, or establishing baseline measurements. Comprehensive catalog of HR metrics across all functions with targets and calculation methods.

**`/references/analytics-tools.md`** — Read when selecting analytics platforms, evaluating BI tools, or building analytics infrastructure. Covers tool comparisons, implementation considerations, and technology stack recommendations.