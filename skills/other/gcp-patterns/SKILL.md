---
name: gcp-patterns
description: Cloud Run deployment, BigQuery optimization, Pub/Sub patterns, IAM best practices
---

# GCP Patterns

## Cloud Run Deployment

### Dockerfile for Cloud Run

```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER app
EXPOSE 8080
ENV PORT=8080 NODE_ENV=production
CMD ["node", "dist/server.js"]
```

### Cloud Run Service YAML

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: order-service
  annotations:
    run.googleapis.com/launch-stage: GA
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/startup-cpu-boost: "true"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      serviceAccountName: order-service@project-id.iam.gserviceaccount.com
      containers:
        - image: gcr.io/project-id/order-service:latest
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "2"
              memory: 1Gi
          env:
            - name: DB_CONNECTION
              valueFrom:
                secretKeyRef:
                  key: latest
                  name: db-connection-string
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 3
```

### Deploy Command

```bash
gcloud run deploy order-service \
  --image gcr.io/$PROJECT_ID/order-service:$GIT_SHA \
  --region us-central1 \
  --service-account order-service@$PROJECT_ID.iam.gserviceaccount.com \
  --set-secrets "DB_URL=db-connection:latest" \
  --min-instances 1 \
  --max-instances 100 \
  --cpu 2 --memory 1Gi \
  --concurrency 80 \
  --no-allow-unauthenticated
```

## BigQuery Optimization

```sql
-- Use partitioning and clustering
CREATE TABLE `project.dataset.events`
PARTITION BY DATE(event_timestamp)
CLUSTER BY user_id, event_type
AS SELECT * FROM `project.dataset.raw_events`;

-- Always filter on partition column
SELECT event_type, COUNT(*) as cnt
FROM `project.dataset.events`
WHERE event_timestamp BETWEEN '2025-01-01' AND '2025-01-31'
  AND event_type = 'purchase'
GROUP BY event_type;

-- Use approximate functions for large datasets
SELECT APPROX_COUNT_DISTINCT(user_id) as unique_users
FROM `project.dataset.events`
WHERE DATE(event_timestamp) = CURRENT_DATE();

-- Avoid SELECT * (scans all columns, costs more)
-- Use column selection and LIMIT for exploration
```

## Pub/Sub Patterns

```python
from google.cloud import pubsub_v1
from google.api_core import retry
import json

# Publisher with ordering and retry
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("project-id", "order-events")

def publish_event(event: dict, ordering_key: str = "") -> str:
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(
        topic_path,
        data,
        ordering_key=ordering_key,
        event_type=event["type"],
    )
    return future.result(timeout=30)

# Subscriber with exactly-once processing
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("project-id", "order-events-sub")

def callback(message: pubsub_v1.types.PubsubMessage) -> None:
    try:
        event = json.loads(message.data.decode("utf-8"))
        idempotency_key = message.message_id

        if already_processed(idempotency_key):
            message.ack()
            return

        process_event(event)
        mark_processed(idempotency_key)
        message.ack()
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        message.nack()

subscriber.subscribe(subscription_path, callback=callback)
```

## IAM Best Practices

```yaml
Principles:
  - Least privilege: grant minimum permissions needed
  - Service accounts per service (not shared)
  - No user accounts in production workloads
  - Prefer predefined roles over primitive roles

Per-Service Pattern:
  order-service:
    roles:
      - roles/cloudsql.client          # DB access
      - roles/pubsub.publisher         # Publish events
      - roles/secretmanager.secretAccessor  # Read secrets
    # NOT: roles/editor (too broad)

Workload Identity (GKE):
  - Bind K8s SA to GCP SA
  - No key files, automatic credential rotation
```

## Checklist

- [ ] Cloud Run services use dedicated service accounts
- [ ] Secrets stored in Secret Manager, not env vars
- [ ] BigQuery tables partitioned and clustered
- [ ] Pub/Sub subscribers implement idempotent processing
- [ ] Health check endpoints configured for all services
- [ ] Min instances set for latency-sensitive services
- [ ] IAM follows least privilege (no primitive roles)
- [ ] Cloud Armor WAF in front of public endpoints
- [ ] VPC connector for private resource access

## Anti-Patterns

- Using default compute service account (overprivileged)
- SELECT * on BigQuery (scans all columns, high cost)
- Pub/Sub without dead letter queue (messages lost on repeated failure)
- Hardcoding project ID instead of using environment detection
- Not setting concurrency limits on Cloud Run (OOM under load)
- Using Cloud Run for long-running background jobs (use Cloud Tasks)
- Storing secrets in environment variables instead of Secret Manager
