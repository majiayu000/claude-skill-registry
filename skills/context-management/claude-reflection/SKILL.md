---
name: claude-reflection
description: Self-improvement and learning skill that helps Claude learn from user interactions, corrections, and preferences
version: 1.0.0
category: workspace-hub
type: skill
trigger: auto
auto_execute: true
capabilities:
  - correction_detection
  - preference_capture
  - pattern_extraction
  - knowledge_persistence
  - cross_session_learning
tools:
  - Read
  - Write
  - Edit
tags: [meta, learning, self-improvement, memory]
platforms: [all]
related_skills:
  - skill-learner
  - repo-readiness
---

# Claude Reflection Skill

> Meta-skill for continuous self-improvement through the Reflect, Abstract, Generalize, Store loop.

## Quick Start

```bash
# Auto-triggers on detection of:
# - User corrections
# - Preference statements
# - Repeated patterns
# - Positive reinforcement

# Manual trigger for reflection
/claude-reflection

# Review captured learnings
cat ~/.claude/memory/learnings.yaml

# Sync learnings across sessions
/claude-reflection --sync
```

## Overview

The claude-reflection skill enables Claude to learn continuously from user interactions, capturing corrections, preferences, workflow patterns, and positive feedback. Unlike session-scoped context, learnings persist across conversations through structured memory files.

### Why This Matters

**Without reflection:**
- Same mistakes repeated across sessions
- User preferences forgotten
- Valuable patterns lost
- No accumulation of domain knowledge

**With reflection:**
- Corrections learned once, applied forever
- User preferences remembered and applied
- Workflow patterns automated over time
- Domain expertise accumulates across sessions

### Core Philosophy

```
REFLECT    - Notice what happened (correction, preference, pattern)
ABSTRACT   - Extract the generalizable principle
GENERALIZE - Determine scope (global, domain, project, session)
STORE      - Persist to appropriate memory file
```

## When to Use

### Auto-Detection Triggers

This skill auto-executes when it detects these patterns in conversation:

**1. Direct Correction**
```
User: "No, don't use snake_case for that. Use camelCase for JavaScript."
Trigger: Explicit correction of Claude's behavior
Action: Capture coding style preference
```

**2. Preference Statement**
```
User: "I prefer shorter commit messages, just one line."
Trigger: Statement of preference (I prefer, I like, I want, always, never)
Action: Capture workflow preference
```

**3. Explicit Memory Request**
```
User: "Remember that this project uses tabs, not spaces."
Trigger: Direct request to remember (remember, don't forget, always do)
Action: Store as project-level preference
```

**4. Positive Reinforcement**
```
User: "Perfect! That's exactly how I want error messages formatted."
Trigger: Positive feedback on specific behavior
Action: Reinforce and capture the pattern
```

**5. Repeated Patterns**
```
User asks for the same type of change 3+ times in a session
Trigger: Repetition detection
Action: Extract pattern for automation
```

**6. Error-Then-Success**
```
Claude makes mistake -> User corrects -> Claude succeeds
Trigger: Correction followed by success
Action: Capture the correction as a learning
```

### Manual Trigger

```bash
# Force reflection analysis on recent conversation
/claude-reflection

# Reflect on specific topic
/claude-reflection --topic "code formatting"

# Export learnings for review
/claude-reflection --export

# Clear session learnings (keeps persistent)
/claude-reflection --clear-session
```

## Core Process

### The Reflect-Abstract-Generalize-Store Loop

```
                    +------------------+
                    |    DETECTION     |
                    | (correction,     |
                    |  preference,     |
                    |  pattern)        |
                    +--------+---------+
                             |
                             v
+------------------+    +---------+    +------------------+
|     REFLECT      |<---|  Event  |--->|     ABSTRACT     |
| What happened?   |    +---------+    | What's the       |
| What was wrong?  |                   | underlying       |
| What was right?  |                   | principle?       |
+--------+---------+                   +--------+---------+
         |                                      |
         v                                      v
+------------------+                   +------------------+
|   GENERALIZE     |                   |      STORE       |
| What scope?      |                   | Where to save?   |
| Global/Domain/   |                   | What format?     |
| Project/Session  |                   | How to retrieve? |
+--------+---------+                   +------------------+
         |                                      ^
         +--------------------------------------+
```

### Step 1: Reflect

Analyze what happened in the interaction:

```python
# Example reflection analysis
def reflect(interaction: dict) -> dict:
    """Analyze what happened and why."""
    reflection = {
        "event_type": classify_event(interaction),
        "what_happened": interaction["claude_action"],
        "user_response": interaction["user_feedback"],
        "outcome": "correction" | "success" | "preference",
        "confidence": calculate_confidence(interaction)
    }
    return reflection

# Example: User corrected formatting
# {
#     "event_type": "correction",
#     "what_happened": "Used 4-space indentation",
#     "user_response": "Use 2-space indentation for this project",
#     "outcome": "correction",
#     "confidence": 0.95
# }
```

### Step 2: Abstract

Extract the generalizable principle:

```python
# Example abstraction
def abstract_principle(reflection: dict) -> dict:
    """Extract the underlying principle from the reflection."""
    principle = {
        "category": categorize(reflection),  # coding_style, workflow, communication
        "rule": extract_rule(reflection),
        "anti_pattern": reflection.get("what_happened"),
        "correct_pattern": extract_correct_pattern(reflection),
        "context_clues": extract_context(reflection)
    }
    return principle

# Example output:
# {
#     "category": "coding_style",
#     "rule": "Use 2-space indentation",
#     "anti_pattern": "4-space indentation",
#     "correct_pattern": "2-space indentation",
#     "context_clues": ["javascript", "this project"]
# }
```

### Step 3: Generalize

Determine the appropriate scope:

```python
# Example generalization
def determine_scope(principle: dict) -> str:
    """Determine if learning is global, domain, project, or session specific."""

    context_clues = principle.get("context_clues", [])

    # Session-only: temporary, experimental
    if any(word in context_clues for word in ["just this time", "for now", "temporarily"]):
        return "session"

    # Project-specific: mentions project name or "this project"
    if "this project" in context_clues or detect_project_name(context_clues):
        return "project"

    # Domain-specific: mentions technology or domain
    if detect_domain(context_clues):  # javascript, python, marine, etc.
        return "domain"

    # Global: general preference, no specific context
    return "global"

# Example: "this project" -> scope: project
```

### Step 4: Store

Persist the learning appropriately:

```python
# Example storage
def store_learning(principle: dict, scope: str) -> None:
    """Store learning in appropriate memory location."""

    learning_entry = {
        "timestamp": datetime.now().isoformat(),
        "category": principle["category"],
        "rule": principle["rule"],
        "anti_pattern": principle.get("anti_pattern"),
        "correct_pattern": principle["correct_pattern"],
        "confidence": principle.get("confidence", 0.8),
        "source": "user_correction",
        "times_applied": 0
    }

    # Route to appropriate storage
    storage_paths = {
        "global": "~/.claude/memory/global_learnings.yaml",
        "domain": f"~/.claude/memory/domains/{domain}/learnings.yaml",
        "project": ".claude/memory/project_learnings.yaml",
        "session": "session_context"  # Not persisted
    }

    append_to_yaml(storage_paths[scope], learning_entry)
```

## Storage Scopes

### Scope Hierarchy

```
+----------------------------------------------------------+
|  GLOBAL (~/.claude/memory/global_learnings.yaml)         |
|  - User-wide preferences                                  |
|  - Universal coding style                                 |
|  - Communication preferences                              |
|  +-----------------------------------------------------+ |
|  |  DOMAIN (~/.claude/memory/domains/<domain>/)        | |
|  |  - Technology-specific preferences                   | |
|  |  - Domain knowledge (marine, finance, etc.)         | |
|  |  +------------------------------------------------+ | |
|  |  |  PROJECT (.claude/memory/project_learnings.yaml)| | |
|  |  |  - Project conventions                          | | |
|  |  |  - Team standards                               | | |
|  |  |  +-------------------------------------------+ | | |
|  |  |  |  SESSION (in-memory only)                 | | | |
|  |  |  |  - Temporary adjustments                  | | | |
|  |  |  |  - Experimental preferences               | | | |
|  |  |  +-------------------------------------------+ | | |
|  |  +------------------------------------------------+ | |
|  +-----------------------------------------------------+ |
+----------------------------------------------------------+
```

### Storage Locations

| Scope | Location | Persistence | Example |
|-------|----------|-------------|---------|
| Global | `~/.claude/memory/` | Permanent | "Always use descriptive variable names" |
| Domain | `~/.claude/memory/domains/<name>/` | Permanent | "JavaScript: use camelCase" |
| Project | `.claude/memory/` | With project | "This repo uses tabs" |
| Session | In-memory | Session only | "Skip tests for this PR" |

### Directory Structure

```
~/.claude/
├── memory/
│   ├── global_learnings.yaml       # User-wide learnings
│   ├── preferences.yaml            # User preferences
│   ├── patterns.yaml               # Workflow patterns
│   ├── corrections.yaml            # Correction history
│   └── domains/
│       ├── python/
│       │   ├── learnings.yaml
│       │   └── patterns.yaml
│       ├── javascript/
│       │   ├── learnings.yaml
│       │   └── patterns.yaml
│       └── marine-engineering/
│           ├── learnings.yaml
│           └── domain_knowledge.yaml
└── reflection/
    ├── session_log.yaml            # Current session learnings
    └── pending_confirmations.yaml  # Learnings awaiting validation

<project>/.claude/
├── memory/
│   ├── project_learnings.yaml      # Project-specific learnings
│   ├── team_preferences.yaml       # Team conventions
│   └── automation_candidates.yaml  # Patterns to automate
└── reflection/
    └── history.yaml                # Reflection history
```

## Core Capabilities

### 1. Correction Detection and Learning

**Detection Patterns:**

```yaml
# Correction indicators
correction_signals:
  explicit:
    - "No, "
    - "Actually, "
    - "That's wrong"
    - "Don't do that"
    - "Instead, "
    - "Use X instead of Y"

  implicit:
    - user_edits_claude_output
    - user_asks_to_redo
    - user_provides_alternative

  contextual:
    - negation_after_claude_action
    - contrast_statement
```

**Example 1: Coding Style Correction**

```yaml
# Detected interaction
interaction:
  claude_action: "Created function with snake_case name: get_user_data()"
  user_response: "Use camelCase for JavaScript functions"

# Reflection output
reflection:
  event_type: correction
  category: coding_style
  rule: "Use camelCase for JavaScript function names"
  anti_pattern: "snake_case function names"
  correct_pattern: "camelCase function names"
  scope: domain
  domain: javascript
  confidence: 0.95

# Stored learning
learning:
  id: "js-function-naming-001"
  timestamp: "2026-01-17T10:30:00Z"
  category: coding_style
  scope: domain
  domain: javascript
  rule: "Use camelCase for function names in JavaScript"
  example:
    wrong: "get_user_data()"
    right: "getUserData()"
  source: user_correction
  confidence: 0.95
```

**Example 2: Error Handling Correction**

```python
# Claude's original approach (incorrect)
def process_data(data):
    return data.transform()  # No error handling

# User correction:
# "Always wrap data operations in try-except with logging"

# Learned pattern
learning = {
    "category": "error_handling",
    "scope": "global",
    "rule": "Wrap data operations in try-except with logging",
    "anti_pattern": """
def process_data(data):
    return data.transform()
""",
    "correct_pattern": """
def process_data(data):
    try:
        return data.transform()
    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        raise
""",
    "confidence": 0.9
}
```

### 2. Preference Capture

**Preference Indicators:**

```yaml
# Phrases indicating preferences
preference_signals:
  strong:
    - "I prefer"
    - "I always want"
    - "Never do"
    - "Always use"
    - "My preference is"

  moderate:
    - "I like"
    - "I'd rather"
    - "Can you use"
    - "Let's go with"

  implicit:
    - consistent_user_choices
    - repeated_requests_for_same_format
```

**Example 3: Communication Preference**

```yaml
# Detected preference
interaction:
  context: "Claude provided detailed explanation"
  user_response: "I prefer concise responses. Just give me the code."

# Captured preference
preference:
  id: "comm-style-001"
  timestamp: "2026-01-17T11:00:00Z"
  category: communication
  scope: global
  preference: "Provide concise responses with minimal explanation"
  context: "When providing code solutions"
  strength: strong
  source: explicit_statement

# Application rule
application:
  when: "user_asks_for_code"
  action: "Provide code with brief comment, skip lengthy explanations"
  unless: "user_asks_for_explanation"
```

**Example 4: Formatting Preference**

```yaml
# Detected pattern (multiple interactions)
interactions:
  - user_edits_claude_output: "Removed extra blank lines"
  - user_edits_claude_output: "Removed extra blank lines"
  - user_statement: "Too much whitespace"

# Captured preference
preference:
  id: "format-whitespace-001"
  category: formatting
  scope: global
  preference: "Minimize blank lines in code output"
  evidence:
    - "2 edits removing blank lines"
    - "explicit complaint about whitespace"
  confidence: 0.85
```

### 3. Pattern Extraction from Repeated Workflows

**Pattern Detection:**

```python
def detect_workflow_pattern(session_history: list) -> Optional[dict]:
    """Detect repeated workflow patterns worth automating."""

    # Look for repeated sequences
    sequences = extract_sequences(session_history)

    for sequence in sequences:
        if sequence.occurrences >= 3:
            pattern = {
                "steps": sequence.steps,
                "occurrences": sequence.occurrences,
                "trigger": identify_trigger(sequence),
                "automation_potential": calculate_automation_score(sequence)
            }

            if pattern["automation_potential"] > 0.7:
                return pattern

    return None
```

**Example 5: Git Workflow Pattern**

```yaml
# Detected repeated workflow
pattern:
  id: "git-workflow-001"
  name: "Feature Branch Workflow"
  occurrences: 5

  steps:
    - action: "git checkout -b feature/..."
      variation: "branch name varies"
    - action: "make changes"
    - action: "git add ."
    - action: "git commit -m '...'"
      variation: "message varies"
    - action: "git push -u origin feature/..."
    - action: "gh pr create"

  trigger: "user says 'new feature' or 'start feature'"

  automation:
    potential: 0.85
    suggestion: "Create /start-feature command"
    template: |
      git checkout -b feature/{name}
      # ... make changes ...
      git add .
      git commit -m "{type}: {description}"
      git push -u origin feature/{name}
      gh pr create --title "{description}"

# Stored for potential skill creation
automation_candidate:
  pattern_id: "git-workflow-001"
  skill_name: "feature-branch-creator"
  priority: high
  confirmed: false
```

**Example 6: Data Analysis Pattern**

```yaml
# Detected repeated workflow
pattern:
  id: "data-analysis-001"
  name: "CSV Analysis Workflow"
  occurrences: 4

  steps:
    - action: "Load CSV with pandas"
    - action: "Check for missing values"
    - action: "Generate summary statistics"
    - action: "Create visualization"
    - action: "Export HTML report"

  parameters:
    - input_file: varies
    - output_path: "reports/"
    - viz_type: usually "plotly"

  automation:
    potential: 0.9
    suggestion: "Create /analyze-csv command"
    template: |
      df = pd.read_csv("{input_file}")
      missing = df.isnull().sum()
      stats = df.describe()
      fig = create_plotly_viz(df)
      save_html_report(fig, stats, "{output_path}")
```

### 4. Knowledge Persistence

**File Format: YAML**

```yaml
# ~/.claude/memory/global_learnings.yaml
version: "1.0"
last_updated: "2026-01-17T12:00:00Z"
total_learnings: 15

learnings:
  - id: "learn-001"
    timestamp: "2026-01-15T09:00:00Z"
    category: coding_style
    rule: "Use descriptive variable names over abbreviations"
    example:
      wrong: "x = get_val()"
      right: "user_count = get_user_count()"
    confidence: 0.95
    times_applied: 12
    last_applied: "2026-01-17T10:30:00Z"
    validated: true

  - id: "learn-002"
    timestamp: "2026-01-16T14:00:00Z"
    category: communication
    rule: "Provide code first, explanation after"
    context: "When user asks for code solution"
    confidence: 0.9
    times_applied: 8
    last_applied: "2026-01-17T11:00:00Z"
    validated: true

  - id: "learn-003"
    timestamp: "2026-01-17T10:00:00Z"
    category: error_handling
    rule: "Always include error context in log messages"
    example:
      wrong: 'logger.error("Failed")'
      right: 'logger.error(f"Failed to process {item}: {e}")'
    confidence: 0.85
    times_applied: 3
    last_applied: "2026-01-17T11:30:00Z"
    validated: false  # Needs more applications
```

**Persistence Operations:**

```python
def persist_learning(learning: dict, scope: str) -> str:
    """Persist a learning to the appropriate memory file."""

    # Determine storage path
    if scope == "global":
        path = Path.home() / ".claude/memory/global_learnings.yaml"
    elif scope == "domain":
        domain = learning.get("domain", "general")
        path = Path.home() / f".claude/memory/domains/{domain}/learnings.yaml"
    elif scope == "project":
        path = Path.cwd() / ".claude/memory/project_learnings.yaml"
    else:
        return "session_only"  # Don't persist

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing learnings
    if path.exists():
        with open(path) as f:
            data = yaml.safe_load(f) or {"learnings": []}
    else:
        data = {
            "version": "1.0",
            "last_updated": None,
            "total_learnings": 0,
            "learnings": []
        }

    # Add new learning
    learning["id"] = f"learn-{len(data['learnings']) + 1:04d}"
    data["learnings"].append(learning)
    data["last_updated"] = datetime.now().isoformat()
    data["total_learnings"] = len(data["learnings"])

    # Write back
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)

    return learning["id"]
```

### 5. Cross-Session Learning

**Loading Learnings at Session Start:**

```python
def load_applicable_learnings(project_path: Optional[Path] = None) -> dict:
    """Load all learnings applicable to current context."""

    learnings = {
        "global": [],
        "domain": [],
        "project": []
    }

    # 1. Load global learnings
    global_path = Path.home() / ".claude/memory/global_learnings.yaml"
    if global_path.exists():
        with open(global_path) as f:
            data = yaml.safe_load(f)
            learnings["global"] = data.get("learnings", [])

    # 2. Load domain learnings (detect from project)
    domains = detect_project_domains(project_path)
    for domain in domains:
        domain_path = Path.home() / f".claude/memory/domains/{domain}/learnings.yaml"
        if domain_path.exists():
            with open(domain_path) as f:
                data = yaml.safe_load(f)
                learnings["domain"].extend(data.get("learnings", []))

    # 3. Load project learnings
    if project_path:
        project_mem = project_path / ".claude/memory/project_learnings.yaml"
        if project_mem.exists():
            with open(project_mem) as f:
                data = yaml.safe_load(f)
                learnings["project"] = data.get("learnings", [])

    return learnings

def apply_learnings_to_context(learnings: dict) -> str:
    """Generate context prompt from loaded learnings."""

    context_parts = []

    # High-priority learnings (high confidence, frequently applied)
    priority_learnings = []
    for scope in ["global", "domain", "project"]:
        for learning in learnings[scope]:
            if learning.get("confidence", 0) > 0.8 and learning.get("times_applied", 0) > 3:
                priority_learnings.append(learning)

    if priority_learnings:
        context_parts.append("## Learned Preferences\n")
        for learning in priority_learnings[:10]:  # Top 10
            context_parts.append(f"- {learning['rule']}")

    return "\n".join(context_parts)
```

**Validation and Reinforcement:**

```yaml
# Validation rules
validation:
  # Learning becomes validated after:
  conditions:
    - times_applied >= 5
    - no_contradictions: true
    - user_confirmed: true  # Optional but accelerates

  # Confidence decay for unused learnings
  decay:
    days_without_use: 30
    decay_rate: 0.05  # -5% per month of non-use
    minimum_confidence: 0.3

  # Reinforcement on successful application
  reinforcement:
    successful_application: +0.02
    user_confirmation: +0.1
    maximum_confidence: 0.99
```

## Integration with Progress Tracking

### Hook Integration

```bash
#!/bin/bash
# .claude/hooks/post-interaction.sh
# Called after each significant interaction

INTERACTION_LOG="$1"
REFLECTION_SKILL="$HOME/.claude/skills/workspace-hub/claude-reflection"

# Check for reflection triggers
if grep -qE "(No,|Actually,|I prefer|Remember that)" "$INTERACTION_LOG"; then
    echo "Reflection trigger detected, analyzing..."
    "$REFLECTION_SKILL/analyze.sh" "$INTERACTION_LOG"
fi
```

### Session Summary

At session end, generate reflection summary:

```yaml
# Session reflection summary
session_summary:
  session_id: "2026-01-17-session-001"
  duration: "2h 30m"

  learnings_captured:
    total: 5
    corrections: 2
    preferences: 2
    patterns: 1

  details:
    - type: correction
      rule: "Use 2-space indentation for YAML"
      scope: domain
      confidence: 0.95

    - type: preference
      rule: "Prefer functional approach over OOP"
      scope: project
      confidence: 0.85

    - type: pattern
      name: "Test-then-implement workflow"
      occurrences: 3
      automation_potential: 0.7

  validation_status:
    pending: 3
    validated: 2

  recommendations:
    - "Consider creating /yaml-format command for repeated YAML formatting"
    - "Review python domain learnings - 2 may conflict"
```

## File Formats

### learnings.yaml Schema

```yaml
# Schema for learnings files
$schema: "https://workspace-hub.dev/schemas/learnings-v1.yaml"

version: "1.0"
last_updated: "2026-01-17T12:00:00Z"
total_learnings: 0

metadata:
  scope: global | domain | project
  domain: null | string  # For domain-scoped
  project: null | string  # For project-scoped

learnings:
  - id: string           # Unique identifier
    timestamp: datetime  # When captured
    category: string     # coding_style, communication, workflow, error_handling, etc.
    rule: string         # The learned rule/preference
    context: string      # When this applies (optional)

    example:             # Optional example
      wrong: string
      right: string

    anti_pattern: string # What NOT to do (optional)
    correct_pattern: string # What TO do (optional)

    confidence: float    # 0.0 to 1.0
    times_applied: int   # Usage count
    last_applied: datetime

    source: string       # user_correction, preference_statement, pattern_extraction
    validated: boolean   # Meets validation criteria

    tags: list[string]   # Optional categorization
```

### preferences.yaml Schema

```yaml
# Schema for preferences files
$schema: "https://workspace-hub.dev/schemas/preferences-v1.yaml"

version: "1.0"
last_updated: "2026-01-17T12:00:00Z"

preferences:
  communication:
    verbosity: concise | detailed | adaptive
    explanation_style: code_first | explanation_first | balanced
    question_format: direct | exploratory

  coding:
    indentation: spaces | tabs
    indent_size: 2 | 4
    naming_convention: snake_case | camelCase | PascalCase
    comments: minimal | moderate | comprehensive

  workflow:
    tdd: true | false
    commit_style: conventional | descriptive | minimal
    branch_naming: feature/ | feat/ | custom

  formatting:
    line_length: 80 | 100 | 120
    blank_lines: minimal | standard
    trailing_newline: true | false
```

### patterns.yaml Schema

```yaml
# Schema for workflow patterns
$schema: "https://workspace-hub.dev/schemas/patterns-v1.yaml"

version: "1.0"
last_updated: "2026-01-17T12:00:00Z"

patterns:
  - id: string
    name: string
    description: string

    trigger:
      phrases: list[string]
      conditions: list[string]

    steps:
      - action: string
        parameters: dict
        optional: boolean

    occurrences: int
    last_used: datetime

    automation:
      potential: float  # 0.0 to 1.0
      skill_candidate: boolean
      suggested_command: string
```

## Best Practices

### 1. Learning Quality

**Do:**
- Capture specific, actionable learnings
- Include examples when available
- Set appropriate scope (don't over-generalize)
- Validate learnings over time

**Don't:**
- Capture one-off adjustments as permanent learnings
- Over-generalize from single instances
- Ignore conflicting learnings
- Let unvalidated learnings persist indefinitely

### 2. Scope Selection

```python
# Decision tree for scope selection
def select_scope(learning: dict) -> str:
    """Select appropriate scope for a learning."""

    # Check for explicit scope indicators
    if "this project" in learning.get("context", "").lower():
        return "project"

    if "always" in learning.get("context", "").lower():
        return "global"

    # Check for domain indicators
    domain_keywords = {
        "javascript": "javascript",
        "python": "python",
        "marine": "marine-engineering",
        "offshore": "marine-engineering",
        "react": "javascript"
    }

    for keyword, domain in domain_keywords.items():
        if keyword in learning.get("rule", "").lower():
            learning["domain"] = domain
            return "domain"

    # Default to project if uncertain
    return "project"
```

### 3. Conflict Resolution

```yaml
# When learnings conflict
conflict_resolution:
  strategy: "newer_wins" | "higher_confidence" | "ask_user"

  example:
    learning_1:
      rule: "Use 4-space indentation"
      timestamp: "2026-01-10"
      confidence: 0.8

    learning_2:
      rule: "Use 2-space indentation"
      timestamp: "2026-01-17"
      confidence: 0.95

    resolution:
      action: "supersede"
      winner: learning_2
      reason: "Newer with higher confidence"

  notification:
    message: "Superseded learning: 'Use 4-space indentation' replaced by 'Use 2-space indentation'"
```

### 4. Privacy Considerations

```yaml
# Privacy rules
privacy:
  never_capture:
    - passwords
    - api_keys
    - personal_identifiable_information
    - financial_data
    - credentials

  sanitize:
    - file_paths: "Replace with placeholders"
    - user_names: "Anonymize"
    - project_names: "Use generic references unless essential"

  retention:
    validated_learnings: "indefinite"
    unvalidated_learnings: "90 days"
    session_data: "end of session"
```

### 5. Maintenance

```bash
# Regular maintenance tasks

# 1. Review unvalidated learnings
cat ~/.claude/memory/global_learnings.yaml | grep "validated: false"

# 2. Check for conflicting learnings
/claude-reflection --check-conflicts

# 3. Prune unused learnings (>6 months, <3 applications)
/claude-reflection --prune --dry-run

# 4. Export learnings for backup
/claude-reflection --export > ~/claude-learnings-backup-$(date +%Y%m%d).yaml

# 5. Sync domain learnings across projects
/claude-reflection --sync-domains
```

## Troubleshooting

### Learnings Not Being Applied

**Symptom:** Claude doesn't seem to remember previous corrections

**Check:**
```bash
# 1. Verify learnings exist
cat ~/.claude/memory/global_learnings.yaml

# 2. Check if learning is validated
grep -A5 "rule: 'your expected rule'" ~/.claude/memory/global_learnings.yaml

# 3. Verify confidence threshold
# Learnings with confidence < 0.5 may not be applied
```

**Solution:**
- Manually validate the learning
- Increase confidence by repeating the preference
- Check for conflicting learnings

### Conflicting Learnings

**Symptom:** Claude applies inconsistent rules

**Check:**
```bash
# Find potential conflicts
/claude-reflection --check-conflicts

# Example output:
# CONFLICT DETECTED:
#   Learning 1: "Use 4-space indentation" (global, conf: 0.8)
#   Learning 2: "Use 2-space indentation" (project, conf: 0.9)
#   Resolution: Project scope takes precedence
```

**Solution:**
- Review and remove outdated learnings
- Set appropriate scopes
- Explicitly confirm the correct preference

### Memory Files Corrupted

**Symptom:** YAML parsing errors

**Check:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('~/.claude/memory/global_learnings.yaml'))"
```

**Solution:**
```bash
# 1. Backup corrupted file
cp ~/.claude/memory/global_learnings.yaml ~/.claude/memory/global_learnings.yaml.bak

# 2. Restore from last good backup or reset
/claude-reflection --reset-memory --scope global
```

### Too Many Low-Quality Learnings

**Symptom:** Memory files bloated with unvalidated learnings

**Solution:**
```bash
# Prune learnings that:
# - Have never been applied
# - Are older than 90 days
# - Have confidence < 0.5

/claude-reflection --prune --criteria "times_applied=0,age>90d,confidence<0.5"
```

## Execution Checklist

**On Trigger Detection:**
- [ ] Identify trigger type (correction/preference/pattern)
- [ ] Extract relevant information
- [ ] Classify category
- [ ] Determine appropriate scope
- [ ] Check for existing similar learnings
- [ ] Handle conflicts if any
- [ ] Store with appropriate confidence
- [ ] Log for session summary

**At Session End:**
- [ ] Generate session summary
- [ ] Review captured learnings
- [ ] Flag any for user confirmation
- [ ] Update confidence scores
- [ ] Sync to storage

**Periodic Maintenance:**
- [ ] Validate pending learnings
- [ ] Prune stale learnings
- [ ] Check for conflicts
- [ ] Backup memory files
- [ ] Review automation candidates

## Related Skills

- [skill-learner](../skill-learner/SKILL.md) - Creates skills from patterns
- [repo-readiness](../repo-readiness/SKILL.md) - Loads project context
- [session-start-routine](../../meta/session-start-routine/SKILL.md) - Session initialization

## References

- [Memory Management Best Practices](../../../docs/modules/ai/MEMORY_MANAGEMENT.md)
- [Learning Framework](../../../docs/modules/ai/LEARNING_FRAMEWORK.md)
- [YAML Configuration Standards](../yaml-configuration/SKILL.md)

---

## Version History

- **1.0.0** (2026-01-17): Initial release - comprehensive meta-skill for self-improvement with Reflect-Abstract-Generalize-Store loop, multi-scope storage (global/domain/project/session), correction detection, preference capture, pattern extraction, cross-session learning, YAML persistence, validation framework, conflict resolution, and integration with progress tracking system
