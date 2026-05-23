---
name: aws-cloudformation-bedrock
description: Provides AWS CloudFormation patterns for Amazon Bedrock resources including agents, knowledge bases, data sources, guardrails, prompts, flows, and inference profiles. Use when creating Bedrock agents with action groups, implementing RAG with knowledge bases, configuring vector stores, setting up content moderation guardrails, managing prompts, orchestrating workflows with flows, and configuring inference profiles for model optimization.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Amazon Bedrock

## Overview

Creates production-ready AI infrastructure using AWS CloudFormation templates for Amazon Bedrock. Covers Bedrock agents, knowledge bases for RAG implementations, data source connectors, guardrails for content moderation, prompt management, workflow orchestration with flows, and inference profiles for optimized model access.

## When to Use

- Creating Bedrock agents with action groups
- Implementing RAG with knowledge bases
- Configuring S3 or web crawl data sources
- Setting up content moderation guardrails
- Managing prompt templates
- Orchestrating AI workflows with Bedrock Flows
- Configuring inference profiles for multi-model access
- Organizing templates with Parameters and cross-stack references

## Instructions

### 1. Define Parameters

```yaml
Parameters:
  FoundationModel:
    Type: String
    Default: anthropic.claude-3-sonnet-20240229-v1:0
    AllowedValues:
      - anthropic.claude-3-sonnet-20240229-v1:0
      - anthropic.claude-3-haiku-20240307-v1:0
      - amazon.titan-text-express-v1
    Description: Foundation model for agent
```

### 2. Create Agent Role

```yaml
Resources:
  AgentRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: bedrock.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: BedrockPermissions
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - bedrock:InvokeModel
                Resource: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:foundation-model/${FoundationModel}"
```

### 3. Create Agent

```yaml
  BedrockAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Sub "${AWS::StackName}-agent"
      AgentResourceRoleArn: !GetAtt AgentRole.Arn
      FoundationModelArn: !Sub "arn:aws:bedrock:${AWS::Region}::foundation-model/${FoundationModel}"
      AutoPrepare: true
      Instruction: |
        You are a helpful assistant. Use the knowledge base to answer questions.
```

### 4. Create Knowledge Base

```yaml
  KnowledgeBaseRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: bedrock.amazonaws.com
            Action: sts:AssumeRole

  KnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      Name: !Sub "${AWS::StackName}-kb"
      RoleArn: !GetAtt KnowledgeBaseRole.Arn
      KnowledgeBaseConfiguration:
        Type: VECTOR
        VectorKnowledgeBaseConfiguration:
          EmbeddingModelArn: !Sub "arn:aws:bedrock:${AWS::Region}::embedding-model/amazon.titan-embed-text-v1"
```

### 5. Create Data Source

```yaml
  DataBucket:
    Type: AWS::S3::Bucket

  S3DataSource:
    Type: AWS::Bedrock::DataSource
    Properties:
      KnowledgeBaseId: !Ref KnowledgeBase
      Name: s3-data-source
      Type: S3
      DataSourceConfiguration:
        S3Configuration:
          BucketArn: !GetAtt DataBucket.Arn
          InclusionPrefixes:
            - documents/
```

### 6. Add Guardrail

```yaml
  Guardrail:
    Type: AWS::Bedrock::Guardrail
    Properties:
      Name: !Sub "${AWS::StackName}-guardrail"
      BlockedInputMessaging: "I cannot help with that request."
      ContentPolicyConfig:
        filtersConfig:
          - type: PROFANITY
          - type: MISCONDUCT
```

### 7. Create Action Group

```yaml
  ActionLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.12
      Handler: index.handler
      Role: !GetAtt ActionLambdaRole.Arn
      Code:
        ZipFile: |
          def handler(event, context):
              return {"statusCode": 200, "body": "{\"result\": \"success\"}"}

  ActionGroup:
    Type: AWS::Bedrock::AgentActionGroup
    Properties:
      ActionGroupName: api-operations
      ActionGroupState: ENABLED
      AgentId: !GetAtt BedrockAgent.AgentId
      ActionGroupExecutor:
        Lambda: !Ref ActionLambdaFunction
      FunctionSchema:
        functionConfigurations:
          - function: |
              { "name": "get_inventory", "description": "Get current inventory status", "parameters": { "type": "object", "properties": { "sku": { "type": "string" } }, "required": [] } }
```

### 8. Validate Before Deploy

Always validate the template before deployment:

```bash
aws cloudformation validate-template --template-body file://bedrock-template.yaml
```

### 9. Verify After Deploy

```bash
# Check agent status
aws bedrock-agent get-agent --agent-id $(aws cloudformation describe-stacks --stack-name STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`AgentId`].OutputValue' --output text)

# Check knowledge base sync status
aws bedrock-agent list-knowledge-bases --agent-id AGENT_ID

# Test guardrail
aws bedrock-runtime apply_guardrail --guardrail-identifier GUARDRAIL_ID --source SOURCE
```

## Examples

### Minimal RAG Agent Template

Complete working template for a RAG-enabled agent:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "Bedrock RAG Agent with Knowledge Base"

Parameters:
  FoundationModel:
    Type: String
    Default: anthropic.claude-3-sonnet-20240229-v1:0

Resources:
  # IAM Role for Agent
  AgentRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-agent-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: bedrock.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: InvokeModel
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action: bedrock:InvokeModel
                Resource: "*"

  # IAM Role for Knowledge Base
  KnowledgeBaseRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-kb-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: bedrock.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action: s3:GetObject
                Resource: !Sub "${DataBucket.Arn}/*"

  # S3 Bucket for Documents
  DataBucket:
    Type: AWS::S3::Bucket

  # Knowledge Base
  KnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      Name: !Sub "${AWS::StackName}-kb"
      RoleArn: !GetAtt KnowledgeBaseRole.Arn
      KnowledgeBaseConfiguration:
        Type: VECTOR
        VectorKnowledgeBaseConfiguration:
          EmbeddingModelArn: !Sub "arn:aws:bedrock:${AWS::Region}::embedding-model/amazon.titan-embed-text-v1"

  # Data Source
  DataSource:
    Type: AWS::Bedrock::DataSource
    Properties:
      KnowledgeBaseId: !Ref KnowledgeBase
      Name: !Sub "${AWS::StackName}-ds"
      Type: S3
      DataSourceConfiguration:
        S3Configuration:
          BucketArn: !GetAtt DataBucket.Arn

  # Bedrock Agent
  BedrockAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Sub "${AWS::StackName}-agent"
      AgentResourceRoleArn: !GetAtt AgentRole.Arn
      FoundationModelArn: !Sub "arn:aws:bedrock:${AWS::Region}::foundation-model/${FoundationModel}"
      AutoPrepare: true
      Instruction: |
        You are a helpful assistant. Use the knowledge base to answer user questions accurately.

Outputs:
  AgentId:
    Description: Bedrock Agent ID
    Value: !GetAtt BedrockAgent.AgentId
  KnowledgeBaseId:
    Description: Knowledge Base ID
    Value: !Ref KnowledgeBase
```

### Guardrail with Content Filtering

```yaml
Resources:
  Guardrail:
    Type: AWS::Bedrock::Guardrail
    Properties:
      Name: !Sub "${AWS::StackName}-guardrail"
      blockedInputMessaging: "Content blocked by safety filters."
      blockedOutputMessaging: "Response filtered for safety."
      contentPolicyConfig:
        filtersConfig:
          - type: PROFANITY
            inputStrength: HIGH
            outputStrength: HIGH
          - type: MISCONDUCT
            inputStrength: HIGH
            outputStrength: HIGH
      sensitiveInformationPolicyConfig:
        piiEntitiesConfig:
          - type: EMAIL
            action: ANONYMIZE
          - type: SSN
            action: BLOCK
```

## Best Practices

### Security
- Use least privilege IAM policies for agent and knowledge base roles
- Restrict web crawl data sources to trusted internal domains
- Encrypt sensitive data in knowledge bases
- Parameterize all TemplateURL values for nested stacks

### Cost Optimization
- Select appropriate model size for task complexity
- Configure retrieval filtering to reduce token usage
- Set chunk size limits to control storage costs
- Monitor usage with CloudWatch dashboards

### Performance
- Optimize chunk size for embedding quality
- Use provisioned throughput for high-traffic vector stores
- Configure appropriate knowledge base sync intervals
- Implement caching for frequently accessed content

### Validation
- Always run `aws cloudformation validate-template` before deploy
- Verify agent status after stack creation completes
- Test guardrails with sample inputs
- Monitor knowledge base sync status in CloudWatch

## Constraints and Warnings

For detailed limits, see [constraints.md](references/constraints.md):

- **Regional limits**: Not all models available in all regions
- **Agent initialization**: AutoPrepare may take several minutes
- **Knowledge base sync**: S3 sync is near-instant; web crawl takes longer
- **Web crawl security**: Always restrict to trusted domains to prevent prompt injection
- **Token limits**: Configure MaxTokens parameter for your use case
- **Quota management**: Request quota increases via AWS Support if needed

### Security

- Restrict web crawl data sources to trusted internal domains only
- Validate content before ingesting into knowledge bases
- Use parameterized TemplateURL values for nested stacks
- Implement guardrails for content moderation
- Apply least privilege IAM policies to agent roles
- Encrypt sensitive data in knowledge bases
- Monitor for prompt injection in web-crawled content

### Cost Optimization

- Use appropriate model selection for task complexity
- Implement knowledge base retrieval filtering
- Set chunk size limits to control token usage
- Monitor token consumption with CloudWatch
- Use auto-prepare agents strategically
- Implement batch processing for non-real-time workloads
- Use knowledge base filtering to reduce costs

### Performance

- Optimize chunk size for embedding quality vs. cost
- Use vector store optimization (OpenSearch, Pinecone)
- Implement caching for frequently accessed knowledge base content
- Configure appropriate knowledge base sync intervals
- Use provisioned throughput for vector databases
- Monitor agent initialization and cold start times
- Implement graceful degradation for rate limiting

### Data Management

- Use appropriate inclusion/exclusion filters for data sources
- Implement document validation before indexing
- Use versioning for knowledge base updates
- Configure appropriate sync intervals for data sources
- Implement content deduplication in knowledge bases
- Use metadata filtering for improved retrieval accuracy
- Monitor knowledge base size and document limits

## References

- **[constraints.md](references/constraints.md)** - Resource limits, regional constraints, operational limits, and cost considerations
- **[reference.md](references/reference.md)** - API reference and resource properties
- **[examples.md](references/examples.md)** - Additional usage examples

## Related Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [CloudFormation Bedrock Resource Types](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html)
- [Bedrock Agents User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
