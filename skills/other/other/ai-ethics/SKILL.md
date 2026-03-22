---
name: ai-ethics
description: "Implement ethical AI practices and responsible AI governance. Use for: identifying and mitigating bias in datasets and models, ensuring fairness across demographic groups, implementing transparency and explainability requirements, protecting user privacy and data security, establishing accountability frameworks, conducting ethical impact assessments, complying with AI regulations (GDPR, EU AI Act), implementing human oversight mechanisms, and building trustworthy AI systems aligned with societal values."
---

# AI Ethics

Build responsible, fair, and trustworthy AI systems that respect human rights and societal values.

## Overview

AI ethics addresses moral questions and societal impacts of artificial intelligence systems. As AI increasingly influences critical decisions in healthcare, finance, criminal justice, and employment, ensuring ethical development and deployment is paramount. This skill covers fairness, transparency, accountability, privacy, safety, and governance frameworks for responsible AI.

## Core Ethical Principles

### Fairness and Non-Discrimination

Ensure AI systems treat all individuals and groups equitably.

**Key Concepts:**
- **Individual Fairness**: Similar individuals receive similar outcomes
- **Group Fairness**: Equal outcomes across demographic groups
- **Equalized Odds**: Equal true positive and false positive rates across groups
- **Demographic Parity**: Equal prediction rates across groups

```python
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing

# Load dataset with protected attributes
dataset = BinaryLabelDataset(
    df=df,
    label_names=['outcome'],
    protected_attribute_names=['race', 'gender']
)

# Measure bias
metric = BinaryLabelDatasetMetric(
    dataset,
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)

print(f"Disparate Impact: {metric.disparate_impact()}")
print(f"Statistical Parity Difference: {metric.statistical_parity_difference()}")

# Mitigate bias with reweighing
rw = Reweighing(
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)
dataset_transformed = rw.fit_transform(dataset)
```

### Transparency and Explainability

Make AI decision-making processes understandable to stakeholders.

```python
import shap

# SHAP explanations
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Visualize feature importance
shap.summary_plot(shap_values, X_test, plot_type="bar")

# Individual prediction explanation
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

### Accountability

Establish clear responsibility for AI system outcomes.

```python
class AIAccountabilityFramework:
    def __init__(self, model_name, owner, stakeholders):
        self.model_name = model_name
        self.owner = owner
        self.stakeholders = stakeholders
        self.decision_log = []
        self.audit_trail = []
    
    def log_decision(self, input_data, prediction, confidence, timestamp):
        self.decision_log.append({
            'timestamp': timestamp,
            'input': input_data,
            'prediction': prediction,
            'confidence': confidence,
            'model_version': self.get_model_version()
        })
    
    def audit(self):
        return {
            'total_decisions': len(self.decision_log),
            'average_confidence': np.mean([d['confidence'] for d in self.decision_log]),
            'decision_distribution': self.analyze_distribution(),
            'bias_metrics': self.calculate_bias_metrics()
        }
```

### Privacy and Data Protection

Protect personal information throughout the AI lifecycle.

```python
# Differential privacy
from diffprivlib.models import LogisticRegression

# Train with differential privacy
dp_model = LogisticRegression(epsilon=1.0)
dp_model.fit(X_train, y_train)

# Federated learning for privacy
import flwr as fl

class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self):
        return model.get_weights()
    
    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(X_train, y_train, epochs=1, batch_size=32)
        return model.get_weights(), len(X_train), {}
    
    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(X_test, y_test)
        return loss, len(X_test), {"accuracy": accuracy}

# Data anonymization
from faker import Faker
fake = Faker()

def anonymize_data(df):
    df['name'] = df['name'].apply(lambda x: fake.name())
    df['email'] = df['email'].apply(lambda x: fake.email())
    df['ssn'] = df['ssn'].apply(lambda x: fake.ssn())
    return df
```

## Bias Detection and Mitigation

### Identifying Bias Sources

**Data Bias:**
- Historical bias in training data
- Sampling bias (underrepresentation)
- Measurement bias (proxy variables)
- Label bias (biased annotations)

**Algorithmic Bias:**
- Feature selection bias
- Model architecture bias
- Optimization objective bias

**Deployment Bias:**
- Population shift
- Feedback loops
- User interaction bias

### Bias Mitigation Techniques

**Pre-processing:**
```python
from aif360.algorithms.preprocessing import DisparateImpactRemover

# Remove disparate impact
di_remover = DisparateImpactRemover(repair_level=1.0)
dataset_transformed = di_remover.fit_transform(dataset)
```

**In-processing:**
```python
from aif360.algorithms.inprocessing import PrejudiceRemover

# Train with fairness constraints
pr = PrejudiceRemover(sensitive_attr='race', eta=1.0)
pr.fit(dataset)
```

**Post-processing:**
```python
from aif360.algorithms.postprocessing import EqOddsPostprocessing

# Adjust predictions for equal odds
eop = EqOddsPostprocessing(
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)
dataset_pred_transformed = eop.fit_predict(dataset_val, dataset_pred)
```

## Fairness Metrics

```python
def calculate_fairness_metrics(y_true, y_pred, sensitive_attr):
    metrics = {}
    
    # Demographic parity
    metrics['demographic_parity'] = abs(
        y_pred[sensitive_attr == 0].mean() - 
        y_pred[sensitive_attr == 1].mean()
    )
    
    # Equal opportunity
    tpr_0 = ((y_pred[sensitive_attr == 0] == 1) & (y_true[sensitive_attr == 0] == 1)).mean()
    tpr_1 = ((y_pred[sensitive_attr == 1] == 1) & (y_true[sensitive_attr == 1] == 1)).mean()
    metrics['equal_opportunity'] = abs(tpr_0 - tpr_1)
    
    # Equalized odds
    fpr_0 = ((y_pred[sensitive_attr == 0] == 1) & (y_true[sensitive_attr == 0] == 0)).mean()
    fpr_1 = ((y_pred[sensitive_attr == 1] == 1) & (y_true[sensitive_attr == 1] == 0)).mean()
    metrics['equalized_odds'] = abs(tpr_0 - tpr_1) + abs(fpr_0 - fpr_1)
    
    return metrics
```

## AI Governance Frameworks

### OECD AI Principles

1. **Inclusive Growth**: AI should benefit all people and the planet
2. **Sustainable Development**: Support environmental sustainability
3. **Human-Centered Values**: Respect rule of law, human rights, democratic values
4. **Transparency**: Provide meaningful information about AI systems
5. **Robustness and Safety**: Function appropriately and safely

### EU AI Act Risk Classification

```python
class AIRiskClassifier:
    UNACCEPTABLE_RISK = [
        'social_scoring',
        'subliminal_manipulation',
        'exploitation_of_vulnerabilities',
        'biometric_categorization'
    ]
    
    HIGH_RISK = [
        'critical_infrastructure',
        'education_access',
        'employment',
        'essential_services',
        'law_enforcement',
        'migration_management',
        'justice_administration'
    ]
    
    def classify_system(self, use_case, domain):
        if use_case in self.UNACCEPTABLE_RISK:
            return 'PROHIBITED'
        elif domain in self.HIGH_RISK:
            return 'HIGH_RISK'  # Requires conformity assessment
        else:
            return 'LIMITED_RISK'  # Transparency obligations
```

### NIST AI Risk Management Framework

```python
class NISTAIRiskFramework:
    def __init__(self):
        self.functions = ['govern', 'map', 'measure', 'manage']
    
    def govern(self):
        # Establish policies, processes, and procedures
        return {
            'policies': self.define_policies(),
            'roles': self.assign_roles(),
            'resources': self.allocate_resources()
        }
    
    def map(self):
        # Understand AI system context and risks
        return {
            'context': self.document_context(),
            'risks': self.identify_risks(),
            'impacts': self.assess_impacts()
        }
    
    def measure(self):
        # Quantify and assess risks
        return {
            'metrics': self.define_metrics(),
            'testing': self.conduct_testing(),
            'validation': self.validate_system()
        }
    
    def manage(self):
        # Prioritize and respond to risks
        return {
            'mitigation': self.implement_controls(),
            'monitoring': self.continuous_monitoring(),
            'response': self.incident_response()
        }
```

## Ethical Impact Assessment

```python
class EthicalImpactAssessment:
    def __init__(self, ai_system):
        self.ai_system = ai_system
        self.assessment = {}
    
    def assess(self):
        self.assessment['stakeholder_analysis'] = self.identify_stakeholders()
        self.assessment['benefit_harm_analysis'] = self.analyze_benefits_harms()
        self.assessment['fairness_evaluation'] = self.evaluate_fairness()
        self.assessment['transparency_check'] = self.check_transparency()
        self.assessment['privacy_assessment'] = self.assess_privacy()
        self.assessment['safety_evaluation'] = self.evaluate_safety()
        self.assessment['accountability_framework'] = self.establish_accountability()
        
        return self.generate_report()
    
    def identify_stakeholders(self):
        return {
            'direct_users': [],
            'indirect_affected': [],
            'decision_makers': [],
            'oversight_bodies': []
        }
    
    def analyze_benefits_harms(self):
        return {
            'benefits': {
                'efficiency': 'score',
                'accuracy': 'score',
                'accessibility': 'score'
            },
            'harms': {
                'discrimination_risk': 'score',
                'privacy_risk': 'score',
                'safety_risk': 'score'
            }
        }
```

## Human Oversight

```python
class HumanInTheLoop:
    def __init__(self, model, confidence_threshold=0.8):
        self.model = model
        self.confidence_threshold = confidence_threshold
    
    def predict_with_oversight(self, input_data):
        prediction = self.model.predict(input_data)
        confidence = self.model.predict_proba(input_data).max()
        
        if confidence < self.confidence_threshold:
            # Flag for human review
            return {
                'prediction': prediction,
                'confidence': confidence,
                'requires_review': True,
                'reason': 'Low confidence'
            }
        
        # High-stakes decisions always require human review
        if self.is_high_stakes(input_data):
            return {
                'prediction': prediction,
                'confidence': confidence,
                'requires_review': True,
                'reason': 'High-stakes decision'
            }
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'requires_review': False
        }
```

## Model Cards and Documentation

```python
class ModelCard:
    def __init__(self, model_name):
        self.model_name = model_name
        self.card = {
            'model_details': {},
            'intended_use': {},
            'factors': {},
            'metrics': {},
            'evaluation_data': {},
            'training_data': {},
            'quantitative_analyses': {},
            'ethical_considerations': {},
            'caveats_recommendations': {}
        }
    
    def populate(self):
        self.card['model_details'] = {
            'developer': 'Organization name',
            'model_date': '2026-03-16',
            'model_version': '1.0',
            'model_type': 'Classification',
            'training_algorithms': 'Random Forest',
            'paper_or_resources': 'Link to paper'
        }
        
        self.card['intended_use'] = {
            'primary_uses': 'Credit risk assessment',
            'primary_users': 'Financial institutions',
            'out_of_scope': 'Not for medical decisions'
        }
        
        self.card['ethical_considerations'] = {
            'sensitive_data': 'Contains demographic information',
            'human_life': 'Impacts financial access',
            'mitigations': 'Bias testing and monitoring',
            'risks_and_harms': 'Potential for discriminatory outcomes'
        }
        
        return self.card
```

## Best Practices

**Development:**
- Conduct ethical impact assessments early
- Include diverse perspectives in design
- Document assumptions and limitations
- Test for bias across demographic groups

**Deployment:**
- Implement human oversight for high-stakes decisions
- Provide clear explanations to affected individuals
- Enable appeals and recourse mechanisms
- Monitor for unintended consequences

**Governance:**
- Establish clear accountability structures
- Create ethics review boards
- Implement regular audits
- Maintain comprehensive documentation

**Continuous Improvement:**
- Monitor fairness metrics in production
- Collect feedback from affected communities
- Update models to address emerging issues
- Stay informed on evolving regulations

## Regulatory Compliance

**GDPR (EU):**
- Right to explanation for automated decisions
- Data minimization and purpose limitation
- Privacy by design and default

**EU AI Act:**
- Risk-based classification
- Conformity assessments for high-risk systems
- Transparency obligations

**US Executive Orders:**
- Safety and security standards
- Equity and civil rights protections
- Privacy safeguards

## Tools and Resources

- **AI Fairness 360 (AIF360)**: IBM's bias detection and mitigation toolkit
- **Fairlearn**: Microsoft's fairness assessment and mitigation library
- **What-If Tool**: Google's model understanding tool
- **Model Cards Toolkit**: TensorFlow's model documentation framework
- **Responsible AI Toolbox**: Microsoft's comprehensive toolkit

## Learning Path

1. **Foundations**: Ethical principles, bias concepts
2. **Technical**: Fairness metrics, bias mitigation
3. **Governance**: Frameworks, compliance, documentation
4. **Advanced**: Impact assessment, oversight mechanisms

See `references/` for regulatory guides, case studies, and implementation templates.
