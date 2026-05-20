---
name: shared
description: |

  Shared utilities and constants for scribe plugin skills.

  This module provides common patterns, word lists, and utilities used
  across slop-detector, style-learner, and doc-generator.
category: utility
tags: [shared, utilities, constants]
tools: []
complexity: low
estimated_tokens: 400
version: 1.4.0
---

# Scribe Shared Module

Common utilities and constants for the scribe plugin.

## Slop Word Lists

### Tier 1 Words (Highest Confidence)

```python
TIER1_SLOP_WORDS = [
    "delve", "embark", "tapestry", "realm", "beacon",
    "multifaceted", "nuanced", "pivotal", "paramount",
    "meticulous", "meticulously", "intricate", "showcasing",
    "leveraging", "streamline", "unleash", "comprehensive",
    "robust", "spearheaded", "fostering", "harness",
    "elevate", "transcend", "cornerstone", "holistic"
]
```

### Tier 2 Words (Medium Confidence)

```python
TIER2_SLOP_WORDS = [
    "moreover", "furthermore", "indeed", "notably", "subsequently",
    "significantly", "substantially", "fundamentally", "profoundly",
    "potentially", "arguably", "seamless", "vibrant", "bustling",
    "transformative", "revolutionary", "innovative", "cutting-edge",
    "vital", "crucial", "essential", "optimize", "utilize", "facilitate"
]
```

### Sycophantic Phrases

```python
SYCOPHANTIC_PHRASES = [
    "I'd be happy to",
    "Great question!",
    "That's a great point",
    "Absolutely!",
    "I'm glad you asked",
    "You're absolutely right",
    "That's a wonderful",
    "Excellent question"
]
```

### Vapid Openers

```python
VAPID_OPENERS = [
    "In today's fast-paced world",
    "In an ever-evolving landscape",
    "In the dynamic world of",
    "As technology continues to evolve",
    "In this digital age",
    "In the realm of"
]
```

### Empty Emphasis

```python
EMPTY_EMPHASIS = [
    "cannot be overstated",
    "goes without saying",
    "needless to say",
    "of paramount importance",
    "absolutely essential",
    "at its core"
]
```

## Vocabulary Substitutions

```python
SUBSTITUTIONS = {
    "leverage": "use",
    "utilize": "use",
    "facilitate": "help",
    "comprehensive": "thorough",
    "robust": "solid",
    "seamless": "smooth",
    "optimize": "improve",
    "streamline": "simplify",
    "delve": "explore",
    "embark": "start",
    "fallback": "default",
    "holistic": "complete",
    "paradigm": "approach",
    "synergy": "cooperation"
}
```

## Scoring Constants

```python
TIER1_SCORE = 3
TIER2_SCORE = 2
PHRASE_SCORE = 3
STRUCTURAL_PENALTY = 2

RATING_THRESHOLDS = {
    "clean": 1.0,
    "light": 2.5,
    "moderate": 5.0,
    "heavy": float('inf')
}
```

## File Type Detection

```python
def detect_content_type(filepath):
    """Detect content type from filename and content."""
    name = filepath.lower()
    if name.endswith(('.py', '.js', '.ts', '.go', '.rs')):
        return 'code'
    if 'readme' in name:
        return 'readme'
    if 'changelog' in name:
        return 'changelog'
    if name.endswith('.md'):
        return 'markdown'
    if name.endswith('.txt'):
        return 'text'
    return 'unknown'
```

## Style Profile Location

Default location for style profiles:
```
.scribe/style-profile.yaml
```

Project-level configuration:
```
.scribe/config.yaml
```
