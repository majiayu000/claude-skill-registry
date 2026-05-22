---
name: two-sigma-ml-at-scale
description: Build trading systems in the style of Two Sigma, the systematic investment manager pioneering machine learning at scale. Emphasizes alternative data, distributed computing, feature engineering, and rigorous ML infrastructure. Use when building ML pipelines for alpha research, feature stores, or large-scale backtesting systems.
---

# Two Sigma Style Guide

## Overview

Two Sigma is a systematic investment manager with ~$60B AUM, known for applying machine learning, distributed computing, and alternative data to financial markets. They operate like a technology company, investing heavily in data infrastructure, ML platforms, and research tooling.

## Core Philosophy

> "We're a technology company that happens to be in finance."

> "Data is the new oil, but only if you can refine it."

> "The best model is worthless without the infrastructure to deploy it."

Two Sigma believes that competitive advantage comes from data infrastructure and research velocity—the ability to test more ideas faster than competitors.

## Design Principles

1. **Data Platform First**: Build the platform, then the models.

2. **Feature Store**: Features are first-class citizens, versioned and shared.

3. **Reproducibility**: Every experiment must be reproducible.

4. **Scale Horizontally**: Design for 1000x more data than you have today.

5. **Research Velocity**: Reduce time from idea to tested hypothesis.

## When Building ML Trading Systems

### Always

- Version everything: data, features, models, code
- Store point-in-time snapshots (no lookahead bias)
- Track feature lineage and dependencies
- Use distributed backtesting for scale
- Monitor model drift in production
- Separate feature engineering from model training

### Never

- Use future data in features (even accidentally)
- Train and test on overlapping time periods
- Ignore transaction costs in backtests
- Deploy models without monitoring
- Hardcode features in model code
- Trust a single backtest run

### Prefer

- Feature stores over ad-hoc feature computation
- Declarative pipelines over imperative scripts
- Ensemble methods over single models
- Online learning for adaptation
- A/B testing for model deployment
- Distributed compute over single-machine

## Code Patterns

### Feature Store Architecture

```python
class FeatureStore:
    """
    Two Sigma's insight: features are the real IP.
    Centralize, version, and share them.
    """
    
    def __init__(self, storage_backend, metadata_db):
        self.storage = storage_backend  # e.g., S3, HDFS
        self.metadata = metadata_db     # e.g., PostgreSQL
    
    def register_feature(self, 
                         name: str,
                         computation: Callable,
                         dependencies: List[str],
                         lookback_window: timedelta,
                         description: str):
        """Register a new feature definition."""
        feature_def = FeatureDefinition(
            name=name,
            computation=computation,
            dependencies=dependencies,
            lookback_window=lookback_window,
            description=description,
            version=self.get_next_version(name),
            created_at=datetime.utcnow()
        )
        self.metadata.save(feature_def)
        return feature_def
    
    def compute_feature(self, 
                        feature_name: str, 
                        as_of_date: date,
                        universe: List[str]) -> pd.DataFrame:
        """
        Compute feature values as of a specific date.
        CRITICAL: No future information leakage.
        """
        feature_def = self.metadata.get_latest(feature_name)
        
        # Get point-in-time data for dependencies
        dependency_data = {}
        for dep in feature_def.dependencies:
            dependency_data[dep] = self.get_pit_data(
                dep, 
                as_of_date, 
                lookback=feature_def.lookback_window
            )
        
        # Compute feature
        result = feature_def.computation(dependency_data, universe, as_of_date)
        
        # Cache result
        self.storage.save(
            feature_name=feature_name,
            version=feature_def.version,
            as_of_date=as_of_date,
            values=result
        )
        
        return result
    
    def get_training_data(self,
                          features: List[str],
                          target: str,
                          start_date: date,
                          end_date: date,
                          universe: List[str]) -> pd.DataFrame:
        """
        Get feature matrix for training.
        Each row is (date, symbol) with features computed as-of that date.
        """
        rows = []
        
        for current_date in date_range(start_date, end_date):
            feature_values = {}
            
            for feature_name in features:
                feature_values[feature_name] = self.compute_feature(
                    feature_name, current_date, universe
                )
            
            # Target must be from the FUTURE (what we're predicting)
            target_values = self.get_future_target(
                target, current_date, universe
            )
            
            row = self.merge_features_and_target(
                feature_values, target_values, current_date
            )
            rows.append(row)
        
        return pd.concat(rows)
```

### Distributed Backtesting

```python
class DistributedBacktester:
    """
    Two Sigma approach: parallelize backtesting across cluster.
    Test hundreds of configurations simultaneously.
    """
    
    def __init__(self, cluster: SparkCluster):
        self.cluster = cluster
        self.feature_store = FeatureStore()
    
    def run_parameter_sweep(self,
                            strategy_class: Type[Strategy],
                            param_grid: Dict[str, List],
                            start_date: date,
                            end_date: date,
                            n_splits: int = 5) -> pd.DataFrame:
        """
        Distributed parameter sweep with cross-validation.
        """
        # Generate all parameter combinations
        param_combinations = list(ParameterGrid(param_grid))
        
        # Create time-series cross-validation splits
        cv_splits = self.create_ts_splits(start_date, end_date, n_splits)
        
        # Distribute work: (params, cv_fold) pairs
        work_items = [
            (params, train_dates, test_dates)
            for params in param_combinations
            for train_dates, test_dates in cv_splits
        ]
        
        # Run in parallel on cluster
        results = self.cluster.map(
            self.run_single_backtest,
            work_items,
            strategy_class=strategy_class
        )
        
        return self.aggregate_results(results)
    
    def run_single_backtest(self,
                            params: Dict,
                            train_dates: Tuple[date, date],
                            test_dates: Tuple[date, date],
                            strategy_class: Type[Strategy]) -> BacktestResult:
        """Single backtest run on a worker node."""
        
        # Get training data
        train_data = self.feature_store.get_training_data(
            features=strategy_class.required_features(),
            target='forward_returns',
            start_date=train_dates[0],
            end_date=train_dates[1]
        )
        
        # Train strategy
        strategy = strategy_class(**params)
        strategy.fit(train_data)
        
        # Run backtest on test period
        test_data = self.feature_store.get_training_data(
            features=strategy_class.required_features(),
            target='forward_returns',
            start_date=test_dates[0],
            end_date=test_dates[1]
        )
        
        returns = self.simulate_trading(strategy, test_data)
        
        return BacktestResult(
            params=params,
            train_period=train_dates,
            test_period=test_dates,
            returns=returns,
            sharpe=self.calculate_sharpe(returns),
            max_drawdown=self.calculate_max_drawdown(returns)
        )
```

### Alternative Data Pipeline

```python
class AlternativeDataPipeline:
    """
    Two Sigma's edge: alternative data processed at scale.
    Satellite imagery, credit card data, web scraping, etc.
    """
    
    def __init__(self, raw_storage, processed_storage, feature_store):
        self.raw = raw_storage
        self.processed = processed_storage
        self.feature_store = feature_store
    
    def ingest_satellite_imagery(self, 
                                  source: str,
                                  date: date) -> Dict[str, Any]:
        """
        Example: count cars in retail parking lots.
        """
        # Download raw imagery
        raw_images = self.fetch_images(source, date)
        
        # Store raw with metadata
        raw_path = self.raw.save(
            data=raw_images,
            source=source,
            date=date,
            ingested_at=datetime.utcnow()
        )
        
        # Process: detect and count vehicles
        processed = {}
        for location_id, image in raw_images.items():
            vehicle_count = self.detect_vehicles(image)
            processed[location_id] = {
                'vehicle_count': vehicle_count,
                'image_quality': self.assess_quality(image),
                'weather_conditions': self.detect_weather(image)
            }
        
        # Store processed
        processed_path = self.processed.save(
            data=processed,
            source=source,
            date=date,
            processing_version='v2.3'
        )
        
        return processed
    
    def build_retail_traffic_feature(self):
        """
        Convert satellite data into trading feature.
        """
        def compute(deps, universe, as_of_date):
            # Get satellite data up to as_of_date
            satellite = deps['satellite_parking_counts']
            
            # Map locations to companies
            location_mapping = deps['location_to_ticker']
            
            # Aggregate by company
            company_traffic = {}
            for ticker in universe:
                locations = location_mapping.get(ticker, [])
                counts = [satellite.get(loc, {}).get('vehicle_count', np.nan) 
                          for loc in locations]
                
                # Year-over-year change (careful about seasonality)
                current = np.nanmean(counts)
                year_ago = self.get_year_ago_counts(ticker, as_of_date)
                
                company_traffic[ticker] = {
                    'parking_lot_traffic': current,
                    'traffic_yoy_change': (current - year_ago) / year_ago if year_ago else np.nan
                }
            
            return pd.DataFrame(company_traffic).T
        
        self.feature_store.register_feature(
            name='retail_parking_traffic',
            computation=compute,
            dependencies=['satellite_parking_counts', 'location_to_ticker'],
            lookback_window=timedelta(days=7),
            description='YoY change in parking lot traffic from satellite imagery'
        )
```

### Model Monitoring and Drift Detection

```python
class ModelMonitor:
    """
    Two Sigma approach: continuous monitoring of production models.
    Detect drift before it becomes a problem.
    """
    
    def __init__(self, model_registry, metrics_store):
        self.registry = model_registry
        self.metrics = metrics_store
        self.drift_thresholds = {}
    
    def monitor_model(self, 
                      model_id: str,
                      predictions: pd.Series,
                      actuals: pd.Series,
                      features: pd.DataFrame):
        """Real-time monitoring of model performance."""
        
        # Performance metrics
        ic = stats.spearmanr(predictions, actuals).correlation
        hit_rate = (np.sign(predictions) == np.sign(actuals)).mean()
        
        # Feature drift detection
        feature_drift = self.detect_feature_drift(model_id, features)
        
        # Prediction distribution drift
        pred_drift = self.detect_prediction_drift(model_id, predictions)
        
        # Store metrics
        self.metrics.log(
            model_id=model_id,
            timestamp=datetime.utcnow(),
            ic=ic,
            hit_rate=hit_rate,
            feature_drift=feature_drift,
            prediction_drift=pred_drift
        )
        
        # Alert on significant drift
        if feature_drift > self.drift_thresholds.get(model_id, 0.1):
            self.alert(f"Feature drift detected for {model_id}: {feature_drift}")
        
        if ic < 0:
            self.alert(f"Negative IC for {model_id}: {ic}")
    
    def detect_feature_drift(self, 
                             model_id: str, 
                             current_features: pd.DataFrame) -> float:
        """
        Compare current feature distribution to training distribution.
        Uses Population Stability Index (PSI).
        """
        training_stats = self.registry.get_training_stats(model_id)
        
        psi_scores = []
        for col in current_features.columns:
            expected = training_stats[col]
            actual = current_features[col]
            psi = self.calculate_psi(expected, actual)
            psi_scores.append(psi)
        
        return np.mean(psi_scores)
    
    def calculate_psi(self, expected: pd.Series, actual: pd.Series) -> float:
        """Population Stability Index for drift detection."""
        # Bin the distributions
        bins = np.percentile(expected, np.linspace(0, 100, 11))
        
        expected_pct = np.histogram(expected, bins=bins)[0] / len(expected)
        actual_pct = np.histogram(actual, bins=bins)[0] / len(actual)
        
        # Avoid division by zero
        expected_pct = np.clip(expected_pct, 0.001, 1)
        actual_pct = np.clip(actual_pct, 0.001, 1)
        
        psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
        return psi
```

## Mental Model

Two Sigma approaches ML trading by asking:

1. **What data do we have?** And what data could we get?
2. **What features can we extract?** Systematic feature engineering
3. **How do we avoid lookahead bias?** Point-in-time everything
4. **How do we scale?** Distributed compute for backtesting
5. **How do we monitor?** Continuous drift detection

## Signature Two Sigma Moves

- Feature stores as central infrastructure
- Point-in-time data management
- Distributed backtesting at scale
- Alternative data pipelines
- Continuous model monitoring
- Experiment tracking and reproducibility
- Declarative feature definitions
- Horizontal scaling for research
