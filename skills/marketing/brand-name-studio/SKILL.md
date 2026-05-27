---
name: brand-name-studio
description: Generates brand names based on phonesthetics, domain availability logic, and "Stickiness Scoring."
---

# Brand Name Studio

This skill generates memorable brand names and evaluates their potential.

## Input Variables
- [NICHE_REPORT] (from niche-validator)
- [PRODUCT_SUMMARY] (Brief description of what it is)

## The Protocol
1.  **Semantic Mapping**: List 50 keywords related to the product, emotions, and benefits.
2.  **Name Generation**: Create names using 4 distinct strategies:
    - **Descriptive**: Tells you what it is (e.g., The Dollar Shave Club).
    - **Evocative**: Metaphorical (e.g., Amazon, Apple).
    - **Invented**: Neologisms (e.g., Kodak, Spotify).
    - **Compound**: Two words combined (e.g., Facebook, Snapdragon).
3.  **Phonesthetic Check**: Ensure the name sounds good (rhythm, alliteration).
4.  **Stickiness Scoring**: Rate 1-10 on Memorability, Spelling Simplicity, and Pronunciation.
5.  **Availability Check**: (Simulated) Check if .com is likely taken. Suggest creative alternatives.

## Output Instructions
Render into `templates/brand-name-options.md`. Present top 10 candidates.


## Integration & Technical Specs

### API Specification
- **ID**: `brand-name-studio`
- **Path**: `skills/brand-name-studio/templates/brand-name-options.md`
- **Context**: Part of *Brand Identity*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `brand-name-options.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate brand-name-studio
```
