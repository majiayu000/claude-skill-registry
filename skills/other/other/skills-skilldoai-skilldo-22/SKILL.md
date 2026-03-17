---
name: scikit-learn
description: Machine learning library for classical supervised/unsupervised models, preprocessing, and model evaluation using NumPy/SciPy.
version: 1.8.0
ecosystem: python
license: BSD-3-Clause
generated_with: gpt-5.2
---

## Imports

```python
import sklearn
from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
```

## Core Patterns

### Check installation + environment details ✅ Current
```python
import sklearn

if __name__ == "__main__":
    print("scikit-learn version:", sklearn.__version__)
    sklearn.show_versions()
```
* Use `sklearn.show_versions()` when debugging environment issues (BLAS/OpenMP, NumPy/SciPy versions, compiler info).
* `sklearn.show_versions()` output starts with "System:" in scikit-learn 1.8.0+.

### Train/test split + fit/predict + metrics ✅ Current
```python
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    X, y = datasets.load_breast_cancer(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0, stratify=y
    )

    clf = LogisticRegression(max_iter=2000, solver="lbfgs")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("accuracy:", metrics.accuracy_score(y_test, y_pred))
    print(metrics.classification_report(y_test, y_pred))
```
* Standard estimator workflow: `fit()` on train, `predict()` on test, evaluate with `sklearn.metrics`.

### Pipeline with preprocessing + model ✅ Current
```python
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    X, y = datasets.load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0, stratify=y
    )

    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000)),
        ]
    )

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print("accuracy:", metrics.accuracy_score(y_test, y_pred))
```
* Prefer `Pipeline` to prevent train/test leakage (fit transformers only on training data).

### Hyperparameter search with GridSearchCV ✅ Current
```python
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    X, y = datasets.load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0, stratify=y
    )

    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000)),
        ]
    )

    param_grid = {
        "clf__C": [0.1, 1.0, 10.0],
        "clf__penalty": ["l2"],
        "clf__solver": ["lbfgs"],
    }

    search = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        scoring="accuracy",
        cv=5,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)

    print("best params:", search.best_params_)
    y_pred = search.predict(X_test)
    print("test accuracy:", metrics.accuracy_score(y_test, y_pred))
```
* Use `step__param` names to tune pipeline components.
* Use `n_jobs=-1` to parallelize where supported.

### Nearest-neighbor index + query ✅ Current
```python
import numpy as np
from sklearn.neighbors import NearestNeighbors

if __name__ == "__main__":
    rng = np.random.RandomState(0)
    X = rng.randn(10, 3)
    query = rng.randn(2, 3)

    nn = NearestNeighbors(n_neighbors=3, metric="euclidean")
    nn.fit(X)

    distances, indices = nn.kneighbors(query, return_distance=True)
    print("indices:\n", indices)
    print("distances:\n", distances)
```
* `NearestNeighbors` provides unsupervised neighbor search via `fit()` + `kneighbors()`.

## Configuration

- **Randomness / reproducibility**
  - Many APIs accept `random_state=...` (e.g., `train_test_split`, many estimators). Prefer setting it in tests and benchmarks.
  - Test reproducibility can be controlled via the environment variable **`SKLEARN_SEED`** (used by scikit-learn’s test suite).
- **Installation verification**
  - Prefer `python -m pip ...` to avoid mismatched interpreter vs pip.
  - Useful commands:
    - `python -m pip show scikit-learn`
    - `python -m pip freeze`
    - `python -c "import sklearn; sklearn.show_versions()"`
- **Optional dependencies**
  - Plotting helpers (functions named `plot_...` and classes ending with `...Display`) require `matplotlib`.
- **Running tests**
  - Run from outside the source tree using `pytest sklearn` and ensure pytest meets the minimum required version (per scikit-learn’s developer docs).

## Pitfalls

### Wrong: Mixing OS package manager installs with pip installs (Linux)
```python
# This is a shell sequence, not Python; shown here because it causes Python import/runtime issues.
# sudo apt-get install python3-sklearn
# pip install -U scikit-learn
import sklearn

print(sklearn.__version__)
```

### Right: Use an isolated environment (venv) and verify with sklearn.show_versions()
```python
# Shell sequence:
# python3 -m venv sklearn-env
# source sklearn-env/bin/activate
# python -m pip install -U scikit-learn
# python -c "import sklearn; sklearn.show_versions()"

import sklearn

if __name__ == "__main__":
    sklearn.show_versions()
```

### Wrong: Using `pip` and `python` from different environments/interpreters
```python
# Shell sequence that can target different interpreters:
# pip install -U scikit-learn
# python -c "import sklearn; sklearn.show_versions()"

import sklearn
print(sklearn.__version__)
```

### Right: Always use `python -m pip` with the same interpreter you run
```python
# Shell sequence:
# python -m pip install -U scikit-learn
# python -m pip show scikit-learn
# python -c "import sklearn; sklearn.show_versions()"

import sklearn

if __name__ == "__main__":
    sklearn.show_versions()
```

### Wrong: Plotting API usage without Matplotlib installed
```python
# If matplotlib is not installed, importing plotting helpers can fail at import time.
from sklearn.inspection import PartialDependenceDisplay  # requires matplotlib

print(PartialDependenceDisplay)
```

### Right: Install matplotlib before using plot_* or *Display APIs
```python
# Shell:
# python -m pip install -U scikit-learn matplotlib

from sklearn.inspection import PartialDependenceDisplay

if __name__ == "__main__":
    print("PartialDependenceDisplay import OK:", PartialDependenceDisplay)
```

### Wrong: Data leakage by scaling before train/test split
```python
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    X, y = datasets.load_breast_cancer(return_X_y=True)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # leakage: uses all data statistics

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.25, random_state=0, stratify=y
    )

    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)
    print(metrics.accuracy_score(y_test, clf.predict(X_test)))
```

### Right: Put preprocessing inside a Pipeline
```python
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    X, y = datasets.load_breast_cancer(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0, stratify=y
    )

    pipe = Pipeline(
        steps=[("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=2000))]
    )
    pipe.fit(X_train, y_train)
    print(metrics.accuracy_score(y_test, pipe.predict(X_test)))
```

## References

- [homepage](https://scikit-learn.org)
- [source](https://github.com/scikit-learn/scikit-learn)
- [download](https://pypi.org/project/scikit-learn/#files)
- [tracker](https://github.com/scikit-learn/scikit-learn/issues)
- [release notes](https://scikit-learn.org/stable/whats_new)

## Migration from v1.7

- **No breaking changes in Python version or core APIs between 1.7 and 1.8.0.**
- If upgrading from 1.6 or older, remember: scikit-learn 1.7+ requires **Python >= 3.10**.
- For full migration notes and new features, see: https://scikit-learn.org/stable/whats_new/v1.8.0.html

```python
# Example: Python version runtime guard (if upgrading from <=1.6)
import sys

if __name__ == "__main__":
    if sys.version_info < (3, 10):
        raise RuntimeError("scikit-learn >= 1.7 requires Python >= 3.10")
    print("Python version OK:", sys.version)
```

## API Reference

- **sklearn.__version__** - The installed scikit-learn version (string, e.g., `'1.8.0'`).
- **sklearn.show_versions()** - Print build/runtime dependency versions; use for debugging environment issues.
- **sklearn.clone(estimator, *, safe=True)** - Clone a scikit-learn estimator; returns a new, unfitted estimator with the same parameters.
- **sklearn.get_config()** - Get current global scikit-learn configuration as a dict.
- **sklearn.set_config(assume_finite: bool = False, working_memory: int = 1024, print_changed_only: bool = True, display: str = 'text', pairwise_dist_chunk_size: int = 256)** - Set global scikit-learn configuration.
- **sklearn.config_context(**new_config)** - Context manager for temporarily setting scikit-learn config.
- **sklearn.datasets.load_breast_cancer(return_X_y=True)** - Load a built-in dataset; `return_X_y` returns `(X, y)`.
- **sklearn.model_selection.train_test_split()** - Split arrays into random train/test subsets; key params: `test_size`, `random_state`, `stratify`.
- **sklearn.pipeline.Pipeline(steps=...)** - Chain transformers and an estimator; prevents leakage; params: `steps`.
- **sklearn.preprocessing.StandardScaler()** - Standardize features by removing mean/scaling to unit variance.
- **sklearn.linear_model.LogisticRegression()** - Linear classifier; key params: `C`, `penalty`, `solver`, `max_iter`, `random_state`.
- **sklearn.model_selection.GridSearchCV(estimator, param_grid, cv=..., scoring=...)** - Exhaustive parameter search with CV; key params: `param_grid`, `cv`, `n_jobs`, `scoring`.
- **sklearn.metrics.accuracy_score(y_true, y_pred)** - Classification accuracy metric.
- **sklearn.metrics.classification_report(y_true, y_pred)** - Text summary of precision/recall/F1.
- **sklearn.neighbors.NearestNeighbors(n_neighbors=..., metric=...)** - Unsupervised neighbor search model.
- **NearestNeighbors.fit(X)** - Build neighbor index from training data.
- **NearestNeighbors.kneighbors(X, n_neighbors=..., return_distance=True)** - Query nearest neighbors; returns `(distances, indices)`.
- **sklearn.setup_module(module)** - Used for testing infrastructure; not generally used in user code.
- **pytest (run as: `pytest sklearn`)** - Test invocation convention used by scikit-learn’s test suite.
- **sklearnex.neighbors.NearestNeighbors** - Intel extension drop-in; requires `scikit-learn-intelex` and explicit enablement/patching per its docs.

## Current Library State (from source analysis)

### API Surface
```json
{
  "library_category": "general",
  "apis": [
    {
      "name": "sklearn.clone",
      "type": "function",
      "signature": "clone(estimator, *, safe=True)",
      "signature_truncated": false,
      "return_type": "estimator",
      "module": "sklearn.base",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "estimator": {
          "base_type": "Any",
          "is_optional": false,
          "default_value": null
        },
        "safe": {
          "base_type": "bool",
          "is_optional": true,
          "default_value": "True"
        }
      }
    },
    {
      "name": "sklearn.get_config",
      "type": "function",
      "signature": "get_config() -> dict",
      "signature_truncated": false,
      "return_type": "dict",
      "module": "sklearn._config",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {}
    },
    {
      "name": "sklearn.set_config",
      "type": "function",
      "signature": "set_config(assume_finite: bool = False, working_memory: int = 1024, print_changed_only: bool = True, display: str = 'text', pairwise_dist_chunk_size: int = 256)",
      "signature_truncated": false,
      "return_type": "None",
      "module": "sklearn._config",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "assume_finite": {
          "base_type": "bool",
          "is_optional": true,
          "default_value": "False"
        },
        "working_memory": {
          "base_type": "int",
          "is_optional": true,
          "default_value": "1024"
        },
        "print_changed_only": {
          "base_type": "bool",
          "is_optional": true,
          "default_value": "True"
        },
        "display": {
          "base_type": "str",
          "is_optional": true,
          "default_value": "'text'"
        },
        "pairwise_dist_chunk_size": {
          "base_type": "int",
          "is_optional": true,
          "default_value": "256"
        }
      }
    },
    {
      "name": "sklearn.config_context",
      "type": "class",
      "signature": "config_context(**new_config)",
      "signature_truncated": false,
      "return_type": "config_context",
      "module": "sklearn._config",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {}
    },
    {
      "name": "sklearn.show_versions",
      "type": "function",
      "signature": "show_versions() -> None",
      "signature_truncated": false,
      "return_type": "None",
      "module": "sklearn.utils._show_versions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {}
    },
    {
      "name": "sklearn.setup_module",
      "type": "function",
      "signature": "setup_module(module)",
      "signature_truncated": false,
      "return_type": "None",
      "module": "sklearn",
      "publicity_score": "medium",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "module": {
          "base_type": "Any",
          "is_optional": false,
          "default_value": null
        }
      }
    },
    {
      "name": "sklearn.__version__",
      "type": "descriptor",
      "signature": "__version__ = '1.8.0'",
      "signature_truncated": false,
      "return_type": "str",
      "module": "sklearn",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "sklearn.__check_build.raise_build_error",
      "type": "function",
      "signature": "raise_build_error(e)",
      "signature_truncated": false,
      "return_type": "None",
      "module": "sklearn.__check_build",
      "publicity_score": "low",
      "module_type": "internal",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "note": "Internal build helper for error reporting, not for public use"
    }
    // ... (other high-level public submodules, e.g., sklearn.cluster, sklearn.datasets, etc.)
    // Each submodule (from __all__) is a public API entry point, typically as a module,
    // but here only key functions/classes are shown for brevity. For full API, repeat for each.
  ]
}
```

### Usage Patterns
```json
[
  {
    "api": "DecisionTreeClassifier, ExtraTreeClassifier, RandomForestClassifier, ExtraTreesClassifier",
    "setup_code": [
      "import numpy as np",
      "from sklearn.datasets import make_classification",
      "from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier",
      "from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier"
    ],
    "usage_pattern": [
      "# Setup monotonicity constraints",
      "monotonic_cst = np.zeros(X.shape[1])",
      "monotonic_cst[0] = 1  # monotonic increasing on feature 0",
      "monotonic_cst[1] = -1 # monotonic decreasing on feature 1",
      "est = TreeClassifier(max_depth=None, monotonic_cst=monotonic_cst)",
      "# Optionally: est = TreeClassifier(max_depth=None, monotonic_cst=monotonic_cst, max_leaf_nodes=n_samples_train)",
      "if hasattr(est, 'random_state'): est.set_params(**{'random_state': global_random_seed})",
      "if hasattr(est, 'n_estimators'): est.set_params(**{'n_estimators': 5})",
      "if sparse_splitter: X_train = csc_container(X_train)",
      "est.fit(X_train, y_train)",
      "proba_test = est.predict_proba(X_test)"
    ],
    "assertions": [
      "assert np.logical_and(proba_test >= 0.0, proba_test <= 1.0).all()",
      "assert_allclose(proba_test.sum(axis=1), 1.0)",
      "assert np.all(est.predict_proba(X_test_0incr)[:, 1] >= proba_test[:, 1])  # monotonic increase feature",
      "assert np.all(est.predict_proba(X_test_0decr)[:, 1] <= proba_test[:, 1])",
      "assert np.all(est.predict_proba(X_test_1incr)[:, 1] <= proba_test[:, 1])  # monotonic decrease feature",
      "assert np.all(est.predict_proba(X_test_1decr)[:, 1] >= proba_test[:, 1])"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize (TreeClassifier, depth_first_builder, sparse_splitter, csc_container)",
      "global_random_seed fixture",
      "assert_allclose from sklearn.utils._testing"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "DecisionTreeRegressor, ExtraTreeRegressor, RandomForestRegressor, ExtraTreesRegressor",
    "setup_code": [
      "import numpy as np",
      "from sklearn.datasets import make_regression",
      "from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor",
      "from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor"
    ],
    "usage_pattern": [
      "# Regression with monotonic constraints",
      "monotonic_cst = np.zeros(X.shape[1])",
      "monotonic_cst[0] = 1",
      "monotonic_cst[1] = -1",
      "est = TreeRegressor(max_depth=None, monotonic_cst=monotonic_cst, criterion=criterion)",
      "# Optionally: est = TreeRegressor(max_depth=8, monotonic_cst=monotonic_cst, criterion=criterion, max_leaf_nodes=n_samples_train)",
      "if hasattr(est, 'random_state'): est.set_params(random_state=global_random_seed)",
      "if hasattr(est, 'n_estimators'): est.set_params(**{'n_estimators': 5})",
      "if sparse_splitter: X_train = csc_container(X_train)",
      "est.fit(X_train, y_train)",
      "y = est.predict(X_test)",
      "y_incr = est.predict(X_test_incr)",
      "y_decr = est.predict(X_test_decr)"
    ],
    "assertions": [
      "assert np.all(y_incr >= y)  # monotonic increase constraint",
      "assert np.all(y_decr <= y)  # monotonic decrease constraint"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeRegressor, depth_first_builder, sparse_splitter, criterion, csc_container)",
      "global_random_seed fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "TreeClassifier.fit",
    "setup_code": [
      "from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier, RandomForestClassifier, ExtraTreesClassifier",
      "from sklearn.datasets import make_classification"
    ],
    "usage_pattern": [
      "X, y = make_classification(n_samples=100, n_features=5, n_classes=3, n_informative=3, random_state=0)",
      "monotonic_cst = np.zeros(X.shape[1])",
      "monotonic_cst[0] = -1",
      "monotonic_cst[1] = 1",
      "est = TreeClassifier(max_depth=None, monotonic_cst=monotonic_cst, random_state=0)",
      "est.fit(X, y)"
    ],
    "assertions": [
      "pytest.raises(ValueError, match='Monotonicity constraints are not supported with multiclass classification')"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeClassifier)",
      "pytest.raises context manager"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "TreeClassifier.fit (multiple outputs)",
    "setup_code": [
      "from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier, RandomForestClassifier, ExtraTreesClassifier"
    ],
    "usage_pattern": [
      "X = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]",
      "y = [[1, 0, 1, 0, 1], [1, 0, 1, 0, 1]]",
      "est = TreeClassifier(max_depth=None, monotonic_cst=np.array([-1, 1]), random_state=0)",
      "est.fit(X, y)"
    ],
    "assertions": [
      "pytest.raises(ValueError, match='Monotonicity constraints are not supported with multiple output')"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeClassifier)",
      "pytest.raises context manager"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "Tree.fit (missing values)",
    "setup_code": [
      "from sklearn.datasets import make_classification",
      "from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, ExtraTreeClassifier, ExtraTreeRegressor"
    ],
    "usage_pattern": [
      "X, y = make_classification(n_samples=100, n_features=5, n_classes=2, n_informative=3, random_state=0)",
      "X[0, 0] = np.nan",
      "monotonic_cst = np.zeros(X.shape[1])",
      "monotonic_cst[0] = 1",
      "est = Tree(max_depth=None, monotonic_cst=monotonic_cst, random_state=0)",
      "est.fit(X, y)"
    ],
    "assertions": [
      "pytest.raises(ValueError, match='Input X contains NaN')"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(Tree)",
      "pytest.raises context manager"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "TreeClassifier.fit (bad monotonic_cst shape)",
    "setup_code": [
      "from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier, RandomForestClassifier, ExtraTreesClassifier"
    ],
    "usage_pattern": [
      "X = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]",
      "y = [1, 0, 1, 0, 1]",
      "est = TreeClassifier(max_depth=None, monotonic_cst=np.array([-1, 1, 0]), random_state=0)",
      "est.fit(X, y)"
    ],
    "assertions": [
      "pytest.raises(ValueError, match='monotonic_cst has shape 3 but the input data X has 2 features.')"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeClassifier)",
      "pytest.raises context manager"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "TreeClassifier.fit (bad monotonic_cst values)",
    "setup_code": [
      "from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier, RandomForestClassifier, ExtraTreesClassifier"
    ],
    "usage_pattern": [
      "X = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]",
      "y = [1, 0, 1, 0, 1]",
      "est = TreeClassifier(max_depth=None, monotonic_cst=np.array([-2, 2]), random_state=0)",
      "est.fit(X, y)",
      "est = TreeClassifier(max_depth=None, monotonic_cst=np.array([-1, 0.8]), random_state=0)",
      "est.fit(X, y)"
    ],
    "assertions": [
      "pytest.raises(ValueError, match='monotonic_cst must be None or an array-like of -1, 0 or 1.')",
      "pytest.raises(ValueError, match='monotonic_cst must be None or an array-like of -1, 0 or 1.(.*)0.8]')"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeClassifier)",
      "pytest.raises context manager"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "DecisionTreeRegressor (monotonic 1D, opposite monotonicity)",
    "setup_code": [
      "import numpy as np",
      "from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor"
    ],
    "usage_pattern": [
      "X = np.linspace(-2, 2, 10).reshape(-1, 1)",
      "y = X.ravel()",
      "clf = TreeRegressor(monotonic_cst=[-1])",
      "clf.fit(X, y)",
      "assert clf.tree_.node_count == 1",
      "assert clf.tree_.value[0] == 0.0",
      "clf = TreeRegressor(monotonic_cst=[1])",
      "clf.fit(X, -y)",
      "assert clf.tree_.node_count == 1",
      "assert clf.tree_.value[0] == 0.0"
    ],
    "assertions": [
      "assert clf.tree_.node_count == 1",
      "assert clf.tree_.value[0] == 0.0"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeRegressor)"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "DecisionTreeRegressor/ExtraTreeRegressor (monotonicity for 1D nodes values)",
    "setup_code": [
      "import numpy as np",
      "from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor"
    ],
    "usage_pattern": [
      "X = rng.rand(n_samples, n_features)",
      "y = rng.rand(n_samples)",
      "clf = TreeRegressor(monotonic_cst=[monotonic_sign], criterion=criterion, random_state=global_random_seed)",
      "# Optionally: clf = TreeRegressor(monotonic_cst=[monotonic_sign], max_leaf_nodes=n_samples, criterion=criterion, random_state=global_random_seed)",
      "clf.fit(X, y)",
      "assert_1d_reg_tree_children_monotonic_bounded(clf.tree_, monotonic_sign)",
      "assert_1d_reg_monotonic(clf, monotonic_sign, np.min(X), np.max(X), 100)"
    ],
    "assertions": [
      "assert_1d_reg_tree_children_monotonic_bounded()",
      "assert_1d_reg_monotonic()"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeRegressor, monotonic_sign, depth_first_builder, criterion, global_random_seed)"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "DecisionTreeRegressor/ExtraTreeRegressor (monotonicity for ND nodes values)",
    "setup_code": [
      "import numpy as np",
      "from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor"
    ],
    "usage_pattern": [
      "monotonic_cst = [monotonic_sign, 0]",
      "X = rng.rand(n_samples, n_features)",
      "y = rng.rand(n_samples)",
      "clf = TreeRegressor(monotonic_cst=monotonic_cst, criterion=criterion, random_state=global_random_seed)",
      "# Optionally: clf = TreeRegressor(monotonic_cst=monotonic_cst, max_leaf_nodes=n_samples, criterion=criterion, random_state=global_random_seed)",
      "clf.fit(X, y)",
      "assert_nd_reg_tree_children_monotonic_bounded(clf.tree_, monotonic_cst)"
    ],
    "assertions": [
      "assert_nd_reg_tree_children_monotonic_bounded()"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize(TreeRegressor, monotonic_sign, depth_first_builder, criterion, global_random_seed)"
    ],
    "deprecation_status": "current"
  }
]
```

### Documentation & Changelog
```json
{
  "documented_apis": [
    "sklearn.show_versions",
    "sklearnex.neighbors.NearestNeighbors"
  ],
  "conventions": [
    "Use virtual environments (venv or conda) for isolated and reproducible installations.",
    "Always activate your environment before running Python commands.",
    "Use pip or conda to install official releases of scikit-learn.",
    "Use functions starting with 'plot_' and classes ending with 'Display' for plotting capabilities.",
    "Check versions and installation with 'python -m pip show scikit-learn' and 'python -c \"import sklearn; sklearn.show_versions()\"'.",
    "Use binary wheels for NumPy and SciPy when installing with pip to avoid slow source builds.",
    "Follow the minimum dependency versions as listed in documentation for compatible operation.",
    "After installation, test your setup with 'pytest sklearn' (requires pytest).",
    "For Intel CPUs, consider using 'scikit-learn-intelex' for performance, but be aware solvers are not enabled by default."
  ],
  "pitfalls": [
    {
      "category": "Environment isolation",
      "wrong": "pip install -U scikit-learn  # in system Python or shared environment",
      "why": "Installing scikit-learn globally or in a shared environment can lead to dependency conflicts and unstable environments.",
      "right": "python -m venv sklearn-env\nsource sklearn-env/bin/activate\npip install -U scikit-learn"
    },
    {
      "category": "Linux package conflicts",
      "wrong": "pip install scikit-learn  # after installing system packages via apt/dnf/pacman",
      "why": "Mixing pip installations with OS package manager installations can cause conflicts and broken environments.",
      "right": "Use a virtual environment (venv or conda) and install all packages there, or stick to only your OS package manager."
    },
    {
      "category": "Python version compatibility",
      "wrong": "Using scikit-learn 1.7 with Python 3.9",
      "why": "scikit-learn 1.7 and later require Python 3.10 or newer.",
      "right": "Upgrade your Python version to at least 3.10 before installing scikit-learn 1.7 or newer."
    }
  ],
  "breaking_changes": [
    {
      "version_from": "1.6",
      "version_to": "1.7",
      "change": "Dropped support for Python < 3.10; scikit-learn now requires Python 3.10 or newer.",
      "migration": "Upgrade your environment to Python 3.10 or newer before installing scikit-learn 1.7+."
    }
  ],
  "migration_notes": "See https://scikit-learn.org/dev/whats_new.html for the full changelog and migration guide. Notable: scikit-learn 1.7 requires Python 3.10 or newer. If upgrading from earlier versions, check minimum dependency versions and ensure your environment is compatible."
}
```

---