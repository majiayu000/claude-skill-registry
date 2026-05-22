---
name: categorical-encoder
description: Эксперт categorical encoding. Используй для ML feature engineering, one-hot, target encoding и embeddings.
---

# Categorical Encoder Expert

Эксперт по кодированию категориальных переменных для машинного обучения.

## Выбор на основе кардинальности

| Кардинальность | Рекомендация |
|----------------|--------------|
| Низкая (<10) | One-hot, Dummy |
| Средняя (10-50) | Target, Frequency, Binary |
| Высокая (>50) | Hash, Embeddings |
| Порядковая | Ordinal |

## One-Hot Encoding

```python
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# Для pandas
df_encoded = pd.get_dummies(df, columns=['category_col'], prefix='cat')

# Для sklearn
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_train_encoded = encoder.fit_transform(X_train[['category_col']])
X_test_encoded = encoder.transform(X_test[['category_col']])

# Получить названия признаков
feature_names = encoder.get_feature_names_out(['category_col'])
```

## Target Encoding с кросс-валидацией

```python
from sklearn.model_selection import KFold
import numpy as np

def target_encode_cv(X, y, column, n_splits=5, alpha=1.0):
    """
    Target кодирование с CV для предотвращения переобучения
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    encoded = np.zeros(len(X))
    global_mean = y.mean()

    for train_idx, val_idx in kf.split(X):
        # Вычислить средние на тренировочной выборке
        category_means = y.iloc[train_idx].groupby(
            X[column].iloc[train_idx]
        ).mean()

        # Байесовское сглаживание
        category_counts = X[column].iloc[train_idx].value_counts()
        smoothed_means = (
            category_counts * category_means + alpha * global_mean
        ) / (category_counts + alpha)

        # Закодировать валидационную выборку
        encoded[val_idx] = X[column].iloc[val_idx].map(
            smoothed_means
        ).fillna(global_mean)

    return encoded
```

## Binary Encoding

```python
import category_encoders as ce

# Binary кодирование уменьшает размерность
binary_encoder = ce.BinaryEncoder(cols=['high_cardinality_col'])
X_train_binary = binary_encoder.fit_transform(X_train)
X_test_binary = binary_encoder.transform(X_test)

# Для 100 категорий: one-hot = 100, binary = 7 признаков
print(f"Исходных категорий: {X_train['col'].nunique()}")
print(f"Binary признаков: {len([c for c in X_train_binary.columns if 'col' in c])}")
```

## Frequency и Count Encoding

```python
def frequency_encode(train_series, test_series=None):
    """Кодирование по частоте появления"""
    freq_map = train_series.value_counts(normalize=True).to_dict()
    train_encoded = train_series.map(freq_map)

    if test_series is not None:
        test_encoded = test_series.map(freq_map).fillna(0)
        return train_encoded, test_encoded
    return train_encoded

def count_encode(train_series, test_series=None):
    """Кодирование по количеству"""
    count_map = train_series.value_counts().to_dict()
    train_encoded = train_series.map(count_map)

    if test_series is not None:
        test_encoded = test_series.map(count_map).fillna(0)
        return train_encoded, test_encoded
    return train_encoded
```

## Embeddings для высокой кардинальности

```python
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import OneHotEncoder

def create_categorical_embeddings(X_train, X_test, column, n_components=10):
    """Создать эмбеддинги из one-hot"""
    # One-hot кодирование
    encoder = OneHotEncoder(sparse_output=True, handle_unknown='ignore')
    X_train_oh = encoder.fit_transform(X_train[[column]])
    X_test_oh = encoder.transform(X_test[[column]])

    # Понижение размерности
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    X_train_emb = svd.fit_transform(X_train_oh)
    X_test_emb = svd.transform(X_test_oh)

    return X_train_emb, X_test_emb, encoder, svd
```

## Multiple Encoding Strategy

```python
def multi_encode_categorical(df, column, target=None):
    """Создать множественные кодирования"""
    encodings = {}

    # Frequency
    encodings[f'{column}_freq'] = frequency_encode(df[column])

    # Count
    encodings[f'{column}_count'] = count_encode(df[column])

    # Target (если есть)
    if target is not None:
        encodings[f'{column}_target'] = target_encode_cv(df, target, column)

    # Ordinal для древесных моделей
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    encodings[f'{column}_ordinal'] = le.fit_transform(df[column])

    return pd.DataFrame(encodings)
```

## Production-ready Encoder

```python
class RobustCategoricalEncoder:
    def __init__(self, encoding_type='onehot', handle_unknown='mode'):
        self.encoding_type = encoding_type
        self.handle_unknown = handle_unknown
        self.encoders = {}
        self.fallback_values = {}

    def fit(self, X, y=None):
        for column in X.select_dtypes(include=['object', 'category']).columns:
            if self.encoding_type == 'onehot':
                encoder = OneHotEncoder(
                    sparse_output=False,
                    handle_unknown='ignore'
                )
                encoder.fit(X[[column]])
                self.encoders[column] = encoder

            elif self.encoding_type == 'target' and y is not None:
                target_map = y.groupby(X[column]).mean().to_dict()
                self.encoders[column] = target_map
                self.fallback_values[column] = y.mean()

        return self

    def transform(self, X):
        X_transformed = X.copy()

        for column, encoder in self.encoders.items():
            if self.encoding_type == 'onehot':
                encoded = encoder.transform(X_transformed[[column]])
                feature_names = encoder.get_feature_names_out([column])
                encoded_df = pd.DataFrame(
                    encoded,
                    columns=feature_names,
                    index=X.index
                )
                X_transformed = pd.concat([
                    X_transformed.drop(column, axis=1),
                    encoded_df
                ], axis=1)

            elif self.encoding_type == 'target':
                X_transformed[column] = X_transformed[column].map(
                    encoder
                ).fillna(self.fallback_values[column])

        return X_transformed
```

## Рекомендации для моделей

| Модель | Рекомендуемое кодирование |
|--------|---------------------------|
| Древесные (RF, XGB) | Ordinal, Target, Frequency |
| Линейные (LR, SVM) | One-hot, избегать ordinal |
| Нейронные сети | Embeddings для высокой кардинальности |
| На основе расстояния | Стандартизированные закодированные |

## Предотвращение утечки данных

```python
# ПРАВИЛЬНО: fit только на train
encoder.fit(X_train)
X_train_enc = encoder.transform(X_train)
X_test_enc = encoder.transform(X_test)

# НЕПРАВИЛЬНО: fit на всех данных
encoder.fit(X_all)  # Утечка!
```

## Валидация

```python
def validate_encoding(X_original, X_encoded):
    """Валидировать результаты кодирования"""
    print(f"Исходная размерность: {X_original.shape}")
    print(f"Закодированная размерность: {X_encoded.shape}")
    print(f"Память: {X_encoded.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Проверить NaN
    null_count = X_encoded.isnull().sum().sum()
    if null_count > 0:
        print(f"Предупреждение: {null_count} пустых значений")

    # Коэффициент расширения
    print(f"Расширение: {X_encoded.shape[1] / X_original.shape[1]:.2f}x")
```

## Лучшие практики

1. **Fit только на train** — избегайте утечки данных
2. **Обрабатывайте unknown** — используйте fallback стратегию
3. **Используйте CV для target encoding** — предотвращает переобучение
4. **Мониторьте размерность** — one-hot взрывает размерность
5. **Выбирайте по модели** — разные модели предпочитают разное
