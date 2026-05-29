---
name: novel-truncator
description: Intelligently truncate text while preserving content integrity. Suitable for novel text preprocessing, ensuring text does not exceed specified length limits
category: novel-screening
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: Gong Fan
allowed-tools: []
model: opus
changelog:
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Optimized description field to be more concise and comply with imperative language standards
      - type: improved
        content: Optimized descriptions for functionality, usage scenarios, truncation principles, input requirements, and output format to comply with imperative language standards
      - type: added
        content: Added constraints, examples, and detailed documentation sections
      - type: changed
        content: Changed model to opus
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: Restructured according to Agent Skills official specifications
      - type: improved
        content: Optimized description, used imperative language, streamlined main content
      - type: added
        content: Added license and compatibility optional fields
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Text Truncator Tool (Novel Edition)

## Functionality

Receive text content and maximum length limit, intelligently truncate text while preserving content integrity.

## Usage Scenarios

- Preprocess long novel text to meet length limits
- Extract text segments without compromising semantic integrity
- Ensure text input to other agents does not exceed their processing capacity

## Truncation Principles

1. **Prioritize Sentence Endings**: Break at periods, question marks, exclamation points
2. **Next Paragraph Endings**: Break at spaces, line breaks
3. **Finally Specified Length**: Ensure not exceeding set maximum length limit

## Input Requirements

- **Text Content**: Original text to be truncated (string)
- **Maximum Length Limit**: Target maximum character count for text (integer)
- **Truncation Marker** (optional): String to identify text truncation location, such as "[...]"

## Output Format

```
[Text Truncation Report]

Original Length: [character count]
Truncated Length: [character count]
Truncation Position: [position description, such as: at period in sentence X]

Truncated Text:
[text content]
```

## Constraints

- Truncation process should maximally preserve original text's semantic and contextual integrity
- Strictly adhere to maximum length limit
- Avoid truncating in the middle of words

## Examples

See `{baseDir}/references/examples.md` for more detailed examples:
- `examples.md` - Contains detailed examples for different truncation scenarios (by sentence, by paragraph, forced truncation)

## Detailed Documentation

See `{baseDir}/references/examples.md` for detailed guidance and cases on the text truncator tool.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field; optimized descriptions for functionality, usage scenarios, truncation principles, input requirements, and output format; added constraints, examples, and detailed documentation sections; changed model to opus |
| 2.0.0 | 2026-01-11 | Restructured according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
