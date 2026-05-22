---
name: api-documentation-writer
description: Generate comprehensive API documentation for REST, GraphQL, WebSocket APIs with OpenAPI specs, endpoint descriptions, request/response examples, error codes, authentication guides, and SDKs. USE WHEN user says 'viết document API', 'tạo API docs', 'generate API documentation', 'document REST endpoints', hoặc cần tạo technical reference cho developers.
---
## When to Activate This Skill

- User nói "viết document API"
- User muốn "tạo API documentation"
- Cần generate "OpenAPI spec"
- Cần document "GraphQL schema"
- Cần tạo "developer guide" cho API
- Cần document "webhook" hoặc "authentication"

## Core Workflow

### Phase 1: Gather API Information

Hỏi user những câu hỏi sau để hiểu rõ API:
- **API type**: REST, GraphQL, WebSocket, gRPC?
- **Authentication**: API key, OAuth, JWT, Bearer token?
- **Base URL**: Production URL, versioning strategy?
- **Endpoints**: Danh sách endpoints, mục đích của từng cái?
- **Request/Response format**: JSON, XML, custom format?
- **Rate limiting**: Có giới hạn không, bao nhiêu requests/giờ?
- **Webhooks**: Có support webhooks không?

### Phase 2: Generate Complete Documentation Structure

**Overview Section**:
- Mô tả API (1-2 câu)
- Key capabilities
- Quick start checklist
- Support & resources

**Authentication**:
- Cách lấy credentials
- Nơi đặt auth tokens
- Example authenticated request
- Token refresh process (nếu có)

**Base URL & Versioning**:
- Production + sandbox URLs
- Version format (path, header, query param)
- Current version + changelog

**Endpoints** (mỗi endpoint):
- HTTP method + path
- Mô tả chi tiết
- Path parameters
- Query parameters
- Request headers
- Request body schema
- Response codes + meanings
- Response body schema
- Example requests (curl, JavaScript, Python)
- Example responses (formatted JSON)

**Error Handling**:
- Standard error response format
- Common error codes + meanings
- Troubleshooting guide

**Rate Limiting**:
- Limits + windows
- Headers to check
- How to handle rate limits

**SDKs & Libraries**:
- Official client libraries
- Community libraries
- Installation instructions

**Webhooks** (nếu có):
- Available webhook events
- Setup process
- Payload examples
- Security verification

### Phase 3: Format Output

**REST API Template**:


**Phase 2 details:** `read .claude/skills/api/api-documentation-writer/references/phase2-structure.md`

