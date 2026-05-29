---
name: whole-group-processor
description: |
  Xử lý từng GROUP một cách có hệ thống trong Whole Knowledge Architecture.
  Hỗ trợ expand, refine, và enrich nội dung từng nhóm khái niệm.
  v1.1.0: Added --pr, --commit, --dry flags for GitHub workflow automation.
version: 1.1.0
license: MIT
allowed-tools:
  - Edit
  - Grep
  - Read
  - Bash
  - Task
  - Write
metadata:
  author: "Whole Project"
  category: "documentation"
  created: "2026-01-03"
---

# Whole Group Processor v1.1

**Systematic Group-by-Group Processing** - Xử lý từng nhóm khái niệm một cách có hệ thống với progress tracking.

---

## Overview

Whole Knowledge Architecture có:
- **10 Domains** (FOUNDATIONS → META)
- **50 Functions** (5 per domain)
- **371 Groups** (trung bình 7.4 groups/function)

Skill này cho phép xử lý từng GROUP một cách có hệ thống.

---

## Commands

### `/group [identifier]` - Process a specific group

```
/group 1-1-3    → Process Domain 1, Function 1, Group 3
/group CF5-7    → Process Function 5 (CF5), Group 7
/group next     → Auto-suggest next pending group
```

### `/group-status` - View progress status

```
/group-status           → Overall progress
/group-status 1         → Domain 1 progress
/group-status CF5       → Function 5 progress
```

### `/group-plan [scope]` - Create processing plan

```
/group-plan CF5         → Plan for all groups in CF5
/group-plan 1           → Plan for all groups in Domain 1
/group-plan all         → Full project plan
```

---

## Flags

### `--pr` - Auto GitHub PR Flow

Append `--pr` to any command to automatically push, create PR, and merge after completion.

```
/group 1-1-3 --pr       → Process group + auto PR flow
/group next --pr        → Process next + auto PR flow
```

**PR Flow Steps:**
1. Create feature branch: `claude/group-{identifier}-{timestamp}`
2. Commit changes with conventional commit message
3. Push branch to origin
4. Create PR with auto-generated title and description
5. Auto-merge PR (if checks pass)
6. Return to main branch and pull

**Example Output:**
```
╔══════════════════════════════════════════════════════════════╗
║ PR FLOW COMPLETE                                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ Branch:   claude/group-1-1-3-260103                          ║
║ Commit:   docs(whole): process CF1 group 3                   ║
║ PR:       #123 - Process CF1-3 Emergence & Creative          ║
║ Status:   ✓ Merged                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### `--commit` - Commit only (no PR)

```
/group 1-1-3 --commit   → Process group + commit to current branch
```

### `--dry` - Dry run (no changes)

```
/group 1-1-3 --dry      → Analyze only, show what would change
```

---

## Identifier System

### Format: `D-F-G` (Domain-Function-Group)

```
Examples:
  1-1-3   = FOUNDATIONS > CF1 (First Principles) > Group 3 (Emergence & Creative Principles)
  2-3-5   = DYNAMICS > CF8 (System Evolution) > Group 5 (System Laws & Perverse Effects)
  10-5-8  = META > CF50 (Framework Evolution) > Group 8 (Creative & Cultural Analysis)
```

### Alternative Format: `CFN-G`

```
Examples:
  CF1-3   = Function 1 (FOUNDATIONS > First Principles) > Group 3
  CF15-8  = Function 15 (OPERATIONS > Decision Frameworks) > Group 8
  CF50-1  = Function 50 (META > Framework Evolution) > Group 1
```

---

## Processing Workflow

### Phase 1: LOCATE
```
├─ Parse identifier → Get domain, function, group
├─ Grep for group header in Whole.md
└─ Read group content (concepts list)
```

### Phase 2: ANALYZE + GAP ANALYSIS (CRITICAL)
```
├─ Count concepts in group
├─ Check content completeness (4-point structure)
├─ **[GAP ANALYSIS - MUST DO]**
│   ├─ Research related concepts (web search, knowledge base)
│   ├─ List 2-3 potential concepts that could be added
│   ├─ Evaluate: Are there important theories/principles missing?
│   ├─ Evaluate: Are there practical applications not covered?
│   └─ Rate expansion potential: HIGH/MEDIUM/LOW
├─ Identify gaps or improvements needed
└─ Note cross-references
```

### Phase 3: PROCESS (Choose action - PRIORITY ORDER)
```
**Action Priority (MUST follow this order):**

1. [E] Expand    - Add new concepts (IF expansion potential is HIGH/MEDIUM)
   ↓ (only if expansion potential is LOW)
2. [C] Complete  - Fill missing 4-point structures
   ↓ (only if structure is complete)
3. [R] Refine    - Improve existing concept descriptions
   ↓ (only if descriptions are good)
4. [X] Cross-ref - Add/update cross-references
   ↓ (only if cross-refs are adequate)
5. [V] Validate  - Check and mark as complete

**IMPORTANT: [E] Expand should be the DEFAULT action unless gap analysis shows LOW potential**
```

### Phase 4: EXECUTE
```
├─ Apply chosen action(s)
├─ Validate changes (bilingual, 4-point)
├─ Update cross-references if needed
└─ Mark group as processed
```

### Phase 5: UPDATE
```
├─ Update progress tracker
├─ Log session details
└─ Suggest next group (if applicable)
```

---

## Processing Actions

### [E] Expand - Thêm khái niệm mới (PRIORITY ACTION)

```markdown
**CRITICAL: Đây là action ưu tiên nhất. Mỗi group PHẢI được đánh giá khả năng expand trước.**

**When to use:**
- Group có thể thêm khái niệm bổ sung, liên quan, hoặc chuyên sâu hơn
- Research cho thấy domain có khái niệm quan trọng chưa được cover
- Có sub-topics, principles, theories, hoặc applications chưa mention
- KHÔNG giới hạn bởi số lượng concepts hiện có

**Gap Analysis Checklist (MUST DO BEFORE CHOOSING ACTION):**
1. Search web/knowledge cho related concepts trong domain
2. Kiểm tra: Có principles/theories quan trọng nào chưa mention?
3. Kiểm tra: Có applications/examples thực tế nào cần thêm?
4. Kiểm tra: Có sub-categories hoặc variations nào chưa cover?
5. Kiểm tra: Các domains khác có concepts liên quan chưa được kết nối?

**Output:**
- New concepts added với full 4-point structure
- Vietnamese primary, English secondary
- Cross-references to existing and new concepts
- Minimum 1-2 new concepts per group (nếu có gaps)
```

### [R] Refine - Cải thiện mô tả

```markdown
**When to use:**
- Descriptions quá ngắn hoặc mơ hồ
- Cần thêm clarity hoặc depth
- Terminology inconsistent

**Output:**
- Enhanced descriptions
- Better examples
- Clearer definitions
```

### [C] Complete - Hoàn thiện cấu trúc

```markdown
**When to use:**
- Concepts thiếu 4-point structure
- Missing bullets hoặc cross-references
- Incomplete Vietnamese/English pairs

**Output:**
- All concepts have 4+ points
- Complete bilingual pairs
- Proper formatting
```

### [X] Cross-ref - Cập nhật liên kết

```markdown
**When to use:**
- Missing connections to other domains
- Outdated references
- New relationships discovered

**Output:**
- Bidirectional links verified
- New connections added
- Orphaned links fixed
```

### [V] Validate - Xác nhận hoàn thành

```markdown
**When to use:**
- Group đã đầy đủ, không cần thay đổi
- Chỉ cần review và confirm

**Output:**
- Group marked as validated
- No content changes
- Progress updated
```

---

## Output Format

### Progress Display

```
╔══════════════════════════════════════════════════════════════╗
║ GROUP PROCESSING STATUS                                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ Current: CF1-3 (Emergence & Creative Principles)             ║
║ Domain:  FOUNDATIONS                                         ║
║ Concepts: 4 concepts                                         ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║ Analysis:                                                    ║
║ ├─ Completeness: ⭐⭐⭐⭐☆ (4/5)                              ║
║ ├─ Structure:    ⭐⭐⭐⭐⭐ (5/5)                              ║
║ ├─ Cross-refs:   ⭐⭐⭐☆☆ (3/5)                              ║
║ └─ Overall:      Good - Minor improvements possible          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║ Recommended Action: [X] Cross-ref                            ║
║ Reason: Missing links to DYNAMICS and CREATION               ║
╚══════════════════════════════════════════════════════════════╝
```

### Session Summary

```
╔══════════════════════════════════════════════════════════════╗
║ SESSION COMPLETE                                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ Groups processed: 5                                          ║
║ Actions taken:    E(2), R(1), C(1), V(1)                    ║
║ Concepts added:   8                                          ║
║ Time:             ~25 minutes                                ║
║                                                              ║
║ Progress: 47/371 groups (12.7%)                              ║
║ Next suggested: CF5-2 (System Robustness & Constraints)      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Critical Rules

### ✅ MUST
- Preserve all existing content (Only Add, Never Subtract)
- Maintain bilingual integrity (Vietnamese primary)
- Follow 4-point minimum structure
- Update progress tracker after each group
- Validate cross-references

### ❌ NEVER
- Delete concepts or groups
- Skip progress tracking
- Leave incomplete structures
- Break bilingual pairs
- Ignore cross-reference integrity

---

## Integration with Other Skills

### Coordination
- **whole-regrouper**: If group structure needs reorganization, defer to `/regroup`
- **whole-analyzer**: For deep duplicate analysis before expanding
- **whole-reviewer**: For post-processing validation
- **whole-translator**: For complex translation needs

### When to Escalate
```
Group needs restructuring    → /regroup [function]
Duplicate concepts detected  → /analyze [function]
Major content validation     → whole-reviewer agent
Complex translation          → whole-translator agent
```

---

## Files & Resources

```
.claude/skills/whole-group-processor/
├─ SKILL.md                    # This file
├─ references/
│  ├─ workflow-steps.md        # Detailed workflow
│  └─ quality-checklist.md     # Validation checklist
└─ plans/
   └─ templates/
      └─ group-plan-template.md # Planning template

.group-progress.json           # Progress tracker (root)
```

---

## Quick Reference

| Command | Action |
|---------|--------|
| `/group 1-1-3` | Process specific group |
| `/group CF5-7` | Process using CF format |
| `/group next` | Auto-suggest next group |
| `/group-status` | View overall progress |
| `/group-status CF5` | View function progress |
| `/group-plan CF5` | Create function plan |

| Flag | Effect |
|------|--------|
| `--pr` | Auto push, create PR, merge |
| `--commit` | Commit only (no PR) |
| `--dry` | Dry run, no changes |

| Action | Code | Description |
|--------|------|-------------|
| Expand | E | Add new concepts |
| Refine | R | Improve descriptions |
| Complete | C | Fill 4-point structure |
| Cross-ref | X | Update links |
| Validate | V | Confirm complete |

---

**Version:** 1.1.0 | **Philosophy:** Systematic, incremental, tracked progress
