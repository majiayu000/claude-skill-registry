---
name: active-learning-system
description: Эксперт active learning. Используй для ML с участием человека, uncertainty sampling, annotation workflows и labeling optimization.
---

# Active Learning System Expert

Эксперт по системам активного обучения для машинного обучения.

## Основные стратегии

- **Uncertainty Sampling**: Выбор примеров с наименьшей уверенностью модели
- **Query by Committee**: Использование разногласий ансамбля
- **Expected Model Change**: Выбор наиболее информативных образцов
- **Diversity-based Selection**: Покрытие пространства признаков

## Основной цикл активного обучения

```python
from modAL import ActiveLearner
from modAL.uncertainty import uncertainty_sampling

class ActiveLearningSystem:
    def __init__(self, initial_labeled_pool, unlabeled_pool):
        self.labeled_X, self.labeled_y = initial_labeled_pool
        self.unlabeled_X = unlabeled_pool

        self.learner = ActiveLearner(
            estimator=RandomForestClassifier(n_estimators=100),
            query_strategy=uncertainty_sampling,
            X_training=self.labeled_X,
            y_training=self.labeled_y
        )

    def query_and_update(self, batch_size=10, oracle_func=None):
        query_indices = []
        temp_unlabeled = self.unlabeled_X.copy()

        for _ in range(min(batch_size, len(temp_unlabeled))):
            query_idx, query_instance = self.learner.query(temp_unlabeled)
            query_indices.append(query_idx)
            temp_unlabeled = np.delete(temp_unlabeled, query_idx, axis=0)

        queried_X = self.unlabeled_X[query_indices]
        queried_y = oracle_func(queried_X) if oracle_func else self.simulate_oracle(queried_X)

        self.learner.teach(queried_X, queried_y)
        self.unlabeled_X = np.delete(self.unlabeled_X, query_indices, axis=0)

        return query_indices, queried_X, queried_y
```

## Query by Committee

```python
class CommitteeActiveLearner:
    def __init__(self, X_initial, y_initial):
        self.committee = [
            RandomForestClassifier(n_estimators=50),
            GradientBoostingClassifier(n_estimators=50),
            SVC(probability=True)
        ]

        for clf in self.committee:
            clf.fit(X_initial, y_initial)

    def query_by_committee(self, X_pool, n_instances=1):
        disagreements = []

        for x in X_pool:
            predictions = [clf.predict_proba([x])[0] for clf in self.committee]
            avg_pred = np.mean(predictions, axis=0)
            disagreement = -np.sum(avg_pred * np.log(avg_pred + 1e-10))
            disagreements.append(disagreement)

        selected_indices = np.argsort(disagreements)[-n_instances:]
        return selected_indices, X_pool[selected_indices]
```

## Мониторинг производительности

```python
class ActiveLearningMonitor:
    def track_performance(self, model, X_test, y_test, n_annotations):
        accuracy = accuracy_score(y_test, model.predict(X_test))
        self.performance_history.append(accuracy)
        self.annotation_costs.append(n_annotations)

    def calculate_learning_efficiency(self):
        performance_gains = np.diff(self.performance_history)
        annotation_increments = np.diff(self.annotation_costs)
        efficiency = performance_gains / annotation_increments

        return {
            'current_efficiency': efficiency[-1],
            'average_efficiency': np.mean(efficiency),
            'efficiency_trend': np.polyfit(range(len(efficiency)), efficiency, 1)[0]
        }

    def suggest_stopping_criterion(self):
        efficiency = self.calculate_learning_efficiency()
        if efficiency['current_efficiency'] < 0.001:
            return "Consider stopping - low marginal gains"
        return "Continue learning"
```

## Лучшие практики

### Стратегия холодного старта
- Используйте стратифицированную выборку для начального набора
- Обеспечьте представленность всех классов
- Начинайте минимум с 5-10 примеров на класс

### Оптимизация размера батча
- Маленькие батчи (5-20) для высокой неопределенности
- Большие батчи (50-100) для дорогой аннотации
- Учитывайте усталость аннотатора

### Распространенные ловушки
- Игнорирование дисбаланса классов
- Чрезмерная зависимость от уверенности без калибровки
- Пренебрежение согласованностью аннотаторов
- Неучет шума аннотации
