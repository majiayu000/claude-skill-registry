---
name: scan-vuln
description: Go プロジェクトの脆弱性スキャンを実行する。「脆弱性スキャン」「govulncheck」「セキュリティチェック」「脆弱性確認」「vuln」「CVE チェック」「セキュリティスキャン」などで起動。govulncheck を使用して既知の脆弱性を検出。
allowed-tools: [Read, Bash, Glob, Grep]
---

# Scan-Vuln

Go プロジェクトの脆弱性スキャンを実行します。govulncheck を使用して既知の脆弱性を検出。

## 引数

- `--json`: JSON 形式で出力
- `--help`: ヘルプを表示

## 実行手順

### 1. govulncheck のインストール確認

```bash
which govulncheck || go install golang.org/x/vuln/cmd/govulncheck@latest
```

### 2. 脆弱性スキャン実行

```bash
# 基本的なスキャン
govulncheck ./...

# JSON 形式で出力
govulncheck -json ./...

# バイナリのスキャン
govulncheck -mode=binary ./bin/app
```

### 3. 結果レポート

```
## 脆弱性スキャン結果

### 検出された脆弱性: {N} 件

#### GO-2024-XXXX (Critical)
- **パッケージ**: github.com/xxx/yyy
- **バージョン**: v1.2.3
- **説明**: {脆弱性の説明}
- **影響を受けるコード**: {ファイル:行}
- **修正バージョン**: v1.2.4

#### GO-2024-YYYY (High)
- **パッケージ**: github.com/aaa/bbb
- **バージョン**: v2.0.0
- **説明**: {脆弱性の説明}
- **修正バージョン**: v2.0.1

### 推奨アクション
1. `go get -u github.com/xxx/yyy@v1.2.4`
2. `go get -u github.com/aaa/bbb@v2.0.1`
3. `go mod tidy`
4. `go test ./...` で動作確認
```

## 脆弱性の深刻度

| レベル | 説明 |
|--------|------|
| Critical | 即座に対応が必要、リモートコード実行など |
| High | 早急に対応が必要、データ漏洩など |
| Medium | 計画的に対応、DoS など |
| Low | 時間があるときに対応 |

## 脆弱性対応フロー

1. **検出**: `govulncheck ./...` で脆弱性を検出
2. **評価**: 実際にコードで使用されているか確認
3. **更新**: 修正バージョンへ更新
4. **テスト**: 更新後の動作確認
5. **デプロイ**: 本番環境へ反映

## CI/CD への統合

```yaml
# GitHub Actions の例
- name: Run govulncheck
  run: |
    go install golang.org/x/vuln/cmd/govulncheck@latest
    govulncheck ./...
```

## 重要な注意事項

- ✅ 定期的に govulncheck を実行して新しい脆弱性を検出
- ✅ 脆弱性修正のための更新後は、必ずテストを実行
- ✅ govulncheck は実際に呼び出されるコードパスのみを報告するため、誤検知が少ない
- ✅ 間接依存の脆弱性も検出される
