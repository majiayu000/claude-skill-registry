# Setup — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the setup skill — key resources defining the Model Context
Protocol (MCP) specification, the ENCODE data portal API, and project documentation that inform
server installation, configuration, and connectivity.

The setup skill guides users through installing the ENCODE MCP server, configuring API credentials
(optional, for unreleased data), verifying tool connectivity, and understanding the plugin's
capabilities. Setup requires understanding three foundational resources: the MCP specification
that defines server-client communication, the ENCODE portal API that the server wraps, and the
ENCODE documentation for data access patterns and troubleshooting.

These 3 references are organized by their role in setup: (1) the MCP specification for
server-client communication, (2) the ENCODE portal paper for the wrapped API, and (3) the
ENCODE documentation for detailed reference and troubleshooting.

---

## Model Context Protocol

The Model Context Protocol (MCP) is the standardized interface between AI assistants and
external tools/data sources. Understanding MCP is essential for setup because it determines
how the server is registered with clients (Claude Desktop, Claude Code), how tool definitions
are exposed, and how errors are communicated.

---

### Anthropic 2024 — Model Context Protocol (MCP) specification

- **Citation:** Anthropic. Model Context Protocol Specification, v2024-11-05. Published at
  modelcontextprotocol.io, 2024.
- **DOI:** N/A (technical specification)
- **PMID:** N/A | **PMC:** N/A
- **Citations:** N/A (industry standard specification)
- **Key findings:** MCP defines a JSON-RPC 2.0 interface between AI clients and servers.
  Three primitive types:
  - **Tools:** executable functions with typed parameters and return values
  - **Resources:** data sources addressable by URI
  - **Prompts:** templated interaction patterns

  The ENCODE server implements the Tools primitive, exposing 20 tools for searching,
  downloading, tracking, and cross-referencing. Each tool has a name, description, and
  JSON Schema-defined input/output types.

  Two transport mechanisms:
  - **stdio:** standard I/O for local servers (subprocess communication)
  - **SSE:** Server-Sent Events for remote HTTP servers

  The ENCODE server uses stdio transport — it runs as a subprocess of the client and
  communicates via JSON-RPC on stdin/stdout. This requires registration in the client's
  config file:
  - Claude Desktop: claude_desktop_config.json
  - Claude Code: .claude/settings.json

  The specification also defines:
  - Capability negotiation (server declares supported primitives)
  - Error handling (structured error codes and messages)
  - Logging (server emits log messages at severity levels)

  Understanding these mechanisms is essential for troubleshooting setup: missing tools
  indicates failed capability negotiation; tool errors provide diagnostic codes. The
  setup skill validates connectivity by listing tools and testing a query.

---

## ENCODE Data Portal

The ENCODE portal is the primary data source the MCP server wraps. Understanding the API is
essential for setup because it determines query capabilities, authentication, and rate limits.

---

### Davis et al. 2018 — ENCODE portal REST API

- **Citation:** Davis CA, Hitz BC, Sloan CA, Chan ET, Davidson JM, Gabdank I, Hilton JA,
  Jain K, Baymuradov UK, Narayanan AK, Onate KC, Graham K, Miyasato SR, Dreszer TR,
  Strattan JS, Jolanki O, Tanaka FY, Cherry JM. The Encyclopedia of DNA elements (ENCODE):
  data portal update. *Nucleic Acids Research*, 46(D1), D794-D801, 2018.
- **DOI:** [10.1093/nar/gkx1081](https://doi.org/10.1093/nar/gkx1081)
- **PMID:** 29126249 | **PMC:** PMC5753278
- **Citations:** ~400
- **Key findings:** Documented the ENCODE REST API:
  - Endpoints: /search/, /experiments/, /files/, /biosample-types/
  - Query syntax: field=value with URL encoding
  - Response format: JSON-LD with @context, @id, @type fields
  - Pagination: limit and offset parameters
  - Authentication: HTTP Basic Auth (access_key:secret_key)

  Rate limiting: ~10 requests/second for unauthenticated access. The MCP server respects
  this through request throttling. Authentication is optional — all released data is
  public. Credentials are only needed for unreleased/embargoed datasets. The setup skill
  configures credentials using OS keyring (macOS Keychain, Linux Secret Service, Windows
  Credential Locker) for secure storage, never in plaintext config files.

  Controlled vocabularies determine valid query parameters:
  - biosample_ontology: UBERON, CL, CLO, EFO terms
  - assay_title: standardized assay names
  - organism: Homo sapiens, Mus musculus
  - target: gene symbols (TF ChIP) or histone marks (histone ChIP)

  The setup skill tests connectivity with a simple search query, verifying that the
  response contains valid ENCODE metadata. Common setup issues:
  - Network: firewall blocking outbound HTTPS
  - Environment: missing Python dependencies
  - Version: MCP SDK compatibility conflicts

---

## ENCODE Project Documentation

The ENCODE project documentation serves as the reference manual for data access, experimental
standards, and troubleshooting — complementing the portal paper with practical guidance that
evolves with the project.

---

### ENCODE Project Consortium — Official documentation

- **Citation:** ENCODE Project Consortium. ENCODE Project Documentation. Published at
  encodeproject.org/help, continuously updated.
- **DOI:** N/A (online documentation)
- **PMID:** N/A | **PMC:** N/A
- **Citations:** N/A (reference documentation)
- **Key findings:** Comprehensive guidance organized into sections relevant to setup:

  **Getting Started:** Portal navigation, search interface, experiment/file hierarchy.
  Explains the relationship between experiments (ENCSR), replicates, and files (ENCFF)
  that the MCP tools expose.

  **REST API:** Detailed programmatic access examples using curl, Python requests, and
  other clients. Includes searching, metadata retrieval, batch manifests, and
  authentication with access keys.

  **File Formats:** ENCODE conventions for BED narrowPeak, broadPeak, bigWig, BAM, FASTQ.
  Format understanding is important because download and file listing tools return
  format-specific metadata.

  **Data Standards:** Assay-specific quality thresholds surfaced through the audit system.
  Each assay (ChIP-seq, ATAC-seq, RNA-seq, WGBS, Hi-C) has documented requirements
  determining ERROR, NOT_COMPLIANT, or WARNING flags.

  **Antibody Characterization:** Validation tiers for ChIP-seq antibodies (primary and
  secondary characterization) affecting data reliability scores.

  Users are directed to these sections when setup validation identifies configuration
  problems, when they need deeper understanding beyond what MCP tools expose, or when
  they encounter unfamiliar metadata terms.

---
