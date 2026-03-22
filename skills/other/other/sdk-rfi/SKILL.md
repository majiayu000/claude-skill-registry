---
name: rfi
description: Crowdsourced forecasting questions and predictions from the RAND Forecasting
  Initiative (formerly INFER). Policy-relevant forecasting questions with crowd probabilities,
  individual forecaster predictions with rationales, and comments. Use for any question
  about geopolitics, national security, science and technology policy, or when you
  need calibrated crowd forecasts as base rates. All methods support cutoff_date for
  backtesting.
---

# RAND Forecasting Initiative (RFI)

SDK that provides access to the RAND Forecasting Initiative crowdsourced forecasting platform (formerly INFER, powered by Cultivate Labs). It covers policy-relevant forecasting questions with aggregated crowd probabilities and individual forecaster predictions with rationales.

## Quick Start

```python
from sdk_rfi import Client

client = Client()  # Uses RFI_EMAIL and RFI_PASSWORD env vars
```

## Key Methods

| Method | What it does |
|--------|-------------|
| `client.questions.list(...)` | List forecasting questions with filtering by status, tags, challenges, date ranges |
| `client.questions.get(question_id)` | Get a specific question with answers and crowd probabilities |
| `client.prediction_sets.list(question_id=...)` | Get individual forecaster predictions with rationales for a question |
| `client.comments.list(commentable_id=..., commentable_type=...)` | Get discussion comments on a question |

## Data Coverage

- **Domain**: Politics / policy forecasting
- **Countries/Regions**: Global (US policy focus)
- **Time range**: Questions from ~2020 to present
- **Update frequency**: Event-driven (new questions published, forecasts updated continuously)
- **Key data**: Forecasting questions on geopolitics, national security, science/technology policy, economics, biosecurity, nuclear risk, AI governance

## Forecasting Patterns

- **Crowd forecast as base rate**: Use `client.questions.list()` to find questions matching your topic, then read the crowd probability from `question.answers[i].probability` as a calibrated starting point.
- **Trend analysis via prediction history**: Use `client.prediction_sets.list(question_id=X)` to see how individual forecasts changed over time. Plot `created_at` vs `forecasted_probability` to detect momentum.
- **Expert rationale mining**: Individual prediction sets include `rationale` text explaining the forecaster's reasoning. Use `client.prediction_sets.list(question_id=X)` and examine rationales for weak signals and arguments.
- **Cross-reference with resolution**: Use `client.questions.list(status="closed")` to find resolved questions. Compare crowd probability at various cutoff dates against actual outcomes to measure calibration.
- **Comment-based signal detection**: Use `client.comments.list(commentable_id=X, commentable_type="Forecast::Question")` to find discussion threads that may contain links to evidence or emerging developments.

## Common Queries

```python
# Get all active forecasting questions
questions = client.questions.list()
for q in questions.questions:
    print(f"{q.id}: {q.name}")
    for a in (q.answers or []):
        print(f"  {a.name}: {a.probability_formatted}")

# Get individual forecasts and rationales for a question
forecasts = client.prediction_sets.list(question_id=1234)
for ps in forecasts.prediction_sets:
    print(f"{ps.membership_username}: {ps.rationale}")
    for pred in (ps.predictions or []):
        print(f"  Answer {pred.answer_id}: {pred.forecasted_probability:.1%}")

# Backtest: get data as it was available on a past date
past_questions = client.questions.list(cutoff_date="2025-06-01")
past_forecasts = client.prediction_sets.list(question_id=1234, cutoff_date="2025-06-01")
```

## Full Method Reference

See `references/methods.md` for all 4 methods with complete parameter details.
