---
name: Backend (FastAPI)
description: Documentation for the FastAPI backend, endpoints, and dependency injection.
---

# Backend Architecture (FastAPI)

## Overview

The backend is a **FastAPI** application located in `backend/`. It powers the chatbot and RAG functionality.

## Entry Point

- **File**: `backend/main.py`
- **Run**: `uvicorn backend.main:app --reload` (or via `npm run dev`)
- **Port**: Defaults to `8000`.

## Endpoints

### `POST /api/chat`

- **Purpose**: Main RAG chat endpoint.
- **Input**: `ChatRequest` (query, history, user_context).
- **Process**:
  1. Embed query.
  2. Search Qdrant (`search_qdrant`).
  3. Build prompt (`build_rag_prompt`).
  4. Generate Agent response.
- **Output**: `ChatResponse` (answer, contexts).

### `POST /api/ask-selection`

- **Purpose**: Targeted Q&A on selected text.
- **Input**: `AskSelectionRequest` (question, selected_text).
- **Process**:
  1. Validates selection length.
  2. Builds selection-specific prompt.
  3. specific Agent instructions.

## Dependencies & Utils

- `backend/utils/config.py`: Qdrant initialization.
- `backend/utils/helpers.py`: Embedding and Prompt building logic.
- `backend/models.py`: OpenAI/Gemini client setup.

## Environment Variables

- `GEMINI_API_KEY`: For LLM and Embeddings.
- `QDRANT_URL`, `QDRANT_API_KEY`: Vector DB connection.
