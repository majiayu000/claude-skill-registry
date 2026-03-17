---
name: cloudflare-r2
description: Cloudflare R2 object storage with S3-compatible API and zero egress fees
---

# Cloudflare-R2 Skill

Comprehensive assistance with cloudflare-r2 development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with cloudflare-r2
- Asking about cloudflare-r2 features or APIs
- Implementing cloudflare-r2 solutions
- Debugging cloudflare-r2 code
- Learning cloudflare-r2 best practices

## Quick Reference

### Common Patterns

#### R2 Data Catalog - Apache Iceberg Integration

```bash
# Enable Data Catalog on bucket (Wrangler CLI)
npx wrangler r2 bucket catalog enable my-bucket

# Enable via Dashboard: R2 > Bucket > Settings > R2 Data Catalog > Enable
# Note the Warehouse and Catalog URI values
```

#### Python - PyIceberg Catalog Connection

```python
from pyiceberg.catalog.rest import RestCatalog

# Connection configuration
catalog = RestCatalog(
    name="my_catalog",
    warehouse="<WAREHOUSE_ID>",  # From catalog settings
    uri="<CATALOG_URI>",          # From catalog settings
    token="<API_TOKEN>",          # Admin Read & Write token
)

# Create namespace
catalog.create_namespace_if_not_exists("default")

# Create table with schema
test_table = ("default", "people")
table = catalog.create_table(test_table, schema=df.schema)

# Append data
table.append(df)

# Query data
result = table.scan().to_arrow()

# Drop table
catalog.drop_table(test_table)
```

#### Data Catalog - API Token Setup

```bash
# 1. Navigate to: R2 > Manage API tokens > Create API token
# 2. Select "Admin Read & Write" permission (required for catalog access)
# 3. Save token for authentication

# Token must grant both R2 and catalog permissions for Iceberg clients
```

#### S3-Compatible SDK Usage (boto3)

```python
import boto3

# Configure S3 client for R2
s3_client = boto3.client(
    's3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY_ID>',
    aws_secret_access_key='<SECRET_ACCESS_KEY>',
    region_name='auto'
)

# Upload object
s3_client.put_object(
    Bucket='my-bucket',
    Key='path/to/file.txt',
    Body=b'File contents'
)

# Download object
response = s3_client.get_object(Bucket='my-bucket', Key='path/to/file.txt')
data = response['Body'].read()

# List objects
response = s3_client.list_objects_v2(Bucket='my-bucket', Prefix='path/')
for obj in response.get('Contents', []):
    print(obj['Key'])

# Delete object
s3_client.delete_object(Bucket='my-bucket', Key='path/to/file.txt')
```

#### Presigned URLs

```python
# Generate presigned URL for upload (expires in 1 hour)
presigned_url = s3_client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'uploads/file.txt'
    },
    ExpiresIn=3600
)

# Generate presigned URL for download
download_url = s3_client.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'path/to/file.txt'
    },
    ExpiresIn=3600
)
```

#### Multipart Upload

```python
# Initiate multipart upload
multipart = s3_client.create_multipart_upload(
    Bucket='my-bucket',
    Key='large-file.bin'
)
upload_id = multipart['UploadId']

# Upload parts
parts = []
for i, chunk in enumerate(file_chunks, start=1):
    part = s3_client.upload_part(
        Bucket='my-bucket',
        Key='large-file.bin',
        PartNumber=i,
        UploadId=upload_id,
        Body=chunk
    )
    parts.append({'PartNumber': i, 'ETag': part['ETag']})

# Complete multipart upload
s3_client.complete_multipart_upload(
    Bucket='my-bucket',
    Key='large-file.bin',
    UploadId=upload_id,
    MultipartUpload={'Parts': parts}
)
```

#### Workers Integration

```javascript
export default {
  async fetch(request, env) {
    const bucket = env.MY_BUCKET; // R2 bucket binding

    // Upload to R2
    await bucket.put('key', 'value', {
      httpMetadata: {
        contentType: 'text/plain',
      },
      customMetadata: {
        user: 'example',
      },
    });

    // Retrieve from R2
    const object = await bucket.get('key');

    if (object === null) {
      return new Response('Object Not Found', { status: 404 });
    }

    // Return object with metadata
    return new Response(object.body, {
      headers: {
        'Content-Type': object.httpMetadata.contentType,
        'ETag': object.httpEtag,
      },
    });
  },
};
```

#### Bucket CORS Configuration

```javascript
// Set CORS policy via S3 SDK
const corsConfig = {
  CORSRules: [
    {
      AllowedOrigins: ['https://example.com'],
      AllowedMethods: ['GET', 'PUT', 'POST', 'DELETE'],
      AllowedHeaders: ['*'],
      MaxAgeSeconds: 3000,
    },
  ],
};

await s3_client.put_bucket_cors(
  Bucket='my-bucket',
  CORSConfiguration=corsConfig
);
```

#### Object Metadata

```python
# Upload with custom metadata
s3_client.put_object(
    Bucket='my-bucket',
    Key='document.pdf',
    Body=file_data,
    Metadata={
        'author': 'John Doe',
        'department': 'Engineering',
        'classification': 'internal',
    },
    ContentType='application/pdf',
)

# Retrieve metadata without downloading object
response = s3_client.head_object(Bucket='my-bucket', Key='document.pdf')
metadata = response['Metadata']
content_type = response['ContentType']
```

#### Data Catalog - Apache Spark Integration

```python
from pyspark.sql import SparkSession

# Configure Spark with R2 Data Catalog
spark = SparkSession.builder \
    .config("spark.sql.catalog.r2", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.r2.catalog-impl", "org.apache.iceberg.rest.RESTCatalog") \
    .config("spark.sql.catalog.r2.uri", "<CATALOG_URI>") \
    .config("spark.sql.catalog.r2.warehouse", "<WAREHOUSE_ID>") \
    .config("spark.sql.catalog.r2.token", "<API_TOKEN>") \
    .getOrCreate()

# Create table
spark.sql("""
    CREATE TABLE r2.default.events (
        event_id STRING,
        timestamp TIMESTAMP,
        user_id STRING,
        action STRING
    ) USING iceberg
""")

# Insert data
spark.sql("""
    INSERT INTO r2.default.events
    VALUES ('evt123', current_timestamp(), 'user456', 'login')
""")

# Query data
df = spark.sql("SELECT * FROM r2.default.events WHERE action = 'login'")
df.show()
```

#### R2 SQL - Serverless Analytics Query Engine

```bash
# Query R2 Data Catalog tables with R2 SQL (Wrangler CLI)
npx wrangler r2 sql query "YOUR_WAREHOUSE_NAME" "SELECT * FROM default.table LIMIT 10"

# Authentication setup (required before querying)
export WRANGLER_R2_SQL_AUTH_TOKEN="YOUR_API_TOKEN"

# API token needs: Admin Read & Write + R2 SQL Read permissions
# Create at: R2 > Manage API tokens > Create API token
```

#### R2 SQL - Basic Query Patterns

```bash
# Select with filtering
npx wrangler r2 sql query "warehouse-123" \
  "SELECT user_id, event_type, product_id, amount
   FROM default.ecommerce
   WHERE event_type = 'purchase'
   LIMIT 10"

# Aggregation queries
npx wrangler r2 sql query "warehouse-123" \
  "SELECT
     user_id,
     COUNT(*) as transaction_count,
     SUM(amount) as total_spent
   FROM default.transactions
   GROUP BY user_id
   HAVING total_spent > 1000
   ORDER BY total_spent DESC"

# Time-based filtering
npx wrangler r2 sql query "warehouse-123" \
  "SELECT * FROM default.events
   WHERE timestamp >= '2024-01-01'
     AND timestamp < '2024-02-01'
   ORDER BY timestamp DESC"

# Join operations
npx wrangler r2 sql query "warehouse-123" \
  "SELECT
     u.user_id,
     u.name,
     t.transaction_id,
     t.amount
   FROM default.users u
   JOIN default.transactions t ON u.user_id = t.user_id
   WHERE t.fraud_flag = false"
```

#### R2 SQL - Stream Processing

```bash
# Insert from stream to sink table (continuous processing)
npx wrangler r2 sql query "warehouse-123" \
  "INSERT INTO ecommerce_sink
   SELECT * FROM ecommerce_stream"

# Filtered stream transformation
npx wrangler r2 sql query "warehouse-123" \
  "INSERT INTO high_value_transactions
   SELECT
     transaction_id,
     user_id,
     amount,
     timestamp
   FROM transaction_stream
   WHERE amount > 10000"
```

#### R2 SQL - Advanced Analytics

```bash
# Window functions for ranked queries
npx wrangler r2 sql query "warehouse-123" \
  "SELECT
     user_id,
     product_id,
     amount,
     ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) as purchase_rank
   FROM default.purchases
   QUALIFY purchase_rank <= 5"

# Time-series aggregations
npx wrangler r2 sql query "warehouse-123" \
  "SELECT
     DATE_TRUNC('hour', timestamp) as hour,
     COUNT(*) as event_count,
     AVG(response_time_ms) as avg_response_time
   FROM default.api_logs
   GROUP BY hour
   ORDER BY hour DESC
   LIMIT 24"

# Fraud detection pattern
npx wrangler r2 sql query "warehouse-123" \
  "SELECT
     user_id,
     COUNT(*) as transaction_count,
     SUM(CASE WHEN fraud_flag THEN 1 ELSE 0 END) as fraud_count,
     AVG(amount) as avg_amount
   FROM default.transactions
   WHERE timestamp >= CURRENT_DATE - INTERVAL '7' DAY
   GROUP BY user_id
   HAVING fraud_count > 0
   ORDER BY fraud_count DESC"
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **buckets.md** - Buckets documentation
- **getting_started.md** - Getting Started documentation
- **other.md** - Other documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
