---
name: boto3
description: AWS SDK for Python for creating service clients/resources and calling AWS APIs.
version: 1.42.58
ecosystem: python
license: Apache-2.0
generated_with: gpt-5.2
---

## Imports

```python
import boto3
from botocore.exceptions import ClientError
```

## Core Patterns

### Create a low-level service client ✅ Current
```python
import boto3

def make_s3_client(region_name: str = "us-east-1"):
    # Prefer credentials/region from ~/.aws/{credentials,config};
    # pass region_name explicitly when you need deterministic behavior.
    return boto3.client("s3", region_name=region_name)

if __name__ == "__main__":
    s3 = make_s3_client()
    # This call is safe to run; it only constructs the client.
    print(f"Created client: {s3.meta.service_model.service_name}")
```
* Use `boto3.client(service_name, region_name=...)` for explicit API operations (e.g., `get_bucket_cors`, `put_bucket_cors`, SES/EC2 operations).

### Create a high-level service resource ✅ Current
```python
import boto3

def make_s3_resource(region_name: str = "us-east-1"):
    return boto3.resource("s3", region_name=region_name)

if __name__ == "__main__":
    s3 = make_s3_resource()
    # Resource objects provide an OO interface; operations require AWS access when called.
    print(f"Created resource: {s3.meta.service_name}")
```
* Use `boto3.resource(service_name, ...)` when you want object-oriented access patterns.

### Handle AWS errors with ClientError and error codes ✅ Current
```python
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

def get_bucket_cors_rules(bucket_name: str, region_name: str = "us-east-1") -> list[dict]:
    s3 = boto3.client("s3", region_name=region_name)
    try:
        return s3.get_bucket_cors(Bucket=bucket_name)["CORSRules"]
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        if code == "NoSuchCORSConfiguration":
            return []
        raise  # re-raise unexpected failures (permissions, missing bucket, etc.)

if __name__ == "__main__":
    # Example usage (will make a network call if executed with real bucket name)
    bucket = "amzn-s3-demo-bucket"
    try:
        rules = get_bucket_cors_rules(bucket)
        logging.info("CORS rules: %s", rules)
    except ClientError as e:
        logging.error("AWS error: %s", e)
```
* Catch `botocore.exceptions.ClientError` (not `Exception`) and branch on `e.response['Error']['Code']` for expected conditions.

### Put S3 bucket CORS using the documented request shape ✅ Current
```python
import boto3

def set_bucket_cors(bucket_name: str, region_name: str = "us-east-1") -> None:
    s3 = boto3.client("s3", region_name=region_name)

    cors_configuration: dict = {
        "CORSRules": [
            {
                "AllowedHeaders": ["Authorization"],
                "AllowedMethods": ["GET", "PUT"],
                "AllowedOrigins": ["*"],
                "ExposeHeaders": ["ETag", "x-amz-request-id"],
                "MaxAgeSeconds": 3000,
            }
        ]
    }

    s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)

if __name__ == "__main__":
    # Requires an existing bucket and permissions when executed.
    set_bucket_cors("amzn-s3-demo-bucket")
```
* The top-level key must be `CORSRules` inside `CORSConfiguration=...`.

### Manage SES templates and send templated email ✅ Current
```python
import boto3

def ensure_template(template_name: str, region_name: str = "us-east-1") -> None:
    ses = boto3.client("ses", region_name=region_name)

    valid_html = "<html><body><p>Hello</p></body></html>"
    template: dict = {
        "TemplateName": template_name,
        "SubjectPart": "SUBJECT_LINE",
        "TextPart": "TEXT_CONTENT",
        "HtmlPart": valid_html,
    }

    # Create or update depending on existence
    existing = ses.list_templates().get("TemplatesMetadata", [])
    if any(t.get("Name") == template_name for t in existing):
        ses.update_template(Template=template)
    else:
        ses.create_template(Template=template)

def send_email(template_name: str, to_address: str, from_address: str, region_name: str = "us-east-1") -> None:
    ses = boto3.client("ses", region_name=region_name)

    ses.send_templated_email(
        Source=from_address,
        Destination={"ToAddresses": [to_address]},
        Template=template_name,
        TemplateData='{"name":"World"}',
    )

if __name__ == "__main__":
    # Requires verified identities in SES and correct permissions when executed.
    ensure_template("TEMPLATE_NAME")
    # send_email("TEMPLATE_NAME", "recipient@example.com", "sender@example.com")
```
* SES does not validate HTML; validate/format HTML yourself before calling `create_template`/`update_template`.
* Template operations: `create_template`, `list_templates`, `get_template`, `update_template`, `delete_template`, `send_templated_email`.

### Upload and download files to/from S3 ✅ Current
```python
import boto3
from boto3.s3.transfer import TransferConfig

def upload_file_to_s3(file_path: str, bucket: str, key: str, region_name: str = "us-east-1") -> None:
    """Upload a file to S3 using the high-level upload_file method."""
    s3 = boto3.client("s3", region_name=region_name)
    
    # Configure transfer options
    config = TransferConfig(
        multipart_threshold=8 * 1024 * 1024,  # 8MB
        max_concurrency=10,
        use_threads=True
    )
    
    s3.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
        Config=config
    )

def download_file_from_s3(bucket: str, key: str, file_path: str, region_name: str = "us-east-1") -> None:
    """Download a file from S3 using the high-level download_file method."""
    s3 = boto3.client("s3", region_name=region_name)
    
    config = TransferConfig(
        multipart_threshold=8 * 1024 * 1024,
        max_concurrency=10,
        use_threads=True
    )
    
    s3.download_file(
        Bucket=bucket,
        Key=key,
        Filename=file_path,
        Config=config
    )

if __name__ == "__main__":
    # Example usage (requires valid bucket and permissions)
    # upload_file_to_s3("local_file.txt", "my-bucket", "uploads/file.txt")
    # download_file_from_s3("my-bucket", "uploads/file.txt", "downloaded_file.txt")
    pass
```
* Use `upload_file()` and `download_file()` for efficient file transfers with automatic multipart handling.
* Configure `TransferConfig` to control multipart thresholds, concurrency, and threading behavior.

### Use S3 resources for object-oriented operations ✅ Current
```python
import boto3

def upload_with_resource(file_path: str, bucket_name: str, key: str, region_name: str = "us-east-1") -> None:
    """Upload using the S3 Bucket resource."""
    s3 = boto3.resource("s3", region_name=region_name)
    bucket = s3.Bucket(bucket_name)
    
    bucket.upload_file(Filename=file_path, Key=key)

def load_bucket_metadata(bucket_name: str, region_name: str = "us-east-1") -> dict:
    """Load bucket metadata using resource."""
    s3 = boto3.resource("s3", region_name=region_name)
    bucket = s3.Bucket(bucket_name)
    
    # Calling load() fetches bucket metadata
    bucket.load()
    
    return {
        "name": bucket.name,
        "creation_date": bucket.creation_date
    }

if __name__ == "__main__":
    # Example usage (requires valid bucket)
    # upload_with_resource("file.txt", "my-bucket", "uploads/file.txt")
    # metadata = load_bucket_metadata("my-bucket")
    pass
```
* S3 resources provide object-oriented interfaces: `Bucket.upload_file()`, `Object.download_file()`, etc.
* Call `load()` on bucket/object resources to fetch metadata from AWS.

### Use Session for custom credential and region configuration ✅ Current
```python
import boto3

def create_session_with_profile(profile_name: str) -> boto3.Session:
    """Create a session using a named profile from ~/.aws/config."""
    return boto3.Session(profile_name=profile_name)

def create_client_from_session(profile_name: str, service_name: str, region_name: str) -> boto3.client:
    """Create a client using custom session configuration."""
    session = boto3.Session(
        profile_name=profile_name,
        region_name=region_name
    )
    return session.client(service_name)

if __name__ == "__main__":
    # Use a specific profile and region
    s3 = create_client_from_session("dev-profile", "s3", "us-west-2")
    # s3.list_buckets()
```
* Use `boto3.Session()` to manage custom credential profiles and regions.
* Create clients and resources from sessions to isolate configuration.

## Configuration

- Preferred configuration is via shared config files (avoid hardcoding credentials):
  - `~/.aws/credentials` (profiles, access keys)
  - `~/.aws/config` (default region/output, named profiles)
- Common environment variables (standard AWS SDK behavior):
  - `AWS_PROFILE` (select profile)
  - `AWS_REGION` / `AWS_DEFAULT_REGION` (default region)
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` (temporary creds)
- When region must be deterministic (CI, containers), pass `region_name=...` to `boto3.client(...)` / `boto3.resource(...)`.

## Pitfalls

### Wrong: Assuming region is configured for client creation and calls
```python
import boto3

s3 = boto3.client("s3")
resp = s3.list_buckets()
print(resp)
```

### Right: Set region explicitly when needed (or configure in ~/.aws/config)
```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
resp = s3.list_buckets()
print(resp)
```

### Wrong: Catching Exception hides real AWS failures
```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
bucket_name = "amzn-s3-demo-bucket"

try:
    rules = s3.get_bucket_cors(Bucket=bucket_name)["CORSRules"]
except Exception:
    rules = []
print(rules)
```

### Right: Catch ClientError and branch on AWS error code
```python
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

s3 = boto3.client("s3", region_name="us-east-1")
bucket_name = "amzn-s3-demo-bucket"

try:
    rules = s3.get_bucket_cors(Bucket=bucket_name)["CORSRules"]
except ClientError as e:
    if e.response["Error"]["Code"] == "NoSuchCORSConfiguration":
        rules = []
    else:
        logging.error("Unexpected AWS error: %s", e)
        raise

print(rules)
```

### Wrong: Using the wrong S3 CORS request shape (parameter validation error)
```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")

cors_configuration = {
    "Rules": [  # wrong key; should be "CORSRules"
        {"AllowedMethods": ["GET"], "AllowedOrigins": ["*"]}
    ]
}

s3.put_bucket_cors(Bucket="amzn-s3-demo-bucket", CORSConfiguration=cors_configuration)
```

### Right: Use `CORSConfiguration={'CORSRules': [...]}` with correct keys
```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")

cors_configuration = {
    "CORSRules": [
        {
            "AllowedHeaders": ["Authorization"],
            "AllowedMethods": ["GET", "PUT"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": ["ETag", "x-amz-request-id"],
            "MaxAgeSeconds": 3000,
        }
    ]
}

s3.put_bucket_cors(Bucket="amzn-s3-demo-bucket", CORSConfiguration=cors_configuration)
```

### Wrong: Assuming SES validates HTML template content
```python
import boto3

ses = boto3.client("ses", region_name="us-east-1")

ses.create_template(
    Template={
        "TemplateName": "TEMPLATE_NAME",
        "SubjectPart": "SUBJECT",
        "TextPart": "TEXT",
        "HtmlPart": "<html><body><p>unclosed tags",
    }
)
```

### Right: Validate/produce well-formed HTML before calling SES
```python
import boto3

ses = boto3.client("ses", region_name="us-east-1")

valid_html = "<html><body><p>Hello</p></body></html>"

ses.create_template(
    Template={
        "TemplateName": "TEMPLATE_NAME",
        "SubjectPart": "SUBJECT_LINE",
        "TextPart": "TEXT_CONTENT",
        "HtmlPart": valid_html,
    }
)
```

### Wrong: Not handling AccessDenied when loading bucket metadata
```python
import boto3

s3 = boto3.resource("s3", region_name="us-east-1")
bucket = s3.Bucket("my-bucket")
bucket.load()  # May raise ClientError if access denied
print(bucket.creation_date)
```

### Right: Handle AccessDenied gracefully
```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource("s3", region_name="us-east-1")
bucket = s3.Bucket("my-bucket")

try:
    bucket.load()
    print(f"Bucket created: {bucket.creation_date}")
except ClientError as e:
    if e.response["Error"]["Code"] == "AccessDenied":
        print("Access denied to bucket metadata")
    else:
        raise
```

### Wrong: Using threading with append mode file operations
```python
import boto3
from boto3.s3.transfer import TransferConfig

s3 = boto3.client("s3", region_name="us-east-1")

config = TransferConfig(use_threads=True)

# Opening file in append mode
with open("file.txt", "ab") as f:
    # Threading with append mode can cause corruption
    s3.download_fileobj("my-bucket", "key", f, Config=config)
```

### Right: Disable threading for append mode operations
```python
import boto3
from boto3.s3.transfer import TransferConfig

s3 = boto3.client("s3", region_name="us-east-1")

# Disable threading for append mode
config = TransferConfig(use_threads=False)

with open("file.txt", "ab") as f:
    s3.download_fileobj("my-bucket", "key", f, Config=config)
```

## References

- Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- Source: https://github.com/boto/boto3

## Migration from v1.42.44

- No breaking changes in core APIs between v1.42.44 and v1.42.58.
- Runtime support policy note:
  - Python 3.8 support ended on 2025-04-22 (upgrade off 3.8).
  - Python 3.9 support ends on 2026-04-29 (plan upgrade before that date).
- New capabilities in S3 transfer utilities documented in Core Patterns section.

## API Reference

- **boto3.client(service_name, region_name=...)** - Create a low-level service client for explicit AWS API operations.
- **boto3.resource(service_name, region_name=...)** - Create a high-level resource interface (OO-style) for supported services.
- **boto3.Session(aws_access_key_id=..., aws_secret_access_key=..., aws_session_token=..., region_name=..., profile_name=...)** - Create a session to manage custom credential and region configuration.
- **boto3.setup_default_session(**kwargs)** - Set up a default session with custom parameters.
- **boto3.set_stream_logger(name='boto3', level=logging.DEBUG, format_string=None)** - Add a stream handler for logging.
- **boto3.s3.transfer.S3Transfer(client=..., config=..., osutil=..., manager=...)** - S3 transfer manager for uploading and downloading files.
- **boto3.s3.transfer.TransferConfig(multipart_threshold=..., max_concurrency=..., multipart_chunksize=..., num_download_attempts=..., max_io_queue=..., io_chunksize=..., use_threads=..., max_bandwidth=..., preferred_transfer_client=...)** - Configuration object for S3 transfers.
- **S3.Client.upload_file(Filename=..., Bucket=..., Key=..., ExtraArgs=..., Callback=..., Config=...)** - Upload a file to S3.
- **S3.Client.download_file(Bucket=..., Key=..., Filename=..., ExtraArgs=..., Callback=..., Config=...)** - Download a file from S3.
- **S3.Bucket.upload_file(Filename=..., Key=..., ExtraArgs=..., Callback=..., Config=...)** - Upload a file to bucket (resource method).
- **S3.Bucket.download_file(Key=..., Filename=..., ExtraArgs=..., Callback=..., Config=...)** - Download a file from bucket (resource method).
- **S3.Bucket.load()** - Load bucket metadata from AWS (handles AccessDenied).
- **S3.Object.upload_file(Filename=..., ExtraArgs=..., Callback=..., Config=...)** - Upload file to object (resource method).
- **S3.Object.download_file(Filename=..., ExtraArgs=..., Callback=..., Config=...)** - Download file from object (resource method).
- **EC2.Client.describe_addresses()** - Describe Elastic IP addresses allocated to the account (supports filters/queries via parameters).
- **EC2.Client.allocate_address()** - Allocate a new Elastic IP address.
- **EC2.Client.associate_address()** - Associate an Elastic IP address with an instance or network interface.
- **EC2.Client.release_address()** - Release an Elastic IP address back to AWS.
- **S3.Client.get_bucket_cors(Bucket=...)** - Fetch a bucket's CORS rules; may raise `ClientError` with `NoSuchCORSConfiguration`.
- **S3.Client.put_bucket_cors(Bucket=..., CORSConfiguration=...)** - Set a bucket's CORS rules (must use `CORSRules` key).
- **SES.Client.create_template(Template=...)** - Create an email template (SES does not validate HTML).
- **SES.Client.list_templates()** - List template metadata (names).
- **SES.Client.get_template(TemplateName=...)** - Retrieve a template's full content.
- **SES.Client.update_template(Template=...)** - Update an existing template.
- **SES.Client.delete_template(TemplateName=...)** - Delete a template.
- **SES.Client.send_templated_email(Source=..., Destination=..., Template=..., TemplateData=...)** - Send an email using a stored template.
- **botocore.exceptions.ClientError** - Exception type for AWS service API errors; inspect `e.response['Error']['Code']`.
- **boto3.exceptions.RetriesExceededError** - Exception raised when transfer retries are exceeded.
- **boto3.exceptions.S3UploadFailedError** - Exception raised when S3 upload fails.