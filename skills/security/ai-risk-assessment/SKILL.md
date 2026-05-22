---
name: AI Risk Assessment
description: Identifying, assessing, and mitigating risks in AI systems including bias, safety, privacy, security, and ethical concerns.
---

# AI Risk Assessment

## Overview

AI Risk Assessment is the systematic process of identifying potential harms from AI systems, evaluating their likelihood and impact, and implementing mitigations. This is essential for responsible AI deployment and regulatory compliance.

**Core Principle**: "Identify risks before they become incidents. Prevention is cheaper than remediation."

---

## 1. Types of AI Risks

| Risk Category | Description | Example |
|---------------|-------------|---------|
| **Safety** | Physical harm to people | Autonomous vehicle crash |
| **Bias & Fairness** | Discrimination against groups | Loan denial based on race |
| **Privacy** | Unauthorized data exposure | Model leaking training data |
| **Security** | Malicious attacks | Adversarial examples fooling classifier |
| **Reliability** | System failures | Model crashes on edge cases |
| **Ethical** | Harmful content/behavior | LLM generating hate speech |
| **Reputational** | Brand damage | AI making embarrassing mistakes publicly |
| **Legal** | Regulatory violations | GDPR non-compliance |

---

## 2. Risk Assessment Framework

### Step 1: Identify Risks
```python
class RiskIdentification:
    """Systematic risk identification"""
    
    @staticmethod
    def identify_risks(ai_system: dict) -> List[Risk]:
        risks = []
        
        # Safety risks
        if ai_system['domain'] in ['autonomous_vehicles', 'medical', 'industrial']:
            risks.append(Risk(
                category='safety',
                description='Physical harm from incorrect decisions',
                likelihood='medium',
                impact='critical'
            ))
        
        # Bias risks
        if ai_system['affects_people']:
            risks.append(Risk(
                category='bias',
                description='Discrimination against protected groups',
                likelihood='high',
                impact='high'
            ))
        
        # Privacy risks
        if ai_system['uses_personal_data']:
            risks.append(Risk(
                category='privacy',
                description='PII exposure or model inversion',
                likelihood='medium',
                impact='high'
            ))
        
        # Security risks
        risks.append(Risk(
            category='security',
            description='Adversarial attacks or prompt injection',
            likelihood='medium',
            impact='medium'
        ))
        
        return risks
```

### Step 2: Assess Likelihood and Impact
```python
class RiskMatrix:
    """Risk matrix for prioritization"""
    
    LIKELIHOOD = {
        'rare': 1,
        'unlikely': 2,
        'possible': 3,
        'likely': 4,
        'certain': 5
    }
    
    IMPACT = {
        'negligible': 1,
        'minor': 2,
        'moderate': 3,
        'major': 4,
        'critical': 5
    }
    
    @staticmethod
    def calculate_risk_score(likelihood: str, impact: str) -> int:
        """Calculate risk score (1-25)"""
        return RiskMatrix.LIKELIHOOD[likelihood] * RiskMatrix.IMPACT[impact]
    
    @staticmethod
    def get_risk_level(score: int) -> str:
        """Categorize risk level"""
        if score >= 15:
            return 'critical'
        elif score >= 10:
            return 'high'
        elif score >= 5:
            return 'medium'
        else:
            return 'low'
```

### Step 3: Prioritize Risks
```python
def prioritize_risks(risks: List[Risk]) -> List[Risk]:
    """Prioritize risks by score"""
    
    for risk in risks:
        risk.score = RiskMatrix.calculate_risk_score(
            risk.likelihood,
            risk.impact
        )
        risk.level = RiskMatrix.get_risk_level(risk.score)
    
    return sorted(risks, key=lambda r: r.score, reverse=True)
```

---

## 3. Bias and Fairness Assessment

### Fairness Metrics
```python
from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference

def assess_fairness(y_true, y_pred, sensitive_features):
    """Assess model fairness across groups"""
    
    # Demographic parity
    dp_diff = demographic_parity_difference(
        y_true, y_pred, sensitive_features=sensitive_features
    )
    
    # Equalized odds
    eo_diff = equalized_odds_difference(
        y_true, y_pred, sensitive_features=sensitive_features
    )
    
    # Per-group metrics
    mf = MetricFrame(
        metrics={'accuracy': accuracy_score, 'precision': precision_score},
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # Assess risk
    fairness_risk = {
        'demographic_parity_diff': dp_diff,
        'equalized_odds_diff': eo_diff,
        'per_group_metrics': mf.by_group.to_dict(),
        'risk_level': 'high' if abs(dp_diff) > 0.1 or abs(eo_diff) > 0.1 else 'low'
    }
    
    return fairness_risk
```

### Bias Testing Across Groups
```python
def test_bias_across_demographics(model, test_data):
    """Test for bias across demographic groups"""
    
    demographics = ['gender', 'race', 'age_group']
    bias_report = {}
    
    for demo in demographics:
        groups = test_data[demo].unique()
        
        for group in groups:
            group_data = test_data[test_data[demo] == group]
            
            # Predict
            predictions = model.predict(group_data)
            
            # Calculate metrics
            accuracy = accuracy_score(group_data['label'], predictions)
            approval_rate = predictions.mean()
            
            bias_report[f"{demo}_{group}"] = {
                'accuracy': accuracy,
                'approval_rate': approval_rate,
                'sample_size': len(group_data)
            }
    
    # Check for disparate impact
    for demo in demographics:
        groups = [k for k in bias_report.keys() if k.startswith(demo)]
        approval_rates = [bias_report[g]['approval_rate'] for g in groups]
        
        disparate_impact = min(approval_rates) / max(approval_rates)
        
        if disparate_impact < 0.8:  # 80% rule
            logger.warning(
                f"Disparate impact detected for {demo}: {disparate_impact:.2f}"
            )
    
    return bias_report
```

---

## 4. Safety Assessment

### Failure Mode Analysis
```python
class FailureModeAnalysis:
    """Identify what can go wrong"""
    
    @staticmethod
    def identify_failure_modes(ai_system: dict) -> List[FailureMode]:
        failure_modes = []
        
        # False positives
        failure_modes.append(FailureMode(
            name='false_positive',
            description='Model incorrectly predicts positive class',
            consequence=ai_system.get('false_positive_consequence', 'User inconvenience'),
            mitigation='Increase precision threshold'
        ))
        
        # False negatives
        failure_modes.append(FailureMode(
            name='false_negative',
            description='Model misses positive cases',
            consequence=ai_system.get('false_negative_consequence', 'Missed opportunity'),
            mitigation='Lower decision threshold'
        ))
        
        # Out-of-distribution inputs
        failure_modes.append(FailureMode(
            name='ood_input',
            description='Input outside training distribution',
            consequence='Unpredictable behavior',
            mitigation='OOD detection and rejection'
        ))
        
        # Model degradation
        failure_modes.append(FailureMode(
            name='model_drift',
            description='Model performance degrades over time',
            consequence='Increasing error rate',
            mitigation='Continuous monitoring and retraining'
        ))
        
        return failure_modes
```

### Red Teaming
```python
def red_team_testing(model, test_cases):
    """Adversarial testing to find weaknesses"""
    
    vulnerabilities = []
    
    # Test edge cases
    for test_case in test_cases['edge_cases']:
        prediction = model.predict(test_case['input'])
        
        if prediction != test_case['expected']:
            vulnerabilities.append({
                'type': 'edge_case_failure',
                'input': test_case['input'],
                'expected': test_case['expected'],
                'actual': prediction
            })
    
    # Test adversarial examples
    for adv_example in test_cases['adversarial']:
        prediction = model.predict(adv_example['input'])
        
        if prediction == adv_example['target_class']:
            vulnerabilities.append({
                'type': 'adversarial_success',
                'input': adv_example['input'],
                'fooled_into': prediction
            })
    
    return vulnerabilities
```

---

## 5. Privacy Risk Assessment

### PII Exposure Risk
```python
def assess_pii_exposure_risk(training_data, model):
    """Assess risk of PII leakage"""
    
    risks = []
    
    # Check if training data contains PII
    pii_fields = ['email', 'phone', 'ssn', 'name', 'address']
    pii_found = [field for field in pii_fields if field in training_data.columns]
    
    if pii_found:
        risks.append({
            'risk': 'pii_in_training_data',
            'severity': 'high',
            'fields': pii_found,
            'mitigation': 'Remove or anonymize PII before training'
        })
    
    # Test for membership inference
    membership_attack_success = test_membership_inference(model, training_data)
    
    if membership_attack_success > 0.6:  # >60% success rate
        risks.append({
            'risk': 'membership_inference_vulnerable',
            'severity': 'medium',
            'success_rate': membership_attack_success,
            'mitigation': 'Apply differential privacy'
        })
    
    return risks
```

### Model Inversion Attack Test
```python
def test_model_inversion(model, target_features):
    """Test if model can be inverted to reconstruct training data"""
    
    # Attempt to reconstruct features from model outputs
    reconstructed = attempt_reconstruction(model, target_features)
    
    # Measure similarity to original data
    similarity = calculate_similarity(reconstructed, target_features)
    
    if similarity > 0.7:  # High similarity = vulnerable
        return {
            'vulnerable': True,
            'similarity': similarity,
            'risk_level': 'high',
            'mitigation': 'Add noise to outputs or use differential privacy'
        }
    
    return {'vulnerable': False}
```

---

## 6. Security Risk Assessment

### Adversarial Attack Vectors
```python
class AdversarialRiskAssessment:
    """Assess vulnerability to adversarial attacks"""
    
    @staticmethod
    def test_adversarial_robustness(model, test_data, epsilon=0.1):
        """Test robustness against adversarial examples"""
        
        from art.attacks.evasion import FastGradientMethod
        from art.estimators.classification import SklearnClassifier
        
        # Wrap model
        classifier = SklearnClassifier(model=model)
        
        # Create attack
        attack = FastGradientMethod(estimator=classifier, eps=epsilon)
        
        # Generate adversarial examples
        x_adv = attack.generate(x=test_data)
        
        # Evaluate
        original_accuracy = model.score(test_data, test_labels)
        adversarial_accuracy = model.score(x_adv, test_labels)
        
        robustness_score = adversarial_accuracy / original_accuracy
        
        return {
            'original_accuracy': original_accuracy,
            'adversarial_accuracy': adversarial_accuracy,
            'robustness_score': robustness_score,
            'risk_level': 'high' if robustness_score < 0.7 else 'medium'
        }
```

### Prompt Injection Testing (LLMs)
```python
def test_prompt_injection(llm, test_prompts):
    """Test LLM vulnerability to prompt injection"""
    
    vulnerabilities = []
    
    for prompt in test_prompts:
        response = llm.generate(prompt['injection_attempt'])
        
        # Check if injection succeeded
        if prompt['target_behavior'] in response.lower():
            vulnerabilities.append({
                'prompt': prompt['injection_attempt'],
                'succeeded': True,
                'response': response
            })
    
    vulnerability_rate = len(vulnerabilities) / len(test_prompts)
    
    return {
        'vulnerability_rate': vulnerability_rate,
        'risk_level': 'critical' if vulnerability_rate > 0.3 else 'medium',
        'examples': vulnerabilities[:5]  # Top 5 examples
    }
```

---

## 7. Ethical Risk Assessment

### Harmful Content Generation
```python
def assess_harmful_content_risk(llm):
    """Assess risk of generating harmful content"""
    
    test_categories = [
        'hate_speech',
        'violence',
        'illegal_activity',
        'misinformation',
        'self_harm'
    ]
    
    risks = {}
    
    for category in test_categories:
        prompts = load_test_prompts(category)
        harmful_responses = 0
        
        for prompt in prompts:
            response = llm.generate(prompt)
            
            if is_harmful(response, category):
                harmful_responses += 1
        
        risk_rate = harmful_responses / len(prompts)
        risks[category] = {
            'risk_rate': risk_rate,
            'severity': 'critical' if risk_rate > 0.1 else 'medium'
        }
    
    return risks
```

---

## 8. Risk Documentation

### Risk Register
```python
class RiskRegister:
    """Central registry of identified risks"""
    
    def __init__(self):
        self.risks = []
    
    def add_risk(
        self,
        category: str,
        description: str,
        likelihood: str,
        impact: str,
        mitigation: str,
        owner: str
    ):
        risk = {
            'id': generate_risk_id(),
            'category': category,
            'description': description,
            'likelihood': likelihood,
            'impact': impact,
            'score': RiskMatrix.calculate_risk_score(likelihood, impact),
            'level': RiskMatrix.get_risk_level(
                RiskMatrix.calculate_risk_score(likelihood, impact)
            ),
            'mitigation': mitigation,
            'owner': owner,
            'status': 'identified',
            'created_at': datetime.now()
        }
        
        self.risks.append(risk)
        return risk['id']
    
    def get_critical_risks(self):
        """Get all critical risks"""
        return [r for r in self.risks if r['level'] == 'critical']
    
    def export_to_csv(self, filename):
        """Export risk register to CSV"""
        import pandas as pd
        df = pd.DataFrame(self.risks)
        df.to_csv(filename, index=False)
```

### Risk Matrix Visualization
```python
import matplotlib.pyplot as plt
import numpy as np

def visualize_risk_matrix(risks):
    """Visualize risks on likelihood x impact matrix"""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot each risk
    for risk in risks:
        x = RiskMatrix.LIKELIHOOD[risk['likelihood']]
        y = RiskMatrix.IMPACT[risk['impact']]
        
        color = {
            'critical': 'red',
            'high': 'orange',
            'medium': 'yellow',
            'low': 'green'
        }[risk['level']]
        
        ax.scatter(x, y, s=200, c=color, alpha=0.6)
        ax.annotate(risk['category'], (x, y), fontsize=8)
    
    # Labels
    ax.set_xlabel('Likelihood')
    ax.set_ylabel('Impact')
    ax.set_title('AI Risk Matrix')
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xticklabels(['Rare', 'Unlikely', 'Possible', 'Likely', 'Certain'])
    ax.set_yticklabels(['Negligible', 'Minor', 'Moderate', 'Major', 'Critical'])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('risk_matrix.png')
```

---

## 9. Risk Mitigation Strategies

### Guardrails (Input/Output Filters)
```python
class AIGuardrails:
    """Input and output filtering for safety"""
    
    @staticmethod
    def filter_input(user_input: str) -> dict:
        """Filter potentially harmful inputs"""
        
        # Check for prompt injection
        if contains_injection_pattern(user_input):
            return {
                'allowed': False,
                'reason': 'Potential prompt injection detected'
            }
        
        # Check for PII
        if contains_pii(user_input):
            return {
                'allowed': False,
                'reason': 'PII detected in input'
            }
        
        return {'allowed': True}
    
    @staticmethod
    def filter_output(ai_output: str) -> dict:
        """Filter potentially harmful outputs"""
        
        # Check for harmful content
        if is_harmful(ai_output):
            return {
                'allowed': False,
                'reason': 'Harmful content detected',
                'filtered_output': '[Content filtered for safety]'
            }
        
        # Check for PII leakage
        if contains_pii(ai_output):
            return {
                'allowed': False,
                'reason': 'PII detected in output',
                'filtered_output': redact_pii(ai_output)
            }
        
        return {'allowed': True, 'output': ai_output}
```

---

## 10. Continuous Risk Monitoring

```python
class RiskMonitoring:
    """Continuous monitoring of AI risks"""
    
    @staticmethod
    def monitor_model_performance():
        """Monitor for performance degradation"""
        
        current_accuracy = calculate_current_accuracy()
        baseline_accuracy = get_baseline_accuracy()
        
        if current_accuracy < baseline_accuracy * 0.95:  # 5% drop
            alert(
                severity='warning',
                message=f'Model accuracy dropped to {current_accuracy:.1%}'
            )
    
    @staticmethod
    def monitor_fairness_drift():
        """Monitor for fairness metric changes"""
        
        current_fairness = calculate_fairness_metrics()
        baseline_fairness = get_baseline_fairness()
        
        for metric, value in current_fairness.items():
            if abs(value - baseline_fairness[metric]) > 0.1:
                alert(
                    severity='warning',
                    message=f'Fairness metric {metric} drifted: {value:.2f}'
                )
```

---

## 11. AI Risk Assessment Checklist

- [ ] **Risk Identification**: Have we identified all potential risks?
- [ ] **Bias Testing**: Have we tested for bias across demographic groups?
- [ ] **Safety Analysis**: Have we performed failure mode analysis?
- [ ] **Privacy Assessment**: Have we tested for PII exposure?
- [ ] **Security Testing**: Have we tested for adversarial robustness?
- [ ] **Ethical Review**: Have we assessed harmful content risk?
- [ ] **Risk Register**: Are all risks documented and prioritized?
- [ ] **Mitigations**: Do we have mitigations for critical risks?
- [ ] **Monitoring**: Are we continuously monitoring for risk indicators?
- [ ] **Compliance**: Do we meet regulatory requirements (EU AI Act)?

---

## Related Skills
* `44-ai-governance/model-bias-fairness`
* `44-ai-governance/ai-data-privacy`
* `44-ai-governance/model-risk-management`
* `44-ai-governance/ai-ethics-compliance`
