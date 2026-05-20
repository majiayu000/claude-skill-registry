---
name: data-ai-ml
description: Build data pipelines, AI systems, and machine learning models with Python. USE THIS for data processing, model training, LLM integration, RAG systems, NLP, vector databases, prompt engineering, knowledge bases, data analysis, and AI/ML workflows. Include when user mentions AI, ML, data science, LLMs, embeddings, retrieval-augmented generation, or intelligent systems.
---

# Data, AI & ML Development Skill

Build intelligent systems, data pipelines, and machine learning solutions with Python and modern AI tools.

## Your Tech Stack

### Core Libraries
- **Python 3.9+**
- **LLM Integration**: OpenAI, Anthropic Claude, Ollama, LangChain
- **Data Processing**: Pandas, NumPy, Polars
- **NLP**: NLTK, spaCy, Transformers
- **Vector DB**: Pinecone, Weaviate, Chroma, FAISS, Milvus
- **ML Framework**: scikit-learn, PyTorch, TensorFlow
- **Data Viz**: Matplotlib, Plotly, Seaborn

### RAG Systems (Knowledge Bases)
- Document chunking and embedding
- Vector storage and retrieval
- Query augmentation
- Context ranking and reranking

## Workflow Patterns

### 1. Data Processing Pipeline
```python
import pandas as pd
import numpy as np

# ETL Pattern
def extract():
    """Load raw data"""
    return pd.read_csv('data.csv')

def transform(raw_data):
    """Clean and prepare"""
    data = raw_data.dropna()
    data['normalized'] = (data['value'] - data['value'].mean()) / data['value'].std()
    return data

def load(processed_data):
    """Store in database/warehouse"""
    processed_data.to_sql('processed', engine)

# Execute
raw = extract()
clean = transform(raw)
load(clean)
```

### 2. LLM Integration Pattern
```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define prompt with variables
template = """
Context: {context}
Question: {question}
Answer concisely:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# Chain it
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# Execute
result = chain.run(
    context="Legal statute XYZ...",
    question="What is the penalty?"
)
```

### 3. RAG (Retrieval-Augmented Generation) System
```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import JSONLLoader
from langchain.chat_models import ChatOpenAI

# 1. Load documents
loader = JSONLLoader(
    file_path='law_chunks.jsonl',
    jq_schema='.text'
)
documents = loader.load()

# 2. Create embeddings
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents,
    embeddings
)

# 3. Retriever + Generator
retriever = vectorstore.as_retriever(k=3)

def rag_query(question: str):
    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([d.page_content for d in docs])
    
    # Generate answer with context
    llm = ChatOpenAI()
    response = llm.predict(
        f"Context: {context}\n\nQ: {question}"
    )
    return response

answer = rag_query("What are penalties for contract breach?")
```

### 4. Prompt Engineering Best Practices
```python
# System prompt (role definition)
SYSTEM_PROMPT = """You are a legal AI assistant specializing in Moroccan law.
Your responses should be:
- Accurate and cited
- Clear and accessible
- Unbiased and neutral
- Specific to the jurisdiction
"""

# Few-shot examples
examples = [
    {
        "query": "What is a writ of habeas corpus?",
        "answer": "A writ of habeas corpus is a legal action..."
    },
    # More examples
]

# Dynamic prompting
def legal_consultation(question: str):
    prompt = f"""{SYSTEM_PROMPT}

Examples:
{format_examples(examples)}

User Question: {question}

Provide a detailed answer citing relevant articles:"""
    
    return llm.predict(prompt)
```

## Data Processing Patterns

### Chunking Strategy (for embeddings)
```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """Split text into overlapping chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# For structured data
import json

def load_and_chunk_jsonl(filepath: str):
    documents = []
    with open(filepath, 'r') as f:
        for line in f:
            doc = json.loads(line)
            chunks = chunk_text(doc['content'])
            documents.extend([
                {'id': f"{doc['id']}_chunk_{i}", 'content': c}
                for i, c in enumerate(chunks)
            ])
    return documents
```

### Data Validation
```python
from pydantic import BaseModel, validator

class LegalQuery(BaseModel):
    question: str
    jurisdiction: str  # e.g., "Morocco"
    context_type: str  # e.g., "criminal", "civil"
    
    @validator('question')
    def question_not_empty(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Question must be at least 3 characters')
        return v

# Use in API
def handle_query(data: dict):
    query = LegalQuery(**data)  # Auto-validates
    return process_legal_query(query)
```

## Model Training & Evaluation

### Classification Example
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Data preparation
X = features_df.drop('label', axis=1)
y = features_df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Training
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred)

print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1: {f1:.2%}")
```

## Deployment Patterns

### API with FastAPI
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

@app.post("/legal-query")
async def legal_question(request: QueryRequest):
    """Answer legal questions using RAG"""
    docs = retriever.get_relevant_documents(request.question)
    answer = generate_answer(request.question, docs)
    return {"answer": answer, "sources": [d.metadata for d in docs]}

# Run: uvicorn main:app --reload
```

### Batch Processing
```python
def batch_process_documents(source_path: str, batch_size: int = 100):
    """Process large document collections efficiently"""
    documents = load_jsonl(source_path)
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        processed = [process_doc(doc) for doc in batch]
        save_to_vector_db(processed)
        print(f"Processed batch {i//batch_size + 1}")

# Usage
batch_process_documents('law_chunks.jsonl')
```

## Performance Optimization

- **Caching**: Cache embeddings and frequent queries
- **Batch Processing**: Process documents in batches, not individually
- **Index Optimization**: Use appropriate vector database indexing
- **Query Optimization**: Filter documents before retrieval
- **Model Selection**: Choose lightweight models for lower latency

## Testing & Quality

```python
def test_rag_system():
    """Test RAG quality with known Q&A pairs"""
    test_cases = [
        {
            "query": "What is contract law?",
            "expected_keywords": ["agreement", "parties", "terms"]
        }
    ]
    
    for case in test_cases:
        result = rag_query(case["query"])
        has_keywords = any(kw in result.lower() for kw in case["expected_keywords"])
        assert has_keywords, f"Query failed: {case['query']}"
```

## Common Challenges

### Hallucination Prevention
- Use retrieval to ground responses
- Include confidence scores
- Cite sources
- Set temperature appropriately (0.3-0.5 for factual)

### Token Limits
- Chunk responses for long answers
- Summarize documents before passing to LLM
- Use compression techniques

### Quality Consistency
- Test with diverse queries
- Monitor metrics over time
- Maintain benchmark test sets
- Iterate on prompts based on feedback

---

**Output**: Production-ready AI systems with data pipelines, RAG capabilities, and intelligent reasoning.
