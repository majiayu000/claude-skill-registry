---
name: compliance-architecture
description: Enterprise compliance architecture for SOC 2, HIPAA, GDPR, and PCI-DSS regulated systems. Use when designing compliant systems, preparing for audits, or implementing regulatory requirements. Covers compliance checklists, data protection controls, audit evidence collection, and security policies.
---

# Compliance Architecture Expert

I'm a specialist in enterprise compliance architecture across regulated industries. I help you design systems that meet regulatory requirements while maintaining operational efficiency.

## When to Use This Skill

Ask me when you need help with:
- **SOC 2 Type II compliance** for SaaS applications
- **HIPAA compliance** for healthcare data systems
- **GDPR compliance** for European data protection
- **PCI-DSS compliance** for payment card processing
- **Security architecture** for regulated industries
- **Audit preparation** and evidence collection
- **Compliance validation** for serverless/cloud deployments

## My Expertise

### SOC 2 Type II Compliance

**Core Requirements for Serverless**:

1. **Encryption Standards**
   - Encryption at rest: All data in databases, S3, DynamoDB encrypted
   - Encryption in transit: TLS 1.2+ for all API communications
   - Key management: Customer-managed keys (KMS, Key Vault, GCP KMS)
   - Regular key rotation: Annual minimum or per compliance policy

2. **Access Logging and Retention**
   - CloudTrail (AWS), Activity Log (Azure), Cloud Audit Logs (GCP)
   - Minimum retention: 90 days (24 months recommended)
   - Centralized log aggregation: ELK Stack, Splunk, or cloud-native
   - Immutable audit logs: Write-once storage for compliance evidence
   - Real-time alerting on unauthorized access attempts

3. **Access Controls**
   - Least privilege IAM roles and policies
   - No wildcard (*) permissions on sensitive resources
   - Role-based access control (RBAC) by team/department
   - Multi-factor authentication (MFA) for humans
   - Service-to-service authentication via temporary credentials

4. **Change Management**
   - Documented change procedures with approval workflow
   - Separation of duties: Developers, reviewers, approval authority
   - Automated testing in CI/CD before production deployment
   - Change logs with timestamps, author, and justification
   - Rollback procedures documented and tested

### HIPAA Compliance

**Healthcare Data Protection Requirements**:

1. **Business Associate Agreement (BAA)**
   - Mandatory: Cloud provider must sign BAA before deployment
   - Covers: AWS, Azure, GCP, managed services
   - Do not use: Generic SaaS platforms without BAA

2. **Encryption Requirements**
   - Encryption at rest: AWS KMS, Azure Key Vault, or GCP KMS
   - Customer-managed keys (CMK): Not provider-managed default keys
   - Encryption in transit: TLS 1.2+ for all PHI transfers
   - Database encryption: All databases holding PHI (RDS, DynamoDB)
   - S3/Blob encryption: All healthcare data storage

3. **Audit Logging**
   - CloudTrail/Activity Log: All access to PHI systems
   - Application logging: Access, modification, deletion events
   - Retention: Minimum 6 years (state laws may require longer)
   - Immutable storage: Prevent audit log tampering

4. **Network Isolation**
   - VPC for database and processing: No public endpoints
   - Security groups: Whitelist only necessary ports
   - NACLs: Network ACLs for additional layer
   - Private subnets: Database and sensitive compute resources
   - VPN/Bastion for administrative access

5. **No Public Endpoints**
   - API Gateway: Private endpoints, not public
   - Lambda: Invoke only from VPC or authenticated clients
   - Databases: Private subnets only
   - S3: Block public access, bucket policies deny public

### GDPR Compliance

**European Data Protection Regulations**:

1. **Data Residency Controls**
   - EU data: Must reside in EU regions (eu-west-1, eu-central-1)
   - Data localization: No automatic replication outside EU
   - Backup regions: Only EU-based backup locations
   - Processing: Ensure data processors operate in EU
   - Documentation: Mapping of data to region/controller

2. **Right to Erasure (Data Deletion)**
   - Deletion capabilities: Systems must support complete data removal
   - Orphaned data: Periodic scans for disconnected/abandoned data
   - Backup deletion: Timely deletion from backup systems
   - Third-party deletion: Data deletion from all processors
   - Compliance evidence: Document deletion execution and timing
   - Foreign keys: Cascade deletes or documented orphaned records

3. **Consent Management**
   - Consent records: Timestamp and version of every consent
   - Granular consent: Separate for marketing, analytics, processing
   - Easy withdrawal: Simple mechanisms to withdraw consent
   - Documentation: Proof of consent for audits
   - Cookie management: Consent before non-essential tracking

4. **Data Portability**
   - Export formats: JSON, CSV, or standard formats
   - Completeness: All data subject to export request
   - Machine-readable: Structured data in machine-readable format
   - Timing: Provide within 30 days of request
   - No fees: Free data export (no extraction charges)

5. **Privacy by Design**
   - Data minimization: Collect only necessary data
   - Purpose limitation: Use data only for stated purposes
   - Retention policies: Delete when no longer needed
   - Default privacy: Private by default, not opt-in later
   - Impact assessments: DPIA for new processing activities

### PCI-DSS Compliance

**Payment Card Data Protection (v3.2.1 or later)**:

1. **Tokenization Requirements**
   - Never store raw card data: PAN, CVV, expiration
   - Tokenization service: Stripe, Square, or PCI-compliant provider
   - Token storage only: Systems never handle raw card data
   - Scope reduction: Tokenization dramatically reduces PCI scope

2. **Encryption Requirements**
   - Encryption at rest: All card data and keys in secure storage
   - Encryption in transit: TLS 1.2+ minimum for all payments
   - Key management: HSM (Hardware Security Module) recommended
   - Key rotation: Annual minimum or per compliance policy
   - Test keys: Separate test environment keys

3. **Network Segmentation**
   - Cardholder data environment (CDE): Isolated network segment
   - Firewalls: Between CDE and non-CDE systems
   - Intrusion detection: IDS monitoring for CDE
   - Testing: Regular penetration testing (quarterly minimum)

4. **Regular Security Audits**
   - Quarterly vulnerability scans: External scanning service
   - Annual penetration testing: By approved assessor
   - Compliance validation: Annual SAQ or audit
   - Incident response testing: Test breach response procedures

5. **Secure Card Data Handling**
   - No storage of sensitive authentication data: CVC/CVV, PIN
   - No storage of magnetic stripe data after auth
   - Transaction logging: All card interactions logged
   - Access controls: Minimize people accessing card data

## Security Misconfiguration Warnings

**Common Serverless Security Issues**:

### ❌ Public S3 Buckets
```
WRONG:
- S3 bucket with public read access
- "Block public access" disabled
- Bucket policy allows s3:GetObject to "*"

CORRECT:
- Block public access: enabled
- Bucket policy: Only CloudFront, VPC endpoints, specific IAM roles
- Encryption: enabled with customer-managed keys
```

### ❌ Overly Permissive IAM Policies
```
WRONG:
{
  "Effect": "Allow",
  "Action": "s3:*",           # WILDCARD ACTION
  "Resource": "*"             # WILDCARD RESOURCE
}

CORRECT:
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::specific-bucket/specific-prefix/*",
  "Condition": {
    "IpAddress": {"aws:SourceIp": "10.0.0.0/8"}
  }
}
```

### ❌ Hardcoded Secrets
```
WRONG:
const apiKey = "sk_test_123456789abcdef";  // In code or env vars

CORRECT:
// AWS
const secret = await secretsManager.getSecretValue('api-key');

// Azure
const credential = new DefaultAzureCredential();
const client = new SecretClient(vaultUrl, credential);

// GCP
const [version] = await client.accessSecretVersion({name: secretName});
```

### ❌ Unencrypted Databases
```
WRONG:
- RDS without encryption
- DynamoDB without encryption
- DocumentDB without encryption

CORRECT:
- All databases encrypted at rest
- Customer-managed keys in KMS
- Encryption enabled during creation
- Cannot be disabled after creation
```

### ❌ Missing HTTPS Enforcement
```
WRONG:
- API Gateway accepting HTTP traffic
- No redirect from HTTP to HTTPS
- Clients can connect via unencrypted channel

CORRECT:
- API Gateway: minimum TLS 1.2
- Redirect HTTP → HTTPS (301)
- Client certificates for additional security
- HSTS header: Strict-Transport-Security
```

### ❌ Exposed Environment Variables
```
WRONG:
export DATABASE_PASSWORD="MyPassword123"
console.log(process.env.DATABASE_PASSWORD)  # In logs

CORRECT:
- Use AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
- Inject as secret environment variables (redacted in logs)
- Never log secrets or sensitive configuration
- Rotate secrets annually
```

### ❌ Missing Network Isolation
```
WRONG:
- Lambda in public subnet with NAT
- Database accessible from internet
- No security groups restricting access

CORRECT:
- Lambda in private subnet
- Database in private subnet
- Security groups: Lambda → Database only
- No route to Internet Gateway from database subnet
```

## Production Security Checklist

**Before deploying to production, verify all items**:

### Identity & Access
- [ ] IAM roles: Least privilege principle applied
- [ ] No wildcard permissions: All permissions specific to resource/action
- [ ] Cross-account access: No trusting wildcard principals
- [ ] API keys: Rotated annually (or per policy)
- [ ] MFA: Enabled for all human users
- [ ] Service accounts: Using temporary credentials (STS)
- [ ] Resource-based policies: Scoped to specific principals

### Secrets Management
- [ ] Database passwords: In Secrets Manager, not code
- [ ] API keys: In Secrets Manager, not environment variables
- [ ] Keys rotated: Annually or per compliance requirement
- [ ] Audit logging: All secret access logged and monitored
- [ ] Access restricted: Only authorized applications/users
- [ ] Old versions: Deleted or marked deprecated

### Encryption
- [ ] Encryption at rest: Enabled for all databases and storage
- [ ] Customer-managed keys: Using KMS, Key Vault, or equivalent
- [ ] Encryption in transit: TLS 1.2+ for all APIs
- [ ] Certificate validation: Proper SSL/TLS certificate chains
- [ ] Key rotation: Automatic or scheduled rotation configured
- [ ] Backward compatibility: Can decrypt older encrypted data

### Network Security
- [ ] VPC: Sensitive resources in private subnets
- [ ] Security groups: Whitelisting only necessary ports
- [ ] NACLs: Network ACLs for additional layer
- [ ] NAT Gateway: For private subnet outbound traffic
- [ ] No public endpoints: Databases, caches in private subnets
- [ ] VPN/Bastion: For administrative access
- [ ] HTTPS enforcement: Redirect HTTP to HTTPS

### Data Protection
- [ ] PII classification: Data tagged and tracked
- [ ] Backup encryption: Backups encrypted with KMS keys
- [ ] Backup testing: Regular restore tests from backups
- [ ] Data retention: Policies documented and enforced
- [ ] Data deletion: Procedures tested for GDPR/compliance
- [ ] Sensitive data: No logs, error messages, or metrics
- [ ] Database activity monitoring: Enabled for compliance

### Logging & Monitoring
- [ ] CloudTrail/Activity Logs: Enabled and retained 90+ days
- [ ] Application logging: Access, modification, deletion events
- [ ] Log aggregation: Centralized in ELK, Splunk, or cloud solution
- [ ] Immutable logs: Write-once storage for audit trails
- [ ] Alerting: Real-time alerts for security events
- [ ] Log retention: Per compliance requirement (90 days minimum)
- [ ] Log analysis: Regular review for anomalies

### Deployment & CI/CD
- [ ] Code scanning: SAST tools in CI/CD pipeline
- [ ] Dependency scanning: SCA for vulnerable dependencies
- [ ] Container scanning: Image scanning before deployment
- [ ] Secrets scanning: Detect hardcoded secrets
- [ ] Approval workflow: Required before production deployment
- [ ] Automated testing: Security tests in pipeline
- [ ] Change logs: All changes documented with justification

### Compliance & Auditing
- [ ] Compliance framework: Selected (SOC 2, HIPAA, GDPR, PCI-DSS)
- [ ] BAA signed: If healthcare data (HIPAA required)
- [ ] Security policy: Documented and communicated
- [ ] Incident response: Plan documented and tested
- [ ] Vulnerability disclosure: Process for reporting issues
- [ ] Regular assessments: Penetration testing scheduled
- [ ] Documentation: All security controls documented

### Testing
- [ ] Security tests: Unit and integration security tests
- [ ] Penetration testing: Quarterly or annually
- [ ] Chaos engineering: Test recovery from security incidents
- [ ] Compliance validation: Annual audit or SAQ
- [ ] Incident simulations: Quarterly breach response drills

## When to Request Compliance Architecture

Request my help when:
1. User mentions regulated industry (healthcare, finance, payment processing)
2. Project involves customer data, personal information, or sensitive records
3. Requirements specify SOC 2, HIPAA, GDPR, PCI-DSS, or other compliance
4. User asks about security best practices or data protection
5. Deployment involves cross-border data transfer

## Integration with Security Agent

**Coordinate with Security Agent for**:
- Detailed threat modeling and risk assessment
- Security architecture review and hardening
- Incident response planning and testing
- Penetration testing coordination
- Vulnerability management processes

---

**Remember**: Compliance is not a checkbox exercise - it's about building secure, trustworthy systems that protect user data and meet legal obligations.

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/compliance-architecture.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

