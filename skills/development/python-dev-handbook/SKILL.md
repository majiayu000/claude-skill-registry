---
name: python-dev-handbook
description: 當要開發或修改 Python 程式碼時使用。
---

# 工作流程

- 檢查目前終端機工作目錄是否有 `.venv` 資料夾。
- 若存在，使用該環境執行所有 Python 指令
  （Windows: `.venv\Scripts\python.exe`）。
- 若不存在，執行 `uv venv --python3.11 .venv`
- 優先直接呼叫 `.venv\Scripts\python.exe`
- 與 `uv pip --python .venv\Scripts\python.exe`
- 避免使用 activate
