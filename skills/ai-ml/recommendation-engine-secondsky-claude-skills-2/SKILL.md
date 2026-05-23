---
name: recommendation-engine
description: Build recommendation systems with collaborative filtering, matrix factorization, hybrid approaches. Use for product recommendations, personalization, or encountering cold start, sparsity, quality evaluation issues.
keywords: recommendation engine, collaborative filtering, matrix factorization, SVD, ALS, NMF, user-based CF, item-based CF, cold start, precision@k, recall@k, NDCG, hybrid recommender, content-based filtering, cosine similarity, implicit feedback, evaluation metrics, diversity, coverage
license: MIT
---

# Recommendation Engine

Build recommendation systems for personalized content and product suggestions.

## Recommendation Approaches

| Approach | How It Works | Pros | Cons |
|----------|--------------|------|------|
| Collaborative | User-item interactions | Discovers hidden patterns | Cold start |
| Content-based | Item features | Works for new items | Limited discovery |
| Hybrid | Combines both | Best of both | Complex |

## Collaborative Filtering

```python
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFilter:
    def __init__(self):
        self.user_similarity = None
        self.item_similarity = None

    def fit(self, user_item_matrix):
        # User-based similarity
        self.user_similarity = cosine_similarity(user_item_matrix)
        # Item-based similarity
        self.item_similarity = cosine_similarity(user_item_matrix.T)

    def recommend_for_user(self, user_id, n=10):
        scores = self.user_similarity[user_id].dot(self.user_item_matrix)
        # Exclude already interacted items
        already_interacted = self.user_item_matrix[user_id].nonzero()[0]
        scores[already_interacted] = -np.inf
        return np.argsort(scores)[-n:][::-1]
```

## Matrix Factorization (SVD)

```python
from sklearn.decomposition import TruncatedSVD

class MatrixFactorization:
    def __init__(self, n_factors=50):
        self.svd = TruncatedSVD(n_components=n_factors)

    def fit(self, user_item_matrix):
        self.user_factors = self.svd.fit_transform(user_item_matrix)
        self.item_factors = self.svd.components_.T

    def predict(self, user_id, item_id):
        return np.dot(self.user_factors[user_id], self.item_factors[item_id])
```

## Hybrid Recommender

```python
class HybridRecommender:
    def __init__(self, collab_weight=0.7, content_weight=0.3):
        self.collab = CollaborativeFilter()
        self.content = ContentBasedFilter()
        self.weights = (collab_weight, content_weight)

    def recommend(self, user_id, n=10):
        collab_scores = self.collab.score(user_id)
        content_scores = self.content.score(user_id)
        combined = self.weights[0] * collab_scores + self.weights[1] * content_scores
        return np.argsort(combined)[-n:][::-1]
```

## Evaluation Metrics

- Precision@K, Recall@K
- NDCG (ranking quality)
- Coverage (catalog diversity)
- A/B test conversion rate

## Cold Start Solutions

- **New users**: Popular items, onboarding preferences, demographic-based
- **New items**: Content-based bootstrapping, active learning
- **Exploration strategies**: ε-greedy, Thompson sampling bandits

## Quick Start: Build a Recommender in 5 Steps

```python
from scipy.sparse import csr_matrix
import numpy as np

# 1. Prepare user-item interaction matrix
# rows = users, cols = items, values = ratings/interactions
ratings_data = [(0, 5, 5), (0, 10, 4), (1, 5, 3), ...]  # (user, item, rating)
n_users, n_items = 1000, 5000

row_idx = [r[0] for r in ratings_data]
col_idx = [r[1] for r in ratings_data]
ratings = [r[2] for r in ratings_data]
user_item_matrix = csr_matrix((ratings, (row_idx, col_idx)), shape=(n_users, n_items))

# 2. Choose and train model
from recommendation_engine import ItemBasedCollaborativeFilter  # See references

model = ItemBasedCollaborativeFilter(similarity_metric='cosine', k_neighbors=20)
model.fit(user_item_matrix)

# 3. Generate recommendations
recommendations = model.recommend(user_id=42, n=10)
print(recommendations)  # [(item_id, score), ...]

# 4. Evaluate on test set
from evaluation_metrics import precision_at_k, recall_at_k

test_items = {42: {10, 25, 30}}  # True relevant items for user 42
rec_items = [item for item, score in recommendations]

precision = precision_at_k(rec_items, test_items[42], k=10)
recall = recall_at_k(rec_items, test_items[42], k=10)
print(f"Precision@10: {precision:.3f}, Recall@10: {recall:.3f}")

# 5. Handle cold start
from cold_start import PopularityRecommender

popularity_model = PopularityRecommender()
popularity_model.fit(interactions_with_timestamps)
new_user_recs = popularity_model.recommend(n=10)
```

## Known Issues Prevention

### 1. Popularity Bias
**Problem**: Recommending only popular items, ignoring long tail. Reduces diversity and serendipity.

**Solution**: Balance popularity with personalization, apply re-ranking for diversity:
```python
def diversify_recommendations(
    recommendations: List[Tuple[int, float]],
    item_features: np.ndarray,
    diversity_weight: float = 0.3
) -> List[Tuple[int, float]]:
    """Re-rank to increase diversity while maintaining relevance."""
    from sklearn.metrics.pairwise import cosine_distances

    selected = []
    candidates = recommendations.copy()

    while len(selected) < len(recommendations) and candidates:
        if not selected:
            # First item: highest score
            selected.append(candidates.pop(0))
            continue

        # Compute diversity scores
        selected_features = item_features[[item for item, _ in selected]]
        diversity_scores = []

        for item, relevance in candidates:
            item_feature = item_features[item].reshape(1, -1)
            # Average distance to already selected items
            avg_distance = cosine_distances(item_feature, selected_features).mean()
            # Combined score: relevance + diversity
            combined = (1 - diversity_weight) * relevance + diversity_weight * avg_distance
            diversity_scores.append((item, relevance, combined))

        # Select item with best combined score
        best = max(diversity_scores, key=lambda x: x[2])
        selected.append((best[0], best[1]))
        candidates = [(i, s) for i, s, _ in diversity_scores if i != best[0]]

    return selected
```

### 2. Data Sparsity (Matrix >99% Empty)
**Problem**: Collaborative filtering fails when most users have rated <1% of items.

**Solution**: Use matrix factorization (SVD, ALS) instead of memory-based CF:
```python
# ❌ Bad: User-based CF on sparse data (fails to find similar users)
user_cf = UserBasedCollaborativeFilter()
user_cf.fit(sparse_matrix)  # Most users have <10 ratings

# ✅ Good: Matrix factorization handles sparsity
from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=50)
user_factors = svd.fit_transform(sparse_matrix)
item_factors = svd.components_.T

# Predict rating: user_factors[u] @ item_factors[i]
```

### 3. Cold Start Without Fallback
**Problem**: Recommender crashes or returns empty results for new users/items.

**Solution**: Always implement fallback chain:
```python
def recommend_with_fallback(user_id, n=10):
    """Graceful degradation through fallback chain."""
    try:
        # Try personalized recommendations
        if has_sufficient_history(user_id, min_interactions=5):
            return collaborative_filter.recommend(user_id, n)
    except Exception as e:
        logger.warning(f"CF failed for user {user_id}: {e}")

    # Fallback 1: Demographic-based
    if user_demographics_available(user_id):
        return demographic_recommender.recommend(user_id, n)

    # Fallback 2: Popularity
    return popularity_recommender.recommend(n)
```

### 4. Not Excluding Already-Interacted Items
**Problem**: Recommending items user already purchased/viewed wastes recommendation slots.

**Solution**: Always filter interacted items:
```python
# ✅ Correct: Exclude interacted items
user_items = user_item_matrix[user_id].nonzero()[1]
scores[user_items] = -np.inf  # Ensure they don't appear in top-K
recommendations = np.argsort(scores)[-n:][::-1]

# ❌ Wrong: Forgetting to filter
recommendations = np.argsort(scores)[-n:][::-1]  # May include already purchased!
```

### 5. Ignoring Implicit Feedback Confidence
**Problem**: Treating all clicks/views equally. 1 view ≠ 100 views.

**Solution**: Weight by interaction strength (view count, watch time, etc.):
```python
# For implicit feedback, use confidence weighting
confidence_matrix = 1 + alpha * np.log(1 + interaction_counts)

# In ALS: C_ui * (P_ui - X_ui)²
# Higher confidence for items with more interactions
```

### 6. Not Evaluating Ranking Quality (Using Only Accuracy)
**Problem**: High prediction accuracy (RMSE) doesn't mean good top-K recommendations.

**Solution**: Use ranking metrics (NDCG, MAP@K):
```python
# ❌ Bad: Only RMSE
from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

# ✅ Good: Ranking metrics for top-K evaluation
from evaluation_metrics import ndcg_at_k, mean_average_precision_at_k

# NDCG rewards putting highly relevant items first
ndcg = ndcg_at_k(recommendations, relevance_scores, k=10)

# MAP@K considers precision at each relevant item position
map_score = mean_average_precision_at_k(all_recommendations, ground_truth, k=10)
```

### 7. Filter Bubble (Lack of Exploration)
**Problem**: Always recommending similar items limits discovery, reduces user engagement over time.

**Solution**: Implement explore-exploit strategy:
```python
class ExploreExploitRecommender:
    def __init__(self, base_model, epsilon=0.1):
        self.base_model = base_model
        self.epsilon = epsilon  # 10% exploration

    def recommend(self, user_id, n=10):
        # Exploit: Use trained model for most recommendations
        n_exploit = int(n * (1 - self.epsilon))
        exploitative_recs = self.base_model.recommend(user_id, n=n_exploit)

        # Explore: Add random diverse items
        n_explore = n - n_exploit
        explored_items = sample_diverse_items(n_explore)

        return exploitative_recs + explored_items
```

## When to Load References

Load reference files when you need detailed implementations:

- **Collaborative Filtering**: Load `references/collaborative-filtering-deep-dive.md` for complete user-based and item-based CF implementations with similarity metrics (cosine, Pearson, Jaccard), scalability optimizations (sparse matrices, approximate nearest neighbors), and handling edge cases (cold start, sparsity)

- **Matrix Factorization**: Load `references/matrix-factorization-methods.md` for SVD, ALS, and NMF implementations with hyperparameter tuning, implicit feedback handling, and advanced techniques (BPR, WARP)

- **Evaluation Metrics**: Load `references/evaluation-metrics-implementation.md` for Precision@K, Recall@K, NDCG, coverage, diversity metrics, cross-validation strategies, and statistical significance testing (paired t-test, bootstrap confidence intervals)

- **Cold Start Solutions**: Load `references/cold-start-strategies.md` for new user/item strategies (popularity-based, onboarding, demographic, content-based bootstrapping, active learning), explore-exploit approaches (ε-greedy, Thompson sampling), and hybrid fallback chains
