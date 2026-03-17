---
name: blackhat-go
description: Go-based security techniques from "Black Hat Go" extended with macOS, Cloud, Mobile, IoT, Supply Chain, API, Web3, AI/ML, Red Team, ATT&CK, and LLM chapters. 186 techniques, 36 tools, 33 defenses across 37 chapters. Includes adversarial bisimulation games with Ungar (order-dependent) and join-semilattice structures. AAIF-compatible multiplayer agent games for human-agent security exercises.
version: 1.0.0
---


# BlackHat Go Skill: Security Techniques Knowledge Base

**Status**: ✅ Production Ready  
**Source**: "Black Hat Go" by Steele, Patten, Kottmann (No Starch Press)  
**Extended**: Chapters 15-37 (macOS, Cloud, Mobile, IoT, SupplyChain, API, Web3, AI, RedTeam, ATT&CK, LLM)  
**AAIF Integration**: MCP-native, AGENTS.md compliant, goose-compatible

---

## Overview

Structured knowledge base of offensive security techniques implemented in Go:

- **186 Techniques** across 37 chapters
- **36 Tools** (stdlib + third-party)
- **33 Defenses** with effectiveness ratings
- **6 Exploitation** relationships
- **103 Passing Tests** (including adversarial bisimulation)

## AAIF Integration (Agentic AI Foundation)

This skill is designed for **multiplayer human-agent security games** in the AAIF ecosystem:

### Core AAIF Projects Integrated

| Project | Role | Integration |
|---------|------|-------------|
| **MCP** (Model Context Protocol) | Agent-tool connectivity | Techniques exposed as MCP tools |
| **goose** | Local-first agent framework | Attack chain execution |
| **AGENTS.md** | Project-specific guidance | Security context for agents |

### Multiplayer Game Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AAIF MULTIPLAYER SECURITY GAME                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Browser Clients (CatColab + Automerge CRDT)                              │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│   │ Human 🧑 │  │ Agent 🤖 │  │ Human 🧑 │  │ Agent 🤖 │                   │
│   │ Attacker │  │ Defender │  │ Arbiter  │  │ Observer │                   │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│        │             │             │             │                          │
│        └─────────────┴──────┬──────┴─────────────┘                          │
│                             │                                               │
│                    WebSocket / MCP                                          │
│                             │                                               │
│              ┌──────────────┴──────────────┐                               │
│              │     Automerge Doc Server     │                               │
│              │  (CRDT Real-time Sync)       │                               │
│              └──────────────┬──────────────┘                                │
│                             │                                               │
│              ┌──────────────┴──────────────┐                               │
│              │     CatColab Backend         │                               │
│              │  (Double Category Theory)    │                               │
│              │  • Reachability Analysis     │                               │
│              │  • Bisimulation Checking     │                               │
│              │  • GF(3) Conservation        │                               │
│              └─────────────────────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Three Worlds for Multiplayer Games

| World | Seed | Operator | Game Type | Players |
|-------|------|----------|-----------|---------|
| 🔴 ZAHN | 1069 | ⊗ tensor | **Ungar Games** | Attack chain validation |
| 🟢 JULES | 69 | ⊕ coproduct | **Bisimulation** | Defense equivalence |
| 🔵 FABRIZ | 0 | ⊛ convolution | **Both/Neither** | Arbiter/Observer |

---

## Chapter Index

| Chapters | Domain | Techniques |
|----------|--------|------------|
| 1-14 | Core (Book) | Foundation, Network, Web, Windows, Crypto, RAT |
| 15-24 | macOS | TCC, Keychain, Persistence, Kernel, EDR Bypass |
| 25 | Cloud | K8s Pod Escape, AWS SSRF, Container Enum |
| 26 | Mobile | APK Analysis, Frida, ADB, SSL Pinning |
| 27 | IoT | Firmware, MQTT, CoAP, UART, ZigBee |
| 28 | Supply Chain | Dependency Confusion, CI/CD Injection, Lockfile |
| 29 | API Security | GraphQL, OAuth, JWT, BOLA |
| 30 | Web3/Blockchain | Reentrancy, Flash Loans, Wallet Drainer |
| 31 | AI/ML Security | Prompt Injection, Model Poisoning, Jailbreaks |
| 32 | Red Team Infra | Redirectors, Phishing Infra, C2 Rotation |
| 33 | Reconnaissance | Active Scanning, OSINT, Network Gathering (ATT&CK TA0043) |
| 34 | Resource Dev | Infrastructure, Capabilities, Accounts (ATT&CK TA0042) |
| 35 | Collection | Data Harvesting, Audio/Screen Capture (ATT&CK TA0009) |
| 36 | Lateral Movement | Remote Services, Session Hijacking (ATT&CK TA0008) |
| 37 | LLM/GenAI | OWASP Top 10 LLM 2025, RAG Poisoning, Prompt Leakage |

---

## NEW: Adversarial Bisimulation Games

The knowledge base includes **three game types** from gayzip.gay:

### Join-Semilattice for Security States

The **join-semilattice** enables Ungar Games by providing:

1. **Partial order** on attack/defense states (more compromised > less compromised)
2. **Least upper bounds** (joins) for combining observations
3. **Prerequisite chains** as lattice paths (order matters!)

```go
// SecurityState represents a point in the attack/defense lattice
type SecurityState struct {
    TechniquesExecuted []string  // Attack surface
    DefensesActive     []string  // Protection layer
    RiskLevel          int       // Cumulative risk (0-10)
    Compromised        bool      // System compromised?
}

// Join computes least upper bound
joined := lattice.Join(state1, state2)
// - Techniques: UNION (more attacks)
// - Defenses: INTERSECTION (only surviving defenses)
// - Risk: MAX
```

### Ungar Game (Order Matters)

In Ungar Games, attack chains must respect **prerequisites**:

```go
game := NewUngarGame(kb)

// WRONG ORDER - will fail!
game.AttackerMove("tcp-proxy")  // Error: requires tcp-port-scan first!

// CORRECT ORDER (Ungar constraint satisfied)
game.AttackerMove("go-concurrency")   // No prereqs
game.AttackerMove("tcp-port-scan")    // Requires go-concurrency ✓
game.AttackerMove("tcp-proxy")        // Requires tcp-port-scan ✓
```

### Bisimulation Game (Order Agnostic)

Two security states are **bisimilar** if the Attacker cannot distinguish them:

```go
bisim := NewBisimulationGame(kb, state1, state2)
if bisim.AreBisimilar() {
    // Defender wins: states are observationally equivalent
    // For every attack in state1, Defender can match in state2
}
```

### GF(3) Conservation

Every round maintains **GF(3) trit conservation**:

```
Attacker move: trit = -1 (attack)
Defender move: trit = +1 (defend)
Arbiter verify: trit = 0  (balance)
─────────────────────────────────────
Sum ≡ 0 (mod 3) ✓
```

---

## AAIF Committee Participation Skills

### How to Succeed on Technical Committees

This skill includes patterns for effective participation in AAIF and similar open source governance:

#### 1. MCP Technical Steering Committee (TSC)

**Key responsibilities**:
- Protocol specification evolution
- Security model review
- Interoperability testing

**Success patterns**:
```markdown
# AGENTS.md for MCP TSC Participation

## Context
You are participating in the MCP Technical Steering Committee.

## Decision Framework
1. **Backward Compatibility**: Never break existing MCP servers
2. **Security First**: All changes reviewed for attack surface
3. **Minimal Specification**: Only specify what's necessary
4. **Reference Implementation**: Changes must have working code

## Voting Protocol
- Lazy consensus for minor changes
- 2/3 majority for breaking changes
- Binding votes from TSC members only

## Communication
- Use GitHub Issues for proposals
- RFC process for major changes
- Weekly sync calls (recorded)
```

#### 2. goose Maintainer Best Practices

**Agent framework governance**:
```markdown
# AGENTS.md for goose Contribution

## Architecture Decisions
- Local-first: Never require cloud by default
- MCP-native: All tools exposed via MCP
- Extensible: Plugin architecture for custom tools

## Review Checklist
□ Does this work offline?
□ Is the MCP interface clean?
□ Are there integration tests?
□ Is the documentation updated?

## Release Process
1. Feature freeze (2 weeks before)
2. RC testing with AAIF members
3. Changelog review
4. Tag and publish
```

#### 3. Cross-Foundation Coordination

**Working across AAIF, LF AI & Data, CNCF**:

```markdown
# Multi-Foundation Participation

## Overlapping Interests
- AAIF: Agentic AI protocols (MCP, AGENTS.md)
- LF AI & Data: ML infrastructure (PyTorch, ONNX)
- CNCF: Cloud native (Kubernetes, envoy)

## Coordination Patterns
1. **Joint Working Groups**: Propose cross-foundation WGs
2. **Specification Alignment**: Ensure MCP works with CNCF networking
3. **Shared Governance**: Learn from CNCF's graduated project model

## Committee Meeting Preparation
- Read agenda 24h before
- Prepare 1-2 specific proposals
- Identify blocking issues early
- Follow up in writing within 48h
```

---

## Multiplayer Security Exercise Examples

### Example 1: Browser-Based CTF with Human + Agent Teams

**Setup**: CatColab diagram with attack/defense morphisms

```typescript
// CatColab model for security game
const securityGame = {
  theory: "th_bisimulation_adversarial",
  objects: [
    { id: "initial", type: "SecurityState" },
    { id: "compromised", type: "SecurityState" },
    { id: "defended", type: "SecurityState" }
  ],
  morphisms: [
    { id: "tcp-scan", src: "initial", tgt: "initial", type: "Attack" },
    { id: "ids-deploy", src: "initial", tgt: "defended", type: "Defense" },
    { id: "exploit", src: "initial", tgt: "compromised", type: "Attack" }
  ]
};

// Reachability query: Can attacker reach 'compromised'?
const result = await catcolab.subreachability(model, {
  tokens: { "initial": 1 },
  forbidden: { "compromised": 1 }
});
// result: true (forbidden state is reachable)
```

### Example 2: MCP-Based Agent Attack Chain

**goose agent executing attack chain**:

```yaml
# goose workflow for security testing
name: attack-chain-validation
description: Validate attack chain ordering via MCP

tools:
  - mcp://blackhat-go/techniques
  - mcp://blackhat-go/defenses
  - mcp://catcolab/reachability

steps:
  - name: Load knowledge base
    tool: blackhat-go/load-kb
    
  - name: Propose attack chain
    tool: blackhat-go/validate-chain
    params:
      techniques:
        - go-concurrency
        - tcp-port-scan
        - tcp-proxy
        
  - name: Check reachability
    tool: catcolab/reachability
    params:
      initial: { "defended": 0, "compromised": 0 }
      forbidden: { "compromised": 1 }
```

### Example 3: Real-Time Multiplayer via Automerge

**WebSocket game synchronization**:

```typescript
// Connect to CatColab Automerge server
const repo = new Repo({
  network: [new BrowserWebSocketClientAdapter("wss://catcolab.io/automerge")]
});

// Join security game document
const handle = repo.find(gameDocId);

// Human player makes attack move
handle.change(doc => {
  doc.moves.push({
    player: "human-attacker",
    action: "AttackerMove",
    technique: "tcp-port-scan",
    trit: -1,  // GF(3)
    timestamp: Date.now()
  });
});

// Agent defender responds (via MCP)
const agentResponse = await mcp.invoke("blackhat-go/defender-move", {
  gameState: handle.doc(),
  defense: "ids-ips"
});

// Arbiter verifies GF(3) conservation
const balance = doc.moves.reduce((sum, m) => sum + m.trit, 0);
console.assert(balance % 3 === 0, "GF(3) violated!");
```

---

## High-Risk Techniques (Risk ≥ 8)

```go
// From kb.GetHighRiskTechniques(8) - 30+ techniques:
cicd-injection           // Ch.28, Risk: 10, SupplyChain
smart-contract-reentrancy // Ch.30, Risk: 10, Web3
flash-loan-exploit       // Ch.30, Risk: 10, Web3
private-key-extract      // Ch.30, Risk: 10, Web3
k8s-pod-escape           // Ch.25, Risk: 10, Cloud
process-injection        // Ch.12, Risk: 10, Windows
rat-implant              // Ch.14, Risk: 10, Evasion
dependency-confusion     // Ch.28, Risk: 9, SupplyChain
oauth-token-theft        // Ch.29, Risk: 9, API
wallet-drainer           // Ch.30, Risk: 9, Web3
model-poisoning          // Ch.31, Risk: 9, AI
```

## Categories Summary

| Category | Count | Chapters | Risk Range |
|----------|-------|----------|------------|
| Foundation | 4 | 1 | 0 |
| Network | 12 | 2,5,6 | 2-8 |
| Web | 15 | 3,4 | 2-8 |
| Exploitation | 6 | 9 | 5-10 |
| Evasion | 12 | 13,14 | 3-10 |
| Crypto | 7 | 11 | 2-3 |
| Windows | 4 | 12 | 4-10 |
| macOS | 50 | 15-24 | 2-10 |
| Cloud | 5 | 25 | 3-10 |
| Mobile | 5 | 26 | 3-8 |
| IoT | 5 | 27 | 4-8 |
| SupplyChain | 5 | 28 | 7-10 |
| API | 5 | 29 | 4-9 |
| Web3 | 5 | 30 | 7-10 |
| AI | 11 | 31, 37 | 6-9 |
| RedTeam | 5 | 32 | 4-7 |
| Reconnaissance | 6 | 33 | 2-5 |
| ResourceDev | 5 | 34 | 4-7 |
| Collection | 5 | 35 | 4-7 |
| LateralMovement | 5 | 36 | 6-8 |

## Key Go Packages by Domain

### Core
| Package | Purpose | Chapters |
|---------|---------|----------|
| `net` | TCP/UDP sockets | 2, 5 |
| `net/http` | HTTP client/server | 3, 4 |
| `crypto/*` | Encryption, hashing | 11 |
| `syscall` | Windows API | 12 |
| `debug/macho` | Mach-O parsing | 15 |

### Extended
| Package | Purpose | Chapters |
|---------|---------|----------|
| `k8s.io/client-go` | Kubernetes API | 25 |
| `github.com/eclipse/paho.mqtt.golang` | MQTT | 27 |
| `github.com/ethereum/go-ethereum` | Ethereum | 30 |
| `github.com/golang-jwt/jwt/v5` | JWT | 29 |
| `golang.org/x/oauth2` | OAuth 2.0 | 29 |
| `gonum.org/v1/gonum` | ML/Scientific | 31 |
| `net/http/httputil` | Reverse Proxy | 32 |
| `github.com/projectdiscovery/nuclei` | Vuln Scanning | 33 |
| `github.com/sashabaranov/go-openai` | OpenAI API | 37 |
| `github.com/pgvector/pgvector-go` | Vector DB | 37 |

## Defense Effectiveness

| Defense | Effectiveness | Mitigates |
|---------|--------------|-----------|
| Hardware Wallet | 95% | private-key-extract, wallet-drainer |
| MFA | 95% | credential-harvester, pass-the-hash |
| SIP Enabled | 95% | nvram-persist, dyld-injection |
| Zero Trust | 85% | remote-services, session-hijacking |
| IMDSv2 | 90% | aws-metadata-ssrf, cloud-cred-harvest |
| JWT Validation | 90% | jwt-none-alg, oauth-token-theft |
| EDR | 85% | process-injection, rat-implant |
| Smart Contract Audit | 85% | reentrancy, flash-loan-exploit |
| CI/CD Hardening | 85% | cicd-injection, build-artifact-poison |
| SBOM Verification | 80% | dependency-confusion, typosquatting |
| RAG Guardrails | 75% | rag-poisoning, vector-embedding-attack |

## Usage Patterns

### Query by Chapter
```go
kb := LoadBlackHatKnowledge()
ch33 := kb.GetTechniquesByChapter(33) // Reconnaissance
ch36 := kb.GetTechniquesByChapter(36) // Lateral Movement
ch37 := kb.GetTechniquesByChapter(37) // LLM/GenAI
```

### Query by Category
```go
recon := kb.GetTechniquesByCategory("Reconnaissance")
lateral := kb.GetTechniquesByCategory("LateralMovement")
ai := kb.GetTechniquesByCategory("AI")
```

### Ungar Game (Attack Chain Validation)
```go
game := NewUngarGame(kb)

// Execute attack chain (order matters!)
game.AttackerMove("go-concurrency")
game.AttackerMove("tcp-port-scan")
game.DefenderMove("ids-ips")
game.ArbiterVerify()

game.PrintTranscript() // Colored output
```

### Bisimulation (State Equivalence)
```go
s1 := &SecurityState{TechniquesExecuted: []string{"tcp-port-scan"}}
s2 := &SecurityState{TechniquesExecuted: []string{"tcp-port-scan"}}

bisim := NewBisimulationGame(kb, s1, s2)
if bisim.AreBisimilar() {
    fmt.Println("States are observationally equivalent")
}
```

### Validate Attack Chain
```go
chain := ValidateChain(kb, []string{
    "go-concurrency",
    "tcp-port-scan",
    "tcp-proxy",
})

if chain.IsValid {
    fmt.Println("Chain is Ungar-compliant (order respected)")
} else {
    fmt.Println("Errors:", chain.Errors)
}
```

## Build and Test

```bash
cd ~/ies/music-topos
go test -v ./...       # Run all 103 tests
go run .               # Print knowledge base summary
```

## CatColab Integration

### Double Theory for Bisimulation Games

```rust
// packages/catlog/src/stdlib/theories.rs

/// The theory of adversarial bisimulation games.
/// 
/// Object types:
/// - SecurityState: points in the attack/defense lattice
/// - Player: Attacker(-1), Defender(+1), Arbiter(0)
/// 
/// Morphism types:
/// - Attack: state transitions (ordered by prerequisites)
/// - Defense: mitigation deployments
/// - Verify: arbiter checks (GF(3) conservation)
pub fn th_bisimulation_adversarial() -> DiscreteDblTheory {
    let mut cat = FpCategory::new();
    
    // Object types
    cat.add_ob_generator(name("SecurityState"));
    cat.add_ob_generator(name("Player"));
    
    // Morphism types with GF(3) semantics
    cat.add_mor_generator(name("Attack"), name("SecurityState"), name("SecurityState"));
    cat.add_mor_generator(name("Defense"), name("SecurityState"), name("SecurityState"));
    cat.add_mor_generator(name("Verify"), name("SecurityState"), name("SecurityState"));
    
    // Attack chains compose (Ungar: order matters)
    cat.equate(
        Path::pair(name("Attack"), name("Attack")),
        name("Attack").into()
    );
    
    // Defense is idempotent
    cat.equate(
        Path::pair(name("Defense"), name("Defense")),
        name("Defense").into()
    );
    
    // Attack + Defense + Verify = Identity (GF(3) conservation)
    cat.equate(
        Path::Seq(nonempty![name("Attack"), name("Defense"), name("Verify")]),
        Path::empty(name("SecurityState"))
    );
    
    cat.into()
}
```

### Reachability Analysis for Security Games

```rust
// packages/catlog/src/stdlib/analyses/bisimulation.rs

/// Check if attacker can reach compromised state from initial state
pub fn attack_reachability(
    model: &DiscreteDblModel,
    initial: &SecurityState,
    target: &SecurityState
) -> bool {
    // Use existing reachability infrastructure
    let data = ReachabilityProblemData {
        tokens: state_to_tokens(initial),
        forbidden: state_to_tokens(target),
    };
    
    !subreachability(model.into_modal(), data)
}

/// Check if two security states are bisimilar
pub fn check_bisimilar(
    model: &DiscreteDblModel,
    s1: &SecurityState,
    s2: &SecurityState
) -> bool {
    // For every attack from s1, check s2 can match
    let attacks_from_s1 = get_attacks(model, s1);
    let attacks_from_s2 = get_attacks(model, s2);
    
    attacks_from_s1.iter().all(|a1| {
        attacks_from_s2.iter().any(|a2| {
            attack_equivalent(a1, a2)
        })
    }) && attacks_from_s2.iter().all(|a2| {
        attacks_from_s1.iter().any(|a1| {
            attack_equivalent(a1, a2)
        })
    })
}
```

---

## AAIF Governance Patterns

### Proposal Template for AAIF TSC

```markdown
# RFC: Bisimulation Game Protocol Extension

## Summary
Add adversarial game semantics to MCP for security analysis.

## Motivation
Security testing requires ordered attack chains (Ungar games) and
equivalence checking (bisimulation games). Current MCP lacks game-theoretic
primitives.

## Proposal

### New MCP Message Types

```json
{
  "type": "game/move",
  "role": "attacker" | "defender" | "arbiter",
  "action": {
    "technique": "tcp-port-scan",
    "prerequisites": ["go-concurrency"]
  },
  "trit": -1 | 0 | 1,
  "state_hash": "abc123"
}
```

### GF(3) Conservation Invariant

Every game round MUST satisfy:
```
sum(moves.map(m => m.trit)) ≡ 0 (mod 3)
```

## Backward Compatibility
Fully backward compatible - new message types are optional.

## Security Considerations
- Attack chains validated against prerequisite graph
- GF(3) conservation prevents game state tampering
- Arbiter role required for state transitions

## Implementation
Reference implementation in goose: `goose-bisim-game`
```

### Committee Meeting Participation Checklist

```markdown
## Pre-Meeting (24h before)
□ Review agenda and attached materials
□ Identify items requiring your input
□ Prepare 1-2 specific proposals or questions
□ Check for blocking issues needing resolution

## During Meeting
□ Arrive 5 minutes early for tech check
□ Keep comments focused and time-boxed
□ Use "+1" for agreement, don't repeat points
□ Take notes on action items assigned to you

## Post-Meeting (within 48h)
□ Review meeting notes/recording
□ Complete assigned action items
□ Follow up on any blocking issues in writing
□ Update relevant GitHub issues/PRs
```

---

## File Locations

```
music-topos/blackhat_knowledge.go           # Main knowledge base (3200+ lines)
music-topos/blackhat_knowledge_test.go      # 79 tests
music-topos/bisimulation_adversarial.go     # Ungar/Bisim games (600+ lines)
music-topos/bisimulation_adversarial_test.go # 24 tests
plurigrid/asi/skills/blackhat-go/SKILL.md   # This skill (AAIF-enhanced)
```

---

## Related AAIF Projects

| Project | URL | Integration |
|---------|-----|-------------|
| MCP | github.com/modelcontextprotocol | Technique exposure |
| goose | block.github.io/goose | Agent execution |
| AGENTS.md | agents.md | Context specification |
| CatColab | catcolab.io | Diagram collaboration |

## MCP Dev Summit 2026

**Next Event**: New York City, April 2-3, 2026  
**CFP Open**: Submit proposals for security game presentations  
**URL**: events.linuxfoundation.org/mcp-dev-summit-north-america/

---

*"For AI agents to reach their full potential, developers and enterprises need trustworthy infrastructure and accessible tools to build on."* — Nick Cooper, OpenAI

## r2con Speaker Resources

| Speaker | Handle | Repository | Relevance |
|---------|--------|------------|-----------|
| oleavr | oleavr | [frida-core](https://github.com/frida/frida-core) | Dynamic instrumentation for mobile/desktop security |
| oleavr | oleavr | [cryptoshark](https://github.com/nicknisi/cryptoshark) | Self-modifying code analysis |
| cryptax | cryptax | [droidlysis](https://github.com/cryptax/droidlysis) | Android malware automated analysis |
| cryptax | cryptax | [APKiD](https://github.com/rednaga/APKiD) | Android application identifier (packers, protectors) |
| iGio90 | iGio90 | [Dwarf](https://github.com/iGio90/Dwarf) | Full-featured Frida GUI debugger |

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
blackhat-go (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch6: Layering
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch7: Propagators

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
