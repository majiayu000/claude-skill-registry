---
name: deployment-aws-serverless-setup
description: "Step-by-step guide for setting up AWS serverless deployment with CDK, Lambda, and DynamoDB."
compatibility: "AWS CLI v2, CDK v2, Go 1.25+"
metadata:
  target_cloud: aws
  type: setup
---

# Skill: AWS Serverless Deployment Setup

This skill teaches you how to set up a complete AWS serverless deployment infrastructure for  microservices. You'll configure AWS CDK with Go, create Lambda handlers with proper dependency injection, design DynamoDB tables following single-table patterns, integrate EventBridge for domain events, and automate deployment with Makefiles.

AWS Lambda provides a serverless compute platform that scales automatically, charges only for execution time, and eliminates server management overhead. Combined with API Gateway, DynamoDB, and EventBridge, it forms a complete serverless architecture for event-driven microservices following Clean Architecture and DDD patterns.

This setup follows  reference architecture patterns, ensuring consistency across all bounded contexts while maintaining independent deployability per service.

## Prerequisites

- AWS CLI v2 installed and configured with appropriate credentials
- AWS CDK v2 installed (`npm install -g aws-cdk`)
- Go 1.25 or later installed
- Understanding of Clean Architecture and bounded contexts
- Node.js 18+ (required for CDK)
- A microservice following  directory structure

## Overview

In this skill, you will:
1. Create the project structure for Lambda deployment
2. Implement Go CDK infrastructure code (app, stack, constructs)
3. Create Lambda handler entry points for API, Worker, and EventHandler
4. Design DynamoDB single-table schema
5. Configure EventBridge integration for domain events
6. Create Makefile with build, package, and deploy targets
7. Deploy and verify the serverless stack

## Step 1: Create Deployment Directory Structure

Set up the deployment directory within your microservice to hold CDK code and build artifacts.

### Directory Layout

```bash
# From your microservice root (e.g., services/go/facilitysvc/)
mkdir -p deploy/cdk/constructs
mkdir -p dist
mkdir -p bin/api
mkdir -p bin/worker
mkdir -p bin/eventhandler
```

### Final Structure

After setup, your microservice should have:

```
facilitysvc/
├── cmd/
│   ├── api/
│   │   └── main.go              # API Gateway Lambda
│   ├── worker/
│   │   └── main.go              # SQS Worker Lambda
│   └── eventhandler/
│       └── main.go              # EventBridge Lambda
├── core/
│   ├── domain/
│   └── application/
├── adapters/
│   ├── inbound/
│   └── outbound/
├── deploy/
│   └── cdk/
│       ├── app.go               # CDK app entry point
│       ├── stack.go             # Service stack definition
│       ├── go.mod               # CDK dependencies
│       └── constructs/
│           ├── lambda.go        # Reusable Lambda construct
│           ├── api.go           # API Gateway construct
│           └── table.go         # DynamoDB construct
├── dist/                        # Build artifacts (zip files)
├── Makefile
└── go.mod
```

This structure separates deployment concerns from application code, following hexagonal principles.

## Step 2: Initialize CDK Go Module

Create a separate Go module for CDK infrastructure code to avoid mixing infrastructure dependencies with application code.

```go
// deploy/cdk/go.mod
module github.com//services/go/facilitysvc/deploy/cdk

go 1.25

require (
	github.com/aws/aws-cdk-go/awscdk/v2 v2.180.0
	github.com/aws/constructs-go/constructs/v10 v10.4.2
	github.com/aws/jsii-runtime-go v1.108.0
)
```

Initialize with:

```bash
cd deploy/cdk
go mod init github.com//services/go/facilitysvc/deploy/cdk
go get github.com/aws/aws-cdk-go/awscdk/v2@latest
go get github.com/aws/constructs-go/constructs/v10@latest
go get github.com/aws/jsii-runtime-go@latest
go mod tidy
```

## Step 3: Create CDK App Entry Point

The CDK app is the entry point for infrastructure deployment. It creates stacks based on environment variables.

```go
// deploy/cdk/app.go
package main

import (
	"os"

	"github.com/aws/aws-cdk-go/awscdk/v2"
	"github.com/aws/jsii-runtime-go"
)

func main() {
	defer jsii.Close()

	// Create CDK app
	app := awscdk.NewApp(nil)

	// Get stage from environment (dev, staging, prod)
	stage := os.Getenv("STAGE")
	if stage == "" {
		stage = "dev"
	}

	// Get version for deployment tracking
	version := os.Getenv("VERSION")
	if version == "" {
		version = "latest"
	}

	// Get AWS region
	region := os.Getenv("AWS_REGION")
	if region == "" {
		region = "eu-west-1"
	}

	// Create service stack
	// Stack name includes stage for multi-environment support
	stackName := jsii.String("FacilitySvc-" + stage)

	NewFacilitySvcStack(app, stackName, &FacilitySvcStackProps{
		StackProps: awscdk.StackProps{
			Env: &awscdk.Environment{
				Region: jsii.String(region),
			},
		},
		Stage:   stage,
		Version: version,
	})

	// Synthesize CloudFormation template
	app.Synth(nil)
}
```

This entry point:
- Reads environment variables to configure the stack
- Creates stage-specific stack names for parallel deployments
- Synthesizes the CDK app into CloudFormation templates

## Step 4: Create Service Stack with AWS Resources

Define all AWS resources for the service in a single stack.

```go
// deploy/cdk/stack.go
package main

import (
	"github.com/aws/aws-cdk-go/awscdk/v2"
	"github.com/aws/aws-cdk-go/awscdk/v2/awsapigatewayv2"
	"github.com/aws/aws-cdk-go/awscdk/v2/awsdynamodb"
	"github.com/aws/aws-cdk-go/awscdk/v2/awsevents"
	"github.com/aws/aws-cdk-go/awscdk/v2/awseventstargets"
	"github.com/aws/aws-cdk-go/awscdk/v2/awslambda"
	"github.com/aws/aws-cdk-go/awscdk/v2/awslambdaeventsources"
	"github.com/aws/aws-cdk-go/awscdk/v2/awssqs"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

// FacilitySvcStackProps defines stack configuration.
type FacilitySvcStackProps struct {
	awscdk.StackProps
	Stage   string
	Version string
}

// NewFacilitySvcStack creates the service infrastructure stack.
func NewFacilitySvcStack(scope constructs.Construct, id *string, props *FacilitySvcStackProps) awscdk.Stack {
	stack := awscdk.NewStack(scope, id, &props.StackProps)

	// DynamoDB Table - single table design
	table := awsdynamodb.NewTable(stack, jsii.String("FacilitiesTable"), &awsdynamodb.TableProps{
		TableName:    jsii.String("facilities-" + props.Stage),
		PartitionKey: &awsdynamodb.Attribute{Name: jsii.String("PK"), Type: awsdynamodb.AttributeType_STRING},
		SortKey:      &awsdynamodb.Attribute{Name: jsii.String("SK"), Type: awsdynamodb.AttributeType_STRING},
		BillingMode:  awsdynamodb.BillingMode_PAY_PER_REQUEST,
		// RETAIN prevents accidental data loss during stack updates
		RemovalPolicy:  awscdk.RemovalPolicy_RETAIN,
		PointInTimeRecovery: jsii.Bool(true),
	})

	// Add GSI for facility queries
	table.AddGlobalSecondaryIndex(&awsdynamodb.GlobalSecondaryIndexProps{
		IndexName:    jsii.String("GSI1"),
		PartitionKey: &awsdynamodb.Attribute{Name: jsii.String("GSI1PK"), Type: awsdynamodb.AttributeType_STRING},
		SortKey:      &awsdynamodb.Attribute{Name: jsii.String("GSI1SK"), Type: awsdynamodb.AttributeType_STRING},
	})

	// API Lambda Handler
	apiHandler := awslambda.NewFunction(stack, jsii.String("ApiHandler"), &awslambda.FunctionProps{
		FunctionName: jsii.String("facilitysvc-api-" + props.Stage),
		Runtime:      awslambda.Runtime_PROVIDED_AL2023(),
		Handler:      jsii.String("bootstrap"),
		Architecture: awslambda.Architecture_ARM_64(),
		Code:         awslambda.Code_FromAsset(jsii.String("../../dist/api.zip"), nil),
		MemorySize:   jsii.Number(256),
		Timeout:      awscdk.Duration_Seconds(jsii.Number(30)),
		Environment: &map[string]*string{
			"TABLE_NAME":    table.TableName(),
			"STAGE":         jsii.String(props.Stage),
			"VERSION":       jsii.String(props.Version),
			"EVENT_BUS_NAME": jsii.String("default"),
		},
		Tracing: awslambda.Tracing_ACTIVE,
	})
	table.GrantReadWriteData(apiHandler)

	// SQS Queue for async work
	queue := awssqs.NewQueue(stack, jsii.String("WorkerQueue"), &awssqs.QueueProps{
		QueueName:         jsii.String("facilitysvc-worker-" + props.Stage),
		VisibilityTimeout: awscdk.Duration_Minutes(jsii.Number(5)),
		DeadLetterQueue: &awssqs.DeadLetterQueue{
			Queue:              awssqs.NewQueue(stack, jsii.String("WorkerDLQ"), nil),
			MaxReceiveCount:    jsii.Number(3),
		},
	})

	// Worker Lambda Handler (processes SQS messages)
	workerHandler := awslambda.NewFunction(stack, jsii.String("WorkerHandler"), &awslambda.FunctionProps{
		FunctionName: jsii.String("facilitysvc-worker-" + props.Stage),
		Runtime:      awslambda.Runtime_PROVIDED_AL2023(),
		Handler:      jsii.String("bootstrap"),
		Architecture: awslambda.Architecture_ARM_64(),
		Code:         awslambda.Code_FromAsset(jsii.String("../../dist/worker.zip"), nil),
		MemorySize:   jsii.Number(512),
		Timeout:      awscdk.Duration_Minutes(jsii.Number(5)),
		Environment: &map[string]*string{
			"TABLE_NAME": table.TableName(),
			"STAGE":      jsii.String(props.Stage),
		},
		Tracing: awslambda.Tracing_ACTIVE,
	})
	table.GrantReadWriteData(workerHandler)
	// Connect worker to SQS queue
	workerHandler.AddEventSource(awslambdaeventsources.NewSqsEventSource(queue, &awslambdaeventsources.SqsEventSourceProps{
		BatchSize: jsii.Number(10),
	}))

	// EventBridge Event Handler
	eventHandler := awslambda.NewFunction(stack, jsii.String("EventHandler"), &awslambda.FunctionProps{
		FunctionName: jsii.String("facilitysvc-eventhandler-" + props.Stage),
		Runtime:      awslambda.Runtime_PROVIDED_AL2023(),
		Handler:      jsii.String("bootstrap"),
		Architecture: awslambda.Architecture_ARM_64(),
		Code:         awslambda.Code_FromAsset(jsii.String("../../dist/eventhandler.zip"), nil),
		MemorySize:   jsii.Number(256),
		Timeout:      awscdk.Duration_Seconds(jsii.Number(60)),
		Environment: &map[string]*string{
			"TABLE_NAME": table.TableName(),
			"STAGE":      jsii.String(props.Stage),
		},
		Tracing: awslambda.Tracing_ACTIVE,
	})
	table.GrantReadWriteData(eventHandler)

	// EventBridge Rule - subscribe to domain events
	defaultBus := awsevents.EventBus_FromEventBusName(stack, jsii.String("DefaultBus"), jsii.String("default"))
	rule := awsevents.NewRule(stack, jsii.String("FacilityEventRule"), &awsevents.RuleProps{
		EventBus: defaultBus,
		EventPattern: &awsevents.EventPattern{
			Source: jsii.Strings("asset.context"),
			DetailType: jsii.Strings("AssetStateChanged", "AssetRegistered"),
		},
	})
	rule.AddTarget(awseventstargets.NewLambdaFunction(eventHandler, nil))

	// API Gateway HTTP API
	httpApi := awsapigatewayv2.NewHttpApi(stack, jsii.String("HttpApi"), &awsapigatewayv2.HttpApiProps{
		ApiName: jsii.String("facilitysvc-" + props.Stage),
	})

	// CloudFormation Outputs
	awscdk.NewCfnOutput(stack, jsii.String("ApiUrl"), &awscdk.CfnOutputProps{
		Value:       httpApi.ApiEndpoint(),
		Description: jsii.String("API Gateway endpoint URL"),
	})
	awscdk.NewCfnOutput(stack, jsii.String("TableName"), &awscdk.CfnOutputProps{
		Value:       table.TableName(),
		Description: jsii.String("DynamoDB table name"),
	})

	return stack
}
```

This stack creates:
- DynamoDB table with single-table design (PK/SK)
- API Lambda triggered by API Gateway
- Worker Lambda triggered by SQS
- EventHandler Lambda triggered by EventBridge rules
- Dead-letter queues for reliability

## Step 5: Create Lambda Handler Entry Points

Implement Lambda handlers that initialize dependencies once during cold start, then handle requests efficiently.

### API Handler

```go
// cmd/api/main.go
package main

import (
	"context"
	"log"
	"os"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/eventbridge"
	"github.com/awslabs/aws-lambda-go-api-proxy/httpadapter"

	"github.com//services/go/facilitysvc/adapters/inbound/http"
	"github.com//services/go/facilitysvc/adapters/outbound/dynamodbrepo"
	"github.com//services/go/facilitysvc/adapters/outbound/eventpublisher"
	"github.com//services/go/facilitysvc/core/application"
)

var httpAdapter *httpadapter.HandlerAdapterV2

// init runs once per Lambda cold start - set up dependencies here
func init() {
	ctx := context.Background()

	// Load AWS SDK config
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		log.Fatalf("failed to load AWS config: %v", err)
	}

	// Create AWS service clients
	dynamoClient := dynamodb.NewFromConfig(cfg)
	eventbridgeClient := eventbridge.NewFromConfig(cfg)

	// Get environment variables
	tableName := os.Getenv("TABLE_NAME")
	eventBusName := os.Getenv("EVENT_BUS_NAME")

	// Create adapters (hexagonal architecture)
	repo := dynamodbrepo.NewFacilityRepository(dynamoClient, tableName)
	publisher := eventpublisher.NewEventBridgePublisher(eventbridgeClient, eventBusName)

	// Create application service (use cases)
	appService := application.NewFacilityService(repo, publisher)

	// Create HTTP router (inbound adapter)
	router := http.NewRouter(appService)

	// Wrap router with Lambda API Gateway proxy adapter
	httpAdapter = httpadapter.NewV2(router)
}

// handler processes API Gateway requests
func handler(ctx context.Context, req events.APIGatewayV2HTTPRequest) (events.APIGatewayV2HTTPResponse, error) {
	return httpAdapter.ProxyWithContext(ctx, req)
}

func main() {
	lambda.Start(handler)
}
```

### Worker Handler

```go
// cmd/worker/main.go
package main

import (
	"context"
	"encoding/json"
	"log"
	"os"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"

	"github.com//services/go/facilitysvc/adapters/outbound/dynamodbrepo"
	"github.com//services/go/facilitysvc/core/application"
)

var appService *application.FacilityService

func init() {
	ctx := context.Background()

	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		log.Fatalf("failed to load AWS config: %v", err)
	}

	dynamoClient := dynamodb.NewFromConfig(cfg)
	tableName := os.Getenv("TABLE_NAME")

	repo := dynamodbrepo.NewFacilityRepository(dynamoClient, tableName)
	appService = application.NewFacilityService(repo, nil)
}

// handler processes SQS messages with partial batch failure support
func handler(ctx context.Context, event events.SQSEvent) (events.SQSEventResponse, error) {
	var failures []events.SQSBatchItemFailure

	for _, record := range event.Records {
		var message application.WorkMessage
		if err := json.Unmarshal([]byte(record.Body), &message); err != nil {
			log.Printf("failed to unmarshal message: %v", err)
			failures = append(failures, events.SQSBatchItemFailure{ItemIdentifier: record.MessageId})
			continue
		}

		if err := appService.ProcessWorkMessage(ctx, message); err != nil {
			log.Printf("failed to process message: %v", err)
			failures = append(failures, events.SQSBatchItemFailure{ItemIdentifier: record.MessageId})
		}
	}

	// Return partial batch failures - SQS will reprocess only failed messages
	return events.SQSEventResponse{BatchItemFailures: failures}, nil
}

func main() {
	lambda.Start(handler)
}
```

### EventHandler Lambda

```go
// cmd/eventhandler/main.go
package main

import (
	"context"
	"encoding/json"
	"log"
	"os"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"

	"github.com//services/go/facilitysvc/adapters/outbound/dynamodbrepo"
	"github.com//services/go/facilitysvc/core/application"
)

var appService *application.FacilityService

func init() {
	ctx := context.Background()

	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		log.Fatalf("failed to load AWS config: %v", err)
	}

	dynamoClient := dynamodb.NewFromConfig(cfg)
	tableName := os.Getenv("TABLE_NAME")

	repo := dynamodbrepo.NewFacilityRepository(dynamoClient, tableName)
	appService = application.NewFacilityService(repo, nil)
}

// handler processes EventBridge events
func handler(ctx context.Context, event events.CloudWatchEvent) error {
	log.Printf("received event: %s", event.DetailType)

	var detail map[string]interface{}
	if err := json.Unmarshal(event.Detail, &detail); err != nil {
		return err
	}

	// Route to appropriate handler based on event type
	switch event.DetailType {
	case "AssetStateChanged":
		return appService.HandleAssetStateChanged(ctx, detail)
	case "AssetRegistered":
		return appService.HandleAssetRegistered(ctx, detail)
	default:
		log.Printf("unhandled event type: %s", event.DetailType)
	}

	return nil
}

func main() {
	lambda.Start(handler)
}
```

## Step 6: Create Makefile for Build and Deployment

Automate building, packaging, and deploying Lambda functions.

```makefile
# Makefile
SERVICE_NAME := facilitysvc
VERSION ?= $(shell git describe --tags --always --dirty)

# AWS settings
AWS_REGION ?= eu-west-1
STAGE ?= dev

# Lambda handlers to build
HANDLERS := api worker eventhandler

# CDK directory
CDK_DIR := deploy/cdk

.PHONY: build test package deploy clean

##@ Building

# Build all Lambda handlers
build: $(HANDLERS)

# Build individual handler
$(HANDLERS):
	@echo "Building $@..."
	@GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build \
		-tags lambda.norpc \
		-ldflags="-s -w -X main.version=$(VERSION)" \
		-o bin/$@/bootstrap \
		./cmd/$@

##@ Testing

test: test-unit test-integration

test-unit:
	go test -v -race -coverprofile=coverage.out ./core/...

test-integration:
	go test -v ./tests/integration/...

##@ Packaging

# Package Lambda binaries into zip files
package: build
	@mkdir -p dist
	@for handler in $(HANDLERS); do \
		echo "Packaging $$handler..."; \
		cd bin/$$handler && zip -j ../../dist/$$handler.zip bootstrap && cd ../..; \
	done

##@ Deployment (CDK)

# Bootstrap CDK (run once per account/region)
cdk-bootstrap:
	@cd $(CDK_DIR) && cdk bootstrap aws://$(AWS_ACCOUNT_ID)/$(AWS_REGION)

# Synthesize CDK stack (preview CloudFormation)
cdk-synth: package
	@cd $(CDK_DIR) && STAGE=$(STAGE) VERSION=$(VERSION) cdk synth

# Deploy to AWS
deploy: package
ifndef STAGE
	$(error STAGE is required: make deploy STAGE=dev)
endif
	@echo "Deploying $(SERVICE_NAME) to $(STAGE)..."
	@cd $(CDK_DIR) && STAGE=$(STAGE) VERSION=$(VERSION) AWS_REGION=$(AWS_REGION) cdk deploy --require-approval never

# Show diff before deploying
deploy-diff: package
	@cd $(CDK_DIR) && STAGE=$(STAGE) VERSION=$(VERSION) cdk diff

# Destroy stack (careful!)
destroy:
ifndef STAGE
	$(error STAGE is required)
endif
	@cd $(CDK_DIR) && STAGE=$(STAGE) cdk destroy --require-approval never

##@ Utilities

# Tail Lambda logs
logs:
ifndef STAGE
	$(error STAGE is required)
endif
ifndef HANDLER
	HANDLER=api
endif
	@aws logs tail /aws/lambda/$(SERVICE_NAME)-$(HANDLER)-$(STAGE) --follow --region $(AWS_REGION)

# Invoke API Lambda locally (SAM)
invoke-local: build
	@echo '{"httpMethod":"GET","path":"/facilities"}' | sam local invoke -t $(CDK_DIR)/cdk.out/FacilitySvc-$(STAGE).template.json ApiHandler

# Clean build artifacts
clean:
	@rm -rf bin dist $(CDK_DIR)/cdk.out
	@cd $(CDK_DIR) && rm -rf node_modules

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)
```

## Step 7: Deploy and Verify

Deploy your serverless infrastructure to AWS.

### First Time Setup

```bash
# Bootstrap CDK (once per AWS account/region)
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
make cdk-bootstrap AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID

# Deploy to dev
make deploy STAGE=dev
```

### Regular Deployment

```bash
# Deploy with auto-generated version
make deploy STAGE=dev

# Deploy with specific version
make deploy STAGE=prod VERSION=v1.2.3

# Preview changes before deploying
make deploy-diff STAGE=staging
```

### Verify Deployment

```bash
# Get stack outputs
aws cloudformation describe-stacks \
  --stack-name FacilitySvc-dev \
  --query 'Stacks[0].Outputs' \
  --output table

# Test API endpoint
API_URL=$(aws cloudformation describe-stacks \
  --stack-name FacilitySvc-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text)

curl $API_URL/health

# Tail Lambda logs
make logs STAGE=dev HANDLER=api
```

## Verification Checklist

After completing the AWS serverless setup, verify:

- [ ] CDK directory has separate go.mod from application code
- [ ] CDK app.go reads STAGE, VERSION, and AWS_REGION from environment
- [ ] Stack creates DynamoDB table with PK, SK, and GSI
- [ ] Stack includes API, Worker, and EventHandler Lambdas
- [ ] Lambda functions use PROVIDED_AL2023 runtime with ARM64 architecture
- [ ] All Lambdas have X-Ray tracing enabled
- [ ] SQS queue has dead-letter queue configured
- [ ] EventBridge rule filters events by source and detail type
- [ ] Lambda init() functions set up dependencies (run once per cold start)
- [ ] Lambda handlers are thin wrappers delegating to application layer
- [ ] Makefile builds for GOOS=linux GOARCH=arm64
- [ ] Makefile packages each handler into separate zip files
- [ ] Environment variables passed to Lambdas (TABLE_NAME, STAGE)
- [ ] CloudFormation outputs include API URL and table name
- [ ] CDK bootstrap completed successfully
- [ ] Deployment succeeds without errors
- [ ] API endpoint returns successful response
- [ ] Lambda logs appear in CloudWatch
- [ ] DynamoDB table created with correct configuration
