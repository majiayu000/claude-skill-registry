---
name: pandasai
description: Conversational data analysis using natural language queries on DataFrames. Chat with your data using LLMs to generate insights, create visualizations, and explain code.
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
  - natural_language_queries
  - dataframe_conversations
  - chart_generation
  - code_explanation
  - multi_dataframe_analysis
  - custom_prompts
  - llm_backend_flexibility
  - data_privacy_modes
tools:
  - Read
  - Write
  - Bash
  - Grep
tags: [pandasai, llm, dataframe, natural-language, data-analysis, visualization, conversational-ai, pandas]
platforms: [python]
related_skills:
  - langchain
  - pandas-data-processing
  - plotly
  - streamlit
---

# PandasAI Skill

> Chat with your data using natural language. Ask questions about DataFrames and get insights, visualizations, and explanations powered by LLMs.

## Quick Start

```bash
# Install PandasAI
pip install pandasai

# Install with OpenAI support
pip install pandasai openai

# Install with visualization support
pip install pandasai matplotlib seaborn plotly

# Set API key
export OPENAI_API_KEY="your-api-key"
```

## When to Use This Skill

**USE when:**
- You need to analyze data without writing code
- Exploring unfamiliar datasets with natural language questions
- Creating quick visualizations from descriptive prompts
- Explaining complex data transformations to stakeholders
- Building conversational interfaces for data exploration
- Prototyping data analysis workflows rapidly
- Need LLM-powered data insights on pandas DataFrames
- Creating reports from data with natural language descriptions

**DON'T USE when:**
- Production data pipelines requiring deterministic outputs
- Processing highly sensitive data (consider privacy modes)
- Need precise control over generated code
- Performance-critical applications with large datasets
- Simple queries better handled by direct pandas operations
- Reproducible analyses requiring version-controlled code

## Prerequisites

```bash
# Core installation
pip install pandasai>=2.0.0

# For OpenAI backend (recommended)
pip install pandasai[openai]

# For visualization
pip install pandasai matplotlib seaborn plotly

# For Excel/CSV handling
pip install pandasai openpyxl xlrd

# For database connections
pip install pandasai sqlalchemy psycopg2-binary pymysql

# Environment setup
export OPENAI_API_KEY="sk-..."
# Or for other providers
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

### Verify Installation

```python
import pandasai
from pandasai import SmartDataframe
import pandas as pd

print(f"PandasAI version: {pandasai.__version__}")

# Quick test
df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
smart_df = SmartDataframe(df)
print("PandasAI installed successfully!")
```

## Core Capabilities

### 1. Basic Natural Language Queries

**Simple DataFrame Conversations:**
```python
"""
Query DataFrames using natural language with PandasAI.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def create_smart_dataframe(
    df: pd.DataFrame,
    model: str = "gpt-4",
    temperature: float = 0.0
) -> SmartDataframe:
    """
    Create a SmartDataframe for natural language queries.

    Args:
        df: Input pandas DataFrame
        model: LLM model to use
        temperature: Sampling temperature (0 for deterministic)

    Returns:
        SmartDataframe instance ready for queries
    """
    # Initialize LLM
    llm = OpenAI(
        model=model,
        temperature=temperature
    )

    # Create SmartDataframe
    smart_df = SmartDataframe(
        df,
        config={
            "llm": llm,
            "verbose": True,
            "enable_cache": True,
            "conversational": False
        }
    )

    return smart_df


def query_dataframe(smart_df: SmartDataframe, question: str) -> any:
    """
    Ask a natural language question about the data.

    Args:
        smart_df: SmartDataframe instance
        question: Natural language question

    Returns:
        Query result (can be value, DataFrame, or visualization)
    """
    try:
        result = smart_df.chat(question)
        return result
    except Exception as e:
        print(f"Query error: {e}")
        return None


# Usage Example
# Create sample sales data
sales_data = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=100, freq="D"),
    "product": ["Widget A", "Widget B", "Widget C", "Widget D"] * 25,
    "region": ["North", "South", "East", "West"] * 25,
    "units_sold": [50, 75, 100, 125] * 25,
    "revenue": [500, 1125, 2000, 3125] * 25,
    "cost": [300, 600, 1200, 1800] * 25
})

# Create SmartDataframe
smart_sales = create_smart_dataframe(sales_data)

# Ask questions in natural language
questions = [
    "What is the total revenue?",
    "Which product has the highest average revenue?",
    "What is the profit margin by product?",
    "Show me the top 5 days by units sold"
]

for question in questions:
    print(f"\nQ: {question}")
    result = query_dataframe(smart_sales, question)
    print(f"A: {result}")
```

**Aggregation and Statistical Queries:**
```python
"""
Perform aggregations and statistical analysis using natural language.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def create_analytics_interface(df: pd.DataFrame) -> SmartDataframe:
    """Create an analytics interface for statistical queries."""
    llm = OpenAI(model="gpt-4", temperature=0)

    return SmartDataframe(
        df,
        config={
            "llm": llm,
            "verbose": False,
            "enable_cache": True,
            "custom_whitelisted_dependencies": ["scipy", "numpy"]
        }
    )


# Create sample employee performance data
employee_data = pd.DataFrame({
    "employee_id": range(1, 101),
    "department": ["Engineering", "Sales", "Marketing", "HR", "Finance"] * 20,
    "experience_years": [1, 2, 3, 5, 7, 10, 12, 15, 18, 20] * 10,
    "performance_score": [round(3.0 + i * 0.02, 2) for i in range(100)],
    "salary": [50000 + i * 500 for i in range(100)],
    "projects_completed": [5 + i % 20 for i in range(100)]
})

smart_employees = create_analytics_interface(employee_data)

# Statistical queries
statistical_questions = [
    "What is the average salary by department?",
    "Calculate the correlation between experience_years and salary",
    "What is the standard deviation of performance scores?",
    "Find the median projects completed by department",
    "Which department has the highest variance in salary?",
    "Show the salary distribution statistics (mean, median, std, min, max)"
]

print("Statistical Analysis Results:")
print("=" * 50)

for question in statistical_questions:
    print(f"\nQuestion: {question}")
    result = smart_employees.chat(question)
    print(f"Answer: {result}")
```

### 2. Chart Generation and Visualization

**Creating Charts from Natural Language:**
```python
"""
Generate visualizations using natural language descriptions.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import matplotlib.pyplot as plt
from pathlib import Path

def create_visualization_interface(
    df: pd.DataFrame,
    save_charts: bool = True,
    charts_path: str = "./charts"
) -> SmartDataframe:
    """
    Create interface optimized for chart generation.

    Args:
        df: Input DataFrame
        save_charts: Whether to save generated charts
        charts_path: Directory to save charts

    Returns:
        SmartDataframe configured for visualization
    """
    llm = OpenAI(model="gpt-4", temperature=0)

    # Create charts directory
    Path(charts_path).mkdir(parents=True, exist_ok=True)

    return SmartDataframe(
        df,
        config={
            "llm": llm,
            "save_charts": save_charts,
            "save_charts_path": charts_path,
            "verbose": True,
            "custom_whitelisted_dependencies": [
                "matplotlib",
                "seaborn",
                "plotly"
            ]
        }
    )


# Create sample time series data
import numpy as np

np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=365, freq="D")
time_series_data = pd.DataFrame({
    "date": dates,
    "sales": np.random.normal(1000, 200, 365).cumsum(),
    "customers": np.random.poisson(50, 365),
    "category": ["Electronics", "Clothing", "Food", "Home"] * 91 + ["Electronics"],
    "region": ["North", "South", "East", "West", "Central"] * 73
})

smart_viz = create_visualization_interface(time_series_data)

# Generate various chart types
chart_prompts = [
    "Create a line chart showing sales trend over time",
    "Plot a bar chart of average sales by category",
    "Generate a pie chart showing customer distribution by region",
    "Create a scatter plot of sales vs customers",
    "Make a heatmap showing sales by category and region",
    "Plot monthly sales with a trend line"
]

print("Generating visualizations...")
for prompt in chart_prompts:
    print(f"\nGenerating: {prompt}")
    result = smart_viz.chat(prompt)
    print(f"Result: {result}")


def generate_dashboard_charts(
    df: pd.DataFrame,
    output_dir: str = "./dashboard"
) -> dict:
    """
    Generate multiple charts for a dashboard.

    Args:
        df: Input DataFrame
        output_dir: Directory to save charts

    Returns:
        Dictionary with chart paths and descriptions
    """
    smart_df = create_visualization_interface(df, charts_path=output_dir)

    dashboard_charts = {
        "trend": "Create a line chart showing the main trend over time",
        "distribution": "Create a histogram showing the distribution of the primary metric",
        "comparison": "Create a bar chart comparing categories",
        "relationship": "Create a scatter plot showing key relationships",
        "composition": "Create a pie chart showing composition breakdown"
    }

    results = {}
    for chart_name, prompt in dashboard_charts.items():
        try:
            result = smart_df.chat(prompt)
            results[chart_name] = {
                "prompt": prompt,
                "result": result,
                "status": "success"
            }
        except Exception as e:
            results[chart_name] = {
                "prompt": prompt,
                "error": str(e),
                "status": "failed"
            }

    return results


# Generate dashboard
dashboard_results = generate_dashboard_charts(time_series_data)
for name, info in dashboard_results.items():
    print(f"\n{name}: {info['status']}")
```

**Advanced Visualization Customization:**
```python
"""
Customize chart appearance and style using natural language.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def create_styled_visualization(
    df: pd.DataFrame,
    style_config: dict = None
) -> SmartDataframe:
    """
    Create visualization interface with custom styling.

    Args:
        df: Input DataFrame
        style_config: Custom style configuration

    Returns:
        SmartDataframe with styling configuration
    """
    default_style = {
        "figure.figsize": (12, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10
    }

    style = {**default_style, **(style_config or {})}

    # Apply matplotlib style
    import matplotlib.pyplot as plt
    plt.rcParams.update(style)

    llm = OpenAI(model="gpt-4", temperature=0)

    return SmartDataframe(
        df,
        config={
            "llm": llm,
            "verbose": True,
            "custom_whitelisted_dependencies": [
                "matplotlib",
                "seaborn"
            ]
        }
    )


# Sample financial data
financial_data = pd.DataFrame({
    "quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
    "year": [2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024, 2025, 2025, 2025, 2025],
    "revenue": [100, 120, 115, 140, 150, 165, 180, 200, 210, 225, 240, 260],
    "expenses": [80, 90, 85, 100, 110, 120, 130, 145, 150, 160, 170, 185],
    "profit": [20, 30, 30, 40, 40, 45, 50, 55, 60, 65, 70, 75]
})

smart_finance = create_styled_visualization(financial_data)

# Detailed visualization requests
visualization_requests = [
    """Create a grouped bar chart comparing revenue and expenses by quarter,
    with a secondary line showing profit trend. Use blue for revenue,
    red for expenses, and green for profit.""",

    """Generate a stacked area chart showing revenue, expenses, and profit
    over time with year-quarter on x-axis. Use a professional color palette.""",

    """Create a dual-axis chart with revenue bars on the left axis and
    profit margin percentage line on the right axis."""
]

for request in visualization_requests:
    print(f"\nRequest: {request[:50]}...")
    result = smart_finance.chat(request)
    print(f"Result type: {type(result)}")
```

### 3. Code Explanation and Generation

**Understanding Generated Code:**
```python
"""
Get explanations of generated code and data transformations.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def create_explanatory_interface(df: pd.DataFrame) -> SmartDataframe:
    """Create interface that provides code explanations."""
    llm = OpenAI(model="gpt-4", temperature=0)

    return SmartDataframe(
        df,
        config={
            "llm": llm,
            "verbose": True,
            "enable_cache": False,  # Disable to always show code
            "explain": True  # Enable explanations
        }
    )


def query_with_explanation(
    smart_df: SmartDataframe,
    question: str
) -> dict:
    """
    Query data and get both result and explanation.

    Args:
        smart_df: SmartDataframe instance
        question: Natural language question

    Returns:
        Dictionary with result, code, and explanation
    """
    # Get the result
    result = smart_df.chat(question)

    # Get the last generated code
    last_code = smart_df.last_code_generated

    # Ask for explanation
    explanation_prompt = f"""
    Explain what this code does in simple terms:
    ```python
    {last_code}
    ```
    """
    explanation = smart_df.chat(explanation_prompt)

    return {
        "question": question,
        "result": result,
        "code": last_code,
        "explanation": explanation
    }


# Sample inventory data
inventory_data = pd.DataFrame({
    "sku": [f"SKU-{i:04d}" for i in range(1, 51)],
    "product_name": [f"Product {i}" for i in range(1, 51)],
    "category": ["Electronics", "Clothing", "Home", "Sports", "Books"] * 10,
    "quantity": [100, 50, 200, 75, 150] * 10,
    "unit_price": [29.99, 49.99, 19.99, 79.99, 14.99] * 10,
    "reorder_level": [20, 10, 40, 15, 30] * 10,
    "supplier_id": ["SUP-A", "SUP-B", "SUP-C", "SUP-D", "SUP-E"] * 10
})

smart_inventory = create_explanatory_interface(inventory_data)

# Complex queries with explanations
complex_queries = [
    "Which products are below their reorder level?",
    "Calculate the total inventory value by category",
    "Find suppliers with the most products and their total inventory value",
    "What percentage of products in each category are below reorder level?"
]

print("Queries with Code Explanations")
print("=" * 60)

for query in complex_queries:
    result = query_with_explanation(smart_inventory, query)
    print(f"\nQuestion: {result['question']}")
    print(f"\nGenerated Code:\n{result['code']}")
    print(f"\nResult: {result['result']}")
    print("-" * 40)
```

**Custom Code Generation:**
```python
"""
Generate custom analysis code using natural language specifications.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def generate_analysis_code(
    df: pd.DataFrame,
    analysis_description: str
) -> str:
    """
    Generate analysis code from natural language description.

    Args:
        df: Sample DataFrame for context
        analysis_description: Natural language description of desired analysis

    Returns:
        Generated Python code as string
    """
    llm = OpenAI(model="gpt-4", temperature=0)

    smart_df = SmartDataframe(
        df,
        config={
            "llm": llm,
            "verbose": True,
            "response_parser": None  # Get raw code
        }
    )

    # Generate the code
    smart_df.chat(analysis_description)

    return smart_df.last_code_generated


def create_analysis_function(
    df: pd.DataFrame,
    function_spec: str
) -> callable:
    """
    Create a reusable analysis function from specification.

    Args:
        df: Sample DataFrame for context
        function_spec: Natural language specification

    Returns:
        Callable function
    """
    code = generate_analysis_code(df, function_spec)

    # Extract and wrap the code
    wrapped_code = f"""
def analysis_function(df):
    import pandas as pd
    import numpy as np
    {code}
    return result
"""

    # Execute to define function
    local_vars = {}
    exec(wrapped_code, {"pd": pd, "np": __import__("numpy")}, local_vars)

    return local_vars["analysis_function"]


# Example: Generate reusable analysis code
sample_df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=30),
    "metric_a": range(30),
    "metric_b": range(30, 60)
})

# Generate code for specific analysis
code = generate_analysis_code(
    sample_df,
    """Create a rolling 7-day average of metric_a and identify
    days where metric_b exceeds 2 standard deviations from its mean"""
)

print("Generated Analysis Code:")
print("=" * 40)
print(code)
```

### 4. Multiple LLM Backends

**Configuring Different LLM Providers:**
```python
"""
Use various LLM backends with PandasAI.
"""
import pandas as pd
from pandasai import SmartDataframe
from typing import Optional

def create_openai_backend(
    model: str = "gpt-4",
    temperature: float = 0.0,
    api_key: Optional[str] = None
):
    """Create OpenAI LLM backend."""
    from pandasai.llm import OpenAI

    return OpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key  # Uses env var if None
    )


def create_anthropic_backend(
    model: str = "claude-3-opus-20240229",
    temperature: float = 0.0,
    api_key: Optional[str] = None
):
    """Create Anthropic Claude LLM backend."""
    from pandasai.llm import Anthropic

    return Anthropic(
        model=model,
        temperature=temperature,
        api_key=api_key
    )


def create_google_backend(
    model: str = "gemini-pro",
    temperature: float = 0.0,
    api_key: Optional[str] = None
):
    """Create Google Gemini LLM backend."""
    from pandasai.llm import GoogleGemini

    return GoogleGemini(
        model=model,
        temperature=temperature,
        api_key=api_key
    )


def create_local_backend(
    model_path: str,
    model_type: str = "llama"
):
    """Create local LLM backend using Ollama or similar."""
    from pandasai.llm import LocalLLM

    return LocalLLM(
        model_path=model_path,
        model_type=model_type
    )


def create_azure_openai_backend(
    deployment_name: str,
    api_base: str,
    api_version: str = "2024-02-15-preview",
    api_key: Optional[str] = None
):
    """Create Azure OpenAI LLM backend."""
    from pandasai.llm import AzureOpenAI

    return AzureOpenAI(
        deployment_name=deployment_name,
        api_base=api_base,
        api_version=api_version,
        api_key=api_key
    )


class MultiBackendAnalyzer:
    """
    Analyzer supporting multiple LLM backends with fallback.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.backends = {}
        self.current_backend = None

    def add_backend(self, name: str, llm):
        """Add an LLM backend."""
        self.backends[name] = llm
        if self.current_backend is None:
            self.current_backend = name

    def set_backend(self, name: str):
        """Set the active backend."""
        if name not in self.backends:
            raise ValueError(f"Backend '{name}' not found")
        self.current_backend = name

    def query(self, question: str, backend: str = None) -> any:
        """
        Query using specified or current backend.

        Args:
            question: Natural language question
            backend: Backend name (uses current if None)

        Returns:
            Query result
        """
        backend_name = backend or self.current_backend
        llm = self.backends[backend_name]

        smart_df = SmartDataframe(
            self.df,
            config={"llm": llm, "verbose": False}
        )

        return smart_df.chat(question)

    def query_with_fallback(
        self,
        question: str,
        backend_order: list = None
    ) -> tuple:
        """
        Query with automatic fallback to other backends on failure.

        Args:
            question: Natural language question
            backend_order: Order of backends to try

        Returns:
            Tuple of (result, backend_used)
        """
        backends_to_try = backend_order or list(self.backends.keys())

        for backend_name in backends_to_try:
            try:
                result = self.query(question, backend_name)
                return result, backend_name
            except Exception as e:
                print(f"Backend '{backend_name}' failed: {e}")
                continue

        raise RuntimeError("All backends failed")


# Usage Example
sample_data = pd.DataFrame({
    "product": ["A", "B", "C"],
    "sales": [100, 200, 150]
})

# Create multi-backend analyzer
analyzer = MultiBackendAnalyzer(sample_data)

# Add backends (uncomment based on available API keys)
analyzer.add_backend("openai", create_openai_backend("gpt-4"))
# analyzer.add_backend("anthropic", create_anthropic_backend())
# analyzer.add_backend("google", create_google_backend())

# Query with specific backend
result = analyzer.query("What is the total sales?", backend="openai")
print(f"Result: {result}")

# Query with fallback
# result, used_backend = analyzer.query_with_fallback("What is the average sales?")
# print(f"Result: {result} (using {used_backend})")
```

### 5. Multi-DataFrame Analysis

**Analyzing Multiple Related DataFrames:**
```python
"""
Work with multiple related DataFrames using PandasAI.
"""
import pandas as pd
from pandasai import SmartDatalake
from pandasai.llm import OpenAI

def create_smart_datalake(
    dataframes: dict,
    model: str = "gpt-4"
) -> SmartDatalake:
    """
    Create a SmartDatalake for multi-DataFrame analysis.

    Args:
        dataframes: Dictionary of name: DataFrame pairs
        model: LLM model to use

    Returns:
        SmartDatalake instance
    """
    llm = OpenAI(model=model, temperature=0)

    # Convert dict to list with names
    df_list = []
    for name, df in dataframes.items():
        df.name = name  # Assign name attribute
        df_list.append(df)

    return SmartDatalake(
        df_list,
        config={
            "llm": llm,
            "verbose": True,
            "enable_cache": True
        }
    )


# Create related business DataFrames
customers = pd.DataFrame({
    "customer_id": range(1, 101),
    "customer_name": [f"Customer {i}" for i in range(1, 101)],
    "segment": ["Enterprise", "SMB", "Startup"] * 33 + ["Enterprise"],
    "region": ["North", "South", "East", "West"] * 25,
    "signup_date": pd.date_range("2023-01-01", periods=100, freq="3D")
})
customers.name = "customers"

orders = pd.DataFrame({
    "order_id": range(1, 501),
    "customer_id": [i % 100 + 1 for i in range(500)],
    "order_date": pd.date_range("2024-01-01", periods=500, freq="6H"),
    "product_id": [i % 20 + 1 for i in range(500)],
    "quantity": [1, 2, 3, 5, 10] * 100,
    "unit_price": [29.99, 49.99, 99.99, 149.99, 199.99] * 100
})
orders.name = "orders"

products = pd.DataFrame({
    "product_id": range(1, 21),
    "product_name": [f"Product {i}" for i in range(1, 21)],
    "category": ["Electronics", "Software", "Hardware", "Services"] * 5,
    "cost": [15, 25, 50, 75, 100] * 4
})
products.name = "products"

# Create SmartDatalake
datalake = create_smart_datalake({
    "customers": customers,
    "orders": orders,
    "products": products
})

# Cross-DataFrame queries
cross_df_queries = [
    "What is the total revenue by customer segment?",
    "Which products are most popular among Enterprise customers?",
    "Show the monthly order trend by product category",
    "Find customers who have never ordered",
    "What is the average order value by region?",
    "Which product category has the highest profit margin?"
]

print("Multi-DataFrame Analysis")
print("=" * 50)

for query in cross_df_queries:
    print(f"\nQuery: {query}")
    result = datalake.chat(query)
    print(f"Result: {result}")
```

**Building a Data Warehouse Interface:**
```python
"""
Create a conversational interface for data warehouse queries.
"""
import pandas as pd
from pandasai import SmartDatalake
from pandasai.llm import OpenAI
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TableSchema:
    """Schema definition for a table."""
    name: str
    description: str
    columns: Dict[str, str]  # column_name: description
    primary_key: str
    foreign_keys: Dict[str, str] = None  # column: referenced_table.column


class DataWarehouseInterface:
    """
    Conversational interface for data warehouse exploration.
    """

    def __init__(self, model: str = "gpt-4"):
        self.llm = OpenAI(model=model, temperature=0)
        self.tables: Dict[str, pd.DataFrame] = {}
        self.schemas: Dict[str, TableSchema] = {}
        self.datalake: Optional[SmartDatalake] = None

    def add_table(
        self,
        name: str,
        df: pd.DataFrame,
        schema: TableSchema = None
    ):
        """Add a table to the data warehouse."""
        df.name = name
        self.tables[name] = df
        if schema:
            self.schemas[name] = schema

        # Rebuild datalake
        self._rebuild_datalake()

    def _rebuild_datalake(self):
        """Rebuild the SmartDatalake with current tables."""
        if self.tables:
            self.datalake = SmartDatalake(
                list(self.tables.values()),
                config={
                    "llm": self.llm,
                    "verbose": True,
                    "enable_cache": True
                }
            )

    def get_table_info(self) -> str:
        """Get information about available tables."""
        info_lines = ["Available Tables:"]

        for name, schema in self.schemas.items():
            info_lines.append(f"\n{name}: {schema.description}")
            info_lines.append(f"  Primary Key: {schema.primary_key}")
            info_lines.append("  Columns:")
            for col, desc in schema.columns.items():
                info_lines.append(f"    - {col}: {desc}")

        return "\n".join(info_lines)

    def query(self, question: str) -> any:
        """
        Query the data warehouse using natural language.

        Args:
            question: Natural language question

        Returns:
            Query result
        """
        if not self.datalake:
            raise ValueError("No tables loaded")

        return self.datalake.chat(question)

    def suggest_queries(self, table_name: str = None) -> List[str]:
        """
        Suggest useful queries based on available data.

        Args:
            table_name: Specific table to focus on (optional)

        Returns:
            List of suggested queries
        """
        suggestions = []

        if table_name and table_name in self.tables:
            df = self.tables[table_name]

            # Numeric column suggestions
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols[:3]:
                suggestions.append(f"What is the average {col} in {table_name}?")

            # Categorical column suggestions
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            for col in cat_cols[:2]:
                suggestions.append(f"Show distribution of {col} in {table_name}")
        else:
            # Cross-table suggestions
            if len(self.tables) > 1:
                tables = list(self.tables.keys())
                suggestions.append(f"How are {tables[0]} and {tables[1]} related?")
                suggestions.append("What are the key metrics across all tables?")

        return suggestions


# Usage
warehouse = DataWarehouseInterface()

# Add tables with schemas
warehouse.add_table(
    "customers",
    customers,
    TableSchema(
        name="customers",
        description="Customer master data",
        columns={
            "customer_id": "Unique customer identifier",
            "customer_name": "Customer company name",
            "segment": "Business segment (Enterprise/SMB/Startup)",
            "region": "Geographic region"
        },
        primary_key="customer_id"
    )
)

warehouse.add_table(
    "orders",
    orders,
    TableSchema(
        name="orders",
        description="Customer orders",
        columns={
            "order_id": "Unique order identifier",
            "customer_id": "Reference to customer",
            "order_date": "Date of order",
            "quantity": "Quantity ordered",
            "unit_price": "Price per unit"
        },
        primary_key="order_id",
        foreign_keys={"customer_id": "customers.customer_id"}
    )
)

# Get table information
print(warehouse.get_table_info())

# Query the warehouse
result = warehouse.query("What is the total revenue by customer segment?")
print(f"\nResult: {result}")

# Get query suggestions
suggestions = warehouse.suggest_queries()
print(f"\nSuggested queries: {suggestions}")
```

### 6. Privacy and Security Modes

**Configuring Privacy-Preserving Analysis:**
```python
"""
Configure PandasAI for privacy-sensitive data analysis.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from typing import List, Dict, Optional
import hashlib

def anonymize_column(series: pd.Series, method: str = "hash") -> pd.Series:
    """
    Anonymize a column for privacy.

    Args:
        series: Pandas Series to anonymize
        method: Anonymization method ('hash', 'mask', 'generalize')

    Returns:
        Anonymized Series
    """
    if method == "hash":
        return series.apply(
            lambda x: hashlib.md5(str(x).encode()).hexdigest()[:8]
            if pd.notna(x) else x
        )
    elif method == "mask":
        return series.apply(
            lambda x: str(x)[:2] + "*" * (len(str(x)) - 2)
            if pd.notna(x) and len(str(x)) > 2 else "**"
        )
    elif method == "generalize":
        if pd.api.types.is_numeric_dtype(series):
            return pd.cut(series, bins=5, labels=["Very Low", "Low", "Medium", "High", "Very High"])
        return series
    else:
        raise ValueError(f"Unknown method: {method}")


def create_privacy_safe_interface(
    df: pd.DataFrame,
    sensitive_columns: List[str],
    anonymization_method: str = "hash"
) -> SmartDataframe:
    """
    Create SmartDataframe with anonymized sensitive columns.

    Args:
        df: Input DataFrame
        sensitive_columns: List of columns to anonymize
        anonymization_method: Method for anonymization

    Returns:
        SmartDataframe with anonymized data
    """
    # Create copy and anonymize
    safe_df = df.copy()

    for col in sensitive_columns:
        if col in safe_df.columns:
            safe_df[col] = anonymize_column(safe_df[col], anonymization_method)

    llm = OpenAI(model="gpt-4", temperature=0)

    return SmartDataframe(
        safe_df,
        config={
            "llm": llm,
            "verbose": False,
            "enforce_privacy": True,
            "enable_cache": False  # Don't cache sensitive queries
        }
    )


class PrivacyAwareAnalyzer:
    """
    Analyzer with privacy controls and audit logging.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        sensitive_columns: List[str],
        allowed_operations: List[str] = None
    ):
        self.original_df = df
        self.sensitive_columns = sensitive_columns
        self.allowed_operations = allowed_operations or [
            "aggregate", "count", "average", "sum", "distribution"
        ]
        self.query_log = []

        # Create anonymized version
        self.safe_df = self._create_safe_df()

        # Create SmartDataframe
        llm = OpenAI(model="gpt-4", temperature=0)
        self.smart_df = SmartDataframe(
            self.safe_df,
            config={
                "llm": llm,
                "verbose": True
            }
        )

    def _create_safe_df(self) -> pd.DataFrame:
        """Create anonymized DataFrame."""
        safe_df = self.original_df.copy()

        for col in self.sensitive_columns:
            if col in safe_df.columns:
                safe_df[col] = anonymize_column(safe_df[col], "hash")

        return safe_df

    def _check_query_safety(self, query: str) -> bool:
        """
        Check if query is safe to execute.

        Args:
            query: Natural language query

        Returns:
            True if query is safe
        """
        query_lower = query.lower()

        # Check for attempts to access sensitive columns directly
        for col in self.sensitive_columns:
            if f"show {col}" in query_lower or f"list {col}" in query_lower:
                return False

        # Check if query uses allowed operations
        has_allowed_op = any(
            op in query_lower for op in self.allowed_operations
        )

        return has_allowed_op

    def query(self, question: str, user_id: str = "anonymous") -> any:
        """
        Execute a privacy-safe query.

        Args:
            question: Natural language question
            user_id: User identifier for audit

        Returns:
            Query result or error message
        """
        # Log query attempt
        self.query_log.append({
            "user_id": user_id,
            "question": question,
            "timestamp": pd.Timestamp.now()
        })

        # Check query safety
        if not self._check_query_safety(question):
            return "Query denied: Attempting to access sensitive data directly"

        # Execute query
        try:
            result = self.smart_df.chat(question)
            return result
        except Exception as e:
            return f"Query error: {e}"

    def get_audit_log(self) -> pd.DataFrame:
        """Get query audit log."""
        return pd.DataFrame(self.query_log)


# Example with sensitive data
sensitive_data = pd.DataFrame({
    "employee_id": range(1, 101),
    "name": [f"Employee {i}" for i in range(1, 101)],  # Sensitive
    "email": [f"emp{i}@company.com" for i in range(1, 101)],  # Sensitive
    "ssn": [f"XXX-XX-{i:04d}" for i in range(1, 101)],  # Highly sensitive
    "department": ["Engineering", "Sales", "Marketing", "HR", "Finance"] * 20,
    "salary": [50000 + i * 1000 for i in range(100)],
    "performance_score": [3.0 + (i % 20) * 0.1 for i in range(100)]
})

# Create privacy-aware analyzer
analyzer = PrivacyAwareAnalyzer(
    sensitive_data,
    sensitive_columns=["name", "email", "ssn"],
    allowed_operations=["aggregate", "average", "count", "distribution", "compare"]
)

# Safe queries
safe_queries = [
    "What is the average salary by department?",
    "How many employees are in each department?",
    "What is the distribution of performance scores?"
]

print("Privacy-Safe Analysis Results:")
print("=" * 50)

for query in safe_queries:
    print(f"\nQuery: {query}")
    result = analyzer.query(query, user_id="analyst_001")
    print(f"Result: {result}")

# Unsafe query attempt
unsafe_query = "Show me all employee names and emails"
print(f"\nUnsafe Query: {unsafe_query}")
result = analyzer.query(unsafe_query, user_id="analyst_001")
print(f"Result: {result}")

# View audit log
print("\nAudit Log:")
print(analyzer.get_audit_log())
```

## Integration Examples

### Streamlit Dashboard Integration

```python
"""
Build an interactive data analysis dashboard with Streamlit and PandasAI.
"""
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def create_streamlit_dashboard():
    """Create a Streamlit dashboard for conversational data analysis."""

    st.title("Conversational Data Analysis")
    st.write("Ask questions about your data in natural language")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)

        # Display data preview
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # Display data info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

        # Initialize PandasAI
        api_key = st.sidebar.text_input("OpenAI API Key", type="password")

        if api_key:
            llm = OpenAI(api_key=api_key, model="gpt-4", temperature=0)
            smart_df = SmartDataframe(df, config={"llm": llm, "verbose": False})

            # Query interface
            st.subheader("Ask a Question")

            # Suggested queries
            st.write("**Suggested queries:**")
            suggestions = [
                f"What is the average of {df.select_dtypes(include='number').columns[0]}?" if len(df.select_dtypes(include='number').columns) > 0 else None,
                f"Show the distribution of {df.columns[0]}",
                "How many rows are there?",
                "What are the column names and their types?"
            ]
            suggestions = [s for s in suggestions if s]

            selected_suggestion = st.selectbox("Or choose a suggestion:", [""] + suggestions)

            # Query input
            query = st.text_area(
                "Your question:",
                value=selected_suggestion,
                placeholder="e.g., What is the total sales by region?"
            )

            if st.button("Ask"):
                if query:
                    with st.spinner("Analyzing..."):
                        try:
                            result = smart_df.chat(query)

                            st.subheader("Result")

                            # Display based on result type
                            if isinstance(result, pd.DataFrame):
                                st.dataframe(result)
                            elif hasattr(result, 'savefig'):
                                st.pyplot(result)
                            else:
                                st.write(result)

                            # Show generated code
                            with st.expander("View Generated Code"):
                                st.code(smart_df.last_code_generated, language="python")

                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.warning("Please enter your OpenAI API key in the sidebar")


# To run: streamlit run dashboard.py
# if __name__ == "__main__":
#     create_streamlit_dashboard()
```

### FastAPI Service Integration

```python
"""
Create a REST API for PandasAI queries.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import io
import json

app = FastAPI(title="PandasAI Query Service", version="1.0.0")

# In-memory storage for datasets
datasets: Dict[str, pd.DataFrame] = {}
smart_dfs: Dict[str, SmartDataframe] = {}


class QueryRequest(BaseModel):
    """Request model for queries."""
    dataset_id: str
    question: str
    include_code: bool = False


class QueryResponse(BaseModel):
    """Response model for queries."""
    result: Any
    code: Optional[str] = None
    result_type: str


class DatasetInfo(BaseModel):
    """Information about a dataset."""
    dataset_id: str
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]


@app.post("/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    dataset_id: Optional[str] = None
) -> Dict[str, str]:
    """Upload a CSV dataset."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files are supported")

    # Read CSV
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Generate ID if not provided
    if dataset_id is None:
        dataset_id = file.filename.replace('.csv', '')

    # Store dataset
    datasets[dataset_id] = df

    # Create SmartDataframe
    llm = OpenAI(model="gpt-4", temperature=0)
    smart_dfs[dataset_id] = SmartDataframe(df, config={"llm": llm, "verbose": False})

    return {"dataset_id": dataset_id, "message": "Dataset uploaded successfully"}


@app.get("/datasets/{dataset_id}", response_model=DatasetInfo)
async def get_dataset_info(dataset_id: str) -> DatasetInfo:
    """Get information about a dataset."""
    if dataset_id not in datasets:
        raise HTTPException(404, f"Dataset '{dataset_id}' not found")

    df = datasets[dataset_id]

    return DatasetInfo(
        dataset_id=dataset_id,
        rows=len(df),
        columns=len(df.columns),
        column_names=list(df.columns),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()}
    )


@app.post("/query", response_model=QueryResponse)
async def query_dataset(request: QueryRequest) -> QueryResponse:
    """Query a dataset using natural language."""
    if request.dataset_id not in smart_dfs:
        raise HTTPException(404, f"Dataset '{request.dataset_id}' not found")

    smart_df = smart_dfs[request.dataset_id]

    try:
        result = smart_df.chat(request.question)

        # Determine result type
        if isinstance(result, pd.DataFrame):
            result_type = "dataframe"
            result = result.to_dict(orient="records")
        elif isinstance(result, (int, float)):
            result_type = "number"
        else:
            result_type = "text"
            result = str(result)

        response = QueryResponse(
            result=result,
            result_type=result_type
        )

        if request.include_code:
            response.code = smart_df.last_code_generated

        return response

    except Exception as e:
        raise HTTPException(500, f"Query failed: {str(e)}")


@app.get("/datasets")
async def list_datasets() -> List[str]:
    """List all available datasets."""
    return list(datasets.keys())


@app.delete("/datasets/{dataset_id}")
async def delete_dataset(dataset_id: str) -> Dict[str, str]:
    """Delete a dataset."""
    if dataset_id not in datasets:
        raise HTTPException(404, f"Dataset '{dataset_id}' not found")

    del datasets[dataset_id]
    del smart_dfs[dataset_id]

    return {"message": f"Dataset '{dataset_id}' deleted"}


# Run with: uvicorn api:app --reload
```

### Jupyter Notebook Integration

```python
"""
Enhanced PandasAI usage in Jupyter notebooks.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from IPython.display import display, Markdown, HTML

class JupyterPandasAI:
    """
    Enhanced PandasAI interface for Jupyter notebooks.
    """

    def __init__(self, df: pd.DataFrame, model: str = "gpt-4"):
        self.df = df
        self.llm = OpenAI(model=model, temperature=0)
        self.smart_df = SmartDataframe(
            df,
            config={
                "llm": self.llm,
                "verbose": False,
                "save_charts": True,
                "save_charts_path": "./notebook_charts"
            }
        )
        self.history = []

    def ask(self, question: str, show_code: bool = True) -> any:
        """
        Ask a question with rich Jupyter output.

        Args:
            question: Natural language question
            show_code: Whether to display generated code

        Returns:
            Query result
        """
        # Display question
        display(Markdown(f"**Question:** {question}"))

        # Execute query
        result = self.smart_df.chat(question)

        # Store in history
        self.history.append({
            "question": question,
            "result": result,
            "code": self.smart_df.last_code_generated
        })

        # Display result
        display(Markdown("**Result:**"))

        if isinstance(result, pd.DataFrame):
            display(result)
        else:
            display(result)

        # Optionally show code
        if show_code:
            display(Markdown("**Generated Code:**"))
            display(Markdown(f"```python\n{self.smart_df.last_code_generated}\n```"))

        return result

    def explain(self, question: str) -> str:
        """
        Ask a question and get a detailed explanation.

        Args:
            question: Natural language question

        Returns:
            Explanation string
        """
        # First get the result
        result = self.smart_df.chat(question)

        # Then ask for explanation
        explanation = self.smart_df.chat(
            f"Explain in detail how you calculated: {question}"
        )

        display(Markdown(f"**Question:** {question}"))
        display(Markdown(f"**Result:** {result}"))
        display(Markdown(f"**Explanation:** {explanation}"))

        return explanation

    def compare(self, questions: list) -> pd.DataFrame:
        """
        Run multiple queries and compare results.

        Args:
            questions: List of questions to compare

        Returns:
            DataFrame with questions and results
        """
        results = []

        for q in questions:
            result = self.smart_df.chat(q)
            results.append({
                "Question": q,
                "Result": result
            })

        comparison_df = pd.DataFrame(results)
        display(comparison_df)

        return comparison_df

    def show_history(self) -> None:
        """Display query history."""
        for i, item in enumerate(self.history, 1):
            display(Markdown(f"### Query {i}"))
            display(Markdown(f"**Q:** {item['question']}"))
            display(Markdown(f"**A:** {item['result']}"))
            display(Markdown("---"))


# Usage in Jupyter:
# jpa = JupyterPandasAI(my_dataframe)
# jpa.ask("What is the average sales by region?")
# jpa.explain("Why did Q3 have lower sales?")
# jpa.compare(["Total sales", "Average sales", "Max sales"])
```

## Best Practices

### 1. Query Optimization

```python
"""Best practices for optimizing PandasAI queries."""

# DO: Be specific in your questions
good_queries = [
    "What is the total revenue for Q1 2024?",  # Specific time frame
    "Show the top 5 products by units sold",    # Clear limit
    "Calculate the average order value by customer segment"  # Clear metric
]

# DON'T: Ask vague questions
bad_queries = [
    "Tell me about the data",  # Too vague
    "What's interesting?",     # No clear objective
    "Analyze everything"       # No focus
]

# DO: Break complex questions into steps
def multi_step_analysis(smart_df, questions):
    """Execute analysis in logical steps."""
    results = {}
    for i, q in enumerate(questions, 1):
        print(f"Step {i}: {q}")
        results[f"step_{i}"] = smart_df.chat(q)
    return results

# Example multi-step analysis
steps = [
    "First, what are the column names and their data types?",
    "What is the date range of the data?",
    "What is the total revenue by month?",
    "Which month had the highest growth rate?"
]
```

### 2. Error Handling

```python
"""Robust error handling for PandasAI operations."""
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def safe_query(
    smart_df: SmartDataframe,
    question: str,
    max_retries: int = 3
) -> Tuple[Optional[any], Optional[str]]:
    """
    Execute query with error handling and retries.

    Args:
        smart_df: SmartDataframe instance
        question: Natural language question
        max_retries: Maximum retry attempts

    Returns:
        Tuple of (result, error_message)
    """
    for attempt in range(max_retries):
        try:
            result = smart_df.chat(question)
            return result, None
        except Exception as e:
            logger.warning(f"Query attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return None, str(e)

    return None, "Max retries exceeded"


def validate_result(result: any, expected_type: type = None) -> bool:
    """Validate query result."""
    if result is None:
        return False

    if expected_type and not isinstance(result, expected_type):
        return False

    return True
```

### 3. Caching Strategy

```python
"""Implement caching for repeated queries."""
from functools import lru_cache
import hashlib

class CachedPandasAI:
    """PandasAI wrapper with query caching."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.smart_df = SmartDataframe(df, config={"enable_cache": True})
        self._result_cache = {}

    def _get_cache_key(self, question: str) -> str:
        """Generate cache key for question."""
        df_hash = hashlib.md5(
            pd.util.hash_pandas_object(self.df).values.tobytes()
        ).hexdigest()[:8]
        q_hash = hashlib.md5(question.encode()).hexdigest()[:8]
        return f"{df_hash}_{q_hash}"

    def query(self, question: str, use_cache: bool = True) -> any:
        """Query with caching."""
        cache_key = self._get_cache_key(question)

        if use_cache and cache_key in self._result_cache:
            return self._result_cache[cache_key]

        result = self.smart_df.chat(question)
        self._result_cache[cache_key] = result

        return result

    def clear_cache(self):
        """Clear the result cache."""
        self._result_cache.clear()
```

### 4. Cost Management

```python
"""Monitor and manage LLM API costs."""

class CostAwarePandasAI:
    """PandasAI wrapper with cost tracking."""

    # Approximate costs per 1K tokens (adjust based on current pricing)
    COSTS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
    }

    def __init__(self, df: pd.DataFrame, model: str = "gpt-4", budget: float = 10.0):
        self.model = model
        self.budget = budget
        self.total_cost = 0.0

        llm = OpenAI(model=model, temperature=0)
        self.smart_df = SmartDataframe(df, config={"llm": llm, "verbose": False})

    def estimate_cost(self, question: str) -> float:
        """Estimate query cost."""
        # Rough estimation: 1 token ~ 4 characters
        input_tokens = len(question) / 4
        output_tokens = 500  # Estimated average output

        costs = self.COSTS.get(self.model, self.COSTS["gpt-4"])
        estimated = (input_tokens / 1000 * costs["input"] +
                    output_tokens / 1000 * costs["output"])

        return estimated

    def query(self, question: str) -> any:
        """Query with cost checking."""
        estimated_cost = self.estimate_cost(question)

        if self.total_cost + estimated_cost > self.budget:
            raise ValueError(
                f"Query would exceed budget. "
                f"Current: ${self.total_cost:.4f}, Budget: ${self.budget}"
            )

        result = self.smart_df.chat(question)
        self.total_cost += estimated_cost

        return result

    def get_cost_summary(self) -> dict:
        """Get cost summary."""
        return {
            "total_spent": self.total_cost,
            "budget": self.budget,
            "remaining": self.budget - self.total_cost
        }
```

## Troubleshooting

### Common Issues

#### 1. API Key Errors

```python
# Problem: API key not found or invalid
# Solution: Verify environment variable or explicit key

import os

def verify_api_key():
    """Verify API key is configured."""
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        print("Error: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return False

    if not key.startswith("sk-"):
        print("Warning: API key format may be incorrect")
        return False

    return True

# Alternative: Pass key explicitly
from pandasai.llm import OpenAI
llm = OpenAI(api_key="your-api-key-here")
```

#### 2. Memory Issues with Large DataFrames

```python
# Problem: Out of memory with large DataFrames
# Solution: Sample or aggregate before querying

def create_efficient_smart_df(df: pd.DataFrame, max_rows: int = 10000):
    """Create SmartDataframe with large data handling."""

    if len(df) > max_rows:
        print(f"Sampling {max_rows} rows from {len(df)} total rows")
        sample_df = df.sample(n=max_rows, random_state=42)
    else:
        sample_df = df

    return SmartDataframe(
        sample_df,
        config={
            "llm": OpenAI(model="gpt-4"),
            "verbose": False,
            "max_retries": 3
        }
    )
```

#### 3. Incorrect Results

```python
# Problem: PandasAI returns incorrect or unexpected results
# Solution: Verify with explicit code and add context

def verify_result(smart_df, question, expected_type=None):
    """Verify PandasAI result against pandas."""
    # Get PandasAI result
    ai_result = smart_df.chat(question)

    # Get generated code
    code = smart_df.last_code_generated

    print(f"Question: {question}")
    print(f"AI Result: {ai_result}")
    print(f"Generated Code:\n{code}")

    # Manual verification prompt
    print("\nPlease verify the generated code produces the expected result.")

    return ai_result, code
```

#### 4. Chart Generation Failures

```python
# Problem: Charts not generating or displaying
# Solution: Check dependencies and configuration

def diagnose_chart_issues():
    """Diagnose chart generation issues."""
    issues = []

    # Check matplotlib
    try:
        import matplotlib
        print(f"Matplotlib version: {matplotlib.__version__}")
    except ImportError:
        issues.append("matplotlib not installed")

    # Check backend
    try:
        import matplotlib.pyplot as plt
        backend = plt.get_backend()
        print(f"Matplotlib backend: {backend}")
    except Exception as e:
        issues.append(f"Backend issue: {e}")

    # Check save path
    from pathlib import Path
    charts_path = Path("./charts")
    if not charts_path.exists():
        print("Creating charts directory...")
        charts_path.mkdir(parents=True)

    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No issues detected")

    return issues
```

## Resources

- **PandasAI Documentation**: https://docs.pandas-ai.com/
- **GitHub Repository**: https://github.com/gventuri/pandas-ai
- **PyPI Package**: https://pypi.org/project/pandasai/
- **Examples Gallery**: https://github.com/gventuri/pandas-ai/tree/main/examples

## Version History

- **1.0.0** (2026-01-17): Initial release with natural language queries, chart generation, multiple backends, privacy modes

---

*This skill provides comprehensive patterns for conversational data analysis with PandasAI, refined from production data exploration workflows.*
