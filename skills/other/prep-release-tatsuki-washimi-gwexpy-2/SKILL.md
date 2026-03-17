---
name: prep_release
description: バージョン更新、CHANGELOG整備、パッケージビルド・公開など、リリース前・リリース時の準備を行う
---

# Prepare Release

リリース前後の包括的な準備・公開を自動化します。

## Quick Usage

```bash
/prep_release              # Interactive release preparation
/prep_release --build      # Build only
/prep_release --testpypi   # Upload to TestPyPI
/prep_release --production # Upload to production PyPI
```

## Release Workflow

リリースプロセスは以下のステップで構成：

1. **Versioning** - バージョン番号の更新
2. **Changelog** - CHANGELOG.md の整備
3. **Build** - パッケージのビルド
4. **Verification** - メタデータ検証
5. **Publish** - PyPI への公開

## Modes

### Build Mode (デフォルト)

パッケージをビルドし、dist/ に生成：

詳細：[reference/build.md](reference/build.md)

### TestPyPI Mode

テスト環境（TestPyPI）に公開：

詳細：[reference/testpypi.md](reference/testpypi.md)

### Production Mode

本番 PyPI に公開：

詳細はセキュリティ上の理由から省略。用途に応じて参照。

## Steps

1. [reference/versioning.md](reference/versioning.md) - バージョン更新
2. [reference/changelog.md](reference/changelog.md) - CHANGELOG 整備
3. [reference/build.md](reference/build.md) - パッケージビルド
