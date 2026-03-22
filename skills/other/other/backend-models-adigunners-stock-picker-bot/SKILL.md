---
name: Backend Models
description: SQLAlchemy ORM models and Pydantic schemas for stock_picker_bot. Includes database models for portfolios, stock data, and Pydantic models for API validation and serialization.
---

# Backend Models

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to SQLAlchemy and Pydantic models in the stock_picker_bot backend.

## When to use this skill

Use this skill when:

1. Creating SQLAlchemy ORM models in `app/models/` for stocks, portfolios, and historical data
2. Defining Pydantic request/response schemas for API endpoints
3. Implementing relationships between models (portfolios to stocks, users to portfolios)
4. Adding database fields for yfinance data storage (prices, volumes, technical indicators)
5. Creating validators on Pydantic models for stock symbols, price ranges, and date fields
6. Defining SQLAlchemy column types and constraints for financial data accuracy
7. Building models to store LLM analysis results and recommendations from Claude or Gemini
8. Implementing computed properties or methods on models for portfolio calculations

## Instructions

For details, refer to the information provided in this file:
[backend models](../../../agent-os/standards/backend/models.md)
