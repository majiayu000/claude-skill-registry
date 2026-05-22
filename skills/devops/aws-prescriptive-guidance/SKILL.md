---
name: aws-prescriptive-guidance
description: AWS Prescriptive Guidance for best practices and architectural patterns. Use for AWS architecture recommendations, SageMaker AI endpoints guidance, deployment patterns, and AWS solution architectures.
---

# AWS Prescriptive Guidance Skill

Comprehensive AWS architectural patterns, ML deployment strategies, and cloud design best practices from official AWS documentation.

## When to Use This Skill

This skill should be triggered when:

- **Designing AWS architectures** - Multi-tier applications, microservices, serverless systems
- **Deploying ML models** - SageMaker endpoints, inference pipelines, MLOps workflows
- **Implementing cloud patterns** - Circuit breakers, saga patterns, event sourcing, API routing
- **Modernizing applications** - Strangler fig migrations, anti-corruption layers, hexagonal architecture
- **Building resilient systems** - Retry with backoff, scatter-gather, publish-subscribe patterns
- **Creating MLOps pipelines** - Model training, deployment automation, cross-cloud workflows
- **Integrating preprocessing with inference** - SageMaker inference pipelines, feature engineering
- **Implementing DevOps practices** - CI/CD patterns, infrastructure as code, deployment strategies

**Specific triggers:**
- Questions about SageMaker deployment patterns
- Architecture design for AWS services
- MLOps workflow implementation
- Microservices design patterns
- System modernization strategies
- DevOps and CI/CD best practices

## Quick Reference

### 1. SageMaker Inference Pipeline Setup

Deploy preprocessing and ML model in a single endpoint:

```python
import sagemaker
from sagemaker import get_execution_role

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = get_execution_role()
bucket = sagemaker_session.default_bucket()

# Upload training data
train_input = sagemaker_session.upload_data(
    path="data/training.csv",
    bucket=bucket,
    key_prefix="myproject/train"
)
```

### 2. Create SKLearn Preprocessor

Build a preprocessing stage for your inference pipeline:

```python
from sagemaker.sklearn.estimator import SKLearn

sklearn_preprocessor = SKLearn(
    entry_point="preprocessing.py",
    role=role,
    framework_version="0.23-1",
    instance_type="ml.c4.xlarge",
    sagemaker_session=sagemaker_session
)

sklearn_preprocessor.fit({"train": train_input})
```

### 3. Train Linear Learner Model

Create and train a regression model:

```python
from sagemaker.image_uris import retrieve

ll_image = retrieve("linear-learner", boto3.Session().region_name)

ll_estimator = sagemaker.estimator.Estimator(
    ll_image,
    role,
    instance_count=1,
    instance_type="ml.m4.2xlarge",
    output_path=f"s3://{bucket}/model-output"
)

ll_estimator.set_hyperparameters(
    feature_dim=10,
    predictor_type="regressor",
    mini_batch_size=32
)

ll_estimator.fit({"train": preprocessed_data})
```

### 4. Deploy Pipeline Model

Combine preprocessing and inference in single endpoint:

```python
from sagemaker.pipeline import PipelineModel
from time import gmtime, strftime

# Create models from trained estimators
preprocessing_model = sklearn_preprocessor.create_model()
inference_model = ll_estimator.create_model()

# Create pipeline
timestamp = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
pipeline = PipelineModel(
    name=f"pipeline-{timestamp}",
    role=role,
    models=[preprocessing_model, inference_model]
)

# Deploy to endpoint
pipeline.deploy(
    initial_instance_count=1,
    instance_type="ml.c4.xlarge",
    endpoint_name=f"pipeline-endpoint-{timestamp}"
)
```

### 5. Test Inference Endpoint

Send data to your deployed pipeline:

```python
from sagemaker.predictor import Predictor
from sagemaker.serializers import CSVSerializer

predictor = Predictor(
    endpoint_name="pipeline-endpoint-2024-01-15",
    sagemaker_session=sagemaker_session,
    serializer=CSVSerializer()
)

# Raw data input (preprocessing happens automatically)
payload = "0.44, 0.365, 0.125, 0.516, 0.2155, 0.114"
prediction = predictor.predict(payload)
print(f"Prediction: {prediction}")
```

### 6. Batch Transform for Testing

Test preprocessing before full pipeline deployment:

```python
# Create transformer from preprocessor
transformer = sklearn_preprocessor.transformer(
    instance_count=1,
    instance_type="ml.m5.xlarge",
    assemble_with="Line",
    accept="text/csv"
)

# Transform training data
transformer.transform(train_input, content_type="text/csv")
transformer.wait()

# Get preprocessed output location
preprocessed_data = transformer.output_path
```

### 7. Circuit Breaker Pattern

Implement resilient service calls with circuit breaker:

```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### 8. Retry with Exponential Backoff

Implement resilient API calls:

```python
import time
import random

def retry_with_backoff(func, max_retries=5, base_delay=1, max_delay=60):
    """
    Retry function with exponential backoff and jitter
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e

            # Calculate exponential backoff with jitter
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            sleep_time = delay + jitter

            print(f"Attempt {attempt + 1} failed. Retrying in {sleep_time:.2f}s")
            time.sleep(sleep_time)

# Usage
result = retry_with_backoff(lambda: api_call())
```

### 9. Publish-Subscribe Pattern (SNS/SQS)

Decouple services with pub-sub messaging:

```python
import boto3

# Create SNS client
sns = boto3.client('sns')
sqs = boto3.client('sqs')

# Create topic
topic_response = sns.create_topic(Name='order-events')
topic_arn = topic_response['TopicArn']

# Create queue and subscribe to topic
queue_response = sqs.create_queue(QueueName='order-processing')
queue_url = queue_response['QueueUrl']
queue_arn = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['QueueArn']
)['Attributes']['QueueArn']

# Subscribe queue to topic
sns.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint=queue_arn
)

# Publish message
sns.publish(
    TopicArn=topic_arn,
    Message='{"order_id": "12345", "status": "created"}',
    Subject='OrderCreated'
)
```

### 10. API Gateway Lambda Integration

Serverless API with request routing:

```python
import json

def lambda_handler(event, context):
    """
    Lambda function for API Gateway integration
    """
    # Extract request details
    http_method = event.get('httpMethod')
    path = event.get('path')
    body = json.loads(event.get('body', '{}'))

    # Route based on method and path
    if http_method == 'GET' and path == '/items':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'items': ['item1', 'item2']})
        }

    elif http_method == 'POST' and path == '/items':
        # Process new item
        item_id = body.get('id')
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'id': item_id, 'status': 'created'})
        }

    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not found'})
    }
```

## Key Concepts

### Cloud Design Patterns

AWS Prescriptive Guidance covers 13 primary architectural patterns for modern cloud applications:

1. **Anti-corruption Layer** - Mediates between legacy systems and modern microservices, translating data formats and protocols
2. **API Routing Patterns** - Three strategies for routing requests (hostname, path, HTTP header based)
3. **Circuit Breaker** - Prevents cascading failures by detecting faults and stopping requests to failing services
4. **Event Sourcing** - Captures all state changes as a sequence of events for audit trails and replay capability
5. **Hexagonal Architecture** - Separates core business logic from external dependencies and infrastructure
6. **Publish-Subscribe** - Enables asynchronous, decoupled communication between services
7. **Retry with Backoff** - Handles transient failures with progressive delay increases
8. **Saga Patterns** - Manages distributed transactions across microservices (choreography vs orchestration)
9. **Scatter-Gather** - Aggregates results from parallel requests to multiple services
10. **Strangler Fig** - Incrementally replaces legacy systems without complete rewrites
11. **Transactional Outbox** - Ensures reliable message publishing with database transactions

### SageMaker ML Deployment Patterns

**Inference Pipelines:**
- Combine preprocessing and model inference in single endpoint
- Reduce latency by eliminating intermediate data storage
- Simplify deployment by bundling feature engineering with prediction
- Support real-time and batch inference workflows

**MLOps Workflows:**
- Automated model training and deployment pipelines
- Cross-platform integration (Azure DevOps, GitHub Actions)
- Self-service templates with Backstage for standardized deployments
- GPU-optimized training for custom deep learning models

**Architecture Benefits:**
- Single endpoint for preprocessing + inference = lower latency
- Automatic scaling of both preprocessing and model inference
- Consistent feature engineering between training and inference
- Simplified monitoring and logging

### Microservices Architecture Principles

Modern applications emphasize:
- **Scalability** - Horizontal scaling of independent services
- **Release Velocity** - Fast, independent deployments per service
- **Fault Isolation** - Failures contained to individual services
- **Technology Diversity** - Different services can use different tech stacks

### Design Pattern Categories

**Integration Patterns:**
- Anti-corruption layer, API routing, event sourcing

**Resilience Patterns:**
- Circuit breaker, retry with backoff, scatter-gather

**Data Patterns:**
- Event sourcing, transactional outbox, saga orchestration

**Migration Patterns:**
- Strangler fig, hexagonal architecture

## Reference Files

### best_practices.md
Official AWS Prescriptive Guidance best practices for cloud architecture, covering:
- AWS Well-Architected Framework alignment
- Security best practices
- Cost optimization strategies
- Operational excellence guidelines
- Performance efficiency recommendations
- Reliability design patterns

**When to use:** Start here for general AWS architecture guidance and foundational principles.

### patterns.md
Comprehensive catalog of AWS implementation patterns, including:
- MLOps and SageMaker deployment patterns
- Microservices architecture patterns
- DevOps and CI/CD patterns
- Data engineering patterns
- Serverless architecture patterns
- Migration and modernization strategies

**When to use:** Reference when implementing specific solutions or looking for proven architectural approaches.

## Working with This Skill

### For Beginners

**Start with:**
1. Review `best_practices.md` for AWS foundational concepts
2. Explore simple patterns like retry with backoff or publish-subscribe
3. Use the Quick Reference section for copy-paste examples
4. Focus on single-service patterns before multi-service architectures

**Recommended learning path:**
- Basic SageMaker deployment → Inference pipelines → MLOps workflows
- Simple Lambda functions → API Gateway integration → Microservices
- Single pattern → Combined patterns → Full architecture design

### For Intermediate Users

**Focus on:**
1. Multi-service integration patterns (circuit breaker, saga patterns)
2. SageMaker inference pipelines with custom preprocessing
3. Event-driven architectures with SNS/SQS
4. API Gateway patterns with Lambda integrations
5. DevOps automation for ML model deployment

**Navigation tips:**
- Use `patterns.md` for comprehensive implementation guides
- Combine multiple patterns for complex architectures
- Reference Quick Reference for implementation details
- Study MLOps workflows for production ML systems

### For Advanced Users

**Deep dive into:**
1. Complex saga orchestration patterns
2. Multi-region, multi-account architectures
3. Custom SageMaker algorithms with GPU optimization
4. Hexagonal architecture for domain-driven design
5. Event sourcing with CQRS patterns
6. Cross-cloud MLOps with Azure DevOps or GitHub Actions

**Best practices:**
- Combine multiple patterns for enterprise architectures
- Implement observability and monitoring from the start
- Use infrastructure as code (CloudFormation, CDK, Terraform)
- Design for failure with circuit breakers and retry logic
- Implement proper security boundaries and IAM policies

## Technology Stack

### Core AWS Services
- **Amazon SageMaker** - ML model training and deployment
- **Amazon SageMaker Studio** - Integrated ML development environment
- **AWS Lambda** - Serverless compute
- **Amazon API Gateway** - RESTful API management
- **Amazon SNS** - Pub-sub messaging
- **Amazon SQS** - Message queuing
- **Amazon ECR** - Container registry
- **Amazon S3** - Object storage
- **AWS CloudFormation** - Infrastructure as code

### ML Frameworks
- **Scikit-learn** - Preprocessing and traditional ML
- **PyTorch** - Deep learning models
- **TensorFlow** - Neural network frameworks
- **XGBoost** - Gradient boosting
- **CatBoost** - Categorical feature handling

### DevOps Tools
- **Azure DevOps** - Cross-cloud CI/CD
- **GitHub Actions** - Workflow automation
- **Backstage** - Developer portal and templates
- **Hydra** - ML experiment configuration

## Common Workflows

### Deploy ML Model with Preprocessing

1. **Prepare data and upload to S3**
2. **Create preprocessing estimator** (SKLearn, custom containers)
3. **Train preprocessing on sample data**
4. **Create ML model estimator** (Linear Learner, XGBoost, custom)
5. **Train model on preprocessed data**
6. **Combine into pipeline model**
7. **Deploy pipeline to SageMaker endpoint**
8. **Test with raw input data**

### Implement Resilient Microservice

1. **Design service boundaries** (hexagonal architecture)
2. **Implement circuit breaker** for external calls
3. **Add retry with exponential backoff** for transient failures
4. **Use pub-sub pattern** for async communication
5. **Implement health checks** and monitoring
6. **Add API Gateway** for routing and throttling
7. **Deploy with auto-scaling** and load balancing

### Modernize Legacy System

1. **Analyze legacy system** and identify boundaries
2. **Implement anti-corruption layer** for integration
3. **Use strangler fig pattern** for incremental migration
4. **Build new services** with hexagonal architecture
5. **Route traffic gradually** to new services
6. **Monitor and validate** new implementations
7. **Decommission legacy components** incrementally

## Prerequisites

### For SageMaker Development
- Active AWS account with appropriate IAM permissions
- Python 3.9 or higher
- SageMaker Python SDK (v2.49.2+)
- Boto3 library for AWS API access
- Understanding of ML concepts and workflows

### For Architecture Implementation
- AWS account with admin or PowerUser access
- Familiarity with AWS core services (EC2, S3, Lambda)
- Understanding of distributed systems concepts
- Experience with microservices architectures (helpful)
- Knowledge of IaC tools (CloudFormation, CDK, Terraform)

### Development Environment
```bash
# Install required Python packages
pip install boto3 sagemaker scikit-learn pandas numpy

# Configure AWS credentials
aws configure
```

## Resources

### Official Documentation Links
- AWS Prescriptive Guidance: https://docs.aws.amazon.com/prescriptive-guidance/
- SageMaker Developer Guide: https://docs.aws.amazon.com/sagemaker/
- AWS Architecture Center: https://aws.amazon.com/architecture/

### Pattern Categories
- **MLOps Patterns** - Model deployment, training automation, endpoint management
- **DevOps Patterns** - CI/CD pipelines, infrastructure automation, deployment strategies
- **Microservices Patterns** - Service communication, resilience, API design
- **Data Patterns** - Data pipelines, event streaming, batch processing
- **Migration Patterns** - Legacy modernization, cloud migration, hybrid architectures

## Notes

- Patterns include step-by-step implementation guides with code examples
- All code examples tested with latest AWS SDK versions
- SageMaker examples use Python 3.9+ and SageMaker SDK 2.x
- Architecture patterns follow AWS Well-Architected Framework
- Reference implementations available in AWS Solutions Library
- Examples assume standard AWS regions (us-east-1, us-west-2)

## Best Practices

### SageMaker Deployment
- Use inference pipelines to bundle preprocessing with models
- Implement batch transform for large-scale predictions
- Enable auto-scaling for production endpoints
- Use multi-model endpoints for cost optimization
- Implement proper IAM roles with least privilege
- Enable CloudWatch logging and monitoring

### Architecture Design
- Design for failure - assume components will fail
- Implement retry logic with exponential backoff
- Use circuit breakers to prevent cascade failures
- Decouple services with asynchronous messaging
- Implement proper observability from day one
- Use infrastructure as code for reproducibility
- Follow the strangler fig pattern for migrations

### Cost Optimization
- Use SageMaker Savings Plans for predictable workloads
- Leverage spot instances for training jobs
- Implement auto-scaling for endpoints
- Use multi-model endpoints to reduce costs
- Monitor and optimize compute instance types
- Clean up unused resources and endpoints

## Updating

This skill is based on AWS Prescriptive Guidance documentation. AWS regularly updates patterns and best practices, so:
- Check AWS Prescriptive Guidance website for latest patterns
- Review SageMaker SDK changelogs for API updates
- Follow AWS architecture blog for new design patterns
- Subscribe to AWS What's New for service updates
