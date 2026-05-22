---
name: create-threat-model
description: "Analyze a codebase and produce a structured threat model at .turbo/threat-model.md covering assets, trust boundaries, attack surfaces with existing mitigations, attacker stories, and calibrated severity. Use when the user asks to \"create a threat model\", \"threat model\", \"threat model this codebase\", \"security analysis\", \"analyze the attack surface\", \"what are the threats\", or \"identify security risks\"."
---

# Create Threat Model

Analyze the current codebase and produce a structured threat model at `.turbo/threat-model.md`.

The threat model describes the current state of the codebase: what it protects, where trust boundaries are, how it can be attacked, what defenses exist, and how severe each risk is. It is descriptive, not prescriptive. Do not include remediation recommendations.

Optional: `$ARGUMENTS` may specify scope (directories, modules, or focus areas). When scope is provided, limit reconnaissance and code discovery to the specified directories or modules. Still produce all four sections, but title the overview to reflect the narrowed scope and note what is excluded.

## Step 1: Reconnaissance

Build a mental model of the system before analyzing threats.

1. Read the project README, CLAUDE.md, and any architecture or security documentation.
2. Examine top-level directory structure, build files, and dependency manifests to identify modules, languages, frameworks, and deployment model.
3. **Classify the application type**: library, CLI tool, web service, desktop app, mobile app, or hybrid. This determines which threat categories and trust boundary patterns apply.
4. Identify security-critical dependencies (crypto libraries, auth providers, network stacks, native/FFI libraries). Note what this codebase delegates versus what it owns.
5. Read any existing security documentation: `SECURITY.md`, audit reports, threat models, or changelog entries mentioning CVEs.

## Step 2: Security-Relevant Code Discovery

Search the codebase for code that handles security-sensitive operations. Do not read every file. Use targeted searches.

**Categories to search for:**
- Authentication and authorization (login, OAuth, tokens, sessions, RBAC, API keys)
- Cryptographic operations (encryption, signing, hashing, key generation, key derivation)
- Secret and credential storage (keychains, vaults, env vars, config files with secrets)
- Network communication (HTTP clients, TLS configuration, certificate handling, WebSocket, gRPC)
- Untrusted input processing (file parsing, deserialization, XML/JSON/YAML from external sources)
- IPC and process boundaries (sockets, pipes, CLI subprocesses, shared memory)
- Plugin and extension loading (dynamic imports, ServiceLoader, plugin directories)
- Update and distribution mechanisms (auto-update, download verification, signature checking)
- Implicit network behavior (link previews, auto-fetches, thumbnail generation triggered by remote data)
- Native code / FFI boundaries (C interop, JNI, ctypes, unsafe blocks, bridging headers)

For each flow found, note the relevant files and trace data from input to processing to output.

Read [references/analysis-guide.md](references/analysis-guide.md) for detailed guidance by application type and platform.

## Step 3: Write the Threat Model

Write to `.turbo/threat-model.md` (create `.turbo/` if needed). The document has exactly four sections. Adapt depth to the codebase: a small CLI tool needs less detail than a multi-component crypto system.

### Section 1: Overview

Write 1-2 paragraphs covering:
- What the software is, its deployment model, and high-level architecture with key components (reference source paths)
- Security-sensitive flows as a bulleted list (3-5 items, one sentence each)
- What this repo owns versus what it delegates, and where the largest risks concentrate

For codebases with unique security properties (zero-knowledge design, client-side crypto, opportunistic encryption), call them out explicitly.

### Section 2: Threat Model, Trust Boundaries and Assumptions

**Assets**: What has value to an attacker. Be specific: name data types, key material, tokens, metadata. Group naturally (user data, secrets, integrity artifacts).

**Trust boundaries**: Where trust levels change. Each boundary gets a **bold name**, a colon, 1-2 sentences explaining what crosses it, and a parenthetical code reference. Typical boundaries: untrusted storage/network, local OS/filesystem, IPC, admin configuration, identity provider, database.

**Inputs by control tier**:
- **Attacker-controlled**: Data from untrusted sources that the software parses. For libraries, include data passed through the API from untrusted origins. Reference specific entry points.
- **Operator-controlled**: Configuration, credentials, deployment parameters. Trusted but can be misconfigured.
- **Developer-controlled**: Build scripts, dependency versions, test fixtures, debug-only behavior. The supply chain boundary.

**Assumptions**: Explicit statements about what must be true for the security model to hold. Include environmental assumptions (OS isolation, entropy sources), dependency assumptions (crypto library correctness), and operational assumptions (caller protects passwords). 2-4 bullets.

### Section 3: Attack Surface, Mitigations and Attacker Stories

Organize into subsections by attack surface area (not by STRIDE category or component). Each subsection follows this structure:

```
### [3.N] [Surface Name]
**Surface**: What is exposed and where (1-2 sentences with file references).

**Mitigations**
- What the code already does to defend this surface (observations, not recommendations).

**Attacker stories**
- Concrete scenario: "[Attacker type] does [action] to [goal]: [consequence and severity context]."
```

**Decomposition heuristic**: One surface per distinct trust boundary crossing or distinct attacker capability. If two areas share the same entry points AND mitigations, merge them. If a single surface needs more than 3-4 unrelated risk/mitigation pairs, split it. Typical range: 4-9 surfaces.

**For each surface, document**:
- 1-2 sentence surface description with file references
- 2-4 mitigation bullets describing existing defenses (what the code does, not what it should do)
- 2-3 attacker stories: one sentence each, naming attacker type, action, and consequence

**End section 3 with**: A brief note on vulnerability classes that are less relevant for this application type, explaining why (e.g., "Web-specific issues like XSS and CSRF do not apply because this is a local library without network endpoints").

### Section 4: Criticality Calibration

Group findings into four tiers. Each tier has 2-4 items, each a single sentence describing the **impact** (not the attack vector).

- **Critical**: Remote exploitation compromising crown jewels or achieving code execution. Auth bypass, key/credential theft, RCE, cryptographic bypass.
- **High**: Significant compromise requiring specific preconditions. Privilege escalation, targeted data theft, bypassing a major security control, integration compromise.
- **Medium**: Real but limited impact or unlikely preconditions. Metadata leaks, DoS, policy bypass without data compromise, local data exposure.
- **Low**: Theoretical, requires pre-compromised environment, or minimal impact. Verbose error messages, UI-only issues, log noise, debug-only risks.

Close with a calibration paragraph explaining how the application's deployment model and trust boundaries influence severity. For the attacker-position-vs-impact matrix and application-type adjustments, consult [references/analysis-guide.md](references/analysis-guide.md).

## Step 4: Review

Before presenting the output, validate:

1. **Codebase-specific**: Every claim references actual files, modules, or architectural patterns. No generic filler.
2. **Complete coverage**: All security-sensitive flows from Step 2 appear in at least one attack surface.
3. **Balanced mitigations**: Each surface lists existing defenses. If none exist, state that explicitly.
4. **Concrete stories**: Each attacker story names a specific attacker, action, and consequence. No abstract "an attacker could exploit a vulnerability."
5. **Consistent severity**: Calibration in section 4 is consistent with severity context in section 3 stories.
6. **Appropriate scope**: Dependencies are acknowledged with assumptions, not audited internally. Integration boundaries are analyzed.
7. **Out-of-scope declared**: Irrelevant vulnerability classes are named and dismissed with reasons.

Fix any gaps, then present the threat model to the user.

## Rules

- Ground every claim in code. Reference specific classes, functions, or file paths. Do not speculate about code you have not read.
- When a mitigation is absent, say so explicitly. Do not invent mitigations.
- Do not audit the internals of external dependencies. Analyze the integration boundary only.
- Adapt depth to the project. A 500-line CLI tool does not need the same depth as a cryptographic filesystem library.
- The threat model is the only output. Do not create code, fix vulnerabilities, or modify the codebase.
- Use `##` for the four top-level sections (numbered 1-4), `###` for attack surface subsections, and `**bold**` for sub-headings within subsections.
- If the codebase has no meaningful security surface (no crypto, no auth, no network, no untrusted input), produce a brief threat model stating this with rationale, covering only dependency and supply-chain risks.
