---
name: eda-and-visualization
description: Exploratory data analysis workflows, visualization library patterns, statistical plots, and ML evaluation visuals.
---

# EDA and Visualization

## Visualization Library Selection

| Requirement | matplotlib | seaborn | plotly | altair |
|---|---|---|---|---|
| Publication-quality static plots | Best | Good | | |
| Statistical visualizations | Manual | Built-in | Manual | Declarative |
| Interactive exploration | | | Best | Good |
| Dashboard / web embedding | | | Best | Good |
| Large datasets (>100k points) | Good | Slow | datashader | Good |
| Minimal code for common plots | Verbose | Minimal | Moderate | Minimal |
| Customization depth | Full | Moderate | Full | Moderate |
| Notebook-first workflow | Good | Best | Best | Good |

**Default recommendation**: seaborn for static EDA, plotly for interactive/stakeholder-facing.

## EDA Template Function

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def eda_summary(df: pd.DataFrame, target: str | None = None) -> None:
    """Quick EDA overview. Prints stats, shows distributions and correlations."""
    print(f"Shape: {df.shape}")
    print(f"Dtypes:\n{df.dtypes.value_counts()}\n")
    print(f"Missing:\n{df.isnull().sum()[df.isnull().sum() > 0]}\n")
    print(f"Duplicates: {df.duplicated().sum()}\n")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Numeric distributions
    if num_cols:
        n = len(num_cols)
        fig, axes = plt.subplots(
            nrows=(n + 2) // 3, ncols=min(n, 3),
            figsize=(5 * min(n, 3), 4 * ((n + 2) // 3)),
        )
        for ax, col in zip(np.ravel(axes) if n > 1 else [axes], num_cols):
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(col)
        plt.tight_layout()
        plt.show()

    # Correlation matrix
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        fig, ax = plt.subplots(figsize=(max(8, len(num_cols)), max(6, len(num_cols) * 0.8)))
        sns.heatmap(
            corr, mask=mask, annot=True, fmt=".2f",
            cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax,
        )
        plt.title("Correlation Matrix")
        plt.tight_layout()
        plt.show()

    # Categorical value counts
    for col in cat_cols[:10]:
        vc = df[col].value_counts()
        if len(vc) <= 20:
            fig, ax = plt.subplots(figsize=(8, max(3, len(vc) * 0.3)))
            sns.countplot(data=df, y=col, order=vc.index, ax=ax)
            ax.set_title(f"{col} (nunique={len(vc)})")
            plt.tight_layout()
            plt.show()
```

## Publication-Quality Figures

```python
import matplotlib.pyplot as plt
from matplotlib import rcParams

def set_pub_style():
    """Configure matplotlib for publication-quality output."""
    rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.figsize": (6.4, 4.0),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
    })

set_pub_style()

# Example: grouped bar chart with error bars
fig, ax = plt.subplots()
x = np.arange(4)
width = 0.35
ax.bar(x - width/2, [3.1, 2.8, 4.2, 3.9], width, yerr=[0.2]*4, label="Model A", capsize=3)
ax.bar(x + width/2, [2.9, 3.1, 3.8, 4.1], width, yerr=[0.3]*4, label="Model B", capsize=3)
ax.set_xticks(x)
ax.set_xticklabels(["Q1", "Q2", "Q3", "Q4"])
ax.set_ylabel("Score")
ax.legend()
fig.savefig("comparison.png")
```

## Interactive Plotly Dashboards

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def interactive_eda(df: pd.DataFrame, target: str) -> go.Figure:
    """Build an interactive multi-panel EDA figure."""
    num_cols = df.select_dtypes(include="number").columns.tolist()
    num_cols = [c for c in num_cols if c \!= target][:4]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f"{c} vs {target}" for c in num_cols],
    )
    for i, col in enumerate(num_cols):
        row, col_idx = divmod(i, 2)
        fig.add_trace(
            go.Scatter(
                x=df[col], y=df[target], mode="markers",
                marker=dict(size=4, opacity=0.5),
                name=col,
            ),
            row=row + 1, col=col_idx + 1,
        )
    fig.update_layout(height=700, showlegend=False, template="plotly_white")
    return fig
```

## ML Evaluation Plots

### Confusion Matrix + ROC + Learning Curve

```python
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import learning_curve

def plot_classification_eval(model, X_test, y_test, class_names=None):
    """Three-panel classification evaluation."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", ax=axes[0],
        xticklabels=class_names, yticklabels=class_names,
    )
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")
    axes[0].set_title("Confusion Matrix")

    # ROC curve
    if y_proba is not None:
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        axes[1].plot(fpr, tpr, label=f"AUC = {auc(fpr, tpr):.3f}")
        axes[1].plot([0, 1], [0, 1], "k--", alpha=0.3)
        axes[1].set_xlabel("FPR")
        axes[1].set_ylabel("TPR")
        axes[1].set_title("ROC Curve")
        axes[1].legend()

    # Learning curve
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_test, y_test, cv=5,
        train_sizes=np.linspace(0.1, 1.0, 10), scoring="accuracy",
    )
    axes[2].plot(train_sizes, train_scores.mean(axis=1), label="Train")
    axes[2].fill_between(
        train_sizes,
        train_scores.mean(axis=1) - train_scores.std(axis=1),
        train_scores.mean(axis=1) + train_scores.std(axis=1), alpha=0.2,
    )
    axes[2].plot(train_sizes, val_scores.mean(axis=1), label="Validation")
    axes[2].fill_between(
        train_sizes,
        val_scores.mean(axis=1) - val_scores.std(axis=1),
        val_scores.mean(axis=1) + val_scores.std(axis=1), alpha=0.2,
    )
    axes[2].set_xlabel("Training Size")
    axes[2].set_ylabel("Accuracy")
    axes[2].set_title("Learning Curve")
    axes[2].legend()

    plt.tight_layout()
    return fig
```

## Gotchas and Anti-Patterns

### Misleading Axis Scales
- **Problem**: Truncated y-axis exaggerates small differences. Dual axes conflate unrelated metrics.
- **Fix**: Start y-axis at 0 for bar charts. Annotate scale breaks explicitly. Avoid dual y-axes; use facets instead.

### Color Accessibility
- **Problem**: Red-green palettes are invisible to ~8% of males.
- **Fix**: Use `cmap="viridis"` (perceptually uniform, colorblind-safe). For categorical: `sns.color_palette("colorblind")`. Test with [Coblis simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/).

### Overplotting
- **Problem**: Scatter plots with >10k points become unreadable blobs.
- **Fix**: Use `alpha=0.1`, `hexbin`, `kde`, or `datashader`. Sample for exploration, full data for final.

```python
# hexbin for large datasets
ax.hexbin(df["x"], df["y"], gridsize=40, cmap="YlOrRd", mincnt=1)
plt.colorbar(ax.collections[0], label="Count")
```

### Chart Junk
- **Problem**: 3D effects, excessive gridlines, decorative elements obscure data.
- **Fix**: Maximize data-ink ratio. Remove top/right spines. Use `sns.despine()`. Reserve color for meaning, not decoration.

### Forgetting to Close Figures
- **Problem**: Memory leak in loops generating many plots.
- **Fix**: Always `plt.close(fig)` after saving in batch operations, or use `plt.close("all")`.
