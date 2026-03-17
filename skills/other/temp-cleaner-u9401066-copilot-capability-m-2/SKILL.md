---
name: temp-cleaner
description: |
  Clean temporary files, caches, and build artifacts.
  LOAD THIS SKILL WHEN: User says "清理", "clean", "刪除暫存", "清除快取" | disk space issues | before archiving | end of workflow.
  CAPABILITIES: Python cache (__pycache__, .pytest_cache), Node.js (dist, .cache), safe deletion with confirmation, protected files list.
---

# 臨時檔案清理技能

## 描述
清理專案中的臨時檔案、快取和建置產物。

## 觸發條件
- 「清理暫存」
- 「清除快取」
- 「clean」
- Workflow 結束時的清理步驟

## 清理目標

### Python 專案
```bash
# Byte-compiled files
__pycache__/
*.py[cod]
*$py.class

# Distribution
dist/
build/
*.egg-info/

# Virtual Environment
.venv/
venv/

# Cache
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Coverage
.coverage
htmlcov/
```

### Node.js 專案
```bash
# Dependencies (可選)
node_modules/

# Build
dist/
build/
.next/

# Cache
.cache/
.npm/
.eslintcache

# Coverage
coverage/
```

### 通用
```bash
# IDE
.idea/
.vscode/settings.json (保留基本設定)

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temp
tmp/
temp/
*.tmp
```

## 安全機制

### 保護清單（不會刪除）
- `.git/`
- `node_modules/` (需明確指定)
- `.venv/` (需明確指定)
- `memory-bank/`
- 任何原始碼檔案

### 確認機制
```
⚠️ 即將刪除以下項目：

📁 __pycache__/ (15 個檔案, 234 KB)
📁 .pytest_cache/ (8 個檔案, 12 KB)
📄 *.pyc (23 個檔案, 156 KB)

總計：46 個項目, 402 KB

確認刪除？[y/N]
```

## 輸出格式
```
🧹 清理報告

═══════════════════════════════════════

清理的項目：
  ✅ __pycache__/ - 15 個檔案
  ✅ .pytest_cache/ - 8 個檔案
  ✅ *.pyc - 23 個檔案
  ⏭️ node_modules/ - 已跳過（需明確指定）

═══════════════════════════════════════

📊 統計：
  - 刪除檔案：46 個
  - 釋放空間：402 KB
  - 保留項目：3 個

✅ 清理完成！
```

## 使用範例
```
「清理暫存檔」
「clean --all」        # 包含 node_modules
「清理 Python 快取」
```

```
