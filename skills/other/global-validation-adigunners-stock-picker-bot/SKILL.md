---
name: Global Validation
description: Data validation strategies for stock_picker_bot using Pydantic models and SQLAlchemy constraints. Covers API input validation, stock data validation, and database integrity.
---

# Global Validation

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to data validation in the stock_picker_bot project.

## When to use this skill

Use this skill when:

1. Creating Pydantic models for API request validation with field constraints
2. Validating stock symbols and date ranges in API endpoints
3. Implementing field validators for price ranges and portfolio limits
4. Adding SQLAlchemy column constraints for financial data accuracy
5. Validating data from yfinance before storing in database
6. Ensuring portfolio values and percentages are logically valid
7. Validating LLM API responses and recommendation outputs
8. Implementing custom validators for business logic (e.g., valid trading rules)

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
