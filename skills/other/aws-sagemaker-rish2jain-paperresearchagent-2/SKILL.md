---
name: aws-sagemaker
description: Amazon SageMaker for building, training, and deploying machine learning models. Use for SageMaker AI endpoints, model training, inference, MLOps, and AWS machine learning services.
---

# AWS SageMaker Skill

Comprehensive assistance with Amazon SageMaker development, covering the complete ML lifecycle from data preparation to model deployment and monitoring.

## When to Use This Skill

This skill should be triggered when:

**Model Training & Development**
- Training ML models on SageMaker infrastructure
- Using SageMaker training jobs or HyperPod clusters
- Implementing distributed training workflows
- Building custom training containers

**Model Deployment & Inference**
- Deploying models to real-time endpoints
- Setting up serverless inference endpoints
- Configuring batch transform jobs
- Managing endpoint auto-scaling
- Deploying models with Inference Recommender

**Data Preparation**
- Working with SageMaker Data Wrangler
- Preparing datasets for training
- Implementing data transformation pipelines

**Model Management & MLOps**
- Registering models in Model Registry
- Managing model versions and lifecycle
- Setting up model monitoring with Model Monitor
- Tracking model quality, bias, and drift
- Implementing CI/CD for ML workflows

**SageMaker Studio & Environments**
- Setting up SageMaker domains and user profiles
- Configuring Studio environments
- Working with JumpStart foundation models
- Using Canvas for low-code ML

**Edge Deployment**
- Deploying models to edge devices with Edge Manager
- Optimizing models with SageMaker Neo

## Key Concepts

**SageMaker Domain**: A centralized environment for ML workflows, providing authentication, authorization, and resource management for teams.

**Model Registry**: Versioned catalog of ML models with metadata, approval workflows, and deployment tracking.

**Endpoints**: Deployed models that provide real-time or serverless inference capabilities.

**Model Monitor**: Automated monitoring for data quality, model quality, bias drift, and feature attribution drift in production.

**Training Jobs**: Managed infrastructure for training ML models at scale with automatic resource provisioning.

**Model Packages**: Versioned entities in Model Registry containing model artifacts, inference specifications, and metadata.

## Quick Reference

### Example 1: List Recent Monitoring Executions

Monitor your model's performance by checking execution history:

```python
# List the latest monitoring executions
mon_executions = my_default_monitor.list_executions()

print("Waiting for the 1st execution to happen...")
while len(mon_executions) == 0:
    print("Waiting for the 1st execution to happen...")
    time.sleep(60)
    mon_executions = my_default_monitor.list_executions()
```

### Example 2: AWS CLI Configuration for SageMaker

Set up AWS CLI for SageMaker operations:

```bash
# Configure AWS credentials
aws configure

# This will prompt for:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region name
# - Default output format
```

### Example 3: Data Wrangler URLs for Firewall Configuration

If using a firewall, whitelist these Data Wrangler URLs:

```
https://ui.prod-1.data-wrangler.sagemaker.aws/
https://ui.prod-2.data-wrangler.sagemaker.aws/
https://ui.prod-3.data-wrangler.sagemaker.aws/
https://ui.prod-4.data-wrangler.sagemaker.aws/
```

### Example 4: Create Model with ModelBuilder

Deploy models with fine-grained control using the SageMaker Python SDK:

```python
from sagemaker.model_builder import ModelBuilder

# Initialize ModelBuilder with custom configuration
model = ModelBuilder(
    model_data="s3://my-bucket/model.tar.gz",
    role=execution_role,
    instance_type="ml.m5.xlarge",
    framework="pytorch",
    framework_version="1.12"
)

# Deploy to endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.xlarge"
)
```

### Example 5: Model Registry ARN Pattern

Model packages in Registry follow this ARN structure:

```
arn:aws:sagemaker:region:account:model-package-group/version
```

Example:
```
arn:aws:sagemaker:us-east-1:123456789012:model-package-group/my-model-group/version/1
```

### Example 6: AWS Marketplace Subscription Management

Grant permissions for Partner AI Apps:

```python
# Attach the managed policy for AWS Marketplace
policy_arn = "AWSMarketplaceManageSubscriptions"

# This policy allows administrators to:
# - Subscribe to Partner AI Apps
# - Manage marketplace subscriptions
# - Purchase apps from AWS Marketplace
```

### Example 7: Serverless Endpoint Monitoring Metrics

Key CloudWatch metrics for serverless endpoints:

```python
# Monitor for cold starts
metric_name = "OverheadLatency"

# Handle validation errors
error_type = "ValidationError"

# These metrics help you understand:
# - Cold start frequency and duration
# - Request validation failures
# - Overall endpoint performance
```

### Example 8: Model Package Resource Groups

Work with model metadata using resource groups:

```python
# Resource groups help organize and manage models
resource_group_tag = "sagemaker"

# Model artifacts should include this tag for:
# - Easier discovery in Model Registry
# - Integration with IAM policies
# - Automated resource management
```

### Example 9: Processing Job Environment Variables

Configure processing jobs with custom environment:

```python
from sagemaker.processing import ProcessingInput, ProcessingOutput

processing_job_config = {
    "Environment": {
        "MY_VARIABLE": "value",
        "DATA_PATH": "/opt/ml/processing/input"
    },
    "ProcessingInputs": [
        ProcessingInput(
            source="s3://my-bucket/data/",
            destination="/opt/ml/processing/input"
        )
    ]
}

# Environment variables follow pattern: [a-zA-Z_][a-zA-Z0-9_]*
```

### Example 10: Model Monitoring Violations Report

Check model quality violations:

```python
# List generated reports
reports = monitor.list_reports()

# Check violations report for issues
violations = monitor.list_violations()

# Violations are generated when:
# - Data quality degrades below threshold
# - Model predictions drift from baseline
# - Bias metrics exceed acceptable limits
```

## Reference Files

This skill includes comprehensive documentation organized by topic:

### endpoints.md (2 pages)
- **Edge Manager**: Deploy and manage ML models on edge devices (cameras, IoT devices, mobile)
- **Canvas Model Deployment**: Deploy models from Canvas to SageMaker endpoints
- **Deployment Permissions**: IAM roles and policies for model deployment
- **Best for**: Understanding edge deployment strategies and Canvas integration

### getting_started.md (22 pages)
- **Partner AI Apps Setup**: Configure third-party AI applications in SageMaker
- **Data Wrangler Setup**: Prerequisites and access instructions
- **Domain Configuration**: Set up SageMaker domains with IAM Identity Center
- **AWS Marketplace Integration**: Subscribe to and manage marketplace apps
- **Best for**: Initial setup, onboarding new users, understanding prerequisites

### inference.md (12 pages)
- **Inference Recommender**: Automated load testing and instance selection
- **Real-time Endpoints**: Deploy models for low-latency predictions
- **Serverless Inference**: Auto-scaling, on-demand inference without infrastructure management
- **Model Dashboard**: Centralized monitoring and governance for deployed models
- **Model Quality Monitoring**: Track prediction accuracy and model degradation
- **CloudWatch Integration**: Metrics, logs, and alarms for production models
- **Best for**: Production deployment strategies, performance optimization, monitoring setup

### models.md (9 pages)
- **Model Registry**: Version control and lifecycle management for ML models
- **Model Packages**: Create and manage versioned model artifacts
- **IAM Policies**: Managed policies for Model Registry access (AmazonSageMakerModelRegistryFullAccess)
- **Model Comparison**: Evaluate and compare model versions
- **Auto-scaling**: Configure automatic scaling for endpoints
- **Deployment Tracking**: Monitor deployment history and lineage
- **Best for**: MLOps workflows, model governance, version management

### studio.md
- **Studio Environment**: Configure and use SageMaker Studio Classic
- **JumpStart**: Pre-trained models and solution templates
- **Custom Models**: Build, train, and evaluate custom ML models
- **Best for**: Interactive development, experimentation, JumpStart usage

### training.md
- **Training Jobs**: Configure and run distributed training
- **HyperPod**: Large-scale training infrastructure
- **Training Recipes**: Pre-configured training workflows
- **Training Plans**: Reserved compute for predictable costs
- **Best for**: Model training workflows, distributed training, cost optimization

### other.md
- **Additional Features**: Miscellaneous SageMaker capabilities
- **Partner Integrations**: Third-party tool integrations
- **Advanced Configurations**: Special use cases and configurations

## Working with This Skill

### For Beginners

**Start Here:**
1. Review `getting_started.md` for prerequisites and domain setup
2. Learn about SageMaker domains and authentication methods
3. Explore `studio.md` for JumpStart pre-trained models
4. Try Canvas in `endpoints.md` for low-code ML

**First Tasks:**
- Set up a SageMaker domain with IAM Identity Center
- Deploy a JumpStart model for quick experimentation
- Use Canvas to build a simple predictive model

### For Intermediate Users

**Focus Areas:**
1. `training.md` - Create custom training jobs
2. `inference.md` - Deploy models with Inference Recommender
3. `models.md` - Set up Model Registry for version control
4. Configure basic Model Monitor for production models

**Common Workflows:**
- Train a custom model with your dataset
- Register trained models in Model Registry
- Deploy to real-time or serverless endpoints
- Set up basic monitoring with CloudWatch

### For Advanced Users

**Advanced Topics:**
1. **MLOps Pipelines**: Automate training and deployment workflows
2. **Model Governance**: Implement approval workflows in Model Registry
3. **Advanced Monitoring**: Configure drift detection and bias monitoring
4. **Edge Deployment**: Deploy models to edge devices with Edge Manager
5. **Cost Optimization**: Use Training Plans and Serverless Inference with Provisioned Concurrency

**Best Practices:**
- Use Model Registry approval workflows for production deployments
- Implement comprehensive monitoring (data quality, model quality, bias, drift)
- Configure auto-scaling for variable traffic patterns
- Use Inference Recommender for optimal instance selection
- Implement cross-account Model Registry for team collaboration

## Common Patterns

### Pattern 1: Domain ID Format
When working with SageMaker domains, IDs follow this pattern:
```
d-(-*[a-z0-9]){1,61}
```
Example: `d-abc123def456`

### Pattern 2: User Profile Name Format
User profiles use this naming convention:
```
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```
Example: `data-scientist-john-doe`

### Pattern 3: Model Package ARN Format
Full ARN structure for model packages:
```
arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:user-profile/.*
```

### Pattern 4: IAM Role Pattern for SageMaker
SageMaker execution roles follow this format:
```
arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+
```

### Pattern 5: Environment Variable Naming
Processing job environment variables must match:
```
Key: [a-zA-Z_][a-zA-Z0-9_]*
Value: [\S\s]*
```

## Integration Examples

### Canvas Model Deployment Flow
```
1. Build model in Canvas (low-code)
2. Deploy model to endpoint with one click
3. Model hosted on SageMaker infrastructure
4. Invoke endpoint for real-time predictions
5. Integrate with applications via API
```

### Model Registry Workflow
```
1. Train model (SageMaker training job or external)
2. Register model version in Model Registry
3. Evaluate model performance
4. Update approval status (Approved/Rejected)
5. Deploy approved models to production
6. Track deployment history and lineage
```

### Model Monitoring Pipeline
```
1. Deploy model to endpoint
2. Configure Model Monitor baseline
3. Schedule monitoring jobs (hourly/daily)
4. Monitor metrics in Model Dashboard
5. Set CloudWatch alarms for violations
6. Receive alerts when quality degrades
7. Investigate and retrain model if needed
```

## Resources

### Official Documentation
- AWS SageMaker Developer Guide
- SageMaker Python SDK Documentation
- AWS SDK (Boto3) SageMaker Reference

### Key AWS Services Integration
- **Amazon S3**: Model artifacts and training data storage
- **IAM**: Authentication and authorization
- **CloudWatch**: Monitoring, logging, and alarms
- **ECR**: Custom container images
- **AWS Marketplace**: Partner AI Apps and algorithms
- **AWS KMS**: Encryption for model artifacts and data

### Cost Optimization Tips
- Use Serverless Inference for sporadic traffic
- Configure auto-scaling for variable workloads
- Use Spot Instances for training jobs (cost savings up to 90%)
- Implement Training Plans for predictable training workloads
- Use Inference Recommender to select cost-effective instances
- Monitor with Model Dashboard to identify underutilized endpoints

## Troubleshooting Common Issues

### Cold Starts (Serverless Inference)
- **Issue**: High latency on first request
- **Solution**: Use Provisioned Concurrency for predictable performance
- **Monitor**: `OverheadLatency` CloudWatch metric

### Model Monitoring Violations
- **Issue**: `CompletedWithViolations` status
- **Solution**: Check violations report, investigate data drift
- **Prevention**: Set appropriate baseline constraints

### Endpoint Deployment Failures
- **Issue**: `FailureReason` and `ExitMessage` in logs
- **Solution**: Verify IAM role permissions, check model artifacts
- **Debug**: Review CloudWatch Logs for container errors

### Permission Errors
- **Issue**: Access denied when deploying or monitoring
- **Solution**: Attach `AmazonSageMakerFullAccess` or create custom policy
- **Model Registry**: Use `AmazonSageMakerModelRegistryFullAccess`

## Notes

- This skill was automatically generated from official AWS SageMaker documentation
- Reference files are organized by major feature area for easy navigation
- Code examples include proper language annotations for syntax highlighting
- Quick reference patterns are extracted from production use cases
- All ARN formats and naming patterns follow AWS standards

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. Review new features and API changes
3. Update code examples to reflect current best practices
4. The skill will be rebuilt with the latest information

## Version Information

- **Source**: AWS SageMaker Official Documentation
- **Coverage**: Endpoints, Models, Inference, Training, Studio, Getting Started
- **Last Updated**: Based on latest documentation scrape
- **Regions**: Generally available in 21+ AWS regions (varies by feature)
