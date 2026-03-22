---
name: arch-lens-deployment
categories: [arch-lens]
description: Create Deployment/Physical architecture diagram showing infrastructure topology, process boundaries, and network communication. Physical lens answering "Where does it run?"
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Deployment Lens - Analyzing infrastructure topology...'"
          once: true
---

# Deployment/Physical Architecture Lens

**Cognitive Mode:** Physical
**Primary Question:** "Where does it run?"
**Focus:** Infrastructure Topology, Process Boundaries, Data Storage Locations, Network Communication

## When to Use

- Need to understand physical deployment
- Documenting infrastructure and processes
- Analyzing where components execute
- User invokes `/autoskillit:arch-lens-deployment` or `/autoskillit:make-arch-diag deployment`

## Critical Constraints

**NEVER:**
- Modify any source code files
- Include code-level details
- Show internal logic

**ALWAYS:**
- Focus on PHYSICAL deployment
- Show process boundaries
- Include network/communication protocols
- Document storage locations
- BEFORE creating any diagram, LOAD the `/autoskillit:mermaid` skill using the Skill tool - this is MANDATORY

---

## Analysis Workflow

### Step 1: Launch Parallel Exploration Subagents

Spawn Explore subagents to investigate:

**Process Boundaries**
- Find main process entry points
- Identify subprocess spawning
- Look for: main, entry_points, subprocess, process spawning, daemon processes

**Container/Docker**
- Find containerization config
- Identify services
- Look for: Dockerfile, docker-compose.yml, container definitions, Kubernetes configs

**Local Storage**
- Find file storage locations
- Identify database paths
- Look for: data directories, database files, storage volumes, persistent storage

**Network Services**
- Find service definitions
- Identify ports and protocols
- Look for: port, bind, listen, server, API, endpoint, network services

**External Services**
- Find external API calls
- Identify cloud services
- Look for: external APIs, cloud services, third-party integrations

**Web/Frontend**
- Find frontend deployment
- Identify static file serving
- Look for: web servers, frontend builds, static assets, CDN

### Step 2: Map Physical Topology

| Component | Location | Technology | Port/Protocol |
|-----------|----------|------------|---------------|
| {name} | {where} | {tech} | {port/protocol} |

**CRITICAL - Analyze Read/Write Direction:**
For EVERY process and storage location:
- **Reads from**: What does this process READ? (files, databases, APIs)
- **Writes to**: What does this process WRITE? (files, databases, APIs)
- **Network direction**: Client->Server or bidirectional?

For storage locations:
- **Read/write storage**: Process both reads and writes (databases, state files)
- **Write-only storage**: Process writes, humans or other systems read (logs, artifacts)
- **Read-only sources**: Process reads, doesn't modify (config, external APIs)

Label all connections with direction (reads, writes, or both)

### Step 3: Identify Communication Paths

- Process-to-process (IPC, subprocess)
- Network (HTTP, WebSocket, gRPC)
- File system (shared files)
- Database (connections)

### Step 4: Create the Diagram

Use flowchart with:

**Direction:** `TB` for infrastructure layers

**Subgraphs by Physical Location:**
- Developer Machine (local processes)
- Local Storage (files, DBs)
- Docker Stack (if containerized)
- Web Stack (if applicable)
- External Services (cloud, APIs)

**Node Styling:**
- `cli` class: Main processes
- `stateNode` class: Local storage, databases
- `output` class: File artifacts
- `handler` class: Services, APIs
- `phase` class: Frontend, web UI
- `integration` class: External services

**Connection Labels:**
- Show protocols (HTTP, subprocess, file)
- Show ports where relevant

### Step 5: Write Output

Write the diagram to: `temp/arch-lens-deployment/arch_diag_deployment_{YYYY-MM-DD_HHMMSS}.md` (relative to the current working directory)

After writing the diagram file, emit a structured output line:

```
diagram_path = {absolute_path_to_diagram_file}
```

---

## Output Template

```markdown
# Deployment Diagram: {System Name}

**Lens:** Deployment/Physical
**Question:** Where does it run?
**Date:** {YYYY-MM-DD}
**Scope:** {What was analyzed}

## Deployment Topology

| Component | Port | Technology | Purpose |
|-----------|------|------------|---------|
| {name} | {port} | {tech} | {purpose} |

## Deployment Diagram

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 50, 'rankSpacing': 60, 'curve': 'basis'}}}%%
flowchart TB
    %% CLASS DEFINITIONS %%
    classDef cli fill:#1a237e,stroke:#7986cb,stroke-width:2px,color:#fff;
    classDef stateNode fill:#004d40,stroke:#4db6ac,stroke-width:2px,color:#fff;
    classDef handler fill:#e65100,stroke:#ffb74d,stroke-width:2px,color:#fff;
    classDef phase fill:#6a1b9a,stroke:#ba68c8,stroke-width:2px,color:#fff;
    classDef output fill:#00695c,stroke:#4db6ac,stroke-width:2px,color:#fff;
    classDef integration fill:#c62828,stroke:#ef9a9a,stroke-width:2px,color:#fff;

    subgraph LocalMachine ["LOCAL MACHINE"]
        direction TB
        MAIN["Main Process<br/>━━━━━━━━━━<br/>Runtime<br/>Orchestration"]
        SUB["Subprocess<br/>━━━━━━━━━━<br/>Isolated execution"]
    end

    subgraph LocalStorage ["LOCAL STORAGE"]
        direction TB
        DB[("Database<br/>━━━━━━━━━━<br/>Technology<br/>Location")]
        FILES["Files<br/>━━━━━━━━━━<br/>Artifacts<br/>Path"]
    end

    subgraph Docker ["DOCKER STACK"]
        direction TB
        SERVICE1["Service<br/>━━━━━━━━━━<br/>:port<br/>Purpose"]
    end

    subgraph Web ["WEB STACK"]
        direction TB
        API["API Server<br/>━━━━━━━━━━<br/>:port<br/>Protocol"]
        FRONTEND["Frontend<br/>━━━━━━━━━━<br/>:port<br/>Technology"]
    end

    subgraph External ["EXTERNAL"]
        direction TB
        CLOUD["Cloud API<br/>━━━━━━━━━━<br/>Protocol<br/>Third-party"]
    end

    %% CONNECTIONS %%
    MAIN -->|"spawns"| SUB
    MAIN -->|"reads/writes"| DB
    MAIN -->|"writes"| FILES
    MAIN -->|"HTTPS"| CLOUD

    SERVICE1 -->|"connects"| DB
    API -->|"REST"| FRONTEND

    %% CLASS ASSIGNMENTS %%
    class MAIN,SUB cli;
    class DB,FILES stateNode;
    class SERVICE1,API handler;
    class FRONTEND phase;
    class CLOUD integration;
```

**Color Legend:**
| Color | Category | Description |
|-------|----------|-------------|
| Dark Blue | Processes | Local CLI and subprocess |
| Teal | Storage | Databases and file storage |
| Orange | Services | Backend services and APIs |
| Purple | Frontend | Web UI |
| Red | External | External/cloud services |

## Communication Protocols

| From | To | Protocol | Purpose |
|------|-----|----------|---------|
| {source} | {target} | {protocol} | {purpose} |

## Storage Locations

| Data | Location | Technology |
|------|----------|------------|
| {data} | {path} | {tech} |
```

---

## Pre-Diagram Checklist

Before creating the diagram, verify:

- [ ] LOADED `/autoskillit:mermaid` skill using the Skill tool
- [ ] Using ONLY classDef styles from the mermaid skill (no invented colors)
- [ ] Diagram will include a color legend table

---

## Related Skills

- `/autoskillit:make-arch-diag` - Parent skill for lens selection
- `/autoskillit:mermaid` - MUST BE LOADED before creating diagram
- `/autoskillit:arch-lens-c4-container` - For container-level view