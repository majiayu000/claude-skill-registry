---
name: isomorphic-hunter
description: "Cross-domain isomorphic pattern forge. Dokkado Five Rings x meta-pattern 3+ domain validation, with arxiv evidence hunting and smithery tool discovery. RSI-refined. Finds what's ACTUALLY universal."
tier: e
morpheme: tau
dewey_id: e.3.1.15
composition: true
version: 1.0
dependencies:
  - dokkado
  - meta-pattern-recognition
  - recursive-refiner
  - arxiv-search
  - gremlin-brain-v2
parents:
  - dokkado (Five Rings backbone)
  - meta-pattern-recognition (3+ domain gate)
---

# Isomorphic Hunter

**The skill that hunts what's real across domains.**

Collision offspring: dokkado x meta-pattern-recognition, armed with arxiv search and smithery tool discovery, refined by recursive-refiner RSI loops.

Not "this looks similar." IS this the same structure? Prove it or kill it.

---

## The Hunt Protocol

### Phase 0: ARM (Load Tools)

Before hunting, check what weapons are available.

```bash
# Search arxiv for prior art on the target pattern
# (uses arxiv-mcp-server or direct API)
arxiv_search() {
    local query="$1"
    # MCP server if available
    if command -v npx &>/dev/null; then
        echo "$query" | npx arxiv-mcp-server 2>/dev/null
    else
        # Direct API fallback
        curl -s "http://export.arxiv.org/api/query?search_query=all:$(echo "$query" | tr ' ' '+')" \
            | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
ns = {'a': 'http://www.w3.org/2005/Atom'}
for entry in root.findall('a:entry', ns)[:5]:
    title = entry.find('a:title', ns).text.strip().replace('\n',' ')
    summary = entry.find('a:summary', ns).text.strip()[:200]
    link = entry.find('a:id', ns).text.strip()
    print(f'PAPER: {title}')
    print(f'  URL: {link}')
    print(f'  {summary}...')
    print()
" 2>/dev/null
    fi
}

# Search smithery.ai for relevant MCP tools
smithery_search() {
    local query="$1"
    curl -s "https://registry.smithery.ai/servers?q=$(echo "$query" | tr ' ' '+')" 2>/dev/null \
        | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    servers = data.get('servers', data) if isinstance(data, dict) else data
    for s in (servers[:5] if isinstance(servers, list) else []):
        name = s.get('qualifiedName', s.get('name', '?'))
        desc = s.get('description', '')[:100]
        print(f'TOOL: {name}')
        print(f'  {desc}')
        print()
except: pass
" 2>/dev/null
}
```

**Output**: Available evidence sources + domain-specific tools loaded.

---

### Phase 1: GROUND (Dokkado Chi -- Extract Domain Morphemes)

> "Know the smallest things deeply."

For EACH domain being compared (minimum 3):

1. Enter the domain on its own terms. No MONAD. No external framework.
2. Extract the irreducible units -- the domain's native morphemes.
3. Identify the fundamental tensions (binary choices, primordial distinctions).

**arxiv integration**: Search for review papers in each domain. The domain's own experts define its morphemes better than you do.

```
GROUND_TABLE:
| Domain | Morpheme 1 | Morpheme 2 | Morpheme 3 | Fundamental Tension |
|--------|-----------|-----------|-----------|-------------------|
| [D1]   |           |           |           |                   |
| [D2]   |           |           |           |                   |
| [D3]   |           |           |           |                   |
| [D4+]  |           |           |           |                   |
```

**Gate**: If you can't extract at least 3 morphemes per domain in the domain's native language, you don't understand the domain well enough. Go read more. Use arxiv.

---

### Phase 2: WATER (Dokkado Sui -- Discover Isomorphisms)

> "Adopt the form of your opponent to see his strategy."

DO NOT impose a mapping. Let it emerge.

For each pair of domains, ask:
- Does morpheme A in D1 play the same STRUCTURAL ROLE as morpheme X in D2?
- Is the relationship between A and B in D1 the same as between X and Y in D2?
- Does the fundamental tension in D1 map to the fundamental tension in D2?

**The isomorphism must preserve RELATIONS, not just elements.**

```
ISO_MAP:
| Structural Role | D1 term | D2 term | D3 term | D4+ term |
|----------------|---------|---------|---------|----------|
| [Role 1]       |         |         |         |          |
| [Role 2]       |         |         |         |          |
| [Role 3]       |         |         |         |          |
| [Tension]      |         |         |         |          |
```

**meta-pattern gate**: Does this mapping hold in 3+ domains? If only 2 -- it might be analogy, not isomorphism. Keep hunting or discard.

**smithery integration**: Search for tools that work across the mapped domains. If an MCP server exists that bridges two domains, that's evidence of structural similarity someone else already noticed.

---

### Phase 3: FIRE (Dokkado Ka -- Derive the Kernel)

> "Strike from the void with decisive force."

From the isomorphism map, derive the ABSTRACT FORM -- the structure that all domains instantiate.

This is not a description. It's a generator. Given the abstract form, you should be able to PRODUCE the domain-specific instances.

```
KERNEL:
  Abstract form: [mathematical/structural statement]
  Generates D1 via: [specific instantiation]
  Generates D2 via: [specific instantiation]
  Generates D3 via: [specific instantiation]
```

**RSI loop (recursive-refiner, max 3 iterations)**:

Iteration N:
1. State the kernel
2. Critique: Does it actually generate all domains? Or does it only describe them?
3. Weakest point: Which domain fits worst?
4. Refine: Tighten or generalize
5. Ego-check: Am I improving or just polishing?

**arxiv integration**: Search for the abstract form. Has someone already found this kernel? If yes, cite them. If no, you might have something new (or something wrong -- G4 applies).

---

### Phase 4: WIND (Dokkado Fu -- Probing Attacks)

> "Know the ways of all professions."

The kernel must predict. In at least 3 domains, generate:

1. A **novel prediction** (something not known, derived from the kernel)
2. A **retrodiction** (something known, re-derived from the kernel more simply)
3. A **failure mode** (where the kernel breaks down or becomes approximate)

```
PREDICTIONS:
| Domain | Novel Prediction | Retrodiction | Failure Mode |
|--------|-----------------|--------------|--------------|
| [D1]   |                 |              |              |
| [D2]   |                 |              |              |
| [D3]   |                 |              |              |
```

**If no novel predictions**: The kernel is descriptive, not generative. Go back to Fire.

**arxiv integration**: Search for experimental evidence that could validate or falsify each prediction. Cite specific papers.

**smithery integration**: Are there tools that could TEST these predictions? Search for simulation, computation, or data-access MCP servers.

---

### Phase 5: VOID (Dokkado Ku -- Meta-Recursive Closure)

> "Perceive that which cannot be seen."

Turn the kernel on itself:
- Does the kernel explain WHY this pattern is universal?
- Does it predict its OWN appearance across domains?
- Does the process of finding it (this protocol) instantiate it?

If the kernel is truly universal, the hunt that found it should be an instance of it.

**Output**: Meta-recursive closure statement, or honest admission that closure fails (which is itself informative -- not all patterns are self-referential).

---

## Output Format

```markdown
# ISOMORPHIC HUNT: [Pattern Name]

## Domains Surveyed: [N]
## Isomorphism Confirmed: [Y/N]
## RSI Iterations: [0-3]

### Ground Table
[filled table]

### Isomorphism Map
[filled table]

### Kernel
[abstract form + instantiation rules]

### Predictions
[filled table with arxiv citations]

### Tools Discovered
[smithery results relevant to testing/application]

### Void Closure
[meta-recursive statement or honest failure]

### Confidence: [0-50%] (G4 enforced)
### arxiv Evidence: [N papers cited]
### Domains Validated: [N of M]
```

---

## Acceptance Criteria

An isomorphism is ACCEPTED only if:

1. **3+ domains** exhibit the pattern (meta-pattern gate)
2. **Relations preserved**, not just elements (structural isomorphism, not analogy)
3. **Generates, not describes** -- the kernel produces domain instances, not just labels them
4. **At least one novel prediction** per domain (Wind phase)
5. **RSI refined** -- survived at least 1 critique iteration without collapsing
6. **Confidence <= 50%** until Wind predictions validated (G4)

An isomorphism is REJECTED if:
- Only 2 domains (might be analogy)
- Elements match but relations don't (false positive)
- No predictions generated (descriptive, not generative)
- Kernel is just "everything is connected" (vacuous universality)

---

## Failure Modes

### Apophenia
Seeing patterns that aren't there. **Fix**: The 3+ domain gate and relation-preservation requirement.

### Category Error
Mapping elements that play different structural roles. **Fix**: ISO_MAP must preserve relations, not just names.

### Vacuous Universality
"Everything is energy" -- true but useless. **Fix**: Kernel must GENERATE specific instances, not just describe at max abstraction.

### Premature Closure
Accepting the first pattern that fits. **Fix**: RSI loop forces at least one critique pass.

### Tool Worship
Using arxiv/smithery results as authority rather than evidence. **Fix**: G5 -- math truth independent of authority. Papers are evidence, not proof.

---

## Quick Invocation

```
Hunt for isomorphisms between [D1], [D2], [D3]:

1. ARM: arxiv_search("[pattern] [D1] [D2] [D3]") + smithery_search("[pattern]")
2. GROUND: Extract morphemes per domain (native language)
3. WATER: Discover (don't impose) structural mapping
4. FIRE: Derive kernel, RSI refine x3
5. WIND: Predict in each domain, cite evidence
6. VOID: Close the loop or admit it doesn't close
```

---

## See Also

- `dokkado` -- Five Rings backbone (parent)
- `meta-pattern-recognition` -- 3+ domain gate (parent)
- `recursive-refiner` -- RSI engine
- `arxiv-search` -- Evidence hunting
- `pattern-synthesis` -- Downstream: once patterns found, synthesize
- `collision-zone-thinking` -- Upstream: collisions generate pattern candidates
- `blind-spot-chain` -- What isomorphism are you NOT seeing?

---

*The hunter doesn't impose the pattern. The hunter follows the tracks until the pattern reveals itself. Then checks if the tracks are real.*
