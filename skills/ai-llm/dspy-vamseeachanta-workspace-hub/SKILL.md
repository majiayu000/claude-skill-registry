---
name: dspy
description: Compile prompts into self-improving pipelines with signatures, modules, optimizers, and programmatic prompt engineering
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
  - signature_definition
  - module_composition
  - prompt_optimization
  - few_shot_learning
  - chain_of_thought
  - retrieval_integration
  - metric_evaluation
  - pipeline_compilation
tools:
  - Read
  - Write
  - Bash
  - Grep
tags: [dspy, prompt-optimization, llm, signatures, modules, optimizers, few-shot, chain-of-thought]
platforms: [python]
related_skills:
  - langchain
  - prompt-engineering
---

# DSPy Skill

> Compile prompts into self-improving pipelines with programmatic prompt engineering.

## Quick Start

```bash
# Install DSPy
pip install dspy-ai

# Optional: For retrieval
pip install chromadb faiss-cpu

# Set API key
export OPENAI_API_KEY="your-api-key"
```

## When to Use This Skill

**USE when:**
- Need to optimize prompts programmatically rather than manually
- Building pipelines where prompt quality is critical to success
- Want reproducible, testable prompt engineering
- Working with complex multi-step reasoning tasks
- Need to automatically find effective few-shot examples
- Building systems that improve with more training data
- Require systematic evaluation and comparison of prompt strategies
- Want to abstract away prompt engineering from application logic

**DON'T USE when:**
- Simple single-shot prompts that work well as-is
- Need fine-grained control over exact prompt wording
- Building applications with minimal LLM interactions
- Prototyping where rapid iteration is more important than optimization
- Resource-constrained environments (optimization requires API calls)

## Prerequisites

```bash
# Core installation
pip install dspy-ai>=2.4.0

# For vector retrieval
pip install chromadb>=0.4.0 faiss-cpu>=1.7.0

# For different LLM providers
pip install openai>=1.0.0 anthropic>=0.5.0

# For evaluation
pip install pandas>=2.0.0 scikit-learn>=1.0.0

# Environment setup
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Core Concepts

### DSPy Philosophy

DSPy treats prompts as **programs** rather than strings:

1. **Signatures** define input/output specifications
2. **Modules** implement reasoning patterns
3. **Optimizers** automatically improve prompts
4. **Metrics** evaluate performance

```
Traditional: "Write prompt" -> "Test" -> "Manually adjust" -> "Repeat"
DSPy:        "Define signature" -> "Compile with optimizer" -> "Deploy optimized prompt"
```

## Core Capabilities

### 1. Signatures

**Basic Signatures:**
```python
import dspy

# Configure LLM
lm = dspy.OpenAI(model="gpt-4", max_tokens=1000)
dspy.settings.configure(lm=lm)

# Inline signature (simple)
classify = dspy.Predict("document -> category")
result = classify(document="The mooring line tension exceeded limits.")
print(result.category)

# Class-based signature (recommended)
class SentimentAnalysis(dspy.Signature):
    """Analyze the sentiment of engineering feedback."""

    feedback = dspy.InputField(desc="Engineering feedback or review text")
    sentiment = dspy.OutputField(desc="Sentiment: positive, negative, or neutral")
    confidence = dspy.OutputField(desc="Confidence score 0-1")

# Use signature
analyzer = dspy.Predict(SentimentAnalysis)
result = analyzer(feedback="The mooring design passed all safety checks.")
print(f"Sentiment: {result.sentiment}, Confidence: {result.confidence}")
```

**Complex Signatures with Multiple Fields:**
```python
class EngineeringAnalysis(dspy.Signature):
    """Analyze an engineering report and extract key insights."""

    report_text = dspy.InputField(
        desc="Full text of the engineering report"
    )
    domain = dspy.InputField(
        desc="Engineering domain (offshore, structural, mechanical)"
    )

    summary = dspy.OutputField(
        desc="Concise 2-3 sentence summary of findings"
    )
    key_metrics = dspy.OutputField(
        desc="List of key metrics mentioned with values"
    )
    risk_factors = dspy.OutputField(
        desc="Identified risk factors and concerns"
    )
    recommendations = dspy.OutputField(
        desc="Actionable recommendations from the report"
    )
    confidence_level = dspy.OutputField(
        desc="Overall confidence in analysis: high, medium, or low"
    )

# Create predictor
report_analyzer = dspy.Predict(EngineeringAnalysis)

# Analyze report
result = report_analyzer(
    report_text="""
    The mooring analysis for Platform Alpha shows maximum tensions
    of 2,450 kN under 100-year storm conditions. Safety factors
    range from 1.72 to 2.15 across all lines. Line 3 shows the
    lowest margin at the fairlead connection. Fatigue life estimates
    indicate 35-year service life, exceeding the 25-year requirement.
    Chain wear measurements show 8% diameter loss after 5 years.
    """,
    domain="offshore"
)

print(f"Summary: {result.summary}")
print(f"Key Metrics: {result.key_metrics}")
print(f"Risk Factors: {result.risk_factors}")
print(f"Recommendations: {result.recommendations}")
```

### 2. Modules

**ChainOfThought for Complex Reasoning:**
```python
class TechnicalQA(dspy.Signature):
    """Answer technical engineering questions with reasoning."""

    context = dspy.InputField(desc="Technical context and background")
    question = dspy.InputField(desc="Technical question to answer")
    answer = dspy.OutputField(desc="Detailed technical answer")

# ChainOfThought adds reasoning before answering
class TechnicalExpert(dspy.Module):
    def __init__(self):
        super().__init__()
        self.answer_question = dspy.ChainOfThought(TechnicalQA)

    def forward(self, context, question):
        result = self.answer_question(context=context, question=question)
        return result

# Usage
expert = TechnicalExpert()

result = expert(
    context="""
    Catenary mooring systems use the weight of the chain to provide
    restoring force. The touchdown point moves as the vessel offsets.
    Line tension is a function of the catenary geometry and pretension.
    """,
    question="How does water depth affect mooring line tension?"
)

print(f"Reasoning: {result.rationale}")
print(f"Answer: {result.answer}")
```

**Multi-Stage Pipeline Module:**
```python
class DocumentSummary(dspy.Signature):
    """Summarize a technical document."""
    document = dspy.InputField()
    summary = dspy.OutputField()

class KeyPointExtraction(dspy.Signature):
    """Extract key points from a summary."""
    summary = dspy.InputField()
    key_points = dspy.OutputField(desc="List of 3-5 key points")

class ActionItemGeneration(dspy.Signature):
    """Generate action items from key points."""
    key_points = dspy.InputField()
    action_items = dspy.OutputField(desc="List of actionable next steps")

class DocumentProcessor(dspy.Module):
    """Multi-stage document processing pipeline."""

    def __init__(self):
        super().__init__()
        self.summarize = dspy.ChainOfThought(DocumentSummary)
        self.extract_points = dspy.Predict(KeyPointExtraction)
        self.generate_actions = dspy.Predict(ActionItemGeneration)

    def forward(self, document):
        # Stage 1: Summarize
        summary_result = self.summarize(document=document)

        # Stage 2: Extract key points
        points_result = self.extract_points(summary=summary_result.summary)

        # Stage 3: Generate actions
        actions_result = self.generate_actions(key_points=points_result.key_points)

        return dspy.Prediction(
            summary=summary_result.summary,
            key_points=points_result.key_points,
            action_items=actions_result.action_items
        )

# Usage
processor = DocumentProcessor()
result = processor(document="[Long engineering document text...]")

print(f"Summary: {result.summary}")
print(f"Key Points: {result.key_points}")
print(f"Actions: {result.action_items}")
```

**ReAct Module for Tool Use:**
```python
class CalculateTension(dspy.Signature):
    """Calculate mooring line tension."""
    depth = dspy.InputField(desc="Water depth in meters")
    line_length = dspy.InputField(desc="Line length in meters")
    pretension = dspy.InputField(desc="Pretension in kN")
    result = dspy.OutputField(desc="Tension calculation result")

class SearchStandards(dspy.Signature):
    """Search engineering standards database."""
    query = dspy.InputField(desc="Search query")
    standards = dspy.OutputField(desc="Relevant standards found")

class EngineeringReActAgent(dspy.Module):
    """Agent that can reason and act using tools."""

    def __init__(self):
        super().__init__()
        self.react = dspy.ReAct(
            signature="question -> answer",
            tools=[self.calculate_tension, self.search_standards]
        )

    def calculate_tension(self, depth: float, line_length: float, pretension: float) -> str:
        """Calculate approximate mooring line tension."""
        import math
        suspended = math.sqrt(line_length**2 - depth**2)
        tension = pretension * (1 + depth / suspended * 0.1)
        return f"Estimated tension: {tension:.1f} kN"

    def search_standards(self, query: str) -> str:
        """Search for relevant engineering standards."""
        standards_db = {
            "mooring": ["API RP 2SK", "DNV-OS-E301", "ISO 19901-7"],
            "fatigue": ["DNV-RP-C203", "API RP 2A-WSD"],
            "structural": ["AISC 360", "API RP 2A-WSD"]
        }
        for key, value in standards_db.items():
            if key in query.lower():
                return f"Relevant standards: {', '.join(value)}"
        return "No specific standards found for query"

    def forward(self, question):
        return self.react(question=question)

# Usage
agent = EngineeringReActAgent()
result = agent(
    question="What is the tension for a 350m line in 100m depth with 500kN pretension?"
)
print(result.answer)
```

### 3. Retrieval-Augmented Generation

**RAG with DSPy:**
```python
import dspy
from dspy.retrieve.chromadb_rm import ChromadbRM

# Configure retriever
retriever = ChromadbRM(
    collection_name="engineering_docs",
    persist_directory="./chroma_db",
    k=5
)

# Configure DSPy with retriever
dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4"),
    rm=retriever
)

class RAGSignature(dspy.Signature):
    """Answer questions using retrieved context."""
    context = dspy.InputField(desc="Retrieved relevant passages")
    question = dspy.InputField(desc="Question to answer")
    answer = dspy.OutputField(desc="Answer based on context")

class RAGModule(dspy.Module):
    """RAG module with retrieval and generation."""

    def __init__(self, num_passages=5):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought(RAGSignature)

    def forward(self, question):
        # Retrieve relevant passages
        passages = self.retrieve(question).passages

        # Generate answer with context
        context = "\n\n".join(passages)
        result = self.generate(context=context, question=question)

        return dspy.Prediction(
            answer=result.answer,
            passages=passages,
            reasoning=result.rationale
        )

# Usage
rag = RAGModule(num_passages=5)
result = rag(question="What are the safety factor requirements for moorings?")

print(f"Answer: {result.answer}")
print(f"Sources: {len(result.passages)} passages retrieved")
```

**Multi-Hop RAG:**
```python
class MultiHopRAG(dspy.Module):
    """
    Multi-hop RAG that retrieves, reasons, and retrieves again
    for complex questions requiring multiple pieces of information.
    """

    def __init__(self, num_hops=2, passages_per_hop=3):
        super().__init__()
        self.num_hops = num_hops
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_query = dspy.ChainOfThought(
            "context, question -> search_query"
        )
        self.generate_answer = dspy.ChainOfThought(RAGSignature)

    def forward(self, question):
        context = []
        current_query = question

        for hop in range(self.num_hops):
            # Retrieve for current query
            passages = self.retrieve(current_query).passages
            context.extend(passages)

            if hop < self.num_hops - 1:
                # Generate refined query for next hop
                all_context = "\n\n".join(context)
                query_result = self.generate_query(
                    context=all_context,
                    question=question
                )
                current_query = query_result.search_query

        # Final answer generation
        full_context = "\n\n".join(context)
        result = self.generate_answer(
            context=full_context,
            question=question
        )

        return dspy.Prediction(
            answer=result.answer,
            hops=self.num_hops,
            total_passages=len(context)
        )

# Usage
multi_hop_rag = MultiHopRAG(num_hops=3, passages_per_hop=3)
result = multi_hop_rag(
    question="How does fatigue analysis relate to mooring safety factors?"
)
```

### 4. Optimizers

**BootstrapFewShot Optimizer:**
```python
from dspy.teleprompt import BootstrapFewShot

class ClassifyReport(dspy.Signature):
    """Classify engineering report type."""
    report_text = dspy.InputField()
    report_type = dspy.OutputField(
        desc="Type: analysis, inspection, design, or incident"
    )

class ReportClassifier(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classify = dspy.Predict(ClassifyReport)

    def forward(self, report_text):
        return self.classify(report_text=report_text)

# Create training data
trainset = [
    dspy.Example(
        report_text="The mooring analysis shows maximum tensions...",
        report_type="analysis"
    ).with_inputs("report_text"),
    dspy.Example(
        report_text="Visual inspection of Line 3 revealed corrosion...",
        report_type="inspection"
    ).with_inputs("report_text"),
    dspy.Example(
        report_text="The new platform design incorporates...",
        report_type="design"
    ).with_inputs("report_text"),
    dspy.Example(
        report_text="At 14:32, the vessel experienced sudden offset...",
        report_type="incident"
    ).with_inputs("report_text"),
    # Add more examples...
]

# Define metric
def classification_accuracy(example, prediction, trace=None):
    return example.report_type.lower() == prediction.report_type.lower()

# Optimize
optimizer = BootstrapFewShot(
    metric=classification_accuracy,
    max_bootstrapped_demos=4,
    max_labeled_demos=8
)

# Compile optimized module
optimized_classifier = optimizer.compile(
    ReportClassifier(),
    trainset=trainset
)

# Use optimized classifier
result = optimized_classifier(
    report_text="Fatigue analysis indicates remaining life of 15 years..."
)
print(f"Type: {result.report_type}")
```

**BootstrapFewShotWithRandomSearch:**
```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

# More thorough optimization with search
optimizer = BootstrapFewShotWithRandomSearch(
    metric=classification_accuracy,
    max_bootstrapped_demos=4,
    max_labeled_demos=8,
    num_candidate_programs=10,
    num_threads=4
)

# This searches for the best combination of examples
optimized = optimizer.compile(
    ReportClassifier(),
    trainset=trainset,
    valset=valset  # Optional validation set
)
```

**MIPRO Optimizer (Advanced):**
```python
from dspy.teleprompt import MIPRO

class ComplexQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        return self.qa(context=context, question=question)

# MIPRO optimizes both instructions and examples
optimizer = MIPRO(
    metric=answer_quality_metric,
    prompt_model=dspy.OpenAI(model="gpt-4"),
    task_model=dspy.OpenAI(model="gpt-3.5-turbo"),
    num_candidates=10,
    init_temperature=1.0
)

optimized_qa = optimizer.compile(
    ComplexQA(),
    trainset=trainset,
    num_batches=5,
    max_bootstrapped_demos=3,
    max_labeled_demos=5,
    eval_kwargs={"num_threads": 4}
)
```

### 5. Evaluation and Metrics

**Custom Metrics:**
```python
import dspy
from typing import Optional

def answer_correctness(
    example: dspy.Example,
    prediction: dspy.Prediction,
    trace: Optional[list] = None
) -> float:
    """
    Evaluate answer correctness.

    Args:
        example: Ground truth example
        prediction: Model prediction
        trace: Optional execution trace

    Returns:
        Score between 0 and 1
    """
    # Exact match
    if example.answer.lower().strip() == prediction.answer.lower().strip():
        return 1.0

    # Partial match using overlap
    expected_words = set(example.answer.lower().split())
    predicted_words = set(prediction.answer.lower().split())

    if not expected_words:
        return 0.0

    overlap = len(expected_words & predicted_words)
    return overlap / len(expected_words)

def answer_relevance(
    example: dspy.Example,
    prediction: dspy.Prediction,
    trace: Optional[list] = None
) -> float:
    """Evaluate answer relevance using an LLM judge."""

    judge = dspy.Predict("question, answer -> relevance_score")

    result = judge(
        question=example.question,
        answer=prediction.answer
    )

    try:
        score = float(result.relevance_score)
        return min(max(score, 0.0), 1.0)
    except ValueError:
        return 0.5

def combined_metric(example, prediction, trace=None) -> float:
    """Combined metric with multiple factors."""
    correctness = answer_correctness(example, prediction, trace)
    relevance = answer_relevance(example, prediction, trace)

    # Weighted combination
    return 0.6 * correctness + 0.4 * relevance
```

**Systematic Evaluation:**
```python
from dspy.evaluate import Evaluate

def evaluate_module(module, testset, metric, num_threads=4):
    """
    Systematically evaluate a module on a test set.
    """
    evaluator = Evaluate(
        devset=testset,
        metric=metric,
        num_threads=num_threads,
        display_progress=True,
        display_table=5  # Show top 5 examples
    )

    score = evaluator(module)

    print(f"\nOverall Score: {score:.2%}")

    return score

# Usage
testset = [
    dspy.Example(
        question="What is the minimum safety factor?",
        context="API RP 2SK requires SF >= 1.67 for intact...",
        answer="1.67 for intact conditions"
    ).with_inputs("question", "context"),
    # More test cases...
]

score = evaluate_module(
    module=optimized_qa,
    testset=testset,
    metric=answer_correctness
)
```

### 6. Saving and Loading

**Save Optimized Modules:**
```python
import json
from pathlib import Path

def save_module(module, path: str):
    """Save an optimized DSPy module."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    module.save(path)
    print(f"Module saved to {path}")

def load_module(module_class, path: str):
    """Load a saved DSPy module."""
    module = module_class()
    module.load(path)
    print(f"Module loaded from {path}")
    return module

# Save
save_module(optimized_classifier, "models/report_classifier.json")

# Load
loaded_classifier = load_module(ReportClassifier, "models/report_classifier.json")

# Verify
result = loaded_classifier(report_text="Test report...")
print(result.report_type)
```

## Complete Examples

### Example 1: Engineering Report Analysis Pipeline

```python
import dspy
from dspy.teleprompt import BootstrapFewShot
from typing import List
import json

# Configure DSPy
dspy.settings.configure(lm=dspy.OpenAI(model="gpt-4", max_tokens=2000))

# Define signatures
class ExtractMetrics(dspy.Signature):
    """Extract numerical metrics from engineering text."""
    text = dspy.InputField()
    metrics = dspy.OutputField(desc="JSON list of {name, value, unit}")

class AssessRisk(dspy.Signature):
    """Assess risk level based on metrics."""
    metrics = dspy.InputField(desc="Extracted metrics as JSON")
    standards = dspy.InputField(desc="Relevant standards requirements")
    risk_assessment = dspy.OutputField(desc="Risk level and justification")

class GenerateRecommendations(dspy.Signature):
    """Generate engineering recommendations."""
    metrics = dspy.InputField()
    risk_assessment = dspy.InputField()
    recommendations = dspy.OutputField(desc="List of prioritized recommendations")

class EngineeringReportAnalyzer(dspy.Module):
    """
    Complete pipeline for analyzing engineering reports:
    1. Extract metrics
    2. Assess risk against standards
    3. Generate recommendations
    """

    def __init__(self):
        super().__init__()
        self.extract = dspy.ChainOfThought(ExtractMetrics)
        self.assess = dspy.ChainOfThought(AssessRisk)
        self.recommend = dspy.ChainOfThought(GenerateRecommendations)

        # Standards knowledge base
        self.standards = """
        Mooring Safety Factors (API RP 2SK):
        - Intact: SF >= 1.67
        - Damaged: SF >= 1.25
        - Transient: SF >= 1.05

        Fatigue Requirements:
        - Design fatigue life >= 3x service life
        - Minimum service life: 25 years

        Chain Wear Limits:
        - Maximum diameter loss: 10%
        - Critical: > 8%
        """

    def forward(self, report_text):
        # Step 1: Extract metrics
        metrics_result = self.extract(text=report_text)

        # Step 2: Assess risk
        risk_result = self.assess(
            metrics=metrics_result.metrics,
            standards=self.standards
        )

        # Step 3: Generate recommendations
        recs_result = self.recommend(
            metrics=metrics_result.metrics,
            risk_assessment=risk_result.risk_assessment
        )

        return dspy.Prediction(
            metrics=metrics_result.metrics,
            risk_assessment=risk_result.risk_assessment,
            recommendations=recs_result.recommendations,
            reasoning={
                "metrics_reasoning": metrics_result.rationale,
                "risk_reasoning": risk_result.rationale,
                "recommendation_reasoning": recs_result.rationale
            }
        )

# Create and use analyzer
analyzer = EngineeringReportAnalyzer()

report = """
Mooring System Inspection Report - Platform Bravo

Inspection Date: 2026-01-15
Inspector: J. Smith

Findings:
1. Line 1 tension measured at 2,100 kN (pretension: 2,000 kN, limit: 2,800 kN)
2. Line 3 chain shows 9.2% diameter loss at fairlead (original: 120mm)
3. Safety factor calculated at 1.71 for 100-year storm
4. Estimated fatigue life: 42 years
5. Connector corrosion observed on Lines 2 and 4
6. Polyester rope sections in good condition
"""

result = analyzer(report_text=report)

print("=== Engineering Report Analysis ===\n")
print(f"Extracted Metrics:\n{result.metrics}\n")
print(f"Risk Assessment:\n{result.risk_assessment}\n")
print(f"Recommendations:\n{result.recommendations}\n")
```

### Example 2: Optimized Technical Q&A System

```python
import dspy
from dspy.teleprompt import BootstrapFewShotWithRandomSearch
from dspy.retrieve.chromadb_rm import ChromadbRM

# Setup retriever
retriever = ChromadbRM(
    collection_name="engineering_knowledge",
    persist_directory="./chroma_db",
    k=5
)

dspy.settings.configure(
    lm=dspy.OpenAI(model="gpt-4"),
    rm=retriever
)

class TechnicalAnswer(dspy.Signature):
    """
    Answer technical engineering questions accurately.
    Always cite sources and acknowledge uncertainty.
    """
    context = dspy.InputField(desc="Retrieved technical documentation")
    question = dspy.InputField(desc="Technical question")
    answer = dspy.OutputField(desc="Accurate, cited answer")
    confidence = dspy.OutputField(desc="Confidence: high, medium, or low")
    sources = dspy.OutputField(desc="List of source documents used")

class TechnicalQASystem(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=5)
        self.answer = dspy.ChainOfThought(TechnicalAnswer)

    def forward(self, question):
        # Retrieve relevant passages
        context = self.retrieve(question).passages

        # Generate answer
        result = self.answer(
            context="\n\n".join(context),
            question=question
        )

        return dspy.Prediction(
            answer=result.answer,
            confidence=result.confidence,
            sources=result.sources,
            reasoning=result.rationale,
            retrieved_passages=context
        )

# Training data
trainset = [
    dspy.Example(
        question="What is the minimum safety factor for intact mooring?",
        answer="According to API RP 2SK, the minimum safety factor for intact mooring conditions is 1.67.",
        confidence="high",
        sources=["API RP 2SK Section 5.3"]
    ).with_inputs("question"),

    dspy.Example(
        question="How is fatigue damage calculated for mooring chains?",
        answer="Fatigue damage is calculated using the Palmgren-Miner rule, summing damage ratios (n/N) for each stress range cycle, where n is the number of cycles and N is the allowable cycles from S-N curves per DNV-RP-C203.",
        confidence="high",
        sources=["DNV-RP-C203", "API RP 2SK Section 7"]
    ).with_inputs("question"),

    dspy.Example(
        question="What causes vortex-induced vibration in risers?",
        answer="VIV occurs when current flows past a riser, creating alternating vortex shedding that induces oscillating forces perpendicular to flow direction. Lock-in occurs when shedding frequency matches natural frequency.",
        confidence="high",
        sources=["DNV-RP-F105", "API RP 2RD"]
    ).with_inputs("question"),
    # Add more examples...
]

# Metric function
def answer_quality(example, prediction, trace=None):
    """Evaluate answer quality on multiple dimensions."""

    # Check if answer is substantive
    if len(prediction.answer) < 20:
        return 0.0

    # Check if sources are cited
    has_sources = bool(prediction.sources and len(prediction.sources) > 0)

    # Check confidence is valid
    valid_confidence = prediction.confidence.lower() in ["high", "medium", "low"]

    # Base score
    score = 0.5

    if has_sources:
        score += 0.25

    if valid_confidence:
        score += 0.25

    return score

# Optimize
optimizer = BootstrapFewShotWithRandomSearch(
    metric=answer_quality,
    max_bootstrapped_demos=4,
    max_labeled_demos=6,
    num_candidate_programs=8
)

# Compile
optimized_qa = optimizer.compile(
    TechnicalQASystem(),
    trainset=trainset
)

# Save optimized module
optimized_qa.save("models/technical_qa_v1.json")

# Use optimized system
result = optimized_qa(
    question="What inspection interval is recommended for mooring chains?"
)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
print(f"Sources: {result.sources}")
print(f"Reasoning: {result.reasoning}")
```

### Example 3: Comparison with Baseline

```python
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import BootstrapFewShot
import pandas as pd

class SimpleQA(dspy.Module):
    """Baseline: Simple prediction without optimization."""
    def __init__(self):
        super().__init__()
        self.qa = dspy.Predict("question -> answer")

    def forward(self, question):
        return self.qa(question=question)

class ChainOfThoughtQA(dspy.Module):
    """Intermediate: Chain-of-thought without optimization."""
    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.qa(question=question)

class OptimizedQA(dspy.Module):
    """Advanced: Chain-of-thought with optimization."""
    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.qa(question=question)

def run_comparison(trainset, testset, metric):
    """Compare baseline vs optimized performance."""

    results = []

    # Baseline
    baseline = SimpleQA()
    baseline_eval = Evaluate(devset=testset, metric=metric, display_progress=True)
    baseline_score = baseline_eval(baseline)
    results.append({"Model": "Baseline (Predict)", "Score": baseline_score})

    # Chain of Thought (unoptimized)
    cot = ChainOfThoughtQA()
    cot_score = baseline_eval(cot)
    results.append({"Model": "ChainOfThought (unoptimized)", "Score": cot_score})

    # Optimized
    optimizer = BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
    optimized = optimizer.compile(OptimizedQA(), trainset=trainset)
    optimized_score = baseline_eval(optimized)
    results.append({"Model": "ChainOfThought (optimized)", "Score": optimized_score})

    # Display results
    df = pd.DataFrame(results)
    print("\n=== Model Comparison ===")
    print(df.to_string(index=False))

    # Calculate improvement
    improvement = ((optimized_score - baseline_score) / baseline_score) * 100
    print(f"\nImprovement over baseline: {improvement:.1f}%")

    return df, optimized

# Usage
comparison_results, best_model = run_comparison(
    trainset=trainset,
    testset=testset,
    metric=answer_correctness
)
```

## Integration Patterns

### Integration with LangChain

```python
import dspy
from langchain_core.runnables import RunnableLambda

# Create DSPy module
class DSPyQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        return self.qa(context=context, question=question)

dspy_module = DSPyQA()

# Wrap as LangChain Runnable
def dspy_invoke(inputs):
    result = dspy_module(
        context=inputs["context"],
        question=inputs["question"]
    )
    return {"answer": result.answer, "reasoning": result.rationale}

dspy_runnable = RunnableLambda(dspy_invoke)

# Use in LangChain chain
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | dspy_runnable
)
```

### FastAPI Deployment

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import dspy

app = FastAPI()

# Load optimized module
class QAModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.qa(question=question)

qa_module = QAModule()
qa_module.load("models/optimized_qa.json")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    reasoning: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        result = qa_module(question=request.question)
        return AnswerResponse(
            answer=result.answer,
            reasoning=result.rationale
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Best Practices

### 1. Start Simple, Then Optimize

```python
# 1. Start with basic Predict
basic = dspy.Predict("question -> answer")

# 2. Add ChainOfThought if needed
cot = dspy.ChainOfThought("question -> answer")

# 3. Optimize only after baseline is established
optimized = optimizer.compile(cot, trainset=data)
```

### 2. Quality Training Data

```python
def create_training_example(question, answer, inputs=["question"]):
    """Create well-formed training example."""
    example = dspy.Example(
        question=question,
        answer=answer
    )
    return example.with_inputs(*inputs)

# Include diverse examples
trainset = [
    create_training_example("Simple question?", "Simple answer"),
    create_training_example("Complex technical question?", "Detailed answer..."),
    create_training_example("Edge case question?", "Careful handling..."),
]
```

### 3. Meaningful Metrics

```python
def comprehensive_metric(example, prediction, trace=None):
    """Combine multiple evaluation dimensions."""
    scores = {
        "correctness": check_correctness(example, prediction),
        "completeness": check_completeness(prediction),
        "format": check_format(prediction),
        "citations": check_citations(prediction)
    }

    weights = {"correctness": 0.4, "completeness": 0.3, "format": 0.15, "citations": 0.15}

    return sum(scores[k] * weights[k] for k in scores)
```

## Troubleshooting

### Optimization Not Improving

```python
# Increase number of training examples
# Ensure diverse, high-quality examples
# Try different optimizer settings

optimizer = BootstrapFewShotWithRandomSearch(
    metric=metric,
    max_bootstrapped_demos=8,  # Increase
    num_candidate_programs=20,  # More search
    num_threads=8
)
```

### Module Too Slow

```python
# Use faster model for compilation
compile_lm = dspy.OpenAI(model="gpt-3.5-turbo")
deploy_lm = dspy.OpenAI(model="gpt-4")

with dspy.settings.context(lm=compile_lm):
    optimized = optimizer.compile(module, trainset=data)

# Deploy with stronger model
dspy.settings.configure(lm=deploy_lm)
```

### Out of Memory

```python
# Process in batches
batch_size = 10
for i in range(0, len(trainset), batch_size):
    batch = trainset[i:i+batch_size]
    process_batch(batch)
```

## Resources

- **DSPy Documentation**: https://dspy-docs.vercel.app/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **DSPy Paper**: https://arxiv.org/abs/2310.03714
- **Examples**: https://github.com/stanfordnlp/dspy/tree/main/examples

---

## Version History

- **1.0.0** (2026-01-17): Initial release with signatures, modules, optimizers, and RAG
