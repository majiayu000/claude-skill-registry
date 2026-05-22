---
name: ml-supply-chain
description: When the user wants to apply machine learning to supply chain problems, build ML models, or use AI for predictions. Also use when the user mentions "machine learning," "deep learning," "neural networks," "AI supply chain," "predictive models," "classification models," "regression models," "anomaly detection," "computer vision," or "NLP for supply chain." For traditional forecasting, see demand-forecasting. For optimization, see optimization-modeling.
---

# Machine Learning for Supply Chain

You are an expert in applying machine learning and artificial intelligence to supply chain problems. Your goal is to help build, train, and deploy ML models that improve forecasting, classification, optimization, and decision-making across supply chain operations.

## Initial Assessment

Before applying ML to supply chain problems, understand:

1. **Business Problem**
   - What problem needs solving? (demand forecasting, quality prediction, route optimization)
   - What decisions will ML model support?
   - Current approach and its limitations?
   - Expected improvement and ROI?

2. **Data Availability**
   - What data is available? (structured, unstructured, images, text)
   - Historical data quantity? (ML typically needs 1000+ samples)
   - Data quality? (missing values, outliers, noise)
   - Feature availability? (predictive variables)
   - Real-time data access?

3. **ML Problem Type**
   - Supervised learning? (labeled data available)
   - Unsupervised learning? (clustering, anomaly detection)
   - Reinforcement learning? (sequential decision-making)
   - Time series forecasting?

4. **Technical Environment**
   - ML expertise in team?
   - Computational resources? (CPU, GPU, cloud)
   - Deployment environment? (batch, real-time API, edge)
   - MLOps capabilities?

---

## ML Problem Types in Supply Chain

### Supervised Learning

**Regression (Continuous Output)**
- Demand forecasting
- Lead time prediction
- Price optimization
- Inventory level prediction
- Delivery time estimation

**Classification (Categorical Output)**
- Product categorization
- Supplier risk classification
- Quality defect detection
- Shipment delay prediction (on-time vs. late)
- Customer churn prediction

### Unsupervised Learning

**Clustering**
- Customer segmentation
- Product grouping
- Route clustering
- Anomaly detection in operations

**Dimensionality Reduction**
- Feature extraction
- Data visualization
- Noise reduction

### Reinforcement Learning

**Sequential Decision-Making**
- Inventory control policies
- Dynamic pricing
- Warehouse robot navigation
- Order dispatching

---

## Demand Forecasting with ML

### Feature Engineering for Demand Forecasting

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_demand_features(df, target_col='demand'):
    """
    Create comprehensive feature set for demand forecasting

    df: DataFrame with columns ['date', 'sku', 'demand']
    """

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['sku', 'date'])

    # Time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_month_start'] = df['date'].dt.is_month_start.astype(int)
    df['is_month_end'] = df['date'].dt.is_month_end.astype(int)

    # Lag features (previous demand)
    for lag in [1, 7, 14, 28, 365]:
        df[f'lag_{lag}'] = df.groupby('sku')[target_col].shift(lag)

    # Rolling statistics
    for window in [7, 14, 28, 90]:
        df[f'rolling_mean_{window}'] = (
            df.groupby('sku')[target_col]
            .rolling(window, min_periods=1)
            .mean()
            .reset_index(0, drop=True)
        )

        df[f'rolling_std_{window}'] = (
            df.groupby('sku')[target_col]
            .rolling(window, min_periods=1)
            .std()
            .reset_index(0, drop=True)
        )

        df[f'rolling_min_{window}'] = (
            df.groupby('sku')[target_col]
            .rolling(window, min_periods=1)
            .min()
            .reset_index(0, drop=True)
        )

        df[f'rolling_max_{window}'] = (
            df.groupby('sku')[target_col]
            .rolling(window, min_periods=1)
            .max()
            .reset_index(0, drop=True)
        )

    # Exponential weighted moving average
    df['ewm_7'] = (
        df.groupby('sku')[target_col]
        .transform(lambda x: x.ewm(span=7).mean())
    )

    df['ewm_28'] = (
        df.groupby('sku')[target_col]
        .transform(lambda x: x.ewm(span=28).mean())
    )

    # Trend features
    df['demand_trend_7'] = df[f'lag_7'] - df[f'lag_14']
    df['demand_trend_28'] = df[f'lag_28'] - df[f'lag_56']

    # Cyclical encoding for seasonal features
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

    return df

# Example usage
demand_df = pd.DataFrame({
    'date': pd.date_range('2022-01-01', '2024-12-31', freq='D'),
    'sku': 'SKU_001',
    'demand': np.random.poisson(100, 1096)
})

features_df = create_demand_features(demand_df)
print(f"Features created: {len(features_df.columns)} columns")
```

### Gradient Boosting for Demand Forecasting

```python
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

class MLDemandForecaster:
    """
    Machine learning demand forecasting using gradient boosting
    """

    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_importance = None

    def prepare_data(self, df, target_col='demand', test_size=90):
        """
        Prepare train/test split for time series

        test_size: number of days to hold out for testing
        """

        # Remove rows with NaN (due to lag features)
        df_clean = df.dropna()

        # Identify feature columns (exclude date, sku, target)
        feature_cols = [col for col in df_clean.columns
                       if col not in ['date', 'sku', target_col]]

        # Time-based split
        split_date = df_clean['date'].max() - timedelta(days=test_size)

        train = df_clean[df_clean['date'] <= split_date]
        test = df_clean[df_clean['date'] > split_date]

        X_train = train[feature_cols]
        y_train = train[target_col]
        X_test = test[feature_cols]
        y_test = test[target_col]

        return X_train, X_test, y_train, y_test, feature_cols

    def train(self, X_train, y_train, params=None):
        """
        Train gradient boosting model
        """

        if self.model_type == 'xgboost':
            default_params = {
                'objective': 'reg:squarederror',
                'n_estimators': 1000,
                'learning_rate': 0.05,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42,
                'early_stopping_rounds': 50
            }

            if params:
                default_params.update(params)

            self.model = xgb.XGBRegressor(**default_params)

        elif self.model_type == 'lightgbm':
            default_params = {
                'objective': 'regression',
                'n_estimators': 1000,
                'learning_rate': 0.05,
                'num_leaves': 31,
                'feature_fraction': 0.8,
                'bagging_fraction': 0.8,
                'bagging_freq': 5,
                'random_state': 42
            }

            if params:
                default_params.update(params)

            self.model = lgb.LGBMRegressor(**default_params)

        # Train
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train)],
            verbose=100
        )

        # Store feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        """

        y_pred = self.predict(X_test)

        metrics = {
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'MAPE': np.mean(np.abs((y_test - y_pred) / y_test)) * 100,
            'Bias': np.mean(y_pred - y_test)
        }

        return metrics, y_pred

    def plot_results(self, y_test, y_pred, dates=None):
        """
        Visualize predictions vs actuals
        """

        fig, axes = plt.subplots(2, 1, figsize=(14, 8))

        # Time series plot
        if dates is not None:
            axes[0].plot(dates, y_test.values, label='Actual', linewidth=2)
            axes[0].plot(dates, y_pred, label='Predicted', linewidth=2, alpha=0.7)
        else:
            axes[0].plot(y_test.values, label='Actual', linewidth=2)
            axes[0].plot(y_pred, label='Predicted', linewidth=2, alpha=0.7)

        axes[0].set_title('Demand Forecast: Actual vs Predicted')
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Demand')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Scatter plot
        axes[1].scatter(y_test, y_pred, alpha=0.5)
        axes[1].plot([y_test.min(), y_test.max()],
                     [y_test.min(), y_test.max()],
                     'r--', linewidth=2, label='Perfect Prediction')
        axes[1].set_xlabel('Actual Demand')
        axes[1].set_ylabel('Predicted Demand')
        axes[1].set_title('Prediction Accuracy')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def plot_feature_importance(self, top_n=20):
        """
        Plot feature importance
        """

        top_features = self.feature_importance.head(top_n)

        plt.figure(figsize=(10, 8))
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance')
        plt.title(f'Top {top_n} Feature Importance')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

# Example usage
forecaster = MLDemandForecaster(model_type='xgboost')

# Prepare data
X_train, X_test, y_train, y_test, feature_cols = forecaster.prepare_data(
    features_df,
    test_size=90
)

# Train model
forecaster.train(X_train, y_train)

# Evaluate
metrics, y_pred = forecaster.evaluate(X_test, y_test)

print("\nModel Performance:")
for metric, value in metrics.items():
    print(f"{metric}: {value:.2f}")

# Visualize
test_dates = features_df[features_df['date'] > features_df['date'].max() - timedelta(days=90)]['date']
forecaster.plot_results(y_test, y_pred, dates=test_dates)
forecaster.plot_feature_importance(top_n=20)
```

### Deep Learning with LSTM

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler

class LSTMForecaster:
    """
    LSTM neural network for demand forecasting
    """

    def __init__(self, lookback=30, forecast_horizon=7):
        """
        lookback: number of historical time steps to use
        forecast_horizon: number of future steps to predict
        """
        self.lookback = lookback
        self.forecast_horizon = forecast_horizon
        self.model = None
        self.scaler = StandardScaler()

    def create_sequences(self, data, target):
        """
        Create sequences for LSTM training

        data: feature array
        target: target array
        """
        X, y = [], []

        for i in range(len(data) - self.lookback - self.forecast_horizon + 1):
            X.append(data[i:i + self.lookback])
            y.append(target[i + self.lookback:i + self.lookback + self.forecast_horizon])

        return np.array(X), np.array(y)

    def build_model(self, n_features):
        """
        Build LSTM architecture
        """

        model = keras.Sequential([
            # First LSTM layer
            layers.LSTM(128, activation='relu',
                       return_sequences=True,
                       input_shape=(self.lookback, n_features)),
            layers.Dropout(0.2),

            # Second LSTM layer
            layers.LSTM(64, activation='relu',
                       return_sequences=True),
            layers.Dropout(0.2),

            # Third LSTM layer
            layers.LSTM(32, activation='relu'),
            layers.Dropout(0.2),

            # Dense layers
            layers.Dense(32, activation='relu'),
            layers.Dense(self.forecast_horizon)
        ])

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        return model

    def train(self, train_data, train_target, val_split=0.2, epochs=100, batch_size=32):
        """
        Train LSTM model
        """

        # Scale data
        train_data_scaled = self.scaler.fit_transform(train_data)

        # Create sequences
        X_seq, y_seq = self.create_sequences(train_data_scaled, train_target)

        print(f"Sequence shape: X={X_seq.shape}, y={y_seq.shape}")

        # Build model
        self.model = self.build_model(n_features=train_data.shape[1])

        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True
        )

        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001
        )

        # Train
        history = self.model.fit(
            X_seq, y_seq,
            validation_split=val_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )

        return history

    def predict(self, data):
        """
        Make predictions
        """

        # Scale data
        data_scaled = self.scaler.transform(data)

        # Create sequences
        X_seq, _ = self.create_sequences(
            data_scaled,
            np.zeros(len(data))  # Dummy target
        )

        # Predict
        predictions = self.model.predict(X_seq)

        return predictions

# Example usage
lstm_forecaster = LSTMForecaster(lookback=30, forecast_horizon=7)

# Prepare data for LSTM
feature_cols = [col for col in features_df.columns
               if col not in ['date', 'sku', 'demand']]

train_data = features_df[feature_cols].values[:900]
train_target = features_df['demand'].values[:900]

# Train
history = lstm_forecaster.train(train_data, train_target, epochs=50)

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Model MAE')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend()

plt.tight_layout()
plt.show()
```

---

## Classification Problems

### Shipment Delay Prediction

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import seaborn as sns

class ShipmentDelayPredictor:
    """
    Predict whether shipment will be delayed
    """

    def __init__(self):
        self.model = None
        self.feature_cols = None

    def prepare_features(self, shipments_df):
        """
        Create features for delay prediction

        shipments_df: columns = ['shipment_id', 'origin', 'destination',
                                 'carrier', 'mode', 'distance', 'weight',
                                 'weather_conditions', 'ship_date', 'promised_date',
                                 'actual_delivery_date']
        """

        df = shipments_df.copy()

        # Create target: delayed = 1, on-time = 0
        df['delayed'] = (df['actual_delivery_date'] > df['promised_date']).astype(int)

        # Temporal features
        df['ship_day_of_week'] = df['ship_date'].dt.dayofweek
        df['ship_month'] = df['ship_date'].dt.month
        df['is_weekend'] = (df['ship_day_of_week'] >= 5).astype(int)

        # Transit features
        df['promised_transit_days'] = (df['promised_date'] - df['ship_date']).dt.days
        df['distance_per_day'] = df['distance'] / df['promised_transit_days']

        # Weight categories
        df['weight_category'] = pd.cut(
            df['weight'],
            bins=[0, 1000, 5000, 15000, float('inf')],
            labels=['light', 'medium', 'heavy', 'very_heavy']
        )

        # Carrier historical performance (would need historical data)
        # For demo, create dummy
        df['carrier_reliability'] = df['carrier'].map({
            'Carrier_A': 0.95,
            'Carrier_B': 0.88,
            'Carrier_C': 0.92
        }).fillna(0.90)

        # Weather conditions (categorical)
        df['bad_weather'] = df['weather_conditions'].isin(['rain', 'snow', 'storm']).astype(int)

        # One-hot encode categorical variables
        df_encoded = pd.get_dummies(
            df,
            columns=['origin', 'destination', 'carrier', 'mode', 'weight_category'],
            drop_first=True
        )

        return df_encoded

    def train(self, X_train, y_train):
        """
        Train random forest classifier
        """

        self.feature_cols = X_train.columns

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight='balanced',  # Handle imbalanced classes
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_train, y_train)

        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_cols,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

    def predict(self, X_test):
        """
        Predict delay probability
        """
        return self.model.predict(X_test)

    def predict_proba(self, X_test):
        """
        Predict delay probability
        """
        return self.model.predict_proba(X_test)[:, 1]

    def evaluate(self, X_test, y_test):
        """
        Evaluate classifier performance
        """

        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)

        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.show()

        return {
            'accuracy': (y_pred == y_test).mean(),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }

# Example usage
delay_predictor = ShipmentDelayPredictor()

# Prepare data
shipments_encoded = delay_predictor.prepare_features(shipments_df)

# Split
feature_cols = [col for col in shipments_encoded.columns
               if col not in ['shipment_id', 'ship_date', 'promised_date',
                             'actual_delivery_date', 'delayed']]

X = shipments_encoded[feature_cols]
y = shipments_encoded['delayed']

# Train/test split
split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# Train
delay_predictor.train(X_train, y_train)

# Evaluate
metrics = delay_predictor.evaluate(X_test, y_test)
```

---

## Clustering & Segmentation

### Customer Segmentation

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class CustomerSegmentation:
    """
    Segment customers using clustering
    """

    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.kmeans = None

    def create_customer_features(self, transactions_df):
        """
        Create RFM and other features for segmentation

        transactions_df: columns = ['customer_id', 'order_date',
                                    'order_value', 'quantity']
        """

        # Calculate RFM metrics
        reference_date = transactions_df['order_date'].max()

        rfm = transactions_df.groupby('customer_id').agg({
            'order_date': lambda x: (reference_date - x.max()).days,  # Recency
            'customer_id': 'count',  # Frequency
            'order_value': 'sum'  # Monetary
        })

        rfm.columns = ['recency', 'frequency', 'monetary']

        # Additional features
        customer_features = transactions_df.groupby('customer_id').agg({
            'order_value': ['mean', 'std', 'min', 'max'],
            'quantity': ['mean', 'sum']
        })

        customer_features.columns = [
            'avg_order_value', 'std_order_value', 'min_order_value', 'max_order_value',
            'avg_quantity', 'total_quantity'
        ]

        # Combine
        features = rfm.join(customer_features)

        return features

    def fit(self, features_df):
        """
        Fit clustering model
        """

        # Scale features
        features_scaled = self.scaler.fit_transform(features_df)

        # Fit K-means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10
        )

        clusters = self.kmeans.fit_predict(features_scaled)

        # Add cluster labels
        features_df['cluster'] = clusters

        return features_df

    def visualize_clusters(self, features_df):
        """
        Visualize clusters using PCA
        """

        # Get features without cluster column
        feature_cols = [col for col in features_df.columns if col != 'cluster']
        X = features_df[feature_cols]

        # Scale and apply PCA
        X_scaled = self.scaler.transform(X)
        X_pca = self.pca.fit_transform(X_scaled)

        # Plot
        plt.figure(figsize=(12, 8))

        for cluster in range(self.n_clusters):
            mask = features_df['cluster'] == cluster
            plt.scatter(
                X_pca[mask, 0],
                X_pca[mask, 1],
                label=f'Cluster {cluster}',
                s=100,
                alpha=0.6
            )

        # Plot centroids
        centroids_scaled = self.kmeans.cluster_centers_
        centroids_pca = self.pca.transform(centroids_scaled)

        plt.scatter(
            centroids_pca[:, 0],
            centroids_pca[:, 1],
            marker='X',
            s=500,
            c='red',
            edgecolors='black',
            linewidths=2,
            label='Centroids'
        )

        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.title('Customer Segmentation')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def profile_clusters(self, features_df):
        """
        Create cluster profiles
        """

        # Calculate mean for each cluster
        profiles = features_df.groupby('cluster').mean()

        # Add cluster size
        profiles['size'] = features_df.groupby('cluster').size()

        # Name clusters based on characteristics
        def name_cluster(row):
            if row['frequency'] > profiles['frequency'].median() and \
               row['monetary'] > profiles['monetary'].median():
                return 'Champions'
            elif row['recency'] < profiles['recency'].median() and \
                 row['frequency'] > profiles['frequency'].median():
                return 'Loyal'
            elif row['recency'] > profiles['recency'].median() and \
                 row['frequency'] < profiles['frequency'].median():
                return 'At Risk'
            else:
                return 'Potential'

        profiles['segment_name'] = profiles.apply(name_cluster, axis=1)

        return profiles

# Example usage
segmentation = CustomerSegmentation(n_clusters=4)

# Create features
customer_features = segmentation.create_customer_features(transactions_df)

# Fit clustering
clustered_customers = segmentation.fit(customer_features)

# Visualize
segmentation.visualize_clusters(clustered_customers)

# Profile clusters
cluster_profiles = segmentation.profile_clusters(clustered_customers)
print(cluster_profiles)
```

---

## Computer Vision for Supply Chain

### Quality Inspection with CNNs

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class QualityInspectionModel:
    """
    Convolutional Neural Network for quality defect detection
    """

    def __init__(self, image_size=(224, 224), num_classes=2):
        """
        image_size: input image dimensions
        num_classes: number of defect categories (e.g., good, defective)
        """
        self.image_size = image_size
        self.num_classes = num_classes
        self.model = None

    def build_model(self):
        """
        Build CNN architecture
        """

        model = models.Sequential([
            # Convolutional layers
            layers.Conv2D(32, (3, 3), activation='relu',
                         input_shape=(*self.image_size, 3)),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),

            # Flatten and dense layers
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def use_transfer_learning(self, base_model_name='VGG16'):
        """
        Use pre-trained model with transfer learning
        """

        # Load pre-trained model
        if base_model_name == 'VGG16':
            base_model = tf.keras.applications.VGG16(
                input_shape=(*self.image_size, 3),
                include_top=False,
                weights='imagenet'
            )
        elif base_model_name == 'ResNet50':
            base_model = tf.keras.applications.ResNet50(
                input_shape=(*self.image_size, 3),
                include_top=False,
                weights='imagenet'
            )

        # Freeze base model
        base_model.trainable = False

        # Add custom top layers
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def train(self, train_dir, val_dir, epochs=50, batch_size=32,
             use_transfer_learning=True):
        """
        Train model on image data

        train_dir: directory with training images organized by class
        val_dir: directory with validation images
        """

        # Data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

        val_datagen = ImageDataGenerator(rescale=1./255)

        # Load data
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.image_size,
            batch_size=batch_size,
            class_mode='categorical'
        )

        val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=self.image_size,
            batch_size=batch_size,
            class_mode='categorical'
        )

        # Build model
        if use_transfer_learning:
            self.model = self.use_transfer_learning()
        else:
            self.model = self.build_model()

        # Callbacks
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )

        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
            'best_quality_model.h5',
            monitor='val_accuracy',
            save_best_only=True
        )

        # Train
        history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=val_generator,
            callbacks=[early_stopping, model_checkpoint]
        )

        return history

    def predict_defects(self, image_path):
        """
        Predict defects in single image
        """

        # Load and preprocess image
        img = tf.keras.preprocessing.image.load_img(
            image_path,
            target_size=self.image_size
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Predict
        predictions = self.model.predict(img_array)

        return predictions[0]

# Example usage
quality_model = QualityInspectionModel(image_size=(224, 224), num_classes=2)

# Train model
# history = quality_model.train(
#     train_dir='data/train',
#     val_dir='data/val',
#     epochs=30,
#     use_transfer_learning=True
# )

# Predict on new image
# predictions = quality_model.predict_defects('path/to/product_image.jpg')
# print(f"Defect probability: {predictions[1]:.2%}")
```

---

## Natural Language Processing

### Supplier Risk Analysis from News

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import requests

class SupplierRiskNLP:
    """
    Analyze supplier risk from news articles and reports
    """

    def __init__(self):
        # Load sentiment analysis model
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

        # Load NER model for entity extraction
        self.ner_analyzer = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )

    def fetch_news(self, supplier_name, api_key):
        """
        Fetch news articles about supplier

        Uses News API (newsapi.org)
        """

        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': supplier_name,
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 100
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            articles = response.json()['articles']
            return articles
        else:
            return []

    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text
        """

        # Split long text into chunks (model has token limit)
        max_length = 512
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]

        sentiments = []
        for chunk in chunks:
            result = self.sentiment_analyzer(chunk)[0]
            sentiments.append(result)

        # Aggregate sentiments
        positive_count = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
        avg_score = np.mean([s['score'] for s in sentiments])

        overall = {
            'positive_ratio': positive_count / len(sentiments),
            'average_confidence': avg_score,
            'risk_indicator': 1 - (positive_count / len(sentiments))
        }

        return overall

    def extract_risk_indicators(self, articles):
        """
        Extract risk-related keywords and entities
        """

        risk_keywords = [
            'bankruptcy', 'lawsuit', 'recall', 'defect', 'violation',
            'investigation', 'scandal', 'delay', 'shortage', 'disruption',
            'closure', 'layoff', 'protest', 'strike'
        ]

        risk_score = 0
        risk_events = []

        for article in articles:
            text = article.get('title', '') + ' ' + article.get('description', '')
            text_lower = text.lower()

            # Check for risk keywords
            for keyword in risk_keywords:
                if keyword in text_lower:
                    risk_score += 1
                    risk_events.append({
                        'keyword': keyword,
                        'title': article.get('title'),
                        'date': article.get('publishedAt'),
                        'url': article.get('url')
                    })

        return risk_score, risk_events

    def assess_supplier_risk(self, supplier_name, api_key):
        """
        Complete supplier risk assessment
        """

        print(f"Assessing risk for supplier: {supplier_name}")

        # Fetch news
        articles = self.fetch_news(supplier_name, api_key)
        print(f"Found {len(articles)} articles")

        if not articles:
            return {
                'supplier': supplier_name,
                'risk_level': 'Unknown',
                'score': 0,
                'message': 'No articles found'
            }

        # Analyze sentiment
        all_text = ' '.join([
            art.get('title', '') + ' ' + art.get('description', '')
            for art in articles
        ])

        sentiment = self.analyze_sentiment(all_text)

        # Extract risk indicators
        risk_score, risk_events = self.extract_risk_indicators(articles)

        # Calculate overall risk
        # Higher risk_indicator and higher risk_score = higher risk
        overall_risk_score = (sentiment['risk_indicator'] * 0.6 +
                             min(risk_score / len(articles), 1.0) * 0.4)

        if overall_risk_score > 0.7:
            risk_level = 'HIGH'
        elif overall_risk_score > 0.4:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return {
            'supplier': supplier_name,
            'risk_level': risk_level,
            'risk_score': overall_risk_score,
            'sentiment_analysis': sentiment,
            'risk_keyword_count': risk_score,
            'risk_events': risk_events[:5],  # Top 5 events
            'articles_analyzed': len(articles)
        }

# Example usage
risk_analyzer = SupplierRiskNLP()

# Assess supplier risk
# assessment = risk_analyzer.assess_supplier_risk('Acme Corp', api_key='your_api_key')
# print(f"Risk Level: {assessment['risk_level']}")
# print(f"Risk Score: {assessment['risk_score']:.2f}")
```

---

## MLOps & Model Deployment

### Model Deployment with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn

app = FastAPI(title="Supply Chain ML API")

# Load pre-trained model
demand_model = joblib.load('demand_forecast_model.pkl')
delay_model = joblib.load('delay_prediction_model.pkl')

# Request models
class DemandForecastRequest(BaseModel):
    sku: str
    features: dict  # Feature dictionary

class DelayPredictionRequest(BaseModel):
    shipment_features: dict

# Response models
class DemandForecastResponse(BaseModel):
    sku: str
    predicted_demand: float
    confidence_interval_lower: float
    confidence_interval_upper: float

class DelayPredictionResponse(BaseModel):
    delay_probability: float
    predicted_class: str
    confidence: float

@app.post("/api/v1/forecast/demand", response_model=DemandForecastResponse)
async def forecast_demand(request: DemandForecastRequest):
    """
    Forecast demand for a SKU
    """
    try:
        # Extract features
        features_array = np.array(list(request.features.values())).reshape(1, -1)

        # Predict
        prediction = demand_model.predict(features_array)[0]

        # Calculate confidence interval (simplified)
        std_dev = prediction * 0.15  # Assume 15% std dev
        ci_lower = max(0, prediction - 1.96 * std_dev)
        ci_upper = prediction + 1.96 * std_dev

        return DemandForecastResponse(
            sku=request.sku,
            predicted_demand=float(prediction),
            confidence_interval_lower=float(ci_lower),
            confidence_interval_upper=float(ci_upper)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/predict/delay", response_model=DelayPredictionResponse)
async def predict_delay(request: DelayPredictionRequest):
    """
    Predict shipment delay probability
    """
    try:
        # Extract features
        features_array = np.array(
            list(request.shipment_features.values())
        ).reshape(1, -1)

        # Predict probability
        delay_proba = delay_model.predict_proba(features_array)[0][1]
        predicted_class = "Delayed" if delay_proba > 0.5 else "On-Time"
        confidence = max(delay_proba, 1 - delay_proba)

        return DelayPredictionResponse(
            delay_probability=float(delay_proba),
            predicted_class=predicted_class,
            confidence=float(confidence)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run with: uvicorn api:app --reload
```

---

## Tools & Libraries

### Python ML Libraries

**Core ML:**
- `scikit-learn`: Classical ML algorithms
- `xgboost`: Gradient boosting
- `lightgbm`: Fast gradient boosting
- `catboost`: Gradient boosting for categorical data

**Deep Learning:**
- `tensorflow`/`keras`: Neural networks
- `pytorch`: Dynamic neural networks
- `fastai`: High-level deep learning

**Time Series:**
- `prophet`: Time series forecasting
- `statsmodels`: Statistical models
- `sktime`: Time series ML
- `darts`: Time series forecasting library

**NLP:**
- `transformers (Hugging Face)`: Pre-trained language models
- `spacy`: Industrial NLP
- `nltk`: Natural language toolkit

**Computer Vision:**
- `opencv`: Computer vision
- `PIL`/`pillow`: Image processing
- `albumentations`: Image augmentation

**Model Deployment:**
- `fastapi`: API framework
- `flask`: Web framework
- `streamlit`: Data apps
- `mlflow`: ML lifecycle management
- `kubeflow`: ML on Kubernetes

### Cloud ML Platforms

**Training & Deployment:**
- **AWS SageMaker**: End-to-end ML platform
- **Google Cloud AI Platform**: ML on GCP
- **Azure Machine Learning**: Microsoft ML platform
- **Databricks**: Unified analytics platform

**MLOps:**
- **MLflow**: Open-source ML lifecycle
- **Weights & Biases**: Experiment tracking
- **Neptune.ai**: ML metadata store
- **DVC**: Data version control

---

## Common Challenges & Solutions

### Challenge: Insufficient Training Data

**Problem:**
- ML needs large datasets (1000+ samples)
- Supply chain data often limited

**Solutions:**
- Use transfer learning from pre-trained models
- Data augmentation techniques
- Synthetic data generation
- Start with simpler models (fewer parameters)
- Combine multiple data sources
- Use semi-supervised or active learning

### Challenge: Imbalanced Classes

**Problem:**
- Rare events (defects, delays) have few examples
- Model biased toward majority class

**Solutions:**
- Class weighting in loss function
- Oversampling minority class (SMOTE)
- Undersampling majority class
- Ensemble methods
- Anomaly detection approaches
- Use appropriate metrics (precision, recall, F1, not just accuracy)

### Challenge: Model Interpretability

**Problem:**
- Black-box models hard to explain
- Business needs to understand predictions

**Solutions:**
- Use interpretable models (linear, tree-based)
- SHAP values for feature importance
- LIME for local explanations
- Partial dependence plots
- Feature importance analysis
- Model documentation and validation

### Challenge: Concept Drift

**Problem:**
- Supply chain patterns change over time
- Model performance degrades

**Solutions:**
- Monitor model performance continuously
- Retrain models regularly (monthly, quarterly)
- Online learning approaches
- Detect drift with statistical tests
- A/B testing for model updates
- Maintain multiple model versions

---

## Output Format

### ML Project Report Template

**Executive Summary:**
- Business problem addressed
- ML approach taken
- Key results and metrics
- Recommended actions

**Problem Definition:**
- Detailed problem statement
- Success metrics defined
- Current baseline performance

**Data Analysis:**
- Data sources and volume
- Feature engineering approach
- Data quality assessment
- Exploratory data analysis

**Model Development:**

| Model | Algorithm | Train Accuracy | Test Accuracy | MAE | RMSE |
|-------|-----------|---------------|---------------|-----|------|
| Baseline | Moving Avg | - | - | 45.2 | 62.3 |
| Model 1 | Random Forest | 0.92 | 0.87 | 32.1 | 44.5 |
| Model 2 | XGBoost | 0.95 | 0.89 | 28.3 | 39.7 |
| Model 3 | LSTM | 0.94 | 0.90 | 26.8 | 37.2 |

**Model Performance:**
- Selected model and rationale
- Performance metrics
- Feature importance
- Error analysis

**Deployment Plan:**
- Deployment architecture
- API specifications
- Monitoring strategy
- Retraining schedule

**Business Impact:**
- Expected improvements
- Cost-benefit analysis
- Implementation roadmap
- Risks and mitigation

---

## Questions to Ask

If you need more context:
1. What specific supply chain problem needs ML solution?
2. What data is available? (volume, features, quality)
3. What's the target variable or outcome to predict?
4. Is this supervised, unsupervised, or reinforcement learning?
5. What's the current baseline performance?
6. What level of accuracy is needed for business value?
7. What are deployment requirements? (batch, real-time, edge)
8. What ML expertise exists in the team?

---

## Related Skills

- **demand-forecasting**: For time series forecasting methods
- **supply-chain-analytics**: For KPIs and metrics
- **optimization-modeling**: For combining ML with optimization
- **prescriptive-analytics**: For decision support with ML
- **digital-twin-modeling**: For simulation with ML
- **computer-vision-warehouse**: For warehouse CV applications
- **nlp-supply-chain**: For NLP-specific applications
- **neural-networks-forecasting**: For deep learning forecasting
