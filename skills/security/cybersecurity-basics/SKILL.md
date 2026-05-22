---
name: cybersecurity-basics
description: Foundational cybersecurity literacy covering threat landscape (malware, phishing, social engineering, network attacks), defensive practices (encryption, authentication, access control, patching), privacy fundamentals (data collection, tracking, regulatory frameworks), and security reasoning (threat modeling, risk assessment, defense in depth). Use when explaining security concepts, evaluating system security, teaching safe technology practices, or reasoning about digital privacy. Distinct from professional penetration testing -- this skill covers what every technology user and designer should understand.
type: skill
category: technology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/technology/cybersecurity-basics/SKILL.md
superseded_by: null
---
# Cybersecurity Basics

Cybersecurity is the practice of protecting systems, networks, and data from unauthorized access, damage, or disruption. In a world where nearly every aspect of life involves digital systems, security literacy is not optional -- it is a prerequisite for informed technology use. This skill covers the threat landscape, defensive practices, privacy fundamentals, and the reasoning frameworks that security professionals use to think about protection.

**Agent affinity:** borg (systems security, infrastructure hardening), berners-lee (web security, open standards), joy (risk assessment for critical systems)

**Concept IDs:** tech-information-security, tech-digital-rights-privacy

## Part I -- The Threat Landscape

### Malware

Malware (malicious software) is any software designed to harm, exploit, or gain unauthorized access to a system.

| Type | Behavior | Example vector |
|---|---|---|
| Virus | Attaches to files, spreads when file is executed | Infected email attachment |
| Worm | Self-replicates across networks without user action | Exploits network vulnerability |
| Trojan | Disguised as legitimate software | Fake app download |
| Ransomware | Encrypts files, demands payment for decryption key | Phishing email with malicious link |
| Spyware | Monitors activity, steals data silently | Bundled with free software |
| Rootkit | Hides deep in the OS, grants persistent access | Compromised system update |

### Social Engineering

Social engineering attacks exploit human psychology rather than technical vulnerabilities. They are often more effective than technical attacks because humans are more predictable than software.

- **Phishing:** Fraudulent messages impersonating trusted entities to extract credentials or install malware. Spear phishing targets specific individuals with personalized content.
- **Pretexting:** Creating a fabricated scenario to gain trust and extract information ("I'm from IT, I need your password to fix your account").
- **Baiting:** Leaving infected USB drives or offering free downloads that install malware.
- **Tailgating:** Following an authorized person through a secured door without credentials.

**The human layer is always the weakest link.** Technical defenses fail when a user willingly provides their password to a convincing impersonator.

### Network Attacks

- **Man-in-the-middle (MITM):** Intercepting communication between two parties. Mitigated by encryption (HTTPS, TLS).
- **Denial of Service (DoS/DDoS):** Overwhelming a server with traffic so legitimate users cannot connect.
- **SQL injection:** Inserting malicious database queries through input fields in web applications.
- **Cross-site scripting (XSS):** Injecting malicious scripts into web pages viewed by other users.

## Part II -- Defensive Practices

### Encryption

Encryption transforms readable data (plaintext) into unreadable data (ciphertext) using a key. Only someone with the correct key can reverse the transformation.

- **Symmetric encryption:** Same key for encryption and decryption (AES). Fast. Used for data at rest and bulk data transfer.
- **Asymmetric encryption:** Public key encrypts, private key decrypts (RSA, ECC). Slower. Used for key exchange and digital signatures.
- **HTTPS/TLS:** Combines both -- asymmetric encryption establishes a shared key, then symmetric encryption handles the session. The padlock in your browser means TLS is active.

### Authentication

Authentication verifies identity -- confirming that someone is who they claim to be.

**Three factors:**

| Factor | What it is | Example |
|---|---|---|
| Something you know | Secret information | Password, PIN, security question |
| Something you have | Physical token | Phone (SMS code), hardware key (YubiKey) |
| Something you are | Biometric | Fingerprint, face scan, iris pattern |

**Multi-factor authentication (MFA)** requires two or more factors. A password plus a phone code is far more secure than a password alone, because an attacker must compromise two independent channels.

### Password Hygiene

- Use a unique password for every account. Password reuse means one breach compromises all accounts.
- Use a password manager. Human memory cannot reliably store unique passwords for dozens of accounts.
- Prefer long passphrases over short complex passwords. "correct horse battery staple" is both stronger and more memorable than "P@55w0rd!"
- Enable MFA on every account that supports it, especially email and financial accounts.

### Access Control

Access control determines who can access what resources and what they can do with them.

- **Principle of least privilege:** Grant the minimum access necessary for a task. An accountant does not need administrator access.
- **Role-based access control (RBAC):** Permissions assigned to roles (admin, editor, viewer), users assigned to roles.
- **Separation of duties:** No single person should control all steps of a critical process.

### Defense in Depth

No single security measure is sufficient. Defense in depth layers multiple protections so that the failure of one layer does not compromise the whole system.

| Layer | Controls |
|---|---|
| Physical | Locked doors, badge access, security cameras |
| Network | Firewalls, intrusion detection, network segmentation |
| Host | Antivirus, OS hardening, patch management |
| Application | Input validation, secure coding, code review |
| Data | Encryption, backup, access controls |
| Human | Security training, phishing simulations, incident response procedures |

### Patching and Updates

Software vulnerabilities are discovered continuously. Patches fix known vulnerabilities. Delaying patches leaves known doors open. Automatic updates are the single most effective security practice for most users.

## Part III -- Privacy Fundamentals

### Data Collection and Tracking

Modern digital services collect vast amounts of personal data -- browsing history, location, contacts, messages, purchase history, biometrics. This data has economic value (targeted advertising) and surveillance value (government and corporate monitoring).

- **First-party data:** Collected by the service you are directly using.
- **Third-party data:** Collected by entities embedded in the service (ad trackers, analytics scripts, data brokers).
- **Data minimization principle:** Collect only what is necessary for the stated purpose. Many services collect far more than they need.

### Regulatory Frameworks

| Framework | Jurisdiction | Key principles |
|---|---|---|
| GDPR (2018) | European Union | Consent, right to erasure, data portability, breach notification |
| CCPA/CPRA (2020/2023) | California, USA | Right to know, right to delete, right to opt out of sale |
| COPPA (1998) | USA (children under 13) | Parental consent for data collection from children |
| PIPEDA (2000) | Canada | Consent, limited collection, accountability |

### Privacy as a Design Principle

Privacy by design (Ann Cavoukian, 2009) embeds privacy into system architecture rather than bolting it on after the fact. Seven principles:

1. Proactive, not reactive
2. Privacy as the default setting
3. Privacy embedded into design
4. Full functionality (privacy and functionality are not trade-offs)
5. End-to-end security
6. Visibility and transparency
7. Respect for user privacy

## Part IV -- Security Reasoning

### Threat Modeling

Threat modeling is a structured approach to identifying security risks before they are exploited.

**STRIDE model (Microsoft):**

| Threat | Targets | Example |
|---|---|---|
| **S**poofing | Authentication | Fake login page |
| **T**ampering | Integrity | Modified database record |
| **R**epudiation | Non-repudiation | Denying a transaction occurred |
| **I**nformation disclosure | Confidentiality | Database breach |
| **D**enial of service | Availability | DDoS attack |
| **E**levation of privilege | Authorization | User gains admin access |

### Risk Assessment

Risk = Likelihood x Impact. Not all threats deserve equal attention. Focus defensive resources on high-likelihood, high-impact threats first.

| | Low impact | High impact |
|---|---|---|
| **High likelihood** | Monitor | Prioritize |
| **Low likelihood** | Accept | Mitigate |

## Cross-References

- **borg agent:** Systems security, infrastructure hardening. Primary agent for security architecture questions.
- **berners-lee agent:** Web security, protocol security, open standards for security.
- **joy agent:** Risk assessment for critical and emerging technology systems.
- **digital-systems skill:** The systems that cybersecurity protects.
- **responsible-innovation skill:** Ethical dimensions of security decisions (surveillance vs safety).

## References

- Schneier, B. (2015). *Data and Goliath*. W. W. Norton.
- Mitnick, K. & Simon, W. L. (2002). *The Art of Deception*. Wiley.
- Stallings, W. (2017). *Cryptography and Network Security*. 7th edition. Pearson.
- Cavoukian, A. (2009). *Privacy by Design: The 7 Foundational Principles*. Information and Privacy Commissioner of Ontario.
- NIST. (2018). *Framework for Improving Critical Infrastructure Cybersecurity*. Version 1.1.
- Zuboff, S. (2019). *The Age of Surveillance Capitalism*. PublicAffairs.
