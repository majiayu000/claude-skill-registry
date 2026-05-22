---
name: api-documentation-generator
description: Automated API documentation generation with support for OpenAPI/Swagger specifications, endpoint analysis, request/response examples, authentication methods, rate limiting, and integration guides. Use when Claude needs to generate API documentation, analyze existing APIs, create specification files, or produce developer-friendly documentation.
---

# API Documentation Generator

## Overview
This skill automates the creation and maintenance of comprehensive API documentation with support for industry-standard formats and developer-friendly presentation. It intelligently analyzes source code to extract API contracts and generates complete, accurate documentation.

## When to Use This Skill
- Generating OpenAPI/Swagger specifications from code
- Creating API documentation from existing endpoints
- Updating documentation to match API changes
- Producing developer guides and integration tutorials
- Analyzing API contracts and dependencies
- Converting API specifications between formats
- Reverse-engineering undocumented APIs
- Generating client SDK documentation
- Creating interactive API explorers

## Supported Languages & Frameworks
### REST APIs
- Express.js / Fastify (Node.js)
- Flask / Django (Python)
- Spring Boot (Java)
- ASP.NET Core (C#)
- Ruby on Rails
- Laravel (PHP)

### GraphQL APIs
- Schema introspection
- Query/mutation/subscription documentation
- Type definitions and relationships

### Other API Types
- gRPC services and protobuf definitions
- SOAP web services
- Webhook documentation

## Supported Formats
- OpenAPI 3.0/3.1 (formerly Swagger)
- Swagger 2.0
- AsyncAPI 2.x (for event-driven APIs)
- RAML 1.0
- API Blueprint
- Postman Collections
- GraphQL Schema Definition Language (SDL)
- JSON Schema
- HAR (HTTP Archive format)

## Documentation Components

### API Information
- Title, description, and version
- Contact details and support information
- License information and terms of service
- External documentation links
- API lifecycle stage (development, beta, stable, deprecated)

### Endpoints & Operations
- HTTP methods and paths
- Path, query, header, and cookie parameters
- Request body schemas with validation rules
- Response schemas for all status codes
- Example requests and responses
- Deprecation notices and migration guidance

### Security Definitions
- API key authentication
- OAuth 2.0 flows (Authorization Code, Client Credentials, etc.)
- JWT/Token authentication
- Basic/Digest authentication
- Mutual TLS
- Custom authentication schemes
- Security requirement mappings per endpoint

### Advanced Features
- Server definitions with variables
- Tags for logical grouping
- External documentation
- Callback definitions
- Link relations
- Webhooks and event documentation
- Discriminator objects for polymorphism

## Analysis Capabilities

### Code Analysis
- Framework-specific route detection
- Parameter and schema inference
- Authentication method identification
- Error response pattern recognition
- Validation rule extraction

### Schema Detection
- Request/response schema analysis
- Type inference from code
- Validation constraints mapping
- Default value extraction
- Enum value detection

### Security Analysis
- Authentication scheme identification
- Permission/role mapping
- Security requirement inference
- Credential location detection

## Best Practices

### Writing Effective Descriptions
- Use clear, concise language
- Explain purpose and behavior
- Document side effects
- Specify business context
- Include usage examples
- Define business terminology

### Parameter Documentation
- Specify data types and constraints
- Indicate required vs optional
- Document default values
- Explain validation rules
- Include example values
- Describe inter-parameter relationships

### Response Documentation
- Detail all possible status codes
- Document error response formats
- Specify success and failure cases
- Include example payloads
- Explain response headers
- Describe pagination patterns

### Security Documentation
- Document authentication requirements
- Explain authorization scopes
- Specify rate limiting policies
- Detail security headers
- Provide security best practices

## Generation Process

### 1. API Discovery
- Scan source code for API endpoints
- Extract route definitions and HTTP methods
- Identify API framework and patterns
- Map endpoint relationships

### 2. Schema Analysis
- Analyze request/response structures
- Infer data types and validation rules
- Extract example values
- Map relationships between entities

### 3. Security Mapping
- Identify authentication methods
- Map authorization requirements
- Document security schemes
- Extract API key locations

### 4. Specification Creation
- Generate OpenAPI specification
- Validate against standards
- Add descriptions and examples
- Organize endpoints by tags
- Include server definitions

### 5. Documentation Generation
- Create human-readable documentation
- Generate interactive API explorer
- Produce client SDK documentation
- Build integration guides
- Export in multiple formats

## Quality Assurance
- Verify all endpoints are documented
- Check for consistent naming
- Validate example requests/responses
- Ensure security schemes are clear
- Confirm all parameters are documented
- Test generated documentation usability
- Validate against OpenAPI specification

## Integration Guides
- Authentication setup
- Error handling patterns
- Rate limiting considerations
- Common use case examples
- Troubleshooting tips
- Migration guides for version changes
- Performance optimization recommendations

## Scripts Available
- `scripts/generate-openapi.js` - Generate OpenAPI spec from code
- `scripts/validate-spec.js` - Validate API specification
- `scripts/export-docs.js` - Export documentation in various formats
- `scripts/check-completeness.js` - Verify documentation completeness
- `scripts/analyze-endpoints.js` - Deep endpoint analysis
- `scripts/extract-schemas.js` - Extract and document data schemas
- `scripts/generate-sdk-docs.js` - Generate client SDK documentation

## References
- `references/openapi-specification.md` - Complete OpenAPI specification guidelines and best practices
- `references/documentation-best-practices.md` - API documentation best practices and writing guidelines
- `references/framework-patterns.md` - Framework-specific API patterns and conventions
- `references/security-schemes.md` - Comprehensive security scheme documentation
- `references/error-handling.md` - API error handling patterns and documentation