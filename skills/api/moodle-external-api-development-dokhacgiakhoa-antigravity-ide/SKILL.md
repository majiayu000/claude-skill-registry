---
version: 4.1.0-fractal
name: moodle-external-api-development
description: Create custom external web service APIs for Moodle LMS. Use when implementing web services for course management, user tracking, quiz operations, or custom plugin functionality. Covers parameter validation, database operations, error handling, service registration, and Moodle coding standards.
---

# Moodle External API Development

This skill guides you through creating custom external web service APIs for Moodle LMS, following Moodle's external API framework and coding standards.

## When to Use This Skill

- Creating custom web services for Moodle plugins
- Implementing REST/AJAX endpoints for course management
- Building APIs for quiz operations, user tracking, or reporting
- Exposing Moodle functionality to external applications
- Developing mobile app backends using Moodle

## Core Architecture Pattern

Moodle external APIs follow a strict three-method pattern:

1. **`execute_parameters()`** - Defines input parameter structure
2. **`execute()`** - Contains business logic
3. **`execute_returns()`** - Defines return structure

## Step-by-Step Implementation

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Step 1: Create the External API Class File](./sub-skills/step-1-create-the-external-api-class-file.md)
### 2. [Step 2: Define Input Parameters](./sub-skills/step-2-define-input-parameters.md)
### 3. [Step 3: Implement Business Logic](./sub-skills/step-3-implement-business-logic.md)
### 4. [Step 4: Define Return Structure](./sub-skills/step-4-define-return-structure.md)
### 5. [Step 5: Register the Service](./sub-skills/step-5-register-the-service.md)
### 6. [Step 6: Implement Error Handling & Logging](./sub-skills/step-6-implement-error-handling-logging.md)
### 7. [Complex Database Operations](./sub-skills/complex-database-operations.md)
### 8. [Working with Course Modules](./sub-skills/working-with-course-modules.md)
### 9. [Access Restrictions (Groups/Availability)](./sub-skills/access-restrictions-groupsavailability.md)
### 10. [Random Question Selection with Tags](./sub-skills/random-question-selection-with-tags.md)
### 11. [1. Via Moodle Web Services Test Client](./sub-skills/1-via-moodle-web-services-test-client.md)
### 12. [2. Via curl](./sub-skills/2-via-curl.md)
### 13. [3. Via JavaScript (AJAX)](./sub-skills/3-via-javascript-ajax.md)
### 14. [1. "Function not found" Error](./sub-skills/1-function-not-found-error.md)
### 15. [2. "Invalid parameter value detected"](./sub-skills/2-invalid-parameter-value-detected.md)
### 16. [3. SQL Injection Vulnerabilities](./sub-skills/3-sql-injection-vulnerabilities.md)
### 17. [4. Permission Denied Errors](./sub-skills/4-permission-denied-errors.md)
### 18. [5. Transaction Deadlocks](./sub-skills/5-transaction-deadlocks.md)
### 19. [Simple Read API (Get Quiz Attempts)](./sub-skills/simple-read-api-get-quiz-attempts.md)
### 20. [Complex Write API (Create Quiz from Categories)](./sub-skills/complex-write-api-create-quiz-from-categories.md)
