---
name: Manifest Generator
description: Auto-generate capability manifests from skill/MCP descriptions using Codex-powered semantic analysis and structured extraction.
version: 1.0.0
category: ai-native
tags:
  - codex
  - automation
  - manifest
---

# Manifest Generator

**Auto-generate capability manifests from skill/MCP descriptions using Codex**

## Purpose

Uses OpenAI Codex to analyze existing skills, MCPs, tools, and components to automatically generate their capability manifests. This bootstraps the entire orchestration system by inferring preconditions, effects, domains, and relationships from descriptions and implementations.

## When to Use

- Bootstrapping: Generate manifests for all 59 skills + 50 MCPs at once
- New resources: Auto-generate manifest when creating new skills/MCPs
- Updates: Regenerate manifest when skill description changes
- Validation: Compare generated manifest with existing to detect drift

## Key Capabilities

- **Precondition Inference**: Analyzes skill description to determine what must exist before use
- **Effect Extraction**: Identifies state changes the skill produces
- **Domain Detection**: Categorizes skill into technical domains
- **Relationship Discovery**: Infers which skills this enables/conflicts with/composes with
- **Risk Assessment**: Evaluates cost, latency, and risk level from description

## Inputs

```yaml
inputs:
  skill_path: string # Path to skill directory (e.g., SKILLS/rag-implementer)
  resource_type: string # "skill" | "mcp" | "tool" | "component" | "integration"
  description_file: string # Usually SKILL.md or README.md
  implementation_file: string # Optional: actual code file for validation
  output_path: string # Where to write manifest.yaml (default: same directory)
```

## Process

### Step 1: Read Source Materials

```bash
# Read skill description
DESCRIPTION=$(cat $skill_path/SKILL.md)

# Read implementation if available
if [ -f "$skill_path/index.js" ]; then
  IMPLEMENTATION=$(head -100 $skill_path/index.js)
fi

# Read existing registry entry
REGISTRY_ENTRY=$(jq ".[] | select(.name==\"$skill_name\")" META/skill-registry.json)
```

### Step 2: Generate Manifest with Codex

```bash
codex exec "
Analyze this ${resource_type} and generate a capability manifest.

DESCRIPTION:
${DESCRIPTION}

IMPLEMENTATION (if available):
${IMPLEMENTATION}

REGISTRY ENTRY:
${REGISTRY_ENTRY}

Generate a YAML manifest matching this schema:
$(cat SCHEMAS/capability-manifest.schema.json)

Infer the following:

1. PRECONDITIONS: What files, dependencies, or state must exist?
   Examples:
   - file_exists('package.json')
   - has_dependency('react')
   - env_var_set('OPENAI_API_KEY')
   - not file_exists('.vector-index')

2. EFFECTS: What does this create/modify/delete?
   Examples:
   - creates_vector_index
   - adds_auth_middleware
   - configures_database
   - updates_tests

3. DOMAINS: What technical areas does it touch?
   Examples: rag, auth, api, database, testing, nextjs, react

4. COMPATIBILITY:
   - requires: What must exist first?
   - conflicts_with: What can't coexist?
   - composes_with: What works well together?
   - enables: What does this unlock?

5. RISK ASSESSMENT:
   - cost: free/low/medium/high (API calls, compute)
   - latency: instant/fast/slow (execution time)
   - risk_level: safe/low/medium/high (side effects)

6. SUCCESS SIGNAL: How do we know it worked?
   Examples:
   - 'tests pass'
   - 'file exists: .vector-index'
   - 'HTTP 200 from /api/search'
   - 'can query vector database'

Output ONLY valid YAML. No explanatory text.
"
```

### Step 3: Validate and Write

```bash
# Validate generated YAML against schema
npx ajv validate \
  -s SCHEMAS/capability-manifest.schema.json \
  -d /tmp/generated-manifest.yaml

# Write to output location
cp /tmp/generated-manifest.yaml $output_path
```

## Codex Prompt Template

```
Analyze this ${kind} and extract capability information:

NAME: ${name}
DESCRIPTION:
${description}

${implementation ? "IMPLEMENTATION:\n" + implementation : ""}

Generate a capability manifest with:

1. PRECONDITIONS (what must be true to use this?):
   - File checks: file_exists('path'), not file_exists('path')
   - Dependency checks: has_dependency('package-name')
   - Env checks: env_var_set('VAR_NAME')
   - State checks: describe project state requirements

2. EFFECTS (what changes does it make?):
   - Use imperative verbs: creates_, adds_, configures_, updates_, removes_
   - Be specific: "creates_vector_index", not "does vector stuff"

3. DOMAINS (what technical areas?):
   - Choose from: rag, auth, api, database, testing, nextjs, react, security, performance, etc.

4. COMPATIBILITY:
   - requires: [list of required capabilities]
   - conflicts_with: [capabilities that can't coexist]
   - composes_with: [capabilities that work well together]
   - enables: [capabilities this unlocks]

5. COST/LATENCY/RISK:
   - cost: free (no API calls), low (< $0.10), medium (< $1), high (> $1)
   - latency: instant (< 1s), fast (< 10s), slow (> 10s)
   - risk_level: safe (no side effects), low (idempotent), medium (modifies files), high (irreversible changes)

6. SUCCESS_SIGNAL: What confirms it worked?

Output as YAML matching capability-manifest schema.
```

## Example Output

```yaml
# SKILLS/rag-implementer/manifest.yaml
name: rag-implementer
kind: skill
description: Implement retrieval-augmented generation systems with vector databases and embedding pipelines
preconditions:
  - check: file_exists('package.json')
    description: Node.js project with package.json
    required: true
  - check: not file_exists('.vector-index')
    description: Vector database not already configured
    required: false
  - check: env_var_set('OPENAI_API_KEY') or env_var_set('ANTHROPIC_API_KEY')
    description: LLM API key for embeddings
    required: true
effects:
  - creates_vector_index
  - adds_embedding_pipeline
  - configures_retrieval_api
  - adds_rag_tests
domains:
  - rag
  - ai
  - search
  - embeddings
  - api
cost: medium
latency: slow
risk_level: low
side_effects:
  - modifies_files
  - makes_api_calls
idempotent: false
success_signal: 'Vector index created and queryable with test embeddings'
failure_signals:
  - 'API key invalid'
  - 'Vector database connection failed'
  - 'Embedding generation failed'
compatibility:
  requires:
    - openai-integration OR anthropic-integration
  conflicts_with:
    - existing-vector-database
  composes_with:
    - pinecone-mcp
    - weaviate-mcp
    - embedding-generator-mcp
  enables:
    - semantic-search
    - document-qa
    - knowledge-retrieval
observability:
  logs:
    - 'Embedding X documents'
    - 'Vector index created with Y dimensions'
    - 'Retrieval query: {query} returned {count} results'
  metrics:
    - embedding_count
    - retrieval_latency_ms
    - search_relevance_score
metadata:
  version: '1.0.0'
  created_at: '2025-10-28'
  tags:
    - rag
    - vector-database
    - embeddings
    - semantic-search
  examples:
    - 'Implement RAG for Next.js documentation site'
    - 'Add semantic search to existing API'
    - 'Build document Q&A system'
```

## Bootstrap Script

Run this to generate manifests for ALL resources:

```bash
#!/bin/bash
# scripts/bootstrap-manifests.sh

echo "Generating manifests for all skills..."
for skill_dir in SKILLS/*/; do
  skill_name=$(basename "$skill_dir")
  echo "  Processing $skill_name..."

  # Use manifest-generator skill
  bash scripts/skills/manifest-generator.sh \
    --path "$skill_dir" \
    --type "skill" \
    --description "$skill_dir/SKILL.md" \
    --output "$skill_dir/manifest.yaml"
done

echo "\nGenerating manifests for all MCPs..."
for mcp_dir in MCP-SERVERS/*/; do
  mcp_name=$(basename "$mcp_dir")
  echo "  Processing $mcp_name..."

  bash scripts/skills/manifest-generator.sh \
    --path "$mcp_dir" \
    --type "mcp" \
    --description "$mcp_dir/README.md" \
    --implementation "$mcp_dir/index.js" \
    --output "$mcp_dir/manifest.yaml"
done

echo "\nDone! Generated $(find SKILLS MCP-SERVERS -name 'manifest.yaml' | wc -l) manifests"
```

## Benefits

1. **Speed**: Generate 109 manifests in minutes instead of weeks
2. **Consistency**: Uniform format and completeness
3. **Discovery**: Codex finds relationships humans miss
4. **Validation**: Compare to detect description/implementation drift
5. **Evolution**: Re-run to update as skills change

## Integration

### With capability-graph-builder

Manifests become nodes in the capability graph. Relationships inferred from compatibility fields.

### With orchestration-planner

Planner queries manifests to find capabilities matching goal requirements.

### With skill-validator

Validator compares generated manifest with actual implementation to find discrepancies.

## Success Metrics

- ✅ 100% of skills/MCPs have manifests
- ✅ All manifests validate against schema
- ✅ Preconditions cover 90%+ of actual requirements
- ✅ Effects accurately describe state changes
- ✅ Relationship inferences 80%+ accurate

## Related Skills

- capability-graph-builder: Consumes manifests to build graph
- skill-validator: Validates manifests match implementations
- orchestration-planner: Uses manifests for planning
