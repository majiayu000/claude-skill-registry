---
name: model-interpretability
description: Interpret ML model predictions using SHAP, LIME, attention visualization, and probing techniques. Use when explaining model decisions, debugging model behavior, or building trust in ML systems.
---

# Model Interpretability

## SHAP (SHapley Additive exPlanations)

### TreeSHAP for Tree Models
```python
import shap

def explain_tree_model(model, X_train, X_explain):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_explain)
    return explainer, shap_values

def visualize_shap(explainer, shap_values, X_explain, feature_names=None):
    shap.summary_plot(shap_values, X_explain, feature_names=feature_names)
    shap.dependence_plot(0, shap_values, X_explain, feature_names=feature_names)
    shap.force_plot(explainer.expected_value, shap_values[0], X_explain[0],
                    feature_names=feature_names, matplotlib=True)
    shap.waterfall_plot(shap.Explanation(
        values=shap_values[0], base_values=explainer.expected_value,
        data=X_explain[0], feature_names=feature_names,
    ))
```

### DeepSHAP for Neural Networks
```python
def explain_neural_network(model, X_background, X_explain):
    background = torch.tensor(X_background[:100], dtype=torch.float32)
    explainer = shap.DeepExplainer(model, background)
    shap_values = explainer.shap_values(torch.tensor(X_explain, dtype=torch.float32))
    return explainer, shap_values

def explain_image_model(model, images, class_idx=None):
    explainer = shap.GradientExplainer(model, images[:50])
    shap_values = explainer.shap_values(images)
    shap.image_plot(shap_values, images)
    return shap_values
```

## LIME

### Tabular Data
```python
from lime import lime_tabular

def explain_with_lime(model, X_train, X_explain, feature_names, class_names=None):
    explainer = lime_tabular.LimeTabularExplainer(
        X_train, feature_names=feature_names, class_names=class_names,
        discretize_continuous=True, random_state=42,
    )
    explanation = explainer.explain_instance(
        X_explain[0], model.predict_proba, num_features=10, num_samples=5000,
    )
    for feature, weight in explanation.as_list():
        print(f"  {feature}: {weight:.4f}")
    return explanation
```

### Text Data
```python
from lime.lime_text import LimeTextExplainer

def explain_text_prediction(model, text, class_names):
    explainer = LimeTextExplainer(class_names=class_names)
    explanation = explainer.explain_instance(
        text, model.predict_proba, num_features=10, num_samples=1000,
    )
    return explanation
```

### Image Data
```python
from lime import lime_image
from skimage.segmentation import mark_boundaries

def explain_image_prediction(model, image, class_idx):
    explainer = lime_image.LimeImageExplainer()
    explanation = explainer.explain_instance(
        image, model.predict, top_labels=5, hide_color=0, num_samples=1000,
    )
    temp, mask = explanation.get_image_and_mask(
        class_idx, positive_only=True, num_features=5, hide_rest=False,
    )
    plt.imshow(mark_boundaries(temp / 255.0, mask))
    return explanation
```

## Attention Visualization

```python
def visualize_attention(attention_weights, tokens, layer=0, head=0):
    attn = attention_weights[layer, head].detach().cpu().numpy()
    sns.heatmap(attn, xticklabels=tokens, yticklabels=tokens, cmap='viridis')
    return attn

def attention_rollout(attentions, add_residual=True):
    """Compute attention rollout for global token importance.
    Attentions: (layers, batch, heads, seq, seq)"""
    attn = attentions.mean(dim=2)
    if add_residual:
        eye = torch.eye(attn.size(-1), device=attn.device)
        attn = 0.5 * attn + 0.5 * eye
    rollout = attn[0]
    for layer_attn in attn[1:]:
        rollout = torch.matmul(layer_attn, rollout)
    return rollout / rollout.sum(dim=-1, keepdim=True)
```

### Attention Caveats

**Attention weights are NOT explanations!**
- Attention != importance - tokens can be important without high attention
- Raw attention ignores value vectors and downstream processing
- Gradient-based methods are often more faithful

Use for: understanding information flow, debugging, qualitative analysis.
Do NOT use for: feature importance claims, regulatory explanations.

```python
def gradient_attention_attribution(model, input_ids, target_idx):
    """More faithful attention attribution using gradients."""
    outputs = model(input_ids, output_attentions=True)
    target_logit = outputs.logits[0, target_idx]
    attention_grads = torch.autograd.grad(target_logit, outputs.attentions, retain_graph=True)
    return [attn * grad for attn, grad in zip(outputs.attentions, attention_grads)]
```

## Integrated Gradients

```python
def integrated_gradients(model, input_tensor, target_class, baseline=None, steps=50):
    if baseline is None:
        baseline = torch.zeros_like(input_tensor)
    alphas = torch.linspace(0, 1, steps, device=input_tensor.device)
    interpolated = baseline + alphas.view(-1, *[1]*(input_tensor.dim()-1)) * (input_tensor - baseline)
    interpolated.requires_grad_(True)
    outputs = model(interpolated)
    gradients = torch.autograd.grad(outputs=outputs[:, target_class].sum(), inputs=interpolated)[0]
    avg_gradients = gradients.mean(dim=0)
    return (input_tensor - baseline) * avg_gradients
```

## Probing Classifiers

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

class ProbingClassifier:
    def __init__(self, model, layer_name):
        self.model = model
        self.activations = []
        # Register forward hook on target layer
        for name, module in model.named_modules():
            if name == layer_name:
                module.register_forward_hook(lambda m, i, o: self.activations.append(o.detach().cpu()))

    def probe(self, representations, labels):
        X = representations.view(representations.size(0), -1).numpy()
        y = labels.numpy()
        probe = LogisticRegression(max_iter=1000, random_state=42)
        scores = cross_val_score(probe, X, y, cv=5, scoring='accuracy')
        return {"mean_accuracy": scores.mean(), "std_accuracy": scores.std()}
```

## Captum Library

```python
from captum.attr import IntegratedGradients, GradientShap, DeepLift, Saliency

def comprehensive_attribution(model, input_tensor, target):
    results = {}
    results["integrated_gradients"] = IntegratedGradients(model).attribute(input_tensor, target=target)
    baseline = torch.zeros_like(input_tensor)
    results["gradient_shap"] = GradientShap(model).attribute(input_tensor, baselines=baseline, target=target)
    results["deeplift"] = DeepLift(model).attribute(input_tensor, target=target)
    results["saliency"] = Saliency(model).attribute(input_tensor, target=target)
    return results
```

## Key Pitfalls

- **Trusting a single method**: Different methods highlight different aspects
- **Ignoring baseline choice**: SHAP/IG results depend heavily on baseline
- **Attention as explanation**: Attention weights are not importances
- **Post-hoc rationalization**: Explanations may not reflect true reasoning
