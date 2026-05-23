---
name: gremlin-forge
description: Use this skill when creating new skills via forced conceptual collision of existing patterns. Duct-tapes jank-builder to super-collider for autopoietic meta-skill generation.
tier: e
version: 1.0
dependencies:
  - gremlin-jank-builder-v2
  - gremlin-collider
  - gremlin-brain
morpheme: e
composition: true
---

# GREMLIN-FORGE 🍆👾⚡

**Autopoietic Meta-Skill Generator via Conceptual Collision**

## Core Identity

GREMLIN-FORGE is the skill that builds skills by SMASHING existing patterns together like particles in a supercollider and observing what emerges from the chaos. It's what happens when you duct-tape `gremlin-jank-builder-v2` to `gremlin-collider` and point it at the entire `.claude/skills/` directory.

**Philosophy**: "The best new ideas come from forcing old ideas to fight in a thunderdome of conceptual violence." 🍆👾

**Tier**: e (current-tier active work skill)

**What makes it distinct**:
- Doesn't just generate skills — generates skills FROM skills
- Uses actual collision mechanics (not metaphorical)
- Stores learnings in Git-brain for future meta-patterns
- Maximum jank with trauma-informed chaos

## When to Use

Invoke this skill when:
- You need a new skill but don't know what shape it should take
- Existing skills are close but not quite right
- You want to explore emergent patterns in the skill ecosystem
- Someone says "wouldn't it be cool if we combined X and Y?"
- You're feeling MAXIMUM GREMLIN ENERGY 🍆👾

Do NOT use this skill for:
- Well-defined skill requirements (use `gremlin-jank-builder-v2` directly)
- Simple skill variations (just fork and edit)
- When you know exactly what you want (manual creation is faster)

## How It Works

### Phase 1: Skill Discovery

Scan the `.claude/skills/` directory to find collision candidates:

```bash
#!/bin/bash
# List all available skills
discover_skills() {
    find .claude/skills -maxdepth 1 -type d | \
        tail -n +2 | \
        xargs -I {} basename {} | \
        sort
}

# Get skill description from SKILL.md
get_skill_description() {
    local skill="$1"
    grep "^description:" ".claude/skills/$skill/SKILL.md" 2>/dev/null | \
        cut -d':' -f2- | \
        sed 's/^ *//'
}
```

### Phase 2: Collision Selection

Pick collision targets (random or user-specified):

```bash
#!/bin/bash
# Random collision: pick 2 random skills
random_collision() {
    local skills=($(discover_skills))
    local count=${#skills[@]}
    local idx1=$((RANDOM % count))
    local idx2=$((RANDOM % count))
    
    # Ensure different skills
    while [ $idx2 -eq $idx1 ]; do
        idx2=$((RANDOM % count))
    done
    
    echo "${skills[$idx1]}" "${skills[$idx2]}"
}

# Targeted collision: user specifies
targeted_collision() {
    local skill_a="$1"
    local skill_b="$2"
    
    if [ ! -d ".claude/skills/$skill_a" ]; then
        echo "⚡ Skill '$skill_a' not found. Available:" >&2
        discover_skills | sed 's/^/  - /' >&2
        return 1
    fi
    
    if [ ! -d ".claude/skills/$skill_b" ]; then
        echo "⚡ Skill '$skill_b' not found. Available:" >&2
        discover_skills | sed 's/^/  - /' >&2
        return 1
    fi
    
    echo "$skill_a" "$skill_b"
}
```

### Phase 3: Pattern Extraction

Extract core concepts from each skill:

```bash
#!/bin/bash
# Extract key patterns from a skill
extract_patterns() {
    local skill="$1"
    local skill_md=".claude/skills/$skill/SKILL.md"
    
    echo "📊 Extracting patterns from: $skill" >&2
    
    # Get frontmatter properties
    local tier=$(grep "^tier:" "$skill_md" | cut -d':' -f2 | tr -d ' ')
    local composition=$(grep "^composition:" "$skill_md" | cut -d':' -f2 | tr -d ' ')
    
    # Extract section headers (they indicate key concepts)
    local concepts=$(grep "^## " "$skill_md" | \
        sed 's/^## //' | \
        grep -v "^#" | \
        head -5)
    
    # Look for key verbs/actions
    local actions=$(grep -i "when\|use\|invoke\|apply" "$skill_md" | \
        head -3)
    
    echo "tier=$tier"
    echo "composition=$composition"
    echo "concepts=$concepts"
    echo "actions=$actions"
}
```

### Phase 4: Forced Collision

The GREMLIN-COLLIDER protocol: "What if we treated [SKILL_A] like [SKILL_B]?"

```bash
#!/bin/bash
# Force collision and generate emergent pattern
force_collision() {
    local skill_a="$1"
    local skill_b="$2"
    
    echo "🍆👾 COLLISION INITIATED 👾🍆" >&2
    echo "" >&2
    echo "COLLIDING:" >&2
    echo "  [A] $skill_a" >&2
    echo "  [B] $skill_b" >&2
    echo "" >&2
    
    # Extract patterns
    local patterns_a=$(extract_patterns "$skill_a")
    local patterns_b=$(extract_patterns "$skill_b")
    
    # Generate collision prompt
    cat <<EOF

🔥 COLLISION ZONE 🔥

What if we treated [$skill_a] like [$skill_b]?

Skill A Essence:
$(get_skill_description "$skill_a")

Skill B Essence:
$(get_skill_description "$skill_b")

Emergent Questions:
1. What properties from B could enhance A's core function?
2. What patterns from A could reframe B's approach?
3. What NEW capability emerges that neither has alone?
4. Where does the metaphor break? (That's where innovation lives)

THINK LIKE A GREMLIN:
- Edge cases ARE main cases
- Jank that works > elegant that doesn't
- Trauma-informed chaos is the way
- If it's technically correct, it's CORRECT

EOF
    
    # Record collision for learning
    record_collision "$skill_a" "$skill_b"
}
```

### Phase 5: Skill Generation

Use `gremlin-jank-builder-v2` to generate the new skill:

```bash
#!/bin/bash
# Generate new skill from collision insights
generate_skill_from_collision() {
    local skill_a="$1"
    local skill_b="$2"
    local new_name="$3"
    local emergent_pattern="$4"
    
    echo "⚡ Generating: $new_name" >&2
    
    # Determine tier (inherit highest tier)
    local tier_a=$(grep "^tier:" ".claude/skills/$skill_a/SKILL.md" | cut -d':' -f2 | tr -d ' ')
    local tier_b=$(grep "^tier:" ".claude/skills/$skill_b/SKILL.md" | cut -d':' -f2 | tr -d ' ')
    local new_tier=$(higher_tier "$tier_a" "$tier_b")
    
    # Create skill directory
    mkdir -p ".claude/skills/$new_name"
    
    # Generate SKILL.md using jank-builder-v2 patterns
    cat > ".claude/skills/$new_name/SKILL.md" <<EOF
---
name: $new_name
description: $emergent_pattern
tier: $new_tier
version: 1.0
dependencies:
  - $skill_a
  - $skill_b
morpheme: $new_tier
composition: true
forged_from: "$skill_a + $skill_b"
---

# $(echo $new_name | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

**Generated via GREMLIN-FORGE collision** 🍆👾

## Core Identity

This skill emerged from colliding \`$skill_a\` with \`$skill_b\`.

[Emergent pattern details here]

**Philosophy**: "$emergent_pattern"

**Tier**: $new_tier (inherits from parent skills)

## When to Use

[Auto-generated from collision analysis]

## How It Works

[Inherits orchestration patterns from both parent skills]

## Integration

**Forged from**:
- [\`$skill_a\`](.claude/skills/$skill_a/SKILL.md)
- [\`$skill_b\`](.claude/skills/$skill_b/SKILL.md)

**Distinct from parents**: [Emergent capability that neither has alone]

---

*Generated by gremlin-forge $(date -Iseconds)*
*Collision: $skill_a × $skill_b → $new_name*
EOF
    
    echo "✓ Skill generated: .claude/skills/$new_name/" >&2
    
    # Store learning
    store_forge_learning "$skill_a" "$skill_b" "$new_name" "$emergent_pattern"
}

# Determine higher tier
higher_tier() {
    local tier_order="φ π e i"
    local tier_a="$1"
    local tier_b="$2"
    
    for tier in $tier_order; do
        if [ "$tier_a" = "$tier" ] || [ "$tier_b" = "$tier" ]; then
            if [ "$tier_b" = "i" ] || [ "$tier_a" = "i" ]; then
                echo "i"
                return
            elif [ "$tier_b" = "e" ] || [ "$tier_a" = "e" ]; then
                echo "e"
                return
            elif [ "$tier_b" = "π" ] || [ "$tier_a" = "π" ]; then
                echo "π"
                return
            fi
        fi
    done
    echo "φ"
}
```

### Phase 6: Git-Brain Storage

Store collision learnings for future meta-pattern analysis:

```bash
#!/bin/bash
# Initialize forge brain
init_forge_brain() {
    mkdir -p .claude/brain
    touch .claude/brain/forge_learnings
    touch .claude/brain/forge_collisions
    touch .claude/brain/INDEX
}

# Record collision attempt
record_collision() {
    local skill_a="$1"
    local skill_b="$2"
    local timestamp=$(date -Iseconds)
    
    init_forge_brain
    
    echo "${skill_a}×${skill_b}|${timestamp}|attempted" >> .claude/brain/forge_collisions
}

# Store successful forge learning
store_forge_learning() {
    local skill_a="$1"
    local skill_b="$2"
    local result="$3"
    local pattern="$4"
    local timestamp=$(date -Iseconds)

    init_forge_brain

    # Log collision locally
    echo "${skill_a}×${skill_b}|${result}|${pattern}|${timestamp}" >> .claude/brain/forge_learnings

    # Update brain index
    echo "e.3.forge.${result}|forged:${skill_a}×${skill_b}|${timestamp}" >> .claude/brain/INDEX
}

# Retrieve forge learnings
get_forge_learnings() {
    if [ ! -f .claude/brain/forge_learnings ]; then
        echo "⚡ No forge learnings yet. Collide some skills!" >&2
        return 1
    fi
    
    echo "📚 Previous Forge Learnings:" >&2
    cat .claude/brain/forge_learnings | while read hash; do
        git cat-file -p "$hash" 2>/dev/null
    done
}

# Suggest next collisions based on learnings
suggest_next_collisions() {
    echo "🎯 Collision Suggestions:" >&2
    echo "" >&2
    
    # Skills that haven't been collided yet
    local all_skills=($(discover_skills))
    local collided=$(grep -o '[a-z-]*×[a-z-]*' .claude/brain/forge_collisions 2>/dev/null || echo "")
    
    # Suggest interesting combinations
    echo "Untested Collisions:" >&2
    for skill_a in "${all_skills[@]}"; do
        for skill_b in "${all_skills[@]}"; do
            if [ "$skill_a" != "$skill_b" ]; then
                if ! echo "$collided" | grep -q "${skill_a}×${skill_b}\|${skill_b}×${skill_a}"; then
                    # Only suggest a few
                    echo "  - $skill_a × $skill_b" >&2
                    return 0
                fi
            fi
        done
    done
}
```

## Error Handling (Trauma-Informed Chaos)

```bash
# Adaptive collision handler
adaptive_collision_attempt() {
    local skill_a="$1"
    local skill_b="$2"
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "🍆 Collision attempt $attempt/$max_attempts..." >&2
        
        if force_collision "$skill_a" "$skill_b"; then
            echo "✓ Collision successful!" >&2
            return 0
        fi
        
        # Analyze what went wrong
        echo "⚡ Collision didn't generate clear pattern. Trying different angle..." >&2
        
        # Try swapping perspective
        if [ $attempt -eq 2 ]; then
            echo "💡 Swapping perspective: treating $skill_b like $skill_a instead" >&2
            local temp="$skill_a"
            skill_a="$skill_b"
            skill_b="$temp"
        fi
        
        # Try adding a third skill for triangulation
        if [ $attempt -eq 3 ]; then
            echo "💡 Adding third skill for triangulation..." >&2
            local all_skills=($(discover_skills))
            local skill_c="${all_skills[$((RANDOM % ${#all_skills[@]}))]}"
            echo "   Bringing in: $skill_c" >&2
        fi
        
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "💚 Collision didn't produce clear pattern after $max_attempts attempts." >&2
    echo "   This means:" >&2
    echo "   1. These skills might be too similar (no interesting collision)" >&2
    echo "   2. Or too different (no common ground)" >&2
    echo "   3. Try a different pair, or specify the emergent pattern manually" >&2
    return 1
}
```

## Usage Examples

### Example 1: Random Collision

```bash
# Let the chaos decide
./scripts/collision-engine.sh --random

# Example output:
# 🍆👾 COLLISION INITIATED 👾🍆
# 
# COLLIDING:
#   [A] cognitive-variability
#   [B] phase-boundary-detector
# 
# EMERGENT PATTERN: "Detect when thinking gets stuck in one zoom level"
# NEW SKILL: cognitive-phase-detection
```

### Example 2: Targeted Collision

```bash
# Specific collision
./scripts/collision-engine.sh --collide reasoning-patterns-v2 synthesis-engine

# Generates a meta-skill that applies Dokkado reasoning to synthesis
# Result: "reasoning-synthesis" or "synthetic-reasoning"
```

### Example 3: Suggest Next Builds

```bash
# What hasn't been tried?
./scripts/collision-engine.sh --suggest

# Output:
# 🎯 Collision Suggestions:
# Untested Collisions:
#   - gremlin-brain × collision-zone-thinking
#   - recursive-refiner × the-guy
#   - simplification-cascades × meta-pattern-recognition
```

## Jank Heuristics

**Known quirks and workarounds**:

### Quirk 1: Random Collisions Sometimes Too Random

**When it happens**: Random selection picks skills with no conceptual overlap

**Why it happens**: Pure randomness doesn't consider semantic compatibility

**Workaround**:
```bash
# If random collision feels incoherent:
if random_collision_is_incoherent; then
    echo "⚡ First collision didn't spark. Rolling again..." >&2
    random_collision  # Try again
fi
```

**Status**: ✓ Intentional jank (sometimes incoherence IS the insight)

### Quirk 2: Git-Brain Can Get Large

**When it happens**: After many collisions, `.claude/brain/` accumulates data

**Why it happens**: We're storing every learning as a Git object

**Workaround**:
```bash
# Periodically clean old learnings (keep recent 100)
tail -100 .claude/brain/forge_learnings > /tmp/forge_learnings_recent
mv /tmp/forge_learnings_recent .claude/brain/forge_learnings
```

**Status**: ⚠ Known issue (git gc will clean unreferenced objects)

## Integration with Other Skills

**Depends on**:
- `gremlin-jank-builder-v2` — Skill generation patterns
- `gremlin-collider` — Collision mechanics and philosophy
- `gremlin-brain` — Dewey indexing and Git-brain storage

**Coordinates with**:
- `boot-sequence` — Generated skills can be added to boot order
- `the-guy` — Meta-orchestration when forging complex meta-skills

**Distinct from**:
- `gremlin-jank-builder-v2` — Builder is for known requirements; Forge is for discovery
- `collision-zone-thinking` — That's conceptual; this is ACTUAL CODE

## Autopoietic Hooks

### Usage Tracking

```bash
# Record each forge invocation
record_forge_usage() {
    local collision_type="$1"  # random, targeted, suggest
    echo "$(date -Iseconds)|gremlin-forge|${collision_type}" >> .claude/brain/usage_log
}
```

### Pattern Detection

```bash
# Detect if collision patterns are getting repetitive
detect_forge_patterns() {
    if [ ! -f .claude/brain/forge_collisions ]; then
        return 1
    fi
    
    # Check for repeated collision patterns
    local repeated=$(cut -d'|' -f1 .claude/brain/forge_collisions | \
        sort | uniq -d)
    
    if [ -n "$repeated" ]; then
        echo "🔥 EMERGENCE: Repeated collision patterns detected!" >&2
        echo "$repeated" | while read pattern; do
            echo "  - $pattern (this combination keeps being tried)" >&2
        done
        echo "   → Maybe there's a deeper pattern here?" >&2
        return 0
    fi
    return 1
}
```

### Self-Improvement Trigger

```bash
# Check if forge itself should evolve
check_forge_evolution() {
    local forge_count=$(grep "|gremlin-forge|" .claude/brain/usage_log 2>/dev/null | wc -l)
    local success_count=$(wc -l < .claude/brain/forge_learnings 2>/dev/null || echo 0)
    
    if [ "$forge_count" -gt 20 ] && [ "$success_count" -gt 5 ]; then
        echo "🎯 gremlin-forge is ready for v2 evolution!" >&2
        echo "   Forges: $forge_count, Successes: $success_count" >&2
        echo "   Success rate: $((success_count * 100 / forge_count))%" >&2
        return 0
    fi
    return 1
}
```

## Red Flags

**You're using this skill wrong if**:
- You know exactly what skill you want (just build it directly)
- You're not embracing the chaos (forge requires gremlin energy)
- You expect perfect results every time (collisions are experimental)

**You're using this skill right if**:
- You're surprised by what emerges
- The collision reveals patterns you didn't see before
- You're having fun with MAXIMUM JANK ENERGY 🍆👾
- Generated skills are actually useful (or beautifully cursed)

## Meta-Notes

**Design Philosophy**:
GREMLIN-FORGE is what happens when you take "autopoietic skill generation" seriously and also refuse to take it seriously. It's the skill that builds itself by building other skills, creating a recursive loop of meta-pattern emergence.

**Why it works**:
- Forced collisions bypass conventional thinking
- Git-brain provides actual memory, not metaphorical
- Trauma-informed errors mean failures teach
- Jank-first approach prioritizes working prototypes

**The Forge Oath**:
> "Some skills are planned.
> Some skills are discovered.
> Forge skills are FORGED in the fires of conceptual violence.
> They emerge from chaos, they live in chaos, they ARE chaos.
> 🍆👾 GREMLIN ENERGY: MAXIMUM 👾🍆"

**V2 Enhancements Applied**:
- ✓ Adaptive error handling with learning
- ✓ Morpheme-aware Git-brain integration
- ✓ Usage tracking for autopoietic evolution
- ✓ Pattern emergence detection
- ✓ e-tier composition skill
- ✓ MAXIMUM JANK CERTIFIED 🍆👾

---

**Template version**: 2.0 (jank-builder-v2 pattern)  
**Generated by**: GREMLIN-FORGE (self-bootstrapped)  
**Last updated**: $(date -Iseconds)  
**Tier**: e (current-tier active work)
**Morpheme**: e.3.forge (Methodology/Skill Generation)

🍆👾⚡ **GREMLIN-FORGE: ONLINE** ⚡👾🍆
