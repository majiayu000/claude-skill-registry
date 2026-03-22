---
name: explainable-ai
description: "Make AI model decisions interpretable and transparent. Use for: implementing SHAP for feature importance analysis, using LIME for local explanations, creating attention visualizations for deep learning, generating counterfactual explanations, building inherently interpretable models, visualizing decision boundaries and activation maps, explaining predictions to stakeholders, debugging model behavior, ensuring regulatory compliance with explainability requirements, and building trust in AI systems."
---

# Explainable AI (XAI)

Make AI model decisions understandable, interpretable, and transparent to humans.

## Overview

Explainable AI (XAI) encompasses techniques and processes that provide human-understandable explanations for AI model predictions and behaviors. As AI systems increasingly influence critical decisions, explainability is essential for building trust, ensuring fairness, meeting regulatory requirements, and debugging models. XAI bridges the gap between complex "black-box" models and human understanding.

## Why Explainability Matters

**Trust and Adoption**: Users trust systems they understand
**Regulatory Compliance**: GDPR, EU AI Act require explainability
**Debugging**: Identify model errors and biases
**Fairness**: Detect discriminatory patterns
**Safety**: Understand failure modes
**Scientific Discovery**: Extract insights from learned patterns

## Types of Explainability

### Global Explainability

Understanding overall model behavior across all predictions.

### Local Explainability

Understanding individual predictions for specific instances.

### Model-Agnostic vs Model-Specific

**Model-Agnostic**: Works with any model (SHAP, LIME)
**Model-Specific**: Tailored to specific architectures (attention maps, gradient-based methods)

## SHAP (SHapley Additive exPlanations)

SHAP uses game theory to assign each feature an importance value for a prediction.

### Basic SHAP Usage

```python
import shap
import numpy as np

# Tree-based models
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Visualize single prediction
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])

# Summary plot (global importance)
shap.summary_plot(shap_values, X_test)

# Dependence plot (feature interaction)
shap.dependence_plot("feature_name", shap_values, X_test)
```

### SHAP for Deep Learning

```python
# Deep learning models
import tensorflow as tf

# Use GradientExplainer for neural networks
explainer = shap.GradientExplainer(model, X_train[:100])
shap_values = explainer.shap_values(X_test[:10])

# Visualize for images
shap.image_plot(shap_values, X_test[:10])
```

### SHAP Waterfall Plot

```python
# Detailed breakdown of single prediction
shap.waterfall_plot(shap.Explanation(
    values=shap_values[0],
    base_values=explainer.expected_value,
    data=X_test.iloc[0],
    feature_names=X_test.columns.tolist()
))
```

### SHAP Interaction Values

```python
# Capture feature interactions
shap_interaction_values = explainer.shap_interaction_values(X_test)

# Visualize interactions
shap.summary_plot(shap_interaction_values, X_test)
```

## LIME (Local Interpretable Model-agnostic Explanations)

LIME explains individual predictions by approximating the model locally with an interpretable model.

### LIME for Tabular Data

```python
from lime import lime_tabular

# Create explainer
explainer = lime_tabular.LimeTabularExplainer(
    X_train.values,
    feature_names=X_train.columns.tolist(),
    class_names=['Class 0', 'Class 1'],
    mode='classification'
)

# Explain single prediction
exp = explainer.explain_instance(
    X_test.iloc[0].values,
    model.predict_proba,
    num_features=10
)

# Visualize
exp.show_in_notebook()
exp.as_pyplot_figure()

# Get feature importance
print(exp.as_list())
```

### LIME for Images

```python
from lime import lime_image
from skimage.segmentation import mark_boundaries

# Create explainer
explainer = lime_image.LimeImageExplainer()

# Explain prediction
explanation = explainer.explain_instance(
    image,
    model.predict,
    top_labels=5,
    hide_color=0,
    num_samples=1000
)

# Visualize
temp, mask = explanation.get_image_and_mask(
    explanation.top_labels[0],
    positive_only=True,
    num_features=5,
    hide_rest=False
)

plt.imshow(mark_boundaries(temp / 2 + 0.5, mask))
```

### LIME for Text

```python
from lime.lime_text import LimeTextExplainer

# Create explainer
explainer = LimeTextExplainer(class_names=['negative', 'positive'])

# Explain prediction
exp = explainer.explain_instance(
    text_instance,
    model.predict_proba,
    num_features=10
)

# Visualize
exp.show_in_notebook(text=True)
```

## Attention Mechanisms

Visualize what parts of input the model focuses on.

### Attention Weights Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_attention(attention_weights, tokens):
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        attention_weights,
        xticklabels=tokens,
        yticklabels=tokens,
        cmap='viridis',
        annot=True
    )
    plt.xlabel('Key')
    plt.ylabel('Query')
    plt.title('Attention Weights')
    plt.show()

# Extract attention from transformer
outputs = model(input_ids, output_attentions=True)
attention = outputs.attentions[-1][0].mean(dim=0).detach().numpy()
visualize_attention(attention, tokens)
```

### Multi-Head Attention Visualization

```python
def visualize_multihead_attention(attention_weights, tokens, num_heads):
    fig, axes = plt.subplots(2, num_heads // 2, figsize=(20, 8))
    axes = axes.flatten()
    
    for head in range(num_heads):
        sns.heatmap(
            attention_weights[head],
            xticklabels=tokens,
            yticklabels=tokens,
            ax=axes[head],
            cmap='viridis'
        )
        axes[head].set_title(f'Head {head + 1}')
    
    plt.tight_layout()
    plt.show()
```

## Gradient-Based Methods

### Saliency Maps

```python
import torch

def compute_saliency_map(model, image, target_class):
    image.requires_grad = True
    
    output = model(image)
    model.zero_grad()
    
    # Backward pass for target class
    output[0, target_class].backward()
    
    # Get gradients
    saliency = image.grad.data.abs()
    saliency = saliency.max(dim=1)[0]  # Max across color channels
    
    return saliency.squeeze().cpu().numpy()

# Visualize
saliency = compute_saliency_map(model, image_tensor, target_class=5)
plt.imshow(saliency, cmap='hot')
plt.colorbar()
plt.title('Saliency Map')
```

### Grad-CAM (Gradient-weighted Class Activation Mapping)

```python
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate_cam(self, input_image, target_class):
        # Forward pass
        output = self.model(input_image)
        
        # Backward pass
        self.model.zero_grad()
        output[0, target_class].backward()
        
        # Compute weights
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        
        # Weighted combination
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam)
        
        # Normalize
        cam = cam - cam.min()
        cam = cam / cam.max()
        
        return cam.squeeze().cpu().numpy()

# Usage
gradcam = GradCAM(model, model.layer4[-1])
cam = gradcam.generate_cam(image_tensor, target_class=5)

# Overlay on image
plt.imshow(image)
plt.imshow(cam, alpha=0.5, cmap='jet')
plt.title('Grad-CAM')
```

### Integrated Gradients

```python
def integrated_gradients(model, image, target_class, baseline=None, steps=50):
    if baseline is None:
        baseline = torch.zeros_like(image)
    
    # Generate interpolated images
    alphas = torch.linspace(0, 1, steps)
    interpolated_images = [baseline + alpha * (image - baseline) for alpha in alphas]
    interpolated_images = torch.stack(interpolated_images)
    
    # Compute gradients
    interpolated_images.requires_grad = True
    outputs = model(interpolated_images)
    
    gradients = []
    for i in range(steps):
        model.zero_grad()
        outputs[i, target_class].backward(retain_graph=True)
        gradients.append(interpolated_images.grad[i].detach())
    
    # Average gradients
    avg_gradients = torch.stack(gradients).mean(dim=0)
    
    # Integrated gradients
    integrated_grads = (image - baseline) * avg_gradients
    
    return integrated_grads.squeeze().cpu().numpy()
```

## Counterfactual Explanations

Generate alternative scenarios that would change the prediction.

```python
from dice_ml import Data, Model, Dice

# Setup DiCE
data = Data(dataframe=df, continuous_features=continuous_cols, outcome_name='target')
model_dice = Model(model=model, backend='sklearn')
dice_exp = Dice(data, model_dice)

# Generate counterfactuals
counterfactuals = dice_exp.generate_counterfactuals(
    query_instance=X_test.iloc[0],
    total_CFs=5,
    desired_class='opposite'
)

# Visualize
counterfactuals.visualize_as_dataframe()
```

## Inherently Interpretable Models

### Decision Trees Visualization

```python
from sklearn.tree import plot_tree, export_text

# Visualize tree
plt.figure(figsize=(20, 10))
plot_tree(
    model,
    feature_names=feature_names,
    class_names=class_names,
    filled=True,
    rounded=True
)

# Text representation
tree_rules = export_text(model, feature_names=feature_names)
print(tree_rules)
```

### Linear Model Coefficients

```python
import pandas as pd

# Feature importance from coefficients
coef_df = pd.DataFrame({
    'feature': feature_names,
    'coefficient': model.coef_[0],
    'abs_coefficient': np.abs(model.coef_[0])
}).sort_values('abs_coefficient', ascending=False)

# Visualize
plt.barh(coef_df['feature'][:10], coef_df['coefficient'][:10])
plt.xlabel('Coefficient')
plt.title('Top 10 Feature Importances')
```

### GAM (Generalized Additive Models)

```python
from interpret.glassbox import ExplainableBoostingClassifier

# Train interpretable model
ebm = ExplainableBoostingClassifier()
ebm.fit(X_train, y_train)

# Global explanation
ebm_global = ebm.explain_global()
show(ebm_global)

# Local explanation
ebm_local = ebm.explain_local(X_test[:5], y_test[:5])
show(ebm_local)
```

## Feature Importance

### Permutation Importance

```python
from sklearn.inspection import permutation_importance

# Calculate permutation importance
result = permutation_importance(
    model, X_test, y_test,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

# Visualize
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': result.importances_mean,
    'std': result.importances_std
}).sort_values('importance', ascending=False)

plt.barh(importance_df['feature'][:10], importance_df['importance'][:10])
plt.xlabel('Permutation Importance')
```

### Partial Dependence Plots

```python
from sklearn.inspection import PartialDependenceDisplay

# Create partial dependence plots
features = [0, 1, (0, 1)]  # Individual and interaction
PartialDependenceDisplay.from_estimator(
    model, X_train, features,
    feature_names=feature_names
)
plt.tight_layout()
```

## Model-Specific Explanations

### Random Forest Feature Importance

```python
# Built-in feature importance
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))


## Best Practices

**Choosing Methods**: Use SHAP for comprehensive analysis, LIME for quick local explanations, attention for sequences/images
**Communication**: Tailor to audience, provide multiple explanation types, include uncertainty
**Validation**: Verify domain sense, test stability, involve experts
**Production**: Cache explanations, provide on-demand, log for audits

## Tools

- **SHAP**: Comprehensive framework
- **LIME**: Local explanations
- **InterpretML**: Microsoft toolkit
- **Captum**: PyTorch interpretability
- **Alibi**: Model inspection

## Learning Path

1. **Basics**: Feature importance, visualizations
2. **Intermediate**: SHAP, LIME, attention
3. **Advanced**: Counterfactuals, custom methods
4. **Expert**: Quality metrics, production deployment

See `references/` for method comparisons, case studies, and implementation guides.
