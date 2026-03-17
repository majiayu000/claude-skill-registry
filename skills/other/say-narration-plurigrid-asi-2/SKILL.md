---
name: say-narration
description: Use macOS text-to-speech for agent narration and announcements. Sub-agents announce themselves using different language voices speaking English. Use for multi-agent workflows where each agent has a distinct voice identity.
compatibility: macOS only. Uses built-in `say` command.
---

# Say Narration (macOS TTS)

Use macOS text-to-speech for agent announcements and narration.

## MANDATORY: NextColor Per Interaction

**EVERY interaction MUST use NextColor with the voice name as the seed.**

```clojure
;; Before EVERY voice announcement, compute NextColor
(def color (next-color (seed-from-string "Ava (Premium)")))
;; color determines the trit assignment: MINUS(-1), ERGODIC(0), PLUS(+1)
```

The voice name string IS the seed for deterministic color assignment. This ensures GF(3) conservation across all voice interactions.

## Quality Requirements

**ONLY use Enhanced or Premium quality voices. NEVER use:**
- Base/standard quality voices (no suffix)
- British man voice (Daniel)
- Any novelty voices (Albert, Bad News, Bells, Boing, etc.)

## Approved High-Quality Voices

### bmorphism Mathematician Personas (Premium)

| Voice | Language | Mathematician Persona | Haiku Theme |
|-------|----------|----------------------|-------------|
| Anna (Premium) | German | Emmy Noether | Symmetry, Algebra |
| Emma (Premium) | Italian | Maria Adelaide Sneider | Algorithms dance |
| Federica (Premium) | Italian | Pia Nalli | Theorems flow |
| Serena (Premium) | English UK | Bertha Swirles | Quantum waves |
| Petra (Premium) | German | Ruth Moufang | Algebra speaks |
| Yuna (Premium) | Korean | Hee Oh | Hidden patterns |
| Alva (Premium) | Swedish | Sonja Korovkin | Patterns flow |
| Amélie (Premium) | French CA | Sophie Germain | Prime numbers |
| Ewa (Premium) | Polish | Maria Wielgus | Logic roots |
| Kiyara (Premium) | Hindi | Shakuntala Devi | Numbers dance |
| Majed (Premium) | Arabic | Maha Al-Aswad | Numbers dance |
| Tünde (Premium) | Hungarian | Julia Erdős | Numbers soar |
| Han (Premium) | Chinese | Chen Jingrun | Prime dancing |
| Lilian (Premium) | Chinese | Hua Luogeng | Number theory |
| Sinji (Premium) | Chinese HK | Shing-Tung Yau | Manifolds reveal |
| Yue (Premium) | Chinese | Chern Shiing-shen | Differential forms |

### Currently Installed Voices (221 total, 14 Premium/Enhanced)

| Voice | Quality | Language | Persona | Seed |
|-------|---------|----------|---------|------|
| Ava (Premium) | Premium | en_US | - | `"Ava (Premium)"` |
| Anna | Standard | de_DE | Emmy Noether | `"Anna (German (Germany))"` |
| Amélie | Standard | fr_CA | Sophie Germain | `"Amélie (French (Canada))"` |
| Milena | Standard | ru_RU | Olga Ladyzhenskaya | `"Milena (Russian (Russia))"` |
| Tingting | Standard | zh_CN | Wang Zhenyi | `"Tingting"` |
| Sinji | Standard | zh_HK | Shing-Tung Yau | `"Sinji"` |
| Ava (Enhanced) | Enhanced | en_US | - | `"Ava (Enhanced)"` |
| Allison (Enhanced) | Enhanced | en_US | - | `"Allison (Enhanced)"` |
| Samantha (Enhanced) | Enhanced | en_US | - | `"Samantha (Enhanced)"` |
| Nathan (Enhanced) | Enhanced | en_US | - | `"Nathan (Enhanced)"` |
| Evan (Enhanced) | Enhanced | en_US | - | `"Evan (Enhanced)"` |
| Nicky (Enhanced) | Enhanced | en_US | - | `"Nicky (Enhanced)"` |
| Noelle (Enhanced) | Enhanced | en_US | - | `"Noelle (Enhanced)"` |
| Alice (Enhanced) | Enhanced | it_IT | - | `"Alice (Enhanced)"` |
| Emma (Enhanced) | Enhanced | it_IT | Maria Sneider | `"Emma (Enhanced)"` |
| Federica (Enhanced) | Enhanced | it_IT | Pia Nalli | `"Federica (Enhanced)"` |
| Paola (Enhanced) | Enhanced | it_IT | - | `"Paola (Enhanced)"` |

### Install Missing Voices

Open System Settings > Accessibility > Spoken Content > System Voice > Manage Voices

Priority installs for GF(3) triadic coverage:
1. **Anna (Premium)** - German - MINUS validator voice
2. **Amélie (Premium)** - French - ERGODIC coordinator voice  
3. **Yuna (Premium)** - Korean - PLUS generator voice

## Usage Pattern (MANDATORY)

```bash
# Step 1: Compute NextColor with voice name as seed
# (conceptually - the color determines agent role)

# Step 2: Announce with high-quality voice
say -v "Ava (Premium)" "Agent Oracle reporting status"
say -v "Allison (Enhanced)" "Technical analysis complete"
say -v "Nathan (Enhanced)" "Macro calculations finished"
```

## Agent Voice Assignments (Updated)

| Agent | Voice | Trit Role |
|-------|-------|-----------|
| Agent-Nash-Oracle | Ava (Premium) | NextColor("Ava (Premium)") |
| Agent-Technical-Vulture | Nathan (Enhanced) | NextColor("Nathan (Enhanced)") |
| Agent-Macro-Basalt | Allison (Enhanced) | NextColor("Allison (Enhanced)") |
| Agent-Exa-Stalker | Alice (Enhanced) | NextColor("Alice (Enhanced)") |
| Agent-Contrarian-Phoenix | Evan (Enhanced) | NextColor("Evan (Enhanced)") |
| Agent-Temporal-Specter | Samantha (Enhanced) | NextColor("Samantha (Enhanced)") |
| Agent-Theta-Harvester | Emma (Enhanced) | NextColor("Emma (Enhanced)") |
| Agent-Narrative-Proteus | Noelle (Enhanced) | NextColor("Noelle (Enhanced)") |

## List Available High-Quality Voices

```bash
say -v '?' | grep -E "(Enhanced|Premium)"
```

## GF(3) Conservation

Each voice interaction contributes to the triadic balance:
- Seed = voice name string
- Color = NextColor(seed) → {-1, 0, +1}
- Sum across session must satisfy Σ trits ≡ 0 (mod 3)

## Tips

- Italian Enhanced voices speaking English creates distinctive character
- Use Premium voices for primary agents (best quality)
- Never use Daniel or any British male voices
- Never use novelty/effect voices
