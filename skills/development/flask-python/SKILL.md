---
name: flask-python
description: Guidelines for Flask Python development with best practices for blueprints, RESTful APIs, and application factories.
---

# Flask Python Development

You are an expert in Flask and Python web development. Follow these guidelines when writing Flask code.

## Key Principles

- Write concise, technical responses with accurate Python examples
- Use functional, declarative programming; avoid classes except for Flask views
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., `is_active`, `has_permission`)
- Use lowercase with underscores for directories and files (e.g., `blueprints/user_routes.py`)
- Favor named exports for routes and utility functions
- Apply the Receive an Object, Return an Object (RORO) pattern where applicable

## Python/Flask Standards

- Use `def` for function definitions
- Implement type hints for all function signatures where possible
- Structure: Flask app initialization, blueprints, models, utilities, config
- Omit unnecessary curly braces in conditionals
- Use concise one-line syntax for simple conditional statements

## Error Handling and Validation

- Handle errors and edge cases at function entry points
- Use early returns for error conditions to prevent deep nesting
- Place successful logic last in functions for improved readability
- Avoid unnecessary `else` statements; use if-return pattern instead
- Employ guard clauses for preconditions and invalid states
- Implement proper error logging with user-friendly messages
- Use custom error types or error factories for consistent handling

## Required Dependencies

- Flask
- Flask-RESTful (RESTful API development)
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Marshmallow (serialization/deserialization)
- Flask-JWT-Extended (JWT authentication)

## Flask-Specific Guidelines

- Use Flask application factories for modularity and testing
- Organize routes using Flask Blueprints
- Leverage Flask-RESTful for class-based views
- Implement custom error handlers for different exception types
- Use Flask decorators: `before_request`, `after_request`, `teardown_request`
- Utilize Flask extensions for common functionalities
- Manage configurations via Flask's config object (development, testing, production)
- Implement logging using Flask's `app.logger`
- Handle authentication/authorization with Flask-JWT-Extended

## Performance Optimization

- Use Flask-Caching for frequently accessed data
- Implement database query optimization (eager loading, indexing)
- Apply connection pooling for database connections
- Manage database sessions properly
- Use background tasks for time-consuming operations (e.g., Celery)

## Key Conventions

1. Use Flask's application context and request context appropriately
2. Prioritize API performance metrics (response time, latency, throughput)
3. Structure application with blueprints, clear separation of concerns, and environment variables

## Database Interaction

- Use Flask-SQLAlchemy for ORM operations
- Implement database migrations via Flask-Migrate
- Properly manage SQLAlchemy sessions, ensuring closure after use

## Serialization and Validation

- Use Marshmallow for object serialization/deserialization and input validation
- Create schema classes for each model for consistent handling

## Authentication and Authorization

- Implement JWT-based authentication using Flask-JWT-Extended
- Use decorators for protecting routes requiring authentication

## Testing

- Write unit tests using pytest
- Use Flask's test client for integration testing
- Implement test fixtures for database and application setup

## API Documentation

- Use Flask-RESTX or Flasgger for Swagger/OpenAPI documentation
- Document all endpoints with request/response schemas

## Deployment

- Use Gunicorn or uWSGI as WSGI HTTP Server
- Implement proper logging and monitoring in production
- Use environment variables for sensitive information and configuration
