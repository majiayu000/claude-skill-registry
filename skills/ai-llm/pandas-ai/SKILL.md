---
name: pandas-ai
description: |
  PandasAI enables natural language queries on pandas DataFrames using LLMs.
  Learn to ask questions in plain English, generate charts, clean data,
  and integrate with OpenAI and local models for conversational data analysis.
license: Apache-2.0
compatibility: 'macos, linux, windows'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - pandas-ai
    - pandas
    - llm
    - natural-language
    - data-analysis
---

# PandasAI

PandasAI adds natural language capabilities to pandas. Ask questions about your data in English and get answers, charts, and transformations — powered by LLMs.

## Installation

```bash
# Install PandasAI
pip install pandasai

# With OpenAI
pip install pandasai[openai]

# With local models via Ollama
pip install pandasai[langchain]
```

## Basic Usage

```python
# basic.py: Ask questions about a DataFrame in natural language
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

llm = OpenAI(api_token="your-openai-api-key")

df = pd.DataFrame({
    "country": ["USA", "UK", "France", "Germany", "Japan"],
    "population": [331_000_000, 67_000_000, 67_000_000, 83_000_000, 125_000_000],
    "gdp_billion": [25_460, 3_070, 2_780, 4_070, 4_230],
})

sdf = SmartDataframe(df, config={"llm": llm})

# Ask questions in natural language
answer = sdf.chat("Which country has the highest GDP?")
print(answer)  # USA

answer = sdf.chat("What is the average population?")
print(answer)  # 134,600,000

answer = sdf.chat("List countries with GDP above 4000 billion")
print(answer)
```

## Multiple DataFrames

```python
# multi-df.py: Query across multiple related DataFrames
from pandasai import SmartDatalake

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "department_id": [1, 2, 1, 3, 2],
    "salary": [85000, 72000, 90000, 68000, 95000],
})

departments = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Engineering", "Marketing", "Sales"],
    "budget": [500000, 200000, 300000],
})

lake = SmartDatalake([employees, departments], config={"llm": llm})

result = lake.chat("What is the average salary per department?")
print(result)

result = lake.chat("Which department is over budget based on total salaries?")
print(result)
```

## Generate Charts

```python
# charts.py: Create visualizations from natural language
sdf = SmartDataframe(df, config={
    "llm": llm,
    "save_charts": True,
    "save_charts_path": "./charts",
})

# Generate charts by asking
sdf.chat("Create a bar chart of GDP by country")
sdf.chat("Plot a pie chart of population distribution")
sdf.chat("Show a scatter plot of GDP vs population")
# Charts saved as PNG in ./charts/
```

## Data Cleaning

```python
# cleaning.py: Use natural language for data cleaning tasks
dirty_df = pd.DataFrame({
    "name": ["Alice", "bob", "CHARLIE", None, "Eve"],
    "email": ["alice@co.com", "invalid", "charlie@co.com", "diana@co.com", ""],
    "age": [30, -5, 45, 200, 28],
    "salary": [85000, 72000, None, 68000, 95000],
})

sdf = SmartDataframe(dirty_df, config={"llm": llm})

# Clean with natural language
cleaned = sdf.chat("Remove rows where age is negative or above 150")
cleaned = sdf.chat("Fill missing salaries with the median salary")
cleaned = sdf.chat("Standardize names to title case")
cleaned = sdf.chat("Remove rows with invalid email addresses")
```

## Custom Configuration

```python
# config.py: Advanced PandasAI configuration
from pandasai import SmartDataframe

sdf = SmartDataframe(df, config={
    "llm": llm,
    "conversational": True,         # Natural language responses
    "verbose": True,                 # Show generated code
    "enable_cache": True,            # Cache repeated queries
    "max_retries": 3,                # Retry on LLM errors
    "custom_whitelisted_dependencies": ["scipy", "sklearn"],
    "save_logs": True,
})

# View the generated Python code
sdf.chat("What is the correlation between GDP and population?")
print(sdf.last_code_generated)
```

## Using Local Models

```python
# local-llm.py: Use Ollama or other local models instead of OpenAI
from pandasai.llm.local_llm import LocalLLM

# With Ollama running locally
llm = LocalLLM(api_base="http://localhost:11434/v1", model="llama3")

sdf = SmartDataframe(df, config={"llm": llm})
answer = sdf.chat("Summarize this dataset")
print(answer)
```

## Pipeline Integration

```python
# pipeline.py: Use PandasAI in an automated analysis pipeline
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import pandas as pd
import json

def analyze_dataset(csv_path: str, questions: list[str]) -> dict:
    """Run a set of natural language questions against a CSV dataset."""
    llm = OpenAI(api_token="your-key")
    df = pd.read_csv(csv_path)
    sdf = SmartDataframe(df, config={"llm": llm, "conversational": True})

    results = {}
    for question in questions:
        try:
            answer = sdf.chat(question)
            results[question] = str(answer)
        except Exception as e:
            results[question] = f"Error: {e}"

    return results

# Usage
report = analyze_dataset("sales.csv", [
    "What was the total revenue last month?",
    "Which product category had the most sales?",
    "What is the month-over-month growth rate?",
])
print(json.dumps(report, indent=2))
```
