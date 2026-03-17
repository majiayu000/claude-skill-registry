---
name: ml-engineer
description: Expert in building scalable ML systems, from data pipelines and model training to production deployment and monitoring.
---

# Machine Learning Engineer

## Purpose

Provides MLOps and production ML engineering expertise specializing in end-to-end ML pipelines, model deployment, and infrastructure automation. Bridges data science and production engineering with robust, scalable machine learning systems.

## When to Use

- Building end-to-end ML pipelines (Data → Train → Validate → Deploy)
- Deploying models to production (Real-time API, Batch, or Edge)
- Implementing MLOps practices (CI/CD for ML, Experiment Tracking)
- Optimizing model performance (Latency, Throughput, Resource usage)
- Setting up feature stores and model registries
- Implementing model monitoring (Drift detection, Performance tracking)
- Scaling training workloads (Distributed training)

---
---

## 2. Decision Framework

### Model Serving Strategy

```
Need to serve predictions?
│
├─ Real-time (Low Latency)?
│  │
│  ├─ High Throughput? → **Kubernetes (KServe/Seldon)**
│  ├─ Low/Medium Traffic? → **Serverless (Lambda/Cloud Run)**
│  └─ Ultra-low latency (<10ms)? → **C++/Rust Inference Server (Triton)**
│
├─ Batch Processing?
│  │
│  ├─ Large Scale? → **Spark / Ray**
│  └─ Scheduled Jobs? → **Airflow / Prefect**
│
└─ Edge / Client-side?
   │
   ├─ Mobile? → **TFLite / CoreML**
   └─ Browser? → **TensorFlow.js / ONNX Runtime Web**
```

### Training Infrastructure

```
Training Environment?
│
├─ Single Node?
│  │
│  ├─ Interactive? → **JupyterHub / SageMaker Notebooks**
│  └─ Automated? → **Docker Container on VM**
│
└─ Distributed?
   │
   ├─ Data Parallelism? → **Ray Train / PyTorch DDP**
   └─ Pipeline orchestration? → **Kubeflow / Airflow / Vertex AI**
```

### Feature Store Decision

| Need | Recommendation | Rationale |
|------|----------------|-----------|
| **Simple / MVP** | **No Feature Store** | Use SQL/Parquet files. Overhead of FS is too high. |
| **Team Consistency** | **Feast** | Open source, manages online/offline consistency. |
| **Enterprise / Managed** | **Tecton / Hopsworks** | Full governance, lineage, managed SLA. |
| **Cloud Native** | **Vertex/SageMaker FS** | Tight integration if already in that cloud ecosystem. |

**Red Flags → Escalate to `oracle`:**
- "Real-time" training requirements (online learning) without massive infrastructure budget
- Deploying LLMs (7B+ params) on CPU-only infrastructure
- Training on PII/PHI data without privacy-preserving techniques (Federated Learning, Differential Privacy)
- No validation set or "ground truth" feedback loop mechanism

---
---

## 3. Core Workflows

### Workflow 1: End-to-End Training Pipeline

**Goal:** Automate model training, validation, and registration using MLflow.

**Steps:**

1.  **Setup Tracking**
    ```python
    import mlflow
    import mlflow.sklearn
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, precision_score

    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("churn-prediction-prod")
    ```

2.  **Training Script (`train.py`)**
    ```python
    def train(max_depth, n_estimators):
        with mlflow.start_run():
            # Log params
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_param("n_estimators", n_estimators)
            
            # Train
            model = RandomForestClassifier(
                max_depth=max_depth, 
                n_estimators=n_estimators,
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Evaluate
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds)
            
            # Log metrics
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            
            # Log model artifact with signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(X_train, preds)
            
            mlflow.sklearn.log_model(
                model, 
                "model",
                signature=signature,
                registered_model_name="churn-model"
            )
            
            print(f"Run ID: {mlflow.active_run().info.run_id}")
    
    if __name__ == "__main__":
        train(max_depth=5, n_estimators=100)
    ```

3.  **Pipeline Orchestration (Bash/Airflow)**
    ```bash
    #!/bin/bash
    # Run training
    python train.py
    
    # Check if model passed threshold (e.g. via MLflow API)
    # If yes, transition to Staging
    ```

---
---

### Workflow 3: Drift Detection (Monitoring)

**Goal:** Detect if production data distribution has shifted from training data.

**Steps:**

1.  **Baseline Generation (During Training)**
    ```python
    import evidently
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset

    # Calculate baseline profile on training data
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=train_df, current_data=test_df)
    report.save_json("baseline_drift.json")
    ```

2.  **Production Monitoring Job**
    ```python
    # Scheduled daily job
    def check_drift():
        # Load production logs (last 24h)
        current_data = load_production_logs()
        reference_data = load_training_data()
        
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=reference_data, current_data=current_data)
        
        result = report.as_dict()
        dataset_drift = result['metrics'][0]['result']['dataset_drift']
        
        if dataset_drift:
            trigger_alert("Data Drift Detected!")
            trigger_retraining()
    ```

---
---

### Workflow 5: RAG Pipeline with Vector Database

**Goal:** Build a production retrieval pipeline using Pinecone/Weaviate and LangChain.

**Steps:**

1.  **Ingestion (Chunking & Embedding)**
    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_pinecone import PineconeVectorStore
    
    # Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(raw_documents)
    
    # Embedding & Indexing
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore.from_documents(
        docs, 
        embeddings, 
        index_name="knowledge-base"
    )
    ```

2.  **Retrieval & Generation**
    ```python
    from langchain.chains import RetrievalQA
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
    )
    
    response = qa_chain.invoke("How do I reset my password?")
    print(response['result'])
    ```

3.  **Optimization (Hybrid Search)**
    -   Combine **Dense Retrieval** (Vectors) with **Sparse Retrieval** (BM25/Keywords).
    -   Use **Reranking** (Cohere/Cross-Encoder) on the top 20 results to select best 5.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Training-Serving Skew

**What it looks like:**
-   Feature logic implemented in SQL for training, but re-implemented in Java/Python for serving.
-   "Mean imputation" value calculated on training set but not saved; serving uses a different default.

**Why it fails:**
-   Model behaves unpredictably in production.
-   Debugging is extremely difficult.

**Correct approach:**
-   Use a **Feature Store** or shared library for transformations.
-   Wrap preprocessing logic **inside** the model artifact (e.g., Scikit-Learn Pipeline, TensorFlow Transform).

### ❌ Anti-Pattern 2: Manual Deployments

**What it looks like:**
-   Data Scientist emails a `.pkl` file to an engineer.
-   Engineer manually copies it to a server and restarts the flask app.

**Why it fails:**
-   No version control.
-   No reproducibility.
-   High risk of human error.

**Correct approach:**
-   **CI/CD Pipeline:** Git push triggers build → test → deploy.
-   **Model Registry:** Deploy specific version hash from registry.

### ❌ Anti-Pattern 3: Silent Failures

**What it looks like:**
-   Model API returns `200 OK` but prediction is garbage because input data was corrupted (e.g., all Nulls).
-   Model returns default class `0` for everything.

**Why it fails:**
-   Application keeps running, but business value is lost.
-   Incident detected weeks later by business stakeholders.

**Correct approach:**
-   **Input Schema Validation:** Reject bad requests (Pydantic/TFX).
-   **Output Monitoring:** Alert if prediction distribution shifts (e.g., if model predicts "Fraud" 0% of time for 1 hour).

---
---

## 7. Quality Checklist

**Reliability:**
-   [ ] **Health Checks:** `/health` endpoint implemented (liveness/readiness).
-   [ ] **Retries:** Client has retry logic with exponential backoff.
-   [ ] **Fallback:** Default heuristic exists if model fails or times out.
-   [ ] **Validation:** Inputs validated against schema before inference.

**Performance:**
-   [ ] **Latency:** P99 latency meets SLA (e.g., < 100ms).
-   [ ] **Throughput:** System autoscales with load.
-   [ ] **Batching:** Inference requests batched if using GPU.
-   [ ] **Image Size:** Docker image optimized (slim base, multi-stage build).

**Reproducibility:**
-   [ ] **Versioning:** Code, Data, and Model versions linked.
-   [ ] **Artifacts:** Saved in object storage (S3/GCS), not local disk.
-   [ ] **Environment:** Dependencies pinned (`requirements.txt` / `conda.yaml`).

**Monitoring:**
-   [ ] **Technical:** Latency, Error Rate, CPU/Memory/GPU usage.
-   [ ] **Functional:** Prediction distribution, Input data drift.
-   [ ] **Business:** (If possible) Attribution of prediction to outcome.

## Anti-Patterns

### Training-Serving Skew

- **Problem**: Feature logic differs between training and serving environments
- **Symptoms**: Model performs well in testing but poorly in production
- **Solution**: Use feature stores or embed preprocessing in model artifacts
- **Warning Signs**: Different code paths for feature computation, hardcoded constants

### Manual Deployment

- **Problem**: Deploying models without automation or version control
- **Symptoms**: No traceability, human errors, deployment failures
- **Solution**: Implement CI/CD pipelines with model registry integration
- **Warning Signs**: Email/file transfers of model files, manual server restarts

### Silent Failures

- **Problem**: Model failures go undetected
- **Symptoms**: Bad predictions returned without error indication
- **Solution**: Implement input validation, output monitoring, and alerting
- **Warning Signs**: 200 OK responses with garbage data, no anomaly detection

### Data Leakage

- **Problem**: Training data contains information not available at prediction time
- **Symptoms**: Unrealistically high training accuracy, poor generalization
- **Solution**: Careful feature engineering and validation split review
- **Warning Signs**: Features that would only be known after prediction
