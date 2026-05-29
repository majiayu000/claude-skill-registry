---
name: self-learning
version: 1.0
last_updated: 2025-10-23
description: Automatic self-learning system that captures user feedback and updates project rules in real-time
license: MIT
priority: highest
triggers:
  - User feedback patterns ("too long", "too many duplicates", "slow")
  - Performance issues (5+ min response time)
  - User corrections ("not what I asked", "do it again")
dependencies:
  - none (standalone)
compatibility:
  - claude-code: ">=1.0"
  - CLAUDE.md: ">=2.0"
changelog:
  - 1.0 (2025-10-23): Initial release with real-time CLAUDE.md updates
---

# 🧠 Self-Learning SKILL

## Purpose

Automatically detect user feedback patterns and update CLAUDE.md / SKILL files in real-time to prevent recurring issues.

---

## Auto-Trigger Conditions

**Activate when user says:**
- "too long" / "too verbose"
- "too many duplicates" / "repetitive"
- "slow" / "takes too long"
- "not what I asked" / "wrong"
- "do it again" / "try again"
- "improve this" / "make it better"

**Activate when detecting:**
- Response time > 5 minutes
- Response length > 300 lines (without user request for detail)
- Same content repeated 2+ times in single response
- User explicitly asks for rule updates

---

## Learning Process (4 Steps)

### Step 1: Detect Feedback Pattern

🚨 **SPECIAL CASE: Multi-AI Workflow Language Violation (CRITICAL)**

**Auto-detect when user says:**
- "Why English response?" / "Answer in my language"
- "This is in English" / "Wrong language"
- "Review is in English"
- "Why send raw output from other AI?"

**Auto-classification:**
```typescript
{
  issue_type: "language_violation",
  severity: "critical",
  specific_complaint: "Multi-AI Workflow Step 4 bypassed language translation",
  affected_area: "multi-ai-workflow",
  target_file: ".skills/multi-ai-workflow-SKILL.md",
  target_section: "Step 4: Claude - Final Synthesis Report"
}
```

**Immediate Action (Auto-triggered):**
1. ✅ Detect: Multi-AI Step 4 sent wrong language to user
2. ✅ Generate rule: Add "Language Output Enforcement Checklist" to Step 4
3. ✅ Update: `.skills/multi-ai-workflow-SKILL.md` (Step 4 section)
4. ✅ Update: `CLAUDE.md` behavioral_rules (add rule)
5. ✅ Notify user: "✅ Language output enforcement rule added - recurrence prevented"

---

**General Pattern Analysis:**

**Analyze user message for:**
```typescript
{
  issue_type: "efficiency" | "quality" | "accuracy" | "format" | "language_violation",
  severity: "low" | "medium" | "high" | "critical",
  specific_complaint: string,
  affected_area: "response_length" | "duplicates" | "speed" | "format" | "accuracy" | "multi-ai-workflow"
}
```

**Examples:**
```
User: "too long, took 5+ minutes"
→ Issue: efficiency
→ Severity: high
→ Complaint: "response took 5+ minutes"
→ Area: response_length + speed

User: "same content repeated 3 times"
→ Issue: quality
→ Severity: critical
→ Complaint: "duplicate content"
→ Area: duplicates

User: "why is the review in English?"
→ Issue: language_violation
→ Severity: critical
→ Complaint: "Multi-AI Step 4 English output to non-English user"
→ Area: multi-ai-workflow
→ Auto-fix: Add Language Output Enforcement Checklist

User: "I didn't do this" / "this is from another session"
→ Issue: multi_session_conflict
→ Severity: medium
→ Complaint: "Git commit included other session's work"
→ Area: git-workflow
→ Auto-fix: Adjust multi-session threshold (30min → Xmin)
```

---

### Step 2: Generate Improvement Rule

⚠️ **LANGUAGE RULE: Match User's Language**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**If user communicates in language X, ALL outputs MUST be in language X:**
- ✅ Self-learning rule summaries → User's language
- ✅ Problem descriptions → User's language
- ✅ Recommendations → User's language
- ✅ File update notifications → User's language

**ONLY keep English for:**
- File names (`CLAUDE.md`, `.skills/example-SKILL.md`)
- Code snippets (`interface BuilderState`)
- Technical terms with no translation equivalent

**Template:**
```markdown
## [Issue Type] - [Date]

**Problem:**
[User's complaint in 1-2 sentences - IN USER'S LANGUAGE]

**Root Cause:**
[Why it happened - specific behavior/pattern - IN USER'S LANGUAGE]

**New Rule:**
[Actionable rule to prevent recurrence - IN USER'S LANGUAGE]

**Example:**
Before: [Bad example - IN USER'S LANGUAGE]
After: [Good example - IN USER'S LANGUAGE]

**Priority:** [low/medium/high/critical]
```

**Real Example (2025-10-23):**
```markdown
## Efficiency - 2025-10-23

**Problem:**
User requested simple summary, received 600+ line response in 5+ minutes

**Root Cause:**
- No duplicate detection
- No length limit enforcement
- Auto-generated detailed docs without request

**New Rule:**
- HIGHEST PRIORITY: No duplicate explanations (same content only once)
- Response length: 20-300 lines based on request type
- Detailed docs only when user explicitly asks

**Example:**
Before:
- 600+ lines
- Same explanation 5 times
- Auto-generated comprehensive summary

After:
- 50 lines
- Each topic mentioned once
- Summary only, detailed docs on request

**Priority:** critical
```

---

### Step 3: Update CLAUDE.md or Create SKILL

**Decision Matrix:**

| Issue Type | Applies to All Tasks? | Action |
|-----------|----------------------|---------|
| Efficiency (response length, duplicates) | ✅ Yes | Update CLAUDE.md `<behavioral_rules>` |
| Specific workflow (errors, specialized tools) | ❌ No | Update relevant SKILL file |
| New capability needed | ❌ No | Create new SKILL file |
| Format/structure | ✅ Yes | Update CLAUDE.md Response Protocol |

**Where to Update:**

1. **Universal Rules → CLAUDE.md**
   - Location: `<behavioral_rules>` section
   - Add new rule with clear description
   - Update Response Protocol section

2. **Workflow-Specific → .skills/*.md**
   - collaboration: Collaboration-specific improvements
   - multi-ai-workflow: Multi-model collaboration improvements
   - error-recovery: Error handling improvements

3. **New Capability → New SKILL**
   - Create `.skills/[name]-SKILL.md`
   - Follow SKILL template format
   - Add to auto-trigger conditions

---

### Step 4: Verify & Inform User

**Output Format:**
```markdown
✅ Self-Learning Applied

**Issue Detected:**
[User's complaint]

**Rule Added:**
[New rule in 1-2 sentences]

**Updated Files:**
- CLAUDE.md: Line X (behavioral_rules)
- CLAUDE.md: Lines Y-Z (Response Protocol)

**Effective Immediately:**
All future responses will follow this rule.

**Test:**
[Show how next response will be different]
```

**Example:**
```markdown
✅ Self-Learning Applied

**Issue Detected:**
Response too long (600+ lines) with duplicates, took 5+ minutes

**Rules Added:**
1. No duplicate explanations (HIGHEST PRIORITY)
2. Response length: 20-300 lines based on request type
3. Detailed docs only when explicitly requested

**Updated Files:**
- CLAUDE.md: Lines 7-17 (added rules)
- CLAUDE.md: Lines 30-72 (Response Efficiency Rules)

**Effective Immediately:**
Next responses will be 50-150 lines, no duplicates.

**Test:**
If you ask for a summary now → 30-50 lines, each topic once, no auto-docs.
```

---

## Learning Categories & Examples

### Category 1: Efficiency Issues

**Triggers:**
- "too long", "takes too long", "slow"

**Common Problems:**
- Response > 300 lines
- Time > 5 minutes
- Duplicate explanations

**Auto-Fix:**
```markdown
Rule: Response length limits
- Simple: 20-50 lines
- Medium: 50-150 lines
- Complex: 100-200 lines
- Large refactor: 200-300 lines

Rule: No duplicates
- Each concept mentioned exactly once
- No repeated code examples
- No redundant explanations
```

---

### Category 2: Quality Issues

**Triggers:**
- "too many duplicates", "same content", "repeated"

**Common Problems:**
- Same explanation in multiple sections
- Repeated code examples
- Redundant summaries

**Auto-Fix:**
```markdown
Rule: Duplicate Detection
Before sending response:
1. List all topics covered
2. Check if any topic appears 2+ times
3. If yes, consolidate to single mention
4. Remove redundant sections
```

---

### Category 3: Format Issues

**Triggers:**
- "no boxes", "keep it simple", "format too complex"

**Common Problems:**
- Over-complicated diagrams
- Excessive markdown formatting
- Nested tables/boxes

**Auto-Fix:**
```markdown
Rule: Simple Format
✅ Use:
- Simple bullet points
- Plain lists
- File:line format

❌ Avoid:
- Box-drawing characters (┌┐└┘├┤)
- Nested tables
- Complex diagrams (unless requested)
```

---

### Category 4: Accuracy Issues

**Triggers:**
- "not what I asked", "wrong", "check again"

**Common Problems:**
- Wrong file paths
- Incorrect line numbers
- Misunderstood requirements

**Auto-Fix:**
```markdown
Rule: Verification Before Response
1. Read actual files (don't assume)
2. Verify line numbers with Read tool
3. Confirm understanding with user if unclear
4. Show evidence (file paths, line numbers)
```

---

### Category 5: Plan Mode Transparency

**Triggers:**
- "Did [AI tool] participate?"
- "Did you call [external API]?"
- "Why use Sub Agent?"
- "Didn't check Plan Mode"
- "Should have told me beforehand"

**Common Problems:**
- Multi-AI (external API) requested in Plan Mode → Silent fallback to Sub Agent
- No notification BEFORE API call blocked
- User discovers fallback AFTER completion
- Quality downgrade (100% → 85-90%) without user approval
- Policy changes (policy_score ≥ 5.0) processed without validation

**Solution Protocol:**

1. **Detect BEFORE execution:**
   ```python
   if plan_mode_active and external_api_requested:
       STOP_IMMEDIATELY()
       CALCULATE_POLICY_SCORE()  # if policy files involved
       NOTIFY_USER()
       WAIT_FOR_CHOICE()
   ```

2. **Show full notification:**
   ```
   ⚠️ PLAN MODE CONSTRAINT DETECTED

   Your request: [External API] collaboration
   Current context: Plan Mode (analysis-only)

   CONSTRAINT:
   - External API: ❌ BLOCKED

   FALLBACK:
   - Sub Agent: ✅ ALLOWED
   - Quality: 85-90% (vs 100%)

   ${policy_score ≥ 5.0 ? 'POLICY DESIGN: External API preferred' : ''}

   OPTIONS:
   A. Sub Agent (proceed now, 85-90%)
   B. Exit Plan Mode → Use requested tool (100%)
   ```

3. **Wait for user choice:**
   - Option A: Proceed with Sub Agent (user accepted quality trade-off)
   - Option B: HALT execution, instruct user to exit Plan Mode

**Auto-Update Rules:**

| Trigger Pattern | Update Location | New Rule |
|----------------|-----------------|----------|
| "Did tool participate?" | CLAUDE.md Self-Check | Add Plan Mode detection step |
| "Did you call API?" | collaboration SKILL | Add notification BEFORE API call |
| "Why Sub Agent?" | multi-ai-workflow | Add quality comparison table |
| "Didn't check Plan Mode" | ALL SKILL files | Add Plan Mode constraint sections |

---

### Category 6: Multi-Session Git Conflicts

**Triggers:**
- "I didn't do this"
- "This is from another session"
- "Why is this file committed?"
- "30min threshold too short"
- "Files from 2 hours ago are also mine"

**Common Problems:**
- Multi-Session Detection threshold too strict (30min)
- User takes long break → files marked as "other session"
- User works continuously → 30min threshold correct

**Learning Actions:**

1. **Detect Pattern:**
   ```typescript
   {
     issue_type: "multi_session_conflict",
     severity: "medium",
     complaint: "30min threshold too short / files from 2 hours ago are mine",
     affected_area: "git-workflow"
   }
   ```

2. **Analyze User Workflow:**
   ```
   Scenario A: User takes 1-2 hour breaks
   → 30min threshold too strict
   → Suggest: Increase to 2 hours

   Scenario B: User switches sessions rapidly
   → 30min threshold too loose
   → Suggest: Decrease to 15 minutes
   ```

3. **Generate Adjustment Rule:**
   ```markdown
   ✅ Self-Learning: Git Workflow Threshold Adjustment

   **User Pattern Detected:**
   - Average break time: 1-2 hours
   - Work session length: 30min-2 hours
   - Session switching frequency: Low

   **Current Threshold:** 30min (too short)
   **Suggested Threshold:** 2 hours (1800s → 7200s)

   **Updated Files:**
   .skills/git-workflow/SKILL.md
   - Line 143: THRESHOLD=1800 → THRESHOLD=7200

   **Effect:**
   - False positive reduction (work within 2 hours classified as "current session")
   - User inconvenience resolved

   **Apply changes?** (yes/no)
   ```

4. **Update SKILL File:**
   ```markdown
   # .skills/git-workflow/SKILL.md update

   Before:
   THRESHOLD=1800  # 30 minutes

   After:
   THRESHOLD=7200  # 2 hours (user feedback: 2025-10-23)
   # Adjusted based on user workflow pattern (long breaks common)
   ```

**Decision Matrix for Threshold Adjustment:**

| User Feedback | Current Threshold | Suggested Threshold | Reasoning |
|---------------|------------------|-------------------|-----------|
| "30min too short" | 30min | 2 hours | User takes long breaks |
| "2hr ago files are mine" | 30min | 4 hours | Very long work sessions |
| "10min ago why other?" | 30min | 15 minutes | Rapid session switching |
| "Just did this why old?" | 30min | 10 minutes | Very active sessions |

**Learning Rate:**
- 1st complaint → Suggest adjustment
- 2nd complaint (same pattern) → Auto-adjust with user confirmation
- 3rd complaint → Consider smart threshold (session gap detection)

---

### Category 7: Session Summary Rule Loss (NEW - 2025-10-24)

**Triggers:**
- "Why English response?" (after continuation session)
- "Rule violation again"
- "Previous session was in [language]"
- "Rules lost during summarization"
- "Context got long and summarization missed our rules"

**Common Problems:**
- Context length exceeds 50K+ tokens → Auto-summary triggered
- Session summary omits behavioral_rules
- Next session violates rules (language, self-check, brevity)
- Summary language ≠ user language → AI follows summary language (wrong)

**Root Cause Analysis (RCA 2025-10-24):**
```
Primary: Session summary generation doesn't reference CLAUDE.md behavioral_rules
Secondary: Self-Check protocol not executed (rule violation)
Tertiary: Over-interpretation of "all"/"complete" (brevity rule violated 10x)
```

**Solution Protocol:**

1. **BEFORE responding to continuation session:**
   ```python
   if session_is_continuation:
       MANDATORY_READ("CLAUDE.md", behavioral_rules_section)
       VERIFY_USER_LANGUAGE()  # English? Other?
       DETECT_LANGUAGE_MISMATCH(summary_lang, user_lang)
       RUN_SELF_CHECK()
       THEN_RESPOND()
   ```

2. **If summary language ≠ user language:**
   ```
   ⚠️ Language mismatch detected
   Summary: English
   User message: [Other language]

   → OVERRIDE: Switch to user's language (Rule)
   → IGNORE summary language
   → USE user message language
   ```

3. **Response length pre-check:**
   ```python
   if estimated_response_length > 300 lines:
       ASK_USER("Create detailed docs in separate file?")
       WAIT_FOR_CONFIRMATION()

   # Prevent over-interpretation
   if user_says("all", "complete", "everything"):
       interpret_as = "complete list (200-300 line summary)"
       NOT_interpret_as = "detailed expansion of all items (2,000+ lines)"
   ```

**Auto-Update Rules:**

| Trigger Pattern | Update Location | New Rule |
|----------------|-----------------|----------|
| "Why wrong language?" (continuation) | CLAUDE.md | Add session summary requirements rule |
| "Rule violation" | CLAUDE.md Self-Check | Add session type check in Self-Check |
| "Rules lost in summary" | CLAUDE.md Self-Check | Add continuation session detection protocol |
| "Too long" (300+ lines) | CLAUDE.md | Add response length pre-check |

**Prevention Checklist:**

```markdown
✅ Continuation Session Detection
- [ ] Detected session type (New / Continuation)
- [ ] If Continuation: Re-read behavioral_rules
- [ ] Verified user language
- [ ] Checked summary language vs user language
- [ ] Override if mismatch detected

✅ Response Length Pre-Check
- [ ] Estimated response length: [X] lines
- [ ] If 300+: Asked user for confirmation first
- [ ] Interpreted "all/complete" correctly (complete list, NOT detailed expansion)

✅ Self-Check Execution
- [ ] Session Type: [New/Continuation] declared
- [ ] User Language: [Language] declared
- [ ] Rule compliance confirmed
```

---

### Category 8: Database/RLS Debugging Failures (NEW - 2025-10-25)

**Triggers:**
- "Why couldn't [AI] find this?"
- "Deep research step by step"
- "Call expert tool for analysis"
- Database query succeeded but browser shows nothing
- INSERT duplicate key error but SELECT returns 0 rows

**Common Problems (AI Failure Patterns):**
1. **Assumption Trap**
   - Screenshot shows "RLS policy exists" → Assume policy works
   - User says "ran query" → Trust it was executed
   - See symptoms, guess causes (env vars, cache, errors)

2. **Symptom vs Root Cause Confusion**
   - Blog not showing → env vars? → errors? → cache?
   - Cycle through symptoms instead of finding root cause

3. **Contradiction Detection Failure**
   - Signal A: `SELECT blog_authors` → 0 rows
   - Signal B: `INSERT blog_authors` → "duplicate key exists"
   - **Contradiction (A+B = Row exists BUT cannot be read)**
   - AI: Analyze each signal individually (miss contradiction)

4. **UI vs Actual Behavior Verification Lacking**
   - Supabase Dashboard: "Enable read access for all users" policy visible
   - Actual query: `SELECT COUNT(*) FROM v_published_posts` → 0
   - UI ≠ actual behavior (verification needed)

**Expert Tool Success Pattern:**

1. **Step-by-Step Data Flow Tracking**
   ```
   Step 1: .env.local loaded? ✅ Confirmed
   Step 2: Supabase connection success? ✅ Confirmed
   Step 3: blog_posts 36 items? ✅ Confirmed
   Step 4: blog_authors 1 item? ❌ 0 found
   Step 5: INSERT vs SELECT contradiction? ✅ Contradiction found
   Step 6: RLS SELECT policy failure? ✅ ROOT CAUSE
   ```

2. **Contradiction Detection**
   ```typescript
   // Test: blog_authors SELECT
   Result: 0 rows  // ← Signal A

   // User: Executed INSERT
   Error: "duplicate key (id)=(...) already exists"  // ← Signal B

   // Analysis
   if (Signal A == 0 && Signal B == "duplicate") {
     CONTRADICTION_DETECTED = true
     ROOT_CAUSE = "RLS SELECT policy blocks reads BUT row exists"
   }
   ```

3. **Verify UI with Actual Queries**
   ```sql
   -- UI says: "Enable read access policy exists"
   -- Verify with actual query:
   SET ROLE anon;
   SELECT COUNT(*) FROM blog_authors;
   -- Result: 0 (POLICY NOT WORKING)
   ```

**Solution Protocol:**

**Phase 1: Systematic Data Flow Tracking (7 Steps)**
```markdown
Step 1: Environment variable load confirmation
  → .env.local file exists?
  → Logs show "Reload env"?

Step 2: Database connection test
  → createClient() success?
  → Simple query (SELECT 1) works?

Step 3: Base table data confirmation
  → blog_posts 36 published?
  → author_id matching blog_authors exist?

Step 4: JOIN tables individual test
  → blog_authors: X items
  → blog_categories: Y items
  → blog_seo_metadata: Z items
  → Which table has 0? (JOIN failure cause)

Step 5: INSERT vs SELECT contradiction test
  → INSERT attempt → duplicate key?
  → SELECT execution → 0 rows?
  → Contradiction found? → RLS SELECT policy issue

Step 6: RLS policy actual behavior verification
  → SET ROLE anon;
  → SELECT COUNT(*) FROM [table];
  → If 0, policy failure confirmed

Step 7: Policy recreation + verification
  → DROP POLICY + CREATE POLICY
  → SET ROLE anon; SELECT COUNT(*);
  → Data returned confirmed
```

**Phase 2: Contradiction Detection Automation**
```typescript
interface QueryResult {
  select_count: number
  insert_error: string | null
}

function detectContradiction(result: QueryResult): boolean {
  // Pattern 1: SELECT 0 BUT INSERT duplicate
  if (result.select_count === 0 && result.insert_error?.includes("duplicate key")) {
    return true  // RLS SELECT policy blocks reads
  }

  // Pattern 2: View 0 BUT base table has data
  const viewCount = await query("SELECT COUNT(*) FROM v_published_posts")
  const tableCount = await query("SELECT COUNT(*) FROM blog_posts WHERE status='published'")
  if (viewCount === 0 && tableCount > 0) {
    return true  // View JOIN fails or RLS blocks view
  }

  return false
}
```

**Phase 3: UI vs Actual Behavior Verification**
```markdown
For Database Issues (Supabase, PostgreSQL, RLS):

❌ NEVER trust:
- Dashboard screenshots ("policy exists")
- User claims ("ran query")
- UI indicators (green checkmarks)

✅ ALWAYS verify:
- Run actual SQL query (SELECT COUNT(*))
- Test with role switching (SET ROLE anon)
- Check query results, not UI
- Validate INSERT vs SELECT consistency
```

**Prevention Checklist:**

```markdown
✅ Database/RLS Debugging Protocol
- [ ] Step 1-7 sequential execution (no skips)
- [ ] Each step verified with actual query (no UI trust)
- [ ] INSERT vs SELECT result comparison (contradiction detection)
- [ ] SET ROLE anon test (RLS policy actual behavior confirmation)
- [ ] UI display ≠ actual behavior assumption (Always verify)

✅ Contradiction Detection
- [ ] Signal A (SELECT result) recorded
- [ ] Signal B (INSERT/UPDATE error) recorded
- [ ] A + B contradiction check
- [ ] If contradiction → suspect RLS/permission issue

✅ Never Trust, Always Verify
- [ ] Dashboard screenshots → Re-run actual query
- [ ] User "ran query" → Request SQL log or re-run
- [ ] "Enable read access policy" visible → SET ROLE anon; SELECT test
```

**Real Case Study (2025-10-25):**
```
Problem: Blog posts 36 in DB but browser shows "No published blog posts yet"
Basic AI Attempts: Env vars, errors, cache, multiple attempts (90min)
Expert Tool: Step-by-Step tracking → Step 4 found blog_authors 0 → Step 5 found contradiction → RLS SELECT policy failure confirmed (15min)
Result: DROP POLICY + CREATE POLICY → Immediately resolved
Lesson: Systematic tracking + contradiction detection + actual verification = 6x faster resolution
```

---

## Integration with Existing SKILLs

### With collaboration-SKILL

```markdown
If external collaboration response is too long:
  → Apply self-learning rules
  → Update collaboration SKILL with length limits
  → Add "concise prompt" templates
```

### With multi-ai-workflow-SKILL

```markdown
If workflow explanations have duplicates:
  → Consolidate workflow steps
  → Remove redundant model comparisons
  → Single workflow diagram only
```

### With error-recovery-SKILL

```markdown
If error recovery docs are verbose:
  → Compress to decision table only
  → Examples only when user asks
  → Reference full docs, don't repeat
```

---

## Success Metrics

**Track improvements:**
```typescript
{
  before: {
    avg_response_time: "5+ min",
    avg_response_length: "600+ lines",
    duplicate_rate: "30-40%",
    user_satisfaction: "6/10"
  },
  after: {
    avg_response_time: "1-3 min",
    avg_response_length: "100-150 lines",
    duplicate_rate: "0%",
    user_satisfaction: "9/10"
  }
}
```

**Goal:**
- 80% reduction in response time
- 70% reduction in length (maintain quality)
- 0% duplicates
- 90%+ user satisfaction

---

## Learning Log

**❌ NO separate log file needed.**

**Why:**
- Learning applied directly to CLAUDE.md
- Git history already tracks all rule changes
- Separate log = unnecessary maintenance burden
- User can see changes via: `git log CLAUDE.md`

**If user needs history:**
```bash
# Show recent CLAUDE.md changes
git log --oneline CLAUDE.md | head -10

# Show specific rule changes
git diff HEAD~1 CLAUDE.md | grep "behavioral_rules" -A 10
```

---

## Emergency Override

**If self-learning rule causes issues:**

```
User: "Previous approach was better, revert it"

AI Action:
1. Read LEARNING_LOG.md
2. Identify last rule change
3. Revert CLAUDE.md / SKILL file
4. Mark in log: Status: ❌ Reverted
5. Ask user: "What was the problem?" (learn why)
```

---

## Implementation Checklist

When self-learning activates:

- [ ] Detect feedback pattern (Step 1)
- [ ] Generate improvement rule (Step 2)
- [ ] Update CLAUDE.md or SKILL (Step 3)
- [ ] Verify changes work (Step 4)
- [ ] Inform user of update
- [ ] Log in LEARNING_LOG.md
- [ ] Apply immediately to current session

**Time Limit:** Self-learning update should take < 1 minute

---

## Examples of Good Self-Learning

### Example 1: Duplicate Detection

**User:** "Same content appeared 3 times"

**AI Self-Learning:**
```
✅ Detected: duplicate_content

Updating CLAUDE.md:
+ Rule: No duplicate explanations (Line 14)
+ Response Protocol: Duplicate check before sending (Line 68)

Applied immediately.
Next response will mention each topic exactly once.
```

---

### Example 2: Response Too Long

**User:** "Summary is 600 lines, too long"

**AI Self-Learning:**
```
✅ Detected: response_length_exceeded

Updating CLAUDE.md:
+ Rule: Response brevity 20-300 lines (Line 15)
+ Response Protocol: Length guidelines (Lines 39-46)

Applied immediately.
Next summary will be 30-50 lines maximum.
```

---

### Example 3: Format Too Complex

**User:** "No box diagrams, keep it simple"

**AI Self-Learning:**
```
✅ Detected: format_complexity

Updating CLAUDE.md:
+ Response Protocol: Simple format rule (Lines 53-65)

Applied immediately.
Next response will use:
- Simple bullet points
- No box-drawing chars
- File:line format only
```

---

## Anti-Patterns (What NOT to Learn)

**❌ Don't create rules for:**

1. **One-time specific requests**
   - "Just this once, make it a PDF" → Don't make "always PDF" rule

2. **Context-specific preferences**
   - "Explain this file in detail" → Don't make "always detailed" rule

3. **Contradictory feedback**
   - User A: "Make it longer" vs User B: "Make it shorter" → Keep balanced approach

4. **Temporary workarounds**
   - "Tool X not working, use Tool Y" → Don't disable Tool X permanently

**✅ Only create rules for:**
- Recurring patterns (2+ occurrences)
- Universal improvements (helps all tasks)
- Clear efficiency gains (measurable)
- User explicitly says "always", "from now on", "every time"

---

## Final Notes

**Self-Learning Philosophy:**
> "Learn from every feedback, but don't over-correct.
> Balance automation with user control.
> Efficiency without sacrificing quality."

**Key Principles:**
1. **Listen First:** Understand user's real complaint
2. **Act Fast:** Update rules within 1 minute
3. **Apply Immediately:** Current session onwards
4. **Measure Impact:** Track improvements
5. **Allow Revert:** User can undo if needed

**Success = Fewer repeated complaints + Faster responses + Higher satisfaction**
