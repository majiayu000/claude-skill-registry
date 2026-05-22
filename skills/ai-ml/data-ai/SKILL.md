---
name: data-ai-guide
description: Comprehensive data science, machine learning, and AI guide covering Python, deep learning, NLP, LLMs, prompt engineering, and MLOps. Use when building AI models, data pipelines, or machine learning systems.
sasmp_version: "1.3.0"
bonded_agent: 04-data-ai-specialist
bond_type: PRIMARY_BOND
eqhm_enabled: true
---

# Data Science & AI Guide

Master data science, machine learning, generative AI, and modern AI engineering practices.

## Quick Start

### Python Data Science Stack
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load and prepare data
df = pd.read_csv('data.csv')
X = df.drop('target', axis=1)
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
```

### Deep Learning with PyTorch
```python
import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(784, 128)
        self.linear2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        return self.linear2(x)

# Training loop
model = SimpleNN()
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()
```

### LLM Prompt Engineering
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning?"}
  ],
  temperature=0.7
)
```

## Data Science Path

### Fundamentals
- **Mathematics**: Statistics, linear algebra, calculus
- **Python**: Libraries (Pandas, NumPy, Scikit-learn)
- **Data Analysis**: Exploratory analysis, visualization
- **SQL**: Querying and data manipulation

### Machine Learning
- **Supervised Learning**: Regression, classification
- **Unsupervised Learning**: Clustering, dimensionality reduction
- **Model Evaluation**: Cross-validation, metrics
- **Hyperparameter Tuning**: Grid search, Bayesian optimization

### Deep Learning
- **Neural Networks**: Architecture, training
- **CNNs**: Computer vision tasks
- **RNNs**: Sequence modeling
- **Transformers**: Modern architecture for NLP/Vision

### Natural Language Processing
- **Text Processing**: Tokenization, embeddings
- **Word Embeddings**: Word2Vec, GloVe, FastText
- **BERT**: Contextual embeddings
- **Transformers**: GPT, BERT for various NLP tasks

## Generative AI & LLMs

### Large Language Models
- **GPT Family**: GPT-3.5, GPT-4 for text generation
- **Claude**: Constitutional AI models
- **Open Source**: Llama, Mistral, Zephyr
- **Fine-tuning**: Adapting models for specific tasks

### Prompt Engineering
- **Role-based Prompting**: Setting context and expertise
- **Few-shot Learning**: Examples in prompt
- **Chain-of-Thought**: Step-by-step reasoning
- **Retrieval Augmented Generation (RAG)**: Knowledge augmentation

```python
# RAG Example
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

qa = RetrievalQA.from_chain_type(
  llm=llm,
  chain_type="stuff",
  retriever=vectorstore.as_retriever()
)
```

### AI Agents
- **Tool Use**: Agents calling external tools
- **Planning**: Multi-step task execution
- **Memory**: Conversation history, context
- **Evaluation**: Assessing agent performance

## Data Engineering

### ETL Pipelines
- **Apache Airflow**: Workflow orchestration
- **dbt**: Data transformation
- **Kafka**: Stream processing
- **Spark**: Distributed processing

### Big Data
- **Hadoop**: Distributed storage and processing
- **Spark**: In-memory processing framework
- **Scala**: Spark's native language
- **Distributed Systems**: Understanding CAP theorem

### Data Warehousing
- **Snowflake**: Cloud data warehouse
- **BigQuery**: Google's data warehouse
- **Redshift**: AWS data warehouse
- **Star Schema**: Dimensional modeling

## MLOps

### Model Management
- **Model Versioning**: Tracking model versions
- **Model Registry**: MLflow, Weights & Biases
- **Experiment Tracking**: Monitoring training runs
- **Model Cards**: Documenting model capabilities

### Deployment
- **Model Serving**: FastAPI, TFServing
- **Containerization**: Docker for models
- **Kubernetes**: Production ML deployment
- **API Monitoring**: Performance and data drift

### Monitoring
- **Data Drift**: Detecting distribution changes
- **Model Drift**: Performance degradation
- **Feature Store**: Consistent feature serving
- **Observability**: Logging and metrics

## Technology Stack

### Core Libraries
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning
- **Matplotlib/Seaborn**: Visualization
- **Plotly**: Interactive plots

### Deep Learning
- **TensorFlow**: Keras API, distributed training
- **PyTorch**: Dynamic graphs, research-friendly
- **JAX**: Functional programming for ML

### LLM Frameworks
- **LangChain**: Building LLM applications
- **LlamaIndex**: RAG and indexing
- **OpenAI API**: GPT models access
- **Hugging Face**: Model hub and transformers

## Learning Path

1. **Fundamentals** (3 months)
   - Python programming
   - Statistics and mathematics
   - Data manipulation with Pandas

2. **Machine Learning** (3 months)
   - Supervised learning
   - Model evaluation
   - Feature engineering

3. **Deep Learning** (2 months)
   - Neural networks
   - CNNs and RNNs
   - Transformers

4. **Specialization** (ongoing)
   - NLP / Computer Vision / Tabular Data
   - LLMs and generative AI
   - MLOps and production

## Projects

1. **Iris Classification** - Classic ML project
2. **Housing Price Prediction** - Regression
3. **Sentiment Analysis** - NLP with transformers
4. **Image Classification** - CNN with deep learning
5. **LLM Chatbot** - Using prompt engineering
6. **RAG System** - Knowledge-augmented AI
7. **Time Series Forecasting** - Stock predictions

## Resources

### Learning Platforms
- **Coursera**: Andrew Ng's ML course
- **Fast.ai**: Practical deep learning
- **DataCamp**: Interactive data science
- **Kaggle**: Competitions and datasets

### Documentation
- [Scikit-learn](https://scikit-learn.org/)
- [PyTorch](https://pytorch.org/)
- [Hugging Face](https://huggingface.co/)
- [OpenAI API](https://platform.openai.com/)

**Roadmap.sh Reference**: https://roadmap.sh/ai-engineer

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 04-data-ai-specialist
