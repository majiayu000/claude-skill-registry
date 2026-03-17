---
name: reorganize-docs
description: Reorganize project documentation with bilingual (English/Japanese) structure. Use when asked to "reorganize docs", "update documentation", or "sync documentation".
---

# Reorganize Docs

Reorganize and synchronize project documentation with proper bilingual structure.

## Documentation Structure

```text
/
├── CLAUDE.md              # Claude Code guidance (English)
├── README.md              # Project introduction (English)
└── docs/
    ├── CLAUDE.ja.md       # Claude Code guidance (Japanese)
    ├── README.ja.md       # Project introduction (Japanese)
    ├── DEVELOPMENT.md     # Development guide (English)
    └── DEVELOPMENT.ja.md  # Development guide (Japanese)
```

## File Purposes

| File                   | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `CLAUDE.md`            | Claude Code guidance: overview, commands      |
| `README.md`            | Project intro: quickstart, prerequisites      |
| `docs/DEVELOPMENT.md`  | Detailed dev guide: services, troubleshooting |

## Cross-link Format

**English files:** Add after the title heading

```markdown
[🇯🇵 日本語版](path/to/file.ja.md)
```

**Japanese files:** Add after the title heading

```markdown
[🇺🇸 English](path/to/file.md)
```

### Cross-link Paths

| English File          | Japanese File             |
| --------------------- | ------------------------- |
| `CLAUDE.md`           | `docs/CLAUDE.ja.md`       |
| `README.md`           | `docs/README.ja.md`       |
| `docs/DEVELOPMENT.md` | `docs/DEVELOPMENT.ja.md`  |

English files link to Japanese with `[🇯🇵 日本語版](path/to/file.ja.md)`.
Japanese files link to English with `[🇺🇸 English](path/to/file.md)`.

## CLAUDE.md Content Requirements

CLAUDE.md は簡潔に保ち、他ドキュメントで参照可能な内容は削除する。

### 含めるべき内容

1. **Blog Philosophy**: このリポジトリ固有の設計思想
2. **Project Overview**: 概要と他ドキュメントへの参照リンク
3. **Environment Configuration**: 3 環境構成図
4. **Release Flow**: CI/CD フロー図
5. **Authentication**: 認証方式
6. **Package Names**: パッケージ名一覧
7. **Key Technical Decisions**: 技術選定
8. **Deployment**: デプロイ情報（概要のみ）
9. **Tool Management**: ツール管理（簡潔に）

### 他ドキュメントへ委譲する内容

| 内容                     | 参照先                 |
| ------------------------ | ---------------------- |
| 開発コマンド             | `just --list`          |
| ディレクトリ構造         | `README.md`            |
| GitHub Secrets           | `docs/SECRETS.md`      |
| CI/CD ワークフロー詳細   | `.github/workflows/`   |

### 簡潔化ルール

- 冗長な記述は削除し、参照リンクを記載
- コマンド一覧は `just --list` で確認可能なため詳細不要
- テーブルは必要最小限の列のみ
- 重複を避け、Claude Code に必要な情報のみを記載

## README.md Content Requirements

1. **Project Title and Description**
2. **Prerequisites**: Homebrew, mise, pnpm
3. **Quick Start**: Bootstrap and dev commands
4. **Documentation Links**: Links to detailed docs
5. **License**

## Workflow

1. Read existing documentation files
2. Read `justfile` to extract command documentation
3. Read `.github/workflows/` to extract required GitHub Secrets
4. Generate English `CLAUDE.md` with all required sections
5. Generate English `README.md`
6. Create `docs/` directory if not exists
7. Generate Japanese translations (`*.ja.md`)
8. Add cross-links to all files
9. Remove old `DEVELOPMENT.md` from root (if moved to docs/)
10. Run `prek run -a` to verify all linting passes

## Translation Guidelines

- Keep code blocks, commands, file paths, and URLs as-is
- Translate prose content naturally
- Maintain consistent terminology
- Keep table structure identical
- Preserve markdown formatting

## Verification

After completion, run:

```bash
prek run -a
```

All checks must pass before considering the task complete.
