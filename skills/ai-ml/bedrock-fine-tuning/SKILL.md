---
name: bedrock-fine-tuning
description: Amazon Bedrock Model Customization with fine-tuning, continued pre-training, reinforcement fine-tuning (NEW 2025 - 66% accuracy gains), and distillation. Create customization jobs, monitor training, deploy custom models, and evaluate performance. Use when customizing Claude, Titan, or other Bedrock models for domain-specific tasks, adapting to proprietary data, improving accuracy on specialized workflows, or distilling large models to smaller ones.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
---

# Amazon Bedrock Model Customization

Complete guide to customizing Amazon Bedrock foundation models through fine-tuning, continued pre-training, reinforcement fine-tuning, and distillation.

## Overview

Amazon Bedrock Model Customization allows you to adapt foundation models to your specific use cases without managing infrastructure. Four customization approaches are available:

### 1. Fine-Tuning (Supervised Learning)
Adapt models to specific tasks using labeled examples (input-output pairs). Best for:
- Task-specific optimization (classification, extraction, generation)
- Improving responses for domain terminology
- Teaching specific output formats
- **Typical gains**: 20-40% accuracy improvement

### 2. Continued Pre-Training (Domain Adaptation)
Continue training on unlabeled domain-specific text to build domain knowledge. Best for:
- Medical, legal, financial, technical domains
- Proprietary knowledge bases
- Industry-specific language
- **Typical gains**: 15-30% domain accuracy improvement

### 3. Reinforcement Fine-Tuning (NEW 2025)
Use reinforcement learning with human feedback (RLHF) or AI feedback (RLAIF) for alignment. Best for:
- Improving response quality and safety
- Aligning to brand voice and values
- Reducing hallucinations
- **Typical gains**: 40-66% accuracy improvement (AWS announced 66% gains in 2025)

### 4. Distillation (Teacher-Student)
Transfer knowledge from larger models to smaller, faster models. Best for:
- Cost optimization (smaller models are cheaper)
- Latency reduction (faster inference)
- Maintaining quality while reducing size
- **Typical gains**: 80-90% of teacher model quality at 50-70% cost reduction

## Supported Models

| Model | Fine-Tuning | Continued Pre-Training | Reinforcement | Distillation |
|-------|-------------|------------------------|---------------|--------------|
| **Claude 3.5 Sonnet** | ✅ | ✅ | ✅ (2025) | ✅ (teacher) |
| **Claude 3 Haiku** | ✅ | ✅ | ✅ (2025) | ✅ (student) |
| **Claude 3 Opus** | ✅ | ✅ | ✅ (2025) | ✅ (teacher) |
| **Titan Text G1** | ✅ | ✅ | ❌ | ✅ |
| **Titan Text Lite** | ✅ | ✅ | ❌ | ✅ (student) |
| **Titan Embeddings** | ✅ | ✅ | ❌ | ❌ |
| **Cohere Command** | ✅ | ✅ | ✅ | ✅ |
| **AI21 Jurassic-2** | ✅ | ✅ | ❌ | ✅ |

**Note**: Availability varies by region. Check AWS Console for latest model support.

## Training Data Formats

### Fine-Tuning Format (JSONL)

```jsonl
{"prompt": "Classify the medical condition: Patient presents with fever, cough, and fatigue.", "completion": "Likely viral infection. Recommend rest, hydration, and symptomatic treatment."}
{"prompt": "Classify the medical condition: Patient has chest pain, shortness of breath, and dizziness.", "completion": "Potential cardiac event. Immediate emergency evaluation required."}
{"prompt": "Classify the medical condition: Patient reports persistent headache and light sensitivity.", "completion": "Possible migraine. Consider neurological consultation if symptoms persist."}
```

**Requirements**:
- Minimum 32 examples (recommended: 1000+)
- Maximum 10,000 examples per job
- Each example: prompt + completion
- JSONL format (one JSON object per line)
- Max 32K tokens per example

### Continued Pre-Training Format (JSONL)

```jsonl
{"text": "The HIPAA Privacy Rule establishes national standards for protecting individuals' medical records and personal health information. Covered entities must implement safeguards to ensure confidentiality."}
{"text": "Electronic health records (EHR) systems integrate patient data from multiple sources, enabling comprehensive care coordination. Interoperability standards like HL7 FHIR facilitate data exchange."}
{"text": "Clinical decision support systems (CDSS) analyze patient data to provide evidence-based recommendations. Integration with EHR workflows improves diagnostic accuracy and treatment outcomes."}
```

**Requirements**:
- Minimum 1000 examples (recommended: 10,000+)
- Maximum 100,000 examples per job
- Unlabeled text only
- JSONL format
- Max 32K tokens per document

### Reinforcement Fine-Tuning Format (JSONL)

```jsonl
{"prompt": "Explain type 2 diabetes to a patient.", "chosen": "Type 2 diabetes is a condition where your body doesn't use insulin properly. This causes high blood sugar. Managing it involves healthy eating, exercise, and sometimes medication.", "rejected": "Type 2 diabetes mellitus is characterized by insulin resistance and relative insulin deficiency leading to hyperglycemia."}
{"prompt": "What should I do if I miss a dose?", "chosen": "If you miss a dose, take it as soon as you remember. If it's almost time for your next dose, skip the missed one. Don't double up. Call your doctor if you have questions.", "rejected": "Consult the prescribing information or contact your healthcare provider immediately."}
```

**Requirements**:
- Minimum 100 preference pairs (recommended: 1000+)
- Each example: prompt + chosen response + rejected response
- JSONL format
- Max 32K tokens per example
- Ranking score optional (0.0-1.0)

### Distillation Format (No Training Data Required)

Distillation uses the teacher model's outputs automatically:
```python
# Configuration only - no training data needed
distillation_config = {
    'teacherModelId': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
    'studentModelId': 'anthropic.claude-3-haiku-20240307-v1:0',
    'distillationDataSource': {
        'promptDataset': {
            's3Uri': 's3://bucket/prompts.jsonl'  # Just prompts, no completions
        }
    }
}
```

**Prompt Dataset Format**:
```jsonl
{"prompt": "Explain the water cycle."}
{"prompt": "What are the symptoms of the flu?"}
{"prompt": "Describe photosynthesis."}
```

**Requirements**:
- Minimum 1000 prompts (recommended: 10,000+)
- Teacher model generates completions automatically
- Student model trained to match teacher outputs

## Quick Start

### 1. Prepare Training Data

```python
import json

# Fine-tuning examples
training_data = [
    {
        "prompt": "Classify sentiment: This product exceeded my expectations!",
        "completion": "Positive"
    },
    {
        "prompt": "Classify sentiment: Terrible customer service, very disappointed.",
        "completion": "Negative"
    },
    {
        "prompt": "Classify sentiment: The item was okay, nothing special.",
        "completion": "Neutral"
    }
]

# Save as JSONL
with open('training_data.jsonl', 'w') as f:
    for example in training_data:
        f.write(json.dumps(example) + '\n')
```

### 2. Upload to S3

```python
import boto3

s3 = boto3.client('s3')
bucket_name = 'my-bedrock-training-bucket'

# Upload training data
s3.upload_file('training_data.jsonl', bucket_name, 'fine-tuning/training_data.jsonl')

# Upload validation data (optional but recommended)
s3.upload_file('validation_data.jsonl', bucket_name, 'fine-tuning/validation_data.jsonl')
```

### 3. Create Customization Job

```python
bedrock = boto3.client('bedrock')

response = bedrock.create_model_customization_job(
    jobName='sentiment-classifier-v1',
    customModelName='sentiment-classifier',
    roleArn='arn:aws:iam::123456789012:role/BedrockCustomizationRole',
    baseModelIdentifier='anthropic.claude-3-haiku-20240307-v1:0',
    trainingDataConfig={
        's3Uri': f's3://{bucket_name}/fine-tuning/training_data.jsonl'
    },
    validationDataConfig={
        's3Uri': f's3://{bucket_name}/fine-tuning/validation_data.jsonl'
    },
    outputDataConfig={
        's3Uri': f's3://{bucket_name}/fine-tuning/output/'
    },
    hyperParameters={
        'epochCount': '3',
        'batchSize': '8',
        'learningRate': '0.00001'
    }
)

job_arn = response['jobArn']
print(f"Customization job created: {job_arn}")
```

### 4. Monitor Training

```python
# Check job status
response = bedrock.get_model_customization_job(jobIdentifier=job_arn)
status = response['status']  # InProgress, Completed, Failed, Stopped

print(f"Job status: {status}")

if status == 'Completed':
    custom_model_arn = response['outputModelArn']
    print(f"Custom model ARN: {custom_model_arn}")
```

### 5. Deploy and Test

```python
bedrock_runtime = boto3.client('bedrock-runtime')

# Use custom model
response = bedrock_runtime.invoke_model(
    modelId=custom_model_arn,
    body=json.dumps({
        "prompt": "Classify sentiment: I love this product!",
        "max_tokens": 50
    })
)

result = json.loads(response['body'].read())
print(f"Prediction: {result['completion']}")
```

## Operations

### create-fine-tuning-job

Create a supervised fine-tuning job with labeled examples.

```python
import boto3
import json

def create_fine_tuning_job(
    job_name: str,
    model_name: str,
    base_model_id: str,
    training_s3_uri: str,
    output_s3_uri: str,
    role_arn: str,
    validation_s3_uri: str = None,
    hyper_params: dict = None
) -> str:
    """
    Create fine-tuning job for task-specific adaptation.

    Args:
        job_name: Unique job identifier
        model_name: Name for custom model
        base_model_id: Base model ARN (e.g., Claude 3 Haiku)
        training_s3_uri: S3 path to training JSONL
        output_s3_uri: S3 path for outputs
        role_arn: IAM role with Bedrock + S3 permissions
        validation_s3_uri: Optional validation dataset
        hyper_params: Training hyperparameters

    Returns:
        Job ARN for monitoring
    """
    bedrock = boto3.client('bedrock')

    # Default hyperparameters
    if hyper_params is None:
        hyper_params = {
            'epochCount': '3',           # Number of training epochs
            'batchSize': '8',            # Batch size (4, 8, 16, 32)
            'learningRate': '0.00001',   # Learning rate (0.00001 - 0.0001)
            'learningRateWarmupSteps': '0'
        }

    # Build configuration
    config = {
        'jobName': job_name,
        'customModelName': model_name,
        'roleArn': role_arn,
        'baseModelIdentifier': base_model_id,
        'trainingDataConfig': {
            's3Uri': training_s3_uri
        },
        'outputDataConfig': {
            's3Uri': output_s3_uri
        },
        'hyperParameters': hyper_params,
        'customizationType': 'FINE_TUNING'
    }

    # Add validation data if provided
    if validation_s3_uri:
        config['validationDataConfig'] = {
            's3Uri': validation_s3_uri
        }

    # Create job
    response = bedrock.create_model_customization_job(**config)

    print(f"Fine-tuning job created: {response['jobArn']}")
    return response['jobArn']


# Example: Fine-tune Claude 3 Haiku for medical classification
job_arn = create_fine_tuning_job(
    job_name='medical-classifier-v1',
    model_name='medical-classifier',
    base_model_id='anthropic.claude-3-haiku-20240307-v1:0',
    training_s3_uri='s3://my-bucket/medical/training.jsonl',
    output_s3_uri='s3://my-bucket/medical/output/',
    role_arn='arn:aws:iam::123456789012:role/BedrockCustomizationRole',
    validation_s3_uri='s3://my-bucket/medical/validation.jsonl',
    hyper_params={
        'epochCount': '5',
        'batchSize': '16',
        'learningRate': '0.00002'
    }
)
```

### create-continued-pretraining-job

Create continued pre-training job for domain adaptation.

```python
def create_continued_pretraining_job(
    job_name: str,
    model_name: str,
    base_model_id: str,
    training_s3_uri: str,
    output_s3_uri: str,
    role_arn: str,
    validation_s3_uri: str = None
) -> str:
    """
    Create continued pre-training job for domain knowledge.

    Args:
        job_name: Unique job identifier
        model_name: Name for custom model
        base_model_id: Base model ARN
        training_s3_uri: S3 path to unlabeled text JSONL
        output_s3_uri: S3 path for outputs
        role_arn: IAM role ARN
        validation_s3_uri: Optional validation dataset

    Returns:
        Job ARN for monitoring
    """
    bedrock = boto3.client('bedrock')

    config = {
        'jobName': job_name,
        'customModelName': model_name,
        'roleArn': role_arn,
        'baseModelIdentifier': base_model_id,
        'trainingDataConfig': {
            's3Uri': training_s3_uri
        },
        'outputDataConfig': {
            's3Uri': output_s3_uri
        },
        'hyperParameters': {
            'epochCount': '1',  # Usually 1 epoch for continued pre-training
            'batchSize': '16',
            'learningRate': '0.000005'  # Lower LR for stability
        },
        'customizationType': 'CONTINUED_PRE_TRAINING'
    }

    if validation_s3_uri:
        config['validationDataConfig'] = {
            's3Uri': validation_s3_uri
        }

    response = bedrock.create_model_customization_job(**config)

    print(f"Continued pre-training job created: {response['jobArn']}")
    return response['jobArn']


# Example: Adapt Claude for medical domain
job_arn = create_continued_pretraining_job(
    job_name='medical-domain-adapter-v1',
    model_name='claude-medical',
    base_model_id='anthropic.claude-3-5-sonnet-20241022-v2:0',
    training_s3_uri='s3://my-bucket/medical-corpus/documents.jsonl',
    output_s3_uri='s3://my-bucket/medical-corpus/output/',
    role_arn='arn:aws:iam::123456789012:role/BedrockCustomizationRole'
)
```

### create-reinforcement-finetuning-job

Create reinforcement fine-tuning job with preference data (NEW 2025).

```python
def create_reinforcement_finetuning_job(
    job_name: str,
    model_name: str,
    base_model_id: str,
    preference_s3_uri: str,
    output_s3_uri: str,
    role_arn: str,
    algorithm: str = 'DPO'  # DPO, PPO, or RLAIF
) -> str:
    """
    Create reinforcement fine-tuning job for alignment (NEW 2025).

    Args:
        job_name: Unique job identifier
        model_name: Name for custom model
        base_model_id: Base model ARN
        preference_s3_uri: S3 path to preference pairs JSONL
        output_s3_uri: S3 path for outputs
        role_arn: IAM role ARN
        algorithm: RL algorithm (DPO, PPO, RLAIF)

    Returns:
        Job ARN for monitoring
    """
    bedrock = boto3.client('bedrock')

    config = {
        'jobName': job_name,
        'customModelName': model_name,
        'roleArn': role_arn,
        'baseModelIdentifier': base_model_id,
        'trainingDataConfig': {
            's3Uri': preference_s3_uri
        },
        'outputDataConfig': {
            's3Uri': output_s3_uri
        },
        'hyperParameters': {
            'epochCount': '3',
            'batchSize': '8',
            'learningRate': '0.00001',
            'rlAlgorithm': algorithm,
            'beta': '0.1'  # KL divergence coefficient
        },
        'customizationType': 'REINFORCEMENT_FINE_TUNING'
    }

    response = bedrock.create_model_customization_job(**config)

    print(f"Reinforcement fine-tuning job created: {response['jobArn']}")
    print(f"Expected accuracy gains: 40-66% improvement")
    return response['jobArn']


# Example: Improve response quality with preference learning
job_arn = create_reinforcement_finetuning_job(
    job_name='claude-aligned-v1',
    model_name='claude-aligned',
    base_model_id='anthropic.claude-3-5-sonnet-20241022-v2:0',
    preference_s3_uri='s3://my-bucket/preferences/pairs.jsonl',
    output_s3_uri='s3://my-bucket/preferences/output/',
    role_arn='arn:aws:iam::123456789012:role/BedrockCustomizationRole',
    algorithm='DPO'  # Direct Preference Optimization
)
```

### create-distillation-job

Create distillation job to transfer knowledge from large to small model.

```python
def create_distillation_job(
    job_name: str,
    model_name: str,
    teacher_model_id: str,
    student_model_id: str,
    prompts_s3_uri: str,
    output_s3_uri: str,
    role_arn: str
) -> str:
    """
    Create distillation job to compress large model knowledge.

    Args:
        job_name: Unique job identifier
        model_name: Name for distilled model
        teacher_model_id: Large model to learn from
        student_model_id: Small model to train
        prompts_s3_uri: S3 path to prompts JSONL
        output_s3_uri: S3 path for outputs
        role_arn: IAM role ARN

    Returns:
        Job ARN for monitoring
    """
    bedrock = boto3.client('bedrock')

    config = {
        'jobName': job_name,
        'customModelName': model_name,
        'roleArn': role_arn,
        'baseModelIdentifier': student_model_id,
        'trainingDataConfig': {
            's3Uri': prompts_s3_uri,
            'teacherModelIdentifier': teacher_model_id
        },
        'outputDataConfig': {
            's3Uri': output_s3_uri
        },
        'hyperParameters': {
            'epochCount': '3',
            'batchSize': '16',
            'learningRate': '0.00002',
            'temperature': '1.0',  # Softmax temperature for distillation
            'alpha': '0.5'         # Balance between hard and soft targets
        },
        'customizationType': 'DISTILLATION'
    }

    response = bedrock.create_model_customization_job(**config)

    print(f"Distillation job created: {response['jobArn']}")
    print(f"Teacher: {teacher_model_id}")
    print(f"Student: {student_model_id}")
    print(f"Expected: 80-90% teacher quality at 50-70% cost")
    return response['jobArn']


# Example: Distill Claude 3.5 Sonnet to Haiku
job_arn = create_distillation_job(
    job_name='claude-haiku-distilled-v1',
    model_name='claude-haiku-distilled',
    teacher_model_id='anthropic.claude-3-5-sonnet-20241022-v2:0',
    student_model_id='anthropic.claude-3-haiku-20240307-v1:0',
    prompts_s3_uri='s3://my-bucket/distillation/prompts.jsonl',
    output_s3_uri='s3://my-bucket/distillation/output/',
    role_arn='arn:aws:iam::123456789012:role/BedrockCustomizationRole'
)
```

### monitor-job

Track training progress and retrieve metrics.

```python
import time
from typing import Dict, Any

def monitor_job(job_arn: str, poll_interval: int = 60) -> Dict[str, Any]:
    """
    Monitor customization job until completion.

    Args:
        job_arn: Job ARN to monitor
        poll_interval: Seconds between status checks

    Returns:
        Final job details with metrics
    """
    bedrock = boto3.client('bedrock')

    print(f"Monitoring job: {job_arn}")

    while True:
        response = bedrock.get_model_customization_job(
            jobIdentifier=job_arn
        )

        status = response['status']

        print(f"Status: {status}", end='')

        # Show metrics if available
        if 'trainingMetrics' in response:
            metrics = response['trainingMetrics']
            if 'trainingLoss' in metrics:
                print(f" | Loss: {metrics['trainingLoss']:.4f}", end='')

        print()  # Newline

        # Check terminal states
        if status == 'Completed':
            print(f"Job completed successfully!")
            print(f"Custom model ARN: {response['outputModelArn']}")
            return response

        elif status == 'Failed':
            print(f"Job failed: {response.get('failureMessage', 'Unknown error')}")
            return response

        elif status == 'Stopped':
            print(f"Job was stopped")
            return response

        # Wait before next check
        time.sleep(poll_interval)


# Example: Monitor with automatic polling
job_details = monitor_job(job_arn, poll_interval=60)

if job_details['status'] == 'Completed':
    custom_model_arn = job_details['outputModelArn']

    # Download metrics from S3
    output_uri = job_details['outputDataConfig']['s3Uri']
    print(f"Metrics available at: {output_uri}")
```

### deploy-custom-model

Provision custom model for inference.

```python
def deploy_custom_model(
    model_arn: str,
    provisioned_model_name: str,
    model_units: int = 1
) -> str:
    """
    Deploy custom model with provisioned throughput.

    Args:
        model_arn: Custom model ARN from training job
        provisioned_model_name: Name for provisioned model
        model_units: Throughput units (1-10)

    Returns:
        Provisioned model ARN for inference
    """
    bedrock = boto3.client('bedrock')

    response = bedrock.create_provisioned_model_throughput(
        provisionedModelName=provisioned_model_name,
        modelId=model_arn,
        modelUnits=model_units
    )

    provisioned_arn = response['provisionedModelArn']

    print(f"Provisioned model created: {provisioned_arn}")
    print(f"Throughput: {model_units} units")
    print(f"Allow 5-10 minutes for provisioning")

    return provisioned_arn


# Example: Deploy with standard throughput
provisioned_arn = deploy_custom_model(
    model_arn='arn:aws:bedrock:us-east-1:123456789012:custom-model/medical-classifier-v1',
    provisioned_model_name='medical-classifier-prod',
    model_units=2
)

# Wait for provisioning
time.sleep(300)  # 5 minutes

# Use provisioned model
bedrock_runtime = boto3.client('bedrock-runtime')

response = bedrock_runtime.invoke_model(
    modelId=provisioned_arn,
    body=json.dumps({
        "prompt": "Classify: Patient has fever and cough.",
        "max_tokens": 100
    })
)

result = json.loads(response['body'].read())
print(f"Prediction: {result['completion']}")
```

### evaluate-model

Test custom model performance with evaluation dataset.

```python
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def evaluate_model(
    model_id: str,
    test_data_path: str,
    output_path: str = None
) -> Dict[str, float]:
    """
    Evaluate custom model on test dataset.

    Args:
        model_id: Custom model ARN
        test_data_path: Path to test JSONL file
        output_path: Optional path to save predictions

    Returns:
        Evaluation metrics dictionary
    """
    bedrock_runtime = boto3.client('bedrock-runtime')

    # Load test data
    test_data = []
    with open(test_data_path, 'r') as f:
        for line in f:
            test_data.append(json.loads(line))

    # Run predictions
    predictions = []
    ground_truth = []

    print(f"Evaluating {len(test_data)} examples...")

    for i, example in enumerate(test_data):
        if i % 10 == 0:
            print(f"Progress: {i}/{len(test_data)}")

        # Invoke model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "prompt": example['prompt'],
                "max_tokens": 200
            })
        )

        result = json.loads(response['body'].read())
        prediction = result['completion'].strip()

        predictions.append(prediction)
        ground_truth.append(example['completion'].strip())

    # Calculate metrics
    accuracy = accuracy_score(ground_truth, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        ground_truth, predictions, average='weighted', zero_division=0
    )

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'total_examples': len(test_data)
    }

    print("\n=== Evaluation Results ===")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    # Save predictions if requested
    if output_path:
        results_df = pd.DataFrame({
            'prompt': [ex['prompt'] for ex in test_data],
            'ground_truth': ground_truth,
            'prediction': predictions
        })
        results_df.to_csv(output_path, index=False)
        print(f"Predictions saved to: {output_path}")

    return metrics


# Example: Evaluate medical classifier
metrics = evaluate_model(
    model_id='arn:aws:bedrock:us-east-1:123456789012:provisioned-model/medical-classifier-prod',
    test_data_path='test_data.jsonl',
    output_path='evaluation_results.csv'
)
```

## Hyperparameter Tuning

### Fine-Tuning Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| **epochCount** | 1-10 | 3 | Training passes over dataset |
| **batchSize** | 4-32 | 8 | Examples per training step |
| **learningRate** | 0.00001-0.0001 | 0.00001 | Step size for weight updates |
| **learningRateWarmupSteps** | 0-100 | 0 | Gradual LR increase steps |

**Tuning Guidelines**:
- **Small dataset (<100 examples)**: Lower epochs (1-2), smaller batch (4-8)
- **Medium dataset (100-1000)**: Standard settings (3 epochs, batch 8-16)
- **Large dataset (>1000)**: Higher epochs (5-10), larger batch (16-32)
- **Overfitting signs**: Reduce epochs or increase batch size
- **Underfitting signs**: Increase epochs or decrease learning rate

### Example Configurations

```python
# Configuration 1: Small dataset, quick iteration
small_dataset_params = {
    'epochCount': '2',
    'batchSize': '4',
    'learningRate': '0.00002',
    'learningRateWarmupSteps': '10'
}

# Configuration 2: Balanced, general purpose
balanced_params = {
    'epochCount': '3',
    'batchSize': '8',
    'learningRate': '0.00001',
    'learningRateWarmupSteps': '0'
}

# Configuration 3: Large dataset, high quality
large_dataset_params = {
    'epochCount': '5',
    'batchSize': '16',
    'learningRate': '0.000005',
    'learningRateWarmupSteps': '20'
}

# Configuration 4: Continued pre-training
pretraining_params = {
    'epochCount': '1',
    'batchSize': '16',
    'learningRate': '0.000005',
    'learningRateWarmupSteps': '0'
}
```

## Data Preparation Best Practices

### 1. Data Quality

```python
def validate_training_data(data_path: str) -> bool:
    """
    Validate training data quality.

    Checks:
    - JSONL format validity
    - Required fields present
    - Token length within limits
    - Data distribution balance
    """
    import json
    from collections import Counter

    issues = []
    completion_distribution = Counter()

    with open(data_path, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                example = json.loads(line)
            except json.JSONDecodeError:
                issues.append(f"Line {i}: Invalid JSON")
                continue

            # Check required fields
            if 'prompt' not in example:
                issues.append(f"Line {i}: Missing 'prompt' field")
            if 'completion' not in example:
                issues.append(f"Line {i}: Missing 'completion' field")

            # Track completion distribution
            if 'completion' in example:
                completion_distribution[example['completion']] += 1

            # Check token length (approximate)
            prompt_tokens = len(example.get('prompt', '').split())
            completion_tokens = len(example.get('completion', '').split())
            total_tokens = prompt_tokens + completion_tokens

            if total_tokens > 8000:  # Conservative estimate
                issues.append(f"Line {i}: Likely exceeds 32K token limit")

    # Report issues
    if issues:
        print("Data Validation Issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
        return False

    # Check distribution balance
    print("\nCompletion Distribution:")
    for completion, count in completion_distribution.most_common():
        print(f"  {completion}: {count}")

    # Warn about imbalance
    counts = list(completion_distribution.values())
    if max(counts) > 3 * min(counts):
        print("\nWarning: Imbalanced dataset detected")
        print("Consider balancing or stratified sampling")

    print("\nValidation passed!")
    return True


# Example usage
validate_training_data('training_data.jsonl')
```

### 2. Data Augmentation

```python
def augment_training_data(
    input_path: str,
    output_path: str,
    augmentation_factor: int = 2
):
    """
    Augment training data with paraphrasing and variations.

    Args:
        input_path: Original training data
        output_path: Augmented output file
        augmentation_factor: Multiplier for dataset size
    """
    import random

    # Load original data
    original_data = []
    with open(input_path, 'r') as f:
        for line in f:
            original_data.append(json.loads(line))

    # Augmentation strategies
    prompt_prefixes = [
        "",
        "Please ",
        "Could you ",
        "I need you to "
    ]

    augmented_data = []

    for example in original_data:
        # Include original
        augmented_data.append(example)

        # Create variations
        for _ in range(augmentation_factor - 1):
            prefix = random.choice(prompt_prefixes)
            augmented_example = {
                'prompt': prefix + example['prompt'],
                'completion': example['completion']
            }
            augmented_data.append(augmented_example)

    # Save augmented data
    with open(output_path, 'w') as f:
        for example in augmented_data:
            f.write(json.dumps(example) + '\n')

    print(f"Augmented {len(original_data)} → {len(augmented_data)} examples")


# Example usage
augment_training_data('training_data.jsonl', 'training_data_augmented.jsonl')
```

### 3. Train/Validation Split

```python
def split_dataset(
    input_path: str,
    train_path: str,
    val_path: str,
    val_split: float = 0.2
):
    """
    Split dataset into training and validation sets.

    Args:
        input_path: Full dataset JSONL
        train_path: Output training JSONL
        val_path: Output validation JSONL
        val_split: Fraction for validation (0.1-0.3)
    """
    import random

    # Load data
    data = []
    with open(input_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))

    # Shuffle
    random.shuffle(data)

    # Split
    val_size = int(len(data) * val_split)
    train_data = data[val_size:]
    val_data = data[:val_size]

    # Save
    with open(train_path, 'w') as f:
        for example in train_data:
            f.write(json.dumps(example) + '\n')

    with open(val_path, 'w') as f:
        for example in val_data:
            f.write(json.dumps(example) + '\n')

    print(f"Split: {len(train_data)} training, {len(val_data)} validation")


# Example usage
split_dataset('full_dataset.jsonl', 'training.jsonl', 'validation.jsonl', val_split=0.2)
```

## Cost Considerations

### Training Costs

**Cost Structure**:
- **Fine-tuning**: $0.01-0.05 per 1000 tokens processed
- **Continued pre-training**: $0.02-0.08 per 1000 tokens processed
- **Reinforcement fine-tuning**: $0.03-0.10 per 1000 tokens processed
- **Distillation**: $0.02-0.06 per 1000 tokens processed

**Example Calculations**:

```python
def estimate_training_cost(
    num_examples: int,
    avg_tokens_per_example: int,
    num_epochs: int,
    cost_per_1k_tokens: float = 0.03
) -> float:
    """
    Estimate training cost.

    Args:
        num_examples: Number of training examples
        avg_tokens_per_example: Average tokens (prompt + completion)
        num_epochs: Training epochs
        cost_per_1k_tokens: Cost rate

    Returns:
        Estimated cost in USD
    """
    total_tokens = num_examples * avg_tokens_per_example * num_epochs
    cost = (total_tokens / 1000) * cost_per_1k_tokens

    print(f"Training Examples: {num_examples:,}")
    print(f"Avg Tokens/Example: {avg_tokens_per_example}")
    print(f"Epochs: {num_epochs}")
    print(f"Total Tokens: {total_tokens:,}")
    print(f"Estimated Cost: ${cost:.2f}")

    return cost


# Example: Fine-tune with 1000 examples
estimate_training_cost(
    num_examples=1000,
    avg_tokens_per_example=500,
    num_epochs=3,
    cost_per_1k_tokens=0.03
)
# Output: ~$45
```

### Inference Costs

**Provisioned Throughput Pricing**:
- **Model Units**: $X per hour per unit
- **Cost varies by base model**
- **Minimum commitment**: 1 month or 6 months

**Cost Optimization**:

```python
def compare_model_costs(
    requests_per_day: int,
    avg_tokens_per_request: int
):
    """
    Compare on-demand vs provisioned vs distilled model costs.
    """
    # Base Claude 3.5 Sonnet on-demand: $3/$15 per 1M tokens
    base_cost_input = (requests_per_day * avg_tokens_per_request * 30) / 1_000_000 * 3
    base_cost_output = (requests_per_day * avg_tokens_per_request * 0.5 * 30) / 1_000_000 * 15
    base_monthly = base_cost_input + base_cost_output

    # Provisioned throughput: ~$2500/month per unit
    provisioned_monthly = 2500

    # Distilled to Haiku: 50% cost reduction
    distilled_monthly = base_monthly * 0.5

    print(f"Monthly Cost Comparison ({requests_per_day:,} requests/day):")
    print(f"  Base Model On-Demand: ${base_monthly:.2f}")
    print(f"  Provisioned (1 unit):  ${provisioned_monthly:.2f}")
    print(f"  Distilled Model:       ${distilled_monthly:.2f}")

    # Breakeven analysis
    if base_monthly > provisioned_monthly:
        print(f"\nProvisioned throughput recommended (saves ${base_monthly - provisioned_monthly:.2f}/mo)")
    else:
        print(f"\nOn-demand recommended (saves ${provisioned_monthly - base_monthly:.2f}/mo)")


# Example comparison
compare_model_costs(requests_per_day=10000, avg_tokens_per_request=1000)
```

## Related Skills

- **bedrock-inference**: Invoke foundation models and custom models
- **bedrock-knowledge-bases**: RAG with custom models
- **bedrock-guardrails**: Apply safety policies to custom models
- **bedrock-agentcore**: Build agents with custom models
- **claude-cost-optimization**: Optimize model selection and costs
- **claude-context-management**: Manage context for custom models
- **boto3-ecs**: Deploy custom model inference on ECS
- **boto3-eks**: Deploy custom model inference on EKS

## Additional Resources

- [Bedrock Model Customization Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization.html)
- [Fine-tuning Best Practices](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prepare.html)
- [Custom Model Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Reinforcement Fine-tuning Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-rlhf.html) (2025)
