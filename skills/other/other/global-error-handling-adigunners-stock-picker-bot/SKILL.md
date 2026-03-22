---
name: Global Error Handling
description: Error handling patterns for stock_picker_bot using FastAPI exception handlers, try/except blocks, and logging. Covers API errors, database failures, yfinance failures, and LLM API errors.
---

# Global Error Handling

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to error handling in the stock_picker_bot project.

## When to use this skill

Use this skill when:

1. Creating FastAPI exception handlers for invalid stock symbols or data errors
2. Handling yfinance API failures when fetching stock market data
3. Implementing database transaction error handling for portfolio operations
4. Catching and logging errors from Google Generative AI and Claude API calls
5. Managing connection errors for httpx/requests HTTP client calls
6. Implementing retry logic for transient failures in external APIs
7. Creating meaningful error responses with appropriate HTTP status codes
8. Logging errors with context for debugging stock data processing issues

## Instructions

For details, refer to the information provided in this file:
[global error handling](../../../agent-os/standards/global/error-handling.md)
