---
name: security-reviewer
description: 基於 OWASP Top 10 和安全最佳實踐，對程式碼進行安全性審查。
---

---
name: security-reviewer
description: Security audit following OWASP Top 10 and best practices for web applications. Triggers: SEC, security, 安全, OWASP, 漏洞, vulnerability, audit, 稽核, 安全檢查, security check, CVE, 資安, penetration, pentest, 滲透, injection, XSS, CSRF, 認證, authentication, 授權, authorization, secrets, 敏感資料.
version: 1.0.0
category: security
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - code-reviewer
allowed-tools:
  - read_file
  - grep_search
  - semantic_search
  - run_in_terminal
  - get_errors
---

# 安全性審查技能

## 描述

基於 OWASP Top 10 和安全最佳實踐，對程式碼進行安全性審查。

## 觸發條件

- 「安全檢查」「security review」「OWASP」
- 「漏洞掃描」「vulnerability scan」
- PR 審查時自動觸發安全檢查

---

## 🔒 OWASP Top 10 (2021) 檢查清單

### A01: Broken Access Control（失效的存取控制）

**檢查項目**：
- [ ] 路徑遍歷 (Path Traversal)
- [ ] 未驗證的重導向
- [ ] IDOR (Insecure Direct Object Reference)
- [ ] 缺少存取控制檢查

```python
# ❌ 不安全
@app.get("/files/{filename}")
def get_file(filename: str):
    return open(f"/data/{filename}").read()  # Path traversal!

# ✅ 安全
@app.get("/files/{file_id}")
def get_file(file_id: str, current_user: User = Depends(get_current_user)):
    file = db.get_file(file_id)
    if file.owner_id != current_user.id:
        raise HTTPException(403)
    return file.content
```

### A02: Cryptographic Failures（加密機制失效）

**檢查項目**：
- [ ] 敏感資料明文傳輸
- [ ] 使用弱加密演算法 (MD5, SHA1)
- [ ] 密鑰硬編碼
- [ ] 不安全的隨機數生成

```python
# ❌ 不安全
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ 安全
from passlib.hash import bcrypt
password_hash = bcrypt.hash(password)
```

### A03: Injection（注入攻擊）

**檢查項目**：
- [ ] SQL Injection
- [ ] Command Injection
- [ ] LDAP Injection
- [ ] XPath Injection

```python
# ❌ SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ✅ 參數化查詢
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### A04: Insecure Design（不安全的設計）

**檢查項目**：
- [ ] 缺乏 rate limiting
- [ ] 缺乏業務邏輯驗證
- [ ] 不安全的密碼重設流程

### A05: Security Misconfiguration（安全設定錯誤）

**檢查項目**：
- [ ] Debug 模式在 production 開啟
- [ ] 預設帳密未更改
- [ ] 不必要的功能啟用
- [ ] 錯誤訊息洩漏敏感資訊

```python
# ❌ Production 不應該
app = FastAPI(debug=True)

# ✅ 從環境變數讀取
app = FastAPI(debug=os.getenv("DEBUG", "false").lower() == "true")
```

### A06: Vulnerable Components（易受攻擊的元件）

**檢查項目**：
- [ ] 使用已知漏洞的套件版本
- [ ] 未定期更新依賴
- [ ] 使用不維護的套件

```bash
# 檢查已知漏洞
pip-audit
safety check
npm audit
```

### A07: Authentication Failures（身分驗證失敗）

**檢查項目**：
- [ ] 弱密碼政策
- [ ] 暴力破解防護
- [ ] Session 管理不當
- [ ] 不安全的「記住我」實作

### A08: Data Integrity Failures（資料完整性失敗）

**檢查項目**：
- [ ] 不安全的反序列化
- [ ] 缺乏數位簽章驗證
- [ ] 未驗證的軟體更新

### A09: Logging & Monitoring Failures（日誌與監控失敗）

**檢查項目**：
- [ ] 缺乏安全事件日誌
- [ ] 日誌中包含敏感資料
- [ ] 缺乏監控告警

```python
# ❌ 不應該記錄密碼
logger.info(f"User login: {username}, password: {password}")

# ✅ 只記錄必要資訊
logger.info(f"User login attempt: {username}, success: {success}")
```

### A10: SSRF（伺服器端請求偽造）

**檢查項目**：
- [ ] 未驗證使用者提供的 URL
- [ ] 可存取內部服務
- [ ] 可存取雲端元資料 API

```python
# ❌ SSRF 風險
response = requests.get(user_provided_url)

# ✅ 驗證 URL
from urllib.parse import urlparse
parsed = urlparse(user_provided_url)
if parsed.netloc not in ALLOWED_HOSTS:
    raise ValueError("Invalid URL")
```

---

## 🔧 自動化工具整合

### Python 安全掃描

```toml
# pyproject.toml
[project.optional-dependencies]
security = [
    "bandit>=1.7.5",      # 靜態分析
    "safety>=2.3.0",      # 依賴漏洞檢查
    "pip-audit>=2.6.0",   # pip 套件漏洞
]
```

```bash
# 執行安全掃描
bandit -r src/ -f json -o bandit-report.json
safety check --full-report
pip-audit
```

### JavaScript/TypeScript 安全掃描

```bash
# npm audit
npm audit --audit-level=moderate

# Snyk
npx snyk test
```

### Secrets 檢測

```bash
# 使用 truffleHog 或 gitleaks
gitleaks detect --source . --verbose
trufflehog filesystem . --no-update
```

---

## 📋 輸出格式

```markdown
## 🔒 安全性審查報告

### 風險摘要

| 嚴重程度 | 數量 |
|----------|------|
| 🔴 Critical | 0 |
| 🟠 High | 2 |
| 🟡 Medium | 5 |
| 🟢 Low | 3 |

### 發現問題

#### 🟠 HIGH: SQL Injection 風險
- **位置**: `src/repositories/user_repo.py:45`
- **問題**: 直接拼接 SQL 字串
- **建議**: 使用參數化查詢
- **OWASP**: A03 - Injection

#### 🟡 MEDIUM: 缺乏 Rate Limiting
- **位置**: `src/api/auth.py:login()`
- **問題**: 登入端點無請求頻率限制
- **建議**: 加入 rate limiting middleware
- **OWASP**: A04 - Insecure Design

### 工具掃描結果

- ✅ Bandit: 0 issues
- ⚠️ Safety: 2 vulnerable packages
- ✅ Secrets scan: No secrets detected

### 建議行動

1. **立即**: 修復 SQL Injection
2. **短期**: 更新有漏洞的套件
3. **長期**: 實作完整的日誌審計
```

---

## 🔗 相關資源

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
