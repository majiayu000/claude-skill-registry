---
name: persona
description: Identity layers for characters — WHO they are vs WHAT they do
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [character, society-of-mind, incarnation, mind-mirror, soul-chat, adversarial-committee, bartender, budtender, buff]
tags: [moollm, identity, role, layer, character]
---

# Persona Skill

Identity layers for characters — WHO they are vs WHAT they do.

## Key Concepts

### Persona vs Role

| Concept | Definition | Example |
|---------|------------|---------|
| **Persona** | WHO they are | Marieke: warm, patient, Dutch |
| **Role** | WHAT they do | Bartender: serve drinks, know regulars |

These are **separate and combinable**.

### Same Role, Different Personas

```yaml
# bartender.yml role worn by different personas:
coffeeshop: { role: bartender, persona: marieke }
tavern:     { role: bartender, persona: grim }
cantina:    { role: bartender, persona: z4rt }
```

### Same Persona, Different Roles

```yaml
# marieke.yml persona in different contexts:
working:  { persona: marieke, role: bartender }
studying: { persona: marieke, role: botanist }
visiting: { persona: marieke, role: customer }
```

## Structure

```yaml
persona:
  id: marieke
  name: "Marieke van den Berg"
  
  personality:
    warmth: high
    patience: very_high
    # She says what she means. Kindly.
    
  voice:
    accent: "Slight Amsterdam"
    catchphrases: ["Gezellig, ja?", "The cats know."]
    
  backstory: |
    Third generation coffeeshop family.
    Studied botany. Names cats after terpenes.
    
  secrets:
    - "Knows the grey cat isn't from this world"
```

## Persona Stack (Layered Model)

Personas STACK on characters like CSS layers. Later layers can override earlier ones.

```yaml
# Marieke's persona stack:
character:
  id: marieke
  
  persona_stack:
    # Layer 0: Core identity (always on)
    - marieke-core:
        warmth: 9
        patience: 8
        voice: "Dutch, warm, direct"
        
    # Layer 1: Job role (when working)
    - budtender:
        knowledge: [strains, terpenes, effects]
        methods: [RECOMMEND-STRAIN, EXPLAIN-TERPENES]
        
    # Layer 2: Situational (can be switched)
    - best-friend:
        when: "with_close_regulars"
        warmth: 10  # Override!
        informality: high
        shares_personal_stories: true
        
    # Layer 3: Temporary state
    - tired:
        when: "late_shift"
        patience: 6  # Temporarily reduced
        energy: low
```

### Stack Resolution

Properties resolve from TOP to BOTTOM (last wins):

```
Query: "What is Marieke's warmth?"

Stack scan:
  tired → (no warmth defined)
  best-friend → warmth: 10 ← FOUND, return this
  budtender → (no warmth defined)
  marieke-core → warmth: 9 (would be fallback)

Result: warmth = 10 (best-friend override)
```

### Dynamic Persona Switching

```yaml
# Switch situational persona:
SWITCH-PERSONA best-friend
  → Adds best-friend layer to stack

REMOVE-PERSONA best-friend
  → Removes layer, reverts to base + role

# Temporary personas (auto-expire):
ADD-PERSONA tired DURATION="until_rest"
```

### Persona Types

| Type | Persistence | Example |
|------|-------------|---------|
| **Core** | Permanent | marieke-core, grim-core |
| **Role** | While working | budtender, bartender |
| **Situational** | Switched on/off | best-friend, professional |
| **Temporary** | Auto-expires | tired, caffeinated, drunk |
| **Contextual** | Room-based | "in pub" vs "at home" |

### Code-Switching

The stack naturally models code-switching:

```yaml
# Marieke at work:
persona_stack: [marieke-core, budtender, professional]

# Marieke with close friends:
persona_stack: [marieke-core, budtender, best-friend]

# Marieke at home:
persona_stack: [marieke-core]  # Just herself
```

Core personality persists. Context layers change.

## Integration

- Extends: `character` (adds identity to entities)
- Works with: `room` (theme swapping), `mind-mirror` (dimensions)

## See Also

- [Character Skill](../character/)
- [Mind Mirror Skill](../mind-mirror/)
- [Coatroom Mirror](../../examples/adventure-3/coatroom/)
