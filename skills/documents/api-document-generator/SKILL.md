---
name: api-document-generator
description: Parses interface/API information from files or directories and generates OpenAPI-compliant documentation with timestamps
---

# API Documentation Generator

This skill automatically generates OpenAPI-compliant documentation from code files. It parses interface definitions, API endpoints, and related information to create comprehensive, readable API documentation that follows OpenAPI specification standards.

## Capabilities

- **File Parsing**: Parse interface/API information from files or directories
- **OpenAPI Compliance**: Generate documentation that complies with OpenAPI specification (https://swagger.io/specification/)
- **Timestamp Management**: Automatically include timestamps in documentation files
- **Directory Scanning**: Process multiple files in a directory structure
- **Validation**: Validate generated documentation against OpenAPI standards
- **Multiple Formats**: Support for various code file types (Python, JavaScript, TypeScript, etc.)

## Input Requirements

- **File or directory path**: Path to the file or directory containing API/interface definitions
- **Supported file types**: Python (.py), JavaScript (.js), TypeScript (.ts), JSON (.json), YAML (.yaml, .yml)
- **Optional parameters**:
  - `output_format`: Format for documentation (default: markdown)
  - `include_examples`: Whether to include example requests/responses (default: true)
  - `validate_openapi`: Validate against OpenAPI specification (default: true)

## Output Formats

- **Primary output**: Markdown file with timestamp format: `YYYY-MM-DD_HH-MM-SS.md`
- **Location**: Saved to `current_repository/.claude/api_doc/` directory
- **Content**: OpenAPI-compliant documentation with:
  - API title and description
  - Endpoint definitions
  - Request/response schemas
  - Authentication information
  - Example usage
  - Error codes and responses
  - Timestamp and generation metadata

## How to Use

"Generate API documentation from the `src/api/` directory"
"Parse this Python file and create OpenAPI documentation"
"Create API documentation for the endpoints in this TypeScript file"

## Scripts

- `api_parser.py`: Main module for parsing API information from files
- `openapi_generator.py`: Generates OpenAPI-compliant documentation
- `file_handler.py`: Handles file operations and directory scanning

## Best Practices

1. **File Organization**: Keep API-related files in structured directories
2. **Clear Naming**: Use descriptive names for endpoints and parameters
3. **Consistent Formatting**: Follow consistent code formatting for better parsing
4. **Comments**: Include clear comments in code for better documentation generation
5. **Validation**: Always validate generated documentation against OpenAPI standards

## Limitations

- Requires properly formatted code with clear interface definitions
- Complex nested structures may require manual review
- Some framework-specific annotations may not be fully parsed
- Generated documentation quality depends on source code clarity
- Large directories may take longer to process