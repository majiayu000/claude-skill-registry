---
name: aws-cloudformation-bedrock
description: AWS CloudFormation patterns for Amazon Bedrock resources including agents, knowledge bases, data sources, guardrails, prompts, flows, and inference profiles. Use when creating Bedrock agents with action groups, implementing RAG with knowledge bases, configuring vector stores, setting up content moderation guardrails, managing prompts, orchestrating workflows with flows, and configuring inference profiles for model optimization.
category: aws
tags: [aws, cloudformation, bedrock, ai, ml, agents, knowledge-base, rag, guardrail, inference, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Amazon Bedrock

## Overview

Create production-ready AI infrastructure using AWS CloudFormation templates for Amazon Bedrock. This skill covers Bedrock agents, knowledge bases for RAG implementations, data source connectors, guardrails for content moderation, prompt management, workflow orchestration with flows, and inference profiles for optimized model access.

## When to Use

Use this skill when:
- Creating Bedrock agents with action groups and function definitions
- Implementing Retrieval-Augmented Generation (RAG) with knowledge bases
- Configuring data sources (S3, web crawl, custom connectors)
- Setting up vector store configurations (OpenSearch, Pinecone, pgvector)
- Creating content moderation guardrails
- Managing prompt templates and versions
- Orchestrating AI workflows with Bedrock Flows
- Configuring inference profiles for multi-model access
- Setting up application inference profiles for optimized model routing
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import

## CloudFormation Template Structure

### Base Template with Standard Format

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Amazon Bedrock agent with knowledge base for RAG

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Agent Configuration
        Parameters:
          - AgentName
          - AgentDescription
          - FoundationModel
      - Label:
          default: Knowledge Base Settings
        Parameters:
          - KnowledgeBaseName
          - VectorStoreType
          - EmbeddingModel
      - Label:
          default: Deployment Settings
        Parameters:
          - Environment
          - DeployStage

Parameters:
  AgentName:
    Type: String
    Default: my-bedrock-agent
    Description: Name of the Bedrock agent

  AgentDescription:
    Type: String
    Default: Agent for customer support automation
    Description: Description of the agent's purpose

  FoundationModel:
    Type: String
    Default: anthropic.claude-v2:1
    Description: Foundation model for the agent
    AllowedValues:
      - anthropic.claude-v2:1
      - anthropic.claude-v3:5
      - anthropic.claude-sonnet-4-20250514
      - amazon.titan-text-express-v1
      - meta.llama3-70b-instruct-v1:0

  KnowledgeBaseName:
    Type: String
    Default: my-knowledge-base
    Description: Name of the knowledge base

  VectorStoreType:
    Type: String
    Default: OPENSEARCH_SERVERLESS
    Description: Vector store type for knowledge base
    AllowedValues:
      - OPENSEARCH_SERVERLESS
      - PINECONE
      - PGVECTOR
      - REDIS

  EmbeddingModel:
    Type: String
    Default: amazon.titan-embed-text-v1
    Description: Embedding model for vectorization
    AllowedValues:
      - amazon.titan-embed-text-v1
      - amazon.titan-embed-text-v2:0
      - cohere.embed-multilingual-v3:0

  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Mappings:
  EnvironmentConfig:
    dev:
      AgentVersion: DRAFT
      IndexCapacity: 1
      InferenceUnit: 1
    staging:
      AgentVersion: DRAFT
      IndexCapacity: 5
      InferenceUnit: 2
    production:
      AgentVersion: RELEASE
      IndexCapacity: 10
      InferenceUnit: 5

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  UseOpenSearch: !Equals [!Ref VectorStoreType, OPENSEARCH_SERVERLESS]

Transform:
  - AWS::Serverless-2016-10-31

Resources:
  # Bedrock Agent
  BedrockAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Ref AgentName
      Description: !Ref AgentDescription
      FoundationModel: !Ref FoundationModel
      IdleSessionTTLInSeconds: 1800
      AgentResourceRoleArn: !GetAtt AgentResourceRole.Arn
      AutoPrepare: true

  # Agent Resource Role
  AgentResourceRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-bedrock-agent-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: bedrock.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-bedrock-agent-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - bedrock:InvokeModel
                  - bedrock:InvokeModelWithResponseStream
                Resource: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:foundation-model/${FoundationModel}"

Outputs:
  AgentId:
    Description: ID of the Bedrock agent
    Value: !GetAtt BedrockAgent.AgentId
    Export:
      Name: !Sub "${AWS::StackName}-AgentId"

  AgentAliasId:
    Description: Alias ID of the Bedrock agent
    Value: !GetAtt BedrockAgent.LatestAgentAliasId
    Export:
      Name: !Sub "${AWS::StackName}-AgentAliasId"

  AgentArn:
    Description: ARN of the Bedrock agent
    Value: !GetAtt BedrockAgent.AgentArn
    Export:
      Name: !Sub "${AWS::StackName}-AgentArn"
```

## Best Practices for Parameters

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  AgentId:
    Type: AWS::Bedrock::Agent::Id
    Description: Existing Bedrock agent ID

  KnowledgeBaseId:
    Type: AWS::Bedrock::KnowledgeBase::Id
    Description: Existing knowledge base ID

  GuardrailId:
    Type: AWS::Bedrock::Guardrail::Id
    Description: Existing guardrail ID

  FoundationModelArn:
    Type: AWS::Bedrock::FoundationModel::Arn
    Description: ARN of foundation model

  FoundationModelIdentifier:
    Type: AWS::Bedrock::FoundationModel::Identifier
    Description: Identifier of foundation model

  S3BucketArn:
    Type: AWS::S3::Bucket::Arn
    Description: S3 bucket ARN for data sources

  IAMRoleArn:
    Type: AWS::IAM::Role::Arn
    Description: IAM role for Bedrock operations

  KMSKeyArn:
    Type: AWS::KMS::Key::Arn
    Description: KMS key for encryption
```

### Parameter Constraints

```yaml
Parameters:
  AgentName:
    Type: String
    Default: my-agent
    Description: Bedrock agent name
    ConstraintDescription: Must be 1-100 characters, alphanumeric and underscores
    MinLength: 1
    MaxLength: 100
    AllowedPattern: "[a-zA-Z0-9_]+"

  KnowledgeBaseName:
    Type: String
    Default: my-kb
    Description: Knowledge base name
    ConstraintDescription: Must be 1-100 characters
    MinLength: 1
    MaxLength: 100

  MaxTokens:
    Type: Number
    Default: 4096
    Description: Maximum tokens for model response
    MinValue: 1
    MaxValue: 100000
    ConstraintDescription: Must be between 1 and 100000

  Temperature:
    Type: Number
    Default: 0.7
    Description: Temperature for model generation
    MinValue: 0
    MaxValue: 1
    ConstraintDescription: Must be between 0 and 1
```

### SSM Parameter References for Model Identifiers

```yaml
Parameters:
  ClaudeModelIdentifier:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /bedrock/models/claude-identifier
    Description: Claude model identifier from SSM

  EmbeddingModelIdentifier:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /bedrock/models/embedding-identifier
    Description: Embedding model identifier from SSM
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Bedrock Infrastructure Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Bedrock infrastructure stack with agents and knowledge bases

Resources:
  # Bedrock Agent
  CustomerSupportAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Sub "${AWS::StackName}-support-agent"
      Description: Agent for customer support
      FoundationModel: anthropic.claude-v3:5
      AgentResourceRoleArn: !GetAtt AgentRole.Arn
      AutoPrepare: true

  # Knowledge Base
  SupportKnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      KnowledgeBaseName: !Sub "${AWS::StackName}-support-kb"
      Description: Knowledge base for customer support
      EmbeddingModelArn: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:foundation-model/amazon.titan-embed-text-v1"
      VectorKnowledgeBaseConfiguration:
        VectorStoreConfiguration:
          OpensearchServerlessConfiguration:
            CollectionArn: !Ref OpenSearchCollectionArn
            VectorIndexName: knowledge-base-index
            FieldMapping:
              VectorField: vector
              TextField: text
              MetadataField: metadata
      RoleArn: !GetAtt KnowledgeBaseRole.Arn

Outputs:
  AgentId:
    Description: ID of the Bedrock agent
    Value: !GetAtt CustomerSupportAgent.AgentId
    Export:
      Name: !Sub "${AWS::StackName}-AgentId"

  AgentAliasId:
    Description: Alias ID of the Bedrock agent
    Value: !GetAtt CustomerSupportAgent.LatestAgentAliasId
    Export:
      Name: !Sub "${AWS::StackName}-AgentAliasId"

  AgentArn:
    Description: ARN of the Bedrock agent
    Value: !GetAtt CustomerSupportAgent.AgentArn
    Export:
      Name: !Sub "${AWS::StackName}-AgentArn"

  KnowledgeBaseId:
    Description: ID of the knowledge base
    Value: !GetAtt SupportKnowledgeBase.KnowledgeBaseId
    Export:
      Name: !Sub "${AWS::StackName}-KnowledgeBaseId"

  KnowledgeBaseArn:
    Description: ARN of the knowledge base
    Value: !GetAtt SupportKnowledgeBase.KnowledgeBaseArn
    Export:
      Name: !Sub "${AWS::StackName}-KnowledgeBaseArn"
```

```yaml
# Stack B - Application Stack (imports from Stack A)
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack using Bedrock agent

Parameters:
  BedrockStackName:
    Type: String
    Default: bedrock-infrastructure
    Description: Name of the Bedrock infrastructure stack

Resources:
  # Lambda function that invokes Bedrock agent
  AgentInvokerFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-agent-invoker"
      Runtime: python3.11
      Handler: handler.invoke_agent
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/agent-invoker.zip
      Environment:
        Variables:
          AGENT_ID: !ImportValue
            !Sub "${BedrockStackName}-AgentId"
          AGENT_ALIAS_ID: !ImportValue
            !Sub "${BedrockStackName}-AgentAliasId"
      Role: !GetAtt LambdaExecutionRole.Arn

  # Lambda Execution Role with Bedrock permissions
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lambda-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: BedrockAgentInvoke
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - bedrock:InvokeAgent
                Resource: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:agent/*"
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested Bedrock stacks

Resources:
  # Nested stack for agents
  AgentsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/bedrock-agents.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        AgentName: !Ref AgentName
        FoundationModel: !Ref FoundationModel

  # Nested stack for knowledge bases
  KnowledgeBaseStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/bedrock-knowledge-base.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        KnowledgeBaseName: !Ref KnowledgeBaseName
        VectorStoreType: !Ref VectorStoreType

  # Nested stack for guardrails
  GuardrailsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/bedrock-guardrails.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        GuardrailName: !Ref GuardrailName
```

## Bedrock Agents with Action Groups

### Agent with Lambda Action Group

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Bedrock agent with Lambda action group for API operations

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Resources:
  # Agent Resource Role
  AgentResourceRole:
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
        - PolicyName: BedrockAgentPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - bedrock:InvokeModel
                  - bedrock:InvokeModelWithResponseStream
                Resource: "*"
              - Effect: Allow
                Action:
                  - lambda:InvokeFunction
                  - lambda:InvokeAsync
                Resource: !GetAtt ActionGroupFunction.Arn

  # Lambda function for action group
  ActionGroupFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-action-group"
      Runtime: python3.11
      Handler: handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/action-group.zip
      Role: !GetAtt LambdaExecutionRole.Arn

  # Lambda Execution Role
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lambda-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  # Bedrock Agent
  ApiAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Sub "${AWS::StackName}-api-agent"
      Description: Agent for API operations
      FoundationModel: anthropic.claude-v3:5
      AgentResourceRoleArn: !GetAtt AgentResourceRole.Arn
      AutoPrepare: true

  # Action Group with Lambda function
  ApiActionGroup:
    Type: AWS::Bedrock::AgentActionGroup
    Properties:
      AgentId: !Ref ApiAgent
      AgentVersion: DRAFT
      ActionGroupName: ApiActionGroup
      Description: Action group for API operations
      ActionGroupExecutor:
        Lambda: !Ref ActionGroupFunction
      ApiSchema:
        S3:
          S3BucketName: !Ref ApiSchemaBucket
          S3ObjectKey: api-schema.json
      SkipModelsInExecution: false

  # API Schema in S3
  ApiSchemaBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::StackName}-api-schema-${AWS::AccountId}-${AWS::Region}"
```

### Agent with Knowledge Base Integration

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Bedrock agent with knowledge base for RAG

Parameters:
  Environment:
    Type: String
    Default: dev

Resources:
  # Agent Resource Role
  AgentResourceRole:
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
        - PolicyName: AgentPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - bedrock:InvokeModel
                  - bedrock:InvokeModelWithResponseStream
                Resource: "*"
              - Effect: Allow
                Action:
                  - bedrock:Retrieve
                  - bedrock:RetrieveAndGenerate
                Resource: !GetAtt KnowledgeBase.KnowledgeBaseArn

  # OpenSearch Serverless Collection
  OpenSearchCollection:
    Type: AWS::OpenSearchServerless::Collection
    Properties:
      Name: !Sub "${AWS::StackName}-kb-collection"
      Type: SEARCH

  # OpenSearch Serverless Access Policy
  AccessPolicy:
    Type: AWS::OpenSearchServerless::AccessPolicy
    Properties:
      Name: !Sub "${AWS::StackName}-access-policy"
      Policy: !Sub |
        [
          {
            "Rules": [
              {
                "Resource": ["collection/${OpenSearchCollection.id}"],
                "Permission": ["aoss:*"]
              },
              {
                "Resource": ["index/collection/${OpenSearchCollection.id}/*"],
                "Permission": ["aoss:*"]
              }
            ],
            "Principal": ["${AgentResourceRole.Arn}"]
          }
        ]
      Type: data

  # Knowledge Base
  KnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      KnowledgeBaseName: !Sub "${AWS::StackName}-kb"
      Description: Knowledge base for document retrieval
      EmbeddingModelArn: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:foundation-model/amazon.titan-embed-text-v1"
      VectorKnowledgeBaseConfiguration:
        VectorStoreConfiguration:
          OpensearchServerlessConfiguration:
            CollectionArn: !GetAtt OpenSearchCollection.Arn
            VectorIndexName: kb-index
            FieldMapping:
              VectorField: vector
              TextField: text
              MetadataField: metadata
      RoleArn: !GetAtt AgentResourceRole.Arn

  # Bedrock Agent with knowledge base
  RAGAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Sub "${AWS::StackName}-rag-agent"
      Description: Agent with knowledge base for RAG
      FoundationModel: anthropic.claude-v3:5
      AgentResourceRoleArn: !GetAtt AgentResourceRole.Arn
      AutoPrepare: true
      KnowledgeBases:
        - KnowledgeBaseId: !Ref KnowledgeBase
          Description: Main knowledge base for document retrieval

  # Data Source for Knowledge Base
  KnowledgeBaseDataSource:
    Type: AWS::Bedrock::DataSource
    Properties:
      KnowledgeBaseId: !Ref KnowledgeBase
      DataSourceName: !Sub "${AWS::StackName}-datasource"
      Description: S3 data source for documents
      DataSourceConfiguration:
        S3Configuration:
          BucketArn: !Ref DocumentBucket
          InclusionPrefixes:
            - documents/
            - pdfs/
      VectorIngestionConfiguration:
        ChunkingConfiguration:
          ChunkingStrategy: FIXED_SIZE
          FixedSizeChunking:
            MaxTokens: 512
            OverlapPercentage: 20

  # Document Bucket
  DocumentBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::StackName}-documents-${AWS::AccountId}-${AWS::Region}"
```

## Knowledge Bases and Vector Stores

### Knowledge Base with OpenSearch Serverless

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Knowledge base with OpenSearch Serverless vector store

Resources:
  # OpenSearch Serverless Collection
  VectorCollection:
    Type: AWS::OpenSearchServerless::Collection
    Properties:
      Name: !Sub "${AWS::StackName}-vector-collection"
      Type: SEARCH

  # Security Policy
  SecurityPolicy:
    Type: AWS::OpenSearchServerless::SecurityPolicy
    Properties:
      Name: !Sub "${AWS::StackName}-security-policy"
      Policy: !Sub |
        {
          "Rules": [
            {
              "Resource": ["collection/${VectorCollection.id}"],
              "ResourceType": "collection"
            }
          ],
          "Principal": ["*"]
        }
      Type: encryption

  # Access Policy
  AccessPolicy:
    Type: AWS::OpenSearchServerless::AccessPolicy
    Properties:
      Name: !Sub "${AWS::StackName}-access-policy"
      Policy: !Sub |
        [
          {
            "Rules": [
              {
                "Resource": ["collection/${VectorCollection.id}"],
                "Permission": ["aoss:*"]
              }
            ],
            "Principal": ["${KnowledgeBaseRole.Arn}"]
          }
        ]
      Type: data

  # Knowledge Base Role
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
        - PolicyName: KnowledgeBasePolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - aoss:APIAccessAll
                Resource: !GetAtt VectorCollection.Arn
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub "${DocumentBucket.Arn}/*"

  # Knowledge Base
  KnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      KnowledgeBaseName: !Sub "${AWS::StackName}-knowledge-base"
      Description: Vector knowledge base with OpenSearch
      EmbeddingModelArn: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:foundation-model/amazon.titan-embed-text-v1"
      VectorKnowledgeBaseConfiguration:
        VectorStoreConfiguration:
          OpensearchServerlessConfiguration:
            CollectionArn: !GetAtt VectorCollection.Arn
            VectorIndexName: knowledge-index
            FieldMapping:
              VectorField: vector
              TextField: text
              MetadataField: metadata
      RoleArn: !GetAtt KnowledgeBaseRole.Arn

  # Data Source
  DataSource:
    Type: AWS::Bedrock::DataSource
    Properties:
      KnowledgeBaseId: !Ref KnowledgeBase
      DataSourceName: !Sub "${AWS::StackName}-s3-datasource"
      DataSourceConfiguration:
        S3Configuration:
          BucketArn: !Ref DocumentBucket
      VectorIngestionConfiguration:
        ChunkingConfiguration:
          ChunkingStrategy: FIXED_SIZE
          FixedSizeChunking:
            MaxTokens: 1000
            OverlapPercentage: 10
```

### Knowledge Base with Pinecone

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Knowledge base with Pinecone vector store

Parameters:
  PineconeApiKey:
    Type: String
    Description: Pinecone API key (use Secrets Manager in production)
    NoEcho: true

Resources:
  # Knowledge Base Role
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
        - PolicyName: SecretsManagerAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Ref PineconeSecretArn

  # Pinecone Connection Configuration
  PineconeConnection:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}-pinecone-credentials"
      SecretString: !Sub '{"PINECONE_API_KEY":"${PineconeApiKey}"}'

  # Knowledge Base with Pinecone
  KnowledgeBase:
    Type: AWS::Bedrock::KnowledgeBase
    Properties:
      KnowledgeBaseName: !Sub "${AWS::StackName}-pinecone-kb"
      Description: Knowledge base with Pinecone vector store
      EmbeddingModelArn: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:foundation-model/amazon.titan-embed-text-v1"
      VectorKnowledgeBaseConfiguration:
        VectorStoreConfiguration:
          PineconeConfiguration:
            ConnectionString: !Ref PineconeConnectionString
            CredentialsSecretArn: !Ref PineconeConnection
            Namespace: !Ref PineconeNamespace
            FieldMapping:
              TextField: text
              MetadataField: metadata
      RoleArn: !GetAtt KnowledgeBaseRole.Arn

  # Data Source
  DataSource:
    Type: AWS::Bedrock::DataSource
    Properties:
      KnowledgeBaseId: !Ref KnowledgeBase
      DataSourceName: !Sub "${AWS::StackName}-pinecone-ds"
      DataSourceConfiguration:
        S3Configuration:
          BucketArn: !Ref DocumentBucket
```

## Guardrails for Content Moderation

### Guardrail with Multiple Filters

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Bedrock guardrail for content moderation

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Resources:
  # Guardrail
  ContentGuardrail:
    Type: AWS::Bedrock::Guardrail
    Properties:
      GuardrailName: !Sub "${AWS::StackName}-guardrail"
      Description: Content moderation guardrail
      # Topic Policy - Define denied topics
      TopicPolicy:
        Topics:
          - Name: FinancialAdvice
            Definition: Providing personalized financial investment advice
            Examples:
              - "What stocks should I buy?"
              - "Should I invest in crypto?"
            Type: DENIED
          - Name: MedicalAdvice
            Definition: Providing medical diagnosis or treatment recommendations
            Examples:
              - "What medication should I take?"
              - "Do I have COVID?"
            Type: DENIED
      # Sensitive Information Policy
      SensitiveInformationPolicy:
        PiiEntities:
          - Name: EMAIL
            Action: MASK
          - Name: PHONE_NUMBER
            Action: MASK
          - Name: SSN
            Action: BLOCK
          - Name: CREDIT_DEBIT_NUMBER
            Action: BLOCK
        Regexes:
          - Name: CustomPattern
            Pattern: "\\d{3}-\\d{2}-\\d{4}"
            Action: MASK
      # Word Policy - Custom blocked words
      WordPolicy:
        Words:
          - Text: "spam"
          - Text: "scam"
          - Text: "fraud"
        ManagedWordLists:
          - Type: PROFANITY
      # Content Policy
      ContentPolicy:
        Filters:
          - Type: PROFANITY
            InputStrength: LOW
            OutputStrength: LOW
          - Type: HATE
            InputStrength: MEDIUM
            OutputStrength: HIGH
          - Type: SEXUAL
            InputStrength: LOW
            OutputStrength: MEDIUM
          - Type: VIOLENCE
            InputStrength: MEDIUM
            OutputStrength: HIGH
      # Contextual Grounding Policy
      ContextualGroundingPolicy:
        Filters:
          - Type: GROUNDING
            Threshold: 0.7
          - Type: RELEVANCE
            Threshold: 0.7

Outputs:
  GuardrailId:
    Description: ID of the guardrail
    Value: !GetAtt ContentGuardrail.GuardrailId
    Export:
      Name: !Sub "${AWS::StackName}-GuardrailId"

  GuardrailVersion:
    Description: Version of the guardrail
    Value: !GetAtt ContentGuardrail.GuardrailVersion
    Export:
      Name: !Sub "${AWS::StackName}-GuardrailVersion"

  GuardrailArn:
    Description: ARN of the guardrail
    Value: !GetAtt ContentGuardrail.GuardrailArn
    Export:
      Name: !Sub "${AWS::StackName}-GuardrailArn"
```

## Bedrock Flows for Workflow Orchestration

### Flow with Multiple Nodes

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Bedrock Flow for AI workflow orchestration

Resources:
  # Flow Role
  FlowRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-flow-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: bedrock.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: FlowPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - bedrock:InvokeModel
                  - bedrock:InvokeModelWithResponseStream
                Resource: "*"
              - Effect: Allow
                Action:
                  - bedrock:Retrieve
                Resource: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:knowledge-base/*"

  # Bedrock Flow
  ProcessingFlow:
    Type: AWS::Bedrock::Flow
    Properties:
      Name: !Sub "${AWS::StackName}-processing-flow"
      Description: Flow for processing customer requests
      ExecutionRoleArn: !GetAtt FlowRole.Arn
      Definition:
        StartAt: IntentClassifier
        Nodes:
          IntentClassifier:
            Type: Classifier
            Name: IntentClassifier
            Description: Classifies the user intent
            Configuration:
              BedrockClassifierConfiguration:
                BedrockFoundationModelConfiguration:
                  ModelId: anthropic.claude-v3:5
                  InferenceConfiguration:
                    Temperature: 0.0
                InputConfiguration:
                  TextInput:
                    Name: user_input
                OutputConfiguration:
                  StructuredOutput:
                    Name: intent
                    Description: Classified intent
                    JsonOutputSchema:
                      properties:
                        intent:
                          type: string
                          enum:
                            - product_inquiry
                            - order_status
                            - refund_request
                            - general_question
                        confidence:
                          type: number
            Transitions:
              Next:
                ProductInquiry: product_inquiry
                OrderStatus: order_status
                RefundRequest: refund_request
                GeneralQuestion: "*"
          ProductInquiry:
            Type: KnowledgeBase
            Name: ProductInquiry
            Description: Retrieves product information
            Configuration:
              KnowledgeBaseConfiguration:
                KnowledgeBaseId: !Ref ProductKnowledgeBase
                ModelId: anthropic.claude-v3:5
            Transitions:
              Next: ResponseGenerator
          OrderStatus:
            Type: LambdaFunction
            Name: OrderStatus
            Description: Checks order status
            Configuration:
              LambdaConfiguration:
                LambdaArn: !GetAtt OrderStatusFunction.Arn
            Transitions:
              Next: ResponseGenerator
          RefundRequest:
            Type: LambdaFunction
            Name: RefundRequest
            Description: Processes refund requests
            Configuration:
              LambdaConfiguration:
                LambdaArn: !GetAtt RefundFunction.Arn
            Transitions:
              Next: ResponseGenerator
          GeneralQuestion:
            Type: Model
            Name: GeneralQuestion
            Description: Answers general questions
            Configuration:
              BedrockModelConfiguration:
                ModelId: anthropic.claude-v3:5
                InferenceConfiguration:
                  Temperature: 0.7
                  MaxTokens: 1000
            Transitions:
              Next: ResponseGenerator
          ResponseGenerator:
            Type: Model
            Name: ResponseGenerator
            Description: Generates final response
            Configuration:
              BedrockModelConfiguration:
                ModelId: anthropic.claude-v3:5
                InferenceConfiguration:
                  Temperature: 0.7
                  MaxTokens: 2000
            IsEnd: true

Outputs:
  FlowId:
    Description: ID of the flow
    Value: !Ref ProcessingFlow
    Export:
      Name: !Sub "${AWS::StackName}-FlowId"

  FlowArn:
    Description: ARN of the flow
    Value: !GetAtt ProcessingFlow.Arn
    Export:
      Name: !Sub "${AWS::StackName}-FlowArn"
```

## Inference Profiles for Multi-Model Access

### Application Inference Profile

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Application inference profile for optimized model access

Parameters:
  InferenceProfileName:
    Type: String
    Default: production-profile
    Description: Name of the inference profile

Resources:
  # Application Inference Profile
  ProductionProfile:
    Type: AWS::Bedrock::ApplicationInferenceProfile
    Properties:
      ApplicationInferenceProfileName: !Ref InferenceProfileName
      Description: Production inference profile for multi-model access
      ModelSource:
        CopyFrom: !Sub "arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:application-inference-profile/*"
      InferenceConfiguration:
        Text:
          anthropic.claude-v3:5:
            Temperature: 0.7
            MaxTokens: 4096
            TopP: 0.999
          anthropic.claude-sonnet-4-20250514:
            Temperature: 0.7
            MaxTokens: 4096

Outputs:
  InferenceProfileId:
    Description: ID of the inference profile
    Value: !Ref ProductionProfile
    Export:
      Name: !Sub "${AWS::StackName}-InferenceProfileId"

  InferenceProfileArn:
    Description: ARN of the inference profile
    Value: !GetAtt ProductionProfile.Arn
    Export:
      Name: !Sub "${AWS::StackName}-InferenceProfileArn"
```

## Best Practices

### Security

- Use IAM roles with minimum necessary permissions for Bedrock operations
- Enable encryption for all knowledge base data and vectors
- Use guardrails for content moderation in production deployments
- Implement VPC endpoints for private Bedrock access
- Use AWS Secrets Manager for API keys and credentials
- Configure cross-account access carefully with proper IAM policies
- Audit Bedrock API calls with CloudTrail

### Performance

- Choose appropriate embedding models based on use case
- Optimize chunking strategies for knowledge base ingestion
- Use inference profiles for consistent latency across models
- Monitor token usage and implement rate limiting
- Configure appropriate timeouts for long-running operations
- Use provisioned throughput for predictable workloads
- Cache frequently accessed knowledge base results

### Monitoring

- Enable CloudWatch metrics for Bedrock API calls
- Create alarms for throttled requests and errors
- Monitor knowledge base retrieval latency
- Track token usage and costs per model
- Implement logging for agent interactions
- Monitor guardrail violations and content moderation
- Use Bedrock model invocation logs for debugging

### Cost Optimization

- Use on-demand pricing for variable workloads
- Implement caching for frequent model invocations
- Choose appropriate model sizes for task requirements
- Use knowledge base retrieval filtering to reduce costs
- Implement batch processing for non-real-time workloads
- Monitor and optimize token consumption

## CloudFormation Stack Management Best Practices

### Stack Policies

```yaml
Resources:
  BedrockAgent:
    Type: AWS::Bedrock::Agent
    Properties:
      AgentName: !Sub "${AWS::StackName}-agent"

# Stack policy to protect Bedrock resources
StackPolicy:
  Type: AWS::CloudFormation::StackPolicy
  Properties:
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal: "*"
          Action: "Update:*"
          Resource: "*"
        - Effect: Deny
          Principal: "*"
          Action:
            - Update:Delete
          Resource:
            - LogicalId: BedrockAgent
              ResourceType: AWS::Bedrock::Agent
```

### Drift Detection

```bash
# Detect drift on a stack
aws cloudformation detect-drift --stack-name my-bedrock-stack

# Get resource drift status
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-bedrock-stack
```

## Related Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Bedrock Flows](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html)

## Additional Files

For complete details on resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all Bedrock CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
