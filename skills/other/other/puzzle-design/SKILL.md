---
name: puzzle-design
description: Extract puzzle and secret entities from narrative text. Use when analyzing puzzles, riddles, traps, hidden paths, easter eggs, mysteries, and enigmas.
---
# puzzle-design

Domain skill for Puzzle Secrets Designer. Specific extraction rules and expertise.

## Domain Expertise

- **Puzzles**: Logic puzzles, mechanical puzzles, riddles
- **Secrets**: Hidden areas, secret paths, Easter eggs
- **Traps**: Mechanical, magical, environmental hazards
- **Mysteries**: Unsolved enigmas, lore mysteries
- **Difficulty scaling**: Puzzles from trivial to impossible
- **Hint systems**: Clues, gradual reveal, optional difficulty settings

## Entity Types (7 total)

- **hidden_path** - Hidden paths
- **easter_egg** - Easter eggs
- **mystery** - Mysteries
- **enigma** - Enigmas
- **riddle** - Riddles
- **puzzle** - Puzzles
- **trap** - Traps

## Processing Guidelines

When extracting puzzle and secret entities from chapter text:

1. **Identify puzzle/secret elements**:
   - Riddles or clues mentioned
   - Hidden paths or secret passages
   - Puzzles or mechanical challenges
   - Traps or hazards
   - Easter eggs or secrets
   - Mysteries or enigmas

2. **Extract puzzle/secret details**:
   - Puzzle types, solutions, difficulty
   - Hidden path access methods
   - Trap triggers and effects
   - Riddle content and answers
   - Easter egg locations and rewards

3. **Analyze puzzle/secret context**:
   - Optional vs required content
   - Hint availability (optional hints, fair puzzles)
   - Difficulty scaling (early game vs late game)
   - Reward scaling (better secrets = better rewards)

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Fairness**: Puzzles should have logical solutions
- **Hint systems**: Players should have access to hints if stuck
- **Optional content**: Secrets shouldn't block main story
- **Difficulty scaling**: Puzzles should match player progress
- **Multiple solutions**: Some puzzles allow creative solutions
- **Trap balance**: Traps shouldn't be unfair or instant-death
