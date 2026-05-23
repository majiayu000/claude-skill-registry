---
name: llm-document-extraction
description: "Extract structured data from construction documents using LLMs. Process RFIs, submittals, contracts, specifications. Convert unstructured PDFs to structured JSON/Excel."
---

# LLM Document Extraction

## Overview

Construction documents (RFIs, submittals, specs, contracts) contain critical data trapped in unstructured formats. This skill uses LLMs to extract structured data automatically.

> "The construction industry is drowning in a flood of new data: the volume of information has grown from 15 zettabytes in 2015 to 181 zettabytes in 2025, and 90% of all existing data has been created in just the last few years." — Artem Boiko

## Use Cases

| Document Type | Extract |
|---------------|---------|
| RFI | Question, response, dates, parties |
| Submittal | Product specs, approval status, materials |
| Contract | Parties, amounts, dates, scope, clauses |
| Specification | Materials, standards, requirements |
| Daily Report | Weather, labor, equipment, progress |

## Quick Start

```python
from openai import OpenAI
import pdfplumber
import json

client = OpenAI()

def extract_from_pdf(pdf_path: str, extraction_schema: dict) -> dict:
    """Extract structured data from PDF using LLM"""

    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

    # Build extraction prompt
    prompt = f"""
    Extract the following information from this construction document.
    Return ONLY valid JSON matching the schema.

    Schema:
    {json.dumps(extraction_schema, indent=2)}

    Document:
    {text[:8000]}  # Truncate for context limits

    JSON Output:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a construction document analyst. Extract data accurately."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

## Extraction Schemas

### RFI Schema

```python
rfi_schema = {
    "rfi_number": "string",
    "date_submitted": "YYYY-MM-DD",
    "date_required": "YYYY-MM-DD",
    "from_company": "string",
    "to_company": "string",
    "subject": "string",
    "question": "string",
    "response": "string or null",
    "status": "open|closed|pending",
    "cost_impact": "boolean",
    "schedule_impact": "boolean",
    "attachments": ["list of attachment names"]
}

# Extract
rfi_data = extract_from_pdf("RFI-0042.pdf", rfi_schema)
```

### Submittal Schema

```python
submittal_schema = {
    "submittal_number": "string",
    "spec_section": "string",
    "description": "string",
    "manufacturer": "string",
    "product_name": "string",
    "model_number": "string",
    "submitted_by": "string",
    "date_submitted": "YYYY-MM-DD",
    "status": "approved|approved_as_noted|revise_resubmit|rejected",
    "reviewer_comments": "string or null",
    "materials": [
        {
            "name": "string",
            "specification": "string",
            "quantity": "string"
        }
    ]
}
```

### Contract Schema

```python
contract_schema = {
    "contract_number": "string",
    "project_name": "string",
    "owner": {
        "name": "string",
        "address": "string"
    },
    "contractor": {
        "name": "string",
        "address": "string"
    },
    "contract_amount": "number",
    "start_date": "YYYY-MM-DD",
    "completion_date": "YYYY-MM-DD",
    "liquidated_damages": "number per day",
    "retention_percentage": "number",
    "key_clauses": [
        {
            "clause_number": "string",
            "title": "string",
            "summary": "string"
        }
    ]
}
```

## Batch Processing with n8n

```json
{
  "workflow": "Document Extraction Pipeline",
  "trigger": "Watch folder for new PDFs",
  "nodes": [
    {
      "name": "Read PDF",
      "type": "Read Binary Files"
    },
    {
      "name": "Classify Document",
      "type": "AI Agent",
      "prompt": "Classify this document: RFI, Submittal, Contract, Spec, or Other"
    },
    {
      "name": "Route by Type",
      "type": "Switch",
      "rules": ["RFI", "Submittal", "Contract", "Spec"]
    },
    {
      "name": "Extract RFI",
      "type": "OpenAI",
      "schema": "rfi_schema"
    },
    {
      "name": "Extract Submittal",
      "type": "OpenAI",
      "schema": "submittal_schema"
    },
    {
      "name": "Save to Database",
      "type": "PostgreSQL",
      "operation": "insert"
    },
    {
      "name": "Update Dashboard",
      "type": "HTTP Request",
      "method": "POST"
    }
  ]
}
```

## Vision Model for Drawings

```python
import base64

def extract_from_drawing(image_path: str, query: str) -> str:
    """Extract information from drawings using vision model"""

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

# Example: Extract room areas from floor plan
areas = extract_from_drawing(
    "floor_plan.png",
    "List all rooms with their areas in square meters. Return as JSON."
)
```

## RAG for Large Documents

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

def create_document_index(pdf_path: str):
    """Create searchable index for large documents"""

    # Load and split
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    # Create vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Qdrant.from_documents(
        chunks,
        embeddings,
        collection_name="contract_docs"
    )

    return vectorstore

def query_document(vectorstore, question: str) -> str:
    """Query document with RAG"""

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)

    context = "\n".join(doc.page_content for doc in docs)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Answer based on the contract excerpts provided."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )

    return response.choices[0].message.content

# Usage
index = create_document_index("contract_100pages.pdf")
answer = query_document(index, "What are the liquidated damages terms?")
```

## Requirements

```bash
pip install openai pdfplumber langchain langchain-openai qdrant-client
```

## Resources

- OpenAI Vision: https://platform.openai.com/docs/guides/vision
- LangChain RAG: https://python.langchain.com/docs/tutorials/rag/
