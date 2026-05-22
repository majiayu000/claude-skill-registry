---
name: security-scan-trivy
description: Trivyで依存関係/コンテナの脆弱性をスキャンし、重大度順に潰す。リリース前チェックで使う。
---

# Trivy Security Scan

## Instructions

- まずCritical/Highを対象にする
- 例外（許容する脆弱性）は理由と期限を必ず残す
- CIに組み込む場合は「最初は警告→次にfail」に段階導入

