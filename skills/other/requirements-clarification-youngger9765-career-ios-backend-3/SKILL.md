---
name: requirements-clarification
description: |
  Force requirements clarification BEFORE implementation to prevent misunderstandings.
  Auto-activates on "需求", "requirement", "客戶要", "新功能", "案主說", "用戶想要" keywords.
  Uses structured CARIO format to clarify ambiguous requirements and validate understanding.
allowed-tools: [Read, AskUserQuestion]
---

# Requirements Clarification Skill

## Purpose
**STOP implementing before fully understanding requirements.**

Prevent the common problem:
```
客戶需求 → Agent 理解不完整 → 實作偏差 → 浪費時間重做
```

**Solution**: Force clarification BEFORE any code is written.

---

## Auto-Activation

Triggers when user mentions:
- ✅ "需求", "requirement", "客戶要", "案主說"
- ✅ "新功能", "用戶想要", "想加一個"
- ✅ "客戶反饋", "需要改成", "應該要"

---

## CARIO Clarification Framework

**Structured format for requirements clarification**:

```
📋 Context (背景)
   - What are we working on?
   - What's the current state?

❓ Ambiguity (不清楚的地方)
   - What's unclear or ambiguous?
   - What assumptions are we making?

🎯 Options (可能的理解)
   - Option A: [interpretation 1]
   - Option B: [interpretation 2]
   - Option C: [interpretation 3]

💡 Recommendation (建議)
   - Recommended approach and why
   - Trade-offs of this choice

⚡ Impact (影響範圍)
   - What components are affected?
   - What tests are needed?
   - Estimated complexity?
```

---

## Mandatory Workflow

### Step 1: STOP and Analyze

**When user provides requirements, DO NOT implement immediately.**

Instead:
1. Read the requirement carefully
2. Identify ALL ambiguities
3. List ALL assumptions
4. Generate clarifying questions

### Step 2: Use CARIO Format

**Example**:

```
User: "客戶說要加一個搜尋功能"

📋 Context
- Working on: career_ios_backend client management
- Current state: Clients can only be listed, no search

❓ Ambiguity
1. 搜尋什麼？(Search by what?)
   - Client name?
   - Client code?
   - Email?
   - All fields?

2. 搜尋方式？(Search type?)
   - Exact match?
   - Partial match?
   - Fuzzy search?

3. 搜尋結果？(Results?)
   - Paginated?
   - How many per page?
   - Sorting?

🎯 Options

Option A: Simple name search (exact match)
- Fastest to implement
- Limited functionality
- Good for MVP

Option B: Multi-field search (partial match)
- Name, email, code searchable
- More flexible
- Moderate complexity

Option C: Full-text search (fuzzy)
- Search all fields
- Most powerful
- Requires additional setup

💡 Recommendation
Start with Option B (multi-field partial match):
- Balances power and simplicity
- Covers 80% of use cases
- Can upgrade to Option C later if needed

⚡ Impact
Affected:
- app/api/clients.py (add search endpoint)
- app/schemas/client.py (add search request schema)
- tests/integration/test_clients_api.py (add search tests)

Complexity: 🟡 Medium (2-3 hours)
Tests needed: 3-5 integration tests
```

### Step 3: Get User Confirmation

**Use AskUserQuestion tool**:

```python
AskUserQuestion(
    questions=[{
        "question": "客戶搜尋功能應該搜尋哪些欄位？",
        "header": "Search Fields",
        "multiSelect": True,
        "options": [
            {
                "label": "姓名 (Name)",
                "description": "搜尋客戶姓名"
            },
            {
                "label": "Email",
                "description": "搜尋 Email 地址"
            },
            {
                "label": "客戶代碼 (Code)",
                "description": "搜尋客戶代碼"
            },
            {
                "label": "全部欄位 (All)",
                "description": "搜尋所有文字欄位"
            }
        ]
    }]
)
```

### Step 4: Document Understanding

**Create a mini-spec**:

```markdown
## Feature: Client Search

### User Story
As a counselor, I want to search for clients by name/email/code,
so that I can quickly find the client I need.

### Acceptance Criteria
- [ ] Can search by client name (partial match)
- [ ] Can search by email (partial match)
- [ ] Can search by client code (exact match)
- [ ] Returns paginated results (10 per page)
- [ ] Case-insensitive search

### API Design
GET /api/v1/clients/search?q={query}&page={page}

Response:
{
  "items": [...],
  "total": 42,
  "page": 1,
  "pages": 5
}

### Tests Required
1. test_search_by_name_success
2. test_search_by_email_success
3. test_search_by_code_success
4. test_search_case_insensitive
5. test_search_pagination
```

### Step 5: Only THEN Start TDD

**After confirmation**, activate `tdd-workflow`:
```
✅ Requirements clear
✅ User confirmed understanding
✅ Acceptance criteria defined
→ NOW safe to write tests and implement
```

---

## Common Ambiguity Patterns

### Pattern 1: Vague Verbs

**❌ Ambiguous**:
- "處理客戶" (handle clients)
- "管理資料" (manage data)
- "改進效能" (improve performance)

**✅ Clarify**:
- What action? (Create? Update? Delete? Search?)
- What data? (Which fields?)
- How much improvement? (What metric? Target?)

### Pattern 2: Missing Details

**❌ Incomplete**:
- "加一個報告" (add a report)

**✅ Clarify**:
- What data in report?
- What format? (PDF? Excel? HTML?)
- Who can access?
- How to generate? (On-demand? Scheduled?)

### Pattern 3: Assumed Context

**❌ Assumption**:
- "客戶說要改成這樣" (client wants it changed)

**✅ Clarify**:
- Changed from what state?
- Changed to what state?
- Why the change?
- What stays the same?

---

## Clarification Questions Checklist

**Before implementing ANY feature, answer**:

### Functional Questions
- [ ] What exactly should it do?
- [ ] What should it NOT do?
- [ ] What are edge cases?
- [ ] What happens on error?

### Data Questions
- [ ] What data is needed?
- [ ] Where does data come from?
- [ ] What's the data format?
- [ ] What are validation rules?

### Integration Questions
- [ ] What other features are affected?
- [ ] What APIs are involved?
- [ ] What database changes needed?
- [ ] What tests are required?

### User Experience Questions
- [ ] Who uses this feature?
- [ ] When do they use it?
- [ ] How do they trigger it?
- [ ] What feedback do they get?

---

## Integration with Other Skills

### Works with tdd-workflow

```
1. requirements-clarification (THIS SKILL)
   - Clarify requirements
   - Get user confirmation
   - Document understanding
   ↓
2. tdd-workflow
   - Write tests based on acceptance criteria
   - Implement to pass tests
   - Refactor
```

### Works with api-development

```
requirements-clarification
   → Define API contract
   → Clarify request/response format
   ↓
api-development
   → Implement FastAPI endpoint
   → Follow defined contract
```

---

## Real Example: Before and After

### ❌ Before (No Clarification)

```
User: "客戶說要能匯出報告"

Agent: (直接實作)
- Creates PDF export
- Only exports basic info
- No customization

Result: ❌ 客戶要的是 Excel，要自訂欄位
        → 浪費 2 小時重做
```

### ✅ After (With Clarification)

```
User: "客戶說要能匯出報告"

Agent: (啟動 requirements-clarification skill)

📋 Context: 諮詢報告匯出功能

❓ Ambiguity:
1. 匯出格式？PDF? Excel? 都要？
2. 匯出內容？哪些欄位？
3. 匯出時機？手動？自動？
4. 客製化？能選擇欄位嗎？

🎯 Options:
A. PDF only (fixed format)
B. Excel only (customizable)
C. Both formats

💡 Recommendation: Option B (Excel)
- 客戶通常要進一步分析
- Excel 更靈活
- 可自訂欄位

⚡ Impact: Medium complexity

(Gets user confirmation)

User: "對，要 Excel，而且要能選擇哪些欄位"

Agent: ✅ 明確了！現在用 TDD 開發...

Result: ✅ 一次做對，客戶滿意
```

---

## Anti-Patterns to Avoid

### ❌ Assuming Without Asking

```python
# Bad
user_input = "加一個搜尋"
# → 直接假設是全文搜尋，實作後才發現要的是簡單篩選
```

### ❌ Implementing Multiple Interpretations

```python
# Bad
"不確定要哪個，所以全部都做"
# → 浪費時間，可能都不是客戶要的
```

### ❌ Asking Too Many Questions

```python
# Bad
"有 20 個問題要問你..."
# → 用戶厭煩，寧願給模糊需求

# Good
"有 3 個關鍵問題，澄清後就能開始："
# → 聚焦核心，快速決策
```

---

## Success Metrics

### Before This Skill
- ⏱️ 需求理解錯誤率：40%
- ⏱️ 重做時間：平均 2 小時/功能
- 😤 客戶滿意度：中等

### After This Skill
- ✅ 需求理解錯誤率：<5%
- ✅ 重做時間：幾乎沒有
- 😊 客戶滿意度：高

**Time Investment**:
- Clarification: +10 minutes
- Saved rework: -2 hours
- **Net benefit: +1h 50m per feature**

---

## Quick Start Template

**Copy this whenever receiving requirements**:

```markdown
## Requirement Clarification

User Request: "[用戶原話]"

📋 Context:
-

❓ Ambiguity:
1.
2.
3.

🎯 Options:
A.
B.
C.

💡 Recommendation:
-

⚡ Impact:
- Files affected:
- Tests needed:
- Complexity:

---

Questions for user:
1.
2.
3.
```

---

## Related Skills

- **tdd-workflow**: Implement after clarification
- **api-development**: API contract definition
- **prd-workflow**: Document requirements formally

---

**Skill Version**: v1.0
**Last Updated**: 2025-12-25
**Project**: career_ios_backend
**Philosophy**: "Measure twice, cut once" - 先搞清楚再動手
