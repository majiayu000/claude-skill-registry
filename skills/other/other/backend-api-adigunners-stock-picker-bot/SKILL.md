---
name: Backend API
description: FastAPI endpoint design, routing, and request/response handling for the stock_picker_bot backend. Covers API structure, dependency injection, and integration with Pydantic models for stock data processing and analysis endpoints.
---

# Backend API

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to FastAPI endpoint development in the stock_picker_bot backend.

## When to use this skill

Use this skill when:

1. Creating or modifying FastAPI route handlers in `app/routes/` that fetch stock data via yfinance
2. Designing request/response schemas using Pydantic models for stock analysis queries
3. Implementing dependency injection for database sessions in API endpoints
4. Building endpoints that integrate with Google Generative AI or Claude for stock recommendations
5. Adding error handling to API routes using FastAPI exception handlers
6. Structuring endpoints to process pandas DataFrames of stock market data
7. Creating query parameters for stock filtering, date ranges, or portfolio management
8. Implementing response models that serialize SQLAlchemy ORM objects to JSON

## Instructions

For details, refer to the information provided in this file:
[backend API](../../../agent-os/standards/backend/api.md)
