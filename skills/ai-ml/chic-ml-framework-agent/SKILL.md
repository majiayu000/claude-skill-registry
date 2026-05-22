---name: chic-ml-framework-agent
description: Machine learning framework for inferring high-risk clonal hematopoiesis from complete blood count data without sequencing, reducing the number needed to sequence for CHIP screening.
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
  created: "2026-01-20"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
  - write_file

keywords:
  - chic-ml-framework-agent
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# CHIC ML Framework Agent

The **CHIC (Clonal Hematopoiesis Inference from Counts) ML Framework Agent** uses machine learning to identify individuals with high-risk clonal hematopoiesis from routine complete blood count (CBC) data alone. Validated on 431,531 UK Biobank participants, CHIC reduces the "number needed to sequence" from 727 to 40 individuals per case of high-risk CH, enabling population-scale CHIP screening without universal sequencing.

## When to Use This Skill

* When screening large populations for CHIP without sequencing.
* For prioritizing individuals who should undergo genetic testing.
* To identify undiagnosed CCUS/MDS from routine blood counts.
* When sequencing resources are limited but CHIP detection is needed.
* For research studies requiring CHIP prevalence estimation.

## Core Capabilities

1. **CBC-Based CHIP Prediction**: Predict CHIP presence from blood counts.

2. **High-Risk CH Identification**: Focus on clinically relevant clones.

3. **Efficient Screening**: Dramatically reduce number needed to sequence.

4. **CCUS/MDS Detection**: Flag potential undiagnosed blood cancers.

5. **Population Stratification**: Risk-stratify for targeted sequencing.

6. **Longitudinal Monitoring**: Track CBC changes suggesting CH development.

## CHIC Model Features

| CBC Parameter | Importance | CH Association |
|---------------|------------|----------------|
| Red Cell Distribution Width (RDW) | High | ↑ with CH |
| Mean Corpuscular Volume (MCV) | High | ↑ macrocytosis |
| Hemoglobin | Moderate | ↓ in CCUS |
| Platelet Count | Moderate | Variable |
| White Blood Cell Count | Moderate | Often ↑ |
| Mean Platelet Volume (MPV) | Moderate | May ↑ |
| Red Blood Cell Count | Low | ↓ with anemia |

## Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| AUROC | 0.75 | Good discrimination |
| Sensitivity (high threshold) | 85% | High-risk CH capture |
| NNS (standard) | 727 | Without CHIC |
| NNS (with CHIC) | 40 | 18x improvement |
| PPV (stringent cutoff) | 12% | Enriched population |

## Workflow

1. **Input**: CBC data (complete blood count panel).

2. **Feature Engineering**: Calculate derived indices.

3. **Model Inference**: Run CHIC tree-based ensemble.

4. **Risk Scoring**: Generate CHIP probability score.

5. **Stratification**: Categorize into risk groups.

6. **Recommendations**: Prioritize for sequencing.

7. **Output**: Risk scores, sequencing prioritization list.

## Example Usage

**User**: "Screen this population cohort using CHIC to identify individuals who should undergo CHIP sequencing."

**Agent Action**:
```bash
python3 Skills/Hematology/CHIC_ML_Framework_Agent/chic_screening.py \
    --cbc_data population_cbc.csv \
    --demographics demographics.csv \
    --model_weights chic_xgboost_ukbb.pt \
    --threshold stringent \
    --output_prioritization true \
    --output chic_screening_results/
```

## Input Data Format

```csv
sample_id,age,sex,rbc,hgb,hct,mcv,mch,mchc,rdw,wbc,plt,mpv
001,68,M,4.2,13.5,40.2,95.7,32.1,33.6,14.8,7.2,245,10.2
002,72,F,3.8,11.2,34.5,90.8,29.5,32.5,16.2,8.5,312,9.8
```

## Output Components

| Output | Description | Format |
|--------|-------------|--------|
| CHIC Score | Per-individual CH probability | .csv |
| Risk Category | Low/Medium/High | .csv |
| Sequencing Priority | Ranked list for testing | .csv |
| Feature Importance | CBC parameters driving score | .json |
| Potential CCUS | Flagged individuals | .csv |
| Population Statistics | Cohort-level summary | .json |

## Risk Stratification

| CHIC Score | Risk Category | Recommendation |
|------------|---------------|----------------|
| >0.8 | Very High | Prioritize sequencing |
| 0.5-0.8 | High | Recommend sequencing |
| 0.2-0.5 | Moderate | Consider if other risk factors |
| <0.2 | Low | Routine monitoring |

## Model Architecture

| Component | Method | Purpose |
|-----------|--------|---------|
| Base Model | XGBoost | Primary prediction |
| Secondary | Random Forest | Ensemble member |
| Tertiary | Gradient Boosting | Ensemble member |
| Ensemble | Stacking | Final prediction |
| Calibration | Isotonic regression | Probability calibration |

## AI/ML Components

**Feature Engineering**:
- Derived indices (RDW/MCV ratio, etc.)
- Age-sex adjusted values
- Longitudinal trajectory features

**Model Training**:
- UK Biobank 431,531 participants
- 20,860 sequencing-confirmed CH
- Tree-based ensemble methods

**Threshold Optimization**:
- Sensitivity-specificity tradeoffs
- NNS optimization
- Cost-effectiveness modeling

## Clinical Applications

| Application | CHIC Role | Benefit |
|-------------|-----------|---------|
| Population Screening | Prioritize sequencing | Cost reduction |
| Pre-transplant | Flag high-risk donors | Safety |
| Pre-CAR-T | Identify at-risk patients | Outcomes |
| Primary Care | Alert for referral | Early detection |
| Research | Estimate CH prevalence | Study design |

## Validation Results

| Cohort | N | AUROC | NNS Improvement |
|--------|---|-------|-----------------|
| UK Biobank (discovery) | 300,000 | 0.75 | 18x |
| UK Biobank (validation) | 131,531 | 0.74 | 17x |
| External validation | TBD | ~0.72 | ~15x |

## Prerequisites

* Python 3.10+
* XGBoost, scikit-learn
* pandas, numpy
* CHIC model weights
* CBC reference ranges

## Related Skills

* CHIP_Clonal_Hematopoiesis_Agent - Full CHIP analysis with sequencing
* MPN_Progression_Monitor_Agent - MPN monitoring
* Blood_Smear_AI_Agent - Morphology analysis
* MDS_Classification_Agent - MDS diagnosis

## CBC Red Flags for CH

| Finding | CHIC Impact | Significance |
|---------|-------------|--------------|
| RDW >15% | High score | Anisocytosis |
| MCV >100 fL | Increased | Macrocytosis |
| Unexplained anemia | Flagged | Potential CCUS |
| Cytopenias | Very high | Likely CCUS/MDS |
| Persistent changes | Escalated | Progressive CH |

## Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Moderate PPV | False positives | Confirmatory sequencing |
| Training bias | Population-specific | Multi-cohort validation |
| Acute changes | Transient abnormalities | Repeat testing |
| Other causes | Non-CH cytopenias | Clinical context |

## Special Considerations

1. **Population Calibration**: Model trained on UK Biobank demographics
2. **Acute Illness**: Exclude acutely ill patients
3. **Recent Transfusion**: Affects CBC parameters
4. **Medications**: Consider drug effects on CBC
5. **Serial Monitoring**: Longitudinal changes informative

## Cost-Effectiveness

| Scenario | Cost per CHIP Detected |
|----------|----------------------|
| Universal Sequencing | ~$73,000 |
| CHIC-Guided Sequencing | ~$4,000 |
| Improvement | 18x reduction |

## Future Directions

| Enhancement | Status | Impact |
|-------------|--------|--------|
| Multi-ethnic validation | In progress | Broader applicability |
| Longitudinal CHIC | Development | Dynamic risk |
| Integration with genetics | Research | Combined scoring |
| Point-of-care | Conceptual | Real-time screening |

## Author

AI Group - Biomedical AI Platform
