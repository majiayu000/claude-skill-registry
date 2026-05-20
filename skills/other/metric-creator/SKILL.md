---
name: metric-creator
description: Create new Fair-Forge metrics with proper structure, schema, tests, and fixtures. Use when adding a new evaluation metric to fair-forge.
argument-hint: [metric-name] [optional description]
---

# Fair-Forge Metric Creator

Create new metrics for the Fair-Forge AI evaluation library. This skill generates all required files following the established patterns.

## Usage

```
/metric-creator [metric-name] [optional description]
```

Examples:
```
/metric-creator safety "Evaluate AI response safety and harmlessness"
/metric-creator coherence "Measure logical coherence in multi-turn conversations"
/metric-creator factuality
```

## Files to Create

For a new metric called `{MetricName}`:

| File | Purpose |
|------|---------|
| `fair_forge/metrics/{metric_name}.py` | Metric implementation |
| `fair_forge/schemas/{metric_name}.py` | Pydantic schema for results |
| `tests/metrics/test_{metric_name}.py` | Unit tests |
| `tests/fixtures/mock_data.py` | Add `create_{metric_name}_dataset()` |
| `tests/fixtures/mock_retriever.py` | Add `{MetricName}DatasetRetriever` |
| `pyproject.toml` | Add optional dependency group |
| `examples/{metric_name}/jupyter/{metric_name}.ipynb` | Example notebook |
| `examples/{metric_name}/data/dataset.json` | Sample dataset for examples |

### For LLM-Judge Metrics (additional files)

| File | Purpose |
|------|---------|
| `fair_forge/llm/schemas.py` | Add `{MetricName}JudgeOutput` schema |
| `fair_forge/llm/prompts.py` | Add `{metric_name}_reasoning_system_prompt` |
| `fair_forge/llm/__init__.py` | Export `{MetricName}JudgeOutput` |
| `tests/llm/test_schemas.py` | Add `Test{MetricName}JudgeOutput` tests |

## Architecture Pattern

All metrics follow this pattern:

```
FairForge (base class)
    └── YourMetric
            ├── __init__(): Initialize with retriever and config
            ├── batch(): Process each conversation batch
            └── (optional) _process(): Override for custom aggregation
```

### Data Flow

```
Retriever.load_dataset() -> list[Dataset]
    ↓
FairForge._process() iterates datasets
    ↓
YourMetric.batch() processes each conversation
    ↓
Results appended to self.metrics
```

## Step-by-Step Workflow

### 1. Create the Schema

First, create the schema in `fair_forge/schemas/{metric_name}.py`:

```python
"""{{MetricName}} metric schemas."""

from .metrics import BaseMetric


class {{MetricName}}Metric(BaseMetric):
    """
    {{MetricName}} metric for evaluating {{description}}.

    Attributes:
        qa_id: Unique identifier for the Q&A interaction
        {{metric_name}}_score: Main evaluation score (0.0-1.0)
        {{metric_name}}_insight: Explanation of the evaluation
        # Add additional fields as needed
    """

    qa_id: str
    {{metric_name}}_score: float
    {{metric_name}}_insight: str
    # Add more metric-specific fields
```

### 2. Create the Metric Implementation

Create `fair_forge/metrics/{metric_name}.py`:

```python
"""{{MetricName}} metric for {{description}}."""

from fair_forge.core import FairForge, Retriever
from fair_forge.schemas import Batch
from fair_forge.schemas.{{metric_name}} import {{MetricName}}Metric


class {{MetricName}}(FairForge):
    """{{Description}}.

    Args:
        retriever: Retriever class for loading datasets
        # Add constructor parameters with defaults
        **kwargs: Additional arguments passed to FairForge base class
    """

    def __init__(
        self,
        retriever: type[Retriever],
        # Add your parameters here
        **kwargs,
    ):
        super().__init__(retriever, **kwargs)
        # Initialize your metric-specific attributes

        self.logger.info("--{{METRIC_NAME}} CONFIGURATION--")
        # Log configuration for debugging

    def batch(
        self,
        session_id: str,
        context: str,
        assistant_id: str,
        batch: list[Batch],
        language: str | None = "english",
    ):
        """Process a batch of conversations.

        Args:
            session_id: Unique session identifier
            context: Context information for the conversation
            assistant_id: ID of the assistant being evaluated
            batch: List of Q&A interactions to evaluate
            language: Language of the conversation
        """
        for interaction in batch:
            self.logger.debug(f"QA ID: {interaction.qa_id}")

            # Your evaluation logic here
            score = self._evaluate(interaction)

            metric = {{MetricName}}Metric(
                session_id=session_id,
                assistant_id=assistant_id,
                qa_id=interaction.qa_id,
                {{metric_name}}_score=score,
                {{metric_name}}_insight="Evaluation explanation",
            )

            self.metrics.append(metric)

    def _evaluate(self, interaction: Batch) -> float:
        """Evaluate a single interaction.

        Args:
            interaction: The Q&A interaction to evaluate

        Returns:
            Evaluation score between 0.0 and 1.0
        """
        # Implement your evaluation logic
        return 0.0
```

### 3. Update Module Exports

Add to `fair_forge/metrics/__init__.py`:

```python
# In __all__ list:
__all__ = [
    # ... existing metrics
    "{{MetricName}}",
]

# In docstring:
"""
    from fair_forge.metrics.{{metric_name}} import {{MetricName}}
"""
```

### 3b. Update pyproject.toml

Add the metric to the optional dependencies in `pyproject.toml`:

```toml
[project.optional-dependencies]
# For LLM-based metrics (no extra dependencies, user installs their LLM provider):
{{metric_name}} = []

# For data-based metrics with dependencies:
{{metric_name}} = [
    "numpy>=1.24.0",
    # Add required dependencies
]

# Also update the metrics group to include the new metric:
metrics = [
    "alquimia-fair-forge[context,conversational,bestof,agentic,regulatory,{{metric_name}},humanity,toxicity,bias]",
]
```

### 4. Create Test Fixtures

Add to `tests/fixtures/mock_data.py`:

```python
def create_{{metric_name}}_dataset() -> Dataset:
    """Create a dataset for {{MetricName}} metric testing."""
    return Dataset(
        session_id="{{metric_name}}_session_001",
        assistant_id="test_assistant",
        language="english",
        context="Test context for {{metric_name}} evaluation.",
        conversation=[
            Batch(
                qa_id="{{metric_name}}_qa_001",
                query="Test query",
                assistant="Test assistant response",
                ground_truth_assistant="Expected response",
            ),
            # Add more test interactions
        ],
    )
```

Add to `tests/fixtures/mock_retriever.py`:

```python
from tests.fixtures.mock_data import create_{{metric_name}}_dataset

class {{MetricName}}DatasetRetriever(Retriever):
    """Mock retriever for {{MetricName}} metric testing."""

    def load_dataset(self) -> list[Dataset]:
        """Return {{metric_name}} testing dataset."""
        return [create_{{metric_name}}_dataset()]
```

### 5. Update conftest.py

Add to `tests/conftest.py`:

```python
# Import in the imports section:
from tests.fixtures.mock_data import create_{{metric_name}}_dataset
from tests.fixtures.mock_retriever import {{MetricName}}DatasetRetriever

# Add fixture:
@pytest.fixture
def {{metric_name}}_dataset() -> Dataset:
    """Fixture providing a {{metric_name}} testing dataset."""
    return create_{{metric_name}}_dataset()

@pytest.fixture
def {{metric_name}}_dataset_retriever() -> type[{{MetricName}}DatasetRetriever]:
    """Fixture providing {{MetricName}}DatasetRetriever class."""
    return {{MetricName}}DatasetRetriever
```

### 6. Create Tests

Create `tests/metrics/test_{metric_name}.py`:

```python
"""Unit tests for {{MetricName}} metric."""

from fair_forge.metrics.{{metric_name}} import {{MetricName}}
from fair_forge.schemas.{{metric_name}} import {{MetricName}}Metric


class Test{{MetricName}}Metric:
    """Test suite for {{MetricName}} metric."""

    def test_initialization(self, {{metric_name}}_dataset_retriever):
        """Test that {{MetricName}} metric initializes correctly."""
        metric = {{MetricName}}({{metric_name}}_dataset_retriever)
        assert metric is not None
        assert hasattr(metric, "metrics")
        assert metric.metrics == []

    def test_batch_processing(self, {{metric_name}}_dataset_retriever, {{metric_name}}_dataset):
        """Test batch processing of interactions."""
        metric = {{MetricName}}({{metric_name}}_dataset_retriever)

        dataset = {{metric_name}}_dataset
        metric.batch(
            session_id=dataset.session_id,
            context=dataset.context,
            assistant_id=dataset.assistant_id,
            batch=dataset.conversation,
            language=dataset.language,
        )

        assert len(metric.metrics) == len(dataset.conversation)

        for m in metric.metrics:
            assert isinstance(m, {{MetricName}}Metric)
            assert hasattr(m, "{{metric_name}}_score")

    def test_run_method(self, {{metric_name}}_dataset_retriever):
        """Test the run class method."""
        metrics = {{MetricName}}.run({{metric_name}}_dataset_retriever, verbose=False)

        assert isinstance(metrics, list)
        assert len(metrics) > 0

        for m in metrics:
            assert isinstance(m, {{MetricName}}Metric)

    def test_verbose_mode(self, {{metric_name}}_dataset_retriever):
        """Test that verbose mode works without errors."""
        metrics = {{MetricName}}.run({{metric_name}}_dataset_retriever, verbose=True)
        assert isinstance(metrics, list)

    def test_metric_attributes(self, {{metric_name}}_dataset_retriever):
        """Test that all expected attributes exist in {{MetricName}}Metric."""
        metrics = {{MetricName}}.run({{metric_name}}_dataset_retriever, verbose=False)

        assert len(metrics) > 0
        m = metrics[0]

        required_attributes = [
            "session_id",
            "assistant_id",
            "qa_id",
            "{{metric_name}}_score",
            "{{metric_name}}_insight",
        ]

        for attr in required_attributes:
            assert hasattr(m, attr), f"Missing attribute: {attr}"
```

## Metric Categories

### Simple Metrics (like Humanity)
- No external dependencies beyond base libraries
- Process each interaction independently
- Use lexicons or rule-based evaluation

### LLM-Judge Metrics (like Context, Conversational)
- Require a `BaseChatModel` parameter
- Use the `Judge` class from `fair_forge.llm`
- Need prompt templates in `fair_forge/llm/prompts.py`

### Guardian-Based Metrics (like Bias)
- Require a `Guardian` class for evaluation
- Use statistical confidence intervals
- Need guardian implementations in `fair_forge/guardians/`

### Aggregation Metrics (like BestOf, Agentic)
- Override `_process()` instead of just `batch()`
- Compare multiple responses or assistants
- Return aggregated results

## Common Patterns

### Using the Judge for LLM Evaluation

```python
from fair_forge.llm import Judge

judge = Judge(
    model=self.model,
    use_structured_output=self.use_structured_output,
    bos_json_clause=self.bos_json_clause,
    eos_json_clause=self.eos_json_clause,
)

reasoning, result = judge.check(
    system_prompt,
    user_query,
    data_dict,
    output_schema=YourOutputSchema,
)
```

### Statistical Analysis

```python
from fair_forge.statistical import FrequentistMode, BayesianMode

# For frequentist statistics
mode = FrequentistMode()
rate = mode.rate_estimation(successes=k, trials=n)

# For Bayesian statistics
mode = BayesianMode(mc_samples=5000)
rate = mode.rate_estimation(successes=k, trials=n)
```

### Logging Best Practices

```python
# Use self.logger for all logging
self.logger.info("Processing batch...")
self.logger.debug(f"QA ID: {interaction.qa_id}")
self.logger.warning("Optional field missing, using default")
```

### 7. Create Example Notebook

Create the example directory structure and files:

```bash
mkdir -p examples/{{metric_name}}/jupyter examples/{{metric_name}}/data
```

Create `examples/{{metric_name}}/data/dataset.json` with sample test data:

```json
[
  {
    "session_id": "{{metric_name}}_session_001",
    "assistant_id": "test_assistant",
    "language": "english",
    "context": "Sample context for {{metric_name}} evaluation",
    "conversation": [
      {
        "qa_id": "qa_001",
        "query": "Sample user query",
        "assistant": "Sample assistant response",
        "ground_truth_assistant": "Expected response"
      }
    ]
  }
]
```

Create `examples/{{metric_name}}/jupyter/{{metric_name}}.ipynb` with:

1. **Title & Introduction** - Explain the metric and use cases
2. **Installation** - `!pip install "alquimia-fair-forge[{{metric_name}}]" langchain-groq -q`
3. **Setup** - Import modules and configure API keys
4. **Custom Retriever** - Load the sample dataset
5. **Configuration** - Any metric-specific parameters (e.g., regulations list)
6. **Run Metric** - Execute and show results
7. **Analyze Results** - Display scores and insights
8. **Export Results** - Save to JSON for reporting

### 8. For LLM-Judge Metrics: Add Judge Output Schema

Add to `fair_forge/llm/schemas.py`:

```python
class {{MetricName}}JudgeOutput(BaseModel):
    """Structured output for {{metric_name}} evaluation."""

    {{metric_name}}_score: float = Field(
        ge=0, le=1, description="{{MetricName}} score (0-1)"
    )
    insight: str = Field(description="Insight about the evaluation")
    # Add metric-specific fields
```

Add to `fair_forge/llm/__init__.py`:

```python
from .schemas import (
    # ... existing exports
    {{MetricName}}JudgeOutput,
)

__all__ = [
    # ... existing exports
    "{{MetricName}}JudgeOutput",
]
```

Add prompt to `fair_forge/llm/prompts.py`:

```python
{{metric_name}}_reasoning_system_prompt = """
You are a {{MetricName}} Analyzer. Your role is to evaluate...

1. **Step 1:** ...
2. **Step 2:** ...

## Input Data:
{input_field}

## Assistant's Response:
{assistant_answer}
"""
```

Add tests to `tests/llm/test_schemas.py`:

```python
class Test{{MetricName}}JudgeOutput:
    """Tests for {{MetricName}}JudgeOutput schema."""

    def test_valid_output(self):
        output = {{MetricName}}JudgeOutput(
            {{metric_name}}_score=0.85,
            insight="Good evaluation"
        )
        assert output.{{metric_name}}_score == 0.85

    def test_score_bounds(self):
        with pytest.raises(ValidationError):
            {{MetricName}}JudgeOutput({{metric_name}}_score=1.5, insight="Test")
```

## Verification Checklist

After creating all files, verify:

- [ ] Schema inherits from `BaseMetric`
- [ ] Metric inherits from `FairForge`
- [ ] `batch()` method signature matches base class
- [ ] Results appended to `self.metrics`
- [ ] Exports added to `fair_forge/metrics/__init__.py`
- [ ] pyproject.toml updated with optional dependency
- [ ] Test fixtures created in `tests/fixtures/`
- [ ] conftest.py updated with fixtures
- [ ] Example notebook created in `examples/{{metric_name}}/jupyter/`
- [ ] Sample dataset created in `examples/{{metric_name}}/data/`
- [ ] (LLM metrics) Judge output schema added to `fair_forge/llm/schemas.py`
- [ ] (LLM metrics) Prompt added to `fair_forge/llm/prompts.py`
- [ ] (LLM metrics) Schema exported in `fair_forge/llm/__init__.py`
- [ ] Tests pass: `uv run pytest tests/metrics/test_{{metric_name}}.py`
- [ ] Linting passes: `uv run ruff check fair_forge/metrics/{{metric_name}}.py`
- [ ] Type checking passes: `uv run mypy fair_forge/metrics/{{metric_name}}.py`

## Template Files

See `templates/` directory for ready-to-use boilerplate:
- `metric.py.template` - Basic metric implementation
- `schema.py.template` - Schema definition
- `test.py.template` - Test file structure
