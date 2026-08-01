---
name: experiment-tracking
description: 'Integrate Trackio for experiment tracking in Kaggle competitions. Use
  PROACTIVELY when user trains models, logs metrics, or manages experiments. Keywords:
  実験, 訓練, train, training, tracking, metrics, 指'
---

---
name: experiment-tracking
description: Integrate Trackio for experiment tracking in Kaggle competitions. Use PROACTIVELY when user trains models, logs metrics, or manages experiments. Keywords: 実験, 訓練, train, training, tracking, metrics, 指標, ログ
---

## When to Use (PROACTIVE)

This skill should be activated automatically when:

- User starts model training
- User mentions keywords: "実験", "訓練", "train", "training", "tracking"
- User needs to track hyperparameters or metrics
- New training script creation
- User asks about experiment management

## What This Skill Does

Ensures all training runs are properly tracked with **Trackio**:

- Local-first experiment tracking (no cloud required)
- W&B-compatible API
- Automatic metric logging
- Gradio dashboard for visualization

## How to Use

Refer to `trackio-guide.md` for detailed implementation patterns including:

- trackio.init() configuration
- Metric logging in training loops
- Dashboard usage
- Cross-validation tracking
- Complete training script examples
