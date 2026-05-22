---
name: when-debugging-ml-training-use-ml-training-debugger
version: 1.0.0
description: Debug ML training issues and optimize performance including loss divergence, overfitting, and slow convergence
category: machine-learning
tags: [debugging, ml, training, optimization, troubleshooting]
agents: [ml-developer, performance-analyzer, coder]
difficulty: advanced
estimated_duration: 30-60min
success_criteria:
  - Issue diagnosed correctly
  - Root cause identified
  - Fix applied successfully
  - Training convergence restored
validation_method: training_validation
dependencies:
  - claude-flow@alpha
  - tensorflow/pytorch
  - tensorboard (for visualization)
outputs:
  - Diagnostic report
  - Fixed model/training code
  - Performance comparison
  - Optimization recommendations
triggers:
  - Training loss diverging/NaN
  - Overfitting detected
  - Slow convergence
  - Poor validation performance
---

# ML Training Debugger - Diagnose and Fix Training Issues

## Overview

Systematic debugging workflow for ML training issues including loss divergence, overfitting, slow convergence, gradient problems, and performance optimization.

## When to Use

- Training loss becomes NaN or infinite
- Severe overfitting (train >> val performance)
- Training not converging
- Gradient vanishing/exploding
- Poor validation accuracy
- Training too slow

## Phase 1: Diagnose Issue (8 min)

### Objective
Identify the specific training problem

### Agent: ML-Developer

**Step 1.1: Analyze Training Curves**
```python
import json
import numpy as np

# Load training history
with open('training_history.json', 'r') as f:
    history = json.load(f)

# Diagnose issues
diagnosis = {
    'loss_divergence': check_loss_divergence(history['loss']),
    'overfitting': check_overfitting(history['loss'], history['val_loss']),
    'slow_convergence': check_convergence_rate(history['loss']),
    'gradient_issues': check_gradient_health(history),
    'nan_values': any(np.isnan(history['loss']))
}

def check_loss_divergence(losses):
    # Loss increasing over time
    if len(losses) > 10:
        recent_trend = np.mean(losses[-5:]) > np.mean(losses[-10:-5])
        return recent_trend

def check_overfitting(train_loss, val_loss):
    # Val loss diverging from train loss
    if len(train_loss) > 10:
        gap = np.mean(val_loss[-5:]) - np.mean(train_loss[-5:])
        return gap > 0.5  # Significant gap

def check_convergence_rate(losses):
    # Loss barely changing
    if len(losses) > 20:
        recent_change = abs(losses[-1] - losses[-10])
        return recent_change < 0.01  # Plateau

await memory.store('ml-debugger/diagnosis', diagnosis)
```

**Step 1.2: Identify Root Cause**
```python
root_causes = []

if diagnosis['loss_divergence']:
    root_causes.append({
        'issue': 'Loss Divergence',
        'likely_cause': 'Learning rate too high',
        'severity': 'HIGH',
        'fix': 'Reduce learning rate by 10x'
    })

if diagnosis['nan_values']:
    root_causes.append({
        'issue': 'NaN Loss',
        'likely_cause': 'Numerical instability',
        'severity': 'CRITICAL',
        'fix': 'Add gradient clipping, reduce LR, check data for extreme values'
    })

if diagnosis['overfitting']:
    root_causes.append({
        'issue': 'Overfitting',
        'likely_cause': 'Model too complex or insufficient regularization',
        'severity': 'MEDIUM',
        'fix': 'Add dropout, L2 regularization, or more training data'
    })

if diagnosis['slow_convergence']:
    root_causes.append({
        'issue': 'Slow Convergence',
        'likely_cause': 'Learning rate too low or poor initialization',
        'severity': 'LOW',
        'fix': 'Increase learning rate, use better initialization'
    })

await memory.store('ml-debugger/root-causes', root_causes)
```

**Step 1.3: Generate Diagnostic Report**
```python
report = f"""
# ML Training Diagnostic Report

## Issues Detected
{chr(10).join([f"- **{rc['issue']}** (Severity: {rc['severity']})" for rc in root_causes])}

## Root Cause Analysis
{chr(10).join([f"""
### {rc['issue']}
- **Likely Cause**: {rc['likely_cause']}
- **Recommended Fix**: {rc['fix']}
""" for rc in root_causes])}

## Training History Summary
- Final Train Loss: {history['loss'][-1]:.4f}
- Final Val Loss: {history['val_loss'][-1]:.4f}
- Epochs Completed: {len(history['loss'])}
"""

with open('diagnostic_report.md', 'w') as f:
    f.write(report)
```

### Validation Criteria
- [ ] Issues identified
- [ ] Root causes determined
- [ ] Severity assessed
- [ ] Report generated

## Phase 2: Analyze Root Cause (10 min)

### Objective
Deep dive into the specific problem

### Agent: Performance-Analyzer

**Step 2.1: Gradient Analysis**
```python
import tensorflow as tf

# Monitor gradients during training
def gradient_analysis(model, X_batch, y_batch):
    with tf.GradientTape() as tape:
        predictions = model(X_batch, training=True)
        loss = loss_fn(y_batch, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)

    analysis = {
        'gradient_norms': [tf.norm(g).numpy() for g in gradients if g is not None],
        'has_nan': any(tf.reduce_any(tf.math.is_nan(g)) for g in gradients if g is not None),
        'has_inf': any(tf.reduce_any(tf.math.is_inf(g)) for g in gradients if g is not None)
    }

    # Check for vanishing/exploding gradients
    gradient_norms = np.array(analysis['gradient_norms'])
    analysis['vanishing'] = np.mean(gradient_norms) < 1e-7
    analysis['exploding'] = np.mean(gradient_norms) > 100

    return analysis

grad_analysis = gradient_analysis(model, X_train[:32], y_train[:32])
await memory.store('ml-debugger/gradient-analysis', grad_analysis)
```

**Step 2.2: Data Analysis**
```python
# Check for data issues
data_issues = {
    'class_imbalance': check_class_balance(y_train),
    'outliers': detect_outliers(X_train),
    'missing_normalization': check_normalization(X_train),
    'label_noise': estimate_label_noise(X_train, y_train, model)
}

def check_class_balance(labels):
    unique, counts = np.unique(labels, return_counts=True)
    imbalance_ratio = max(counts) / min(counts)
    return imbalance_ratio > 10  # Significant imbalance

def check_normalization(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    # Data should be roughly normalized
    return np.mean(np.abs(mean)) > 1 or np.mean(std) > 10

await memory.store('ml-debugger/data-issues', data_issues)
```

**Step 2.3: Model Architecture Review**
```python
# Analyze model complexity
architecture_analysis = {
    'total_params': model.count_params(),
    'trainable_params': sum([tf.size(v).numpy() for v in model.trainable_variables]),
    'depth': len(model.layers),
    'has_batch_norm': any('batch_norm' in layer.name for layer in model.layers),
    'has_dropout': any('dropout' in layer.name for layer in model.layers),
    'activation_functions': [layer.activation.__name__ for layer in model.layers if hasattr(layer, 'activation')]
}

# Check for common issues
architecture_issues = []

if architecture_analysis['total_params'] / len(X_train) > 10:
    architecture_issues.append('Model too complex relative to data size')

if not architecture_analysis['has_batch_norm'] and architecture_analysis['depth'] > 10:
    architecture_issues.append('Deep model without batch normalization')

await memory.store('ml-debugger/architecture-issues', architecture_issues)
```

### Validation Criteria
- [ ] Gradients analyzed
- [ ] Data issues identified
- [ ] Architecture reviewed
- [ ] Problems documented

## Phase 3: Apply Fix (15 min)

### Objective
Implement corrections based on diagnosis

### Agent: Coder

**Step 3.1: Fix Learning Rate**
```python
if 'Loss Divergence' in [rc['issue'] for rc in root_causes]:
    # Reduce learning rate
    old_lr = model.optimizer.learning_rate.numpy()
    new_lr = old_lr / 10
    model.optimizer.learning_rate.assign(new_lr)
    print(f"✅ Reduced learning rate: {old_lr} → {new_lr}")

if 'Slow Convergence' in [rc['issue'] for rc in root_causes]:
    # Increase learning rate with warmup
    new_lr = old_lr * 5
    model.optimizer.learning_rate.assign(new_lr)

    # Add LR scheduler
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7
    )
```

**Step 3.2: Fix Overfitting**
```python
if 'Overfitting' in [rc['issue'] for rc in root_causes]:
    # Add regularization
    from tensorflow.keras import regularizers

    # Clone model with regularization
    new_layers = []
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Dense):
            new_layer = tf.keras.layers.Dense(
                layer.units,
                activation=layer.activation,
                kernel_regularizer=regularizers.l2(0.01),  # Add L2
                name=layer.name + '_reg'
            )
            new_layers.append(new_layer)

            # Add dropout after dense layers
            new_layers.append(tf.keras.layers.Dropout(0.3))
        else:
            new_layers.append(layer)

    # Rebuild model
    fixed_model = tf.keras.Sequential(new_layers)
    fixed_model.compile(
        optimizer=model.optimizer,
        loss=model.loss,
        metrics=model.metrics
    )

    print("✅ Added L2 regularization and dropout")
```

**Step 3.3: Fix Gradient Issues**
```python
if grad_analysis['exploding']:
    # Add gradient clipping
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=0.001,
        clipnorm=1.0  # Clip by global norm
    )
    model.compile(
        optimizer=optimizer,
        loss=model.loss,
        metrics=model.metrics
    )
    print("✅ Added gradient clipping")

if grad_analysis['vanishing']:
    # Use better activation functions
    # Replace sigmoid/tanh with ReLU/LeakyReLU
    for layer in model.layers:
        if hasattr(layer, 'activation'):
            if layer.activation.__name__ in ['sigmoid', 'tanh']:
                layer.activation = tf.keras.activations.relu
                print(f"✅ Changed {layer.name} activation to ReLU")
```

**Step 3.4: Fix Data Issues**
```python
if data_issues['class_imbalance']:
    # Compute class weights
    from sklearn.utils.class_weight import compute_class_weight

    class_weights = compute_class_weight(
        'balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = dict(enumerate(class_weights))
    print(f"✅ Applying class weights: {class_weight_dict}")

if data_issues['missing_normalization']:
    # Re-normalize data
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train_fixed = scaler.fit_transform(X_train)
    X_val_fixed = scaler.transform(X_val)
    print("✅ Data re-normalized")
```

### Validation Criteria
- [ ] Fixes applied
- [ ] Model recompiled
- [ ] Data corrected
- [ ] Ready for retraining

## Phase 4: Validate Fix (12 min)

### Objective
Verify that fixes resolve the issues

### Agent: Performance-Analyzer

**Step 4.1: Retrain Model**
```python
# Retrain with fixes
print("Retraining model with fixes...")

history_fixed = model.fit(
    X_train_fixed, y_train,
    validation_data=(X_val_fixed, y_val),
    batch_size=32,
    epochs=50,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=10),
        lr_scheduler if 'Slow Convergence' in [rc['issue'] for rc in root_causes] else None
    ],
    class_weight=class_weight_dict if data_issues['class_imbalance'] else None,
    verbose=1
)

# Save fixed training history
with open('training_history_fixed.json', 'w') as f:
    json.dump({
        'loss': history_fixed.history['loss'],
        'val_loss': history_fixed.history['val_loss'],
        'accuracy': history_fixed.history['accuracy'],
        'val_accuracy': history_fixed.history['val_accuracy']
    }, f)
```

**Step 4.2: Compare Before/After**
```python
comparison = {
    'before': {
        'final_train_loss': history['loss'][-1],
        'final_val_loss': history['val_loss'][-1],
        'final_val_acc': history['val_accuracy'][-1],
        'converged': len(history['loss']) < 100
    },
    'after': {
        'final_train_loss': history_fixed.history['loss'][-1],
        'final_val_loss': history_fixed.history['val_loss'][-1],
        'final_val_acc': history_fixed.history['val_accuracy'][-1],
        'converged': history_fixed.history['val_loss'][-1] < history_fixed.history['val_loss'][-10]
    },
    'improvement': {
        'val_loss_reduction': (history['val_loss'][-1] - history_fixed.history['val_loss'][-1]) / history['val_loss'][-1] * 100,
        'val_acc_improvement': (history_fixed.history['val_accuracy'][-1] - history['val_accuracy'][-1]) * 100
    }
}

await memory.store('ml-debugger/comparison', comparison)
```

**Step 4.3: Visualize Comparison**
```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Loss comparison
axes[0,0].plot(history['loss'], label='Before (Train)', alpha=0.7)
axes[0,0].plot(history['val_loss'], label='Before (Val)', alpha=0.7)
axes[0,0].plot(history_fixed.history['loss'], label='After (Train)', linestyle='--')
axes[0,0].plot(history_fixed.history['val_loss'], label='After (Val)', linestyle='--')
axes[0,0].set_title('Loss Comparison')
axes[0,0].legend()
axes[0,0].grid(True)

# Accuracy comparison
axes[0,1].plot(history['accuracy'], label='Before (Train)', alpha=0.7)
axes[0,1].plot(history['val_accuracy'], label='Before (Val)', alpha=0.7)
axes[0,1].plot(history_fixed.history['accuracy'], label='After (Train)', linestyle='--')
axes[0,1].plot(history_fixed.history['val_accuracy'], label='After (Val)', linestyle='--')
axes[0,1].set_title('Accuracy Comparison')
axes[0,1].legend()
axes[0,1].grid(True)

plt.savefig('training_comparison.png')
```

### Validation Criteria
- [ ] Retraining successful
- [ ] Issues resolved
- [ ] Improvement documented
- [ ] Comparison visualized

## Phase 5: Optimize Performance (5 min)

### Objective
Apply additional optimizations

### Agent: ML-Developer

**Step 5.1: Generate Recommendations**
```python
recommendations = []

if comparison['after']['final_val_acc'] < 0.85:
    recommendations.append({
        'type': 'Architecture',
        'suggestion': 'Try deeper model or different architecture (CNN, Transformer)',
        'expected_improvement': '+5-10% accuracy'
    })

if comparison['after']['final_val_loss'] > 0.5:
    recommendations.append({
        'type': 'Data',
        'suggestion': 'Collect more training data or apply data augmentation',
        'expected_improvement': 'Better generalization'
    })

if history_fixed.history['loss'][-1] > 0.1:
    recommendations.append({
        'type': 'Training',
        'suggestion': 'Train longer with learning rate scheduling',
        'expected_improvement': 'Lower training loss'
    })

await memory.store('ml-debugger/recommendations', recommendations)
```

**Step 5.2: Generate Final Report**
```markdown
# ML Training Debug Report

## Original Issues
${root_causes.map(rc => `- ${rc.issue}: ${rc.likely_cause}`).join('\n')}

## Fixes Applied
${fixes_applied.map(fix => `- ${fix}`).join('\n')}

## Results
### Before
- Val Loss: ${comparison.before.final_val_loss.toFixed(4)}
- Val Accuracy: ${(comparison.before.final_val_acc * 100).toFixed(2)}%

### After
- Val Loss: ${comparison.after.final_val_loss.toFixed(4)}
- Val Accuracy: ${(comparison.after.final_val_acc * 100).toFixed(2)}%

### Improvement
- Val Loss Reduction: ${comparison.improvement.val_loss_reduction.toFixed(2)}%
- Val Accuracy Gain: +${comparison.improvement.val_acc_improvement.toFixed(2)}%

## Recommendations for Further Improvement
${recommendations.map((r, i) => `${i+1}. **${r.type}**: ${r.suggestion} (${r.expected_improvement})`).join('\n')}
```

### Validation Criteria
- [ ] Recommendations generated
- [ ] Final report complete
- [ ] Model saved
- [ ] Ready for production

## Success Metrics

- Training converges successfully
- Validation loss improved by >10%
- No NaN or infinite values
- Overfitting reduced

## Skill Completion

Outputs:
1. **diagnostic_report.md**: Issue analysis
2. **fixed_model.h5**: Corrected model
3. **training_comparison.png**: Before/after visualization
4. **optimization_recommendations.md**: Next steps

Complete when training issues resolved and model performing well.
