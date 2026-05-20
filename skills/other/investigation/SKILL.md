---
name: investigation
description: Deep-dive investigation with documentation output.
---

# Investigation

Conducts deep-dive investigations on specific topics and produces detailed documentation.

## Requirements

- Active session must exist (session path in working memory)
- If no active session: **STOP and ask user** for session path

## Execution

**Session path:** [SESSION_PATH from working memory]
**Topic:** $ARGUMENTS

### Steps

1. **Investigate thoroughly:**
   - Check project docs folder for related documents (if exists)
   - Explore the codebase to understand the topic
   - Identify key files, patterns, dependencies
   - Note potential issues or concerns

2. **Create documentation:**
   - File: `[SESSION_PATH]/[TIMESTAMP_FILE]-dive-[topic-slug].md`

   Structure:
   ```markdown
   # Deep Dive: [topic]
   Date: [TIMESTAMP_LOG]

   ## Summary
   [Brief overview of findings]

   ## Key Findings
   [Bullet points]

   ## Code Structure
   [Relevant files with brief explanations]

   ## Dependencies & Relationships
   [How components interact]

   ## Considerations
   [Issues, edge cases, concerns]

   ## Recommendations
   [Suggested next steps]
   ```

3. **Update session:**
   - Edit `[SESSION_PATH]/_overview.md`:
     - Add to Flow Log: `- [TIMESTAMP_ITERATION] Deep dive: [topic] -> [filename].md`
     - Add to Files: `- [filename].md - Deep dive: [topic]`
   - Commit (if git repo): `cd [SESSION_DIR] && git add . && git commit -m "Deep dive: [topic]"`

4. **Report back:** Provide concise summary of key findings with filename
