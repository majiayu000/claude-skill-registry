---
name: gemini-specialist
description: Use Gemini CLI for massive context tasks (1M-2M tokens). Orchestrator evaluates safety and directs usage patterns intelligently.
version: 1.0.0
---

# Gemini Specialist - Orchestrated Integration

Delegate heavy-lifting tasks to Gemini CLI while maintaining safety through intelligent direction.

## Workflow

1. **Evaluate operation**:
   - File criticality (configs, core logic, data)?
   - Git status (clean, uncommitted changes)?
   - Operation type (analysis, generation, modification)?

2. **Choose pattern**:
   - **Low risk** (analysis, new files): Direct execution
   - **Medium risk** (refactoring, critical files): Temp-first review
   - **High risk** (data files, configs): Git commit + temp-first

3. **Structure prompt**:
   - Be specific (bounded scope = predictable output)
   - State constraints ("preserve all function signatures")
   - Define output format ("complete file" vs "suggestions only")

4. **Execute with safety**:
   ```bash
   # Pattern 1: Direct (low risk)
   gemini -p "prompt" < input.txt --yolo -o text > output.txt

   # Pattern 2: Temp-first (medium risk)
   gemini -p "prompt" < critical.py --yolo -o text > /tmp/gemini-out.py
   # Validate, then apply if good

   # Pattern 3: Git safety net (high risk)
   git add . && git commit -m "pre-gemini backup"
   gemini -p "prompt" --yolo -o text < file > file
   # If bad: git restore file
   ```

5. **Validate output**:
   - Check file integrity (not corrupted, valid syntax)
   - Verify scope (did it modify only what was asked?)
   - Compare if needed (`diff` old vs new)

6. **Report unexpected behavior** to user

## When to Use

- **Large codebase analysis** (>100k tokens)
- **Documentation review** (100+ files)
- **Cross-validation** (second opinion on critical decisions)
- **Architecture planning** (high-level design with massive context)
- **Real-time research** (Google Search grounding)

## Gemini Capabilities

- Context: 1M-2M tokens (5-10x Claude)
- Search: Built-in Google Search grounding
- Speed: Fast analysis, slower implementation
- Cost: Free tier (1000 requests/day)

## Key Principle

**Direction > Prohibition.** Evaluate risk, choose pattern, structure prompts. Trust Gemini with proper guidance and safety nets.

---

See EXAMPLES.md for practical workflows and PATTERNS.md for detailed safety strategies.
