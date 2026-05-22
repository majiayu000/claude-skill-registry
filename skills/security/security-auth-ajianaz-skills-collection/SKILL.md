---
name: security-auth
description: Comprehensive security and authentication workflow that orchestrates security architecture, identity management, access control, and compliance implementation. Handles everything from authentication system design and authorization frameworks to security auditing and threat protection.
license: Apache 2.0
tools: []
---

# Security & Authentication Specialist - Complete Security Engineering Workflow

## Overview

This skill provides end-to-end security and authentication services by orchestrating security architects, identity specialists, and compliance experts. It transforms security requirements into production-ready authentication and authorization systems with comprehensive threat protection, compliance adherence, and security monitoring.

**Key Capabilities:**
- 🔐 **Multi-Layer Security Architecture** - Authentication, authorization, and threat protection systems
- 🛡️ **Identity & Access Management** - User authentication, role-based access, and privilege management
- 📊 **Compliance & Auditing** - Regulatory compliance, security auditing, and reporting
- 🔧 **Security Integration** - Seamless integration with existing systems and third-party security services
- 📋 **Threat Protection** - Proactive threat detection, prevention, and incident response

## When to Use This Skill

**Perfect for:**
- Authentication system design and implementation
- Authorization framework development and RBAC implementation
- Security compliance and auditing requirements
- Threat protection and security monitoring setup
- Identity management system integration
- Security assessment and vulnerability management

**Triggers:**
- "Implement authentication and authorization for [application]"
- "Design security architecture for [system]"
- "Set up identity and access management"
- "Implement compliance and security auditing"
- "Create threat protection and monitoring system"

## Security Expert Panel

### **Security Architect** (System Security Design)
- **Focus**: Security architecture, threat modeling, security patterns
- **Techniques**: Zero-trust architecture, defense-in-depth, security frameworks
- **Considerations**: Security by design, attack surface reduction, security controls

### **Identity Specialist** (Authentication & Authorization)
- **Focus**: Authentication systems, identity management, access control
- **Techniques**: OAuth 2.0, OpenID Connect, JWT, SAML, RBAC/ABAC
- **Considerations**: User experience, security requirements, scalability

### **Compliance Expert** (Regulatory & Auditing)
- **Focus**: Regulatory compliance, security auditing, risk assessment
- **Techniques**: SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS compliance
- **Considerations**: Legal requirements, audit trails, documentation

### **Threat Analyst** (Security Monitoring & Response)
- **Focus**: Threat detection, incident response, security monitoring
- **Techniques**: SIEM systems, threat intelligence, security analytics
- **Considerations**: Real-time detection, response procedures, forensic analysis

### **Cryptographic Specialist** (Encryption & Data Protection)
- **Focus**: Encryption implementation, key management, data protection
- **Techniques**: AES, RSA, TLS/SSL, hash functions, digital signatures
- **Considerations**: Key lifecycle management, performance impact, compliance

## Security Implementation Workflow

### Phase 1: Security Requirements Analysis & Threat Modeling
**Use when**: Starting security implementation or security assessment

**Tools Used:**
```bash
/sc:analyze security-requirements
Security Architect: threat modeling and risk assessment
Compliance Expert: regulatory requirement analysis
Threat Analyst: attack surface analysis
```

**Activities:**
- Analyze security requirements and threat landscape
- Identify compliance requirements and regulatory constraints
- Perform threat modeling and attack surface analysis
- Define security policies and procedures
- Plan security architecture and control implementation

### Phase 2: Authentication System Design & Implementation
**Use when**: Designing and implementing authentication systems

**Tools Used:**
```bash
/sc:design --type authentication auth-system
Identity Specialist: authentication framework design
Cryptographic Specialist: secure credential management
Security Architect: authentication security controls
```

**Activities:**
- Design authentication architecture and user identity flows
- Implement secure credential storage and management
- Create multi-factor authentication (MFA) systems
- Design session management and token-based authentication
- Implement password policies and secure recovery mechanisms

### Phase 3: Authorization Framework & Access Control
**Use when**: Implementing authorization and access control systems

**Tools Used:**
```bash
/sc:design --type authorization rbac-system
Identity Specialist: role-based access control implementation
Security Architect: privilege management design
Compliance Expert: access control auditing
```

**Activities:**
- Design role-based access control (RBAC) or attribute-based access control (ABAC)
- Implement fine-grained permissions and privilege management
- Create access control policies and enforcement mechanisms
- Design admin interfaces for user and permission management
- Implement access request and approval workflows

### Phase 4: Security Integration & API Protection
**Use when**: Integrating security controls and protecting APIs

**Tools Used:**
```bash
/sc:implement security-integration
Security Architect: API security and integration
Cryptographic Specialist: encryption and data protection
Threat Analyst: input validation and sanitization
```

**Activities:**
- Implement API authentication and authorization middleware
- Create input validation and output encoding mechanisms
- Implement rate limiting and DDoS protection
- Set up CORS policies and secure headers
- Integrate with third-party security services and tools

### Phase 5: Compliance & Auditing Implementation
**Use when**: Ensuring regulatory compliance and security auditing

**Tools Used:**
```bash
/sc:implement compliance-auditing
Compliance Expert: compliance framework implementation
Security Architect: security monitoring and logging
Threat Analyst: audit trail and forensics
```

**Activities:**
- Implement comprehensive audit logging and monitoring
- Create compliance reporting and documentation
- Set up security incident tracking and reporting
- Implement data retention and deletion policies
- Create security dashboards and compliance metrics

### Phase 6: Threat Protection & Security Monitoring
**Use when**: Setting up proactive threat detection and response

**Tools Used:**
```bash
/sc:implement threat-protection
Threat Analyst: security monitoring and detection
Security Architect: incident response procedures
Compliance Expert: security metrics and reporting
```

**Activities:**
- Implement security information and event management (SIEM)
- Set up real-time threat detection and alerting
- Create incident response procedures and playbooks
- Implement security analytics and anomaly detection
- Design security metrics and KPI tracking

## Integration Patterns

### **SuperClaude Command Integration**

| Command | Use Case | Output |
|---------|---------|--------|
| `/sc:design --type authentication` | Authentication system | Complete auth architecture |
| `/sc:design --type authorization` | Authorization framework | RBAC/ABAC implementation |
| `/sc:implement security` | Security controls | Production-ready security |
| `/sc:analyze threats` | Threat analysis | Threat model and mitigation |
| `/sc:implement compliance` | Compliance | Regulatory compliance system |

### **Security Framework Integration**

| Framework | Role | Capabilities |
|-----------|------|------------|
| **OWASP Top 10** | Security standards | Comprehensive vulnerability protection |
| **NIST Cybersecurity** | Security framework | Complete security program implementation |
| **ISO 27001** | Compliance management | Information security management system |
| **Zero Trust** | Security model | Zero-trust architecture implementation |

### **MCP Server Integration**

| Server | Expertise | Use Case |
|--------|----------|---------|
| **Sequential** | Security reasoning | Complex security analysis and design |
| **Better Auth** | Authentication | Modern authentication implementation |
| **Web Search** | Threat intelligence | Latest security threats and vulnerabilities |

## Usage Examples

### Example 1: Complete Authentication System
```
User: "Implement a secure authentication system for our SaaS application with MFA and SSO support"

Workflow:
1. Phase 1: Analyze security requirements and compliance needs
2. Phase 2: Design OAuth 2.0/OpenID Connect authentication system
3. Phase 3: Implement RBAC with fine-grained permissions
4. Phase 4: Integrate with SSO providers and MFA services
5. Phase 5: Set up audit logging and compliance reporting
6. Phase 6: Implement threat detection and security monitoring

Output: Production-ready authentication system with enterprise-grade security
```

### Example 2: Security Compliance Implementation
```
User: "Implement SOC 2 compliance for our financial services platform"

Workflow:
1. Phase 1: Analyze SOC 2 requirements and current security posture
2. Phase 2: Design security controls to meet SOC 2 criteria
3. Phase 3: Implement access controls and audit trails
4. Phase 4: Set up security monitoring and incident response
5. Phase 5: Create compliance documentation and reporting
6. Phase 6: Implement continuous compliance monitoring

Output: SOC 2 compliant security framework with comprehensive audit capabilities
```

### Example 3: API Security Implementation
```
User: "Secure our REST API with proper authentication, authorization, and threat protection"

Workflow:
1. Phase 1: Analyze API security requirements and threat model
2. Phase 2: Design JWT-based authentication and authorization
3. Phase 3: Implement API gateway with security controls
4. Phase 4: Add rate limiting, input validation, and encryption
5. Phase 5: Set up API security monitoring and logging
6. Phase 6: Implement API security testing and validation

Output: Secure API with comprehensive protection against common attacks
```

## Quality Assurance Mechanisms

### **Multi-Layer Security Validation**
- **Security Architecture Review**: Comprehensive security design validation
- **Penetration Testing**: Automated and manual security testing
- **Compliance Validation**: Regulatory compliance verification
- **Threat Assessment**: Ongoing threat analysis and mitigation

### **Automated Security Checks**
- **Vulnerability Scanning**: Automated security vulnerability detection
- **Compliance Monitoring**: Continuous compliance checking and reporting
- **Security Testing**: Automated security test execution and validation
- **Access Control Validation**: Permission and access right verification

### **Continuous Security Improvement**
- **Security Metrics**: Ongoing security performance tracking
- **Threat Intelligence**: Continuous threat monitoring and adaptation
- **Security Training**: Security awareness and best practices
- **Incident Learning**: Post-incident analysis and improvement

## Output Deliverables

### Primary Deliverable: Complete Security System
```
security-system/
├── authentication/
│   ├── providers/               # Authentication provider implementations
│   ├── middleware/              # Auth middleware and guards
│   ├── tokens/                  # Token generation and validation
│   └── sessions/                # Session management
├── authorization/
│   ├── rbac/                    # Role-based access control
│   ├── permissions/             # Permission definitions
│   ├── policies/                # Access control policies
│   └── admin/                   # Admin interfaces
├── security/
│   ├── encryption/              # Encryption utilities
│   ├── validation/              # Input validation and sanitization
│   ├── headers/                 # Security headers and CORS
│   └── rate-limiting/           # Rate limiting and DDoS protection
├── compliance/
│   ├── audit-logs/              # Audit logging and tracking
│   ├── reports/                 # Compliance reports
│   ├── policies/                # Security policies and procedures
│   └── documentation/           # Compliance documentation
├── monitoring/
│   ├── siem/                    # Security information and event management
│   ├── alerts/                  # Security alerts and notifications
│   ├── dashboards/              # Security monitoring dashboards
│   └── incident-response/       # Incident response procedures
└── config/
    ├── development/             # Development security config
    ├── staging/                 # Staging security config
    └── production/              # Production security config
```

### Supporting Artifacts
- **Security Architecture Documentation**: Detailed security design and implementation
- **Compliance Reports**: Regulatory compliance status and documentation
- **Security Policies**: Comprehensive security policies and procedures
- **Threat Models**: Detailed threat analysis and mitigation strategies
- **Incident Response Plans**: Security incident handling procedures

## Advanced Features

### **Intelligent Threat Detection**
- AI-powered threat detection and analysis
- Behavioral anomaly detection and user behavior analytics
- Real-time threat intelligence integration
- Automated incident response and containment

### **Zero Trust Implementation**
- Comprehensive zero-trust security architecture
- Continuous authentication and authorization
- Micro-segmentation and least privilege access
- Device and location-based access controls

### **Compliance Automation**
- Automated compliance checking and reporting
- Continuous compliance monitoring and alerts
- Automated evidence collection for audits
- Regulatory requirement tracking and management

### **Security Analytics**
- Advanced security analytics and reporting
- Security metrics and KPI tracking
- Risk assessment and scoring
- Security posture analysis and improvement

## Troubleshooting

### Common Security Implementation Challenges
- **Authentication Issues**: Use proper token validation and secure session management
- **Authorization Problems**: Implement clear permission models and regular access reviews
- **Compliance Gaps**: Conduct regular compliance assessments and documentation updates
- **Security Vulnerabilities**: Implement continuous security testing and vulnerability management

### Integration and Operational Issues
- **Third-party Integration**: Use standard protocols and proper error handling
- **Performance Impact**: Optimize security controls and implement caching where appropriate
- **User Experience**: Balance security requirements with user-friendly interfaces
- **Security Monitoring**: Implement comprehensive logging and alerting systems

## Best Practices

### **For Authentication Design**
- Use industry-standard protocols (OAuth 2.0, OpenID Connect, SAML)
- Implement multi-factor authentication for sensitive operations
- Use secure token storage and proper session management
- Implement proper password policies and secure recovery mechanisms

### **For Authorization Implementation**
- Follow principle of least privilege
- Implement role-based or attribute-based access control
- Regularly review and update access permissions
- Implement proper audit trails for access control changes

### **For Security Compliance**
- Stay updated with regulatory requirements and industry standards
- Implement comprehensive audit logging and documentation
- Conduct regular security assessments and penetration testing
- Maintain up-to-date security policies and procedures

### **For Threat Protection**
- Implement defense-in-depth security architecture
- Use automated security monitoring and threat detection
- Maintain incident response procedures and conduct regular drills
- Stay informed about latest security threats and vulnerabilities

---

This security and authentication skill transforms the complex process of security system implementation into a guided, expert-supported workflow that ensures comprehensive protection, regulatory compliance, and operational excellence.