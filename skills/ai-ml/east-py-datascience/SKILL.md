---
name: east-py-datascience
description: "Data science and machine learning platform functions for the East language (TypeScript types). Use when writing East programs that need optimization (MADS, Optuna, SimAnneal, Scipy), machine learning (XGBoost, LightGBM, NGBoost, Torch MLP, Lightning, GP), ML utilities (Sklearn preprocessing, metrics, splits), conformal prediction (MAPIE), or model explainability (SHAP). Triggers for: (1) Writing East programs with @elaraai/east-py-datascience, (2) Derivative-free optimization with MADS, (3) Bayesian optimization with Optuna, (4) Discrete/combinatorial optimization with SimAnneal, (5) Gradient boosting with XGBoost or LightGBM, (6) Probabilistic predictions with NGBoost or GP, (7) Neural networks with Torch MLP or Lightning, (8) Data preprocessing and metrics with Sklearn, (9) Conformal prediction intervals with MAPIE, (10) Model explainability with Shap."
---

# East Data Science

Data science and machine learning platform functions for the East language. Provides optimization, ML models, preprocessing, and explainability.

## Quick Start

```typescript
import { East, FloatType, variant } from "@elaraai/east";
import { MADS } from "@elaraai/east-py-datascience";

// Define objective function
const objective = East.function([MADS.Types.VectorType], FloatType, ($, x) => {
    const x0 = $.let(x.get(0n));
    const x1 = $.let(x.get(1n));
    return $.return(x0.multiply(x0).add(x1.multiply(x1)));
});

// Optimize
const optimize = East.function([], MADS.Types.ResultType, $ => {
    const x0 = $.let([0.5, 0.5]);
    const bounds = $.let({ lower: [-1.0, -1.0], upper: [1.0, 1.0] });
    const config = $.let({
        max_bb_eval: variant('some', 100n),
        display_degree: variant('some', 0n),
        direction_type: variant('none', null),
        initial_mesh_size: variant('none', null),
        min_mesh_size: variant('none', null),
        seed: variant('some', 42n),
    });
    return $.return(MADS.optimize(objective, x0, bounds, variant('none', null), config));
});
```

## Decision Tree: Which Module to Use

```
Task → What do you need?
    │
    ├─ MADS (derivative-free continuous optimization)
    │   └─ .optimize()
    │
    ├─ Optuna (Bayesian hyperparameter tuning)
    │   └─ .optimize()
    │
    ├─ SimAnneal (discrete/combinatorial optimization)
    │   └─ .optimize(), .optimizePermutation(), .optimizeSubset()
    │
    ├─ ALNS (adaptive large neighborhood search)
    │   └─ .optimize([SolutionType], initial, objective, destroys, repairs, config)
    │   └─ Generic over solution type S - define your own struct
    │
    ├─ Scipy
    │   ├─ Optimization → .optimizeMinimize(), .optimizeMinimizeQuadratic(), .optimizeDualAnnealing()
    │   ├─ Statistics → .statsDescribe(), .statsPearsonr(), .statsSpearmanr(), .statsPercentile(), .statsIqr(), .statsMedian(), .statsMad(), .statsRobust()
    │   ├─ Curve Fitting → .curveFit()
    │   └─ Interpolation → .interpolate1dFit(), .interpolate1dPredict()
    │
    ├─ XGBoost (gradient boosting)
    │   ├─ Train → .trainRegressor(), .trainClassifier(), .trainQuantile()
    │   └─ Predict → .predict(), .predictClass(), .predictProba(), .predictQuantile()
    │
    ├─ LightGBM (fast gradient boosting)
    │   ├─ Train → .trainRegressor(), .trainClassifier()
    │   └─ Predict → .predict(), .predictClass(), .predictProba()
    │
    ├─ NGBoost (probabilistic gradient boosting)
    │   ├─ Train → .trainRegressor()
    │   └─ Predict → .predict(), .predictDist()
    │
    ├─ Torch (neural networks)
    │   ├─ Train → .mlpTrain(), .mlpTrainMulti()
    │   ├─ Predict → .mlpPredict(), .mlpPredictMulti()
    │   └─ Embeddings → .mlpEncode(), .mlpDecode()
    │
    ├─ Lightning (PyTorch Lightning neural networks)
    │   ├─ Train → .train(X, y, config, masks, group_weights, conditions)
    │   ├─ Predict → .predict(model, X, masks, conditions)
    │   ├─ Embeddings → .encode(), .decode(), .decodeConditional() (autoencoder only)
    │   ├─ Architectures:
    │   │   ├─ mlp: simple feedforward
    │   │   ├─ autoencoder: encoder → latent → decoder
    │   │   ├─ conv1d: 1D convolutional autoencoder (temporal)
    │   │   ├─ sequential: LSTM/GRU autoencoder (temporal)
    │   │   └─ transformer: attention-based autoencoder (temporal)
    │   ├─ Output modes:
    │   │   ├─ regression: MSE loss
    │   │   ├─ binary: BCE loss, per-position pos_weights (VectorType), masks
    │   │   └─ multi_head: N independent CE heads, per-head class_weights, masks
    │   ├─ Conditional generation: condition_dim in temporal architectures
    │   └─ Features: early stopping, gradient clipping, epoch callbacks, group_weights
    │
    ├─ GP (Gaussian Process regression)
    │   ├─ Train → .train()
    │   └─ Predict → .predict(), .predictStd()
    │
    ├─ MAPIE (conformal prediction intervals)
    │   ├─ Regression → .trainConformalRegressor(), .trainCQR()
    │   ├─ Classification → .trainConformalClassifier()
    │   ├─ Predict → .predictInterval(), .predictSet()
    │   └─ SHAP integration → .uncertaintyPredictorRegressor(), .uncertaintyPredictorClassifier()
    │
    ├─ Sklearn (preprocessing & metrics)
    │   ├─ Splitting (with stratification and rare class filtering) → .trainTestSplit(), .trainValTestSplit()
    │   ├─ Scaling → .standardScalerFit/Transform(), .minMaxScalerFit/Transform(), .robustScalerFit/Transform()
    │   ├─ Encoding → .labelEncoderFit/Transform/InverseTransform(), .ordinalEncoderFit/Transform()
    │   ├─ Class weights → .computeClassWeight()
    │   ├─ Regression metrics → .computeMetrics(), .computeMetricsMulti()
    │   ├─ Classification metrics → .computeClassificationMetrics(), .computeClassificationMetricsMulti()
    │   ├─ Probability metrics → .rocAucScore(), .logLoss(), .confusionMatrix()
    │   └─ Multi-target → .regressorChainTrain(), .regressorChainPredict()
    │
    └─ Shap (model explainability)
        ├─ Create → .treeExplainerCreate() (XGBoost only), .kernelExplainerCreate() (any model)
        ├─ Compute → .computeValues(), .featureImportance()
        └─ Supports → TreeExplainer: XGBoost; KernelExplainer: XGBoost, LightGBM, NGBoost, GP, Torch, RegressorChain, MAPIE
```

## Common Types

| Type | Definition | Description |
|------|------------|-------------|
| `VectorType` | `ArrayType(FloatType)` | 1D array of floats (e.g., `[1.0, 2.0, 3.0]`) |
| `MatrixType` | `ArrayType(ArrayType(FloatType))` | 2D array of floats (e.g., `[[1.0, 2.0], [3.0, 4.0]]`) |
| `LabelVectorType` | `ArrayType(IntegerType)` | Class labels as integers (e.g., `[0n, 1n, 0n, 2n]`) |
| `ModelBlobType` | `BlobType` | Serialized model (opaque, pass to predict functions) |

## Reference Documentation

- **[API Reference](./reference/api.md)** - Complete function signatures, types, and config options
- **[Examples](./reference/examples.md)** - Working code examples by use case

## Available Modules

| Module | Import | Purpose |
|--------|--------|---------|
| MADS | `import { MADS } from "@elaraai/east-py-datascience"` | Derivative-free blackbox optimization |
| Optuna | `import { Optuna } from "@elaraai/east-py-datascience"` | Bayesian optimization (hyperparameter tuning) |
| SimAnneal | `import { SimAnneal } from "@elaraai/east-py-datascience"` | Simulated annealing (permutation/subset) |
| ALNS | `import { ALNS } from "@elaraai/east-py-datascience"` | Adaptive Large Neighborhood Search (generic over solution type) |
| Scipy | `import { Scipy } from "@elaraai/east-py-datascience"` | Statistics, optimization, interpolation |
| XGBoost | `import { XGBoost } from "@elaraai/east-py-datascience"` | Gradient boosting (regression/classification/quantile) |
| LightGBM | `import { LightGBM } from "@elaraai/east-py-datascience"` | Fast gradient boosting |
| NGBoost | `import { NGBoost } from "@elaraai/east-py-datascience"` | Probabilistic gradient boosting |
| Torch | `import { Torch } from "@elaraai/east-py-datascience"` | Neural networks (MLP) |
| Lightning | `import { Lightning } from "@elaraai/east-py-datascience"` | PyTorch Lightning neural networks |
| GP | `import { GP } from "@elaraai/east-py-datascience"` | Gaussian Process regression |
| MAPIE | `import { MAPIE } from "@elaraai/east-py-datascience"` | Conformal prediction intervals |
| Sklearn | `import { Sklearn } from "@elaraai/east-py-datascience"` | Preprocessing, metrics, data splitting |
| Shap | `import { Shap } from "@elaraai/east-py-datascience"` | Model explainability (SHAP values) |

## Accessing Types

```typescript
import { MADS, Optuna, Sklearn, XGBoost, ALNS } from "@elaraai/east-py-datascience";

// Access types via Module.Types.TypeName
MADS.Types.VectorType          // ArrayType(FloatType)
MADS.Types.BoundsType          // StructType({ lower, upper })
MADS.Types.ResultType          // StructType({ x_best, f_best, ... })

Optuna.Types.ParamSpaceType    // Parameter definition
Optuna.Types.StudyResultType   // Optimization result

ALNS.Types.ConfigType          // ALNS configuration
ALNS.Types.ResultType          // Result with "S" placeholder for solution type

Sklearn.Types.SplitConfigType  // Train/test split config
XGBoost.Types.ModelBlobType    // Trained model
```

## Common Patterns

### Train and Predict

```typescript
// 1. Prepare data
const X = $.let([[...], [...], ...]);
const y = $.let([...]);

// 2. Configure and train
const config = $.let({ /* options with variant('some', value) or variant('none', null) */ });
const model = $.let(Module.train(X, y, config));

// 3. Predict
const predictions = $.let(Module.predict(model, X_test));
```

### Optimization

```typescript
// 1. Define objective function
const objective = East.function([VectorType], FloatType, ($, x) => {
    // compute and return objective value
});

// 2. Set bounds and config
const bounds = $.let({ lower: [...], upper: [...] });
const config = $.let({ /* options */ });

// 3. Optimize
const result = $.let(Module.optimize(objective, x0, bounds, config));
// result.x_best, result.f_best
```
