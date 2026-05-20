---
name: prd-update
version: 1.0
description: |
  Fast PRD updates - Quick version and feature status updates.
  Auto-activates on "更新 PRD", "update PRD", "PRD 版本", "完成功能" keywords.
  AMP principle: Automate the meta workflow.
allowed-tools: [Read, Edit, Grep]
trigger_keywords:
  - 更新 PRD
  - update PRD
  - PRD 版本
  - 完成功能
  - PRD version
  - mark complete
  - 标记完成
auto_activate: true
priority: high
---

# PRD Update - 快速更新产品需求文档

**Purpose**: 快速更新 PRD.md 版本和功能状态

**AMP Principle**: 自动化 Meta Workflow

---

## Quick Update Templates

### 更新版本号
```bash
# 从 v2.14 升到 v2.15
sed -i '' 's/Version: v2\.14/Version: v2.15/' /Users/young/project/career_ios_backend/PRD.md
```

### 添加新完成功能
```markdown
## Current Features

**v2.15** (2025-XX-XX):
- Session name field with validation
- Client partial match search

**v2.14** (previous):
- ...
```

### 更新实施状态
```bash
# 标记功能完成
sed -i '' 's/- \[ \] Session name field/- \[x\] Session name field/' /Users/young/project/career_ios_backend/PRD.md
```

---

## Update Workflow

### Step 1: 功能完成后
```
Completed: Session name field
  ↓
Update PRD:
  1. 增加版本号 (v2.14 → v2.15)
  2. 在 Current Features 添加新功能
  3. 在 Implementation Status 标记完成
  4. 更新 API Endpoints (if new)
```

### Step 2: 验证更新
```bash
# 检查版本号
grep "Version:" /Users/young/project/career_ios_backend/PRD.md

# 检查新功能
grep -A 3 "Current Features" /Users/young/project/career_ios_backend/PRD.md

# 检查实施状态
grep "\[x\]" /Users/young/project/career_ios_backend/PRD.md
```

---

## Common Update Patterns

### Pattern 1: 新 API 端点
```markdown
## API Endpoints

**Sessions**:
- POST /api/sessions - Create new session
- GET /api/sessions/{id} - Get session details
- PUT /api/sessions/{id}/name - Update session name ← NEW
```

### Pattern 2: 新数据库字段
```markdown
## Database Schema

**sessions table**:
- id (UUID)
- name (VARCHAR) ← NEW (v2.15)
- created_at (TIMESTAMP)
```

---

## IMPORTANT

- **小步更新** - 每个功能单独 commit
- **保持一致** - 遵循现有格式
- **立即更新** - 不要累积到后面

---

**Version**: 1.0 (Toolbox refactor)
**Size**: ~110 lines
**Philosophy**: Automate the meta workflow
