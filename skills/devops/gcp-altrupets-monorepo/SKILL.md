# ☁️ Skill: Google Cloud Platform Backend

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-gcp` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `gcp`, `gke`, `cloud-run`, `cloud-sql`, `firebase` |

## 🔑 Keywords

- `gcp`, `google-cloud`, `gke`, `cloud-run`, `cloud-sql`, `firebase`, `@skill:gcp`

## 📖 Descripción

GCP ofrece servicios cloud para backends Flutter: GKE (Kubernetes), Cloud Run (serverless containers), Cloud SQL, Firebase, Cloud Storage y más.

## 💻 Servicios Principales

### 1. GKE (Google Kubernetes Engine)

```bash
# Crear cluster
gcloud container clusters create myapp-prod \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 10 \
  --enable-autorepair \
  --enable-autoupgrade

# Configure kubectl
gcloud container clusters get-credentials myapp-prod --zone us-central1-a
```

### 2. Cloud Run (Serverless Containers)

```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp-backend
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containers:
      - image: gcr.io/myproject/backend:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: 512Mi
            cpu: "1"
```

```bash
# Deploy
gcloud run deploy myapp-backend \
  --image gcr.io/myproject/backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --max-instances 10
```

### 3. Cloud SQL (PostgreSQL)

```bash
# Create instance
gcloud sql instances create myapp-db \
  --database-version=POSTGRES_15 \
  --tier=db-g1-small \
  --region=us-central1 \
  --backup \
  --backup-start-time=03:00 \
  --enable-bin-log \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=04

# Create database
gcloud sql databases create myapp_prod --instance=myapp-db

# Create user
gcloud sql users create admin \
  --instance=myapp-db \
  --password=SecurePassword123!
```

### 4. Cloud Storage

```bash
# Create bucket
gsutil mb -l us-central1 gs://myapp-storage-prod

# Set CORS
echo '[
  {
    "origin": ["*"],
    "method": ["GET", "POST", "PUT"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]' > cors.json

gsutil cors set cors.json gs://myapp-storage-prod
```

### 5. Firebase Integration

```bash
# Initialize Firebase
firebase init

# Deploy Functions
firebase deploy --only functions

# Deploy Firestore rules
firebase deploy --only firestore:rules

# Deploy Hosting
firebase deploy --only hosting
```

## 🎯 Mejores Prácticas

1. Use **GKE Autopilot** para managed Kubernetes
2. **Cloud Run** para cargas serverless
3. **Cloud SQL Proxy** para conexiones seguras
4. **Secret Manager** para credentials
5. **Cloud Monitoring** para observability
6. **IAM roles** granulares
7. **Cloud Armor** para DDoS protection

## 📚 Recursos

- [GCP Documentation](https://cloud.google.com/docs)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)

---

**Versión:** 1.0.0
