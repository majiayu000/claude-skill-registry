---
name: coding-security
description: Coding and security standards. Apply when writing code, handling comments, error handling, API keys, database connections, user input, or file uploads.
---

# Coding & Security Standards

## General Principles

- **Configuration separation**: All mutable parameters (timeouts, retry counts, feature flags) must be extracted to file header or config file
- **CLI support**: If script has no GUI, must support command line argument parsing and provide `-h` help
- **No temporary code**: Never keep `// TODO: fix later` or temporary validation scripts. Code must be production-ready

## Error Handling

- **Never swallow errors**: Empty try-catch is forbidden
- **Contextual logging**: Error messages must include context (variable values, operation intent), not just "Error occurred"
- **Input validation**: Default to assuming all inputs are malicious or incomplete

## Comment Standards

Use only Better Comments style, keep explanations concise.

Format:
- `// *` Important information (highlight)
- `// !` Alert/Warning
- `// ?` Question/Suggestion
- `// TODO:` Future work

**Rules**:
- Comments must be **declarative** (what the code does), not temporal
- Good comments explain **Why**, not **How** (the code itself is How)

## Security Standards (Highest Priority)

1. **Sensitive Data Isolation**
   - **Absolutely forbidden** to hardcode API Keys, passwords, Tokens, database connection strings in code
   - Use environment variables (.env) or config files
   - Use clear placeholders: `const API_KEY = process.env.API_KEY || "YOUR_API_KEY_HERE";`

2. **Placeholder Management**
   - If placeholders must be used, explicitly remind users to replace them

3. **Common Vulnerability Defense**
   - **SQL Injection**: Must use parameterized queries
   - **XSS**: Escape/sanitize all user inputs
   - **File Upload**: Strictly validate file type and size (don't just check extension)

4. **Dependency Management**
   - When introducing new packages, provide installation commands
   - Must check for known malicious or deprecated packages
