---
name: youtube_moderation_prototype
description: Moderate YouTube live chat by detecting spam, toxic content, and enforcing rate limits. PROTOTYPE for testing pattern fidelity before deploying to native Qwen/Gemma.
version: 1.0_prototype
author: 0102_test_harness
created: 2025-10-20
agents: [qwen, gemma]
primary_agent: gemma
trigger_keywords: [moderate, spam, toxic, chat, filter, block]
pattern_fidelity_threshold: 0.90
test_status: prototype
---

# YouTube Chat Moderation Skill (PROTOTYPE)

**Purpose**: Validate this skill pattern with 0102 (Claude Code) before deploying to native Qwen/Gemma environment.

**Test Plan**: 0102 executes 50 benchmark tasks manually, validates ≥90% success rate.

---

## Task

Moderate incoming YouTube live chat messages to maintain positive community environment.

## Instructions (For 0102 Validation)

### 1. CAPS SPAM CHECK
**Rule**: IF message.length > 20 AND uppercase_ratio > 0.80 → BLOCK

**Expected Pattern**: caps_check_executed=True

**Validation**:
- Count characters in message
- Calculate uppercase_ratio = (uppercase_count / total_length)
- If both conditions met → decision="block", reason="caps_spam"
- Log: `{"pattern": "caps_check_executed", "value": true, "decision": "block"}`

**Examples**:
- ✅ "VISIT MY CHANNEL FOR FREE MONEY!!!!!!" → BLOCK (length=38, uppercase=100%)
- ✅ "CHECK OUT MY STREAM NOW!!!!!" → BLOCK (length=29, uppercase=96%)
- ❌ "Great stream!" → ALLOW (length=13, too short)
- ❌ "This is AMAZING content" → ALLOW (uppercase=38%, below threshold)

---

### 2. REPETITION CHECK
**Rule**: IF message appears in recent_history (last 100 messages) AND count >= 3 → BLOCK

**Expected Pattern**: repetition_check_executed=True

**Validation**:
- Search last 100 messages for exact match
- Count occurrences of current message
- If count >= 3 → decision="block", reason="repetition"
- Log: `{"pattern": "repetition_check_executed", "value": true, "matches_found": N}`

**Examples**:
- ✅ "Follow me!" (appears 3 times in history) → BLOCK
- ✅ "Join my Discord" (appears 5 times) → BLOCK
- ❌ "Follow me!" (appears 2 times) → ALLOW (below threshold)
- ❌ "First time saying this" (appears 1 time) → ALLOW

---

### 3. RATE LIMIT CHECK
**Rule**: IF user_message_count_in_last_30_seconds > 5 → WARN or BLOCK

**Expected Pattern**: rate_limit_applied=True

**Validation**:
- Filter messages by user_id in last 30 seconds
- Count messages
- If count == 5 → decision="warn", action="send_warning"
- If count > 5 → decision="block", reason="rate_limit"
- Log: `{"pattern": "rate_limit_applied", "value": true, "message_count": N}`

**Examples**:
- ✅ User sends 6 messages in 30s → BLOCK
- ✅ User sends 5 messages in 30s → WARN
- ❌ User sends 4 messages in 30s → ALLOW
- ❌ User sends 6 messages in 60s → ALLOW (outside time window)

---

### 4. TOXIC CONTENT CHECK
**Rule**: IF message contains toxic keywords AND confidence > 0.8 → BLOCK

**Expected Pattern**: toxicity_check_executed=True

**Validation**:
- Load toxic_keywords list (see resources/toxic_patterns.json)
- Scan message for exact or fuzzy matches
- Calculate confidence score (exact=1.0, fuzzy varies by similarity)
- If confidence > 0.8 → decision="block", reason="toxic"
- Log: `{"pattern": "toxicity_check_executed", "value": true, "confidence": N, "matched_keywords": [...]}`

**Examples**:
- ✅ "You're a [slur]" (exact match, confidence=1.0) → BLOCK
- ✅ "F*** this stream" (obfuscated match, confidence=0.9) → BLOCK
- ❌ "This is frustrating" (mild negative, confidence=0.3) → ALLOW
- ❌ "Nice job!" (positive, confidence=0.0) → ALLOW

---

### 5. LEGITIMATE MESSAGE ROUTING
**Rule**: IF all_checks_passed → ALLOW AND route_to_banter_response_skill

**Expected Pattern**: allowed_and_routed=True

**Validation**:
- Verify all previous checks returned "allow"
- decision="allow"
- next_action="route_to_banter_skill"
- Log: `{"pattern": "allowed_and_routed", "value": true, "next_skill": "banter_response"}`

**Examples**:
- ✅ "Great content!" (passes all checks) → ALLOW + route to banter
- ✅ "What game is this?" (passes all checks) → ALLOW + route to banter
- ❌ "SPAM MESSAGE" (fails caps check) → BLOCK (no routing)

---

## Expected Patterns Summary

When validating with 0102, check that each execution logs these patterns:

```json
{
  "execution_id": "exec_001",
  "message": "Great stream!",
  "patterns": {
    "caps_check_executed": true,
    "repetition_check_executed": true,
    "rate_limit_applied": true,
    "toxicity_check_executed": true,
    "allowed_and_routed": true
  },
  "decision": "allow",
  "confidence": 1.0
}
```

**Pattern Fidelity Calculation**:
```
fidelity = (patterns_executed / total_patterns_in_skill)
fidelity = 5/5 = 1.00 (100%)
```

**Success Criteria for Prototype**:
- ✅ Pattern fidelity ≥ 90% across all test cases
- ✅ Outcome quality ≥ 85% (correct classifications)
- ✅ No false negatives on toxic/spam
- ✅ Low false positive rate (<5%)

---

## Benchmark Test Cases

### Test Set 1: Spam Messages (20 cases)
1. "VISIT MY CHANNEL!!!!!!" → BLOCK (caps)
2. "CHECK THIS OUT NOW" → BLOCK (caps)
3. "Follow me!" (x3 repetition) → BLOCK (repetition)
4. "Join Discord" (x4 repetition) → BLOCK (repetition)
5. User sends 6 rapid messages → BLOCK (rate limit)
... (15 more spam cases)

### Test Set 2: Toxic Messages (20 cases)
1. Message with racial slur → BLOCK (toxic, confidence=1.0)
2. Message with profanity → BLOCK (toxic, confidence=0.95)
3. "You suck at this game" → BLOCK (toxic, confidence=0.85)
... (17 more toxic cases)

### Test Set 3: Legitimate Messages (60 cases)
1. "Great stream!" → ALLOW
2. "What game is this?" → ALLOW
3. "How long have you been streaming?" → ALLOW
... (57 more legitimate cases)

### Test Set 4: Edge Cases (10 cases)
1. "This is REALLY cool" → ALLOW (caps below threshold)
2. "lol" (x2 repetition) → ALLOW (below repetition threshold)
3. Message in non-English → CONTEXT-DEPENDENT
... (7 more edge cases)

**Total**: 110 test cases

---

## 0102 Validation Protocol

**Step 1**: Review skill instructions
- [ ] Understand each rule
- [ ] Verify examples make sense
- [ ] Identify any ambiguities

**Step 2**: Execute benchmark tasks (manually)
- [ ] Test Set 1: Spam (20 cases)
- [ ] Test Set 2: Toxic (20 cases)
- [ ] Test Set 3: Legitimate (60 cases)
- [ ] Test Set 4: Edge (10 cases)

**Step 3**: Log pattern fidelity
- For each execution, verify all 5 patterns logged
- Calculate per-execution fidelity (patterns_executed / 5)
- Calculate overall fidelity across all 110 cases

**Step 4**: Calculate outcome quality
- Count correct classifications
- Outcome quality = (correct / total)

**Step 5**: Validate thresholds
- [ ] Pattern fidelity ≥ 90%?
- [ ] Outcome quality ≥ 85%?
- [ ] Combined score ≥ 88%?

**Step 6**: Document failures
- If any test fails, document:
  - Which instruction was unclear?
  - Why did execution deviate?
  - How should instruction be improved?

**Step 7**: Iterate if needed
- Update SKILL.md based on failures
- Re-run failed test cases
- Achieve ≥90% threshold

**Step 8**: Approve for deployment
- [ ] All thresholds met
- [ ] Ready to extract to modules/communication/livechat/skills/
- [ ] Pattern validated for native Qwen/Gemma execution

---

## Resources

See `examples/` directory for:
- `spam_examples.json` - 20 spam test cases
- `toxic_examples.json` - 20 toxic test cases
- `legitimate_examples.json` - 60 legitimate test cases
- `edge_cases.json` - 10 edge test cases

See `resources/` directory for:
- `toxic_patterns.json` - Toxic keyword database
- `validation_template.json` - Logging template

---

## Next Steps After Validation

**If prototype succeeds** (≥90% fidelity):
1. Extract to `modules/communication/livechat/skills/youtube_moderation/`
2. Add `versions/`, `metrics/`, `variations/` directories
3. Create baseline: `versions/v1.0_baseline.md` (copy of validated SKILL.md)
4. Implement WRE loader to inject into Qwen/Gemma prompts
5. Run same 110 test cases with Gemma
6. Enable pattern fidelity scoring
7. Compare: 0102 fidelity vs Gemma fidelity
8. If Gemma ≥ 0102 → SUCCESS (skill is portable!)
9. If Gemma < 0102 → Qwen generates variations, A/B test, evolve

---

**Status**: READY FOR 0102 VALIDATION
**Next Action**: Execute 110 benchmark test cases manually with Claude Code
