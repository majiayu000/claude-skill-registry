---
name: explain
description: Explain data flows, features, and code paths in the varun.surf application with visual diagrams and step-by-step breakdowns
---

# Explain Skill

Explain how data flows through the system, how features work, and trace code paths with clear visualizations and step-by-step breakdowns.

## Instructions

When the user asks to explain something (a feature, data flow, or component), follow this process:

### 1. Identify What to Explain

Parse the user's request to determine:
- **Data flow**: How data moves from source to destination (e.g., "explain how forecasts get to the frontend")
- **Feature**: How a specific feature works end-to-end (e.g., "explain favorites system")
- **Component**: How a specific service or class works internally (e.g., "explain AggregatorService")
- **Integration**: How external APIs are integrated (e.g., "explain Windguru integration")

### 2. Gather Context

Use the following tools to understand the code:
- `Glob` to find relevant files
- `Grep` to search for specific patterns, method calls, and references
- `Read` to examine source code
- `LSP` for finding definitions, references, and call hierarchies

### 3. Trace the Flow

For data flows and features, trace the complete path:

```
Entry Point → Processing Steps → Output
```

Identify:
- Entry points (API endpoints, scheduled tasks, user actions)
- Service layer processing
- Data transformations
- External API calls
- Caching layers
- Response formatting

### 4. Create Visual Diagrams

Use ASCII diagrams to visualize:

**For data flows:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Source    │────▶│  Transform  │────▶│ Destination │
└─────────────┘     └─────────────┘     └─────────────┘
```

**For component interactions:**
```
            ┌──────────────────┐
            │   Controller     │
            └────────┬─────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Service A│  │Service B│  │Service C│
   └─────────┘  └─────────┘  └─────────┘
```

**For state transitions:**
```
[State A] ──(action)──▶ [State B] ──(action)──▶ [State C]
```

### 5. Provide Step-by-Step Breakdown

Structure the explanation as:

1. **Overview**: High-level summary (2-3 sentences)
2. **Entry Point**: Where the flow begins
3. **Step-by-Step Flow**: Each processing step with file:line references
4. **Key Code Snippets**: Important code sections (keep concise)
5. **Data Transformations**: How data shape changes
6. **External Dependencies**: APIs, databases, caches involved
7. **Error Handling**: How errors are managed
8. **Related Components**: Other parts of the system that interact

### 6. Include Code References

Always include file paths with line numbers for easy navigation:
- `src/main/java/.../SpotsController.java:45` - endpoint definition
- `src/main/java/.../AggregatorService.java:120` - data aggregation

## Output Format

```markdown
# Explaining: [Topic]

## Overview
[2-3 sentence summary]

## Visual Diagram
[ASCII diagram showing the flow]

## Step-by-Step Flow

### 1. [Step Name]
**File**: `path/to/file.java:line`

[Description of what happens]

```java
// Key code snippet (if helpful)
```

### 2. [Next Step]
...

## Data Transformations
| Stage | Data Shape | Example |
|-------|------------|---------|
| Input | Type       | {...}   |
| Output| Type       | {...}   |

## Key Files Involved
- `path/to/file1.java` - [purpose]
- `path/to/file2.java` - [purpose]

## Related Features
- [Feature 1]: [brief relation]
- [Feature 2]: [brief relation]
```

## Example Topics

Common explanations users might request:

### Data Flows
- "How do forecasts get from Windguru to the frontend?"
- "How are live conditions fetched and displayed?"
- "How does the caching system work?"
- "How does the spot data flow from JSON to API response?"

### Features
- "How does the favorites system work?"
- "How does country filtering work?"
- "How does the search functionality work?"
- "How does theme switching work?"
- "How does the kite size calculator work?"

### Components
- "How does AggregatorService orchestrate data fetching?"
- "How do the FetchCurrentConditionsStrategy implementations work?"
- "How does the ForecastService parse Windguru data?"
- "How does the frontend manage state?"

### Integrations
- "How is Windguru integrated?"
- "How is Google Maps integration working?"
- "How does the AI analysis feature work?"

## Notes

- Keep explanations concise but complete
- Use diagrams to make complex flows understandable
- Always include file:line references for code navigation
- Focus on the specific topic, don't over-explain tangential concerns
- If the topic is ambiguous, ask clarifying questions
- Reference CLAUDE.md, docs/BACKEND.md, and docs/FRONTEND.md for architectural context
