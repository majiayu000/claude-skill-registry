---
name: aws-sigv4-req-builder
description: Generate Python code to call undocumented AWS APIs using SigV4 authentication from cURL requests captured in browser dev tools. This skill should be used when users need to create Python functions that call AWS internal or undocumented APIs with proper AWS Signature Version 4 authentication.
---

# AWS SigV4 Request Builder

Generate Python code to call undocumented AWS APIs using AWS Signature Version 4 authentication from cURL requests.

## When to Use

Use this skill when users need to:

- Call undocumented AWS APIs from Python
- Convert browser network requests to authenticated Python code
- Build API clients for AWS services without official SDK support

## How to Use

### Step 1: Get cURL from User

Ask the user for the cURL command (from browser dev tools: Network tab → Right-click → Copy as cURL).

### Step 2: Extract Information

From the cURL command, extract:

- **URL**: Full endpoint URL
- **Region**: Extract from URL (e.g., `us-east-1` from `service.us-east-1.amazonaws.com`)
- **Service name**: Extract from authorization header SignedHeaders or URL (e.g., `/us-east-1/q/aws4_request` → "q")
- **Operation name**: Extract from `x-amz-target` header (part after the dot, e.g., `CreateAssignment` from `AmazonQDeveloperService.CreateAssignment`)
- **Function name**: Convert operation name to snake_case (e.g., `CreateAssignment` → `create_assignment`)
- **HTTP method**: From `-X` flag or default to POST if `--data` present
- **Headers**: Content-Type and x-amz-target (exclude authorization, cookie, user-agent, sec-\*, origin, referer, priority)
- **Payload**: From `--data-raw` or `--data`
- **Parameters**: Extract keys from JSON payload

### Step 3: Generate Python Code

Create a Python function following this pattern:

```python
import boto3
import json
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
import requests


def function_name(param1, param2):
    """Call AWS API with description"""

    session = boto3.Session()
    credentials = session.get_credentials()

    payload = {
        "key1": param1,
        "key2": param2
    }

    request = AWSRequest(
        method="POST",
        url="https://service.region.amazonaws.com/",
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/x-amz-json-1.0",
            "x-amz-target": "ServiceName.OperationName",
        },
    )

    SigV4Auth(credentials, "service-name", "region").add_auth(request)

    response = requests.post(request.url, headers=dict(request.headers), data=request.body)

    return response
```

## Example

**User provides cURL:**

```bash
curl 'https://codewhisperer.us-east-1.amazonaws.com/' \
  -H 'authorization: AWS4-HMAC-SHA256 Credential=.../us-east-1/q/aws4_request, ...' \
  -H 'content-type: application/x-amz-json-1.0' \
  -H 'x-amz-target: AmazonQDeveloperService.CreateAssignment' \
  --data-raw '{"principalId":"123","principalType":"USER","subscriptionType":"Q_DEVELOPER_STANDALONE_PRO"}'
```

**Auto-extracted:**

- Service: "q" (from authorization header: `/us-east-1/q/aws4_request`)
- Region: "us-east-1" (from URL)
- Operation: "CreateAssignment" (from x-amz-target)
- Function name: "create_assignment" (snake_case of operation)
- Parameters: principalId, principalType, subscriptionType (from payload)

**Generated code:**

```python
import boto3
import json
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
import requests


def create_assignment(principal_id, principal_type="USER", subscription_type="Q_DEVELOPER_STANDALONE_PRO"):
    """Create Q Developer subscription assignment"""

    session = boto3.Session()
    credentials = session.get_credentials()

    payload = {
        "principalId": principal_id,
        "principalType": principal_type,
        "subscriptionType": subscription_type
    }

    request = AWSRequest(
        method="POST",
        url="https://codewhisperer.us-east-1.amazonaws.com/",
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/x-amz-json-1.0",
            "x-amz-target": "AmazonQDeveloperService.CreateAssignment",
        },
    )

    SigV4Auth(credentials, "q", "us-east-1").add_auth(request)

    response = requests.post(request.url, headers=dict(request.headers), data=request.body)

    return response
```

## Prerequisites

Generated code requires:

- Python 3.6+
- boto3: `pip install boto3`
- requests: `pip install requests`
- AWS credentials configured
