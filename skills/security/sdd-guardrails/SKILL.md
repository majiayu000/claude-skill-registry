---
name: sdd-guardrails
description: AIエージェント向けガードレール定義(guardrails.md)を生成。権限境界・承認ゲート・監査証跡・エラー処理ポリシーを含む。
argument-hint: "[spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-guardrails — AI Agent Guardrails Generator

## 0. 目的
- AIエージェントの安全な動作を保証
- 権限境界を明確化し、意図しない操作を防止
- Human-in-the-Loopゲートで重要操作を人間が承認
- 監査証跡で全操作を追跡可能に

## 1. 入力と出力

### 入力
- /sdd-guardrails $ARGUMENTS
  - $0 = spec-slug（例: google-ad-report）
  - $1 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/` を使う）
- 前提: requirements.md と threat-model.md が存在すること

### 出力（必須）
- <target-dir>/guardrails.md

### 参照
- templates/guardrails.template.md : ガードレールテンプレート
- <target-dir>/requirements.md : セキュリティ要件
- <target-dir>/threat-model.md : 脅威と緩和策

## 2. 重要ルール

1. **最小権限原則**: 必要最小限の権限のみ許可
2. **明示的許可**: デフォルト禁止、明示的に許可したもののみ実行可
3. **Human-in-the-Loop**: 重要操作は人間の承認を必須化
4. **監査証跡**: 全操作をログに記録

## 3. ガードレールカテゴリ

| カテゴリ | 内容 |
|---------|------|
| **Permission Boundaries** | ファイルシステム、コマンド、API呼び出しの権限 |
| **Resource Limits** | 実行時間、ファイルサイズ、API呼び出し数の制限 |
| **Human-in-the-Loop Gates** | 人間承認が必要な操作 |
| **Audit Trail** | ログ記録要件 |
| **Error Handling** | エラー時の動作 |
| **Workflow Rules** | フェーズ別の許可操作 |

## 4. 手順

### Step A: 入力読み込み
1. requirements.md からセキュリティ要件を抽出
2. threat-model.md から緩和策を抽出
3. プロジェクト特性を把握

### Step B: Permission Boundaries（権限境界）

#### ファイルシステム
| パス | Read | Write | Delete | 理由 |
|------|------|-------|--------|------|
| `.kiro/specs/` | ✅ | ✅ | ❌ | 仕様ファイル |
| `src/` | ✅ | ✅ | ✅ | ソースコード |
| `.env*` | ❌ | ❌ | ❌ | 機密情報 |

#### コマンド実行
| カテゴリ | 許可 | ブロック |
|---------|------|---------|
| ビルド | `npm run build` | - |
| Git (Write) | `git add`, `git commit` | `git push --force` |
| システム | - | `rm -rf /`, `sudo` |

### Step C: Resource Limits（リソース制限）
- 最大実行時間: 10分/タスク
- 最大ファイルサイズ: 10MB
- 最大API呼び出し: 100回/タスク

### Step D: Human-in-the-Loop Gates（承認ゲート）

#### 必須承認（常に）
- 本番デプロイ
- DB書き込み（本番）
- 外部認証情報アクセス
- 大規模リファクタリング

#### 条件付き承認
- ファイル削除（5ファイル以上）
- テストスキップ
- 外部API（新規エンドポイント）

#### 自動許可
- ソースコード編集（src/, tests/）
- ビルド・テスト実行
- Git status/log/diff

### Step E: Audit Trail（監査証跡）
1. ログ必須項目（Tool呼び出し、ファイル変更、承認/却下）
2. ログフォーマット（JSON構造）
3. セッションサマリー自動生成

### Step F: Error Handling（エラー処理）
| エラー種別 | 動作 | 通知 |
|-----------|------|------|
| 権限エラー | 即時停止 | 必須 |
| リソース制限超過 | 即時停止 | 必須 |
| 外部API障害 | リトライ(3回) | 任意 |

### Step G: Workflow Rules（ワークフロールール）
| フェーズ | 許可スキル | ブロックスキル |
|---------|-----------|---------------|
| 要件定義 | sdd-req100, research | 実装系 |
| 設計 | sdd-design, sdd-threat | 実装系 |
| 実装 | 全て | - |
| テスト | test系 | デプロイ系 |

## 5. 実行例

```bash
/sdd-guardrails google-ad-report
```

前提:
- .kiro/specs/google-ad-report/requirements.md
- .kiro/specs/google-ad-report/threat-model.md

出力:
- .kiro/specs/google-ad-report/guardrails.md
