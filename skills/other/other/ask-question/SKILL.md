---
name: ask-question
description: Draft a technical research question and send to ChatGPT for investigation
argument-hint: [draft]
allowed-tools: [Read, Glob, Grep, Bash]
---

Help me draft a technical research question about a problem I've encountered, then send it to ChatGPT for research.

**Arguments:** $ARGUMENTS

- If first word is `draft`: Only write the question file, skip sending to ChatGPT
- Otherwise: Write question, send to ChatGPT, read answer, and discuss

**Key Principle: Curiosity over confidence.** The goal is to get useful research, not to sound smart. Be explicit about what we know vs. what we're guessing. Wrong assumptions waste ChatGPT's reasoning on the wrong problem.

**Process:**

1. **Understand the problem context**
   - If topic provided, research it in the current codebase
   - Look at recent errors, code changes, or discussions in our conversation
   - Identify the specific technical issue (error message, unexpected behavior, architectural question)

2. **Gather environmental context**
   - Check language/framework versions (package.json, build.gradle, pom.xml, MODULE.bazel, etc.)
   - Identify relevant dependencies and their versions
   - Note any monorepo or build system constraints

3. **Create minimal reproduction**
   - Extract the specific code that demonstrates the problem
   - Remove project-specific details that aren't relevant
   - Include configuration files if relevant (application.yml, etc.)

4. **Write the question in a local markdown file**

   **File location:** Write to `/tmp/` using pattern `research-{topic-slug}-question.md` (e.g., `research-bazel-caching-question.md`).

   **Structure the question with these sections:**

   ```markdown
   # [Descriptive title as a question]

   ## Keywords
   `keyword1` `keyword2` `keyword3` (help ChatGPT understand the domain)

   ## Question

   [Opening paragraph: What you're trying to do and what's going wrong]

   ### Environment
   - Language/framework version
   - Relevant library versions
   - Build system (if relevant)
   - OS/platform (if relevant)

   ### Code

   **[File or component name]:**
   ```language
   // Minimal code example
   ```

   **[Config file if relevant]:**
   ```yaml
   # Relevant configuration
   ```

   ### Error/Behavior

   ```
   [Exact error message or description of unexpected behavior]
   ```

   ### What We Know (verified facts)

   - [Fact 1 - how we verified it]
   - [Fact 2 - how we verified it]

   ### What We're Uncertain About

   - [Hypothesis 1 - why we suspect this, confidence level]
   - [Hypothesis 2 - why we suspect this, confidence level]
   - [Gap in understanding - what we haven't checked yet]

   ### Specific Questions

   1. [Specific question 1]
   2. [Specific question 2 - optional]
   3. [Specific question 3 - optional]

   ### Constraints

   [Hard constraints that limit solutions: "must use X", "can't change Y", "monorepo requires Z". Only include real constraints, not preferences.]
   ```

5. **Honesty checklist before finishing**
   - [ ] Title is a specific question (not "Problem with X")
   - [ ] Code is minimal but complete (can be copy-pasted to reproduce)
   - [ ] Error message is exact (not paraphrased)
   - [ ] "What We Know" only contains things we actually verified
   - [ ] "What We're Uncertain About" honestly captures our gaps
   - [ ] No fabricated claims (e.g., "tested on Linux" when we didn't)
   - [ ] Confidence levels are calibrated (don't overstate certainty)
   - [ ] Questions are specific and answerable
   - [ ] No sensitive info (credentials, internal URLs, company names)
   - [ ] Constraints are real constraints, not preferences

**Writing style guidelines:**
- Be concise but complete
- Use "we" (collaborative tone with the user)
- Show the problem, don't just describe it
- Explicitly state what you haven't tested or checked
- Include version numbers - they matter!
- If uncertain about something, say so rather than guessing

6. **Send to ChatGPT (unless draft mode)**

   If $ARGUMENTS starts with `draft`, skip this step - just tell the user where the file was saved.

   Otherwise, send the question to ChatGPT using the ask-question CLI:

   ```bash
   ask-question -f /tmp/research-{topic-slug}-question.md \
                -o /tmp/research-{topic-slug}-answer.md \
                -t 1200000
   ```

   **Important:** Always use a timeout of at least 20 minutes (`-t 1200000`). ChatGPT's "Extended Thinking" mode can take several minutes for complex questions. Never use a shorter timeout.

   After ask-question returns successfully, it will print the answer to stdout, as well as save it to the answer file for future reference. Discuss it with the user. Summarize key insights and recommendations from the response.
