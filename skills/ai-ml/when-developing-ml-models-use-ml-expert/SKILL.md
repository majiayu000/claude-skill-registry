---
name: when-developing-ml-models-use-ml-expert
version: 1.0.0
description: Specialized ML model development, training, and deployment workflow
category: machine-learning
tags: [ml, training, deployment, model-development, neural-networks]
agents: [ml-developer, researcher, tester]
difficulty: advanced
estimated_duration: 45-90min
success_criteria:
  - Model trained successfully
  - Validation metrics meet targets
  - Production deployment ready
  - Documentation complete
validation_method: performance_metrics
dependencies:
  - claude-flow@alpha
  - tensorflow/pytorch
  - flow-nexus (optional for distributed training)
outputs:
  - Trained model file
  - Training metrics
  - Evaluation report
  - Deployment package
triggers:
  - New ML model needed
  - Model training required
  - Production deployment
---

# ML Expert - Machine Learning Model Development

## Overview

Specialized workflow for ML model development, training, and deployment. Supports various architectures (CNNs, RNNs, Transformers) with distributed training capabilities.

## When to Use

- Developing new ML models
- Training neural networks
- Model optimization
- Production deployment
- Transfer learning
- Fine-tuning existing models

## Phase 1: Data Preparation (10 min)

### Objective
Clean, preprocess, and prepare training data

### Agent: ML-Developer

**Step 1.1: Load and Analyze Data**
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('dataset.csv')

# Analyze
analysis = {
    'shape': data.shape,
    'columns': data.columns.tolist(),
    'dtypes': data.dtypes.to_dict(),
    'missing': data.isnull().sum().to_dict(),
    'stats': data.describe().to_dict()
}

# Store analysis
await memory.store('ml-expert/data-analysis', analysis)
```

**Step 1.2: Data Cleaning**
```python
# Handle missing values
data = data.fillna(data.mean())

# Remove duplicates
data = data.drop_duplicates()

# Handle outliers
from scipy import stats
z_scores = np.abs(stats.zscore(data.select_dtypes(include=[np.number])))
data = data[(z_scores < 3).all(axis=1)]

# Encode categorical variables
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for col in data.select_dtypes(include=['object']).columns:
    data[col] = le.fit_transform(data[col])
```

**Step 1.3: Split Data**
```python
# Split into train/val/test
X = data.drop('target', axis=1)
y = data['target']

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Normalize
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# Save preprocessed data
np.save('data/X_train.npy', X_train)
np.save('data/X_val.npy', X_val)
np.save('data/X_test.npy', X_test)
```

### Validation Criteria
- [ ] Data loaded successfully
- [ ] Missing values handled
- [ ] Train/val/test split created
- [ ] Normalization applied

## Phase 2: Model Selection (10 min)

### Objective
Choose and configure model architecture

### Agent: Researcher

**Step 2.1: Analyze Task Type**
```python
task_analysis = {
    'type': 'classification|regression|clustering',
    'complexity': 'low|medium|high',
    'dataSize': len(data),
    'features': X.shape[1],
    'classes': len(np.unique(y)) if classification else None
}

# Recommend architecture
if task_analysis['type'] == 'classification' and task_analysis['features'] > 100:
    recommended_architecture = 'deep_neural_network'
elif task_analysis['type'] == 'regression' and task_analysis['dataSize'] < 10000:
    recommended_architecture = 'random_forest'
# ... more logic
```

**Step 2.2: Define Architecture**
```python
import tensorflow as tf

def create_model(architecture='dnn', input_shape, num_classes):
    if architecture == 'dnn':
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation='relu', input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    elif architecture == 'cnn':
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
            tf.keras.layers.MaxPooling2D((2,2)),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2,2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    # ... more architectures

    return model

model = create_model('dnn', input_shape=(X_train.shape[1],), num_classes=len(np.unique(y)))
model.summary()
```

**Step 2.3: Configure Training**
```python
training_config = {
    'optimizer': tf.keras.optimizers.Adam(learning_rate=0.001),
    'loss': 'sparse_categorical_crossentropy',
    'metrics': ['accuracy'],
    'batch_size': 32,
    'epochs': 100,
    'callbacks': [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5),
        tf.keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True)
    ]
}

model.compile(
    optimizer=training_config['optimizer'],
    loss=training_config['loss'],
    metrics=training_config['metrics']
)
```

### Validation Criteria
- [ ] Task analyzed
- [ ] Architecture selected
- [ ] Model configured
- [ ] Training parameters set

## Phase 3: Train Model (20 min)

### Objective
Execute training with monitoring

### Agent: ML-Developer

**Step 3.1: Start Training**
```python
# Train model
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    batch_size=training_config['batch_size'],
    epochs=training_config['epochs'],
    callbacks=training_config['callbacks'],
    verbose=1
)

# Save training history
import json
with open('training_history.json', 'w') as f:
    json.dump({
        'loss': history.history['loss'],
        'val_loss': history.history['val_loss'],
        'accuracy': history.history['accuracy'],
        'val_accuracy': history.history['val_accuracy']
    }, f)
```

**Step 3.2: Monitor Training**
```python
import matplotlib.pyplot as plt

# Plot training curves
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Loss
ax1.plot(history.history['loss'], label='Train Loss')
ax1.plot(history.history['val_loss'], label='Val Loss')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.legend()
ax1.grid(True)

# Accuracy
ax2.plot(history.history['accuracy'], label='Train Accuracy')
ax2.plot(history.history['val_accuracy'], label='Val Accuracy')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.legend()
ax2.grid(True)

plt.savefig('training_curves.png')
```

**Step 3.3: Distributed Training (Optional)**
```python
# Using Flow-Nexus for distributed training
from flow_nexus import DistributedTrainer

trainer = DistributedTrainer({
    'cluster_id': 'ml-training-cluster',
    'num_nodes': 4,
    'strategy': 'data_parallel'
})

# Train across multiple nodes
trainer.fit(
    model=model,
    train_data=(X_train, y_train),
    val_data=(X_val, y_val),
    config=training_config
)
```

### Validation Criteria
- [ ] Training completed
- [ ] No NaN losses
- [ ] Validation metrics improving
- [ ] Model checkpoints saved

## Phase 4: Validate Performance (10 min)

### Objective
Evaluate model on test set

### Agent: Tester

**Step 4.1: Evaluate on Test Set**
```python
# Load best model
best_model = tf.keras.models.load_model('best_model.h5')

# Evaluate
test_loss, test_accuracy = best_model.evaluate(X_test, y_test, verbose=0)

# Predictions
y_pred = best_model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Detailed metrics
from sklearn.metrics import classification_report, confusion_matrix

metrics = {
    'test_loss': float(test_loss),
    'test_accuracy': float(test_accuracy),
    'classification_report': classification_report(y_test, y_pred_classes, output_dict=True),
    'confusion_matrix': confusion_matrix(y_test, y_pred_classes).tolist()
}

await memory.store('ml-expert/metrics', metrics)
```

**Step 4.2: Generate Evaluation Report**
```python
report = f"""
# Model Evaluation Report

## Performance Metrics
- Test Loss: {test_loss:.4f}
- Test Accuracy: {test_accuracy:.4f}

## Classification Report
{classification_report(y_test, y_pred_classes)}

## Model Summary
- Architecture: {recommended_architecture}
- Parameters: {model.count_params()}
- Training Time: {training_time} seconds

## Training History
- Best Val Loss: {min(history.history['val_loss']):.4f}
- Best Val Accuracy: {max(history.history['val_accuracy']):.4f}
- Epochs Trained: {len(history.history['loss'])}
"""

with open('evaluation_report.md', 'w') as f:
    f.write(report)
```

### Validation Criteria
- [ ] Test accuracy > target threshold
- [ ] No overfitting detected
- [ ] Metrics documented
- [ ] Report generated

## Phase 5: Deploy to Production (15 min)

### Objective
Package model for deployment

### Agent: ML-Developer

**Step 5.1: Export Model**
```python
# Save in multiple formats
model.save('model.h5')  # Keras format
model.save('model_savedmodel')  # TensorFlow SavedModel
# Convert to TFLite for mobile
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

# Save preprocessing pipeline
import joblib
joblib.dump(scaler, 'scaler.pkl')
```

**Step 5.2: Create Deployment Package**
```python
import shutil
import os

# Create deployment directory
os.makedirs('deployment', exist_ok=True)

# Copy necessary files
shutil.copy('model.h5', 'deployment/')
shutil.copy('scaler.pkl', 'deployment/')
shutil.copy('evaluation_report.md', 'deployment/')

# Create inference script
inference_script = '''
import tensorflow as tf
import joblib
import numpy as np

class ModelInference:
    def __init__(self, model_path, scaler_path):
        self.model = tf.keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, input_data):
        # Preprocess
        scaled = self.scaler.transform(input_data)
        # Predict
        predictions = self.model.predict(scaled)
        return np.argmax(predictions, axis=1)

# Usage
inference = ModelInference('model.h5', 'scaler.pkl')
result = inference.predict(new_data)
'''

with open('deployment/inference.py', 'w') as f:
    f.write(inference_script)
```

**Step 5.3: Generate Documentation**
```markdown
# Model Deployment Guide

## Files
- `model.h5`: Trained Keras model
- `scaler.pkl`: Preprocessing scaler
- `inference.py`: Inference script

## Usage
\`\`\`python
from inference import ModelInference

model = ModelInference('model.h5', 'scaler.pkl')
predictions = model.predict(new_data)
\`\`\`

## Performance
- Latency: < 50ms per prediction
- Accuracy: ${test_accuracy}
- Model Size: ${model_size}MB

## Requirements
- tensorflow>=2.0
- scikit-learn
- numpy
```

### Validation Criteria
- [ ] Model exported successfully
- [ ] Deployment package created
- [ ] Inference script tested
- [ ] Documentation complete

## Success Metrics

- Test accuracy meets target
- Training converged
- No overfitting
- Production-ready deployment

## Skill Completion

Outputs:
1. **model.h5**: Trained model file
2. **evaluation_report.md**: Performance metrics
3. **deployment/**: Production package
4. **training_history.json**: Training logs

Complete when model deployed and validated.
