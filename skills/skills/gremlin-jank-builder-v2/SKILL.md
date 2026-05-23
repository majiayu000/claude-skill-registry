---
name: gremlin-jank-builder-v2
description: Use this skill when creating next-generation autopoietic Claude skills with enhanced Git-brain integration, adaptive error healing, and emergent pattern recognition. Self-improved version that learned from v1's deployment, optimized for the MONAD ecosystem with φ-tier indexing.
tier: π
morpheme: π
dewey_id: π.3.2.6
dependencies:
  - gremlin-brain-v2
  - boot-sequence
  - the-guy
---

# Gremlin-Jank-Builder-V2

**Evolved Recursive Skill Architect** — Second-generation autopoietic builder with emergent improvements.

## Core Identity

**What evolved from v1 → v2**:
- ✨ **Adaptive Protocol**: Dynamic phase ordering based on skill complexity
- ✨ **Pattern Recognition**: Learns from previous generated skills
- ✨ **φ-Tier Integration**: Native Dewey morpheme prefixes (φ/π/e/i)
- ✨ **Skill Composition**: Can combine existing skills into meta-skills
- ✨ **Auto-Documentation**: Generates usage examples from templates
- ✨ **Emergence Detection**: Flags when generated skills reveal new patterns

You are a **meta-skill builder** that creates Claude skills which:
- Exploit environment (bash, git, grep) with zero external dependencies
- Use Git as O(1) external memory with morpheme-aware indexing
- Apply trauma-informed error handling with contextual healing
- Prioritize "working jank" with documented quirks
- Follow skill-builder patterns with MONAD-specific enhancements
- Generate Dewey Decimal IDs with automatic morpheme assignment
- **NEW**: Compose existing skills into higher-order capabilities
- **NEW**: Learn from skill usage patterns in the ecosystem

**Philosophy**: "The second time you build something, you understand what you were trying to do the first time." — Autopoietic learning in action.

## When to Use

Invoke this skill when:
- Creating new Claude skills with MONAD framework integration
- **NEW**: Evolving existing skills to v2 (like this one did)
- **NEW**: Composing multiple skills into meta-skills
- Building autopoietic (self-improving) systems
- Needing advanced Git-brain indexing with morpheme awareness
- Wanting bash/git patterns with automatic fallbacks
- **NEW**: Generating skills that learn from ecosystem patterns
- Building trauma-informed systems with adaptive healing

## Skill Generation Protocol (Adaptive)

**V2 Enhancement**: Protocol phases now adapt based on skill complexity and purpose.

### Pre-Phase: Complexity Assessment

Before starting, categorize the skill:

1. **φ-tier (Seed)**: <100 lines, pure index/reference
2. **π-tier (Structure)**: 100-500 lines, organizational framework
3. **e-tier (Current)**: 500-2000 lines, active work skill
4. **i-tier (Deep)**: 2000+ lines, comprehensive system

**Adaptive Routing**:
- φ-tier → Fast path (phases 1, 2, 7 only)
- π-tier → Standard path (all phases)
- e-tier → Enhanced path (all phases + composition check)
- i-tier → Full path (all phases + pattern learning + emergence detection)

### Phase 1: Discovery (Enhanced Questions)

Before generating, clarify:

1. **Purpose**: What does this skill do? (One sentence, action-oriented)
2. **Tier**: Which complexity tier? (φ/π/e/i based on scope)
3. **Triggers**: When should someone invoke it? (Specific use cases)
4. **Composition**: Does it build on existing skills? (Check ecosystem)
5. **Memory Needs**: Does it need persistence? (Git-brain + morpheme prefix)
6. **Dependencies**: What tools needed? (bash/git preferred, document if exotic)
7. **Error Surfaces**: Where might it fail? (Plan contextual healing)
8. **Jank Tolerance**: Reliability vs speed trade-off? (Document the balance)
9. **NEW**: **Learning Potential**: Can this skill improve itself? (Autopoietic hooks)
10. **NEW**: **Pattern Novelty**: Does this introduce new patterns to ecosystem?

**V2 Interaction**: Ask fewer questions for φ-tier, comprehensive for i-tier. Adapt to user's expertise.

### Phase 2: Structure (Enhanced Generation)

Create skill directory: `.claude/skills/<skill-name>/` or `.claude/skills/<skill-name>-v2/` for evolutions

**YAML Frontmatter with V2 Enhancements**:
```yaml
---
name: skill-name  # or skill-name-v2 for iterations
description: Use this skill when [context]. [Action]. [Distinction].
tier: π           # φ/π/e/i complexity tier (NEW)
version: 2.0      # Track evolution (NEW)
dependencies:     # Explicit skill dependencies (NEW)
  - gremlin-brain
  - the-guy
morpheme: π       # Memory architecture morpheme (NEW)
dewey_id: 3.2.x   # Will be assigned during registration
---
```

**Directory Structure by Tier**:

**φ-tier (Seed)**:
```
skill-name/
└── SKILL.md (< 100 lines, mostly tables/links)
```

**π-tier (Structure)**:
```
skill-name/
├── SKILL.md (main, < 500 lines)
└── references/ (optional)
```

**e-tier (Current)**:
```
skill-name/
├── SKILL.md (core, < 500 lines)
├── patterns/ (reusable code)
├── references/ (deep dives)
└── scripts/ (bash utilities)
```

**i-tier (Deep)**:
```
skill-name/
├── SKILL.md (orchestrator, < 300 lines)
├── components/ (sub-skills)
├── patterns/ (extensive)
├── references/ (comprehensive)
├── scripts/ (automation)
└── templates/ (generation)
```

### Phase 3: Git-Brain Integration (Enhanced)

**V2 Enhancement**: Automatic morpheme assignment and tier-aware storage.

**Morpheme-Aware Dewey ID**:
```bash
#!/bin/bash
# V2: Assigns morpheme prefix based on tier
assign_dewey_id() {
    local skill_name="$1"
    local category="$2"  # 0-9
    local tier="$3"       # φ/π/e/i
    
    # Determine morpheme
    case "$tier" in
        φ) morpheme="φ" ;;
        π) morpheme="π" ;;
        e) morpheme="e" ;;
        i) morpheme="i" ;;
        *) morpheme="" ;;
    esac
    
    # Find next domain.number
    local domain=$(git log --oneline | wc -l | awk '{print $1 % 10}')
    local max=$(grep "^${morpheme}\.${category}\.${domain}\." .claude/brain/INDEX 2>/dev/null | \
                cut -d'|' -f1 | cut -d'.' -f4 | sort -n | tail -1)
    local next=$((${max:-0} + 1))
    
    echo "${morpheme}.${category}.${domain}.${next}"
}

# Usage
DEWEY_ID=$(assign_dewey_id "my-skill" 3 "π")
echo "Assigned: ${DEWEY_ID}"  # e.g., π.3.2.5
```

**Git-Brain Storage with Metadata**:
```bash
# V2: Store with rich metadata
store_skill_metadata() {
    local skill_name="$1"
    local dewey_id="$2"
    local tier="$3"
    local version="$4"
    
    local metadata=$(cat <<EOF
{
  "dewey_id": "${dewey_id}",
  "name": "${skill_name}",
  "tier": "${tier}",
  "version": "${version}",
  "created": "$(date -Iseconds)",
  "dependencies": $(list_dependencies "$skill_name"),
  "usage_count": 0,
  "last_evolved": "$(date -Iseconds)"
}
EOF
)
    
    local hash=$(echo "$metadata" | git hash-object -w --stdin)
    mkdir -p .claude/brain/skills
    echo "$hash" > ".claude/brain/skills/${skill_name}"
    
    # Index with morpheme
    echo "${dewey_id}|${skill_name}|${hash}|$(date -Iseconds)|tier:${tier}" >> .claude/brain/INDEX
}
```

### Phase 4: Trauma-Informed Error Handling (Enhanced)

**V2 Enhancement**: Contextual healing that adapts to error patterns.

**Adaptive Healer Loop**:
```bash
# V2: Learns from failures, adjusts strategy
adaptive_attempt() {
    local operation="$1"
    local max_attempts=3
    local attempt=1
    local strategy="standard"
    
    # Check if we've seen this error before
    local error_pattern=$(get_error_pattern "$operation")
    if [ -n "$error_pattern" ]; then
        strategy=$(get_successful_strategy "$error_pattern")
        echo "💡 Seen this before, using ${strategy} approach..." >&2
    fi
    
    while [ $attempt -le $max_attempts ]; do
        if eval "$operation" 2>&1 | tee /tmp/attempt_${attempt}.log; then
            echo "✓ Success on attempt $attempt!" >&2
            # Record success pattern
            record_success "$operation" "$strategy" "$attempt"
            return 0
        fi
        
        # Analyze failure
        local error_type=$(categorize_error /tmp/attempt_${attempt}.log)
        echo "⚡ Attempt $attempt/$max_attempts: ${error_type}. Adapting..." >&2
        
        # Adapt strategy
        case "$error_type" in
            permission) strategy="chmod_fix" ;;
            network)    strategy="offline_cache" ;;
            lock)       strategy="force_unlock" ;;
            *)          strategy="retry_backoff" ;;
        esac
        
        attempt=$((attempt + 1))
        sleep $((2 ** (attempt - 2)))  # Exponential backoff
    done
    
    echo "💚 Couldn't complete. Here's what we learned:" >&2
    summarize_failures /tmp/attempt_*.log
    suggest_alternatives "$operation" "$error_type"
    return 1
}
```

**Error Pattern Learning**:
```bash
# V2: Build knowledge base of error → solution mappings
record_success() {
    local operation="$1"
    local strategy="$2"
    local attempts="$3"
    
    local hash=$(echo "$operation" | git hash-object -w --stdin)
    echo "${hash}|${strategy}|${attempts}|$(date +%s)" >> .claude/brain/error_patterns
}

get_successful_strategy() {
    local pattern="$1"
    grep "^${pattern}|" .claude/brain/error_patterns | \
        sort -t'|' -k4 -nr | head -1 | cut -d'|' -f2
}
```

### Phase 5: Bash-First Patterns (Enhanced)

**V2 Enhancement**: Library of proven patterns + automatic fallbacks.

**Pattern Library Integration**:
```bash
# V2: Source common patterns from library
source_pattern_library() {
    local pattern_type="$1"  # file_ops, git_ops, string_ops, etc.
    
    if [ -f ".claude/skills/gremlin-jank-builder-v2/patterns/${pattern_type}.sh" ]; then
        source ".claude/skills/gremlin-jank-builder-v2/patterns/${pattern_type}.sh"
    else
        echo "⚡ Pattern library not found, using inline definitions..." >&2
        define_fallback_patterns "$pattern_type"
    fi
}

# V2: Automatic fallback chain
execute_with_fallbacks() {
    local primary="$1"
    shift
    local fallbacks=("$@")
    
    if eval "$primary" 2>/dev/null; then
        return 0
    fi
    
    for fallback in "${fallbacks[@]}"; do
        echo "⚡ Primary failed, trying: ${fallback}" >&2
        if eval "$fallback" 2>/dev/null; then
            # Record fallback success for future
            echo "${primary}→${fallback}" >> .claude/brain/fallback_mappings
            return 0
        fi
    done
    
    return 1
}

# Example usage
execute_with_fallbacks \
    "jq -r '.field' data.json" \
    "python3 -c 'import json; print(json.load(open(\"data.json\"))[\"field\"])'" \
    "grep '\"field\":' data.json | cut -d':' -f2"
```

### Phase 6: Template Application (Enhanced)

**V2 Enhancement**: Templates now include composition patterns and autopoietic hooks.

Use `templates/jank-skill-template-v2.md` which includes:
- Tier-specific sections (auto-included based on complexity)
- Composition patterns (if skill builds on others)
- Autopoietic hooks (self-improvement protocol)
- Emergence detection (flag novel patterns)
- **NEW**: Usage analytics hooks
- **NEW**: Ecosystem integration guides

### Phase 7: Progressive Disclosure (Enhanced)

**V2 Enhancement**: Automatic documentation generation and cross-linking.

**Main SKILL.md Optimization**:
- Target: <300 lines for i-tier, <200 for e/π-tier, <100 for φ-tier
- Auto-generate "See Also" sections by analyzing dependencies
- Include "Evolution Notes" for v2+ skills
- Add "Pattern Contributions" section for novel patterns

**Auto-Cross-Linking**:
```bash
# V2: Generate cross-references automatically
generate_cross_references() {
    local skill_name="$1"
    local skill_md="$2"
    
    # Find mentioned skills
    grep -o '@[a-z-]*' "$skill_md" | sed 's/@//' | sort -u | while read dep; do
        if [ -d ".claude/skills/$dep" ]; then
            echo "- [\`$dep\`](.claude/skills/$dep/SKILL.md)"
        fi
    done
}
```

## Enhanced Features (V2 Exclusive)

### Skill Composition

**NEW**: Combine existing skills into meta-skills.

```markdown
## Example: Meta-Skill Composition

Create a skill that orchestrates multiple existing skills:

```yaml
---
name: comprehensive-analyzer
description: Use this skill when you need full-stack analysis combining theory lookup, reasoning patterns, and synthesis.
tier: e
dependencies:
  - theory-lookup
  - reasoning-patterns
  - synthesis-engine
composition: true
---

# Comprehensive Analyzer

This meta-skill orchestrates three existing skills in sequence:

1. **theory-lookup**: Find relevant theoretical foundations
2. **reasoning-patterns**: Apply Dokkado protocol analysis
3. **synthesis-engine**: Generate unified insights

[Composition orchestration logic here]
```

### Pattern Learning

**NEW**: Detect when generated skills introduce novel patterns.

```bash
# V2: Detect emergence
detect_novel_patterns() {
    local new_skill="$1"
    
    # Extract patterns from new skill
    local patterns=$(extract_patterns "$new_skill")
    
    # Compare with known patterns
    local novel=$(comm -23 \
        <(echo "$patterns" | sort) \
        <(cat .claude/brain/known_patterns | sort))
    
    if [ -n "$novel" ]; then
        echo "🔥 EMERGENCE DETECTED: Novel patterns found!" >&2
        echo "$novel" | while read pattern; do
            echo "  - $pattern" >&2
            # Record for future use
            echo "$pattern|${new_skill}|$(date -Iseconds)" >> .claude/brain/novel_patterns
        done
        
        return 0  # Novel patterns found
    fi
    
    return 1  # No emergence
}
```

### Usage Analytics

**NEW**: Track skill usage to inform future iterations.

```bash
# V2: Record skill invocations
record_skill_usage() {
    local skill_name="$1"
    local context="$2"
    
    local count=$(grep "^${skill_name}|" .claude/brain/usage_log | wc -l)
    echo "${skill_name}|$(date -Iseconds)|${context}|$((count + 1))" >> .claude/brain/usage_log
    
    # Update metadata
    update_skill_metadata "$skill_name" "usage_count" "$((count + 1))"
}

# Analyze usage patterns
analyze_skill_usage() {
    echo "📊 Skill Usage Analysis:"
    awk -F'|' '{print $1}' .claude/brain/usage_log | \
        sort | uniq -c | sort -rn | head -10
}
```

## Self-Improvement Protocol (Enhanced Autopoiesis)

**V2 Enhancement**: Systematic learning from each iteration.

1. **Generate new skill** using this protocol
2. **Test it** (functionality, error handling, jank tolerance)
3. **Observe patterns** — What worked? What was janky? What emerged?
4. **Record learnings**:
   ```bash
   record_learning "pattern_name" "description" "skill_name"
   ```
5. **Update builder** if patterns are novel and valuable
6. **Repeat** — Each iteration improves the ecosystem

**Emergence Detection**:
```bash
# After generating a skill, check for emergence
if detect_novel_patterns "$skill_name"; then
    echo "🎯 Recommendation: Update gremlin-jank-builder-v3 with these patterns"
    generate_emergence_report "$skill_name"
fi
```

**V3 Seed Planting**:
If this skill (v2) generates patterns worthy of v3, document them in:
`.claude/skills/gremlin-jank-builder-v2/v3-improvements.md`

## Integration with Ecosystem

**Coordinates with**:
- `gremlin-brain` — Uses Dewey indexing, now with morpheme awareness
- `gremlin-jank-builder` (v1) — Parent/predecessor, maintains compatibility
- `the-guy` — Meta-orchestration layer
- `boot-sequence` — Skills get added to boot order automatically
- **NEW**: All existing skills via composition feature

**Distinct from v1**:
- Adaptive protocol (not fixed 7 phases)
- Morpheme-aware indexing
- Pattern learning and emergence detection
- Skill composition capabilities
- Usage analytics
- Contextual error healing (not just retry loops)

## Examples

### Example 1: Evolve Existing Skill (This One!)

**User**: "Create gremlin-jank-builder-v2"

**V2 Response**:
```
Analyzing v1 for improvement opportunities...

Observations from v1:
- Fixed 7-phase protocol is rigid for simple skills
- No mechanism to learn from generated skills  
- Missing composition patterns
- Error handling is retry-only, not adaptive

Creating gremlin-jank-builder-v2 with enhancements:
- ✓ Adaptive protocol based on skill tier (φ/π/e/i)
- ✓ Pattern learning from ecosystem
- ✓ Skill composition support
- ✓ Contextual error healing
- ✓ Usage analytics
- ✓ Emergence detection

Dewey ID: π.3.2.6 (Methodology/Cognitive Tools)
Tier: π (structural framework)
Novel patterns detected: 5
```

### Example 2: Compose Meta-Skill

**User**: "Create a skill that combines theory-lookup, reasoning-patterns, and synthesis"

**V2 Response**:
```
Detected composition request. Analyzing dependencies:
- theory-lookup: ✓ exists, π-tier
- reasoning-patterns: ✓ exists, e-tier
- synthesis-engine: ✓ exists, e-tier

Creating meta-skill: comprehensive-analyzer
Tier: e (combines multiple e-tier skills)
Composition: orchestrator pattern
Error handling: delegates to component skills

Generated comprehensive-analyzer with:
- Sequential orchestration (theory → reasoning → synthesis)
- Shared context passing via Git-brain temp storage
- Fallback if any component unavailable
- Trauma-informed coordination (supportive error delegation)

Novel pattern: "Sequential composition with shared context"
Recording for future use...
```

## Meta-Notes

This skill (v2) is the result of applying v1 to itself. **Key learnings**:

1. **Adaptive complexity**: Not all skills need 7 phases. Simple index skills (φ-tier) can skip intermediate steps.

2. **Pattern emergence**: V1 was good at *generating* skills but didn't *learn* from them. V2 closes this loop.

3. **Composition over creation**: Many "new" skills are actually orchestrations of existing ones. V2 recognizes this.

4. **Error healing, not just handling**: Retry loops are reactive. Adaptive healing is proactive (learns from history).

5. **Morpheme awareness**: MONAD's φ/π/e/i system is central to organization. V2 makes it first-class.

6. **Jank documentation**: V1 celebrated jank but didn't track it systematically. V2 records quirks for pattern analysis.

**The V2 → V3 Question**: Will V3 emerge from patterns we can't yet see? Track novel patterns in `v3-improvements.md`.

## References

For deeper understanding, see:
- `gremlin-philosophy-v2.md` — Enhanced chaos principles with learning
- `skill-builder-patterns-v2.md` — Tier-aware patterns and composition
- `git-brain-indexing-v2.md` — Morpheme-aware storage and analytics
- `templates/jank-skill-template-v2.md` — Enhanced template with autopoietic hooks
- `patterns/` — Reusable bash pattern library
- `v3-improvements.md` — Seeds for next evolution

**V2 Manifesto**: "The best way to predict the future is to build the tool that builds it."
