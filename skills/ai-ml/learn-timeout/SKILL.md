---
name: learn-timeout
triggers:
  - learn-timeout
  - timeout prediction
  - estimate timeout
  - predict timeout
  - timeout model
description: General-purpose timeout estimation skill. Trains dual models (duration regression + risk classification) from corpus data and observation feedback. Returns calibrated timeout predictions with confidence intervals for any task type.

provides:
  - learn-timeout
composes:
  - task-monitor
---

# Learn Timeout

General-purpose timeout estimation that replaces fragmented Ridge/Logistic models with a unified GradientBoosting-based predictor.

## Commands

```bash
./run.sh collect                    # Gather training data from all sources
./run.sh train                      # Train both models
./run.sh predict '{"task_type":"pdf_extraction","page_count":400}'
./run.sh observe --task-id X --actual-seconds Y
./run.sh status                     # Model health dashboard
./run.sh benchmark                  # Classifier-lab backbone comparison
```

## Prediction Output

```json
{
  "estimated_seconds": 4200,
  "confidence_interval": [2800, 6300],
  "risk_probability": 0.35,
  "risk_label": "medium",
  "recommended_timeout_seconds": 6300,
  "features_used": ["page_count", "table_pages", "domain"],
  "model_version": "2026-02-13_v1",
  "duration_model_available": true,
  "risk_model_available": true
}
```

## Task Types

| task_type | Key Features |
|-----------|-------------|
| `pdf_extraction` | page_count, tables, figures, file_size, domain |
| `llm_api_call` | prompt_tokens, model, provider, image_count |
| `subprocess` | command_type, input_size, complexity_hints |
| `remediation` | issue_count, issue_severity, skill_name |

## Training Data Sources

- Corpus `profile.json` + `timings.jsonl` (S00 features + actual durations)
- Supervisor run logs (`extract_timeout` events)
- Aggregate reports (extraction timing events)
- Observation feedback loop (`data/observations.jsonl`)
