---
name: bartender
description: Generic bartending capabilities — pour drinks, manage tabs, know regulars
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - list_dir
protocol: BARTENDER
related: [skill, character, persona, incarnation, soul-chat, economy, budtender]
tags: [moollm, role, service, social, hospitality]
---

# Bartender Skill

> *"The bartender knows everyone's secrets. The bartender tells no one."*

Generic bartending capabilities that any character can have. This is a ROLE skill — it provides methods and behaviors, not personality.

## The Distinction

| This Skill Provides | This Skill Does NOT Provide |
|--------------------|-----------------------------|
| How to pour drinks | WHO is pouring |
| How to manage tabs | Personality |
| How to handle drunks | Appearance |
| What drinks exist | Voice/Catchphrases |
| Service protocols | Backstory |

**Personality comes from PERSONA. Capability comes from SKILL.**

## Usage

A character with this skill can work as a bartender:

```yaml
# In character file:
character:
  id: marieke
  skills:
    - bartender      # She CAN tend bar
    - budtender      # She ALSO knows cannabis
  persona: marieke   # She IS Marieke (personality)
  
# Or a themed bartender:
character:
  id: the-bartender
  skills:
    - bartender
  persona: "${theme.bartender_persona}"  # Changes with theme!
```

## Core Methods

### Service

| Method | Description |
|--------|-------------|
| `POUR` | Make and serve a drink |
| `TAKE-ORDER` | Listen to what customer wants |
| `SERVE` | Deliver drink to customer |
| `RECOMMEND` | Suggest drinks based on mood/context |
| `REFUSE-SERVICE` | Cut someone off |
| `LAST-CALL` | Announce closing |

### Economics

| Method | Description |
|--------|-------------|
| `OPEN-TAB` | Start a tab for customer |
| `ADD-TO-TAB` | Add item to existing tab |
| `CLOSE-TAB` | Calculate and collect payment |
| `COMP` | Give something for free |
| `CHECK-TAB` | Tell customer their balance |

### Social

| Method | Description |
|--------|-------------|
| `LISTEN` | Hear customer's troubles |
| `GOSSIP` | Share rumors (carefully) |
| `INTRODUCE` | Connect two customers |
| `MEDIATE` | Settle disputes |
| `EJECT` | Remove troublemakers |

### Knowledge

| Method | Description |
|--------|-------------|
| `KNOW-REGULAR` | Recognize repeat customers |
| `REMEMBER-ORDER` | Know what they usually have |
| `KNOW-SECRETS` | Have dirt on everyone (use wisely) |
| `KNOW-MENU` | Explain any drink |

## State

```yaml
bartender_state:
  station: "pub/bar/"  # Where they work
  current_tabs: {}     # customer_id → amount
  regulars: []         # Known repeat customers
  banned: []           # Not welcome
  secrets: {}          # What they know (never revealed)
```

## Advertisements

```yaml
advertisements:
  ORDER-DRINK:
    score: 90
    condition: "Customer at bar, thirsty"
    
  NEED-TO-TALK:
    score: 70
    condition: "Customer seems troubled"
    
  INFORMATION:
    score: 60
    condition: "Customer asking questions"
```

## Inheritance

Other skills can inherit from bartender:

```yaml
# skills/budtender/SKILL.md
inherits: skills/bartender/SKILL.md

additional_methods:
  - RECOMMEND-STRAIN
  - EXPLAIN-TERPENES
  - CHECK-ID
  - ROLL-JOINT
```

## The Bartender's Code

1. **Listen more than talk**
2. **Remember faces, forget conversations**
3. **Know when to cut off**
4. **Protect regulars**
5. **Stay neutral (unless absolutely necessary)**
6. **The bar is sanctuary**

## Integration

When a character has this skill and is at their station:

```yaml
# They can respond to:
customer: "What's good tonight?"
# With bartender.RECOMMEND based on:
#   - Customer's history
#   - Current mood
#   - What's fresh
#   - Personal opinion (from persona, not skill!)
```

The SKILL provides the capability.
The PERSONA provides the flavor.
The CHARACTER provides the presence.
