---
name: reasoning-analogical
description: Transfer knowledge from source domains to novel target situations through structural mapping. Use when facing new markets, products, or situations where past experience provides relevant patterns. Produces adapted solutions with explicit mappings and context adjustments.
---

# Analogical Reasoning

Transfer structured knowledge across domains. The logic of pattern recognition and adaptation.

## Type Signature

```
Analogical : Source → StructuralMap → Target → Adaptation

Where:
  Source        : PriorExperience × Relevance → SourceDomain
  StructuralMap : SourceDomain → (Objects × Relations × Constraints)
  Target        : StructuralMap × NewContext → MappedStructure  
  Adaptation    : MappedStructure × ContextDifferences → AdaptedSolution
```

## When to Use

**Use analogical when:**
- Entering new market with experience in similar markets
- Building new product with experience in similar products
- Facing novel situation with structural similarity to past cases
- Need to transfer playbooks across contexts
- "This is like..." patterns in thinking

**Don't use when:**
- Cause-effect chain is known → Use Causal
- Need to explain observation → Use Abductive
- Competing positions to resolve → Use Dialectical

## Four-Stage Process

### Stage 1: Source Retrieval

**Purpose:** Identify relevant prior experience with documented outcomes.

**Source Selection Criteria:**

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Structural similarity** | Same type of problem/situation? | 0.35 |
| **Outcome documented** | Do we know what happened? | 0.25 |
| **Recency** | How recent is the experience? | 0.15 |
| **Success level** | Did the approach work? | 0.15 |
| **Context overlap** | Similar constraints/resources? | 0.10 |

**Source Retrieval Process:**
```yaml
retrieval:
  query: "Entering B2B marketplace vertical"
  
  candidates:
    - source: "Shopify DTC launch (2024)"
      similarity: 0.75
      outcome: "Validated in 6 months, $200K ARR"
      success: high
      
    - source: "Fashion brand pilot (2023)"
      similarity: 0.60
      outcome: "Slow start, pivoted twice"
      success: medium
      
    - source: "Enterprise SDK launch (2024)"
      similarity: 0.50
      outcome: "$400K first deal, strong pipeline"
      success: high
      
  selected: "Shopify DTC launch"
  reason: "Highest structural similarity (platform integration, 
           API-first, self-serve onboarding)"
```

**Output:**
```yaml
source:
  case: "Shopify DTC launch"
  domain: "E-commerce platform integration"
  timeframe: "Q1-Q2 2024"
  outcome: 
    result: "success"
    metrics: "$200K ARR, 50 merchants, 6-month validation"
  key_factors:
    - "Strong app store presence"
    - "Self-serve onboarding"
    - "Integration-first positioning"
  documented_in: "threads/operations/shopify-dtc-launch/"
```

### Stage 2: Structural Mapping

**Purpose:** Extract transferable structure from source domain.

**Mapping Components:**

| Component | Source Example | Abstracted |
|-----------|----------------|------------|
| **Objects** | Shopify merchants | Platform users |
| **Relations** | Merchant → App → Customer | User → Integration → End-user |
| **Constraints** | App store rules | Platform policies |
| **Mechanisms** | App store discovery → trial → purchase | Discovery → trial → convert |
| **Success factors** | Reviews, featured placement | Social proof, visibility |

**Structural Map:**
```yaml
structure:
  objects:
    - User: "Entity adopting our solution"
    - Platform: "Ecosystem we integrate with"
    - EndUser: "Final beneficiary of solution"
    - Solution: "Our product/integration"
    
  relations:
    - Platform ⊃ Marketplace: "Platform has discovery mechanism"
    - User → Solution: "User adopts solution"
    - Solution → EndUser: "Solution serves end users"
    - EndUser feedback → User: "Value demonstration"
    
  mechanisms:
    acquisition:
      - "Platform marketplace discovery"
      - "Peer recommendations"
      - "Content marketing to users"
    activation:
      - "Self-serve trial"
      - "Quick time-to-value"
      - "Integration simplicity"
    retention:
      - "Embedded in workflow"
      - "Switching cost creation"
      - "Continuous value delivery"
      
  constraints:
    - "Platform approval required"
    - "Platform policies must be followed"
    - "Revenue share with platform"
    
  success_factors:
    - "Marketplace ranking/visibility"
    - "User reviews/ratings"
    - "Platform relationship quality"
```

### Stage 3: Target Application

**Purpose:** Map structure to new context, identifying what transfers and what doesn't.

**Target Context:**
```yaml
target:
  domain: "B2B marketplace integration"
  platform: "Faire wholesale marketplace"
  user: "Wholesale brands"
  end_user: "Retailers"
  goal: "Return reduction for wholesale fashion"
```

**Mapping Execution:**
```yaml
mapping:
  objects:
    Platform: "Shopify" → "Faire"
    User: "DTC merchant" → "Wholesale brand"
    EndUser: "Consumer" → "Retailer"
    Solution: "Fit recommendation app" → "Wholesale sizing tool"
    
  relations:
    preserved:
      - "Platform marketplace discovery" (Faire has app marketplace)
      - "User adopts solution" (brands install integrations)
      - "Value to end user" (retailers get better sizing)
      
    modified:
      - "Self-serve trial" → "Account executive assisted"
        reason: "B2B decision process differs"
      - "Individual purchase" → "Contract-based"
        reason: "Wholesale pricing models"
        
    broken:
      - "App store reviews drive adoption"
        reason: "Faire marketplace less review-driven"
        replacement: "Case studies and referrals"
        
  mechanisms:
    acquisition:
      transfers: "Platform marketplace presence"
      adapts: "Content marketing → Trade show presence"
      new: "Wholesale buyer referral program"
      
    activation:
      transfers: "Integration simplicity"
      adapts: "Self-serve → Assisted onboarding"
      new: "Pilot with single retail partner"
      
    retention:
      transfers: "Embedded in workflow"
      transfers: "Value demonstration"
      adapts: "Individual metrics → Fleet metrics"
```

### Stage 4: Adaptation

**Purpose:** Produce concrete plan adjusted for context differences.

**Context Differences Analysis:**
```yaml
differences:
  critical:
    - name: "Decision process"
      source: "Individual merchant, fast"
      target: "Buying committee, slow"
      adaptation: "Add sales support, longer cycle expectations"
      
    - name: "Value demonstration"
      source: "Per-order metrics visible"
      target: "Aggregate across retailers"
      adaptation: "Build analytics dashboard for brands"
      
  moderate:
    - name: "Pricing model"
      source: "Per-store subscription"
      target: "Volume-based or percentage"
      adaptation: "Explore usage-based pricing"
      
  minor:
    - name: "Technical integration"
      source: "Shopify API"
      target: "Faire API"
      adaptation: "Standard integration work"
```

**Adapted Solution:**
```yaml
adaptation:
  strategy: "Platform-assisted B2B wholesale launch"
  
  what_transfers:
    - "Integration-first positioning"
    - "Platform relationship investment"
    - "Quick time-to-value focus"
    - "Embedded workflow stickiness"
    
  what_adapts:
    - "Self-serve → Assisted onboarding with demo"
    - "App store discovery → Trade shows + referrals"
    - "Individual reviews → Case studies"
    - "Per-order metrics → Brand-level analytics"
    
  what's_new:
    - "Sales motion for wholesale buyers"
    - "Multi-retailer aggregation features"
    - "B2B pricing model (volume-based)"
    
  execution_plan:
    phase_1: "Platform partnership + 3 pilot brands"
    phase_2: "Case study development + trade show presence"
    phase_3: "Scale via referrals + platform promotion"
    
  expected_timeline: "9-12 months (vs 6 months for DTC)"
  reason: "B2B sales cycle longer, relationship-building required"
  
  confidence: 0.70
  uncertainty:
    - "Faire marketplace dynamics unknown"
    - "Wholesale brand decision process may vary"
    - "Volume-based pricing acceptance unclear"
```

## Quality Gates

| Gate | Requirement | Failure Action |
|------|-------------|----------------|
| Source quality | Documented outcome with metrics | Find better source |
| Structural clarity | ≥3 objects, ≥3 relations explicit | Complete mapping |
| Mapping coverage | All source elements mapped or marked broken | Complete mapping |
| Adaptation specificity | Concrete actions, not abstract | Add specificity |
| Confidence threshold | ≥0.6 confidence | Flag high uncertainty |

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| **Surface similarity** | Mapped by superficial features, not structure | Focus on relations, not objects |
| **Over-transfer** | Assume everything applies | Explicitly check each element |
| **Under-adaptation** | Copy-paste without adjustment | Force context difference analysis |
| **Single source** | Only one analogy considered | Retrieve multiple candidates |

## Output Contract

```yaml
analogical_output:
  source:
    case: string
    domain: string
    outcome: {result: string, metrics: string}
    thread_ref: optional<string>
    
  mapping:
    objects: {source_name: target_name}
    relations:
      preserved: [string]
      modified: [{from: string, to: string, reason: string}]
      broken: [{relation: string, reason: string, replacement: string}]
      
  adaptation:
    transfers: [string]      # What applies directly
    adapts: [string]         # What needs modification
    new: [string]            # What's genuinely new
    
  plan:
    phases: [{name: string, actions: [string]}]
    timeline: string
    milestones: [string]
    
  confidence: float  # 0.0-1.0
  uncertainty: [string]
  
  next:
    suggested_mode: ReasoningMode  # Usually causal
    canvas_refs: [string]          # Assumptions being tested
    
  trace:
    sources_considered: int
    mapping_coverage: float  # % of source elements mapped
    duration_ms: int
```

## Example Execution

**Context:** "Expand to home goods vertical (currently in fashion)"

**Stage 1 - Source Retrieval:**
```
Selected: Fashion DTC success (highest similarity)
Alternatives considered: 
  - Beauty vertical (rejected: different return dynamics)
  - B2B wholesale (rejected: different buyer)
```

**Stage 2 - Structural Mapping:**
```
Objects: Fashion brand → Home goods brand
Relations: 
  - Fit concern → Dimension/space concern
  - Style matching → Aesthetic matching
  - Return reason: fit → Return reason: scale/compatibility
Mechanisms:
  - Visual AI → Transfer (image analysis)
  - Size recommendation → Adapt (dimension recommendation)
  - Color matching → Transfer (palette matching)
```

**Stage 3 - Target Application:**
```
Preserved: Visual AI core, recommendation engine, integration model
Modified: Fit algorithm → Dimension/space algorithm
Broken: Body measurement input → Room/space measurement input
```

**Stage 4 - Adaptation:**
```
Plan:
  Phase 1: Partner with 2 home goods DTC brands (furniture focus)
  Phase 2: Adapt algorithm for dimension-based recommendations
  Phase 3: Develop room visualization feature (new capability)
  
Timeline: 4-6 months (faster than fashion - simpler measurements)
Confidence: 0.75
Key uncertainty: Room visualization technical complexity
```
