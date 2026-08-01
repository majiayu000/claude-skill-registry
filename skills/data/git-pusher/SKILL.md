---
name: git-pusher
description: 執行 Git commit、push，並確保 CI 流程正確觸發。
---

```markdown
---
name: git-pusher
description: |
  Execute Git commit, push, and trigger CI workflows.
  LOAD THIS SKILL WHEN: User says "push", "推送", "git push", "deploy", "部署" | after completing commits | ready to deploy.
  CAPABILITIES: Pre-push checks, Conventional Commits format, CI status monitoring, force-push with lease.
---

# Git 推送技能

## 描述
執行 Git commit、push，並確保 CI 流程正確觸發。

## 觸發條件
- 「推送」「git push」
- 「部署」「deploy」
- Workflow 中的推送步驟

## 前置條件檢查
- [ ] 所有測試通過
- [ ] Memory Bank 已同步
- [ ] 無未追蹤重要檔案
- [ ] Commit message 符合規範

## 執行流程

### 1. 預檢查
```bash
# 檢查狀態
git status

# 確認分支
git branch --show-current

# 檢查遠端同步
git fetch origin
```

### 2. 提交
```bash
# Staging
git add -A

# Commit (Conventional Commits)
git commit -m "type(scope): description"
```

### 3. 推送
```bash
# Push
git push origin [branch]

# 或強制推送（謹慎使用）
git push --force-with-lease origin [branch]
```

### 4. CI 確認
```
等待 CI 結果...
- GitHub Actions: [狀態]
- Tests: [狀態]
- Build: [狀態]
```

## Commit Message 規範
```
type(scope): description

Types:
- feat:     新功能
- fix:      修復 bug
- docs:     文件變更
- style:    格式調整
- refactor: 重構
- test:     測試
- chore:    雜項

Examples:
- feat(auth): 新增 OAuth 登入
- fix(api): 修復 rate limit 計算錯誤
- docs(readme): 更新安裝說明
```

## 輸出格式
```
🚀 Git 推送流程

═══════════════════════════════════════

[1/4] 預檢查 ✅
  ├─ 分支：main
  ├─ 遠端：origin (github.com/user/repo)
  └─ 狀態：3 個檔案待提交

[2/4] 提交 ✅
  ├─ Message: feat(skills): 新增能力管理器
  └─ Hash: a1b2c3d

[3/4] 推送 ✅
  ├─ 目標：origin/main
  └─ 結果：成功

[4/4] CI 狀態 🔄
  ├─ GitHub Actions: 執行中...
  ├─ 連結：https://github.com/...
  └─ 預計完成：2 分鐘

═══════════════════════════════════════

✅ 推送完成！CI 執行中，請稍後查看結果。
```

## 使用範例
```
「推送到 main」
「git push --force」
「部署到 production」
```

```
