---
name: gcp-expert
version: 1.0.0
description: Expert-level Google Cloud Platform, services, and cloud architecture
category: cloud
tags: [gcp, google-cloud, cloud-functions, bigquery, firestore]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(gcloud:*)
---

# Google Cloud Platform Expert

Expert guidance for Google Cloud Platform services and cloud-native architecture.

## Core Concepts

- Compute Engine, App Engine, Cloud Run
- Cloud Functions (serverless)
- Cloud Storage
- BigQuery (data warehouse)
- Firestore (NoSQL database)
- Pub/Sub (messaging)
- Google Kubernetes Engine (GKE)

## gcloud CLI

```bash
# Initialize
gcloud init

# Create Compute Engine instance
gcloud compute instances create my-instance \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud

# Deploy App Engine
gcloud app deploy

# Create Cloud Storage bucket
gsutil mb gs://my-bucket-name/

# Upload file
gsutil cp myfile.txt gs://my-bucket-name/
```

## Cloud Functions

```python
import functions_framework
from google.cloud import firestore

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    name = request_json.get('name') if request_json else 'World'

    return f'Hello {name}!'

@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    import base64
    data = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    print(f'Received: {data}')
```

## BigQuery

```python
from google.cloud import bigquery

client = bigquery.Client()

# Query
query = """
    SELECT name, COUNT(*) as count
    FROM `project.dataset.table`
    WHERE date >= '2024-01-01'
    GROUP BY name
    ORDER BY count DESC
    LIMIT 10
"""

query_job = client.query(query)
results = query_job.result()

for row in results:
    print(f"{row.name}: {row.count}")

# Load data
dataset_id = 'my_dataset'
table_id = 'my_table'
table_ref = client.dataset(dataset_id).table(table_id)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True
)

with open('data.csv', 'rb') as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()
```

## Firestore

```python
from google.cloud import firestore

db = firestore.Client()

# Create document
doc_ref = db.collection('users').document('user1')
doc_ref.set({
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# Query
users_ref = db.collection('users')
query = users_ref.where('age', '>=', 18).limit(10)

for doc in query.stream():
    print(f'{doc.id} => {doc.to_dict()}')

# Real-time listener
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document: {doc.id}')

doc_ref.on_snapshot(on_snapshot)
```

## Pub/Sub

```python
from google.cloud import pubsub_v1

# Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'topic-name')

data = "Hello World".encode('utf-8')
future = publisher.publish(topic_path, data)
print(f'Published message ID: {future.result()}')

# Subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('project-id', 'subscription-name')

def callback(message):
    print(f'Received: {message.data.decode("utf-8")}')
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
```

## Best Practices

- Use service accounts
- Implement IAM properly
- Use Cloud Storage lifecycle policies
- Monitor with Cloud Monitoring
- Use managed services
- Implement auto-scaling
- Optimize BigQuery costs

## Anti-Patterns

❌ No IAM policies
❌ Storing credentials in code
❌ Ignoring costs
❌ Single region deployments
❌ No data backup
❌ Overly broad permissions

## Resources

- GCP Documentation: https://cloud.google.com/docs
- gcloud CLI: https://cloud.google.com/sdk/gcloud
