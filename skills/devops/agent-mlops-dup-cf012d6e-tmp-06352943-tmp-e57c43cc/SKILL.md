---
name: agent-mlops
description: Production deployment and operationalization of AI agents on Databricks. Use when deploying agents to Model Serving, setting up MLflow logging and tracing for agents, implementing Agent Evaluation frameworks, monitoring agent performance in production, managing agent versions and rollbacks, optimizing agent costs and latency, or establishing CI/CD pipelines for agents. Covers MLflow integration patterns, evaluation best practices, Model Serving configuration, and production monitoring strategies.
---

# Agent MLOps: Production Deployment & Monitoring

Deploy, evaluate, and monitor AI agents in production using Databricks MLflow and Model Serving.

## Core Concepts

### Agent MLOps Lifecycle

```
Development → Logging → Evaluation → Deployment → Monitoring → Iteration
     ↑                                                            ↓
     └────────────────────────────────────────────────────────────┘
```

**Key difference from traditional MLOps:** Agents make dynamic decisions, requiring evaluation of decision-making quality, not just prediction accuracy.

## Problem-Solution Patterns

### Problem 1: Can't Debug Agent Decisions

**Symptoms:**
- Agent makes unexpected tool choices
- No visibility into reasoning process
- Can't reproduce issues
- Debugging requires re-running entire workflow

**Root causes:**
- No tracing enabled
- Tool calls not logged
- Intermediate steps discarded

**Solution: Enable MLflow Tracing**

```python
import mlflow

# Enable automatic tracing for LangChain
mlflow.langchain.autolog()

# All agent executions now automatically traced
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True  # Critical for tracing
)

# Execute with tracing
with mlflow.start_run(run_name="agent_execution"):
    result = agent_executor.invoke({"input": "user query"})
    
    # Tracing captures:
    # - LLM calls and prompts
    # - Tool selection decisions
    # - Tool inputs/outputs
    # - Execution time per step
    # - Token usage
```

**View traces in MLflow UI:**
1. Open MLflow experiment
2. Click run
3. Navigate to "Traces" tab
4. See full execution tree

### Problem 2: No Systematic Evaluation

**Symptoms:**
- Testing is manual and ad-hoc
- Can't measure improvement over versions
- Regression issues slip through
- No confidence in deployment

**Root causes:**
- No test dataset
- No evaluation metrics
- Manual testing only

**Solution: Implement Agent Evaluation**

```python
import mlflow
import pandas as pd
from mlflow.metrics.genai import answer_similarity

# Step 1: Create evaluation dataset
eval_data = pd.DataFrame({
    "question": [
        "What products are trending?",
        "Which locations have lowest turnover?",
        "Trending products at risk of overstock?",
    ],
    "expected_tools": [
        "customer_behavior",
        "inventory",
        "customer_behavior,inventory"
    ],
    "ground_truth_answer": [
        "Products X, Y, Z are currently trending based on purchase data",
        "Location A has lowest turnover at 2.1x annually",
        "Products X and Y are trending but have 60-day supply"
    ]
})

# Step 2: Define evaluation metrics
def tool_selection_accuracy(predictions, targets):
    """Custom metric: Did agent call expected tools?"""
    correct = 0
    for pred_tools, expected_tools in zip(predictions, targets):
        expected_set = set(expected_tools.split(','))
        pred_set = set([step[0].tool for step in pred_tools['intermediate_steps']])
        if expected_set.issubset(pred_set):
            correct += 1
    return correct / len(predictions)

# Step 3: Run evaluation
with mlflow.start_run(run_name="agent_evaluation"):
    results = mlflow.evaluate(
        model=agent_uri,  # URI of logged model
        data=eval_data,
        targets="ground_truth_answer",
        model_type="question-answering",
        evaluators="default",
        extra_metrics=[
            answer_similarity,
            tool_selection_accuracy
        ]
    )
    
    # View results
    print(f"Answer Similarity: {results.metrics['answer_similarity/v1/mean']}")
    print(f"Tool Selection Accuracy: {results.metrics['tool_selection_accuracy']}")
```

### Problem 3: Model Serving Deployment Failures

**Symptoms:**
- Endpoint won't start
- Timeout errors
- Import errors in production
- Works locally, fails in serving

**Root causes:**
- Missing dependencies
- Environment mismatch
- Incorrect model signature
- No validation before deployment

**Solution: Proper Model Packaging**

```python
import mlflow
from mlflow.models import ModelSignature
from mlflow.types.schema import ColSpec, Schema
import pandas as pd

# Step 1: Define clear signature
input_schema = Schema([
    ColSpec("string", "question")
])
output_schema = Schema([
    ColSpec("string", "response")
])
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

# Step 2: Create example for validation
input_example = pd.DataFrame({
    "question": ["What products are trending?"]
})

# Step 3: Specify all dependencies
pip_requirements = [
    "databricks-sdk>=0.20.0",
    "mlflow>=2.10.0",
    "langchain>=0.1.0",
    "langchain-community>=0.0.1",
]

# Step 4: Create MLflow model wrapper
class AgentModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        """Initialize agent when model loads"""
        from your_module import GenieAgent
        self.agent = GenieAgent()
    
    def predict(self, context, model_input):
        """Handle predictions"""
        responses = []
        for question in model_input['question']:
            result = self.agent.query(question)
            responses.append(result['output'])
        return pd.DataFrame({'response': responses})

# Step 5: Log with all metadata
with mlflow.start_run(run_name="agent_v1"):
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=AgentModel(),
        signature=signature,
        input_example=input_example,
        pip_requirements=pip_requirements,
        registered_model_name="main.default.my_agent"
    )
    
    # Log configuration
    mlflow.log_param("foundation_model", "llama-3-1-70b")
    mlflow.log_param("tools", "customer,inventory,web")
    mlflow.log_param("temperature", 0.1)

# Step 6: Test locally before deploying
model_uri = "runs:/<run_id>/agent"
loaded_model = mlflow.pyfunc.load_model(model_uri)

# Validate it works
test_df = pd.DataFrame({"question": ["test query"]})
result = loaded_model.predict(test_df)
assert result is not None, "Model prediction failed"
```

### Problem 4: High Latency in Production

**Symptoms:**
- Responses take >30 seconds
- Users abandoning queries
- High timeout rates
- Poor user experience

**Root causes:**
- Cold starts on serverless
- No request batching
- Inefficient tool implementations
- Wrong workload size

**Solutions:**

**Strategy 1: Configure Model Serving Properly**

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
    ServedEntityInput,
    EndpointCoreConfigInput
)

w = WorkspaceClient()

# For agents, optimize configuration:
w.serving_endpoints.create(
    name="agent-endpoint",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(
                entity_name="main.default.my_agent",
                entity_version=1,
                workload_size="Small",  # Start small
                scale_to_zero_enabled=True,  # Cost optimization
                # For latency-critical apps:
                # scale_to_zero_enabled=False  # Keep warm
            )
        ],
        # Optional: Traffic config for A/B testing
        traffic_config={
            "routes": [
                {"served_model_name": "my_agent-1", "traffic_percentage": 100}
            ]
        }
    )
)
```

**Strategy 2: Implement Request Batching**

```python
class AgentModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        """Batch predictions for efficiency"""
        questions = model_input['question'].tolist()
        
        # Process in batches
        batch_size = 5
        all_responses = []
        
        for i in range(0, len(questions), batch_size):
            batch = questions[i:i+batch_size]
            
            # Parallel processing within batch
            with concurrent.futures.ThreadPoolExecutor() as executor:
                responses = list(executor.map(
                    lambda q: self.agent.query(q)['output'],
                    batch
                ))
            
            all_responses.extend(responses)
        
        return pd.DataFrame({'response': all_responses})
```

**Strategy 3: Cache at Multiple Levels**

```python
from functools import lru_cache
import hashlib

class CachedAgentModel(mlflow.pyfunc.PythonModel):
    def __init__(self):
        self.response_cache = {}  # Simple in-memory cache
    
    def predict(self, context, model_input):
        responses = []
        
        for question in model_input['question']:
            # Check cache
            cache_key = hashlib.md5(question.encode()).hexdigest()
            
            if cache_key in self.response_cache:
                responses.append(self.response_cache[cache_key])
            else:
                # Execute agent
                result = self.agent.query(question)
                response = result['output']
                
                # Cache result
                self.response_cache[cache_key] = response
                responses.append(response)
        
        return pd.DataFrame({'response': responses})
```

### Problem 5: Can't Track Agent Costs

**Symptoms:**
- Unexpected high bills
- Can't attribute costs to queries
- No visibility into token usage
- Can't optimize expensive queries

**Root causes:**
- Not logging token usage
- No cost tracking per query
- Missing Foundation Model API metrics

**Solution: Comprehensive Cost Tracking**

```python
import mlflow
from datetime import datetime

class CostTrackingAgent(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        responses = []
        
        for question in model_input['question']:
            start_time = datetime.now()
            
            # Execute agent
            result = self.agent.query(question)
            
            end_time = datetime.now()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            # Extract metrics from result
            tool_calls = len(result.get('intermediate_steps', []))
            
            # Log to MLflow
            with mlflow.start_span(name="agent_query") as span:
                span.set_attribute("question", question)
                span.set_attribute("latency_ms", latency_ms)
                span.set_attribute("tool_calls", tool_calls)
                span.set_attribute("response_length", len(result['output']))
                
                # If LLM provides token counts:
                if 'token_usage' in result:
                    span.set_attribute("input_tokens", result['token_usage']['input'])
                    span.set_attribute("output_tokens", result['token_usage']['output'])
                    
                    # Calculate cost (example for Llama 3.1 70B)
                    input_cost = result['token_usage']['input'] * 0.001 / 1000
                    output_cost = result['token_usage']['output'] * 0.002 / 1000
                    total_cost = input_cost + output_cost
                    
                    span.set_attribute("cost_usd", total_cost)
            
            responses.append(result['output'])
        
        return pd.DataFrame({'response': responses})
```

## MLflow Integration Patterns

### Pattern 1: Development Workflow

```python
import mlflow

# Set experiment
mlflow.set_experiment("/Users/your_email/agent_development")

# Enable tracing
mlflow.langchain.autolog()

# Development iteration
with mlflow.start_run(run_name="experiment_1"):
    # Build agent
    agent = GenieAgent(temperature=0.1)
    
    # Test queries
    test_queries = ["query1", "query2", "query3"]
    for query in test_queries:
        result = agent.query(query)
        # Automatically traced
    
    # Log parameters
    mlflow.log_param("temperature", 0.1)
    mlflow.log_param("model", "llama-3-1-70b")
    mlflow.log_param("tools", "customer,inventory")
    
    # Log metrics
    mlflow.log_metric("avg_latency_ms", 5000)
    mlflow.log_metric("tool_calls_per_query", 1.5)
```

### Pattern 2: Model Registration

```python
# After development, register for production
with mlflow.start_run(run_name="production_candidate"):
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=AgentModel(),
        signature=signature,
        registered_model_name="main.default.my_agent"
    )
    
    run_id = mlflow.active_run().info.run_id

# Promote to production
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Add model version alias
client.set_registered_model_alias(
    name="main.default.my_agent",
    alias="production",
    version=1
)
```

### Pattern 3: A/B Testing

```python
# Deploy two versions for comparison
w.serving_endpoints.update_config(
    name="agent-endpoint",
    served_entities=[
        ServedEntityInput(
            entity_name="main.default.my_agent",
            entity_version=1,
            workload_size="Small",
            scale_to_zero_enabled=True
        ),
        ServedEntityInput(
            entity_name="main.default.my_agent",
            entity_version=2,
            workload_size="Small",
            scale_to_zero_enabled=True
        )
    ],
    traffic_config={
        "routes": [
            {"served_model_name": "my_agent-1", "traffic_percentage": 50},
            {"served_model_name": "my_agent-2", "traffic_percentage": 50}
        ]
    }
)

# Monitor performance of each version
# After validation, shift 100% to winner
```

## Agent Evaluation Best Practices

### Building Evaluation Datasets

```python
# Principle: Cover all agent capabilities
eval_cases = [
    # Single-tool queries
    {
        "question": "What products are trending?",
        "expected_tools": ["customer_behavior"],
        "expected_answer": "Products X, Y, Z trending...",
        "category": "single_tool"
    },
    
    # Multi-tool queries
    {
        "question": "Trending products at risk of overstock?",
        "expected_tools": ["customer_behavior", "inventory"],
        "expected_answer": "X and Y trending but overstocked...",
        "category": "multi_tool"
    },
    
    # Edge cases
    {
        "question": "Tell me about products",
        "expected_behavior": "ask_clarification",
        "category": "ambiguous"
    },
    
    # Error handling
    {
        "question": "Query invalid data source",
        "expected_behavior": "graceful_error",
        "category": "error"
    }
]

eval_df = pd.DataFrame(eval_cases)
```

### Custom Evaluation Metrics

```python
def evaluate_tool_selection(predictions, targets):
    """Did agent call the right tools?"""
    correct = 0
    for pred, expected in zip(predictions, targets):
        expected_tools = set(expected.split(','))
        actual_tools = set([
            step[0].tool 
            for step in pred['intermediate_steps']
        ])
        if expected_tools == actual_tools:
            correct += 1
    return correct / len(predictions)

def evaluate_latency(predictions):
    """Measure response time"""
    latencies = [pred['latency_ms'] for pred in predictions]
    return {
        "mean": sum(latencies) / len(latencies),
        "p95": sorted(latencies)[int(len(latencies) * 0.95)],
        "max": max(latencies)
    }

def evaluate_cost(predictions):
    """Measure cost per query"""
    costs = [pred['cost_usd'] for pred in predictions]
    return {
        "mean": sum(costs) / len(costs),
        "total": sum(costs)
    }
```

### Running Evaluation

```python
# Step 1: Load evaluation data
eval_df = pd.read_csv("agent_eval_dataset.csv")

# Step 2: Run evaluation
with mlflow.start_run(run_name="evaluation_v1"):
    results = mlflow.evaluate(
        model="main.default.my_agent@production",
        data=eval_df,
        targets="expected_answer",
        model_type="question-answering",
        evaluators=["default"],
        extra_metrics=[
            evaluate_tool_selection,
            evaluate_latency,
            evaluate_cost
        ]
    )
    
    # Step 3: Log results
    mlflow.log_metrics({
        "tool_accuracy": results.metrics['tool_selection'],
        "mean_latency": results.metrics['latency_mean'],
        "p95_latency": results.metrics['latency_p95'],
        "cost_per_query": results.metrics['cost_mean']
    })
    
    # Step 4: Log evaluation dataset
    mlflow.log_table(eval_df, "evaluation_dataset.json")
```

## Production Monitoring

### Key Metrics to Track

```python
# 1. Usage Metrics
- queries_per_minute
- unique_users
- query_distribution_by_tool

# 2. Performance Metrics
- latency_p50, p95, p99
- timeout_rate
- error_rate
- tool_call_distribution

# 3. Cost Metrics
- cost_per_query
- total_daily_cost
- tokens_per_query
- tool_calls_per_query

# 4. Quality Metrics
- user_feedback_score
- retry_rate
- clarification_request_rate
```

### Monitoring Implementation

```python
from databricks.sdk import WorkspaceClient
import time

def monitor_agent_endpoint(endpoint_name: str):
    """Monitor agent serving endpoint"""
    w = WorkspaceClient()
    
    while True:
        # Get endpoint metrics
        metrics = w.serving_endpoints.get(endpoint_name)
        
        # Log to MLflow
        with mlflow.start_run(run_name="monitoring"):
            mlflow.log_metric("requests_per_minute", metrics.rpm)
            mlflow.log_metric("error_rate", metrics.error_rate)
            mlflow.log_metric("p95_latency_ms", metrics.p95_latency)
        
        # Alert if thresholds exceeded
        if metrics.error_rate > 0.05:  # 5% error rate
            send_alert("High error rate on agent endpoint")
        
        if metrics.p95_latency > 30000:  # 30 seconds
            send_alert("High latency on agent endpoint")
        
        time.sleep(60)  # Check every minute
```

## CI/CD for Agents

### Automated Deployment Pipeline

```python
# .github/workflows/agent-deployment.yml
# or Databricks Jobs workflow

# Step 1: Run tests
def test_agent():
    agent = GenieAgent()
    
    # Unit tests
    assert agent.query("test")['output']
    
    # Integration tests
    eval_df = load_eval_dataset()
    results = run_evaluation(agent, eval_df)
    
    # Quality gates
    assert results['tool_accuracy'] > 0.90
    assert results['mean_latency'] < 10000  # 10 seconds
    
    return results

# Step 2: Log to MLflow
with mlflow.start_run():
    test_results = test_agent()
    
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=AgentModel(),
        signature=signature,
        registered_model_name="main.default.my_agent"
    )
    
    run_id = mlflow.active_run().info.run_id

# Step 3: Deploy to staging
deploy_to_endpoint(
    model_uri=f"runs:/{run_id}/agent",
    endpoint_name="agent-staging"
)

# Step 4: Run validation
validation_results = validate_endpoint("agent-staging")

# Step 5: Deploy to production if validation passes
if validation_results['success']:
    deploy_to_endpoint(
        model_uri=f"runs:/{run_id}/agent",
        endpoint_name="agent-production"
    )
```

## Quick Reference

### Deployment Checklist

- [ ] MLflow tracing enabled
- [ ] Evaluation dataset created (20+ diverse examples)
- [ ] Model signature defined
- [ ] Dependencies specified
- [ ] Input example provided
- [ ] Local testing passed
- [ ] Evaluation metrics > thresholds
- [ ] Model registered in Unity Catalog
- [ ] Deployed to staging endpoint
- [ ] Staging validation passed
- [ ] Production deployment
- [ ] Monitoring configured
- [ ] Alerts set up

### Common MLflow Commands

```python
# Set experiment
mlflow.set_experiment("/path/to/experiment")

# Enable tracing
mlflow.langchain.autolog()

# Log model
mlflow.pyfunc.log_model(
    artifact_path="agent",
    python_model=model,
    signature=signature,
    registered_model_name="catalog.schema.model"
)

# Load model
model = mlflow.pyfunc.load_model("models:/catalog.schema.model/1")

# Run evaluation
results = mlflow.evaluate(
    model=model_uri,
    data=eval_df,
    targets="expected",
    evaluators="default"
)
```

## Related Skills

- **mosaic-ai-agent**: Build the agents to deploy
- **genie-integration**: Integrate Genie rooms in production agents
