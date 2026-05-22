---
name: langchain
description: Build production-ready LLM applications with chains, agents, memory, tools, and RAG pipelines using the LangChain framework
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
  - chain_composition
  - agent_orchestration
  - memory_management
  - tool_integration
  - rag_pipelines
  - vector_stores
  - document_processing
  - streaming_responses
tools:
  - Read
  - Write
  - Bash
  - Grep
tags: [langchain, llm, chains, agents, rag, embeddings, vector-stores, memory, tools]
platforms: [python]
related_skills:
  - prompt-engineering
  - dspy
  - pandasai
---

# LangChain Skill

> Build production-ready LLM-powered applications with chains, agents, memory, and RAG pipelines.

## Quick Start

```bash
# Install LangChain ecosystem
pip install langchain langchain-openai langchain-community langchain-core

# Install vector store dependencies
pip install chromadb faiss-cpu

# Install document loaders
pip install unstructured pypdf docx2txt

# Set API key
export OPENAI_API_KEY="your-api-key"
```

## When to Use This Skill

**USE when:**
- Building complex LLM applications with multiple components
- Need agents that can use tools and make autonomous decisions
- Implementing RAG (Retrieval Augmented Generation) systems
- Integrating with various LLM providers (OpenAI, Anthropic, local models)
- Building chatbots with conversation memory
- Processing and querying document collections
- Need streaming responses for real-time applications
- Orchestrating multi-step reasoning workflows

**DON'T USE when:**
- Simple single-prompt LLM calls (use direct API)
- Optimizing prompts programmatically (use DSPy instead)
- Building UI-focused chat applications (use Streamlit/Gradio directly)
- Need minimal dependencies and maximum control
- Performance-critical applications requiring custom optimizations

## Prerequisites

```bash
# Core installation
pip install langchain>=0.2.0 langchain-openai>=0.1.0 langchain-core>=0.2.0

# For RAG applications
pip install chromadb>=0.4.0 faiss-cpu>=1.7.0

# For document processing
pip install unstructured>=0.10.0 pypdf>=3.0.0

# For web search and tools
pip install duckduckgo-search wikipedia arxiv

# Optional: Local LLMs
pip install langchain-community ollama

# Environment setup
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Core Capabilities

### 1. Basic Chain Composition

**Simple LLM Chain:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_simple_chain(
    model: str = "gpt-4",
    temperature: float = 0.7
):
    """
    Create a simple prompt-model-output chain.

    Args:
        model: Model name to use
        temperature: Sampling temperature

    Returns:
        Runnable chain that accepts dict input
    """
    # Define prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant specializing in {domain}."),
        ("human", "{question}")
    ])

    # Initialize LLM
    llm = ChatOpenAI(model=model, temperature=temperature)

    # Create chain with LCEL (LangChain Expression Language)
    chain = prompt | llm | StrOutputParser()

    return chain

# Usage
chain = create_simple_chain(model="gpt-4", temperature=0.3)

response = chain.invoke({
    "domain": "marine engineering",
    "question": "What are the key factors in mooring system design?"
})

print(response)
```

**Sequential Chain with Multiple Steps:**
```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def create_analysis_chain():
    """
    Create a multi-step analysis chain:
    1. Extract key points
    2. Analyze implications
    3. Generate recommendations
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)

    # Step 1: Extract key points
    extract_prompt = ChatPromptTemplate.from_template(
        "Extract the 5 most important points from this text:\n\n{text}\n\nKey Points:"
    )

    # Step 2: Analyze implications
    analyze_prompt = ChatPromptTemplate.from_template(
        "Based on these key points:\n{key_points}\n\n"
        "What are the main implications and potential risks?"
    )

    # Step 3: Generate recommendations
    recommend_prompt = ChatPromptTemplate.from_template(
        "Given these key points:\n{key_points}\n\n"
        "And this analysis:\n{analysis}\n\n"
        "Provide 3-5 actionable recommendations."
    )

    # Build chain
    chain = (
        {"text": RunnablePassthrough()}
        | RunnableParallel(
            text=RunnablePassthrough(),
            key_points=extract_prompt | llm | StrOutputParser()
        )
        | RunnableParallel(
            key_points=lambda x: x["key_points"],
            analysis=analyze_prompt | llm | StrOutputParser()
        )
        | recommend_prompt
        | llm
        | StrOutputParser()
    )

    return chain

# Usage
analysis_chain = create_analysis_chain()

document_text = """
The offshore wind farm project faces several challenges including
supply chain delays, regulatory approval processes, and environmental
impact assessments. Budget overruns of 15% have been reported...
"""

recommendations = analysis_chain.invoke(document_text)
print(recommendations)
```

### 2. Agent with Tools

**ReAct Agent with Custom Tools:**
```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain import hub
from typing import Optional
import requests
import json

@tool
def calculate_mooring_tension(
    depth: float,
    line_length: float,
    pretension: float,
    offset: float
) -> str:
    """
    Calculate approximate mooring line tension given parameters.

    Args:
        depth: Water depth in meters
        line_length: Mooring line length in meters
        pretension: Initial pretension in kN
        offset: Horizontal vessel offset in meters

    Returns:
        Tension calculation result
    """
    # Simplified catenary calculation
    import math

    suspended_length = math.sqrt(line_length**2 - depth**2)
    stretch_factor = 1 + (offset / suspended_length) * 0.1
    tension = pretension * stretch_factor

    return json.dumps({
        "horizontal_tension_kN": round(tension, 2),
        "vertical_tension_kN": round(tension * (depth / line_length), 2),
        "line_angle_deg": round(math.degrees(math.asin(depth / line_length)), 1)
    })

@tool
def get_wave_data(location: str, date: Optional[str] = None) -> str:
    """
    Get wave condition data for a location.

    Args:
        location: Location name or coordinates
        date: Date in YYYY-MM-DD format (optional)

    Returns:
        Wave data including Hs, Tp, direction
    """
    # Simulated data - replace with actual API call
    wave_data = {
        "location": location,
        "significant_wave_height_m": 2.5,
        "peak_period_s": 8.5,
        "wave_direction_deg": 225,
        "data_source": "simulated"
    }
    return json.dumps(wave_data)

@tool
def search_engineering_database(query: str) -> str:
    """
    Search the engineering standards database.

    Args:
        query: Search query for standards/specifications

    Returns:
        Relevant standards and references
    """
    # Simulated database - replace with actual search
    results = {
        "query": query,
        "results": [
            {"standard": "API RP 2SK", "title": "Design and Analysis of Stationkeeping Systems"},
            {"standard": "DNV-OS-E301", "title": "Position Mooring"},
            {"standard": "ISO 19901-7", "title": "Stationkeeping systems"}
        ]
    }
    return json.dumps(results)

def create_engineering_agent():
    """
    Create an agent with engineering-specific tools.
    """
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Define tools
    tools = [
        calculate_mooring_tension,
        get_wave_data,
        search_engineering_database
    ]

    # Get ReAct prompt from hub
    prompt = hub.pull("hwchase17/react")

    # Create agent
    agent = create_react_agent(llm, tools, prompt)

    # Create executor with error handling
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    return agent_executor

# Usage
agent = create_engineering_agent()

response = agent.invoke({
    "input": """
    I need to analyze a mooring system in 100m water depth.
    The lines are 350m long with 500kN pretension.
    What would be the tension if the vessel offset is 15m?
    Also, what standards should I reference?
    """
})

print(response["output"])
```

**Tool Agent with Structured Output:**
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    """Structured analysis result."""
    summary: str = Field(description="Brief summary of findings")
    key_findings: List[str] = Field(description="List of key findings")
    recommendations: List[str] = Field(description="List of recommendations")
    risk_level: str = Field(description="Risk level: low, medium, or high")

@tool
def analyze_document(document_path: str) -> str:
    """
    Analyze an engineering document and extract key information.

    Args:
        document_path: Path to the document

    Returns:
        Extracted information from document
    """
    # Simulated document analysis
    return """
    Document: Mooring Analysis Report
    Key findings:
    - Maximum tension: 2500 kN (within limits)
    - Safety factor: 1.8 (above minimum 1.67)
    - Fatigue life: 45 years (design life: 25 years)
    Recommendations:
    - Monitor chain condition at fairlead
    - Consider dynamic analysis for extreme conditions
    """

def create_structured_agent():
    """Create agent that returns structured output."""

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    tools = [analyze_document]

    system_prompt = """You are an engineering analysis assistant.
    Use the available tools to analyze documents and provide structured insights.
    Always provide your final answer in a structured format with:
    - summary
    - key_findings (list)
    - recommendations (list)
    - risk_level

    {tools}

    {tool_names}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
    ])

    agent = create_structured_chat_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

# Usage
structured_agent = create_structured_agent()
result = structured_agent.invoke({
    "input": "Analyze the mooring report at /data/mooring_report.pdf"
})
```

### 3. Conversation Memory

**Conversation Buffer Memory:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# Store for session histories
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create message history for a session."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def create_conversational_chain():
    """
    Create a chain with conversation memory.
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert offshore engineering consultant.
        You help with mooring design, vessel dynamics, and marine operations.
        Maintain context from previous messages in the conversation."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    # Wrap with message history
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    return chain_with_history

# Usage
conversational_chain = create_conversational_chain()

# First message
response1 = conversational_chain.invoke(
    {"input": "I'm designing a spread mooring system for a 100,000 DWT tanker."},
    config={"configurable": {"session_id": "project-123"}}
)
print(f"Assistant: {response1.content}")

# Follow-up (remembers context)
response2 = conversational_chain.invoke(
    {"input": "What line configuration would you recommend?"},
    config={"configurable": {"session_id": "project-123"}}
)
print(f"Assistant: {response2.content}")

# Check history
history = get_session_history("project-123")
print(f"\nConversation has {len(history.messages)} messages")
```

**Summary Memory for Long Conversations:**
```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain

def create_summary_memory_chain():
    """
    Create chain with summary memory for long conversations.
    Keeps recent messages verbatim, summarizes older ones.
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    # Summary buffer keeps last 1000 tokens verbatim
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        return_messages=True
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    return chain, memory

# Usage
chain, memory = create_summary_memory_chain()

# Simulate long conversation
responses = []
questions = [
    "What are the main types of mooring systems?",
    "Tell me about spread moorings in detail.",
    "What about single point moorings?",
    "How do turret moorings work?",
    "Compare the maintenance requirements.",
    "What are the cost implications?"
]

for q in questions:
    response = chain.predict(input=q)
    responses.append(response)
    print(f"Q: {q}")
    print(f"A: {response[:200]}...")
    print()

# Check memory state
print("Memory Summary:")
print(memory.moving_summary_buffer)
```

### 4. RAG (Retrieval Augmented Generation)

**Complete RAG Pipeline:**
```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
from typing import List

def create_rag_pipeline(
    documents_dir: str,
    collection_name: str = "engineering_docs",
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    """
    Create a complete RAG pipeline.

    Args:
        documents_dir: Directory containing documents
        collection_name: Name for vector store collection
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks

    Returns:
        RAG chain for question answering
    """
    # 1. Load documents
    loader = DirectoryLoader(
        documents_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    documents = loader.load()

    print(f"Loaded {len(documents)} document pages")

    # 2. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # 3. Create embeddings and vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="./chroma_db"
    )

    # 4. Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # 5. Create RAG prompt
    rag_prompt = ChatPromptTemplate.from_template("""
    You are an expert assistant answering questions based on the provided context.
    Use only the information from the context to answer.
    If the context doesn't contain the answer, say "I don't have enough information."

    Context:
    {context}

    Question: {question}

    Answer:
    """)

    # 6. Create LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # 7. Build RAG chain
    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
            for doc in docs
        )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever

# Usage
rag_chain, retriever = create_rag_pipeline(
    documents_dir="./engineering_docs",
    collection_name="offshore_standards"
)

# Query
answer = rag_chain.invoke(
    "What are the safety factor requirements for mooring lines?"
)
print(answer)

# Get source documents
docs = retriever.get_relevant_documents(
    "mooring line safety factors"
)
for doc in docs:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:200]}...")
    print()
```

**RAG with Reranking:**
```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def create_reranked_rag_pipeline(
    vectorstore: Chroma,
    top_k_initial: int = 20,
    top_k_final: int = 5
):
    """
    Create RAG pipeline with reranking for better relevance.

    Args:
        vectorstore: Existing vector store
        top_k_initial: Number of docs to retrieve initially
        top_k_final: Number of docs after reranking
    """
    # Base retriever - get more docs initially
    base_retriever = vectorstore.as_retriever(
        search_kwargs={"k": top_k_initial}
    )

    # Reranker using cross-encoder
    reranker_model = HuggingFaceCrossEncoder(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )
    compressor = CrossEncoderReranker(
        model=reranker_model,
        top_n=top_k_final
    )

    # Compression retriever with reranking
    retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    # Build chain
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based on the context below.
    Cite your sources by mentioning which document the information came from.

    Context:
    {context}

    Question: {question}

    Answer with citations:
    """)

    def format_docs_with_citations(docs):
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            formatted.append(f"[{i}] {source}:\n{doc.page_content}")
        return "\n\n".join(formatted)

    chain = (
        {"context": retriever | format_docs_with_citations, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

# Usage
# Assuming vectorstore already exists
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

reranked_chain = create_reranked_rag_pipeline(vectorstore)

answer = reranked_chain.invoke(
    "What are the fatigue analysis requirements for mooring chains?"
)
print(answer)
```

### 5. Document Processing

**Multi-Format Document Loader:**
```python
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    TextLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class LoaderConfig:
    """Configuration for document loader."""
    glob_pattern: str
    loader_cls: type
    loader_kwargs: dict = None

LOADER_CONFIGS = {
    ".pdf": LoaderConfig("**/*.pdf", PyPDFLoader),
    ".docx": LoaderConfig("**/*.docx", Docx2txtLoader),
    ".xlsx": LoaderConfig("**/*.xlsx", UnstructuredExcelLoader),
    ".csv": LoaderConfig("**/*.csv", CSVLoader),
    ".txt": LoaderConfig("**/*.txt", TextLoader),
    ".md": LoaderConfig("**/*.md", TextLoader),
}

def load_documents_multi_format(
    directory: str,
    extensions: List[str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List:
    """
    Load documents from multiple formats.

    Args:
        directory: Base directory for documents
        extensions: List of extensions to load (None = all)
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks

    Returns:
        List of chunked documents
    """
    if extensions is None:
        extensions = list(LOADER_CONFIGS.keys())

    all_documents = []

    for ext in extensions:
        if ext not in LOADER_CONFIGS:
            print(f"Warning: No loader for {ext}")
            continue

        config = LOADER_CONFIGS[ext]

        try:
            loader = DirectoryLoader(
                directory,
                glob=config.glob_pattern,
                loader_cls=config.loader_cls,
                loader_kwargs=config.loader_kwargs or {},
                show_progress=True
            )
            docs = loader.load()

            print(f"Loaded {len(docs)} documents with extension {ext}")
            all_documents.extend(docs)

        except Exception as e:
            print(f"Error loading {ext} files: {e}")

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = text_splitter.split_documents(all_documents)

    print(f"Total: {len(all_documents)} documents -> {len(chunks)} chunks")

    return chunks

def add_metadata_to_chunks(
    chunks: List,
    additional_metadata: Dict = None
) -> List:
    """
    Enrich document chunks with additional metadata.
    """
    for chunk in chunks:
        # Extract filename without path
        source = chunk.metadata.get("source", "")
        chunk.metadata["filename"] = Path(source).name
        chunk.metadata["extension"] = Path(source).suffix

        # Add custom metadata
        if additional_metadata:
            chunk.metadata.update(additional_metadata)

        # Add chunk stats
        chunk.metadata["chunk_length"] = len(chunk.page_content)
        chunk.metadata["word_count"] = len(chunk.page_content.split())

    return chunks

# Usage
chunks = load_documents_multi_format(
    directory="./project_docs",
    extensions=[".pdf", ".docx", ".md"],
    chunk_size=1500,
    chunk_overlap=300
)

enriched_chunks = add_metadata_to_chunks(
    chunks,
    additional_metadata={
        "project": "Offshore Platform Analysis",
        "version": "2.0"
    }
)

print(f"First chunk metadata: {enriched_chunks[0].metadata}")
```

### 6. Streaming Responses

**Streaming Chain:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import asyncio

def create_streaming_chain():
    """Create chain that supports streaming output."""

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        streaming=True
    )

    prompt = ChatPromptTemplate.from_template(
        "You are an expert engineer. Explain in detail: {topic}"
    )

    chain = prompt | llm | StrOutputParser()

    return chain

# Synchronous streaming
def stream_response(chain, topic: str):
    """Stream response token by token."""
    print("Response: ", end="", flush=True)

    for chunk in chain.stream({"topic": topic}):
        print(chunk, end="", flush=True)

    print("\n")

# Async streaming
async def astream_response(chain, topic: str):
    """Async stream response."""
    print("Response: ", end="", flush=True)

    async for chunk in chain.astream({"topic": topic}):
        print(chunk, end="", flush=True)

    print("\n")

# Usage
chain = create_streaming_chain()

# Sync streaming
stream_response(chain, "mooring line catenary equations")

# Async streaming
asyncio.run(astream_response(chain, "wave-structure interaction"))
```

**Streaming with Callbacks:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List
import json

class CustomStreamHandler(BaseCallbackHandler):
    """Custom callback handler for streaming."""

    def __init__(self):
        self.tokens = []
        self.final_response = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when a new token is generated."""
        self.tokens.append(token)
        self.final_response += token
        # Could send to WebSocket, write to file, etc.
        print(token, end="", flush=True)

    def on_llm_end(self, response: Any, **kwargs) -> None:
        """Called when LLM finishes."""
        print(f"\n\n[Generation complete: {len(self.tokens)} tokens]")

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """Called on error."""
        print(f"\n[Error: {error}]")

def stream_with_callbacks(prompt: str):
    """Stream with custom callbacks."""

    handler = CustomStreamHandler()

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        streaming=True,
        callbacks=[handler]
    )

    response = llm.invoke(prompt)

    return handler.final_response, handler.tokens

# Usage
response, tokens = stream_with_callbacks(
    "Explain the design considerations for a turret mooring system"
)

print(f"\nTotal tokens: {len(tokens)}")
```

## Complete Examples

### Example 1: Engineering Documentation Assistant

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from pathlib import Path

class EngineeringAssistant:
    """
    Complete engineering documentation assistant with:
    - RAG for document retrieval
    - Conversation memory
    - Streaming responses
    """

    def __init__(
        self,
        docs_directory: str,
        persist_directory: str = "./chroma_db"
    ):
        self.docs_directory = docs_directory
        self.persist_directory = persist_directory
        self.session_store = {}

        # Initialize components
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3, streaming=True)

        # Setup RAG
        self.vectorstore = self._setup_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # Setup conversational chain
        self.chain = self._create_chain()

    def _setup_vectorstore(self):
        """Load documents and create vector store."""
        persist_path = Path(self.persist_directory)

        # Check if vector store exists
        if persist_path.exists():
            print("Loading existing vector store...")
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

        # Load and process documents
        print("Creating new vector store...")
        loader = DirectoryLoader(
            self.docs_directory,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        return Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

    def _get_session_history(self, session_id: str):
        """Get or create session history."""
        if session_id not in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
        return self.session_store[session_id]

    def _create_chain(self):
        """Create the conversational RAG chain."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert engineering assistant.

            Use the following context from engineering documents to answer questions.
            Always cite your sources by mentioning the document name.
            If you cannot find the answer in the context, say so.

            Context:
            {context}
            """),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])

        def format_docs(docs):
            return "\n\n---\n\n".join(
                f"[{doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
                for doc in docs
            )

        chain = (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(self.retriever.get_relevant_documents(x["question"]))
            )
            | prompt
            | self.llm
        )

        return RunnableWithMessageHistory(
            chain,
            self._get_session_history,
            input_messages_key="question",
            history_messages_key="history"
        )

    def ask(self, question: str, session_id: str = "default"):
        """Ask a question with conversation context."""
        response = self.chain.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}}
        )
        return response.content

    def stream_ask(self, question: str, session_id: str = "default"):
        """Ask a question with streaming response."""
        for chunk in self.chain.stream(
            {"question": question},
            config={"configurable": {"session_id": session_id}}
        ):
            if hasattr(chunk, 'content'):
                yield chunk.content

    def get_sources(self, question: str, k: int = 5):
        """Get source documents for a question."""
        docs = self.retriever.get_relevant_documents(question)[:k]
        return [
            {
                "source": doc.metadata.get("source"),
                "content": doc.page_content[:500] + "..."
            }
            for doc in docs
        ]

# Usage
assistant = EngineeringAssistant(
    docs_directory="./engineering_standards"
)

# Regular query
answer = assistant.ask(
    "What is the minimum safety factor for permanent mooring lines?",
    session_id="project-001"
)
print(answer)

# Follow-up (uses conversation history)
follow_up = assistant.ask(
    "What about temporary moorings?",
    session_id="project-001"
)
print(follow_up)

# Streaming query
print("\nStreaming response:")
for chunk in assistant.stream_ask("Explain fatigue analysis methodology"):
    print(chunk, end="", flush=True)
print()

# Get sources
sources = assistant.get_sources("mooring safety factors")
for source in sources:
    print(f"\nSource: {source['source']}")
    print(f"Content: {source['content']}")
```

### Example 2: Multi-Tool Research Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class ResearchResult(BaseModel):
    """Structured research result."""
    topic: str
    summary: str
    key_findings: List[str]
    sources: List[str]
    confidence: float

@tool
def save_research_note(
    topic: str,
    content: str,
    tags: List[str]
) -> str:
    """
    Save a research note for later reference.

    Args:
        topic: Research topic
        content: Note content
        tags: List of relevant tags

    Returns:
        Confirmation message
    """
    note_id = hash(topic) % 10000
    # In production, save to database
    return f"Note saved with ID {note_id}. Topic: {topic}, Tags: {', '.join(tags)}"

@tool
def calculate_statistics(
    values: List[float],
    operation: str = "summary"
) -> str:
    """
    Calculate statistics on a list of values.

    Args:
        values: List of numeric values
        operation: Type of calculation (summary, mean, std, range)

    Returns:
        Calculation results
    """
    import statistics

    if operation == "summary":
        result = {
            "count": len(values),
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "median": statistics.median(values)
        }
    elif operation == "mean":
        result = {"mean": statistics.mean(values)}
    elif operation == "std":
        result = {"std": statistics.stdev(values) if len(values) > 1 else 0}
    elif operation == "range":
        result = {"min": min(values), "max": max(values), "range": max(values) - min(values)}
    else:
        result = {"error": f"Unknown operation: {operation}"}

    return json.dumps(result, indent=2)

def create_research_agent():
    """Create a multi-tool research agent."""

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Initialize tools
    search = DuckDuckGoSearchRun()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    tools = [
        search,
        wikipedia,
        save_research_note,
        calculate_statistics
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research assistant that helps gather and analyze information.

        You have access to:
        - Web search for current information
        - Wikipedia for background knowledge
        - Note-taking for saving important findings
        - Statistics calculator for numerical analysis

        When researching:
        1. Search for relevant information
        2. Verify facts from multiple sources
        3. Save important findings as notes
        4. Provide a comprehensive summary

        Always cite your sources and be clear about uncertainty."""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

# Usage
research_agent = create_research_agent()

result = research_agent.invoke({
    "input": """
    Research the current state of floating offshore wind technology.
    I need to know:
    1. What are the main platform types?
    2. What are typical water depths for deployment?
    3. What are the largest projects currently operating?

    Save the key findings as research notes.
    """
})

print(result["output"])
```

## Integration Patterns

### LangServe Deployment

```python
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Create app
app = FastAPI(
    title="Engineering Assistant API",
    version="1.0"
)

# Create chain
prompt = ChatPromptTemplate.from_template(
    "You are an engineering expert. Answer: {question}"
)
llm = ChatOpenAI(model="gpt-4")
chain = prompt | llm | StrOutputParser()

# Add routes
add_routes(app, chain, path="/assistant")

# Run with: uvicorn server:app --reload
```

### LangSmith Tracing

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "engineering-assistant"

# All chain invocations are now traced
chain = ChatPromptTemplate.from_template("{input}") | ChatOpenAI()
response = chain.invoke({"input": "Hello"})
```

## Best Practices

### 1. Error Handling

```python
from langchain_core.runnables import RunnableConfig
from langchain_core.callbacks import CallbackManager
import logging

logger = logging.getLogger(__name__)

def safe_invoke(chain, input_data, max_retries=3):
    """Invoke chain with retry logic."""
    for attempt in range(max_retries):
        try:
            return chain.invoke(input_data)
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 2. Prompt Versioning

```python
from pathlib import Path
import yaml

def load_prompt_template(version: str = "v1"):
    """Load versioned prompt template."""
    prompt_path = Path(f"prompts/{version}.yaml")
    with open(prompt_path) as f:
        config = yaml.safe_load(f)

    return ChatPromptTemplate.from_template(config["template"])
```

### 3. Cost Monitoring

```python
from langchain_community.callbacks import get_openai_callback

def track_costs(chain, input_data):
    """Track API costs for chain invocation."""
    with get_openai_callback() as cb:
        result = chain.invoke(input_data)

    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost: ${cb.total_cost:.4f}")

    return result, cb
```

## Troubleshooting

### Rate Limit Errors

```python
from langchain_openai import ChatOpenAI
from tenacity import retry, wait_exponential, stop_after_attempt

llm = ChatOpenAI(
    model="gpt-4",
    max_retries=3,
    request_timeout=60
)

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def invoke_with_retry(chain, input_data):
    return chain.invoke(input_data)
```

### Memory Issues with Large Documents

```python
# Process documents in batches
def batch_process_documents(documents, batch_size=100):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        yield process_batch(batch)
```

### Vector Store Performance

```python
# Use FAISS for larger collections
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(
    documents,
    embeddings,
    distance_strategy="COSINE"
)

# Add index for faster retrieval
vectorstore.save_local("faiss_index")
```

## Resources

- **LangChain Documentation**: https://python.langchain.com/docs/
- **LangChain Expression Language**: https://python.langchain.com/docs/expression_language/
- **LangSmith**: https://smith.langchain.com/
- **LangServe**: https://python.langchain.com/docs/langserve/

---

## Version History

- **1.0.0** (2026-01-17): Initial release with chains, agents, memory, RAG, and streaming
