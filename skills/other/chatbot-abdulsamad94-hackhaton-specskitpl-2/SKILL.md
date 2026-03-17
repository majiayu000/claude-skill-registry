---
name: Chatbot Implementation
description: Details of the RAG Chatbot, including UI and backend logic.
---

# Chatbot Logic

## Overview
A specialized RAG (Retrieval Augmented Generation) chatbot that helps users learn from the textbook content.

## Backend
- **Route**: `app/api/chat/route.ts`
- **Logic**:
    1.  Receives `query` and `history`.
    2.  Embeds query using Gemini or OpenAI embedding model.
    3.  Searches Qdrant (vector DB) for relevant textbook chunks.
    4.  Constructs context from matches.
    5.  Generates response using Gemini Flash/Pro.

## Vector Search (Qdrant)
We use Qdrant for storing embeddings of the textbook.
- Collection: `textbook_chunks` (or similar).
- Fields: `text`, `source`, `chunk_id`.

## UI Component
- **Location**: `textbook/src/components/Chatbot/index.tsx`.
- **Features**:
    - Floating chat window.
    - Size controls (Small, Medium, Large).
    - Markdown rendering of responses.
    - Context selection (highlight text to ask about it).
    - Mobile responsive design.
    - Auth awareness (personalizes answer based on user profile).

## Styling
- **CSS**: `styles.module.css` (Premium animations, shadow effects).
- **Themes**: Dark/Light mode compatible (using `--ifm` variables).
