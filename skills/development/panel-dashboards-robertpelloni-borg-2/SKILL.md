---
name: panel-dashboards
description: Master interactive dashboard and application development with Panel and Param. Use this skill when building custom web applications with Python, creating reactive component-based UIs, handling file uploads and real-time data streaming, implementing multi-page applications, or developing enterprise dashboards with templates and theming.
version: 2025-01-07
compatibility: Requires panel >= 1.3.0, param >= 2.0.0, bokeh >= 3.0.0, tornado (web server). Supports Material Design, Bootstrap, and custom themes.
---

# Panel Dashboards Skill

## Overview

Master interactive dashboard and application development with Panel and Param. This skill covers building web applications, component systems, and responsive dashboards that scale from simple tools to complex enterprise applications.

## Dependencies

- panel >= 1.3.0
- param >= 2.0.0
- bokeh >= 3.0.0
- tornado (web server)

## Core Capabilities

### 1. Component-Based Application Development

Panel provides a comprehensive component library for building rich user interfaces:

- **Layout Components**: Row, Column, Tabs, Accordion, GridBox
- **Input Widgets**: TextInput, Select, DatePicker, RangeSlider, FileInput
- **Output Display**: Markdown, HTML, DataFrame, Image, Video
- **Container Controls**: Card, Alert, ProgressBar

```python
import panel as pn
import param

pn.extension('material')

class Dashboard(param.Parameterized):
    title = param.String(default="My Dashboard")
    refresh_interval = param.Integer(default=5000, bounds=(1000, 60000))

    @param.depends('refresh_interval')
    def view(self):
        return pn.Column(
            pn.pane.Markdown(f"## {self.title}"),
            pn.param.ObjectSelector.from_param(self.param.refresh_interval),
            pn.Row(self._metric_card(), self._chart())
        )

    def _metric_card(self):
        return pn.Card(
            "Active Users",
            "42,531",
            title="Metrics",
            styles={"background": "#E8F4F8"}
        )

    def _chart(self):
        return pn.pane.Markdown("## Chart Placeholder")

dashboard = Dashboard()
app = dashboard.view

if __name__ == '__main__':
    app.servable()
```

### 2. Reactive Pipelines and Watchers

Panel excels at creating reactive, event-driven applications:

```python
import panel as pn
import param
import numpy as np

class DataAnalyzer(param.Parameterized):
    data_source = param.Selector(default='random', objects=['random', 'file'])
    num_points = param.Integer(default=100, bounds=(10, 1000))
    aggregation = param.Selector(default='mean', objects=['mean', 'sum', 'std'])

    @param.depends('data_source', 'num_points', watch=True)
    def _refresh_data(self):
        if self.data_source == 'random':
            self.data = np.random.randn(self.num_points)

    @param.depends('data_source', 'num_points', 'aggregation')
    def summary(self):
        if not hasattr(self, 'data'):
            self._refresh_data()

        agg_func = getattr(np, self.aggregation)
        result = agg_func(self.data)
        return f"{self.aggregation.capitalize()}: {result:.2f}"

analyzer = DataAnalyzer()

pn.extension('material')
app = pn.Column(
    pn.param.ParamMethod.from_param(analyzer.param),
    analyzer.summary
)
```

### 3. Template and Theming

Panel supports multiple templates for different application styles:

- **BootstrapTemplate**: Modern Bootstrap-based design
- **MaterialTemplate**: Material Design principles
- **VanillaTemplate**: Clean, minimal design
- **DarkTemplate**: Dark mode optimized

```python
import panel as pn
import param

pn.extension('material')

class Config(param.Parameterized):
    theme = param.Selector(default='dark', objects=['dark', 'light'])
    sidebar_width = param.Integer(default=300, bounds=(200, 500))

config = Config()

template = pn.template.MaterialTemplate(
    title="Advanced Dashboard",
    header_background="#2E3440",
    sidebar_width=config.sidebar_width,
    main=[pn.pane.Markdown("# Main Content")],
    sidebar=[
        pn.param.ParamMethod.from_param(config.param)
    ]
)

template.servable()
```

### 4. File Handling and Data Upload

Build applications that accept file uploads and process data:

```python
import panel as pn
import pandas as pd

file_input = pn.widgets.FileInput(accept='.csv,.xlsx')

@pn.depends(file_input)
def process_file(file_input):
    if file_input is None:
        return pn.pane.Markdown("### Upload a file to proceed")

    if file_input.filename.endswith('.csv'):
        df = pd.read_csv(file_input.value)
    else:
        df = pd.read_excel(file_input.value)

    return pn.Column(
        pn.pane.Markdown(f"### {file_input.filename}"),
        pn.pane.DataFrame(df.head(10), width=800),
        pn.pane.Markdown(f"Shape: {df.shape}")
    )

pn.extension('material')
app = pn.Column(
    pn.pane.Markdown("# Data Upload"),
    file_input,
    process_file
)
```

### 5. Real-time Streaming and Updates

Create dashboards with live data updates:

```python
import panel as pn
import param
import numpy as np
from datetime import datetime

class LiveMonitor(param.Parameterized):
    update_frequency = param.Integer(default=1000, bounds=(100, 5000))
    is_running = param.Boolean(default=False)
    current_value = param.Number(default=0)

    def __init__(self, **params):
        super().__init__(**params)
        self._data_history = []

    def start(self):
        self.is_running = True
        pn.state.add_periodic_callback(
            self._update,
            period=self.update_frequency,
            start=True
        )

    def _update(self):
        if self.is_running:
            self.current_value = np.random.randn() + self.current_value * 0.95
            self._data_history.append({
                'timestamp': datetime.now(),
                'value': self.current_value
            })

    def get_plot(self):
        if not self._data_history:
            return pn.pane.Markdown("No data yet...")

        import holoviews as hv
        df = pd.DataFrame(self._data_history)
        return hv.Curve(df, 'timestamp', 'value').opts(responsive=True)

monitor = LiveMonitor()
app = pn.Column(
    pn.widgets.Button.from_param(monitor.param.is_running, label="Start/Stop"),
    monitor.get_plot
)
```

## Best Practices

### 1. Parameter Organization
- Use Param classes to organize all configurable state
- Leverage type hints and validation in parameter definitions
- Use watchers for side effects, depends for reactive updates

### 2. Responsive Design
- Always use `responsive=True` and `sizing_mode` options
- Test on multiple screen sizes
- Use GridBox or CSS Grid for complex layouts

### 3. Performance Optimization
- Lazy-load expensive components using Tabs or Accordion
- Use caching decorators for expensive computations
- Implement pagination for large datasets
- Stream data rather than loading all at once

### 4. Code Organization
- Separate UI concerns from business logic using Param classes
- Create reusable component functions
- Use templates for consistent application structure
- Organize related components into modules

### 5. Error Handling
- Validate input parameters with Param bounds and selectors
- Provide clear error messages to users
- Use try-catch blocks around external API calls
- Implement graceful degradation for failed operations

## Common Patterns

### Pattern 1: Multi-Page Application
```python
class MultiPageApp(param.Parameterized):
    page = param.Selector(default='home', objects=['home', 'analytics', 'settings'])

    @param.depends('page')
    def current_view(self):
        pages = {
            'home': self._home_page,
            'analytics': self._analytics_page,
            'settings': self._settings_page,
        }
        return pages[self.page]()
```

### Pattern 2: Form with Validation
```python
class FormValidator(param.Parameterized):
    email = param.String(default='')
    age = param.Integer(default=0, bounds=(0, 150))

    @param.depends('email', 'age')
    def validation_message(self):
        if not self.email or '@' not in self.email:
            return pn.pane.Alert("Invalid email", alert_type='danger')
        if self.age < 18:
            return pn.pane.Alert("Must be 18+", alert_type='warning')
        return pn.pane.Alert("Validation passed!", alert_type='success')
```

### Pattern 3: Data Filtering Pipeline
```python
class FilteredDataView(param.Parameterized):
    df = param.Parameter(default=None)
    column_filter = param.String(default='')
    value_filter = param.String(default='')

    @param.depends('column_filter', 'value_filter')
    def filtered_data(self):
        if self.column_filter not in self.df.columns:
            return self.df
        return self.df[self.df[self.column_filter].astype(str).str.contains(self.value_filter)]
```

## Integration with HoloViz Ecosystem

Panel integrates seamlessly with other HoloViz libraries:

- **HoloViews**: Embed interactive plots in Panel applications
- **hvPlot**: Quick plotting within Panel dashboards
- **Param**: Unified parameter system for all interactivity
- **GeoViews**: Embed geographic visualizations
- **Datashader**: Render large datasets with Panel

## Common Use Cases

1. **Real-time Monitoring Dashboards**: Live metrics and KPI displays
2. **Data Exploration Tools**: Interactive data analysis applications
3. **Configuration Interfaces**: Complex multi-step configuration UIs
4. **Data Input Applications**: Validated form-based data collection
5. **Report Viewers**: Interactive report generation and browsing
6. **Administrative Interfaces**: Internal tools for data management

## Troubleshooting

### Issue: Slow Dashboard Load Times
- Lazy-load components using Tabs or Accordion
- Implement caching with `@pn.cache` decorator
- Move expensive computations to initialization
- Profile with Panel's built-in profiling tools

### Issue: Unresponsive UI During Computation
- Use `pn.state.add_periodic_callback` for background tasks
- Implement loading indicators during processing
- Break long computations into smaller steps
- Consider async/await patterns

### Issue: Memory Leaks in Long-Running Apps
- Clean up event listeners with `pn.state.clear_caches()`
- Monitor callback registration and removal
- Limit data history sizes in streaming applications
- Profile with memory profilers

## Resources

- [Panel Documentation](https://panel.holoviz.org)
- [Panel Gallery](https://panel.holoviz.org/gallery/index.html)
- [Param Documentation](https://param.holoviz.org)
- [Panel Discourse Community](https://discourse.holoviz.org)
