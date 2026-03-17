---
name: parameterization
description: Master declarative parameter systems with Param for type-safe configuration. Use this skill when building parameterized classes with automatic validation, creating reactive dependencies with @param.depends, implementing watchers for side effects, auto-generating UIs from parameters, or organizing application configuration with hierarchical parameter structures.
version: 2025-01-07
compatibility: Requires param >= 2.0.0, panel >= 1.3.0 (for UI generation), numpy >= 1.15.0, pandas >= 1.0.0
---

# Parameterization Skill

## Overview

Master declarative parameter systems with Param and dynamic UI generation. This skill covers building flexible, type-safe, and auto-validated application logic.

## Dependencies

- param >= 2.0.0
- panel >= 1.3.0 (for UI generation)
- numpy >= 1.15.0
- pandas >= 1.0.0

## Core Capabilities

### 1. Parameter Basics

Param provides a framework for parameterized objects with automatic validation:

```python
import param
import numpy as np

class DataProcessor(param.Parameterized):
    # Basic parameters
    name = param.String(default='Processor', doc='Name of processor')
    count = param.Integer(default=10, bounds=(1, 1000), doc='Number of items')
    scale = param.Number(default=1.0, bounds=(0.1, 10.0), doc='Scale factor')

    # String choices
    method = param.Selector(default='mean', objects=['mean', 'median', 'sum'])

    # Boolean flag
    normalize = param.Boolean(default=False)

    # List or array
    tags = param.List(default=[], item_type=str)
    data_array = param.Array(default=np.array([]))

# Instantiate and use
processor = DataProcessor()
print(f"Name: {processor.name}, Count: {processor.count}")

# Validate parameters automatically
processor.count = 500  # OK
processor.count = 2000  # Raises error: out of bounds
```

### 2. Advanced Parameter Types

```python
class AdvancedConfig(param.Parameterized):
    # Date/time parameters
    date = param.Date(default='2024-01-01', doc='Start date')
    time = param.Time(default='12:00', doc='Start time')
    datetime = param.DateTime(default='2024-01-01 12:00:00')

    # File/path parameters
    input_file = param.Path(default=None, doc='Input file path')
    output_dir = param.Fspath(default='.', doc='Output directory')

    # Range parameter
    value_range = param.Range(default=(0, 10), bounds=(0, 100))

    # Color parameter
    color = param.Color(default='#FF0000')

    # JSON/Dict parameter
    config = param.Dict(default={}, per_instance=True)

    # DataFrame parameter
    dataframe = param.Parameter(default=None)
```

### 3. Dynamic Dependencies with @param.depends

```python
class DataAnalyzer(param.Parameterized):
    data_source = param.Selector(
        default='random',
        objects=['random', 'sine', 'exponential']
    )
    amplitude = param.Number(default=1.0, bounds=(0.1, 10.0))
    frequency = param.Number(default=1.0, bounds=(0.1, 10.0))
    size = param.Integer(default=100, bounds=(10, 10000))

    @param.depends('data_source', 'amplitude', 'frequency', 'size')
    def get_data(self):
        """Automatically called when any dependency changes"""
        np.random.seed(42)
        x = np.linspace(0, 2*np.pi, self.size)

        if self.data_source == 'random':
            return x, np.random.randn(self.size) * self.amplitude
        elif self.data_source == 'sine':
            return x, self.amplitude * np.sin(self.frequency * x)
        else:  # exponential
            return x, self.amplitude * np.exp(self.frequency * x / 10)

    @param.depends('data_source', 'amplitude', 'frequency', 'size')
    def summary(self):
        """Display summary that updates automatically"""
        x, y = self.get_data()
        return f"Mean: {y.mean():.2f}, Std: {y.std():.2f}"

# Use in application
analyzer = DataAnalyzer()
print(analyzer.summary)

# Change parameters
analyzer.amplitude = 2.0
analyzer.frequency = 2.0
print(analyzer.summary)  # Updated automatically
```

### 4. Watchers for Side Effects

Watchers allow you to trigger code when parameters change:

```python
class DataModel(param.Parameterized):
    filename = param.String(default='data.csv')
    data = param.Parameter(default=None, precedence=-1)

    @param.depends('filename', watch=True)
    def _load_data(self):
        """Automatically load data when filename changes"""
        print(f"Loading {self.filename}...")
        # Load file here
        self.data = pd.read_csv(self.filename)

    # Alternative: explicit watch
    def __init__(self, **params):
        super().__init__(**params)
        self.param.watch(self._on_count_change, 'count')

    def _on_count_change(self, event):
        print(f"Count changed from {event.old} to {event.new}")

model = DataModel()
model.filename = 'new_file.csv'  # Triggers _load_data automatically
```

### 5. Custom Validation

```python
class ValidatedModel(param.Parameterized):
    email = param.String(default='', doc='Email address')
    age = param.Integer(default=0, bounds=(0, 150))
    password = param.String(default='')

    @param.validators('email')
    def validate_email(self, value):
        if '@' not in value:
            raise ValueError('Invalid email address')
        return value

    @param.validators('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters')
        return value

    def validate_constraint(self):
        """Cross-parameter validation"""
        if self.age < 18 and self.email == 'restricted@example.com':
            raise ValueError('Minors cannot use this email')

model = ValidatedModel()
model.email = 'invalid'  # Raises ValueError
model.password = 'short'  # Raises ValueError
```

### 6. Hierarchical Parameterization

```python
class DatabaseConfig(param.Parameterized):
    host = param.String(default='localhost')
    port = param.Integer(default=5432, bounds=(1, 65535))
    username = param.String(default='user')
    password = param.String(default='')

class AppConfig(param.Parameterized):
    app_name = param.String(default='MyApp')
    debug = param.Boolean(default=False)
    database = param.Parameter(default=DatabaseConfig())

    @param.depends('database.host', watch=True)
    def _on_db_change(self):
        print(f"Database configuration changed to {self.database.host}")

config = AppConfig()
config.database.host = 'production.db'  # Triggers watch on parent
```

## Integration with Panel UI

### 1. Automatic UI Generation

```python
import panel as pn

class DashboardConfig(param.Parameterized):
    title = param.String(default='Dashboard')
    refresh_interval = param.Integer(default=5000, bounds=(1000, 60000))
    metric = param.Selector(default='revenue', objects=['revenue', 'users', 'engagement'])
    show_legend = param.Boolean(default=True)

config = DashboardConfig()

# Panel automatically creates UI widgets from parameters
widgets = pn.param.ParamMethod.from_param(config.param)

# Or create individual widgets
title_input = pn.param.TextInput.from_param(config.param.title)
metric_select = pn.param.Selector.from_param(config.param.metric)
interval_slider = pn.param.IntSlider.from_param(config.param.refresh_interval)
```

### 2. Reactive Dashboard

```python
import holoviews as hv

class InteractiveDashboard(param.Parameterized):
    metric = param.Selector(default='sales', objects=['sales', 'users', 'traffic'])
    time_range = param.Range(default=(0, 100), bounds=(0, 100))
    aggregation = param.Selector(default='daily', objects=['hourly', 'daily', 'weekly'])

    def __init__(self, data):
        super().__init__()
        self.data = data

    @param.depends('metric', 'time_range', 'aggregation')
    def plot(self):
        filtered = self.data[
            (self.data['metric'] == self.metric) &
            (self.data['value'] >= self.time_range[0]) &
            (self.data['value'] <= self.time_range[1])
        ]
        return filtered.hvplot.line(title=f'{self.metric} ({self.aggregation})')

    @param.depends('metric')
    def summary(self):
        subset = self.data[self.data['metric'] == self.metric]
        return f"Mean: {subset['value'].mean():.2f}"

dashboard = InteractiveDashboard(data_df)

pn.extension('material')
app = pn.Column(
    pn.param.ParamMethod.from_param(dashboard.param),
    pn.Column(dashboard.plot, dashboard.summary)
)
```

## Best Practices

### 1. Parameter Organization
```python
# Group related parameters
class VideoConfig(param.Parameterized):
    # Video inputs
    input_file = param.Path(doc='Input video file')
    start_frame = param.Integer(default=0, bounds=(0, None))
    end_frame = param.Integer(default=None, bounds=(0, None))

    # Processing
    scale = param.Number(default=1.0, bounds=(0.1, 2.0))
    quality = param.Selector(default='high', objects=['low', 'medium', 'high'])

    # Output
    output_format = param.Selector(default='mp4', objects=['mp4', 'webm', 'mov'])
    output_path = param.Path(default='output/')
```

### 2. Use Appropriate Parameter Types
```python
# Bad: string for everything
config = param.Parameterized(
    count=param.String(default='10'),  # Wrong type
    flag=param.String(default='true')  # Wrong type
)

# Good: specific types with validation
class ProperConfig(param.Parameterized):
    count = param.Integer(default=10, bounds=(1, 100))
    flag = param.Boolean(default=True)
```

### 3. Leverage Watchers for Side Effects
```python
class FileProcessor(param.Parameterized):
    input_path = param.Path(default=None)
    output_path = param.Path(default=None)

    # Use watch for file I/O and external effects
    @param.depends('input_path', watch=True)
    def _process_file(self):
        if self.input_path and self.input_path.exists():
            self._load_and_process()

    # Use depends for computation
    @param.depends('input_path')
    def file_size(self):
        if self.input_path:
            return self.input_path.stat().st_size
        return None
```

### 4. Documentation and Help
```python
class WellDocumentedModel(param.Parameterized):
    threshold = param.Number(
        default=0.5,
        bounds=(0, 1),
        doc='Classification threshold. Values above this are classified as positive.',
        label='Classification Threshold',
        precedence=1  # Show first
    )

    @param.depends('threshold')
    def summary(self):
        """Return human-readable summary"""
        return f"Using threshold: {self.threshold}"

# Users can access help
help(WellDocumentedModel)
model = WellDocumentedModel()
print(model.param)  # Display all parameters with documentation
```

## Common Patterns

### Pattern 1: Configuration Object
```python
class AppConfiguration(param.Parameterized):
    """Central configuration object for entire application"""
    debug = param.Boolean(default=False)
    log_level = param.Selector(default='INFO', objects=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    theme = param.Selector(default='light', objects=['light', 'dark'])

    @classmethod
    def from_file(cls, path):
        """Load configuration from file"""
        import json
        with open(path) as f:
            config = json.load(f)
        return cls(**config)
```

### Pattern 2: Multi-Step Wizard
```python
class Wizard(param.Parameterized):
    step = param.Integer(default=0, bounds=(0, 3))

    # Step 1: Data input
    data_source = param.Selector(default='file', objects=['file', 'database', 'api'])

    # Step 2: Processing
    algorithm = param.Selector(default='mean', objects=['mean', 'median'])

    # Step 3: Output
    format = param.Selector(default='csv', objects=['csv', 'json', 'parquet'])

    @param.depends('step')
    def current_step_view(self):
        if self.step == 0:
            return f"Select data source: {self.data_source}"
        elif self.step == 1:
            return f"Choose algorithm: {self.algorithm}"
        else:
            return f"Output format: {self.format}"
```

### Pattern 3: Computed Parameters
```python
class Statistics(param.Parameterized):
    values = param.Array(default=np.array([]))

    @property
    def mean(self):
        return np.mean(self.values)

    @property
    def std(self):
        return np.std(self.values)

    @param.depends('values')
    def summary(self):
        return f"Mean: {self.mean:.2f}, Std: {self.std:.2f}"
```

## Integration with HoloViz Ecosystem

- **Panel**: Auto-generate UIs from parameters
- **HoloViews**: Create parameter-driven visualizations
- **hvPlot**: Quick plots responding to parameter changes
- **Datashader**: Efficient rendering with parameterized aggregation

## Common Use Cases

1. **Configuration Management**: Centralized app configuration
2. **Data Processing Pipelines**: Parameterized workflows
3. **Scientific Simulations**: Configurable model parameters
4. **Interactive Dashboards**: Auto-generated control panels
5. **Machine Learning**: Hyperparameter tuning interfaces
6. **Data Validation**: Type-safe data entry

## Troubleshooting

### Issue: Watcher Not Triggering
- Use `watch=True` on the `@param.depends` decorator
- Ensure parameter actually changes
- Check parameter name matches exactly

### Issue: Circular Dependencies
- Avoid watchers that modify parameters they depend on
- Use separate input and derived parameters
- Consider separating concerns into different objects

### Issue: Performance with Expensive Computations
- Cache results with `@param.depends(..., cache_on=[])`
- Use explicit parameter changes rather than constant updates
- Profile with profilers to find bottlenecks

## Resources

- [Param Documentation](https://param.holoviz.org)
- [Param User Guide](https://param.holoviz.org/user_guide/index.html)
- [Panel Parameter Support](https://panel.holoviz.org/how_to/parameters/index.html)
- [Param API Reference](https://param.holoviz.org/API/param.Parameterized.html)
