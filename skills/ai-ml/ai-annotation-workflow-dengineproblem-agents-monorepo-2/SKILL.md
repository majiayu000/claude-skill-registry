---
name: ai-annotation-workflow
description: Эксперт по data annotation. Используй для ML labeling, annotation workflows и quality control.
---

# AI Annotation Workflow Expert

Эксперт по проектированию и управлению процессами разметки данных для машинного обучения.

## Основные принципы

### Цикл разметки данных
1. **Планирование**: Определение задачи, создание guidelines
2. **Пилот**: Тестирование с малой выборкой
3. **Масштабирование**: Расширение на полный датасет
4. **Контроль качества**: Постоянный мониторинг
5. **Итерация**: Улучшение на основе обратной связи

### Типы задач разметки
- **Классификация**: Категоризация данных
- **Детекция объектов**: Bounding boxes
- **Сегментация**: Пиксельная разметка
- **NER**: Named Entity Recognition
- **Sentiment**: Анализ тональности
- **Транскрипция**: Аудио в текст

## Создание Guidelines

### Структура документа
```markdown
# Annotation Guidelines v1.0

## Задача
Разметка изображений товаров для e-commerce

## Категории
1. Одежда
   - Верхняя одежда
   - Нижняя одежда
   - Аксессуары

2. Электроника
   - Смартфоны
   - Ноутбуки
   - Аксессуары

## Правила разметки
- Выбирайте наиболее специфичную категорию
- При неопределённости используйте "Другое"
- Один объект = одна категория

## Примеры
[Примеры с изображениями и правильной разметкой]

## Edge Cases
- Товар частично виден: размечайте если >50% видно
- Несколько товаров: размечайте каждый отдельно
```

## Метрики качества

### Inter-Annotator Agreement (IAA)
```python
from sklearn.metrics import cohen_kappa_score, fleiss_kappa

def calculate_agreement(annotations_a, annotations_b):
    """Расчёт согласованности между аннотаторами"""

    # Cohen's Kappa для двух аннотаторов
    kappa = cohen_kappa_score(annotations_a, annotations_b)

    # Интерпретация
    if kappa < 0.20:
        interpretation = "Poor"
    elif kappa < 0.40:
        interpretation = "Fair"
    elif kappa < 0.60:
        interpretation = "Moderate"
    elif kappa < 0.80:
        interpretation = "Good"
    else:
        interpretation = "Excellent"

    return {
        'kappa': kappa,
        'interpretation': interpretation
    }
```

### Quality Metrics
```python
class AnnotationQualityMonitor:
    def __init__(self):
        self.metrics = []

    def calculate_metrics(self, annotations, gold_standard):
        """Расчёт метрик качества относительно эталона"""

        from sklearn.metrics import precision_score, recall_score, f1_score

        precision = precision_score(gold_standard, annotations, average='weighted')
        recall = recall_score(gold_standard, annotations, average='weighted')
        f1 = f1_score(gold_standard, annotations, average='weighted')

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'accuracy': sum(a == g for a, g in zip(annotations, gold_standard)) / len(annotations)
        }

    def detect_drift(self, window_size=100):
        """Обнаружение дрифта качества"""

        if len(self.metrics) < window_size * 2:
            return False

        recent = self.metrics[-window_size:]
        previous = self.metrics[-window_size*2:-window_size]

        recent_avg = sum(m['f1'] for m in recent) / len(recent)
        previous_avg = sum(m['f1'] for m in previous) / len(previous)

        # Дрифт если падение > 5%
        return (previous_avg - recent_avg) / previous_avg > 0.05
```

## Workflow автоматизации

### Label Studio интеграция
```python
from label_studio_sdk import Client

class AnnotationPipeline:
    def __init__(self, api_key, url):
        self.client = Client(url=url, api_key=api_key)

    def create_project(self, name, label_config):
        """Создание проекта разметки"""

        project = self.client.create_project(
            title=name,
            label_config=label_config
        )
        return project

    def import_tasks(self, project_id, data):
        """Импорт задач для разметки"""

        project = self.client.get_project(project_id)
        project.import_tasks(data)

    def export_annotations(self, project_id, format='JSON'):
        """Экспорт готовых аннотаций"""

        project = self.client.get_project(project_id)
        return project.export_tasks(format=format)
```

### Active Learning Pipeline
```python
class ActiveLearningAnnotation:
    def __init__(self, model, unlabeled_pool):
        self.model = model
        self.unlabeled_pool = unlabeled_pool
        self.labeled_data = []

    def select_samples_for_annotation(self, n_samples=100, strategy='uncertainty'):
        """Выбор образцов для разметки"""

        if strategy == 'uncertainty':
            # Выбор образцов с наибольшей неопределённостью
            predictions = self.model.predict_proba(self.unlabeled_pool)
            uncertainties = -np.sum(predictions * np.log(predictions + 1e-10), axis=1)
            indices = np.argsort(uncertainties)[-n_samples:]

        elif strategy == 'diversity':
            # Выбор разнообразных образцов
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=n_samples)
            kmeans.fit(self.unlabeled_pool)
            indices = [
                np.argmin(np.linalg.norm(self.unlabeled_pool - center, axis=1))
                for center in kmeans.cluster_centers_
            ]

        return self.unlabeled_pool[indices]

    def update_model(self, new_annotations):
        """Обновление модели после получения аннотаций"""

        self.labeled_data.extend(new_annotations)
        X = [item['features'] for item in self.labeled_data]
        y = [item['label'] for item in self.labeled_data]
        self.model.fit(X, y)
```

## Управление аннотаторами

### Онбординг
```python
class AnnotatorOnboarding:
    def __init__(self, gold_standard_samples):
        self.gold_standard = gold_standard_samples
        self.passing_threshold = 0.85

    def run_qualification_test(self, annotator_id, annotations):
        """Квалификационный тест для новых аннотаторов"""

        correct = sum(
            a == g for a, g in zip(annotations, self.gold_standard)
        )
        accuracy = correct / len(self.gold_standard)

        return {
            'annotator_id': annotator_id,
            'accuracy': accuracy,
            'passed': accuracy >= self.passing_threshold,
            'errors': [
                {'index': i, 'expected': g, 'actual': a}
                for i, (a, g) in enumerate(zip(annotations, self.gold_standard))
                if a != g
            ]
        }
```

### Мониторинг производительности
```python
class AnnotatorPerformanceTracker:
    def __init__(self):
        self.annotator_stats = {}

    def log_annotation(self, annotator_id, task_id, time_spent, quality_score):
        if annotator_id not in self.annotator_stats:
            self.annotator_stats[annotator_id] = []

        self.annotator_stats[annotator_id].append({
            'task_id': task_id,
            'time_spent': time_spent,
            'quality_score': quality_score,
            'timestamp': datetime.now()
        })

    def get_annotator_report(self, annotator_id):
        stats = self.annotator_stats.get(annotator_id, [])

        if not stats:
            return None

        return {
            'total_tasks': len(stats),
            'avg_time': sum(s['time_spent'] for s in stats) / len(stats),
            'avg_quality': sum(s['quality_score'] for s in stats) / len(stats),
            'tasks_per_hour': len(stats) / (
                (stats[-1]['timestamp'] - stats[0]['timestamp']).total_seconds() / 3600
            ) if len(stats) > 1 else 0
        }
```

## Инструменты разметки

### Популярные платформы
- **Label Studio**: Open-source, гибкая конфигурация
- **Labelbox**: Enterprise, ML-assisted labeling
- **Scale AI**: Managed workforce
- **Amazon SageMaker Ground Truth**: AWS интеграция
- **Prodigy**: NLP-focused, active learning

### Выбор инструмента
| Критерий | Label Studio | Labelbox | Scale AI |
|----------|--------------|----------|----------|
| Стоимость | Free/Open | $$ | $$$ |
| Workforce | Self-managed | Optional | Included |
| ML Assist | Basic | Advanced | Advanced |
| Customization | High | Medium | Low |

## Лучшие практики

1. **Начинайте с пилота** — 100-200 образцов для калибровки
2. **Итерируйте guidelines** — обновляйте по мере обнаружения edge cases
3. **Используйте gold standard** — 5-10% данных для контроля качества
4. **Балансируйте скорость и качество** — не давите на аннотаторов
5. **Документируйте решения** — записывайте все разъяснения
6. **Автоматизируйте что можно** — pre-labeling, validation rules
