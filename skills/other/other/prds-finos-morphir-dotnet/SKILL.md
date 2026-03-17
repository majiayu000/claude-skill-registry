---
title: "PRD: Morphir Application Architect Skill"
linkTitle: "Architect Skill"
weight: 100
description: >
  Product Requirements Document for the Morphir Application Architect expert skill - a comprehensive guru for architecture, language design, ecosystem integration, and future-facing technical enhancement.
status: Draft
created: 2025-12-23
last_updated: 2025-12-23
---

# PRD: Morphir Application Architect Skill

## Executive Summary

The Morphir Application Architect skill ("morphir-architect") is a comprehensive expert system that combines deep knowledge of:
- Morphir specifications and ecosystem
- Programming language design (ASTs, CSTs, IRs, type systems)
- Functional programming patterns and design principles
- Cross-language integration patterns (bridging FP and OO worlds)
- WebAssembly Component Model and polyglot architecture
- Semantic web technologies (RDF, JSON-LD, linked data)
- Pluggable pipeline architectures (inspired by unified.js/unist)

This skill serves as the master architect for morphir-dotnet, capable of designing sophisticated technical enhancements, guiding architectural evolution, and leveraging deep ecosystem knowledge to make informed decisions about the project's future direction.

**Integration Technologies Expertise**: The architect is intimately familiar with modern integration protocols including gRPC, JSON-RPC, and JSON Lines (JSONL/NDJSON) for building robust service communication layers and streaming data pipelines.

## Problem Statement

### Current Challenges

1. **Fragmented Expertise**: Deep Morphir knowledge is currently distributed across multiple skills (elm-to-fsharp-guru, aot-guru) without a unifying architectural vision
2. **Language Tool Gaps**: morphir-dotnet needs stronger patterns for AST/CST manipulation, visitor patterns, and transformation pipelines
3. **Ecosystem Integration**: Limited guidance on WebAssembly integration strategies, Component Model usage, and polyglot interop
4. **Extensibility Constraints**: Need better patterns for pluggable transformations inspired by unified.js's ecosystem
5. **Attribution Gaps**: Limited use of semantic web technologies (RDF, JSON-LD) for IR attribution and provenance

### Opportunity

Create a comprehensive architectural skill that:
- Provides holistic guidance on Morphir ecosystem integration
- Designs pluggable, extensible transformation pipelines
- Guides WebAssembly/Component Model integration strategy
- Applies semantic web patterns to IR attribution
- Bridges functional and OO paradigms effectively
- Maintains deep knowledge of language tooling patterns

## Goals and Non-Goals

### Goals

**Primary Goals:**
1. **Architectural Excellence**: Design coherent, extensible architectures for morphir-dotnet enhancements
2. **Ecosystem Mastery**: Maintain deep knowledge of entire Morphir ecosystem (elm, core, dotnet)
3. **Future-Facing**: Guide project toward WebAssembly Component Model integration
4. **Pluggable Design**: Create transformation pipelines with unified.js-like extensibility
5. **Semantic Enrichment**: Apply RDF/JSON-LD for attribution and linked data

**Secondary Goals:**
1. Integration pattern library for cross-language scenarios
2. Visitor pattern implementations for AST/IR traversal
3. Documentation of architectural decisions and rationale
4. Collaboration with other skills (aot-guru, elm-to-fsharp-guru, technical-writer)

### Non-Goals

1. **Implementation Details**: Architect focuses on design; delegates implementation to specialized skills
2. **Day-to-Day Bug Fixes**: Not a general-purpose debugging skill
3. **Build System Management**: Architecture guidance only, not build configuration
4. **Direct User Support**: Technical architecture, not end-user troubleshooting

## User Personas

### Persona 1: Morphir Core Maintainer
**Name**: Sarah (Lead Developer)
**Goals**:
- Design extensible IR transformation pipelines
- Plan WebAssembly Component Model integration
- Ensure architectural coherence across ecosystem

**Needs**:
- Deep knowledge of Morphir specs and ecosystem
- Guidance on pluggable architecture patterns
- WebAssembly/WIT expertise
- Semantic web integration patterns

### Persona 2: Language Integration Developer
**Name**: Marcus (Backend Engineer)
**Goals**:
- Integrate Morphir with new target languages
- Build custom transformation plugins
- Bridge OO and FP paradigms

**Needs**:
- Visitor pattern implementations
- AST/CST traversal strategies
- Cross-language integration patterns
- Pluggable pipeline design

### Persona 3: WebAssembly Integration Specialist
**Name**: Priya (DevOps/Platform Engineer)
**Goals**:
- Integrate morphir-dotnet with Wasm Component Model
- Build polyglot Morphir toolchain
- Leverage Extism for plugin architecture

**Needs**:
- Component Model expertise (WIT, WAC)
- Canonical ABI knowledge
- Extism integration patterns
- Cross-runtime communication strategies

## Feature Requirements

### Phase 1: Core Architectural Guidance (Weeks 1-4)

#### Feature 1.1: Morphir Ecosystem Deep Dive
**Priority**: P0 (Critical)
**Status**: ⏳ Planned

**Requirements**:
- Comprehensive knowledge of morphir-elm, morphir-core, morphir-dotnet
- Understanding of IR format evolution (v1, v2, v3)
- Familiarity with all Morphir tooling (CLI, SDK, visualization)
- Cross-repository pattern recognition

**Acceptance Criteria**:
- Can answer questions about any part of Morphir ecosystem
- Can identify architectural patterns across repositories
- Can suggest improvements based on ecosystem-wide knowledge

#### Feature 1.2: Language Design Expertise
**Priority**: P0 (Critical)
**Status**: ⏳ Planned

**Requirements**:
- Deep understanding of AST, CST, IR representations
- Knowledge of type system design
- Familiarity with semantic analysis and transformation
- Understanding of parser design patterns

**Acceptance Criteria**:
- Can design AST/CST transformations
- Can implement visitor patterns for IR traversal
- Can advise on type system extensions
- Can optimize transformation pipelines

#### Feature 1.3: Functional Programming Patterns
**Priority**: P0 (Critical)
**Status**: ⏳ Planned

**Requirements**:
- Mastery of FP design patterns (monads, functors, applicatives, lenses)
- Railway-oriented programming
- Algebraic data types and pattern matching
- Immutability and effect management

**Acceptance Criteria**:
- Can design FP-first architectures
- Can bridge FP and OO paradigms (visitor pattern, etc.)
- Can recommend FP patterns for specific scenarios
- Can refactor imperative code to FP style

### Phase 2: Pluggable Pipeline Architecture (Weeks 5-8)

#### Feature 2.1: Unified.js-Inspired Pipeline Design
**Priority**: P0 (Critical)
**Status**: ⏳ Planned

**Requirements**:
- Study unified.js architecture (processor, parser, transformer, compiler)
- Study unist (Universal Syntax Tree) specification
- Design .NET/F# equivalent with strong typing
- Create plugin interface for transformations

**Acceptance Criteria**:
- Documented pipeline architecture (ADR)
- Plugin interface design
- Example transformation plugins
- Integration with existing IR structure

**Inspiration**:
```typescript
// unified.js style
unified()
  .use(morphirParser)        // Parse source to IR
  .use(typeValidator)         // Validate types
  .use(optimizationPlugin)    // Optimize IR
  .use(codeGenerator)         // Generate target code
  .process(sourceCode)

// F# equivalent
morphir {
    parse morphirSource
    validate typeRules
    optimize optimizationRules
    generate targetLanguage
}
```

#### Feature 2.2: VFile-Inspired Metadata Management
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Study vfile (virtual file) metadata pattern
- Design metadata attachment for IR nodes
- Support provenance tracking
- Enable transformation history

**Acceptance Criteria**:
- Metadata model for IR nodes
- Source location tracking
- Transformation history
- Error reporting with context

#### Feature 2.3: Chain of Responsibility Pattern
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Design chain of responsibility for IR transformations
- Enable dynamic pipeline composition
- Support transformation ordering constraints
- Handle transformation failures gracefully

**Acceptance Criteria**:
- Transformation chain interface
- Pipeline composition API
- Error handling strategy
- Example transformation chains

### Phase 3: WebAssembly Integration Strategy (Weeks 9-12)

#### Feature 3.1: Component Model Expertise
**Priority**: P0 (Critical)
**Status**: ⏳ Planned

**Requirements**:
- Deep knowledge of WebAssembly Component Model
- Understanding of WIT (WebAssembly Interface Types)
- Familiarity with WAC (WebAssembly Compositions)
- Knowledge of Canonical ABI

**Acceptance Criteria**:
- Can design WIT interfaces for Morphir IR
- Can map Morphir types to Component Model types
- Can advise on component composition strategies
- Can design polyglot Morphir toolchain

**Example WIT Interface**:
```wit
// morphir.wit
interface morphir-ir {
  // Type definitions
  record package-name {
    path: list<string>,
    name: string,
  }

  record type-definition {
    name: package-name,
    params: list<string>,
    constructors: list<constructor>,
  }

  // Transformation functions
  validate: func(ir: string) -> result<_, validation-error>
  optimize: func(ir: string) -> result<string, error>
  generate: func(ir: string, target: string) -> result<string, error>
}
```

#### Feature 3.2: Extism Plugin Architecture
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Understanding of Extism plugin framework
- Design Morphir transformations as Extism plugins
- Enable polyglot plugin development (any WASM language)
- Support plugin discovery and loading

**Acceptance Criteria**:
- Extism integration design
- Example transformation plugin in Rust/Go/C#
- Plugin interface specification
- Plugin loading and execution strategy

#### Feature 3.3: Cross-Runtime Communication
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Design communication between .NET, Elm, and WASM runtimes
- Optimize IR serialization for WASM boundary
- Handle type marshalling across runtimes
- Support async operations across boundaries

**Acceptance Criteria**:
- Cross-runtime communication strategy
- IR serialization format for WASM
- Type mapping documentation
- Performance benchmarks

### Phase 4: Semantic Web Integration (Weeks 13-16)

#### Feature 4.1: RDF Knowledge Graphs
**Priority**: P2 (Medium)
**Status**: ⏳ Planned

**Requirements**:
- Design RDF representation of Morphir IR
- Create ontology for Morphir concepts
- Enable SPARQL queries over IR
- Support reasoning over type relationships

**Acceptance Criteria**:
- RDF schema for Morphir IR
- Example RDF triples
- SPARQL query examples
- Integration strategy

**Example RDF Representation**:
```turtle
@prefix morphir: <http://morphir.finos.org/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:MyModule a morphir:Module ;
  morphir:hasType :UserType ;
  morphir:hasFunction :validateUser .

:UserType a morphir:CustomType ;
  morphir:hasConstructor :User ;
  morphir:inPackage :MyPackage .
```

#### Feature 4.2: JSON-LD Attribution
**Priority**: P2 (Medium)
**Status**: ⏳ Planned

**Requirements**:
- Design JSON-LD context for Morphir IR
- Add attribution metadata to IR nodes
- Support provenance tracking
- Enable linked data traversal

**Acceptance Criteria**:
- JSON-LD context definition
- Attribution metadata schema
- Provenance examples
- Linked data navigation patterns

**Example JSON-LD**:
```json
{
  "@context": {
    "@vocab": "http://morphir.finos.org/vocab#",
    "source": "http://purl.org/dc/terms/source",
    "author": "http://purl.org/dc/terms/creator"
  },
  "@type": "TypeDefinition",
  "@id": "morphir:package:module:User",
  "name": "User",
  "source": "src/MyModule.elm",
  "author": "mailto:dev@example.com",
  "constructors": [...]
}
```

#### Feature 4.3: Linked Data Navigation
**Priority**: P2 (Medium)
**Status**: ⏳ Planned

**Requirements**:
- Support dereferencing IR nodes as URIs
- Enable navigation between related types
- Provide REST API for IR exploration
- Support content negotiation (JSON/RDF/Turtle)

**Acceptance Criteria**:
- URI scheme for IR nodes
- Navigation interface
- Content negotiation implementation
- API documentation

### Phase 4.5: Integration Technologies (Weeks 15-16)

#### Feature 4.5.1: gRPC Integration Design
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Design gRPC service definitions for Morphir operations
- Create Protocol Buffers (.proto) for IR types
- Support bidirectional streaming for transformations
- Enable service discovery and health checks

**Acceptance Criteria**:
- Proto definitions for core IR types
- Service definitions for validation, optimization, generation
- Streaming transformation support
- gRPC-Web support for browser clients

**Example Proto Definition**:
```protobuf
syntax = "proto3";
package morphir.ir;

// Core IR types
message PackageName {
  repeated string path = 1;
  string name = 2;
}

message TypeDefinition {
  PackageName name = 1;
  repeated string type_params = 2;
  repeated Constructor constructors = 3;
}

// Transformation service
service MorphirTransform {
  // Unary: Single IR validation
  rpc Validate(IR) returns (ValidationResult);

  // Server streaming: IR optimizations with progress
  rpc Optimize(IR) returns (stream OptimizationStep);

  // Bidirectional: Interactive code generation
  rpc Generate(stream GenerateRequest) returns (stream GenerateResponse);
}
```

#### Feature 4.5.2: JSON-RPC Integration Design
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Design JSON-RPC 2.0 API for Morphir operations
- Support both request/response and notification patterns
- Enable batch requests for multiple transformations
- Provide WebSocket transport option

**Acceptance Criteria**:
- JSON-RPC 2.0 spec compliance
- API documentation with examples
- Batch request support
- Error code standardization

**Example JSON-RPC API**:
```json
{
  "jsonrpc": "2.0",
  "method": "morphir.ir.validate",
  "params": {
    "ir": {...},
    "schemaVersion": "3"
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "isValid": true,
    "schemaVersion": "3",
    "warnings": []
  },
  "id": 1
}

// Batch request
[
  {"jsonrpc": "2.0", "method": "morphir.ir.validate", "params": {...}, "id": 1},
  {"jsonrpc": "2.0", "method": "morphir.ir.optimize", "params": {...}, "id": 2}
]
```

#### Feature 4.5.3: JSON Lines (JSONL/NDJSON) Integration
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Support JSON Lines format for streaming IR data
- Enable pipeline chaining via stdin/stdout
- Design efficient bulk transformation workflows
- Support progress reporting via JSONL

**Acceptance Criteria**:
- JSONL parser/serializer for IR
- stdin/stdout pipeline support
- Bulk transformation examples
- Progress reporting protocol

**Example JSONL Pipeline**:
```bash
# Stream multiple IR files through transformation pipeline
cat ir-files.jsonl | \
  morphir-dotnet transform --jsonl validate | \
  morphir-dotnet transform --jsonl optimize | \
  morphir-dotnet transform --jsonl generate --target scala > output.jsonl
```

**JSONL Format**:
```jsonl
{"type":"package","name":["com","example"],"modules":[...]}
{"type":"module","name":"User","types":[...]}
{"type":"validation-result","isValid":true,"timestamp":"2025-12-23T10:00:00Z"}
```

**Use Cases**:
- Log streaming and analysis
- Bulk IR transformation jobs
- Unix pipeline integration
- Real-time transformation monitoring

### Phase 5: Integration and Documentation (Weeks 17-20)

#### Feature 5.1: Skill Integration
**Priority**: P0 (Critical)
**Status**: ⏳ Planned

**Requirements**:
- Coordinate with aot-guru on WASM compilation
- Coordinate with elm-to-fsharp-guru on transformations
- Coordinate with technical-writer on documentation
- Create collaboration playbooks

**Acceptance Criteria**:
- Integration points documented
- Cross-skill workflows defined
- Handoff protocols established
- Example multi-skill scenarios

#### Feature 5.2: Pattern Catalog
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Document architectural patterns discovered
- Create pattern catalog with examples
- Provide decision trees for pattern selection
- Maintain pattern evolution history

**Acceptance Criteria**:
- Pattern catalog with 20+ patterns
- Decision trees for common scenarios
- Code examples for each pattern
- Pattern evolution documentation

#### Feature 5.3: Comprehensive Documentation
**Priority**: P1 (High)
**Status**: ⏳ Planned

**Requirements**:
- Architecture guides (pluggable pipeline, WASM integration)
- API documentation for new interfaces
- Tutorial series for plugin development
- Diagrams (Mermaid, PlantUML)

**Acceptance Criteria**:
- Architecture guide published
- API docs complete
- 3+ tutorials created
- 10+ diagrams illustrating concepts

## Technical Architecture

### Skill Structure

```
.claude/skills/morphir-architect/
├── skill.md                          # Main skill definition
├── README.md                          # Quick reference
├── MAINTENANCE.md                     # Evolution guide
├── metadata.yaml                      # Skill metadata
├── scripts/                           # Automation scripts
│   ├── analyze-morphir-ir.fsx         # IR analysis
│   ├── generate-wit-interface.fsx     # WIT generation
│   ├── validate-pipeline.fsx          # Pipeline validation
│   ├── rdf-converter.fsx              # IR to RDF conversion
│   └── architecture-report.fsx        # Architecture health check
├── templates/                         # Reusable templates
│   ├── transformation-plugin.template.fs
│   ├── wit-interface.template.wit
│   ├── adr-template.md
│   └── pipeline-config.template.json
├── patterns/                          # Pattern catalog
│   ├── visitor-pattern.md
│   ├── transformation-chain.md
│   ├── wasm-integration.md
│   ├── semantic-attribution.md
│   └── pluggable-pipeline.md
└── examples/                          # Reference implementations
    ├── type-validator-plugin/
    ├── optimization-plugin/
    ├── wasm-code-generator/
    └── rdf-exporter/
```

### Core Competencies

1. **Morphir Ecosystem Mastery**
   - Deep knowledge of all Morphir repositories
   - IR format evolution and compatibility
   - Cross-tool integration strategies

2. **Language Design Expertise**
   - AST/CST manipulation
   - Type system design
   - Transformation pipeline architecture
   - Visitor and interpreter patterns

3. **Functional Design Patterns**
   - Pure functional architecture
   - Bridging FP and OO paradigms
   - Effect management strategies
   - ADT-first design

4. **Pluggable Architecture**
   - Unified.js-inspired pipelines
   - Chain of responsibility pattern
   - Plugin interfaces and discovery
   - Dynamic composition

5. **WebAssembly Integration**
   - Component Model expertise
   - WIT/WAC interface design
   - Extism plugin development
   - Cross-runtime communication

6. **Semantic Web Technologies**
   - RDF knowledge graphs
   - JSON-LD linked data
   - Ontology design
   - SPARQL querying

7. **Integration Protocols**
   - gRPC service design and Protocol Buffers
   - JSON-RPC 2.0 API design
   - JSON Lines (JSONL/NDJSON) streaming
   - RESTful API design patterns

### Decision Trees

#### Decision Tree 1: "When to Use Morphir Architect?"

```
Need architectural guidance?
  YES → What type of problem?
    ├─ High-level system design → Use Morphir Architect
    ├─ AOT/trimming issues → Delegate to aot-guru
    ├─ Elm migration → Delegate to elm-to-fsharp-guru
    ├─ Testing strategy → Delegate to qa-tester
    ├─ Documentation → Delegate to technical-writer
    └─ Cross-cutting architectural concern → Use Morphir Architect

  NO → Use specialized skill
```

#### Decision Tree 2: "Which Pipeline Architecture?"

```
Need IR transformation pipeline?
  ├─ Simple linear transformations → Direct function composition
  ├─ 3-5 transformations, fixed order → Chain of responsibility
  ├─ Dynamic plugin loading required → Pluggable pipeline
  ├─ Cross-language plugins needed → Extism + WASM
  └─ Highly configurable, user-defined → Unified.js-inspired architecture
```

#### Decision Tree 3: "WebAssembly Integration Strategy?"

```
WebAssembly integration needed?
  ├─ Single language, static linking → WASI
  ├─ Multi-language composition → Component Model
  ├─ Dynamic plugin loading → Extism
  ├─ Complex data structures → WIT + Canonical ABI
  └─ Performance-critical → Native AOT + WASM-AOT
```

#### Decision Tree 4: "Which Integration Protocol?"

```
Need service-to-service communication?
  ├─ High-performance, low-latency required → gRPC
  │   ├─ Streaming transformations? → Bidirectional gRPC streaming
  │   ├─ Browser clients needed? → gRPC-Web
  │   └─ Service mesh integration? → gRPC with Envoy/Linkerd
  │
  ├─ Simple request/response over HTTP → JSON-RPC 2.0
  │   ├─ Batch operations needed? → JSON-RPC batch requests
  │   ├─ WebSocket transport? → JSON-RPC over WebSocket
  │   └─ RESTful preferred? → REST with JSON
  │
  ├─ Bulk data processing / streaming → JSON Lines (JSONL)
  │   ├─ Unix pipeline integration? → JSONL via stdin/stdout
  │   ├─ Real-time monitoring? → JSONL streaming with progress
  │   └─ Log aggregation? → JSONL with structured logging
  │
  └─ Complex workflows combining multiple protocols
      → Use all three as appropriate for each use case
```

## Success Metrics

### Phase 1 Metrics (Weeks 1-4)
- [ ] 95%+ accuracy answering Morphir ecosystem questions
- [ ] 3+ AST/CST transformation patterns documented
- [ ] 5+ FP design pattern examples created

### Phase 2 Metrics (Weeks 5-8)
- [ ] Pluggable pipeline architecture ADR approved
- [ ] 3+ example transformation plugins working
- [ ] Pipeline API documented with examples

### Phase 3 Metrics (Weeks 9-12)
- [ ] WIT interface for Morphir IR designed
- [ ] Extism integration proof-of-concept working
- [ ] Cross-runtime communication documented

### Phase 4 Metrics (Weeks 13-16)
- [ ] RDF schema for Morphir IR published
- [ ] JSON-LD context created
- [ ] 10+ SPARQL query examples

### Phase 4.5 Metrics (Weeks 15-16)
- [ ] gRPC service definitions created
- [ ] Protocol Buffers for IR types designed
- [ ] JSON-RPC 2.0 API specified
- [ ] JSONL streaming pipeline working

### Phase 5 Metrics (Weeks 17-20)
- [ ] 20+ patterns in catalog
- [ ] 3+ architecture guides published
- [ ] 5+ integration playbooks created

## Dependencies and Constraints

### Dependencies

**Internal Dependencies**:
- **aot-guru**: WASM compilation guidance
- **elm-to-fsharp-guru**: Transformation pattern expertise
- **technical-writer**: Documentation and diagrams
- **qa-tester**: Architecture validation testing

**External Dependencies**:
- Morphir ecosystem (morphir-elm, morphir-core)
- WebAssembly Component Model specification
- Extism plugin framework
- RDF/JSON-LD standards

### Constraints

**Technical Constraints**:
- Must maintain backward compatibility with existing IR formats
- WASM integration must support both browser and server runtimes
- RDF ontology must align with W3C best practices
- Pluggable pipeline must be AOT-compatible

**Resource Constraints**:
- Skills are documentation-only (no runtime execution)
- Automation scripts must be self-contained
- Pattern catalog must be maintainable

## Open Questions

1. **Q**: Should the pluggable pipeline use Myriad for code generation?
   **Status**: Open
   **Decision Needed By**: Phase 2, Week 5

2. **Q**: Which RDF library should we recommend for .NET?
   **Status**: Open
   **Options**: dotNetRDF, RDFSharp
   **Decision Needed By**: Phase 4, Week 13

3. **Q**: Should we create a separate morphir-wasm repository for Component Model interfaces?
   **Status**: Open
   **Decision Needed By**: Phase 3, Week 9

4. **Q**: How should we version the WIT interfaces?
   **Status**: Open
   **Decision Needed By**: Phase 3, Week 10

## Implementation Notes

### Phase Selection
Start with Phase 1 (Core Architectural Guidance) as it provides the foundation for all other phases.

### Automation Script Priority
1. `analyze-morphir-ir.fsx` - Immediate value for understanding IR structure
2. `architecture-report.fsx` - Continuous health monitoring
3. `validate-pipeline.fsx` - Essential for Phase 2
4. `generate-wit-interface.fsx` - Essential for Phase 3
5. `rdf-converter.fsx` - Nice-to-have for Phase 4

### Pattern Catalog Seed
Start with 10 core patterns:
1. Visitor pattern for IR traversal
2. Transformation chain pattern
3. Plugin interface design
4. Type-safe builder pattern
5. Railway-oriented pipeline
6. Effect management at edges
7. ADT-first modeling
8. Smart constructor pattern
9. Lens-based transformation
10. Provenance tracking pattern

## Future Considerations

### Post-MVP Enhancements
- Visual pipeline editor (web-based)
- AI-assisted transformation generation
- Performance profiling for transformation chains
- Distributed IR processing
- Real-time collaboration on IR design

### Integration Opportunities
- GitHub Actions for automatic architecture validation
- VS Code extension for pipeline visualization
- Language Server Protocol for Morphir IR
- Browser-based IR explorer with semantic navigation

## Appendices

### Appendix A: Unified.js Study

**Key Concepts to Adopt**:
1. **Processor**: Central coordination of pipeline
2. **Plugin Interface**: Uniform transformation API
3. **AST Utilities**: Helper functions for tree manipulation
4. **Metadata Attachment**: VFile-style metadata on nodes

**Key Differences for .NET**:
1. Strong typing instead of duck typing
2. Immutable data structures by default
3. F# computation expressions instead of promises
4. AOT-compatible plugin loading

### Appendix B: Component Model Resources

**Essential Reading**:
- [WebAssembly Component Model](https://github.com/WebAssembly/component-model)
- [WIT Specification](https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md)
- [Canonical ABI](https://github.com/WebAssembly/component-model/blob/main/design/mvp/CanonicalABI.md)
- [Extism Documentation](https://extism.org/docs/)

### Appendix C: RDF/Linked Data Resources

**Essential Reading**:
- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- [Linked Data Principles](https://www.w3.org/DesignIssues/LinkedData.html)

### Appendix D: Integration Protocols Comparison

| Feature | gRPC | JSON-RPC | JSON Lines |
|---------|------|----------|------------|
| **Transport** | HTTP/2 | HTTP/1.1, WebSocket | Stdin/Stdout, HTTP, Files |
| **Serialization** | Protocol Buffers | JSON | Newline-delimited JSON |
| **Streaming** | ✅ Bidirectional | ❌ (use WebSocket) | ✅ Line-by-line |
| **Browser Support** | ⚠️ (via gRPC-Web) | ✅ Native | ⚠️ (via fetch) |
| **Type Safety** | ✅ Strong (Protobuf) | ⚠️ (JSON Schema) | ⚠️ (JSON Schema) |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Simplicity** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Batch Operations** | ⚠️ (stream) | ✅ Native | ✅ Natural |
| **Unix Philosophy** | ❌ | ❌ | ✅ Perfect fit |

**When to Use Each**:
- **gRPC**: High-performance microservices, internal APIs, real-time streaming
- **JSON-RPC**: Web APIs, simple request/response, broad language support
- **JSON Lines**: Bulk processing, log streaming, Unix pipelines, monitoring

**Example Use Cases for Morphir**:
1. **gRPC**: Real-time IDE integration with streaming diagnostics
2. **JSON-RPC**: Web-based Morphir playground API
3. **JSON Lines**: Bulk IR validation in CI/CD pipelines

### Appendix E: Visitor Pattern for IR

**Example Implementation**:
```fsharp
// Visitor interface
type IIRVisitor<'TResult> =
    abstract VisitPackageDefinition: PackageDefinition -> 'TResult
    abstract VisitModuleDefinition: ModuleDefinition -> 'TResult
    abstract VisitTypeDefinition: TypeDefinition -> 'TResult
    abstract VisitValueDefinition: ValueDefinition -> 'TResult

// Traversal strategy
type TraversalStrategy =
    | PreOrder
    | PostOrder
    | InOrder

// IR node base
type IRNode =
    abstract Accept<'TResult> : IIRVisitor<'TResult> -> 'TResult

// Example visitor implementation
type TypeCollectorVisitor() =
    let mutable types = []

    interface IIRVisitor<unit> with
        member _.VisitTypeDefinition(typeDef) =
            types <- typeDef :: types

        member _.VisitPackageDefinition(pkg) =
            pkg.Modules |> List.iter (fun m -> m.Accept(this))

        // ... other methods

    member _.GetCollectedTypes() = types
```

---

**Document Status**: Draft
**Next Review**: 2025-12-30
**Owner**: morphir-dotnet maintainers
**Feedback**: Open GitHub issue with label `prd:architect-skill`
