---
name: skill-creator
description: 新しい Antigravity スキルを自動的に作成、検証、パッケージ化するためのツール一式。
---

# Skill Creator

このスキルは、ARIA プロジェクトにおける「知能の拡張」を担います。設計原則に基づいた新しいスキルの雛形作成、構造のバリデーション、および配布用のパッケージングを自動化します。

## ワークフロー

### 1. スキルの初期化 (Initialize)
新しいスキルの基盤となるディレクトリ構造とテンプレートファイルを生成します。
[init_skill.py](scripts/init_skill.py) を使用してください。

```bash
python3 .agent/skills/skill-creator/scripts/init_skill.py <スキル名> --path .agent/skills
```

### 2. スキルの検証 (Validate)
作成したスキルが `agentskills.io` の仕様および ARIA の標準に準拠しているか確認します。
[quick_validate.py](scripts/quick_validate.py) を使用してください。

```bash
python3 .agent/skills/skill-creator/scripts/quick_validate.py .agent/skills/<スキル名>
```

### 3. スキルのパッケージ化 (Package)
スキルを配布可能な形式（.skill ファイル）に圧縮します。
[package_skill.py](scripts/package_skill.py) を使用してください。

```bash
python3 .agent/skills/skill-creator/scripts/package_skill.py .agent/skills/<スキル名>
```

## 設計原則 (ARIA Standard)

- **簡潔さ (Conciseness)**: `SKILL.md` は 100 行以内に収め、Claude のコンテキストを節約する。
- **段階的開示 (Progressive Disclosure)**: 詳細な仕様、API リファレンス、巨大なデータ構造は `references/` に配置し、本体からはリンクのみを張る。
- **カプセル化 (Encapsulation)**: 複雑な操作や「壊れやすい」手順は `scripts/` 配下の Python スクリプトとして固定化し、自由度をあえて下げることで確実性を高める。
