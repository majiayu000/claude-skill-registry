---
name: langchain-tools
description: LangChain framework utilities for chains, agents, and RAG
allowed-tools: [Bash, Read, Grep, Glob]
category: ai-tools
requires-env: []
optional-env: [LANGCHAIN_API_KEY, LANGCHAIN_TRACING_V2]
---

# LangChain Tools Skill

## Overview

The LangChain Tools skill provides configuration utilities and template generation for LangChain framework components, including chains, agents, RAG systems, and LangSmith tracing integration.

**Context Savings**: 90%+ reduction vs raw documentation by providing focused, task-specific interfaces to LangChain configurations.

**Use Cases**:

- Chain configuration and template generation
- Agent setup and tool integration
- Document loader configuration
- Vector store setup
- Embedding provider configuration
- LangSmith tracing and evaluation

**Important**: This skill helps configure LangChain components, not run them directly. Actual chain execution happens in application code.

## Requirements

**Python Dependencies**:

```bash
pip install langchain langchain-community langchain-openai
```

**Optional Dependencies** (based on use case):

```bash
# For OpenAI models
pip install openai

# For vector stores
pip install chromadb faiss-cpu pinecone-client

# For document loaders
pip install pypdf docx2txt

# For LangSmith tracing
pip install langsmith
```

**Installation Verification**:

```bash
python -c "import langchain; print(langchain.__version__)"
```

## Tools (Progressive Disclosure)

### Chain Utilities

| Tool               | Description                      | Example                    |
| ------------------ | -------------------------------- | -------------------------- |
| `list-chain-types` | List available chain types       | Show all chain types       |
| `chain-template`   | Get chain configuration template | Get LLMChain template      |
| `validate-chain`   | Validate chain configuration     | Validate chain config file |

### Agent Utilities

| Tool               | Description                      | Example                  |
| ------------------ | -------------------------------- | ------------------------ |
| `list-agent-types` | List available agent types       | Show all agent types     |
| `agent-template`   | Get agent configuration template | Get ReAct agent template |
| `list-tools`       | List available agent tools       | Show built-in tools      |

### Document Loaders

| Tool            | Description                       | Example               |
| --------------- | --------------------------------- | --------------------- |
| `list-loaders`  | List available document loaders   | Show all loader types |
| `loader-config` | Get loader configuration template | Get PDF loader config |

### Vector Stores

| Tool                 | Description                    | Example                |
| -------------------- | ------------------------------ | ---------------------- |
| `list-vectorstores`  | List vector store types        | Show all vector stores |
| `vectorstore-config` | Get vector store configuration | Get Chroma config      |

### Embeddings

| Tool               | Description                 | Example                      |
| ------------------ | --------------------------- | ---------------------------- |
| `list-embeddings`  | List embedding providers    | Show all embedding models    |
| `embedding-config` | Get embedding configuration | Get OpenAI embeddings config |

### LangSmith (Tracing)

| Tool            | Description              | Example             |
| --------------- | ------------------------ | ------------------- |
| `list-traces`   | List recent traces       | Show last 10 traces |
| `trace-details` | Get trace details        | Get trace by ID     |
| `list-datasets` | List evaluation datasets | Show all datasets   |

## Quick Reference

### Chain Types

```bash
# List available chain types
python -c "
from langchain.chains import (
    LLMChain,
    ConversationChain,
    SequentialChain,
    SimpleSequentialChain,
    MapReduceChain,
    RetrievalQA
)

print('Available Chain Types:')
print('- LLMChain: Basic chain with LLM and prompt')
print('- ConversationChain: Chat with memory')
print('- SequentialChain: Multiple chains in sequence')
print('- SimpleSequentialChain: Simple sequential chain')
print('- MapReduceChain: Map-reduce pattern')
print('- RetrievalQA: RAG question-answering')
"
```

### Create Basic LLM Chain

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Define prompt template
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Create LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Create chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run chain
result = chain.run(question="What is quantum computing?")
print(result)
```

### Agent Types

```bash
# List available agent types
python -c "
from langchain.agents import AgentType

print('Available Agent Types:')
print('- ZERO_SHOT_REACT_DESCRIPTION: ReAct agent with tool descriptions')
print('- CONVERSATIONAL_REACT_DESCRIPTION: Chat ReAct agent')
print('- CHAT_ZERO_SHOT_REACT_DESCRIPTION: Chat-optimized ReAct')
print('- STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION: Structured output ReAct')
print('- OPENAI_FUNCTIONS: OpenAI function calling agent')
print('- OPENAI_MULTI_FUNCTIONS: Multi-function OpenAI agent')
"
```

### Create ReAct Agent

```python
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import ChatOpenAI

# Create LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Load tools
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Create agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run agent
result = agent.run("What is the square root of 144?")
print(result)
```

### Document Loaders

```python
# PDF Loader
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Directory Loader
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader("./data", glob="**/*.txt")
documents = loader.load()

# Text Loader
from langchain.document_loaders import TextLoader

loader = TextLoader("document.txt")
documents = loader.load()

# Web Loader
from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
documents = loader.load()
```

### Vector Store Setup

```python
# Chroma Vector Store
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Create vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# FAISS Vector Store
from langchain.vectorstores import FAISS

vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

# Pinecone Vector Store
from langchain.vectorstores import Pinecone
import pinecone

pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

vectorstore = Pinecone.from_documents(
    documents=documents,
    embedding=embeddings,
    index_name="my-index"
)
```

### Embedding Providers

```python
# OpenAI Embeddings
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Hugging Face Embeddings
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Cohere Embeddings
from langchain.embeddings import CohereEmbeddings

embeddings = CohereEmbeddings(model="embed-english-v2.0")
```

### RAG System Setup

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load documents
loader = DirectoryLoader("./data", glob="**/*.txt")
documents = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
texts = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Create QA chain
llm = ChatOpenAI(temperature=0, model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Run query
result = qa_chain({"query": "What is the main topic?"})
print(result["result"])
print(result["source_documents"])
```

### LangSmith Tracing

```python
import os

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# Your LangChain code here
# All executions will be traced in LangSmith

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

template = "Tell me a joke about {topic}"
prompt = PromptTemplate(template=template, input_variables=["topic"])
llm = ChatOpenAI(temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt)

# This will be traced
result = chain.run(topic="programming")
```

## Configuration

### Environment Variables

| Variable               | Purpose                              | Default                           |
| ---------------------- | ------------------------------------ | --------------------------------- |
| `LANGCHAIN_API_KEY`    | LangSmith API key for tracing        | None                              |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing             | `false`                           |
| `LANGCHAIN_PROJECT`    | LangSmith project name               | `default`                         |
| `LANGCHAIN_ENDPOINT`   | Custom LangSmith endpoint            | `https://api.smith.langchain.com` |
| `OPENAI_API_KEY`       | OpenAI API key for models/embeddings | None                              |

### LangSmith Setup

```bash
# Method 1: Environment variables
export LANGCHAIN_API_KEY="your-api-key"
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="my-project"

# Method 2: Python configuration
from langsmith import Client

client = Client(api_key="your-api-key")
```

### Chain Configuration Template

```python
# config/chain_config.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

class ChainConfig:
    """Base chain configuration"""

    def __init__(self, temperature=0, model="gpt-4"):
        self.temperature = temperature
        self.model = model

    def create_llm(self):
        return ChatOpenAI(
            temperature=self.temperature,
            model=self.model
        )

    def create_chain(self, template, input_variables):
        prompt = PromptTemplate(
            template=template,
            input_variables=input_variables
        )
        llm = self.create_llm()
        return LLMChain(llm=llm, prompt=prompt)
```

## Agent Integration

### Primary Agents

| Agent             | Use Case                                                |
| ----------------- | ------------------------------------------------------- |
| **llm-architect** | LangChain system design, RAG architecture, agent design |
| **developer**     | Chain implementation, agent integration, RAG setup      |
| **architect**     | System architecture, integration patterns               |

### Secondary Agents

| Agent                    | Use Case                                     |
| ------------------------ | -------------------------------------------- |
| **qa**                   | Chain testing, agent validation              |
| **performance-engineer** | Chain optimization, embedding performance    |
| **security-architect**   | Security review, prompt injection prevention |

### Integration Pattern

```python
# LLM Architect: Design RAG system
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

# Define architecture
architecture = {
    "loader": "DirectoryLoader",
    "splitter": "RecursiveCharacterTextSplitter",
    "embeddings": "OpenAIEmbeddings",
    "vectorstore": "Chroma",
    "chain_type": "stuff",
    "retriever": {"k": 3}
}

# Developer: Implement RAG system
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

loader = DirectoryLoader("./data", glob="**/*.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(temperature=0, model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# QA: Test RAG system
test_queries = [
    "What is the main topic?",
    "Summarize the key points",
    "What are the conclusions?"
]

for query in test_queries:
    result = qa_chain({"query": query})
    print(f"Query: {query}")
    print(f"Answer: {result['result']}")
    print("---")
```

## Examples

### Example 1: Simple Question-Answering Chain

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Define prompt
template = """You are a helpful assistant. Answer the following question concisely.

Question: {question}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Create chain
llm = ChatOpenAI(temperature=0, model="gpt-4")
chain = LLMChain(llm=llm, prompt=prompt)

# Run chain
questions = [
    "What is machine learning?",
    "Explain neural networks",
    "What is transfer learning?"
]

for question in questions:
    result = chain.run(question=question)
    print(f"Q: {question}")
    print(f"A: {result}\n")
```

### Example 2: Conversational Agent with Memory

```python
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

# Create LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Load tools
tools = load_tools(["llm-math"], llm=llm)

# Create memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Conversation
agent.run("What is 25 * 4?")
agent.run("Add 10 to the previous result")
agent.run("What was the first calculation I asked?")
```

### Example 3: Document Q&A with Sources

```python
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Load document
loader = TextLoader("document.txt")
documents = loader.load()

# Split text
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)

# Create QA chain
llm = ChatOpenAI(temperature=0, model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Query with sources
result = qa_chain({"query": "What are the key findings?"})
print(f"Answer: {result['result']}\n")
print("Sources:")
for doc in result['source_documents']:
    print(f"- {doc.page_content[:100]}...")
```

### Example 4: Custom Tool Agent

```python
from langchain.agents import Tool, AgentType, initialize_agent
from langchain_openai import ChatOpenAI

# Define custom tools
def get_weather(location: str) -> str:
    """Get weather for a location"""
    return f"The weather in {location} is sunny and 72°F"

def calculate_tip(bill: str) -> str:
    """Calculate 20% tip for a bill"""
    amount = float(bill)
    tip = amount * 0.20
    return f"20% tip on ${amount:.2f} is ${tip:.2f}"

tools = [
    Tool(
        name="Weather",
        func=get_weather,
        description="Get weather for a location. Input should be a city name."
    ),
    Tool(
        name="TipCalculator",
        func=calculate_tip,
        description="Calculate 20% tip. Input should be the bill amount."
    )
]

# Create agent
llm = ChatOpenAI(temperature=0, model="gpt-4")
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use agent
agent.run("What's the weather in San Francisco?")
agent.run("Calculate tip for a $50 bill")
```

### Example 5: Multi-Step Chain

```python
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.7, model="gpt-4")

# First chain: Generate topic
topic_template = "Generate a topic for a blog post about {subject}"
topic_prompt = PromptTemplate(template=topic_template, input_variables=["subject"])
topic_chain = LLMChain(llm=llm, prompt=topic_prompt, output_key="topic")

# Second chain: Generate outline
outline_template = "Create an outline for a blog post about: {topic}"
outline_prompt = PromptTemplate(template=outline_template, input_variables=["topic"])
outline_chain = LLMChain(llm=llm, prompt=outline_prompt, output_key="outline")

# Third chain: Write introduction
intro_template = "Write an introduction for this outline:\n{outline}"
intro_prompt = PromptTemplate(template=intro_template, input_variables=["outline"])
intro_chain = LLMChain(llm=llm, prompt=intro_prompt, output_key="introduction")

# Combine chains
overall_chain = SequentialChain(
    chains=[topic_chain, outline_chain, intro_chain],
    input_variables=["subject"],
    output_variables=["topic", "outline", "introduction"],
    verbose=True
)

# Run sequential chain
result = overall_chain({"subject": "artificial intelligence"})
print(f"Topic: {result['topic']}")
print(f"\nOutline: {result['outline']}")
print(f"\nIntroduction: {result['introduction']}")
```

## Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'langchain'`

```bash
# Solution: Install the package
pip install langchain langchain-community langchain-openai
```

**Issue**: `ValueError: Did not find openai_api_key`

```bash
# Solution: Set API key
export OPENAI_API_KEY="your-api-key"

# Or in code
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

**Issue**: `ChromaDB connection error`

```bash
# Solution: Install ChromaDB
pip install chromadb

# Or use in-memory mode
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings
    # No persist_directory = in-memory
)
```

**Issue**: Agent stuck in loop or gives poor results

```python
# Solution: Adjust temperature and add max_iterations
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent

llm = ChatOpenAI(temperature=0, model="gpt-4")  # Lower temperature

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=5,  # Limit iterations
    early_stopping_method="generate",  # Force generation
    verbose=True
)
```

**Issue**: Memory errors with large documents

```python
# Solution: Use smaller chunk sizes and streaming
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Smaller chunks
    chunk_overlap=50
)

# Or use streaming for vector store
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=texts[:100],  # Process in batches
    embedding=embeddings
)
```

**Issue**: LangSmith traces not appearing

```bash
# Solution: Verify environment variables
echo $LANGCHAIN_TRACING_V2  # Should be "true"
echo $LANGCHAIN_API_KEY      # Should be your API key
echo $LANGCHAIN_PROJECT      # Should be your project name

# Check connection
python -c "from langsmith import Client; client = Client(); print('Connected')"
```

### Debug Mode

```python
# Enable verbose logging
import logging

logging.basicConfig(level=logging.DEBUG)

# Enable chain verbose mode
from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# Enable agent verbose mode
from langchain.agents import initialize_agent

agent = initialize_agent(tools, llm, verbose=True)
```

### Verify Installation

```bash
# Check package versions
pip list | grep -E "langchain|openai|chromadb"

# Test basic functionality
python -c "
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

print('LangChain installation verified')
"
```

## Best Practices

1. **Use environment variables**: Store API keys securely in environment variables
2. **Enable tracing**: Use LangSmith for debugging and monitoring production chains
3. **Optimize chunk sizes**: Balance chunk size between context and granularity (500-1000 chars)
4. **Use appropriate embeddings**: Choose embeddings based on use case (ada-002 for general, sentence-transformers for local)
5. **Implement error handling**: Add retries and fallbacks for API calls
6. **Cache vector stores**: Persist vector stores to disk to avoid recomputing embeddings
7. **Monitor token usage**: Track token consumption for cost optimization
8. **Version control prompts**: Store prompt templates in version control

## Related Skills

- **huggingface-hub**: Alternative embedding providers and models
- **repo-rag**: Search codebase for existing LangChain patterns
- **evaluator**: Evaluate chain outputs and agent performance
- **test-generator**: Generate tests for chains and agents
- **dependency-analyzer**: Check for compatibility issues

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangChain Agent Documentation](https://python.langchain.com/docs/modules/agents/)
- [LangChain Chains Documentation](https://python.langchain.com/docs/modules/chains/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates)
