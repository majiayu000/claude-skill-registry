---
name: pytm
description: >
  Python-based threat modeling using pytm library for programmatic STRIDE analysis,
  data flow diagram generation, and automated security threat identification. Use when:
  (1) Creating threat models programmatically using Python code, (2) Generating data flow
  diagrams (DFDs) with automatic STRIDE threat identification, (3) Integrating threat
  modeling into CI/CD pipelines and shift-left security practices, (4) Analyzing system
  architecture for security threats across trust boundaries, (5) Producing threat reports
  with STRIDE categories and mitigation recommendations, (6) Maintaining threat models
  as code for version control and automation.
version: 0.1.0
maintainer: SirAppSec
category: threatmodel
tags: [threat-modeling, stride, dfd, security-architecture, pytm, appsec, risk-analysis]
frameworks: [STRIDE, OWASP, MITRE-ATT&CK, NIST]
dependencies:
  python: ">=3.7"
  packages: [pytm, graphviz]
references:
  - https://github.com/izar/pytm
  - https://owasp.org/www-community/Threat_Modeling
  - https://www.microsoft.com/en-us/security/blog/2007/09/11/stride-chart/
  - https://attack.mitre.org/
---

# Threat Modeling with pytm

## Overview

pytm is a Python library for programmatic threat modeling based on the STRIDE methodology. It enables
security engineers to define system architecture as code, automatically generate data flow diagrams (DFDs),
identify security threats across trust boundaries, and produce comprehensive threat reports. This
approach integrates threat modeling into CI/CD pipelines, enabling shift-left security and continuous
threat analysis.

## Quick Start

Create a basic threat model:

```python
#!/usr/bin/env python3
from pytm import TM, Server, Dataflow, Boundary, Actor

# Initialize threat model
tm = TM("Web Application Threat Model")
tm.description = "E-commerce web application"

# Define trust boundaries
internet = Boundary("Internet")
dmz = Boundary("DMZ")
internal = Boundary("Internal Network")

# Define actors and components
user = Actor("Customer")
user.inBoundary = internet

web = Server("Web Server")
web.inBoundary = dmz

db = Server("Database")
db.inBoundary = internal

# Define data flows
user_to_web = Dataflow(user, web, "HTTPS Request")
user_to_web.protocol = "HTTPS"
user_to_web.data = "credentials, payment info"
user_to_web.isEncrypted = True

web_to_db = Dataflow(web, db, "Database Query")
web_to_db.protocol = "SQL/TLS"
web_to_db.data = "user data, transactions"

# Generate threat report and diagram
tm.process()
```

Install pytm:
```bash
pip install pytm
# Also requires graphviz for diagram generation
brew install graphviz  # macOS
# or: apt-get install graphviz  # Linux
```

## Core Workflows

### Workflow 1: Create New Threat Model

Progress:
[ ] 1. Define system scope and trust boundaries
[ ] 2. Identify all actors (users, administrators, external systems)
[ ] 3. Map system components (servers, databases, APIs, services)
[ ] 4. Define data flows between components with security attributes
[ ] 5. Run `tm.process()` to generate threats and DFD
[ ] 6. Review STRIDE threats and add mitigations
[ ] 7. Generate threat report with `scripts/generate_report.py`

Work through each step systematically. Check off completed items.

### Workflow 2: STRIDE Threat Analysis

pytm automatically identifies threats based on STRIDE categories:

- **Spoofing**: Identity impersonation attacks
- **Tampering**: Unauthorized modification of data
- **Repudiation**: Denial of actions without traceability
- **Information Disclosure**: Unauthorized access to sensitive data
- **Denial of Service**: Availability attacks
- **Elevation of Privilege**: Unauthorized access escalation

For each identified threat:
1. Review threat description and affected component
2. Assess likelihood and impact (use `references/risk_matrix.md`)
3. Determine if existing controls mitigate the threat
4. Add mitigation using `threat.mitigation = "description"`
5. Document residual risk and acceptance criteria

### Workflow 3: Architecture as Code

Define system architecture programmatically:

```python
from pytm import TM, Server, Datastore, Dataflow, Boundary, Actor, Lambda

tm = TM("Microservices Architecture")

# Cloud boundaries
internet = Boundary("Internet")
cloud_vpc = Boundary("Cloud VPC")

# API Gateway
api_gateway = Server("API Gateway")
api_gateway.inBoundary = cloud_vpc
api_gateway.implementsAuthentication = True
api_gateway.implementsAuthorization = True

# Microservices
auth_service = Lambda("Auth Service")
auth_service.inBoundary = cloud_vpc

order_service = Lambda("Order Service")
order_service.inBoundary = cloud_vpc

# Data stores
user_db = Datastore("User Database")
user_db.inBoundary = cloud_vpc
user_db.isEncryptedAtRest = True

# Data flows with security properties
client_to_api = Dataflow(Actor("Client"), api_gateway, "API Request")
client_to_api.protocol = "HTTPS"
client_to_api.isEncrypted = True
client_to_api.data = "user credentials, orders"

api_to_auth = Dataflow(api_gateway, auth_service, "Auth Check")
api_to_auth.protocol = "gRPC/TLS"

auth_to_db = Dataflow(auth_service, user_db, "User Lookup")
auth_to_db.protocol = "TLS"

tm.process()
```

### Workflow 4: CI/CD Integration

Automate threat modeling in continuous integration:

```yaml
# .github/workflows/threat-model.yml
name: Threat Model Analysis
on: [push, pull_request]

jobs:
  threat-model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install pytm
          sudo apt-get install -y graphviz

      - name: Generate threat model
        run: python threat_model.py

      - name: Upload DFD diagram
        uses: actions/upload-artifact@v3
        with:
          name: threat-model-dfd
          path: '*.png'

      - name: Check for unmitigated threats
        run: python scripts/check_mitigations.py threat_model.py
```

### Workflow 5: Threat Report Generation

Generate comprehensive threat documentation:

```bash
# Run threat model with report generation
python threat_model.py

# Generate markdown report
./scripts/generate_report.py --model threat_model.py --output threat_report.md

# Generate JSON for tool integration
./scripts/generate_report.py --model threat_model.py --format json --output threats.json
```

Report includes:
- System architecture overview
- Trust boundary analysis
- Complete STRIDE threat enumeration
- Existing and recommended mitigations
- Risk prioritization matrix

## Security Considerations

### Sensitive Data Handling

- **Threat models as code**: Store in version control but review for sensitive architecture details
- **Credentials and secrets**: Never hardcode in threat models - use placeholders
- **Data classification**: Clearly label data flows with sensitivity levels (PII, PCI, PHI)
- **Report distribution**: Control access to threat reports revealing security architecture

### Access Control

- **Threat model repository**: Restrict write access to security team and architects
- **CI/CD integration**: Protect threat modeling pipeline from tampering
- **Diagram artifacts**: Control distribution of DFDs showing system architecture
- **Mitigation tracking**: Integrate with secure issue tracking systems

### Audit Logging

Log the following for security governance:
- Threat model creation and modification history
- Identified threats and severity assessments
- Mitigation implementation and validation
- Risk acceptance decisions with approval
- Threat model review and update cycles

### Compliance Requirements

- **NIST 800-30**: Risk assessment methodology alignment
- **ISO 27001**: A.14.1.2 - Securing application services on public networks
- **OWASP SAMM**: Threat Assessment practice maturity
- **PCI-DSS 6.3.1**: Security threat identification in development
- **SOC2 CC9.1**: Risk assessment process for system changes

## Bundled Resources

### Scripts (`scripts/`)

- `generate_report.py` - Generate markdown/JSON threat reports with STRIDE categorization
- `check_mitigations.py` - Validate all identified threats have documented mitigations
- `threat_classifier.py` - Classify threats by severity using DREAD or custom risk matrix
- `template_generator.py` - Generate threat model templates for common architectures

### References (`references/`)

- `stride_methodology.md` - Complete STRIDE methodology guide with threat examples
- `risk_matrix.md` - Risk assessment framework with likelihood and impact scoring
- `component_library.md` - Reusable pytm components for common patterns (APIs, databases, cloud services)
- `mitigation_strategies.md` - Common mitigation patterns mapped to STRIDE categories and OWASP controls

### Assets (`assets/`)

- `templates/web_application.py` - Web application threat model template
- `templates/microservices.py` - Microservices architecture template
- `templates/mobile_app.py` - Mobile application threat model template
- `templates/iot_system.py` - IoT system threat model template
- `dfd_styles.json` - Custom graphviz styling for professional diagrams

## Common Patterns

### Pattern 1: Web Application Three-Tier Architecture

```python
from pytm import TM, Server, Datastore, Dataflow, Boundary, Actor

tm = TM("Three-Tier Web Application")

# Boundaries
internet = Boundary("Internet")
dmz = Boundary("DMZ")
internal = Boundary("Internal Network")

# Components
user = Actor("End User")
user.inBoundary = internet

lb = Server("Load Balancer")
lb.inBoundary = dmz
lb.implementsNonce = True

web = Server("Web Server")
web.inBoundary = dmz
web.implementsAuthentication = True
web.implementsAuthenticationOut = False

app = Server("Application Server")
app.inBoundary = internal
app.implementsAuthorization = True

db = Datastore("Database")
db.inBoundary = internal
db.isSQL = True
db.isEncryptedAtRest = True

# Data flows
Dataflow(user, lb, "HTTPS").isEncrypted = True
Dataflow(lb, web, "HTTPS").isEncrypted = True
Dataflow(web, app, "HTTP").data = "session token, requests"
Dataflow(app, db, "SQL/TLS").data = "user data, transactions"

tm.process()
```

### Pattern 2: Cloud Native Microservices

```python
from pytm import TM, Lambda, Datastore, Dataflow, Boundary, Actor

tm = TM("Cloud Microservices")

cloud = Boundary("Cloud Provider VPC")
user = Actor("Mobile App")

# Serverless functions
api_gateway = Lambda("API Gateway")
api_gateway.inBoundary = cloud
api_gateway.implementsAPI = True

auth_fn = Lambda("Auth Function")
auth_fn.inBoundary = cloud

# Managed services
cache = Datastore("Redis Cache")
cache.inBoundary = cloud
cache.isEncrypted = True

db = Datastore("DynamoDB")
db.inBoundary = cloud
db.isEncryptedAtRest = True

# Data flows
Dataflow(user, api_gateway, "API Call").protocol = "HTTPS"
Dataflow(api_gateway, auth_fn, "Auth").protocol = "internal"
Dataflow(auth_fn, cache, "Session").isEncrypted = True
Dataflow(api_gateway, db, "Query").isEncrypted = True

tm.process()
```

### Pattern 3: Adding Custom Threats

Define organization-specific threats:

```python
from pytm import TM, Threat

tm = TM("Custom Threat Model")

# Add custom threat to component
web_server = Server("Web Server")

custom_threat = Threat(
    target=web_server,
    id="CUSTOM-001",
    description="API rate limiting bypass using distributed requests",
    condition="web_server.implementsRateLimiting is False",
    mitigation="Implement distributed rate limiting with Redis",
    references="OWASP API Security Top 10 - API4 Unrestricted Resource Consumption"
)

web_server.threats.append(custom_threat)
```

### Pattern 4: Trust Boundary Analysis

Focus on cross-boundary threats:

```python
# Identify all trust boundary crossings
for flow in tm.dataflows:
    if flow.source.inBoundary != flow.sink.inBoundary:
        print(f"Cross-boundary flow: {flow.name}")
        print(f"  From: {flow.source.inBoundary.name}")
        print(f"  To: {flow.sink.inBoundary.name}")
        print(f"  Encrypted: {flow.isEncrypted}")
        print(f"  Authentication: {flow.implementsAuthentication}")
```

Trust boundary crossings require extra scrutiny:
- Authentication and authorization mechanisms
- Encryption in transit
- Input validation and sanitization
- Logging and monitoring

## Integration Points

### SDLC Integration

- **Design Phase**: Create initial threat model during architecture review
- **Development**: Reference threat model for security requirements
- **Code Review**: Validate mitigations are implemented correctly
- **Testing**: Generate security test cases from identified threats
- **Deployment**: Validate security controls match threat model assumptions
- **Operations**: Update threat model for infrastructure changes

### Security Tools Ecosystem

- **Issue Tracking**: Export threats as Jira/GitHub issues for mitigation tracking
- **Documentation**: Generate threat models for security documentation
- **SIEM**: Map threats to detection rules and monitoring alerts
- **Pentesting**: Provide threat model to pentesters for targeted assessment
- **Code Analysis**: Link SAST/DAST findings to threat model threats

### Cloud and DevOps

- **Infrastructure as Code**: Threat model Terraform/CloudFormation templates
- **Container Security**: Model container orchestration and service mesh
- **API Design**: Threat model API gateway and microservices communication
- **Secrets Management**: Model key management and secrets distribution

## Troubleshooting

### Issue: Missing Threats in Output

**Symptoms**: Expected STRIDE threats not appearing in generated report

**Solution**:
1. Verify component properties are set correctly (e.g., `isSQL=True` for databases)
2. Check data flow security attributes (`isEncrypted`, `protocol`)
3. Ensure components are assigned to boundaries
4. Review trust boundary crossings
5. Consult `references/stride_methodology.md` for threat conditions

### Issue: Diagram Generation Failure

**Symptoms**: DFD not generated or graphviz errors

**Solution**:
```bash
# Verify graphviz installation
dot -V

# Install graphviz if missing
brew install graphviz  # macOS
sudo apt-get install graphviz  # Linux

# Test pytm with simple model
python -c "from pytm import TM; tm = TM('test'); tm.process()"
```

### Issue: Too Many False Positive Threats

**Symptoms**: Identified threats don't apply to your architecture

**Solution**:
1. Set accurate component properties to suppress irrelevant threats
2. Use threat conditions to filter: `threat.condition = "..."`
3. Document why threats don't apply: `threat.mitigation = "N/A - using managed service"`
4. Create custom threat library with `references/component_library.md`

### Issue: Threat Model Maintenance Drift

**Symptoms**: Threat model doesn't reflect current architecture

**Solution**:
1. Store threat models in version control alongside architecture diagrams
2. Trigger threat model regeneration in CI on architecture changes
3. Schedule quarterly threat model reviews
4. Link threat model updates to architecture review board approvals
5. Use `scripts/check_mitigations.py` to validate completeness

## Advanced Configuration

### Custom Threat Definitions

Create organization-specific threat library:

```python
# custom_threats.py
from pytm import Threat

def add_custom_threats(tm):
    """Add organization-specific threats to threat model"""

    # Cloud-specific threats
    cloud_misconfiguration = Threat(
        id="CLOUD-001",
        description="Misconfigured cloud storage bucket exposes sensitive data",
        condition="datastore.inBoundary.name == 'Cloud' and not datastore.isEncrypted",
        mitigation="Enable encryption at rest and bucket policies"
    )

    # API-specific threats
    api_abuse = Threat(
        id="API-001",
        description="API endpoint abuse through lack of rate limiting",
        condition="server.implementsAPI and not server.implementsRateLimiting",
        mitigation="Implement rate limiting and API key rotation"
    )

    return [cloud_misconfiguration, api_abuse]
```

### Risk Scoring Integration

Add DREAD scoring to threats:

```python
class ScoredThreat(Threat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = 0        # 0-10
        self.reproducibility = 0
        self.exploitability = 0
        self.affected_users = 0
        self.discoverability = 0

    def dread_score(self):
        return (self.damage + self.reproducibility + self.exploitability +
                self.affected_users + self.discoverability) / 5

# Usage
threat = ScoredThreat(
    target=component,
    description="SQL Injection",
    damage=9,
    reproducibility=8,
    exploitability=7,
    affected_users=10,
    discoverability=6
)
print(f"DREAD Score: {threat.dread_score()}/10")
```

### Diagram Customization

Customize DFD output with graphviz attributes:

```python
# Set custom colors for trust boundaries
internet.color = "red"
dmz.color = "orange"
internal.color = "green"

# Customize diagram output
tm.graph_options = {
    "rankdir": "LR",  # Left to right layout
    "bgcolor": "white",
    "fontname": "Arial",
    "fontsize": "12"
}
```

## References

- [pytm GitHub Repository](https://github.com/izar/pytm)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [Microsoft STRIDE Methodology](https://www.microsoft.com/en-us/security/blog/2007/09/11/stride-chart/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)
- [NIST 800-30: Risk Assessment](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final)
