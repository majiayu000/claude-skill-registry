---
name: api-builder
description: Comprehensive API design and development workflow that orchestrates API architecture, endpoint design, documentation generation, and integration patterns. Handles everything from RESTful API creation and GraphQL schema design to API gateway setup and version management.
license: Apache 2.0
tools: []
---

# API Builder - Complete API Development Workflow

## Overview

This skill provides end-to-end API development services by orchestrating API architects, integration specialists, and documentation experts. It transforms API requirements into production-ready APIs with comprehensive design, documentation, testing, and integration capabilities.

**Key Capabilities:**
- 🏗️ **Multi-Protocol API Design** - RESTful APIs, GraphQL, gRPC, and WebSocket implementations
- 📚 **Comprehensive Documentation** - Auto-generated API docs, interactive testing, and developer guides
- 🔧 **Integration Architecture** - API gateways, middleware, and third-party service integration
- 📊 **API Analytics & Monitoring** - Usage tracking, performance monitoring, and error analysis
- 🛡️ **API Security & Governance** - Authentication, rate limiting, and API lifecycle management

## When to Use This Skill

**Perfect for:**
- RESTful API design and implementation
- GraphQL schema development and resolver implementation
- API gateway setup and middleware configuration
- API documentation generation and developer portal creation
- API integration patterns and third-party service connections
- API versioning and lifecycle management

**Triggers:**
- "Design and implement a REST API for [application]"
- "Create a GraphQL API with [features]"
- "Set up an API gateway with [middleware]"
- "Generate comprehensive API documentation"
- "Implement API integration with [service]"

## API Development Expert Panel

### **API Architect** (API Design & Architecture)
- **Focus**: API design patterns, protocol selection, architectural decisions
- **Techniques**: RESTful design, GraphQL schema design, API composition
- **Considerations**: Scalability, maintainability, developer experience, performance

### **Integration Specialist** (API Integration & Middleware)
- **Focus**: API gateways, middleware, third-party integrations
- **Techniques**: API composition, service mesh, event-driven architecture
- **Considerations**: Latency, reliability, security, monitoring

### **Documentation Expert** (API Documentation & Developer Experience)
- **Focus**: API documentation, developer portals, interactive testing
- **Techniques**: OpenAPI/Swagger, GraphQL docs, API testing frameworks
- **Considerations**: Developer experience, documentation accuracy, discoverability

### **API Security Specialist** (API Security & Governance)
- **Focus**: API security, authentication, authorization, governance
- **Techniques**: OAuth 2.0, API keys, rate limiting, threat protection
- **Considerations**: Security by design, compliance, usability

### **Performance Engineer** (API Optimization & Monitoring)
- **Focus**: API performance, caching, monitoring, analytics
- **Techniques**: Response optimization, caching strategies, load balancing
- **Considerations**: Response times, throughput, resource utilization

## API Development Workflow

### Phase 1: API Requirements Analysis & Design Planning
**Use when**: Starting API development or API modernization

**Tools Used:**
```bash
/sc:analyze api-requirements
API Architect: API design requirements and constraints
Integration Specialist: integration points and dependencies
Documentation Expert: documentation requirements and developer needs
```

**Activities:**
- Analyze business requirements and translate to API specifications
- Identify API protocols and architectural patterns
- Define API contracts and data models
- Plan integration points and external dependencies
- Establish API governance and versioning strategy

### Phase 2: API Architecture & Protocol Design
**Use when**: Designing the API structure and choosing protocols

**Tools Used:**
```bash
/sc:design --type api restful-architecture
/sc:design --type graphql schema
API Architect: comprehensive API design and protocol selection
Integration Specialist: integration architecture and patterns
```

**Activities:**
- Design API architecture and protocol selection (REST/GraphQL/gRPC)
- Create API specifications and data contracts
- Design endpoint structures and resource relationships
- Plan API composition and orchestration patterns
- Define error handling and response formats

### Phase 3: API Implementation & Development
**Use when**: Writing the actual API code and business logic

**Tools Used:**
```bash
/sc:implement api-endpoints
API Architect: API implementation patterns and best practices
Integration Specialist: middleware and integration implementation
API Security Specialist: security controls and authentication
```

**Activities:**
- Implement API endpoints and business logic
- Create middleware for authentication, validation, and error handling
- Implement data validation and serialization
- Create API versioning and backward compatibility
- Write unit and integration tests for API endpoints

### Phase 4: API Documentation & Developer Experience
**Use when**: Creating comprehensive API documentation and developer resources

**Tools Used:**
```bash
/sc:implement api-documentation
Documentation Expert: API docs and developer portal creation
API Architect: API specification validation and examples
Integration Specialist: integration guides and SDKs
```

**Activities:**
- Generate OpenAPI/Swagger specifications
- Create interactive API documentation and testing interfaces
- Develop SDKs and client libraries
- Write integration guides and code examples
- Create developer portal and onboarding materials

### Phase 5: API Gateway & Integration Setup
**Use when**: Setting up API gateway, middleware, and integrations

**Tools Used:**
```bash
/sc:implement api-gateway
Integration Specialist: API gateway configuration and middleware
API Security Specialist: security policies and access control
Performance Engineer: caching, rate limiting, and optimization
```

**Activities:**
- Configure API gateway with routing and policies
- Implement middleware for authentication, rate limiting, and logging
- Set up API composition and orchestration
- Configure caching and performance optimization
- Implement API monitoring and analytics

### Phase 6: API Testing & Quality Assurance
**Use when**: Ensuring API reliability, performance, and security

**Tools Used:**
```bash
/sc:test api-comprehensive
Performance Engineer: load testing and performance validation
API Security Specialist: security testing and vulnerability assessment
Documentation Expert: documentation accuracy and usability testing
```

**Activities:**
- Implement comprehensive API test suites (unit, integration, E2E)
- Conduct load testing and performance benchmarking
- Perform security testing and vulnerability assessment
- Validate API contracts and documentation accuracy
- Test error scenarios and recovery mechanisms

## Integration Patterns

### **SuperClaude Command Integration**

| Command | Use Case | Output |
|---------|---------|--------|
| `/sc:design --type api` | API design | Complete API architecture |
| `/sc:implement restful` | REST API | Production-ready REST endpoints |
| `/sc:implement graphql` | GraphQL API | GraphQL schema and resolvers |
| `/sc:implement gateway` | API gateway | Configured API gateway |
| `/sc:test api` | API testing | Comprehensive test suite |

### **API Protocol Integration**

| Protocol | Role | Capabilities |
|----------|------|------------|
| **RESTful** | Standard API | HTTP-based REST API with proper semantics |
| **GraphQL** | Flexible API | Flexible query language and type system |
| **gRPC** | High-performance API | Binary protocol for high-performance scenarios |
| **WebSocket** | Real-time API | Real-time bidirectional communication |

### **MCP Server Integration**

| Server | Expertise | Use Case |
|--------|----------|---------|
| **Sequential** | API reasoning | Complex API design and problem-solving |
| **Web Search** | API patterns | Latest API design trends and best practices |
| **Firecrawl** | API testing | External API integration and testing |

## Usage Examples

### Example 1: Complete REST API Development
```
User: "Create a complete REST API for an e-commerce platform with user management, products, and orders"

Workflow:
1. Phase 1: Analyze e-commerce API requirements and design constraints
2. Phase 2: Design RESTful API architecture with proper resource modeling
3. Phase 3: Implement API endpoints with authentication and validation
4. Phase 4: Generate comprehensive API documentation and developer portal
5. Phase 5: Set up API gateway with rate limiting and monitoring
6. Phase 6: Test API performance, security, and documentation accuracy

Output: Production-ready e-commerce API with complete documentation and monitoring
```

### Example 2: GraphQL API Implementation
```
User: "Implement a GraphQL API for a social media platform with real-time features"

Workflow:
1. Phase 1: Analyze GraphQL requirements and schema design needs
2. Phase 2: Design GraphQL schema with types, queries, and mutations
3. Phase 3: Implement resolvers with proper data fetching and caching
4. Phase 4: Create GraphQL documentation with schema explorer
5. Phase 5: Set up GraphQL gateway with subscriptions and real-time features
6. Phase 6: Test GraphQL queries, mutations, and subscription performance

Output: Feature-rich GraphQL API with real-time capabilities and comprehensive documentation
```

### Example 3: API Gateway and Integration
```
User: "Set up an API gateway to integrate multiple microservices with proper security and monitoring"

Workflow:
1. Phase 1: Analyze integration requirements and service dependencies
2. Phase 2: Design API gateway architecture with routing and policies
3. Phase 3: Implement gateway with authentication, rate limiting, and logging
4. Phase 4: Configure service discovery and load balancing
5. Phase 5: Set up monitoring, analytics, and alerting
6. Phase 6: Test gateway performance, security, and failover mechanisms

Output: Enterprise-grade API gateway with comprehensive security and monitoring
```

## Quality Assurance Mechanisms

### **Multi-Layer API Validation**
- **Design Validation**: API architecture and contract validation
- **Implementation Testing**: Comprehensive endpoint and integration testing
- **Documentation Accuracy**: Documentation validation and developer feedback
- **Performance Testing**: Load testing and performance benchmarking

### **Automated Quality Checks**
- **Contract Testing**: Automated API contract validation and compliance
- **Security Testing**: Automated vulnerability scanning and security assessment
- **Performance Monitoring**: Real-time performance tracking and alerting
- **Documentation Testing**: Automated documentation accuracy and completeness checks

### **Continuous API Improvement**
- **Usage Analytics**: API usage tracking and optimization recommendations
- **Developer Feedback**: Developer experience monitoring and improvement
- **Performance Optimization**: Continuous performance monitoring and optimization
- **Security Monitoring**: Ongoing security assessment and threat protection

## Output Deliverables

### Primary Deliverable: Complete API System
```
api-system/
├── endpoints/
│   ├── controllers/              # API endpoint implementations
│   ├── middleware/               # Authentication, validation, error handling
│   ├── routes/                   # API routing and endpoint definitions
│   └── validators/               # Request/response validation
├── schemas/
│   ├── openapi/                  # OpenAPI/Swagger specifications
│   ├── graphql/                  # GraphQL schemas and resolvers
│   ├── models/                   # Data models and DTOs
│   └── contracts/                # API contracts and interfaces
├── documentation/
│   ├── api-docs/                 # Interactive API documentation
│   ├── developer-portal/          # Developer portal and guides
│   ├── examples/                 # Code examples and tutorials
│   └── sdks/                     # Client libraries and SDKs
├── gateway/
│   ├── config/                   # API gateway configuration
│   ├── policies/                 # Gateway policies and rules
│   ├── middleware/               # Custom gateway middleware
│   └── monitoring/               # Gateway monitoring and analytics
├── tests/
│   ├── unit/                     # Unit tests for API endpoints
│   ├── integration/              # Integration tests for API interactions
│   ├── contract/                 # API contract tests
│   └── performance/              # Load and performance tests
└── config/
    ├── development/              # Development environment configuration
    ├── staging/                  # Staging environment configuration
    └── production/               # Production environment configuration
```

### Supporting Artifacts
- **API Specifications**: Complete OpenAPI/Swagger and GraphQL schemas
- **Documentation Portal**: Interactive API documentation and developer guides
- **SDKs and Clients**: Client libraries for multiple programming languages
- **Integration Guides**: Step-by-step integration instructions and examples
- **Performance Reports**: API performance benchmarks and optimization recommendations

## Advanced Features

### **Intelligent API Design**
- AI-powered API design recommendations and optimization
- Automatic API contract generation and validation
- Intelligent endpoint grouping and organization
- Automated API versioning and migration strategies

### **Advanced API Gateway**
- Service mesh integration with advanced routing
- AI-driven API composition and orchestration
- Dynamic policy enforcement and adaptation
- Real-time API analytics and optimization

### **Developer Experience Enhancement**
- Interactive API testing and exploration
- Automated SDK generation for multiple languages
- Real-time collaboration and API design tools
- Comprehensive onboarding and learning resources

### **API Analytics and Intelligence**
- Advanced usage analytics and insights
- Performance prediction and optimization
- Anomaly detection and alerting
- Business intelligence integration

## Troubleshooting

### Common API Development Challenges
- **Design Issues**: Use proper API design patterns and architectural principles
- **Integration Problems**: Implement clear contracts and proper error handling
- **Performance Bottlenecks**: Optimize queries, implement caching, and use proper indexing
- **Documentation Gaps**: Use automated documentation generation and regular updates

### API Gateway and Integration Issues
- **Routing Problems**: Use proper gateway configuration and service discovery
- **Security Issues**: Implement comprehensive authentication and authorization
- **Performance Issues**: Optimize gateway configuration and implement proper caching
- **Monitoring Gaps**: Implement comprehensive logging, monitoring, and alerting

## Best Practices

### **For API Design**
- Follow RESTful principles or GraphQL best practices
- Design for scalability and maintainability
- Use proper HTTP status codes and error handling
- Implement proper versioning and backward compatibility

### **For API Implementation**
- Use proper authentication and authorization mechanisms
- Implement comprehensive input validation and sanitization
- Use proper error handling and logging
- Write comprehensive tests and documentation

### **For API Documentation**
- Use OpenAPI/Swagger for REST APIs
- Create interactive documentation with examples
- Provide clear integration guides and SDKs
- Keep documentation updated and accurate

### **For API Gateway Configuration**
- Implement proper security policies and rate limiting
- Use comprehensive logging and monitoring
- Configure proper load balancing and failover
- Implement caching and optimization strategies

---

This API builder skill transforms the complex process of API development into a guided, expert-supported workflow that ensures well-designed, well-documented, and production-ready APIs with comprehensive integration and monitoring capabilities.