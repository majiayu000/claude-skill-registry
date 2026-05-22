---
name: RSpec Test Framework
description: Execute and generate RSpec tests for Ruby projects with let bindings, before hooks, and mocking support
version: 1.0.0
---

# RSpec Test Framework

## Purpose

Provide RSpec test execution and generation for Ruby projects.

## Usage

```bash
ruby generate-test.rb --source=lib/calculator.rb --output=spec/calculator_spec.rb --description="Division by zero"
ruby run-test.rb --file=spec/calculator_spec.rb
```

## Output Format

JSON with success, passed, failed, total, and failures array.
