---
name: ml-model-training
description: Train ML models with scikit-learn, PyTorch, TensorFlow. Use for classification/regression, neural networks, hyperparameter tuning, or encountering overfitting, underfitting, convergence issues.
keywords: machine learning, model training, PyTorch, TensorFlow, scikit-learn, neural networks, deep learning, classification, regression, hyperparameter tuning, cross-validation, model evaluation, data preprocessing, feature engineering
license: MIT
---

# ML Model Training

Train machine learning models with proper data handling and evaluation.

## Training Workflow

1. Data Preparation → 2. Feature Engineering → 3. Model Selection → 4. Training → 5. Evaluation

## Data Preparation

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load and clean data
df = pd.read_csv('data.csv')
df = df.dropna()

# Encode categorical variables
le = LabelEncoder()
df['category'] = le.fit_transform(df['category'])

# Split data (70/15/15)
X = df.drop('target', axis=1)
y = df['target']
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)
```

## Scikit-learn Training

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_val)
print(classification_report(y_val, y_pred))
```

## PyTorch Training

```python
import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

model = Model(X_train.shape[1])
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.BCELoss()

for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    output = model(X_train_tensor)
    loss = criterion(output, y_train_tensor)
    loss.backward()
    optimizer.step()
```

## Evaluation Metrics

| Task | Metrics |
|------|---------|
| Classification | Accuracy, Precision, Recall, F1, AUC-ROC |
| Regression | MSE, RMSE, MAE, R² |

## Complete Framework Examples

- **PyTorch**: See [references/pytorch-training.md](references/pytorch-training.md) for complete training with:
  - Custom model classes with BatchNorm and Dropout
  - Training/validation loops with early stopping
  - Learning rate scheduling
  - Model checkpointing
  - Full evaluation with classification report

- **TensorFlow/Keras**: See [references/tensorflow-keras.md](references/tensorflow-keras.md) for:
  - Sequential model architecture
  - Callbacks (EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard)
  - Training history visualization
  - TFLite conversion for mobile deployment
  - Custom training loops

## Best Practices

**Do:**
- Use cross-validation for robust evaluation
- Track experiments with MLflow
- Save model checkpoints regularly
- Monitor for overfitting
- Document hyperparameters
- Use 70/15/15 train/val/test split

**Don't:**
- Train without a validation set
- Ignore class imbalance
- Skip feature scaling
- Use test set for hyperparameter tuning
- Forget to set random seeds

## Known Issues Prevention

### 1. Data Leakage
**Problem**: Scaling or transforming data before splitting leads to test set information leaking into training.

**Solution**: Always split data first, then fit transformers only on training data:
```python
# ✅ Correct: Fit on train, transform train/val/test
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)  # Only transform
X_test = scaler.transform(X_test)  # Only transform

# ❌ Wrong: Fitting on all data
X_all = scaler.fit_transform(X)  # Leaks test info!
```

### 2. Class Imbalance Ignored
**Problem**: Training on imbalanced datasets (e.g., 95% class A, 5% class B) leads to models that predict only the majority class.

**Solution**: Use class weights or resampling:
```python
from sklearn.utils.class_weight import compute_class_weight

# Compute class weights
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
model = RandomForestClassifier(class_weight='balanced')

# Or use SMOTE for oversampling minority class
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

### 3. Overfitting Due to No Regularization
**Problem**: Complex models memorize training data, perform poorly on validation/test sets.

**Solution**: Add regularization techniques:
```python
# Dropout in PyTorch
nn.Dropout(0.3)

# L2 regularization in scikit-learn
RandomForestClassifier(max_depth=10, min_samples_split=20)

# Early stopping in Keras
from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model.fit(X_train, y_train, validation_data=(X_val, y_val), callbacks=[early_stop])
```

### 4. Not Setting Random Seeds
**Problem**: Results are not reproducible across runs, making debugging and comparison impossible.

**Solution**: Set all random seeds:
```python
import random
import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)
```

### 5. Using Test Set for Hyperparameter Tuning
**Problem**: Optimizing hyperparameters on test set leads to overfitting to test data.

**Solution**: Use validation set for tuning, test set only for final evaluation:
```python
from sklearn.model_selection import GridSearchCV

# ✅ Correct: Tune on train+val, evaluate on test
param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, 15]}
grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid_search.fit(X_train, y_train)  # Cross-validation on training set
best_model = grid_search.best_estimator_

# Final evaluation on held-out test set
final_score = best_model.score(X_test, y_test)
```

## When to Load References

Load reference files when you need:
- **PyTorch implementation details**: Load `references/pytorch-training.md` for complete training loops with early stopping, learning rate scheduling, and checkpointing
- **TensorFlow/Keras patterns**: Load `references/tensorflow-keras.md` for callback usage, custom training loops, and mobile deployment with TFLite
