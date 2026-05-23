---
name: version-manager
description: Terraform/Terragrunt のバージョンを管理する。「terraform バージョン」「tfenv」「tgswitch」「tf バージョン切り替え」「terraform インストール」「バージョン確認」「tf version」「terraform 1.5 にして」「tg バージョン」などで起動。
allowed-tools: [Bash, Read]
---

# Version Manager

tfenv/tgswitch を使用して Terraform/Terragrunt のバージョンを管理します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| バージョン確認 | 「バージョン確認」「tf version」 | `terraform version` |
| 一覧表示 | 「インストール済み一覧」「tfenv list」 | `tfenv list` |
| リモート一覧 | 「利用可能バージョン」「list-remote」 | `tfenv list-remote` |
| インストール | 「1.5.0 インストール」「install」 | `tfenv install` |
| 切り替え | 「1.5.0 に切り替え」「use」 | `tfenv use` |

## 実行手順

### 1. ツールの確認

```bash
# tfenv の確認
which tfenv && tfenv --version

# tgswitch の確認
which tgswitch && tgswitch --version

# tenv の確認（統合ツール）
which tenv && tenv --version
```

### 2. 現在のバージョン確認

**Terraform**:

```bash
terraform version
```

**Terragrunt**:

```bash
terragrunt --version
```

### 3. インストール済みバージョン一覧

**tfenv**:

```bash
tfenv list
```

**tgswitch**:

```bash
tgswitch --list-all
```

### 4. 利用可能なバージョン一覧

**tfenv**:

```bash
tfenv list-remote | head -20
```

### 5. バージョンインストール

**tfenv**:

```bash
tfenv install {version}
# 例: tfenv install 1.5.0
# 例: tfenv install latest
```

**tgswitch**:

```bash
tgswitch {version}
# 例: tgswitch 0.50.0
```

### 6. バージョン切り替え

**tfenv**:

```bash
tfenv use {version}
# 例: tfenv use 1.5.0
```

**tgswitch**:

```bash
tgswitch {version}
```

**tenv（統合ツール）**:

```bash
# Terraform バージョン切り替え
tenv tf use {version}
# 例: tenv tf use 1.5.0

# Terragrunt バージョン切り替え
tenv tg use {version}
# 例: tenv tg use 0.50.0

# インストール
tenv tf install {version}
tenv tg install {version}

# 一覧表示
tenv tf list
tenv tg list
```

### 7. 出力フォーマット

```
## バージョン情報

### 現在のバージョン
- Terraform: {version}
- Terragrunt: {version}

### インストール済み（Terraform）
| バージョン | 状態 |
|-----------|------|
| 1.5.0 | ✅ 使用中 |
| 1.4.6 | |
| 1.3.9 | |

### プロジェクト設定
- .terraform-version: {内容}
- .terragrunt-version: {内容}
```

## バージョンファイル

### .terraform-version

プロジェクトで使用する Terraform バージョンを固定:

```
1.5.0
```

tfenv は自動的にこのファイルを読み取ってバージョンを切り替えます。

### .terragrunt-version

プロジェクトで使用する Terragrunt バージョンを固定:

```
0.50.0
```

### required_version

`versions.tf` でバージョン制約を設定:

```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
}
```

## バージョン管理ツールのインストール

### tfenv

```bash
# macOS
brew install tfenv

# 手動インストール
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
```

### tgswitch

```bash
# macOS
brew install warrensbox/tap/tgswitch

# 手動インストール
curl -L https://raw.githubusercontent.com/warrensbox/tgswitch/release/install.sh | bash
```

### tenv（統合ツール）

```bash
# macOS
brew install tenv

# 手動インストール
curl -L https://tofuutils.github.io/tenv/install.sh | bash
```

## 注意事項

- ✅ バージョン管理ツールを使うとプロジェクトごとにバージョンを切り替えられる
- ✅ `.terraform-version` でチームでバージョンを統一
- ✅ `required_version` で最低バージョンを保証
- ⚠️ バージョンアップ時は互換性を確認
