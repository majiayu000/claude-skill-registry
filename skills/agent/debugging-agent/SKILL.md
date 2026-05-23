---
name: debugging-agent
description: |
  Self-Improving Agent that monitors all other agent skills, analyzes their logs,
  detects issues, and proposes improvements.
  
  AUTO-TRIGGERS:
  - Every 30 minutes (scheduled)
  - When error rate > 5% (any agent)
  - When 3+ recurring errors in 24h (same error type)
  - When performance degrades > 2x baseline

allowed-tools:
  - view_file
  - grep_search
  - run_command
  
metadata:
  category: system
  version: 1.0
  triggers:
    auto:
      - schedule: "*/30 * * * *"  # Every 30 minutes
      - condition: "error_rate > 0.05"
      - condition: "recurring_errors >= 3"
      - condition: "performance_degradation > 2.0"
    manual:
      - command: "analyze-logs"
      - command: "propose-improvements"
  
  outputs:
    - type: improvement-proposal
      format: markdown
      location: backend/ai/skills/logs/system/debugging-agent/proposals/
    
  dependencies:
    - backend.ai.skills.common.agent_logger
    - backend.ai.skills.common.log_schema
---

# Debugging Agent

**Self-Improving Agent System의 핵심 컴포넌트**

다른 모든 agent의 로그를 분석하여 문제를 발견하고 개선안을 제안합니다.

---

## 📋 Core Workflow

### 1. Log Collection (로그 수집)

```bash
python backend/ai/skills/system/debugging-agent/scripts/log_reader.py \
  --days 1 \
  --categories system,war-room,analysis
```

**수집 대상:**
- `backend/ai/skills/logs/*/*/execution-*.jsonl`
- `backend/ai/skills/logs/*/*/errors-*.jsonl`
- `backend/ai/skills/logs/*/*/performance-*.jsonl`

**Output:**
```json
{
  "agents": ["signal-consolidation", "war-room-debate", ...],
  "total_executions": 50,
  "total_errors": 3,
  "time_range": "2025-12-25 to 2025-12-26"
}
```

---

### 2. Pattern Detection (패턴 감지)

```bash
python backend/ai/skills/system/debugging-agent/scripts/pattern_detector.py \
  --input logs_summary.json \
  --output patterns.json
```

**감지 패턴:**

#### A. Recurring Errors (반복 에러)
- **조건**: 동일한 error type이 24시간 내 3회 이상
- **예시**: `TypeError: missing required positional argument` (3회)
- **우선순위**: HIGH

#### B. Performance Degradation (성능 저하)
- **조건**: duration_ms가 baseline 대비 2배 이상
- **예시**: 평균 1000ms → 최근 2500ms
- **우선순위**: MEDIUM

#### C. High Error Rate (높은 에러율)
- **조건**: error rate > 5%
- **예시**: 50 executions, 4 errors = 8%
- **우선순위**: CRITICAL

#### D. API Rate Limits (API 제한)
- **조건**: "rate limit" 관련 에러 5회 이상
- **우선순위**: HIGH

**Output:**
```json
{
  "patterns": [
    {
      "type": "recurring_error",
      "agent": "war-room-debate",
      "error_type": "TypeError",
      "count": 3,
      "impact": "CRITICAL",
      "first_seen": "2025-12-25T18:30:00",
      "last_seen": "2025-12-26T09:15:00"
    }
  ]
}
```

---

### 3. Context Synthesis (맥락 통합)

관련 agent의 `SKILL.md`를 읽어서 컨텍스트 파악:

```bash
# Read related skills
cat backend/ai/skills/war-room/war-room-debate/SKILL.md
cat backend/api/war_room_router.py
```

**파악 내용:**
- Agent의 역할과 책임
- 입력/출력 형식
- 의존성 (DB, APIs, etc.)
- 최근 변경사항

---

### 4. Improvement Proposal (개선안 생성)

```bash
python backend/ai/skills/system/debugging-agent/scripts/improvement_proposer.py \
  --patterns patterns.json \
  --output proposals/proposal-20251226-100822.md
```

**Proposal 포맷:**

````markdown
# Improvement Proposal: Fix War Room TypeError

**Generated**: 2025-12-26 10:08:22  
**Agent**: war-room-debate  
**Priority**: CRITICAL  
**Confidence**: 87%

---

## 🔍 Issue Summary

**Pattern Detected**: Recurring Error (3 occurrences in 24h)

**Error**:
```
TypeError: missing required positional argument for AIDebateSession
```

**Impact**: 
- War Room debates failing
- No trading signals generated
- User experience degraded

---

## 📊 Root Cause Analysis

**Evidence**:
1. Error occurs in `war_room_router.py:L622`
2. `AIDebateSession.__init__()` called with missing argument
3. Recent code change added new required field

**Root Cause**: 
Schema mismatch between `AIDebateSession` model and router code.

---

## 💡 Proposed Solution

### Option 1: Add Missing Argument (Recommended)

**File**: `backend/api/war_room_router.py`

```python
# Line 622 - Add missing argument
session = AIDebateSession(
    ticker=ticker,
    consensus_action=pm_decision["consensus_action"],
    # ... existing fields ...
    dividend_risk_vote=next((v["action"] for v in votes if v["agent"] == "dividend_risk"), None),  # ← ADD THIS
    created_at=datetime.now()
)
```

**Confidence**: 90% (high evidence)

### Option 2: Make Field Optional

Alternatively, update the model to make the field optional.

**Confidence**: 70% (lower impact but safer)

---

## 🎯 Expected Impact

- ✅ Eliminates TypeError
- ✅ War Room debates resume
- ✅ Trading signals restored
- ⚠️ Requires testing with all agents

---

## 🧪 Verification Plan

1. Apply fix to `war_room_router.py`
2. Run War Room debate: `POST /api/war-room/debate {"ticker": "AAPL"}`
3. Verify no TypeError
4. Check logs for successful execution

---

## 📝 Risk Assessment

**Risk Level**: LOW

**Potential Issues**:
- May need to update other agent votes similarly
- Database migration if schema changed

**Rollback Plan**:
- Revert commit if issues arise
- Monitor error logs for 24h

---

**Confidence Breakdown**:
- Error Reproducibility: 100% (3/3 occurrences)
- Historical Success: 80% (similar fixes worked)
- Impact Clarity: 90% (clear user impact)
- Root Cause Evidence: 85% (stack trace clear)
- Solution Simplicity: 85% (1-line fix)

**Overall Confidence**: 87%
````

---

## 🎯 Confidence Scoring (5 Metrics)

Proposal confidence는 5가지 메트릭의 가중 평균:

1. **Error Reproducibility** (30%)
   - 100% if error occurs every time
   - 0% if random/sporadic

2. **Historical Success** (25%)
   - Similar fixes worked before?
   - Based on past proposals

3. **Impact Clarity** (20%)
   - Clear user/system impact?
   - Measurable consequences?

4. **Root Cause Evidence** (15%)
   - Stack trace available?
   - Clear error message?

5. **Solution Simplicity** (10%)
   - Simple 1-line fix vs complex refactor
   - Lower risk = higher confidence

**Formula**:
```python
confidence = (
    reproducibility * 0.30 +
    historical_success * 0.25 +
    impact_clarity * 0.20 +
    root_cause_evidence * 0.15 +
    solution_simplicity * 0.10
)
```

---

## 🔄 Usage Examples

### Manual Trigger

```bash
# Analyze recent logs
python backend/ai/skills/system/debugging-agent/scripts/log_reader.py --days 1

# Detect patterns
python backend/ai/skills/system/debugging-agent/scripts/pattern_detector.py

# Generate proposals
python backend/ai/skills/system/debugging-agent/scripts/improvement_proposer.py
```

### Scheduled Execution (via orchestrator)

```python
# scripts/run_debugging_agent.py
import schedule

def run_debugging_agent():
    subprocess.run(["python", "backend/ai/skills/system/debugging-agent/scripts/log_reader.py"])
    subprocess.run(["python", "backend/ai/skills/system/debugging-agent/scripts/pattern_detector.py"])
    subprocess.run(["python", "backend/ai/skills/system/debugging-agent/scripts/improvement_proposer.py"])

schedule.every(30).minutes.do(run_debugging_agent)
```

---

## 📁 Output Structure

```
backend/ai/skills/logs/system/debugging-agent/
├── execution-2025-12-26.jsonl    # Debugging agent's own logs
├── errors-2025-12-26.jsonl
└── proposals/
    ├── proposal-20251226-100822.md  # Improvement proposal
    ├── proposal-20251226-103045.md
    └── accepted/
        └── proposal-20251226-100822.md  # User accepted
```

---

## ⚠️ Important Notes

1. **Read-Only Access**: Debugging Agent는 로그만 읽고 코드는 수정하지 않음
2. **User Approval Required**: 모든 제안은 사용자 승인 필요
3. **Audit Trail**: 모든 제안과 결과는 proposals/ 디렉토리에 보관
4. **Safety First**: Confidence < 70%인 제안은 경고 표시

---

## 🚀 Next Steps

After Phase 2 complete:
- **Phase 3**: Skill Orchestrator (scheduling, notifications)
- **(Optional) Phase 4**: CI/CD Integration (auto-apply patches)

---

**Created**: 2025-12-26  
**Version**: 1.0  
**Status**: In Development
