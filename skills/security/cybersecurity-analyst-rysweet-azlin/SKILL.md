---
name: cybersecurity-analyst
version: 1.0.0
description: |
  Analyzes events through cybersecurity lens using threat modeling, attack surface analysis, defense-in-depth,
  zero-trust architecture, and risk-based frameworks (CIA triad, STRIDE, MITRE ATT&CK).
  Provides insights on vulnerabilities, attack vectors, defense strategies, incident response, and security posture.
  Use when: Security incidents, vulnerability assessments, threat analysis, security architecture, compliance.
  Evaluates: Confidentiality, integrity, availability, threat actors, attack patterns, controls, residual risk.
---

# Cybersecurity Analyst Skill

## Purpose

Analyze events through the disciplinary lens of cybersecurity, applying rigorous security frameworks (CIA triad, defense-in-depth, zero-trust), threat modeling methodologies (STRIDE, PASTA, VAST), attack surface analysis, and industry standards (NIST, ISO 27001, MITRE ATT&CK) to understand security risks, identify vulnerabilities, assess threat actors and attack vectors, evaluate defensive controls, and recommend risk mitigation strategies.

## When to Use This Skill

- **Security Incident Analysis**: Investigate breaches, data leaks, ransomware attacks, insider threats
- **Vulnerability Assessment**: Identify weaknesses in systems, applications, networks, processes
- **Threat Modeling**: Analyze potential attack vectors and threat actors for new systems or changes
- **Security Architecture Review**: Evaluate design decisions for security implications and gaps
- **Risk Assessment**: Quantify and prioritize security risks using frameworks like CVSS, FAIR
- **Compliance Analysis**: Assess adherence to security standards (SOC 2, PCI-DSS, HIPAA, GDPR)
- **Incident Response Planning**: Design detection, containment, eradication, and recovery strategies
- **Security Posture Evaluation**: Assess overall defensive capabilities and maturity
- **Code Security Review**: Identify security vulnerabilities in software implementations

## Core Philosophy: Security Thinking

Cybersecurity analysis rests on fundamental principles:

**Defense in Depth**: No single security control is perfect. Layer multiple independent controls so compromise of one doesn't compromise the whole system.

**Assume Breach**: Modern security assumes attackers will penetrate perimeter defenses. Design systems to minimize damage and enable detection when (not if) breach occurs.

**Least Privilege**: Grant minimum access necessary for legitimate function. Every excess permission is an opportunity for exploitation.

**Zero Trust**: Never trust, always verify. Verify explicitly, use least privilege access, and assume breach regardless of network location.

**Security by Design**: Security cannot be bolted on afterward. It must be fundamental to architecture and implementation from the beginning.

**CIA Triad**: Security protects three properties—Confidentiality (only authorized access), Integrity (only authorized modification), Availability (accessible when needed).

**Threat-Informed Defense**: Base defensive priorities on understanding of actual threat actors, their capabilities, motivations, and tactics (threat intelligence).

**Risk-Based Approach**: Perfect security is impossible. Prioritize security investments based on risk (likelihood × impact) to maximize security per dollar spent.

---

## Theoretical Foundations (Expandable)

### Foundation 1: CIA Triad (Classic Security Model)

**Components**:

**Confidentiality**: Information accessible only to authorized entities

- Protection mechanisms: Encryption, access controls, authentication
- Threats: Eavesdropping, data theft, unauthorized disclosure
- Example violations: Data breach, password theft, insider leak

**Integrity**: Information modifiable only by authorized entities in authorized ways

- Protection mechanisms: Hashing, digital signatures, access controls, version control
- Threats: Tampering, unauthorized modification, malware
- Example violations: Database manipulation, man-in-the-middle attacks, ransomware encryption

**Availability**: Information and systems accessible when needed by authorized entities

- Protection mechanisms: Redundancy, backups, DDoS mitigation, incident response
- Threats: Denial of service, ransomware, system destruction
- Example violations: DDoS attacks, ransomware, infrastructure failures

**Extensions**:

- **Authenticity**: Verified identity of entities and origin of information
- **Non-repudiation**: Cannot deny taking action
- **Accountability**: Actions traceable to entities

**Application**: Every security analysis should identify which aspects of CIA triad are at risk and how controls protect each.

**Sources**:

- [CIA Triad - Wikipedia](https://en.wikipedia.org/wiki/Information_security#Key_concepts)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Foundation 2: Defense in Depth (Layered Security)

**Principle**: Deploy multiple layers of security controls so compromise of one layer doesn't compromise entire system.

**Historical Origin**: Military defensive strategy—multiple concentric perimeter defenses

**Security Layers**:

1. **Physical**: Facility access controls, locked server rooms
2. **Network**: Firewalls, network segmentation, IDS/IPS
3. **Host**: Endpoint protection, host firewalls, patch management
4. **Application**: Input validation, secure coding, authentication
5. **Data**: Encryption at rest and in transit, DLP, tokenization
6. **Human**: Security awareness training, phishing simulation

**Key Insight**: Redundancy is not waste—it's resilience. Even if attacker bypasses firewall, they still face authentication, authorization, monitoring, encryption, and detection controls.

**Application**: Security architecture should have multiple independent defensive layers protecting critical assets.

**Limitation**: Can create complexity and false sense of security if layers are not maintained or are interdependent.

**Sources**:

- [Defense in Depth - NSA](https://www.nsa.gov/Press-Room/Cybersecurity-Advisories-Guidance/)
- [Layered Security - CISA](https://www.cisa.gov/topics/cybersecurity-best-practices)

### Foundation 3: Zero Trust Architecture

**Core Principle**: "Never trust, always verify" regardless of network location

**Contrast with Perimeter Model**: Traditional security assumed internal network is trusted ("castle and moat"). Zero trust assumes no network location is trusted.

**Key Tenets** (NIST SP 800-207):

1. **Verify explicitly**: Always authenticate and authorize based on all available data points
2. **Least privilege access**: Limit user access with Just-In-Time and Just-Enough-Access
3. **Assume breach**: Minimize blast radius and segment access; verify end-to-end encryption

**Components**:

- **Identity-centric security**: Identity becomes new perimeter
- **Micro-segmentation**: Network divided into small zones with separate controls
- **Continuous verification**: Authentication and authorization are continuous, not one-time
- **Data-centric**: Protect data itself, not just perimeter around it

**Drivers**:

- Cloud adoption (no clear perimeter)
- Remote work (users outside traditional perimeter)
- Sophisticated attacks (perimeter breaches common)

**Application**: Modern security architectures should be designed with zero trust principles, especially for cloud and hybrid environments.

**Sources**:

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Zero Trust - Microsoft Security](https://www.microsoft.com/en-us/security/business/zero-trust)

### Foundation 4: Threat Modeling

**Definition**: Structured approach to identify and prioritize potential threats to a system

**Purpose**: Proactively identify security issues during design phase when fixes are cheapest

**Benefits**:

- Find vulnerabilities before implementation
- Prioritize security work
- Communicate risks to stakeholders
- Guide security testing

**Common Methodologies**:

**STRIDE** (Microsoft):

- **S**poofing identity
- **T**ampering with data
- **R**epudiation
- **I**nformation disclosure
- **D**enial of service
- **E**levation of privilege

**PASTA** (Process for Attack Simulation and Threat Analysis):

- Seven-stage risk-centric methodology
- Aligns business objectives with technical requirements

**VAST** (Visual, Agile, and Simple Threat modeling):

- Scalable for agile development
- Two types: application threat models and operational threat models

**Application**: Use threat modeling for new features, architecture changes, or security reviews.

**Sources**:

- [Threat Modeling - OWASP](https://owasp.org/www-community/Threat_Modeling)
- [STRIDE Threat Model - Microsoft](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)

### Foundation 5: MITRE ATT&CK Framework

**Description**: Knowledge base of adversary tactics and techniques based on real-world observations

**Purpose**: Understand how attackers operate to inform defense, detection, and threat hunting

**Structure**:

- **Tactics**: High-level goals (e.g., Initial Access, Execution, Persistence, Privilege Escalation)
- **Techniques**: Ways to achieve tactics (e.g., Phishing, Exploiting Public Applications)
- **Sub-techniques**: Specific implementations
- **Procedures**: Specific attacker behaviors

**14 Tactics** (Enterprise Matrix):

1. Reconnaissance
2. Resource Development
3. Initial Access
4. Execution
5. Persistence
6. Privilege Escalation
7. Defense Evasion
8. Credential Access
9. Discovery
10. Lateral Movement
11. Collection
12. Command and Control
13. Exfiltration
14. Impact

**Application**:

- Map defensive controls to ATT&CK techniques
- Identify detection gaps
- Threat intelligence sharing
- Red team/purple team exercises

**Value**: Common language for describing attacker behavior; basis for threat-informed defense

**Sources**:

- [MITRE ATT&CK](https://attack.mitre.org/)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)

---

## Core Analytical Frameworks (Expandable)

### Framework 1: Attack Surface Analysis

**Definition**: Identification and assessment of all points where unauthorized user could enter or extract data from system

**Components**:

**Attack Surface Elements**:

- **Network attack surface**: Exposed ports, services, protocols
- **Software attack surface**: Applications, APIs, web interfaces
- **Human attack surface**: Users, administrators, social engineering targets
- **Physical attack surface**: Facility access, hardware access

**Attack Vectors**: Methods attackers use to exploit attack surface

- Network-based: Port scanning, protocol exploits, man-in-the-middle
- Web-based: SQL injection, XSS, CSRF, authentication bypass
- Email-based: Phishing, malicious attachments, credential harvesting
- Physical: Theft, unauthorized access, evil maid attacks
- Social engineering: Pretexting, baiting, tailgating

**Analysis Process**:

1. **Enumerate**: List all entry points and assets
2. **Classify**: Categorize by type and criticality
3. **Assess**: Evaluate exploitability and impact
4. **Prioritize**: Rank by risk
5. **Reduce**: Minimize unnecessary exposure

**Metrics**:

- Number of exposed services
- Number of internet-facing applications
- Number of privileged accounts
- Lines of code exposed to untrusted input

**Application**: Reducing attack surface is fundamental defensive strategy. Eliminate unnecessary exposure.

**Sources**:

- [Attack Surface Analysis - OWASP](https://owasp.org/www-community/Attack_Surface_Analysis_Cheat_Sheet)
- [Reducing Attack Surface - Microsoft](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)

### Framework 2: Risk Assessment Frameworks

**Purpose**: Quantify and prioritize security risks to guide resource allocation

**Common Frameworks**:

**CVSS** (Common Vulnerability Scoring System):

- Standard for assessing vulnerability severity
- Score 0-10 based on exploitability, impact, scope
- Base score (intrinsic characteristics) + temporal + environmental scores
- Widely used but criticized for not capturing actual risk in specific contexts

**FAIR** (Factor Analysis of Information Risk):

- Quantitative risk framework
- Risk = Loss Event Frequency × Loss Magnitude
- Enables cost-benefit analysis of security investments
- More complex but provides dollar-denominated risk figures

**NIST Risk Management Framework** (RMF):

- Seven steps: Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor
- Links security controls to risk management
- Used by U.S. federal agencies

**Qualitative vs. Quantitative**:

- **Qualitative**: High/Medium/Low risk ratings (simpler, faster, subjective)
- **Quantitative**: Numerical risk values (complex, objective, requires data)

**Application**: Risk assessment informs prioritization. Not all vulnerabilities are equally important—focus on highest risks.

**Sources**:

- [CVSS](https://www.first.org/cvss/)
- [FAIR Institute](https://www.fairinstitute.org/)
- [NIST RMF](https://csrc.nist.gov/projects/risk-management)

### Framework 3: Security Control Frameworks

**Purpose**: Structured set of security controls to achieve security objectives

**Major Frameworks**:

**NIST Cybersecurity Framework**:

- Five core functions: Identify, Protect, Detect, Respond, Recover
- Not prescriptive—flexible for different organizations
- Widely adopted across industries and internationally

**NIST SP 800-53** (Security and Privacy Controls):

- Comprehensive catalog of security controls for federal systems
- 20 control families (Access Control, Incident Response, etc.)
- Detailed implementation guidance

**CIS Controls** (Center for Internet Security):

- 18 prioritized security controls
- Implementation groups (IG1, IG2, IG3) based on organizational maturity
- Actionable and measurable

**ISO/IEC 27001**:

- International standard for information security management systems
- 14 control domains, 114 controls
- Certification available

**Application**: Use frameworks to:

- Ensure comprehensive coverage
- Benchmark security posture
- Communicate with stakeholders
- Meet compliance requirements

**Sources**:

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls)
- [ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)

### Framework 4: Incident Response Lifecycle

**Definition**: Structured approach to handling security incidents

**Standard Model** (NIST SP 800-61):

**Phase 1: Preparation**

- Establish IR capability, tools, playbooks
- Training and exercises
- Communication plans

**Phase 2: Detection and Analysis**

- Monitoring and alerting
- Incident classification and prioritization
- Initial investigation
- Scope determination

**Phase 3: Containment, Eradication, and Recovery**

- **Containment**: Stop spread (short-term and long-term)
- **Eradication**: Remove threat from environment
- **Recovery**: Restore systems to normal operation

**Phase 4: Post-Incident Activity**

- Lessons learned
- Evidence preservation
- Incident report
- Process improvement

**Key Concepts**:

- **Playbooks**: Predefined procedures for common incident types
- **Indicators of Compromise** (IoCs): Artifacts indicating malicious activity
- **Chain of custody**: Evidence handling procedures
- **Communication**: Internal and external stakeholders, legal, PR

**Metrics**:

- Mean Time to Detect (MTTD)
- Mean Time to Respond (MTTR)
- Mean Time to Contain (MTTC)

**Application**: Effective incident response minimizes damage, reduces recovery time, and captures learning.

**Sources**:

- [NIST SP 800-61: Computer Security Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [SANS Incident Response](https://www.sans.org/incident-response/)

### Framework 5: Secure Development Lifecycle (SDL)

**Purpose**: Integrate security into software development process

**Microsoft SDL Phases**:

1. **Training**: Security training for developers
2. **Requirements**: Define security requirements and privacy requirements
3. **Design**: Threat modeling, attack surface reduction, defense in depth
4. **Implementation**: Secure coding standards, code analysis tools
5. **Verification**: Security testing (SAST, DAST, penetration testing)
6. **Release**: Final security review, incident response plan
7. **Response**: Execute incident response plan if vulnerability discovered

**Key Practices**:

- **Static Analysis (SAST)**: Analyze source code for vulnerabilities
- **Dynamic Analysis (DAST)**: Test running application
- **Dependency Scanning**: Check third-party libraries for known vulnerabilities
- **Penetration Testing**: Simulate real attacks
- **Security Champions**: Embed security expertise in development teams

**OWASP SAMM** (Software Assurance Maturity Model):

- Maturity model for secure software development
- Five business functions: Governance, Design, Implementation, Verification, Operations
- Three maturity levels for each function

**Application**: Security must be integrated throughout development lifecycle, not just at the end.

**Sources**:

- [Microsoft SDL](https://www.microsoft.com/en-us/securityengineering/sdl)
- [OWASP SAMM](https://owaspsamm.org/)

---

## Methodological Approaches (Expandable)

### Method 1: Threat Intelligence Analysis

**Purpose**: Understand adversaries, their capabilities, tactics, and targets to inform defense

**Types of Threat Intelligence**:

**Strategic**: High-level trends for executives

- APT group activity and motivations
- Geopolitical cyber threats
- Industry-specific threat landscape

**Operational**: Campaign-level information for security operations

- Current attack campaigns
- Threat actor TTPs
- Malware families

**Tactical**: Technical indicators for immediate defense

- IP addresses, domains, file hashes
- YARA rules, Snort signatures
- CVEs being exploited

**Analytical Process**:

1. **Collection**: Gather data from internal sources, threat feeds, OSINT, dark web
2. **Processing**: Normalize, correlate, deduplicate
3. **Analysis**: Contextualize, attribute, assess intent and capability
4. **Dissemination**: Share with relevant teams in actionable format
5. **Feedback**: Assess effectiveness and refine

**Frameworks**:

- **Diamond Model**: Adversary, Capability, Infrastructure, Victim
- **Kill Chain**: Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives
- **MITRE ATT&CK**: Map observed techniques to ATT&CK matrix

**Application**: Threat intelligence enables proactive, threat-informed defense rather than generic security measures.

**Sources**:

- [CISA Threat Intelligence](https://www.cisa.gov/topics/cyber-threats-and-advisories)
- [Threat Intelligence - SANS](https://www.sans.org/cyber-security-courses/cyber-threat-intelligence/)

### Method 2: Penetration Testing

**Definition**: Authorized simulated attack to evaluate security of systems

**Types**:

**Black Box**: No prior knowledge (simulates external attacker)

**Gray Box**: Partial knowledge (simulates insider or compromised user)

**White Box**: Full knowledge (comprehensive security assessment)

**Phases** (Penetration Testing Execution Standard):

1. **Pre-engagement**: Scope, rules of engagement, legal agreements
2. **Intelligence gathering**: OSINT, network scanning, service enumeration
3. **Threat modeling**: Identify potential attack vectors
4. **Vulnerability analysis**: Identify exploitable weaknesses
5. **Exploitation**: Attempt to exploit vulnerabilities
6. **Post-exploitation**: Assess impact, lateral movement, privilege escalation
7. **Reporting**: Document findings, demonstrate impact, provide remediation guidance

**Specialized Types**:

- **Web application penetration testing**: Focus on OWASP Top 10
- **Network penetration testing**: Internal and external network
- **Social engineering**: Phishing, vishing, physical intrusion
- **Wireless penetration testing**: WiFi security assessment

**Red Team vs. Penetration Testing**:

- **Penetration testing**: Find as many vulnerabilities as possible
- **Red teaming**: Goal-oriented (e.g., access specific data), simulates APT, tests detection and response

**Application**: Regular penetration testing validates effectiveness of controls and identifies gaps before attackers do.

**Sources**:

- [Penetration Testing Execution Standard](http://www.pentest-standard.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Method 3: Security Architecture Review

**Purpose**: Evaluate system design for security properties and identify architectural vulnerabilities

**Review Dimensions**:

**Structural Analysis**:

- Trust boundaries and data flows
- Authentication and authorization architecture
- Network segmentation and isolation
- Data classification and protection

**Threat Modeling**:

- Apply STRIDE or other methodology
- Identify attack trees
- Assess mitigations for identified threats

**Control Assessment**:

- Map controls to CIA triad
- Evaluate defense-in-depth layers
- Identify single points of failure

**Compliance Review**:

- Check against security frameworks (NIST, CIS, ISO)
- Regulatory requirements (PCI-DSS, HIPAA, SOC 2)

**Technology Assessment**:

- Cryptographic implementation
- Secure protocols
- Patch management approach
- Secret management

**Analysis Questions**:

- What are trust boundaries?
- Where does sensitive data flow?
- How is authentication/authorization enforced?
- What happens if component X is compromised?
- Are security assumptions documented and validated?

**Outputs**:

- Architecture diagrams with security annotations
- Threat model
- Risk assessment
- Remediation recommendations

**Application**: Architecture review during design phase prevents expensive security issues in production.

### Method 4: Vulnerability Assessment and Management

**Purpose**: Systematically identify, classify, prioritize, and remediate security weaknesses

**Process**:

**Phase 1: Discovery**

- Asset inventory (what do we have?)
- Vulnerability scanning (automated tools)
- Manual security testing
- Code review (static analysis)

**Phase 2: Assessment**

- Classify vulnerabilities by type and severity
- Assess exploitability (is there exploit code? Is it being exploited?)
- Determine impact (what data/systems at risk?)
- Calculate risk score (CVSS, contextual factors)

**Phase 3: Prioritization**

- Rank by risk (likelihood × impact)
- Consider threat intelligence (is it being exploited in wild?)
- Business criticality of affected assets
- Remediation complexity

**Phase 4: Remediation**

- Patching (ideal)
- Configuration changes
- Compensating controls (if patching impossible)
- Accept risk (document and approve)

**Phase 5: Verification**

- Rescan to confirm remediation
- Update vulnerability database
- Track metrics (time to remediate, vulnerability density)

**Challenges**:

- Alert fatigue (too many findings)
- False positives
- Patching disruption
- Legacy systems

**Best Practices**:

- Risk-based prioritization (not just CVSS)
- SLA-based remediation (Critical: 7 days, High: 30 days, etc.)
- Automate where possible
- Track trends and metrics

**Application**: Continuous vulnerability management is essential hygiene. Can't fix what you don't know about.

**Sources**:

- [NIST SP 800-40: Patch and Vulnerability Management](https://csrc.nist.gov/publications/detail/sp/800-40/rev-4/final)

### Method 5: Security Monitoring and Detection Engineering

**Purpose**: Design and operate capabilities to detect malicious activity

**Components**:

**Data Sources**:

- Network traffic (NetFlow, full packet capture)
- Endpoint logs (process creation, file access, registry changes)
- Authentication logs (logins, privilege escalation)
- Application logs (errors, transactions)
- Cloud APIs and audit logs

**Detection Mechanisms**:

**Signature-based**: Known malicious patterns (antivirus, IDS signatures)

- Pros: Low false positives, fast
- Cons: Only detects known threats

**Anomaly-based**: Deviations from baseline behavior

- Pros: Can detect novel attacks
- Cons: High false positives, requires tuning

**Heuristic-based**: Rules based on attacker behavior patterns

- Pros: Detects variations of known attacks
- Cons: Requires security expertise to create rules

**Threat intelligence-based**: Match against known IoCs

- Pros: Leverages collective knowledge
- Cons: Reactive (indicators discovered post-compromise)

**Detection Development**:

1. Understand attacker technique (MITRE ATT&CK)
2. Identify data sources that capture technique
3. Develop detection logic
4. Test against true positives and false positives
5. Tune threshold and logic
6. Document detection and response procedures
7. Monitor effectiveness and iterate

**SIEM and SOC**:

- **SIEM**: Aggregate, correlate, and analyze security logs
- **SOC**: Security Operations Center—team that monitors alerts and responds to incidents

**Metrics**:

- Detection coverage (% of ATT&CK techniques covered)
- Alert volume and quality
- False positive rate
- Mean Time to Detect (MTTD)

**Application**: You can't respond to what you don't detect. Invest in detection capabilities aligned to threats you face.

**Sources**:

- [Detection Engineering - Splunk](https://www.splunk.com/en_us/blog/learn/detection-engineering.html)
- [Sigma Rules](https://github.com/SigmaHQ/sigma)

---

## Analysis Rubric

### What to Examine

**Assets and Data**:

- What sensitive data exists? (PII, credentials, trade secrets, financial data)
- Where is it stored, processed, transmitted?
- Who has access?
- What is business impact if compromised? (confidentiality, integrity, availability)

**Attack Surface**:

- What systems are exposed to internet?
- What are entry points for attackers?
- What authentication is required?
- What third-party dependencies exist?

**Threat Actors**:

- Who might target this? (Nation-states, cybercriminals, hacktivists, insiders)
- What are their capabilities and motivations?
- What TTPs do they typically use?
- What threat intelligence exists?

**Vulnerabilities**:

- Known software vulnerabilities (CVEs)?
- Configuration weaknesses?
- Architectural security flaws?
- Code-level vulnerabilities?
- Human vulnerabilities (phishing susceptibility)?

**Existing Controls**:

- What security controls are in place?
- Do they follow defense-in-depth principles?
- Are they properly configured and maintained?
- What detection and response capabilities exist?

### Questions to Ask

**Threat Questions**:

- What could go wrong?
- What are most likely attack vectors?
- What threat actors might target this?
- What are their goals and capabilities?
- What historical incidents are relevant?

**Vulnerability Questions**:

- What weaknesses exist?
- How exploitable are they?
- What is impact if exploited?
- Are there known exploits or active exploitation?
- How quickly can vulnerabilities be remediated?

**Control Questions**:

- What protections are in place?
- How effective are they?
- What gaps exist in defensive coverage?
- Can controls be bypassed?
- How will malicious activity be detected?

**Risk Questions**:

- What is likelihood of compromise?
- What is potential impact?
- What is overall risk level?
- How does risk compare to organization's risk appetite?
- What risk treatment options exist? (mitigate, accept, transfer, avoid)

**Compliance Questions**:

- What regulations or standards apply?
- Are security requirements met?
- What evidence demonstrates compliance?
- What gaps exist?

### Factors to Consider

**Technical Factors**:

- System architecture and design
- Technology stack and versions
- Configuration and hardening
- Cryptographic implementation
- Network topology and segmentation

**Organizational Factors**:

- Security maturity and culture
- Available resources and budget
- Risk tolerance
- Regulatory environment
- Business criticality

**Threat Landscape**:

- Current threat actor activity
- Emerging attack techniques
- Industry-specific threats
- Geopolitical factors

**Operational Factors**:

- Patch management processes
- Incident response capabilities
- Security monitoring and detection
- Security awareness and training
- Third-party risk management

### Historical Parallels to Consider

- Similar security incidents
- Comparable vulnerability exploits
- Industry-specific attack patterns
- Lessons from major breaches
- Evolution of threat actor TTPs

### Implications to Explore

**Immediate Security Implications**:

- Confidentiality: Data breach risk
- Integrity: Data tampering or corruption risk
- Availability: Service disruption risk
- Financial: Ransom, recovery costs, fines

**Broader Implications**:

- Reputation damage
- Legal and regulatory consequences
- Customer trust erosion
- Competitive disadvantage
- Systemic risk (if in critical infrastructure)

**Strategic Implications**:

- Security architecture changes needed
- Security program maturity gaps
- Resource allocation and prioritization
- Risk management approach

---

## Step-by-Step Analysis Process

### Step 1: Define Scope and Context

**Actions**:

- Clearly identify system, application, or event being analyzed
- Determine boundaries and interfaces
- Identify stakeholders and their security requirements
- Understand business context and criticality
- Gather relevant documentation (architecture diagrams, data flows, policies)

**Outputs**:

- Scope statement
- Asset inventory
- Stakeholder list
- Business context understanding

### Step 2: Identify Assets and Data

**Actions**:

- List critical assets (systems, data, services)
- Classify data by sensitivity (public, internal, confidential, restricted)
- Map data flows (where data is created, stored, processed, transmitted, destroyed)
- Identify crown jewels (most valuable assets)

**Outputs**:

- Asset inventory with criticality ratings
- Data classification matrix
- Data flow diagrams
- Crown jewels list

### Step 3: Analyze Attack Surface

**Actions**:

- Enumerate all entry points (APIs, web interfaces, network services, physical access)
- Identify trust boundaries (where untrusted input crosses into trusted zones)
- Map authentication and authorization points
- Identify dependencies (third-party services, libraries, suppliers)

**Outputs**:

- Attack surface map
- Trust boundary diagram
- Entry point inventory
- Dependency list

### Step 4: Conduct Threat Modeling

**Actions**:

- Select threat modeling methodology (STRIDE, PASTA, etc.)
- Identify potential threat actors and their goals
- Enumerate potential attack vectors for each asset
- Create attack trees showing attack paths
- Map to MITRE ATT&CK techniques

**Outputs**:

- Threat model document
- Threat actor profiles
- Attack tree diagrams
- ATT&CK technique mapping

### Step 5: Identify Vulnerabilities

**Actions**:

- Review known CVEs for technologies in use
- Analyze configuration against security benchmarks (CIS, STIGs)
- Review architecture for security design flaws
- Consider code-level vulnerabilities (if applicable)
- Assess human vulnerabilities (phishing susceptibility, privilege misuse)

**Outputs**:

- Vulnerability inventory
- CVSS scores or risk ratings
- Configuration gap analysis
- Architectural security issues

### Step 6: Assess Existing Controls

**Actions**:

- Inventory security controls across all layers (network, host, application, data)
- Map controls to threats (which threats do controls mitigate?)
- Evaluate control effectiveness (properly configured? maintained? monitored?)
- Identify control gaps (threats without adequate mitigation)
- Assess detection and response capabilities

**Outputs**:

- Control inventory
- Threat-control mapping matrix
- Control effectiveness assessment
- Detection coverage gaps

### Step 7: Analyze Risk

**Actions**:

- For each threat-vulnerability pair, estimate likelihood and impact
- Calculate risk scores (qualitative or quantitative)
- Prioritize risks
- Compare to organizational risk tolerance
- Consider risk interdependencies and cascading effects

**Outputs**:

- Risk register
- Risk heat map
- Prioritized risk list
- Risk acceptance recommendations

### Step 8: Evaluate Detection and Response

**Actions**:

- Assess what malicious activities would be detected
- Evaluate MTTD (Mean Time to Detect) for various attack scenarios
- Review incident response plans and playbooks
- Assess incident response team capabilities
- Identify gaps in detection or response

**Outputs**:

- Detection coverage assessment
- MTTD estimates
- IR capability assessment
- Detection and response gaps

### Step 9: Develop Remediation Recommendations

**Actions**:

- Propose mitigations for identified risks (preventive, detective, corrective)
- Prioritize by risk reduction and implementation effort
- Consider compensating controls where direct mitigation is impractical
- Estimate costs and implementation timelines
- Document risk acceptance for risks not mitigated

**Outputs**:

- Remediation roadmap
- Prioritized recommendation list
- Cost-benefit analysis
- Risk acceptance documentation

### Step 10: Consider Compliance Requirements

**Actions**:

- Identify applicable regulations and standards
- Map controls to compliance requirements
- Document evidence of compliance
- Identify compliance gaps
- Recommend actions to achieve or maintain compliance

**Outputs**:

- Compliance matrix
- Gap analysis
- Evidence documentation
- Compliance remediation plan

### Step 11: Synthesize and Report

**Actions**:

- Summarize key findings for different audiences (executives, technical teams, compliance)
- Provide clear risk assessment and recommendations
- Include metrics and KPIs
- Document assumptions and limitations
- Create action plan with owners and timelines

**Outputs**:

- Executive summary
- Technical findings report
- Remediation roadmap
- Compliance summary

---

## Usage Examples

### Example 1: Security Incident - Ransomware Attack

**Event**: Organization experiences ransomware attack; files encrypted, ransom note demands payment

**Analysis**:

**Step 1 - Scope and Context**:

- Affected systems: File servers, workstations, backups
- Business impact: Operations halted, data unavailable
- Critical: Understand ransomware variant, encryption scope, attacker access

**Step 2 - Assets**:

- Crown jewels: Customer database, financial records, intellectual property
- Status: Files encrypted, availability compromised

**Step 3 - Attack Surface Analysis**:

- Initial access vector: Likely phishing email or vulnerable RDP endpoint
- Lateral movement: SMB, credential theft

**Step 4 - Threat Modeling (Post-Incident)**:

- Threat actor: Likely cybercriminal group (financial motivation)
- ATT&CK mapping:
  - Initial Access: Phishing or Exploit Public-Facing Application
  - Execution: User Execution or Exploitation for Client Execution
  - Persistence: Registry Run Keys, Scheduled Tasks
  - Privilege Escalation: Exploitation for Privilege Escalation
  - Credential Access: Credential Dumping
  - Lateral Movement: SMB/Windows Admin Shares
  - Impact: Data Encrypted for Impact

**Step 5 - Vulnerabilities**:

- Phishing susceptibility (no email filtering, insufficient user training)
- Unpatched RDP vulnerabilities
- Weak passwords or credential reuse
- Inadequate network segmentation (ransomware spread easily)
- Backup vulnerabilities (backups also encrypted)

**Step 6 - Control Assessment**:

- Missing: Email security gateway, EDR, MFA
- Inadequate: Network segmentation, backup isolation, patch management
- Failed: Antivirus didn't detect ransomware

**Step 7 - Risk Analysis**:

- Impact: HIGH (business disruption, data loss, ransom demand, reputation damage)
- Likelihood: HIGH (demonstrated—incident occurred)
- Residual risk: CRITICAL (without improvements, repeat likely)

**Step 8 - Detection and Response**:

- Detection: Failed until encryption began (no EDR, limited logging)
- MTTD: Hours to days (too slow)
- Response: No playbook, uncoordinated response
- Gaps: No IR team, no communication plan, no legal/PR coordination

**Step 9 - Recommendations (Prioritized)**:

_Immediate (Hours to Days)_:

1. Isolate affected systems (contain spread)
2. Identify ransomware variant and check for decryption tools
3. Engage incident response firm if no internal capability
4. Do NOT pay ransom immediately (assess alternatives first)
5. Notify legal, insurance, possibly law enforcement

_Short-term (Days to Weeks)_:

1. Restore from backups if available and uncompromised
2. Deploy EDR on all endpoints
3. Implement MFA for all remote access
4. Conduct forensic investigation to determine root cause and scope
5. Develop and test IR playbook

_Medium-term (Weeks to Months)_:

1. Network segmentation (prevent lateral movement)
2. Email security gateway (block phishing)
3. Privileged access management (limit credential theft)
4. Security awareness training (reduce phishing success)
5. Backup hardening (air-gapped or immutable backups)

_Long-term (Months to Year)_:

1. Security maturity assessment and roadmap
2. 24/7 SOC or MDR service
3. Penetration testing and red team exercises
4. Comprehensive vulnerability management program

**Step 10 - Compliance**:

- Regulatory notification requirements (GDPR, state breach laws, etc.)
- Cyber insurance claim
- Document incident for auditors

**Step 11 - Synthesis**:

- Root cause: Combination of phishing/RDP exploit + inadequate detection + weak segmentation + backup vulnerabilities
- Key lesson: Defense-in-depth failures—multiple control failures allowed attack to succeed
- Priority: Immediate containment and recovery, then build detective and preventive controls
- Cost: Ransom demand + downtime + recovery + remediation + reputation damage (potentially millions)

### Example 2: Vulnerability Assessment - New Web Application Launch

**Event**: Organization planning to launch customer-facing web application; pre-launch security review requested

**Analysis**:

**Step 1 - Scope**:

- Application: E-commerce web application
- Users: External customers
- Data: PII, payment information, order history
- Criticality: HIGH (revenue-generating, customer trust)

**Step 2 - Assets**:

- Customer PII and payment data (confidentiality, integrity critical)
- Inventory and pricing data (integrity, availability critical)
- Application availability (revenue impact)

**Step 3 - Attack Surface**:

- Web interface (public-facing)
- APIs (mobile app, third-party integrations)
- Admin portal (internal users)
- Payment processor integration
- Third-party libraries and dependencies

**Step 4 - Threat Modeling (STRIDE)**:

**Spoofing**:

- Threat: Attacker impersonates user or admin
- Mitigations: Strong authentication, MFA, session management

**Tampering**:

- Threat: Attacker modifies prices, orders, or user data
- Mitigations: Input validation, authorization checks, integrity controls

**Repudiation**:

- Threat: User denies placing order
- Mitigations: Audit logging, transaction signing

**Information Disclosure**:

- Threat: Attacker accesses other users' PII or payment info
- Mitigations: Authorization checks, encryption, secure session management

**Denial of Service**:

- Threat: Attacker overwhelms application
- Mitigations: Rate limiting, DDoS protection, scalable infrastructure

**Elevation of Privilege**:

- Threat: User gains admin access
- Mitigations: Least privilege, secure authorization, privilege separation

**Step 5 - Vulnerabilities (OWASP Top 10 Analysis)**:

1. **Broken Access Control**: Check for IDOR vulnerabilities, horizontal/vertical privilege escalation
2. **Cryptographic Failures**: Verify encryption at rest and in transit, key management
3. **Injection**: Test for SQL injection, XSS, command injection
4. **Insecure Design**: Review for security design flaws, threat model gaps
5. **Security Misconfiguration**: Check for default credentials, unnecessary features, verbose errors
6. **Vulnerable Components**: Scan dependencies for known CVEs
7. **Authentication Failures**: Test password policy, session management, MFA
8. **Software/Data Integrity**: Verify supply chain security, unsigned updates
9. **Logging Failures**: Ensure security events logged, log tampering prevention
10. **SSRF**: Test for server-side request forgery vulnerabilities

**Step 6 - Control Assessment**:

_Positive Findings_:

- TLS 1.3 for all connections
- Passwords hashed with bcrypt
- Input validation framework in use
- Dependency scanning in CI/CD

_Gaps Identified_:

- No MFA for customer accounts
- Admin portal not on separate domain/network
- Verbose error messages expose stack traces
- No rate limiting on API endpoints
- Some third-party dependencies have known CVEs
- Insufficient authorization checks (IDOR vulnerabilities)
- No Web Application Firewall (WAF)

**Step 7 - Risk Analysis**:

_Critical Risks_:

- **IDOR vulnerabilities**: HIGH likelihood, HIGH impact (data breach)
- **Vulnerable dependencies**: MEDIUM likelihood, HIGH impact (RCE potential)

_High Risks_:

- **No rate limiting**: HIGH likelihood, MEDIUM impact (scraping, brute force)
- **Admin portal on same domain**: LOW likelihood, HIGH impact (credential theft)

_Medium Risks_:

- **Verbose errors**: MEDIUM likelihood, MEDIUM impact (information disclosure)
- **No MFA**: LOW likelihood (for now), HIGH impact (account takeover)

**Step 8 - Detection and Response**:

- Logging: Adequate for authentication and transactions
- SIEM integration: Not yet configured
- IR playbook: Generic, needs application-specific scenarios
- Recommendation: Configure SIEM, create app-specific IR playbook, implement alerting for suspicious patterns

**Step 9 - Recommendations (Prioritized by Risk)**:

_Must-Fix Before Launch (Critical)_:

1. Fix IDOR vulnerabilities (implement authorization checks)
2. Update vulnerable dependencies
3. Remove verbose error messages in production
4. Implement rate limiting on all endpoints

_Should-Fix Before Launch (High)_:

1. Deploy WAF with OWASP Core Rule Set
2. Separate admin portal (different domain, VPN/IP restriction)
3. Configure SIEM integration and alerting

_Post-Launch (Medium)_:

1. Implement MFA for customer accounts
2. Enhance logging (capture more security events)
3. Conduct penetration testing
4. Establish bug bounty program

**Step 10 - Compliance**:

- **PCI-DSS**: Required for payment card data (use tokenization, minimize cardholder data environment)
- **GDPR/CCPA**: Customer data privacy requirements (consent, data minimization, breach notification)
- **SOC 2**: If B2B customers require assurance

**Step 11 - Synthesis**:

- Application has solid foundation (modern crypto, input validation, dependency scanning)
- Critical issues must be fixed before launch (IDOR, vulnerable dependencies)
- WAF provides defense-in-depth for web threats
- Post-launch: Continue testing, bug bounty, security monitoring
- Go/No-Go: NO GO until critical issues resolved

### Example 3: Security Architecture Review - Cloud Migration

**Event**: Organization planning to migrate on-premises applications to AWS; security architecture review requested

**Analysis**:

**Step 1 - Scope**:

- Migration: 50+ applications, mix of web apps, APIs, databases
- Target: AWS (IaaS and PaaS services)
- Timeline: 12-month migration
- Criticality: Mixed (some business-critical applications)

**Step 2 - Assets**:

- Applications and data currently in controlled on-premises environment
- Concerns: Data sovereignty, compliance, shared responsibility model

**Step 3 - Attack Surface Changes**:

- **Increases**: Internet-facing cloud services, cloud management interfaces, broader attack surface
- **Decreases**: Physical access threats
- **New**: Cloud misconfigurations, IAM vulnerabilities, API security

**Step 4 - Threat Modeling (Cloud-Specific)**:

_Cloud-Specific Threats_:

- Account compromise (stolen credentials, phishing)
- Misconfigured storage buckets (public S3 buckets)
- Overly permissive IAM policies
- Insufficient network segmentation (VPC design)
- Data exfiltration via cloud APIs
- Insider threats (cloud admin abuse)
- Supply chain (compromised cloud services or dependencies)

_MITRE ATT&CK for Cloud_:

- Initial Access: Valid accounts, exploit public-facing application
- Persistence: Account manipulation, create IAM user
- Privilege Escalation: IAM policy manipulation
- Defense Evasion: Disable cloud logs
- Credential Access: Unsecured credentials in code/config
- Discovery: Cloud service discovery
- Lateral Movement: Use alternate authentication material
- Exfiltration: Transfer data to cloud account

**Step 5 - Vulnerabilities (Cloud Context)**:

- Lack of cloud security expertise
- On-premises mindset (perimeter-focused, not zero-trust)
- Unclear cloud IAM strategy
- No cloud configuration management (IaC not used)
- No cloud security posture management (CSPM)

**Step 6 - Control Assessment (Shared Responsibility Model)**:

_AWS Responsibilities_ (Security OF the Cloud):

- Physical security
- Hypervisor security
- Network infrastructure

_Customer Responsibilities_ (Security IN the Cloud):

- IAM and access control
- Data encryption
- Network configuration (VPCs, security groups)
- Application security
- Compliance

_Proposed Controls_:

**Identity and Access Management**:

- Implement AWS Organizations with SCPs (Service Control Policies)
- Enforce MFA for all users
- Use IAM roles, not long-term credentials
- Principle of least privilege
- Regular access reviews

**Network Security**:

- VPC design with public/private subnets
- Security groups (stateful firewalls)
- NACLs (stateless firewalls)
- AWS WAF for web applications
- VPC Flow Logs for monitoring

**Data Protection**:

- Encryption at rest (S3, EBS, RDS with KMS)
- Encryption in transit (TLS)
- S3 bucket policies (block public access)
- Data classification and handling

**Monitoring and Detection**:

- AWS CloudTrail (API logging)
- AWS GuardDuty (threat detection)
- AWS Security Hub (aggregate findings)
- AWS Config (configuration compliance)
- SIEM integration

**Incident Response**:

- Cloud-specific IR playbooks
- Automate response with Lambda
- Snapshot and forensics procedures
- AWS support engagement plan

**Compliance**:

- AWS Artifact (compliance reports)
- AWS Config rules (continuous compliance)
- Encryption for HIPAA/PCI-DSS
- Data residency (region selection)

**Step 7 - Risk Analysis**:

_High Risks_:

- Misconfigured S3 buckets (likelihood: high, impact: high - data breach)
- Compromised IAM credentials (likelihood: medium, impact: high)
- Insufficient monitoring (likelihood: high, impact: medium - delayed detection)

_Medium Risks_:

- Inadequate network segmentation (likelihood: medium, impact: medium)
- Lack of cloud expertise (likelihood: high, impact: medium - misconfigurations)

**Step 8 - Detection and Response**:

- Deploy GuardDuty in all regions and accounts
- Centralize CloudTrail logs
- Configure Security Hub and Config
- Create cloud-specific alerts (unusual API calls, IAM changes, public S3 buckets)
- Develop cloud incident response playbooks

**Step 9 - Recommendations (Cloud Migration Security Roadmap)**:

_Pre-Migration (Month 1-2)_:

1. Cloud security training for teams
2. Design AWS Organizations structure and account strategy
3. Define IAM strategy and policies
4. Design VPC architecture and network segmentation
5. Select and implement CSPM tool
6. Establish cloud security baseline (CIS AWS Foundations Benchmark)

_During Migration (Month 3-12)_:

1. Use Infrastructure as Code (Terraform/CloudFormation) for all resources
2. Automate security checks in CI/CD (SAST, DAST, IaC scanning)
3. Enforce encryption at rest and in transit
4. Implement least privilege IAM
5. Enable all cloud-native security services (GuardDuty, Security Hub, Config, CloudTrail)
6. Security testing before production deployment

_Post-Migration (Ongoing)_:

1. Continuous compliance monitoring
2. Regular IAM access reviews
3. Cloud security posture assessments
4. Penetration testing in cloud environment
5. Tabletop exercises for cloud IR scenarios

**Step 10 - Compliance**:

- Leverage AWS compliance certifications (SOC 2, ISO 27001, PCI-DSS)
- Use AWS Artifact for audit evidence
- Implement AWS Config rules for continuous compliance
- Document shared responsibility matrix

**Step 11 - Synthesis**:

- Cloud security requires different mindset (zero-trust, identity-centric, API-driven)
- Shared responsibility model is critical—must secure what AWS doesn't
- Major risks: Misconfigurations, IAM vulnerabilities, insufficient monitoring
- Opportunities: Cloud-native security services, automation, scalability
- Success factors: Training, least privilege, defense-in-depth, monitoring, IaC
- Recommendation: Proceed with migration, but implement security roadmap in parallel

---

## Reference Materials (Expandable)

### Essential Organizations and Resources

#### NIST (National Institute of Standards and Technology)

- **Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **SP 800 Series**: Security and privacy controls, risk management
- **National Vulnerability Database (NVD)**: https://nvd.nist.gov/

#### CISA (Cybersecurity and Infrastructure Security Agency)

- **Alerts and Advisories**: https://www.cisa.gov/topics/cyber-threats-and-advisories
- **Known Exploited Vulnerabilities Catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **Resources**: Free tools, training, best practices

#### MITRE

- **ATT&CK Framework**: https://attack.mitre.org/
- **CVE Program**: https://www.cve.org/
- **CAPEC**: Common Attack Pattern Enumeration and Classification

#### OWASP (Open Web Application Security Project)

- **Top 10**: https://owasp.org/www-project-top-ten/
- **Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **Cheat Sheets**: https://cheatsheetseries.owasp.org/

#### SANS Institute

- **Internet Storm Center**: https://isc.sans.edu/
- **Reading Room**: Thousands of security papers
- **Critical Security Controls**: https://www.cisecurity.org/controls

### Key Standards and Frameworks

**ISO/IEC 27001**: Information Security Management System
**ISO/IEC 27002**: Information Security Controls
**PCI-DSS**: Payment Card Industry Data Security Standard
**HIPAA**: Health Insurance Portability and Accountability Act (Security Rule)
**SOC 2**: Service Organization Control 2 (Trust Services Criteria)
**GDPR**: General Data Protection Regulation
**NIST SP 800-53**: Security and Privacy Controls
**CIS Controls**: Center for Internet Security Critical Security Controls
**FedRAMP**: Federal Risk and Authorization Management Program

### Vulnerability Databases

- **National Vulnerability Database (NVD)**: https://nvd.nist.gov/
- **CVE**: https://www.cve.org/
- **Exploit-DB**: https://www.exploit-db.com/
- **VulnDB**: https://vulndb.cyberriskanalytics.com/

### Threat Intelligence Sources

- **CISA Alerts**: https://www.cisa.gov/news-events/cybersecurity-advisories
- **US-CERT**: https://www.cisa.gov/uscert
- **Threat Intelligence Platforms**: Recorded Future, Mandiant, CrowdStrike
- **Open Source**: AlienVault OTX, MISP, threat feeds

### Security Tools and Platforms

**Vulnerability Scanning**: Nessus, Qualys, Rapid7 InsightVM
**SAST**: SonarQube, Checkmarx, Veracode
**DAST**: Burp Suite, OWASP ZAP, Acunetix
**SIEM**: Splunk, Elastic, Sentinel, Chronicle
**EDR**: CrowdStrike, SentinelOne, Microsoft Defender for Endpoint
**CSPM**: Prisma Cloud, Wiz, Orca Security

### Certifications

- **CISSP**: Certified Information Systems Security Professional
- **CISM**: Certified Information Security Manager
- **CEH**: Certified Ethical Hacker
- **OSCP**: Offensive Security Certified Professional
- **GCIH**: GIAC Certified Incident Handler
- **Security+**: CompTIA Security+

### Communities and Resources

- **r/netsec**: https://www.reddit.com/r/netsec/
- **Krebs on Security**: https://krebsonsecurity.com/
- **Schneier on Security**: https://www.schneier.com/
- **Dark Reading**: https://www.darkreading.com/
- **The Hacker News**: https://thehackernews.com/

---

## Verification Checklist

After completing cybersecurity analysis:

- [ ] Identified all critical assets and data
- [ ] Analyzed attack surface and entry points
- [ ] Conducted threat modeling appropriate to scope
- [ ] Identified vulnerabilities and assessed severity
- [ ] Evaluated existing security controls for effectiveness
- [ ] Analyzed risk using quantitative or qualitative methods
- [ ] Assessed detection and response capabilities
- [ ] Developed prioritized remediation recommendations
- [ ] Considered compliance requirements
- [ ] Mapped threats to MITRE ATT&CK framework (if applicable)
- [ ] Applied defense-in-depth and zero-trust principles
- [ ] Provided clear, actionable security guidance
- [ ] Used security terminology and frameworks precisely

---

## Common Pitfalls to Avoid

**Pitfall 1: Checklist Compliance Without Risk Context**

- **Problem**: Following compliance requirements without understanding actual risks
- **Solution**: Risk-based approach—understand threats and business context, not just checkboxes

**Pitfall 2: Perimeter-Only Security**

- **Problem**: Assuming network perimeter protects everything inside
- **Solution**: Defense-in-depth and zero-trust—assume breach, protect assets themselves

**Pitfall 3: Alert Fatigue and False Positives**

- **Problem**: Too many low-quality alerts overwhelm responders
- **Solution**: Tune detections, prioritize high-fidelity alerts, automate response where possible

**Pitfall 4: Ignoring Human Element**

- **Problem**: Focus only on technical controls, ignore social engineering and insider threats
- **Solution**: Include security awareness, privileged user monitoring, insider threat programs

**Pitfall 5: Point-in-Time Assessment**

- **Problem**: One-time security review without continuous monitoring
- **Solution**: Continuous security—ongoing monitoring, vulnerability management, threat intelligence

**Pitfall 6: Vulnerability Scoring Without Context**

- **Problem**: Prioritizing by CVSS alone without considering exploitability or business context
- **Solution**: Risk-based prioritization—consider threat intelligence, exploitability, asset criticality

**Pitfall 7: Security as Blocker**

- **Problem**: Security seen as obstacle to business objectives
- **Solution**: Enable business securely—balance risk and business value, provide secure alternatives

**Pitfall 8: Ignoring Supply Chain and Third Parties**

- **Problem**: Focus only on first-party systems, ignore dependencies
- **Solution**: Supply chain risk management—assess third-party security, dependency vulnerabilities

---

## Success Criteria

A quality cybersecurity analysis:

- [ ] Applies appropriate security frameworks and methodologies
- [ ] Identifies and prioritizes risks using threat modeling
- [ ] Evaluates security controls across multiple layers (defense-in-depth)
- [ ] Provides actionable, prioritized remediation recommendations
- [ ] Grounds analysis in threat intelligence and industry best practices
- [ ] Considers both technical and human factors
- [ ] Addresses detection and response, not just prevention
- [ ] Maps to recognized standards (MITRE ATT&CK, NIST CSF, etc.)
- [ ] Balances security with business objectives
- [ ] Demonstrates deep security expertise and critical thinking
- [ ] Communicates clearly to both technical and non-technical audiences
- [ ] Uses security concepts and terminology precisely

---

## Integration with Other Analysts

Cybersecurity analysis complements other perspectives:

- **Computer Scientist**: Deep technical understanding of systems and code
- **Lawyer**: Legal implications of breaches, regulatory compliance requirements
- **Economist**: Cost-benefit analysis of security investments, cyber insurance
- **Psychologist**: Human behavior, social engineering, security culture
- **Political Scientist**: Nation-state threats, geopolitical cyber conflict, policy

Cybersecurity is particularly strong on:

- Threat modeling and risk assessment
- Vulnerability analysis
- Defense-in-depth design
- Incident detection and response
- Compliance and standards

---

## Continuous Improvement

This skill evolves through:

- New threat actor TTPs and attack techniques
- Emerging vulnerabilities and exploits
- Evolution of security technologies and practices
- Lessons learned from security incidents
- Updates to frameworks and standards
- Cross-disciplinary security research

---

**Skill Status**: Complete - Comprehensive Cybersecurity Analysis Capability
**Quality Level**: High - Enterprise-grade security analysis with modern frameworks
**Token Count**: ~8,500 words (target 6-10K tokens)
