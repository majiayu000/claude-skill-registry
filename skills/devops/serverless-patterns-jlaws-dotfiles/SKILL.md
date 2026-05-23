---
name: serverless-patterns
description: Build event-driven serverless applications with Lambda, Step Functions, and managed compute
---

# Serverless Patterns

## Serverless vs Containers Decision

| Factor | Serverless (Lambda) | Containers (ECS/K8s) |
|--------|-------------------|----------------------|
| **Startup time** | Cold start 100ms-10s | Always warm |
| **Max duration** | 15min (Lambda) | Unlimited |
| **Concurrency** | 1000 default (adjustable) | Pod/task scaling |
| **Cost at low traffic** | Near zero | Base cost always |
| **Cost at high traffic** | Expensive at scale | More predictable |
| **State** | Stateless only | Stateful possible |
| **Best for** | Event-driven, bursty, glue | Long-running, steady, stateful |

**Rule of thumb:** Lambda for <100ms avg, <15min max, bursty traffic. Containers for steady load, long-running, or >1M invocations/day (cost crossover).

## Lambda Handler Patterns

### API Gateway Handler

```python
import json, logging, urllib.parse, boto3
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def api_handler(event: dict, context: Any) -> dict:
    """API Gateway proxy integration handler."""
    method = event["httpMethod"]
    body = json.loads(event.get("body") or "{}")
    params = event.get("pathParameters") or {}
    try:
        if method == "GET":
            result = get_user(params["user_id"])
        elif method == "POST":
            result = create_user(body)
        else:
            return response(404, {"error": "Not found"})
        return response(200, result)
    except ValidationError as e:
        return response(400, {"error": str(e)})
    except Exception:
        logger.exception("Unhandled error")
        return response(500, {"error": "Internal server error"})

def response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json",
                     "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body, default=str),
    }
```

### SQS Trigger Handler

```python
def sqs_handler(event: dict, context: Any) -> dict:
    """Process SQS batch with partial failure reporting."""
    failed_ids = []
    for record in event["Records"]:
        try:
            process_message(json.loads(record["body"]))
        except Exception as e:
            logger.error(f"Failed: {record['messageId']}: {e}")
            failed_ids.append(record["messageId"])
    return {"batchItemFailures": [{"itemIdentifier": mid} for mid in failed_ids]}
```

### S3 Event Handler

```python
s3 = boto3.client("s3")

def s3_handler(event: dict, context: Any):
    """Process S3 put events (image resize, ETL, etc.)."""
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        if key.startswith("processed/"):  # Guard: skip own output
            continue
        obj = s3.get_object(Bucket=bucket, Key=key)
        result = transform(obj["Body"].read())
        s3.put_object(Bucket=bucket, Key=f"processed/{key}", Body=result)
```

## Cold Start Mitigation

```python
import json                               # stdlib: free
import boto3                              # Pre-installed in Lambda runtime

# Lazy import for heavy libraries
_pandas = None
def get_pandas():
    global _pandas
    if _pandas is None:
        import pandas as _pandas
    return _pandas

# Connection reuse: initialize outside handler, reused across warm invocations
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-table")

def handler(event, context):
    return table.get_item(Key={"pk": event["id"]})
# Deps: don't bundle boto3 (in runtime). Avoid pandas (75MB); use Lambda layer.
```

### Provisioned Concurrency

```python
lambda_client = boto3.client("lambda")

version = lambda_client.publish_version(FunctionName="my-function")["Version"]
lambda_client.put_provisioned_concurrency_config(
    FunctionName="my-function", Qualifier=version,
    ProvisionedConcurrentExecutions=10,   # 10 warm instances always ready
)
lambda_client.create_alias(
    FunctionName="my-function", Name="live", FunctionVersion=version,
)
# API Gateway routes to alias "live" -> always warm
```

## Serverless ML Inference

### SageMaker Serverless Endpoint

```python
sagemaker_rt = boto3.client("sagemaker-runtime")

def invoke_model(endpoint: str, payload: dict) -> dict:
    resp = sagemaker_rt.invoke_endpoint(
        EndpointName=endpoint, ContentType="application/json",
        Body=json.dumps(payload))
    return json.loads(resp["Body"].read().decode())
# Config: MaxConcurrency=10, MemorySizeInMB=4096, ProvisionedConcurrency=2
```

### Modal for Serverless GPU

```python
import modal

app = modal.App("ml-inference")
image = modal.Image.debian_slim().pip_install("torch==2.1.0", "transformers==4.36.0")

@app.cls(gpu="A10G", image=image, container_idle_timeout=300)
class TextGenerator:
    @modal.enter()                        # Runs once on container start
    def load_model(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
        self.model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-v0.1", device_map="auto")

    @modal.method()
    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## Step Functions Workflow Orchestration

```python
workflow = {
    "StartAt": "ValidateOrder",
    "States": {
        "ValidateOrder": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123:function:validate-order",
            "Next": "ProcessPayment",
            "Retry": [{"ErrorEquals": ["States.TaskFailed"],
                        "IntervalSeconds": 2, "MaxAttempts": 3, "BackoffRate": 2.0}],
            "Catch": [{"ErrorEquals": ["States.ALL"],
                        "Next": "OrderFailed", "ResultPath": "$.error"}],
        },
        "ProcessPayment": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123:function:process-payment",
            "Next": "FulfillOrder",
            "Catch": [{"ErrorEquals": ["PaymentDeclined"], "Next": "OrderFailed"},
                       {"ErrorEquals": ["States.ALL"], "Next": "OrderFailed"}],
        },
        "FulfillOrder": {
            "Type": "Parallel",                # Ship + email in parallel
            "Branches": [
                {"StartAt": "Ship", "States": {"Ship": {
                    "Type": "Task", "Resource": "arn:...ship", "End": True}}},
                {"StartAt": "Email", "States": {"Email": {
                    "Type": "Task", "Resource": "arn:...email", "End": True}}},
            ],
            "Next": "OrderComplete",
        },
        "OrderComplete": {"Type": "Succeed"},
        "OrderFailed": {"Type": "Fail", "Cause": "Order processing failed"},
    },
}

# Map state: process array items in parallel
map_state = {
    "Type": "Map",
    "ItemsPath": "$.order.items",         # Array to iterate
    "MaxConcurrency": 10,
    "Iterator": {"StartAt": "ProcessItem", "States": {"ProcessItem": {
        "Type": "Task", "Resource": "arn:...process-item",
        "Retry": [{"ErrorEquals": ["States.TaskFailed"],
                    "IntervalSeconds": 1, "MaxAttempts": 2}],
        "End": True}}},
    "Next": "AggregateResults",
}
```

## Lambda Layers for Shared Dependencies

```python
import subprocess, zipfile, os

def build_lambda_layer(requirements: list[str], layer_name: str) -> str:
    layer_dir = "/tmp/layer/python"
    os.makedirs(layer_dir, exist_ok=True)
    subprocess.run(["pip", "install", *requirements, "-t", layer_dir,
                     "--platform", "manylinux2014_x86_64",
                     "--only-binary=:all:"], check=True)
    zip_path = f"/tmp/{layer_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk("/tmp/layer"):
            for f in files:
                fp = os.path.join(root, f)
                zf.write(fp, os.path.relpath(fp, "/tmp/layer"))
    return zip_path

lambda_client.publish_layer_version(
    LayerName="shared-utils", Content={"ZipFile": open(zip_path, "rb").read()},
    CompatibleRuntimes=["python3.11", "python3.12"])
```

## Gotchas

- **Cold start compounds**: Lambda + VPC + RDS = 5-10s cold start; use RDS Proxy + provisioned concurrency
- **15-minute timeout**: Step Functions for anything longer; don't chain Lambdas via invoke
- **Concurrency limits are account-wide**: 1000 default shared across ALL functions; set reserved concurrency
- **SQS batch size trap**: Batch of 10 = 1 invocation; enable ReportBatchItemFailures for partial retry
- **Idempotency is mandatory**: Lambda retries on timeout; every handler must handle duplicates
- **CloudWatch costs**: Verbose logging at high invocation rates generates surprising log storage bills
- **Step Functions payload limit**: 256KB max per state; use S3 for large payloads, pass references
- **Lambda /tmp is 512MB default**: Request up to 10GB ephemeral storage for ML models
- **Environment variable limit**: 4KB total for all env vars; use Parameter Store for large configs
