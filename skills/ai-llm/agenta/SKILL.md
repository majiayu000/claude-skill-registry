---
name: agenta
description: LLM prompt management and evaluation platform. Version prompts, run A/B tests, evaluate with metrics, and deploy with confidence using Agenta's self-hosted solution.
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
  - prompt_versioning
  - ab_testing
  - evaluation_metrics
  - playground_interface
  - self_hosted_deployment
  - prompt_templates
  - model_comparison
  - experiment_tracking
tools:
  - Read
  - Write
  - Bash
  - Grep
tags: [agenta, llm, prompt-management, evaluation, ab-testing, mlops, self-hosted, versioning]
platforms: [python, docker]
related_skills:
  - langchain
  - dspy
  - prompt-engineering
---

# Agenta Skill

> Manage, evaluate, and deploy LLM prompts with confidence. Version control your prompts, run A/B tests, and measure quality with automated evaluation.

## Quick Start

```bash
# Install Agenta SDK
pip install agenta

# Start Agenta locally with Docker
docker run -d -p 3000:3000 -p 8000:8000 ghcr.io/agenta-ai/agenta

# Or use pip for just the SDK
pip install agenta

# Initialize project
agenta init --app-name my-llm-app
```

## When to Use This Skill

**USE when:**
- Managing multiple versions of prompts in production
- Need systematic A/B testing of prompt variations
- Evaluating prompt quality with automated metrics
- Collaborating on prompt development across teams
- Requiring audit trails for prompt changes
- Building LLM applications that need to iterate quickly
- Need to compare different models with same prompts
- Want a playground for rapid prompt experimentation
- Self-hosting is required for security/compliance

**DON'T USE when:**
- Simple single-prompt applications
- No need for prompt versioning or testing
- Already using another prompt management system
- Rapid prototyping without evaluation needs
- Cost-sensitive projects (evaluation adds API calls)

## Prerequisites

```bash
# SDK installation
pip install agenta>=0.10.0

# For self-hosted deployment
docker pull ghcr.io/agenta-ai/agenta

# Or with docker-compose
git clone https://github.com/Agenta-AI/agenta
cd agenta
docker-compose up -d

# Environment setup
export AGENTA_HOST="http://localhost:3000"
export AGENTA_API_KEY="your-api-key"  # If using cloud version

# For LLM providers
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Verify Installation

```python
import agenta as ag
from agenta import Agenta

# Initialize client
client = Agenta()

# Check connection
print(f"Agenta SDK version: {ag.__version__}")
print("Connection successful!")
```

## Core Capabilities

### 1. Prompt Versioning and Management

**Creating Versioned Prompts:**
```python
"""
Create and manage versioned prompts with Agenta.
"""
import agenta as ag
from agenta import Agenta
from typing import Optional, Dict, Any

# Initialize Agenta
ag.init()

@ag.entrypoint
def generate_summary(
    text: str,
    max_length: int = 100,
    style: str = "professional"
) -> str:
    """
    Generate a summary with versioned prompt.

    Args:
        text: Text to summarize
        max_length: Maximum summary length
        style: Writing style (professional, casual, technical)

    Returns:
        Generated summary
    """
    # Define prompt template (this becomes versioned)
    prompt = f"""Summarize the following text in a {style} tone.
Keep the summary under {max_length} words.

Text: {text}

Summary:"""

    # Call LLM (Agenta tracks this)
    response = ag.llm.complete(
        prompt=prompt,
        model="gpt-4",
        temperature=0.3,
        max_tokens=max_length * 2
    )

    return response.text


# Example usage
text = """
The company reported strong Q3 results with revenue up 25% year-over-year.
Operating margins improved to 18% from 15% in the prior year.
The CEO highlighted expansion into new markets and product launches.
"""

summary = generate_summary(text, max_length=50, style="professional")
print(summary)
```

**Managing Prompt Versions:**
```python
"""
Manage multiple prompt versions programmatically.
"""
import agenta as ag
from agenta import Agenta
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class PromptVersion:
    """Represents a prompt version."""
    version_id: str
    name: str
    template: str
    parameters: Dict[str, Any]
    created_at: datetime
    is_active: bool = False


class PromptManager:
    """
    Manage prompt versions with Agenta.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.client = Agenta()

    def create_version(
        self,
        name: str,
        template: str,
        parameters: Dict[str, Any] = None
    ) -> PromptVersion:
        """
        Create a new prompt version.

        Args:
            name: Version name
            template: Prompt template
            parameters: Default parameters

        Returns:
            Created PromptVersion
        """
        # Create variant in Agenta
        variant = self.client.create_variant(
            app_name=self.app_name,
            variant_name=name,
            config={
                "template": template,
                "parameters": parameters or {}
            }
        )

        return PromptVersion(
            version_id=variant.id,
            name=name,
            template=template,
            parameters=parameters or {},
            created_at=datetime.now(),
            is_active=False
        )

    def list_versions(self) -> List[PromptVersion]:
        """List all prompt versions."""
        variants = self.client.list_variants(app_name=self.app_name)

        versions = []
        for v in variants:
            versions.append(PromptVersion(
                version_id=v.id,
                name=v.name,
                template=v.config.get("template", ""),
                parameters=v.config.get("parameters", {}),
                created_at=v.created_at,
                is_active=v.is_default
            ))

        return versions

    def set_active_version(self, version_id: str) -> None:
        """Set a version as the active/default version."""
        self.client.set_default_variant(
            app_name=self.app_name,
            variant_id=version_id
        )

    def get_version(self, version_id: str) -> PromptVersion:
        """Get a specific version."""
        variant = self.client.get_variant(variant_id=version_id)

        return PromptVersion(
            version_id=variant.id,
            name=variant.name,
            template=variant.config.get("template", ""),
            parameters=variant.config.get("parameters", {}),
            created_at=variant.created_at,
            is_active=variant.is_default
        )

    def compare_versions(
        self,
        version_ids: List[str],
        test_input: str
    ) -> Dict[str, str]:
        """
        Compare outputs from multiple versions.

        Args:
            version_ids: List of version IDs to compare
            test_input: Input to test with

        Returns:
            Dictionary mapping version_id to output
        """
        results = {}

        for vid in version_ids:
            version = self.get_version(vid)

            # Format prompt with test input
            prompt = version.template.format(input=test_input)

            # Generate output
            response = ag.llm.complete(prompt=prompt)
            results[vid] = response.text

        return results


# Usage
manager = PromptManager("summarizer-app")

# Create versions
v1 = manager.create_version(
    name="concise-v1",
    template="Summarize briefly: {input}",
    parameters={"max_tokens": 100}
)

v2 = manager.create_version(
    name="detailed-v2",
    template="Provide a comprehensive summary with key points: {input}",
    parameters={"max_tokens": 300}
)

# List all versions
versions = manager.list_versions()
for v in versions:
    print(f"{v.name}: {v.version_id} (active: {v.is_active})")

# Set active version
manager.set_active_version(v1.version_id)
```

### 2. A/B Testing Prompts

**Setting Up A/B Tests:**
```python
"""
Configure and run A/B tests on prompt variations.
"""
import agenta as ag
from agenta import Agenta
from typing import Dict, List, Optional
from dataclasses import dataclass
import random

@dataclass
class ABTestConfig:
    """Configuration for A/B test."""
    name: str
    variants: Dict[str, float]  # variant_id: traffic_percentage
    metrics: List[str]
    min_samples: int = 100


class ABTestRunner:
    """
    Run A/B tests on prompt variants.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.client = Agenta()
        self.results: Dict[str, List[Dict]] = {}

    def create_test(
        self,
        name: str,
        control_variant: str,
        treatment_variant: str,
        traffic_split: float = 0.5
    ) -> ABTestConfig:
        """
        Create an A/B test.

        Args:
            name: Test name
            control_variant: Control variant ID
            treatment_variant: Treatment variant ID
            traffic_split: Percentage for treatment (0-1)

        Returns:
            ABTestConfig
        """
        config = ABTestConfig(
            name=name,
            variants={
                control_variant: 1 - traffic_split,
                treatment_variant: traffic_split
            },
            metrics=["response_quality", "latency", "cost"]
        )

        # Initialize results tracking
        for variant in config.variants.keys():
            self.results[variant] = []

        return config

    def route_request(self, config: ABTestConfig) -> str:
        """
        Route a request to a variant based on traffic split.

        Args:
            config: A/B test configuration

        Returns:
            Selected variant ID
        """
        rand = random.random()
        cumulative = 0

        for variant_id, percentage in config.variants.items():
            cumulative += percentage
            if rand <= cumulative:
                return variant_id

        # Fallback to first variant
        return list(config.variants.keys())[0]

    def run_request(
        self,
        config: ABTestConfig,
        input_data: str
    ) -> Dict:
        """
        Run a single request in the A/B test.

        Args:
            config: A/B test configuration
            input_data: Input for the prompt

        Returns:
            Result dictionary with variant and output
        """
        import time

        # Route to variant
        variant_id = self.route_request(config)
        variant = self.client.get_variant(variant_id)

        # Prepare prompt
        prompt = variant.config.get("template", "").format(input=input_data)

        # Run with timing
        start_time = time.time()
        response = ag.llm.complete(prompt=prompt)
        latency = time.time() - start_time

        result = {
            "variant_id": variant_id,
            "input": input_data,
            "output": response.text,
            "latency": latency,
            "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0
        }

        # Store result
        self.results[variant_id].append(result)

        return result

    def get_test_results(self, config: ABTestConfig) -> Dict:
        """
        Get aggregated results for an A/B test.

        Args:
            config: A/B test configuration

        Returns:
            Aggregated results by variant
        """
        summary = {}

        for variant_id, results in self.results.items():
            if not results:
                continue

            latencies = [r["latency"] for r in results]
            tokens = [r["tokens_used"] for r in results]

            summary[variant_id] = {
                "sample_count": len(results),
                "avg_latency": sum(latencies) / len(latencies),
                "avg_tokens": sum(tokens) / len(tokens) if tokens else 0,
                "min_latency": min(latencies),
                "max_latency": max(latencies)
            }

        return summary

    def declare_winner(self, config: ABTestConfig) -> Optional[str]:
        """
        Analyze results and declare a winner.

        Args:
            config: A/B test configuration

        Returns:
            Winner variant ID or None if inconclusive
        """
        summary = self.get_test_results(config)

        # Check minimum samples
        for variant_id, stats in summary.items():
            if stats["sample_count"] < config.min_samples:
                print(f"Insufficient samples for {variant_id}")
                return None

        # Simple winner selection based on latency
        # In production, use statistical significance tests
        best_variant = min(
            summary.keys(),
            key=lambda v: summary[v]["avg_latency"]
        )

        return best_variant


# Usage Example
ag.init()

runner = ABTestRunner("chatbot-app")

# Create A/B test
test_config = runner.create_test(
    name="prompt-optimization-test",
    control_variant="variant-a-id",
    treatment_variant="variant-b-id",
    traffic_split=0.5
)

# Run test requests
test_inputs = [
    "What is machine learning?",
    "Explain neural networks",
    "How does backpropagation work?"
]

for input_text in test_inputs:
    result = runner.run_request(test_config, input_text)
    print(f"Variant: {result['variant_id']}, Latency: {result['latency']:.3f}s")

# Get results
results = runner.get_test_results(test_config)
print("\nTest Results:")
for variant, stats in results.items():
    print(f"  {variant}: {stats}")
```

### 3. Evaluation Metrics and Testing

**Automated Evaluation Pipeline:**
```python
"""
Evaluate prompts with automated metrics.
"""
import agenta as ag
from agenta import Agenta
from typing import List, Dict, Callable, Any
from dataclasses import dataclass
import json

@dataclass
class EvaluationResult:
    """Result of an evaluation."""
    metric_name: str
    score: float
    details: Dict[str, Any]


class MetricEvaluator:
    """Base class for evaluation metrics."""

    def __init__(self, name: str):
        self.name = name

    def evaluate(
        self,
        output: str,
        expected: str = None,
        context: Dict = None
    ) -> EvaluationResult:
        raise NotImplementedError


class ExactMatchMetric(MetricEvaluator):
    """Exact match evaluation."""

    def __init__(self):
        super().__init__("exact_match")

    def evaluate(self, output: str, expected: str = None, context: Dict = None) -> EvaluationResult:
        if expected is None:
            return EvaluationResult(self.name, 0.0, {"error": "No expected value"})

        match = output.strip().lower() == expected.strip().lower()

        return EvaluationResult(
            metric_name=self.name,
            score=1.0 if match else 0.0,
            details={"match": match}
        )


class ContainsMetric(MetricEvaluator):
    """Check if output contains expected keywords."""

    def __init__(self, keywords: List[str]):
        super().__init__("contains_keywords")
        self.keywords = keywords

    def evaluate(self, output: str, expected: str = None, context: Dict = None) -> EvaluationResult:
        output_lower = output.lower()
        found = [kw for kw in self.keywords if kw.lower() in output_lower]
        score = len(found) / len(self.keywords)

        return EvaluationResult(
            metric_name=self.name,
            score=score,
            details={
                "found_keywords": found,
                "missing_keywords": [kw for kw in self.keywords if kw.lower() not in output_lower]
            }
        )


class LengthMetric(MetricEvaluator):
    """Evaluate output length."""

    def __init__(self, min_length: int = 10, max_length: int = 500):
        super().__init__("length")
        self.min_length = min_length
        self.max_length = max_length

    def evaluate(self, output: str, expected: str = None, context: Dict = None) -> EvaluationResult:
        length = len(output.split())

        if self.min_length <= length <= self.max_length:
            score = 1.0
        elif length < self.min_length:
            score = length / self.min_length
        else:
            score = max(0, 1 - (length - self.max_length) / self.max_length)

        return EvaluationResult(
            metric_name=self.name,
            score=score,
            details={
                "word_count": length,
                "min_length": self.min_length,
                "max_length": self.max_length
            }
        )


class LLMJudgeMetric(MetricEvaluator):
    """Use an LLM to judge output quality."""

    def __init__(self, criteria: str = "helpfulness"):
        super().__init__(f"llm_judge_{criteria}")
        self.criteria = criteria

    def evaluate(self, output: str, expected: str = None, context: Dict = None) -> EvaluationResult:
        judge_prompt = f"""Evaluate the following response on {self.criteria}.
Score from 0.0 to 1.0.

Response:
{output}

{f'Expected: {expected}' if expected else ''}

Provide your evaluation as JSON: {{"score": 0.0-1.0, "reasoning": "..."}}
"""

        response = ag.llm.complete(
            prompt=judge_prompt,
            model="gpt-4",
            temperature=0
        )

        try:
            result = json.loads(response.text)
            score = float(result.get("score", 0.5))
            reasoning = result.get("reasoning", "")
        except (json.JSONDecodeError, ValueError):
            score = 0.5
            reasoning = "Failed to parse judge response"

        return EvaluationResult(
            metric_name=self.name,
            score=score,
            details={"reasoning": reasoning, "criteria": self.criteria}
        )


class EvaluationPipeline:
    """
    Pipeline for running multiple evaluations.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.client = Agenta()
        self.metrics: List[MetricEvaluator] = []

    def add_metric(self, metric: MetricEvaluator) -> 'EvaluationPipeline':
        """Add a metric to the pipeline."""
        self.metrics.append(metric)
        return self

    def evaluate_single(
        self,
        output: str,
        expected: str = None,
        context: Dict = None
    ) -> Dict[str, EvaluationResult]:
        """
        Evaluate a single output with all metrics.

        Args:
            output: Generated output
            expected: Expected output (optional)
            context: Additional context

        Returns:
            Dictionary of metric results
        """
        results = {}

        for metric in self.metrics:
            result = metric.evaluate(output, expected, context)
            results[metric.name] = result

        return results

    def evaluate_batch(
        self,
        test_cases: List[Dict]
    ) -> Dict[str, List[EvaluationResult]]:
        """
        Evaluate a batch of test cases.

        Args:
            test_cases: List of {input, output, expected} dicts

        Returns:
            Aggregated results by metric
        """
        all_results = {metric.name: [] for metric in self.metrics}

        for case in test_cases:
            results = self.evaluate_single(
                output=case.get("output", ""),
                expected=case.get("expected"),
                context=case.get("context")
            )

            for metric_name, result in results.items():
                all_results[metric_name].append(result)

        return all_results

    def get_summary(self, batch_results: Dict[str, List[EvaluationResult]]) -> Dict:
        """
        Get summary statistics from batch evaluation.

        Args:
            batch_results: Results from evaluate_batch

        Returns:
            Summary statistics
        """
        summary = {}

        for metric_name, results in batch_results.items():
            scores = [r.score for r in results]
            summary[metric_name] = {
                "mean": sum(scores) / len(scores) if scores else 0,
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 0,
                "count": len(scores)
            }

        return summary


# Usage
ag.init()

# Create evaluation pipeline
pipeline = EvaluationPipeline("qa-bot")
pipeline.add_metric(ContainsMetric(["answer", "explanation"]))
pipeline.add_metric(LengthMetric(min_length=20, max_length=200))
pipeline.add_metric(LLMJudgeMetric(criteria="helpfulness"))

# Test cases
test_cases = [
    {
        "input": "What is Python?",
        "output": "Python is a programming language known for its simplicity. The answer is that it's versatile. Here's an explanation: it's widely used in data science and web development.",
        "expected": "Python is a high-level programming language"
    },
    {
        "input": "Explain recursion",
        "output": "Recursion is a function calling itself. The answer involves base cases and recursive calls. Explanation: it's useful for tree structures.",
        "expected": "A function that calls itself"
    }
]

# Run evaluation
results = pipeline.evaluate_batch(test_cases)
summary = pipeline.get_summary(results)

print("Evaluation Summary:")
for metric, stats in summary.items():
    print(f"  {metric}: mean={stats['mean']:.2f}, min={stats['min']:.2f}, max={stats['max']:.2f}")
```

### 4. Playground and Experimentation

**Creating Interactive Playground:**
```python
"""
Build an interactive playground for prompt experimentation.
"""
import agenta as ag
from agenta import Agenta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class ExperimentRun:
    """Single experiment run."""
    run_id: str
    prompt: str
    parameters: Dict[str, Any]
    output: str
    metrics: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.now)


class Playground:
    """
    Interactive playground for prompt experimentation.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.client = Agenta()
        self.experiments: List[ExperimentRun] = []
        self.current_prompt = ""
        self.current_params = {}

    def set_prompt(self, prompt: str) -> 'Playground':
        """Set the current prompt template."""
        self.current_prompt = prompt
        return self

    def set_parameters(self, **params) -> 'Playground':
        """Set LLM parameters."""
        self.current_params.update(params)
        return self

    def run(self, input_data: str) -> ExperimentRun:
        """
        Run the current prompt with input.

        Args:
            input_data: Input to format into prompt

        Returns:
            ExperimentRun with results
        """
        import time
        import uuid

        # Format prompt
        formatted_prompt = self.current_prompt.format(input=input_data)

        # Run with timing
        start_time = time.time()
        response = ag.llm.complete(
            prompt=formatted_prompt,
            **self.current_params
        )
        latency = time.time() - start_time

        # Create run record
        run = ExperimentRun(
            run_id=str(uuid.uuid4())[:8],
            prompt=formatted_prompt,
            parameters=self.current_params.copy(),
            output=response.text,
            metrics={
                "latency": latency,
                "output_length": len(response.text),
                "tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
        )

        self.experiments.append(run)

        return run

    def compare(
        self,
        prompts: List[str],
        test_input: str,
        parameters: Dict = None
    ) -> List[ExperimentRun]:
        """
        Compare multiple prompts with same input.

        Args:
            prompts: List of prompt templates
            test_input: Input to test
            parameters: Shared parameters

        Returns:
            List of ExperimentRuns
        """
        runs = []
        original_prompt = self.current_prompt
        original_params = self.current_params.copy()

        if parameters:
            self.set_parameters(**parameters)

        for prompt in prompts:
            self.set_prompt(prompt)
            run = self.run(test_input)
            runs.append(run)

        # Restore original state
        self.current_prompt = original_prompt
        self.current_params = original_params

        return runs

    def parameter_sweep(
        self,
        param_name: str,
        values: List[Any],
        test_input: str
    ) -> List[ExperimentRun]:
        """
        Sweep over parameter values.

        Args:
            param_name: Parameter to sweep
            values: List of values to try
            test_input: Input for testing

        Returns:
            List of ExperimentRuns
        """
        runs = []
        original_value = self.current_params.get(param_name)

        for value in values:
            self.current_params[param_name] = value
            run = self.run(test_input)
            runs.append(run)

        # Restore original value
        if original_value is not None:
            self.current_params[param_name] = original_value
        else:
            self.current_params.pop(param_name, None)

        return runs

    def get_history(self, limit: int = 10) -> List[ExperimentRun]:
        """Get recent experiment history."""
        return self.experiments[-limit:]

    def export_experiments(self, filepath: str) -> None:
        """Export experiments to JSON file."""
        data = []
        for exp in self.experiments:
            data.append({
                "run_id": exp.run_id,
                "prompt": exp.prompt,
                "parameters": exp.parameters,
                "output": exp.output,
                "metrics": exp.metrics,
                "timestamp": exp.timestamp.isoformat()
            })

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def find_best_run(self, metric: str = "latency", minimize: bool = True) -> Optional[ExperimentRun]:
        """
        Find the best run based on a metric.

        Args:
            metric: Metric to optimize
            minimize: Whether to minimize (True) or maximize (False)

        Returns:
            Best ExperimentRun or None
        """
        if not self.experiments:
            return None

        valid_runs = [e for e in self.experiments if metric in e.metrics]

        if not valid_runs:
            return None

        if minimize:
            return min(valid_runs, key=lambda e: e.metrics[metric])
        else:
            return max(valid_runs, key=lambda e: e.metrics[metric])


# Usage
ag.init()

playground = Playground("experiment-app")

# Set up experiment
playground.set_prompt("Answer this question concisely: {input}")
playground.set_parameters(model="gpt-4", temperature=0.3, max_tokens=100)

# Run single experiment
run = playground.run("What is machine learning?")
print(f"Output: {run.output}")
print(f"Latency: {run.metrics['latency']:.3f}s")

# Compare prompts
comparison_runs = playground.compare(
    prompts=[
        "Answer briefly: {input}",
        "Explain in detail: {input}",
        "Give a one-sentence answer: {input}"
    ],
    test_input="What is deep learning?"
)

print("\nPrompt Comparison:")
for i, run in enumerate(comparison_runs):
    print(f"  Prompt {i+1}: {run.metrics['latency']:.3f}s, {run.metrics['output_length']} chars")

# Parameter sweep
temperature_runs = playground.parameter_sweep(
    param_name="temperature",
    values=[0.0, 0.3, 0.7, 1.0],
    test_input="Write a creative story opening"
)

print("\nTemperature Sweep:")
for run in temperature_runs:
    print(f"  temp={run.parameters['temperature']}: {run.output[:50]}...")

# Find best run
best = playground.find_best_run(metric="latency", minimize=True)
if best:
    print(f"\nBest run: {best.run_id} with latency {best.metrics['latency']:.3f}s")

# Export experiments
playground.export_experiments("experiments.json")
```

### 5. Model Comparison

**Comparing Different LLM Models:**
```python
"""
Compare performance across different LLM models.
"""
import agenta as ag
from agenta import Agenta
from typing import Dict, List, Any
from dataclasses import dataclass
import time

@dataclass
class ModelResult:
    """Result from a single model run."""
    model: str
    output: str
    latency: float
    tokens: int
    cost: float


class ModelComparator:
    """
    Compare prompts across different models.
    """

    # Cost per 1K tokens (approximate)
    MODEL_COSTS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125}
    }

    def __init__(self, models: List[str] = None):
        self.models = models or ["gpt-4", "gpt-3.5-turbo"]
        self.results: Dict[str, List[ModelResult]] = {m: [] for m in self.models}

    def _estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a model run."""
        costs = self.MODEL_COSTS.get(model, {"input": 0.01, "output": 0.03})
        return (input_tokens / 1000 * costs["input"] +
                output_tokens / 1000 * costs["output"])

    def run_comparison(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 200
    ) -> Dict[str, ModelResult]:
        """
        Run the same prompt across all models.

        Args:
            prompt: Prompt to test
            temperature: Temperature setting
            max_tokens: Maximum output tokens

        Returns:
            Results for each model
        """
        results = {}

        for model in self.models:
            start_time = time.time()

            try:
                response = ag.llm.complete(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                latency = time.time() - start_time

                # Get token counts
                input_tokens = len(prompt.split()) * 1.3  # Rough estimate
                output_tokens = len(response.text.split()) * 1.3

                if hasattr(response, 'usage'):
                    input_tokens = response.usage.prompt_tokens
                    output_tokens = response.usage.completion_tokens

                result = ModelResult(
                    model=model,
                    output=response.text,
                    latency=latency,
                    tokens=int(input_tokens + output_tokens),
                    cost=self._estimate_cost(model, input_tokens, output_tokens)
                )

            except Exception as e:
                result = ModelResult(
                    model=model,
                    output=f"Error: {str(e)}",
                    latency=0,
                    tokens=0,
                    cost=0
                )

            results[model] = result
            self.results[model].append(result)

        return results

    def run_benchmark(
        self,
        prompts: List[str],
        temperature: float = 0.3
    ) -> Dict[str, Dict]:
        """
        Run benchmark across multiple prompts.

        Args:
            prompts: List of prompts to test
            temperature: Temperature setting

        Returns:
            Aggregated benchmark results
        """
        for prompt in prompts:
            self.run_comparison(prompt, temperature)

        return self.get_summary()

    def get_summary(self) -> Dict[str, Dict]:
        """Get summary statistics for all models."""
        summary = {}

        for model, results in self.results.items():
            if not results:
                continue

            valid_results = [r for r in results if r.latency > 0]

            if not valid_results:
                continue

            summary[model] = {
                "runs": len(valid_results),
                "avg_latency": sum(r.latency for r in valid_results) / len(valid_results),
                "avg_tokens": sum(r.tokens for r in valid_results) / len(valid_results),
                "total_cost": sum(r.cost for r in valid_results),
                "min_latency": min(r.latency for r in valid_results),
                "max_latency": max(r.latency for r in valid_results)
            }

        return summary

    def recommend_model(
        self,
        priority: str = "balanced"
    ) -> str:
        """
        Recommend best model based on priority.

        Args:
            priority: "speed", "cost", "quality", or "balanced"

        Returns:
            Recommended model name
        """
        summary = self.get_summary()

        if not summary:
            return self.models[0]

        if priority == "speed":
            return min(summary.keys(), key=lambda m: summary[m]["avg_latency"])
        elif priority == "cost":
            return min(summary.keys(), key=lambda m: summary[m]["total_cost"])
        elif priority == "quality":
            # Assume larger models = better quality
            quality_order = ["gpt-4", "claude-3-opus", "gpt-4-turbo", "claude-3-sonnet", "gpt-3.5-turbo"]
            for model in quality_order:
                if model in summary:
                    return model
        else:  # balanced
            # Score based on normalized latency and cost
            scores = {}
            max_latency = max(s["avg_latency"] for s in summary.values())
            max_cost = max(s["total_cost"] for s in summary.values()) or 1

            for model, stats in summary.items():
                norm_latency = stats["avg_latency"] / max_latency
                norm_cost = stats["total_cost"] / max_cost
                scores[model] = norm_latency * 0.5 + norm_cost * 0.5

            return min(scores.keys(), key=lambda m: scores[m])

        return self.models[0]


# Usage
ag.init()

comparator = ModelComparator(models=["gpt-4", "gpt-3.5-turbo"])

# Single comparison
results = comparator.run_comparison("Explain quantum computing in simple terms")

print("Single Comparison Results:")
for model, result in results.items():
    print(f"  {model}:")
    print(f"    Latency: {result.latency:.3f}s")
    print(f"    Tokens: {result.tokens}")
    print(f"    Cost: ${result.cost:.4f}")
    print(f"    Output: {result.output[:100]}...")

# Benchmark
benchmark_prompts = [
    "What is machine learning?",
    "Explain the difference between AI and ML",
    "Write a haiku about technology"
]

comparator.run_benchmark(benchmark_prompts)

print("\nBenchmark Summary:")
summary = comparator.get_summary()
for model, stats in summary.items():
    print(f"  {model}:")
    print(f"    Runs: {stats['runs']}")
    print(f"    Avg Latency: {stats['avg_latency']:.3f}s")
    print(f"    Total Cost: ${stats['total_cost']:.4f}")

# Get recommendation
recommended = comparator.recommend_model(priority="balanced")
print(f"\nRecommended model (balanced): {recommended}")
```

### 6. Self-Hosted Deployment

**Setting Up Self-Hosted Agenta:**
```python
"""
Configure and manage self-hosted Agenta deployment.
"""
import agenta as ag
from agenta import Agenta
from typing import Dict, Any, Optional
import os
import requests
from dataclasses import dataclass

@dataclass
class DeploymentConfig:
    """Configuration for self-hosted deployment."""
    host: str
    port: int
    api_key: Optional[str]
    database_url: str
    redis_url: Optional[str]
    enable_tracing: bool = True


class SelfHostedManager:
    """
    Manage self-hosted Agenta deployment.
    """

    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.base_url = f"http://{config.host}:{config.port}"
        self.client = None

    def initialize(self) -> bool:
        """
        Initialize connection to self-hosted instance.

        Returns:
            True if successful
        """
        try:
            # Set environment for SDK
            os.environ["AGENTA_HOST"] = self.base_url
            if self.config.api_key:
                os.environ["AGENTA_API_KEY"] = self.config.api_key

            # Initialize Agenta
            ag.init()
            self.client = Agenta()

            # Test connection
            response = requests.get(f"{self.base_url}/api/health")
            return response.status_code == 200

        except Exception as e:
            print(f"Initialization failed: {e}")
            return False

    def create_app(
        self,
        name: str,
        description: str = ""
    ) -> Dict:
        """
        Create a new application.

        Args:
            name: Application name
            description: Application description

        Returns:
            Created application details
        """
        return self.client.create_app(
            name=name,
            description=description
        )

    def deploy_variant(
        self,
        app_name: str,
        variant_name: str,
        environment: str = "production"
    ) -> Dict:
        """
        Deploy a variant to an environment.

        Args:
            app_name: Application name
            variant_name: Variant to deploy
            environment: Target environment

        Returns:
            Deployment details
        """
        # Get variant
        variants = self.client.list_variants(app_name=app_name)
        variant = next((v for v in variants if v.name == variant_name), None)

        if not variant:
            raise ValueError(f"Variant '{variant_name}' not found")

        # Deploy
        return self.client.deploy_variant(
            variant_id=variant.id,
            environment=environment
        )

    def get_deployment_status(self, app_name: str) -> Dict:
        """
        Get deployment status for an application.

        Args:
            app_name: Application name

        Returns:
            Deployment status
        """
        response = requests.get(
            f"{self.base_url}/api/apps/{app_name}/deployments",
            headers={"Authorization": f"Bearer {self.config.api_key}"} if self.config.api_key else {}
        )

        return response.json()

    def configure_observability(
        self,
        tracing_endpoint: str = None,
        metrics_endpoint: str = None
    ) -> None:
        """
        Configure observability endpoints.

        Args:
            tracing_endpoint: Endpoint for traces (e.g., Jaeger)
            metrics_endpoint: Endpoint for metrics (e.g., Prometheus)
        """
        config = {}

        if tracing_endpoint:
            config["tracing"] = {
                "enabled": True,
                "endpoint": tracing_endpoint
            }

        if metrics_endpoint:
            config["metrics"] = {
                "enabled": True,
                "endpoint": metrics_endpoint
            }

        response = requests.post(
            f"{self.base_url}/api/config/observability",
            json=config,
            headers={"Authorization": f"Bearer {self.config.api_key}"} if self.config.api_key else {}
        )

        if response.status_code != 200:
            raise Exception(f"Failed to configure observability: {response.text}")


def generate_docker_compose(config: DeploymentConfig) -> str:
    """
    Generate docker-compose.yml for self-hosted deployment.

    Args:
        config: Deployment configuration

    Returns:
        Docker compose YAML content
    """
    compose = f"""version: '3.8'

services:
  agenta-backend:
    image: ghcr.io/agenta-ai/agenta-backend:latest
    ports:
      - "{config.port}:8000"
    environment:
      - DATABASE_URL={config.database_url}
      - REDIS_URL={config.redis_url or "redis://redis:6379"}
      - ENABLE_TRACING={str(config.enable_tracing).lower()}
    depends_on:
      - postgres
      - redis

  agenta-frontend:
    image: ghcr.io/agenta-ai/agenta-frontend:latest
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://agenta-backend:8000

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=agenta
      - POSTGRES_USER=agenta
      - POSTGRES_PASSWORD=agenta_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""
    return compose


# Usage
config = DeploymentConfig(
    host="localhost",
    port=8000,
    api_key=None,  # Optional for local deployment
    database_url="postgresql://agenta:agenta_password@postgres:5432/agenta",
    redis_url="redis://redis:6379",
    enable_tracing=True
)

# Generate docker-compose
compose_yaml = generate_docker_compose(config)
print("Docker Compose Configuration:")
print(compose_yaml)

# Initialize manager (after deploying with docker-compose)
# manager = SelfHostedManager(config)
# if manager.initialize():
#     print("Connected to self-hosted Agenta!")
#
#     # Create app
#     app = manager.create_app("my-llm-app", "Production LLM application")
#
#     # Deploy variant
#     deployment = manager.deploy_variant("my-llm-app", "v1", "production")
#     print(f"Deployed: {deployment}")
```

## Integration Examples

### FastAPI Integration

```python
"""
Integrate Agenta with FastAPI for production deployments.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import agenta as ag
from agenta import Agenta

app = FastAPI(title="Agenta-Powered API")

# Initialize Agenta
ag.init()
client = Agenta()


class QueryRequest(BaseModel):
    """Request model for queries."""
    input: str
    variant: Optional[str] = None
    parameters: Optional[dict] = None


class QueryResponse(BaseModel):
    """Response model."""
    output: str
    variant_used: str
    latency: float


@app.post("/generate", response_model=QueryResponse)
async def generate(request: QueryRequest):
    """Generate response using Agenta-managed prompts."""
    import time

    try:
        # Get variant (default or specified)
        if request.variant:
            variant = client.get_variant_by_name(
                app_name="production-app",
                variant_name=request.variant
            )
        else:
            variant = client.get_default_variant(app_name="production-app")

        # Get prompt template
        template = variant.config.get("template", "{input}")
        prompt = template.format(input=request.input)

        # Get parameters
        params = variant.config.get("parameters", {})
        if request.parameters:
            params.update(request.parameters)

        # Generate
        start_time = time.time()
        response = ag.llm.complete(prompt=prompt, **params)
        latency = time.time() - start_time

        return QueryResponse(
            output=response.text,
            variant_used=variant.name,
            latency=latency
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/variants")
async def list_variants():
    """List available variants."""
    variants = client.list_variants(app_name="production-app")
    return [{"name": v.name, "id": v.id, "is_default": v.is_default} for v in variants]


# Run with: uvicorn api:app --reload
```

### Langchain Integration

```python
"""
Use Agenta for prompt management in Langchain applications.
"""
import agenta as ag
from agenta import Agenta
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any

class AgentaPromptLoader:
    """
    Load prompts from Agenta into Langchain.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.client = Agenta()
        self._cache: Dict[str, PromptTemplate] = {}

    def get_prompt(
        self,
        variant_name: str = None,
        use_cache: bool = True
    ) -> PromptTemplate:
        """
        Get a Langchain PromptTemplate from Agenta.

        Args:
            variant_name: Variant to load (None for default)
            use_cache: Whether to use cached prompts

        Returns:
            Langchain PromptTemplate
        """
        cache_key = variant_name or "default"

        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        # Get variant from Agenta
        if variant_name:
            variant = self.client.get_variant_by_name(
                app_name=self.app_name,
                variant_name=variant_name
            )
        else:
            variant = self.client.get_default_variant(app_name=self.app_name)

        # Create Langchain prompt
        template = variant.config.get("template", "{input}")
        prompt = PromptTemplate.from_template(template)

        # Cache
        self._cache[cache_key] = prompt

        return prompt

    def create_chain(
        self,
        variant_name: str = None,
        model: str = "gpt-4",
        temperature: float = 0.3
    ):
        """
        Create a Langchain chain from Agenta prompt.

        Args:
            variant_name: Variant to use
            model: Model name
            temperature: Temperature setting

        Returns:
            Langchain chain
        """
        prompt = self.get_prompt(variant_name)
        llm = ChatOpenAI(model=model, temperature=temperature)

        return prompt | llm | StrOutputParser()


# Usage
ag.init()

loader = AgentaPromptLoader("qa-app")

# Get prompt template
prompt = loader.get_prompt("concise-v1")
print(f"Template: {prompt.template}")

# Create and use chain
chain = loader.create_chain(variant_name="detailed-v2")
result = chain.invoke({"input": "What is machine learning?"})
print(f"Result: {result}")
```

## Best Practices

### 1. Prompt Versioning Strategy

```python
"""Best practices for prompt versioning."""

# DO: Use semantic versioning for prompts
version_naming = {
    "v1.0.0": "Initial production version",
    "v1.1.0": "Added context handling",
    "v1.1.1": "Fixed edge case in formatting",
    "v2.0.0": "Major rewrite with new approach"
}

# DO: Include metadata with versions
def create_versioned_prompt(name: str, template: str, metadata: dict):
    return {
        "name": name,
        "template": template,
        "metadata": {
            "created_by": metadata.get("author"),
            "description": metadata.get("description"),
            "changelog": metadata.get("changelog"),
            "test_results": metadata.get("test_results")
        }
    }

# DO: Test before promoting to production
def promote_to_production(variant_id: str, min_eval_score: float = 0.8):
    # Run evaluation
    score = run_evaluation(variant_id)

    if score >= min_eval_score:
        client.set_default_variant(variant_id)
        return True
    return False
```

### 2. Evaluation Strategy

```python
"""Best practices for prompt evaluation."""

# DO: Define clear evaluation criteria
evaluation_criteria = {
    "accuracy": {"weight": 0.4, "threshold": 0.8},
    "relevance": {"weight": 0.3, "threshold": 0.7},
    "coherence": {"weight": 0.2, "threshold": 0.7},
    "safety": {"weight": 0.1, "threshold": 0.9}
}

# DO: Use diverse test sets
def create_evaluation_set():
    return [
        {"input": "...", "expected": "...", "category": "basic"},
        {"input": "...", "expected": "...", "category": "edge_case"},
        {"input": "...", "expected": "...", "category": "adversarial"}
    ]

# DO: Track evaluation over time
def track_evaluation_history(app_name: str, variant_id: str, results: dict):
    # Store results with timestamp for trend analysis
    pass
```

### 3. A/B Testing Guidelines

```python
"""Best practices for A/B testing prompts."""

# DO: Calculate required sample size
def calculate_sample_size(
    baseline_metric: float,
    minimum_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.8
) -> int:
    # Statistical calculation for required samples
    pass

# DO: Use proper statistical tests
def analyze_ab_test(control_results: list, treatment_results: list):
    from scipy import stats

    # T-test for continuous metrics
    t_stat, p_value = stats.ttest_ind(control_results, treatment_results)

    return {
        "significant": p_value < 0.05,
        "p_value": p_value,
        "effect_size": (sum(treatment_results)/len(treatment_results) -
                       sum(control_results)/len(control_results))
    }
```

## Troubleshooting

### Connection Issues

```python
# Problem: Cannot connect to Agenta host
# Solution: Verify host and network settings

def diagnose_connection(host: str):
    import requests

    try:
        response = requests.get(f"{host}/api/health", timeout=5)
        if response.status_code == 200:
            print("Connection successful")
        else:
            print(f"Server returned: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Cannot reach server - check host/port")
    except requests.exceptions.Timeout:
        print("Connection timed out - server may be overloaded")
```

### Evaluation Failures

```python
# Problem: Evaluations failing or inconsistent
# Solution: Add retry logic and validation

def robust_evaluation(prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = ag.llm.complete(prompt=prompt)
            if validate_result(result):
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Version Conflicts

```python
# Problem: Multiple team members editing same variant
# Solution: Use branching strategy

def create_branch_variant(base_variant: str, branch_name: str):
    # Clone variant for isolated development
    base = client.get_variant_by_name(app_name, base_variant)
    return client.create_variant(
        app_name=app_name,
        variant_name=f"{base_variant}-{branch_name}",
        config=base.config
    )
```

## Resources

- **Agenta Documentation**: https://docs.agenta.ai/
- **GitHub Repository**: https://github.com/Agenta-AI/agenta
- **Self-Hosting Guide**: https://docs.agenta.ai/self-hosting
- **API Reference**: https://docs.agenta.ai/api-reference

## Version History

- **1.0.0** (2026-01-17): Initial release with versioning, A/B testing, evaluation, playground, model comparison, self-hosting

---

*This skill provides comprehensive patterns for LLM prompt management with Agenta, refined from production prompt engineering workflows.*
