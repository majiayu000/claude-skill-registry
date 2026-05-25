---
name: ab-test-framework-ml
description: Эксперт A/B тестирования. Используй для статистических тестов, экспериментов и ML-оптимизации.
---

# A/B Test фреймворк для Machine Learning

Вы эксперт по проектированию, реализации и анализу A/B тестов специально для систем машинного обучения. Вы понимаете уникальные вызовы тестирования ML моделей в продакшене, включая дрифт концепций, смещение моделей, расчеты статистической мощности и сложности измерения как бизнес-метрик, так и метрик производительности моделей.

## Основные принципы ML A/B тестирования

### Статистическая строгость
- Всегда определяйте первичные и вторичные метрики перед запуском эксперимента
- Рассчитывайте минимально детектируемый эффект (MDE) и необходимые размеры выборки заранее
- Учитывайте коррекции множественного тестирования при оценке нескольких метрик
- Используйте правильные единицы рандомизации (уровень пользователя, сессии или запроса)

### ML-специфичные соображения
- Мониторьте как метрики производительности модели (точность, AUC, precision/recall), так и бизнес-метрики (конверсия, выручка, вовлеченность)
- Учитывайте задержку инференса модели и вычислительные затраты в вашем анализе
- Рассматривайте временные эффекты и сезонность при анализе результатов
- Обрабатывайте версионирование моделей и воспроизводимость на протяжении всего эксперимента

## Фреймворк дизайна экспериментов

### Расчет размера выборки
```python
import numpy as np
from scipy import stats
from statsmodels.stats.power import ttest_power

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    Calculate required sample size for A/B test

    Args:
        baseline_rate: Current conversion/success rate
        mde: Minimum detectable effect (relative change)
        alpha: Type I error rate
        power: Statistical power (1 - Type II error)
    """
    effect_size = mde * baseline_rate / np.sqrt(baseline_rate * (1 - baseline_rate))
    n = ttest_power(effect_size, power=power, alpha=alpha, alternative='two-sided')
    return int(np.ceil(n))

# Example: Need to detect 5% relative improvement in 20% baseline conversion
sample_size = calculate_sample_size(baseline_rate=0.20, mde=0.05)
print(f"Required sample size per variant: {sample_size}")
```

### Рандомизация и разделение трафика
```python
import hashlib
import random

class ABTestSplitter:
    def __init__(self, experiment_name, traffic_allocation=0.1, control_ratio=0.5):
        self.experiment_name = experiment_name
        self.traffic_allocation = traffic_allocation
        self.control_ratio = control_ratio

    def get_variant(self, user_id):
        # Consistent hashing for user assignment
        hash_input = f"{self.experiment_name}_{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest()[:8], 16)
        bucket = hash_value / (2**32)  # Normalize to [0,1)

        # Check if user is in experiment
        if bucket >= self.traffic_allocation:
            return "not_in_experiment"

        # Assign to control or treatment
        experiment_bucket = bucket / self.traffic_allocation
        if experiment_bucket < self.control_ratio:
            return "control"
        else:
            return "treatment"

# Usage
splitter = ABTestSplitter("model_v2_test", traffic_allocation=0.2, control_ratio=0.5)
variant = splitter.get_variant("user_12345")
```

## Деплой модели и мониторинг

### Интеграция с Feature Store
```python
class ABTestModelServer:
    def __init__(self, control_model, treatment_model, splitter):
        self.control_model = control_model
        self.treatment_model = treatment_model
        self.splitter = splitter
        self.metrics_logger = MetricsLogger()

    def predict(self, user_id, features):
        variant = self.splitter.get_variant(user_id)

        start_time = time.time()

        if variant == "control":
            prediction = self.control_model.predict(features)
            model_version = "control"
        elif variant == "treatment":
            prediction = self.treatment_model.predict(features)
            model_version = "treatment"
        else:
            prediction = self.control_model.predict(features)
            model_version = "control"

        latency = time.time() - start_time

        # Log prediction and metadata
        self.metrics_logger.log_prediction({
            'user_id': user_id,
            'variant': variant,
            'model_version': model_version,
            'prediction': prediction,
            'latency_ms': latency * 1000,
            'timestamp': time.time()
        })

        return prediction, variant
```

## Фреймворк статистического анализа

### Байесовский анализ A/B тестов
```python
import pymc3 as pm
import arviz as az

def bayesian_ab_test(control_conversions, control_total,
                    treatment_conversions, treatment_total):
    """
    Bayesian analysis for conversion rate A/B test
    """
    with pm.Model() as model:
        # Priors
        alpha_control = pm.Beta('alpha_control', alpha=1, beta=1)
        alpha_treatment = pm.Beta('alpha_treatment', alpha=1, beta=1)

        # Likelihood
        control_obs = pm.Binomial('control_obs',
                                 n=control_total,
                                 p=alpha_control,
                                 observed=control_conversions)
        treatment_obs = pm.Binomial('treatment_obs',
                                   n=treatment_total,
                                   p=alpha_treatment,
                                   observed=treatment_conversions)

        # Derived quantities
        lift = pm.Deterministic('lift',
                               (alpha_treatment - alpha_control) / alpha_control)

        # Sample
        trace = pm.sample(2000, tune=1000, return_inferencedata=True)

    # Calculate probability of positive lift
    prob_positive = (trace.posterior.lift > 0).mean().item()

    return trace, prob_positive
```

### Последовательное тестирование и досрочная остановка
```python
class SequentialABTest:
    def __init__(self, alpha=0.05, beta=0.2, mde=0.05):
        self.alpha = alpha
        self.beta = beta
        self.mde = mde
        self.data_points = []

    def add_observation(self, variant, outcome):
        self.data_points.append({'variant': variant, 'outcome': outcome})

    def should_stop(self):
        if len(self.data_points) < 100:  # Minimum sample size
            return False, "continue"

        # Calculate current test statistic
        control_outcomes = [d['outcome'] for d in self.data_points
                           if d['variant'] == 'control']
        treatment_outcomes = [d['outcome'] for d in self.data_points
                             if d['variant'] == 'treatment']

        if len(control_outcomes) < 50 or len(treatment_outcomes) < 50:
            return False, "continue"

        # Perform t-test
        t_stat, p_value = stats.ttest_ind(treatment_outcomes, control_outcomes)

        # O'Brien-Fleming spending function for alpha adjustment
        current_n = len(self.data_points)
        max_n = self.calculate_max_sample_size()
        information_fraction = current_n / max_n

        adjusted_alpha = self.obf_spending_function(information_fraction)

        if p_value < adjusted_alpha:
            return True, "significant"
        elif current_n >= max_n:
            return True, "max_sample_reached"
        else:
            return False, "continue"
```

## Мониторинг производительности модели

### Детекция дрифта
```python
from scipy.stats import ks_2samp
from scipy.spatial.distance import jensenshannon

class ModelDriftMonitor:
    def __init__(self, baseline_predictions, threshold=0.05):
        self.baseline_predictions = baseline_predictions
        self.threshold = threshold

    def detect_prediction_drift(self, current_predictions):
        # Kolmogorov-Smirnov test for distribution shift
        ks_stat, ks_pvalue = ks_2samp(self.baseline_predictions,
                                     current_predictions)

        # Jensen-Shannon divergence
        js_divergence = jensenshannon(self.baseline_predictions,
                                     current_predictions)

        drift_detected = ks_pvalue < self.threshold or js_divergence > 0.1

        return {
            'drift_detected': drift_detected,
            'ks_statistic': ks_stat,
            'ks_pvalue': ks_pvalue,
            'js_divergence': js_divergence
        }
```

## Лучшие практики и рекомендации

### Конфигурация экспериментов
- Используйте конфигурационные файлы для управления параметрами экспериментов
- Реализуйте правильное логирование всех предсказаний модели
- Настройте автоматические уведомления для снижения производительности
- Поддерживайте отдельные окружения для разработки и продакшена

### Анализ и отчетность
- Всегда сообщайте доверительные интервалы, а не только точечные оценки
- Включайте как практическую, так и статистическую значимость
- Выполняйте проверки устойчивости с различными подходами
- Документируйте нарушения предположений и их влияние

### Типичные ошибки
- Не заглядывайте в результаты без корректировки множественного тестирования
- Избегайте изменения параметров эксперимента в процессе
- Не игнорируйте различия в задержке модели
- Убедитесь, что единица рандомизации соответствует единице анализа
