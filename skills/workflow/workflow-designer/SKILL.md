---
name: workflow-designer
description: 複数のSkillsを連動させた一連のワークフローを設計するメタスキル。ユーザー確認ポイント、依存関係、エラー時のフォールバックを含む完全なワークフロー定義を生成。
---

## 目的

複数の Skills を連動させて、一連のワークフローとして設計する。

**ユースケース:**
- 開発ワークフロー（計画→実装→テスト→レビュー）
- PM ワークフロー（憲章→要件→リスク→週次）
- 調査ワークフロー（情報収集→分析→レポート）
- カスタムワークフロー

---

## トリガー語

- 「ワークフローを設計」
- 「スキル連動を作成」
- 「一連の流れを定義」
- 「Skills チェーンを設計」
- 「自動化フローを構築」

---

## 入力で最初に聞くこと

| # | 質問 | 目的 |
|---|------|------|
| 1 | **ワークフロー名**: 何のワークフローですか？ | 識別子として使用 |
| 2 | **ゴール**: 最終的に何を達成しますか？ | 成功基準の定義 |
| 3 | **確認粒度**: `phase_level`/`step_level`/`minimal`？ | チェックポイント設計 |
| 4 | **テンプレート使用**: 既存テンプレートを使うか？ | 開発/PM/調査/カスタム |
| 5 | **推定所要時間**: 全体でどのくらいかかりますか？ | タイムアウト設定の参考 |
| 6 | **制約**: 使用可能なSkills、タイムアウト等の制約は？ | 設計の前提条件 |

**Skills 参照先**: `.agent/registry.md` で利用可能な Skills を確認

---

## 手順

### Phase 1: ワークフロー構造の設計

1. **ゴール分解**
   - 最終ゴールを中間成果物に分解
   - 各成果物に必要な Skill を特定

2. **依存関係マッピング**
   ```
   Skill A → Skill B → Skill C
       ↓
   Skill D (並列実行可能)
   ```

3. **フェーズ分割**
   - 論理的なフェーズに分割
   - フェーズ間にユーザー確認ポイントを配置

### Phase 2: チェックポイント設計

**確認粒度に応じて配置:**

| 粒度 | チェックポイント例 |
|------|-------------------|
| フェーズ単位 | 計画完了後、実装完了後 |
| ステップ単位 | 各Skill実行後 |
| 最小限 | クリティカルな分岐点のみ |

**チェックポイントの種類:**

| 種類 | 説明 | 自動進行 |
|------|------|---------|
| `approval` | ユーザー承認必須 | No |
| `review` | 結果レビュー、問題なければ進行 | Optional |
| `notification` | 通知のみ、自動進行 | Yes |
| `none` | チェックポイントなし | Yes |

**確認粒度 (checkpoint_level) の enum 値:**
- `phase_level`: フェーズ単位で確認
- `step_level`: 各ステップ（Skill実行）後に確認
- `minimal`: クリティカルな分岐点のみ

### Phase 3: エラーハンドリング設計

**各 Skill に対して定義:**

```yaml
error_handling:
  on_failure:
    retry: 2                # 再試行回数
    fallback: skill_x       # 代替 Skill
    escalate: user          # ユーザーに介入要請
  on_stuck:
    threshold: 3            # 同一エラー許容回数
    action: pause           # 一時停止して確認
    escalate: user          # ユーザーに介入要請
```

### Phase 3.5: 条件分岐設計（オプション）

**分岐が必要な場合:**

```yaml
steps:
  - id: check
    skill: verification
  - id: success_path
    skill: finalize
    depends_on: [check]
    condition: "check.result == 'success'"
  - id: failure_path
    skill: debug
    depends_on: [check]
    condition: "check.result == 'failure'"
```

条件分岐は結果に応じて異なるパスを実行する場合に使用。

### Phase 4: ワークフロー定義の生成

**Markdown 形式で出力:**

```markdown
# ワークフロー: {name}

## 概要
- **ゴール**: {goal}
- **推定所要時間**: {estimated_time}
- **確認粒度**: {checkpoint_level}

## フェーズ構成

### Phase 1: {phase_name}
| Step | Skill | 入力 | 出力 | チェックポイント |
|------|-------|------|------|-----------------|
| 1.1 | skill_a | ... | ... | review |
| 1.2 | skill_b | 1.1の出力 | ... | none |

**フェーズ完了条件**: {criteria}
**ユーザー確認**: {checkpoint_type}

### Phase 2: ...

## エラーハンドリング
| Skill | 失敗時 | スタック時 |
|-------|--------|-----------|
| skill_a | retry(2) → fallback | escalate |

## 成功基準
- [ ] {criterion_1}
- [ ] {criterion_2}
```

---

## 成果物

| 成果物 | 必須 | 説明 |
|--------|:----:|------|
| ワークフロー定義書 | Yes | Markdown形式の完全な定義 |
| フロー図（Mermaid） | Optional | 視覚的なフロー図 |
| チェックリスト | Optional | 実行時の確認用 |

---

## 検証

- [ ] 全ての Skills が `.agent/registry.md` に登録されている
- [ ] 依存関係に循環がない
- [ ] チェックポイントが適切に配置されている
- [ ] エラーハンドリング（on_failure, on_stuck）が全 Skill に定義されている
- [ ] 成功基準が測定可能

---

## テンプレート

### 開発ワークフローテンプレート

```
Phase 1: 計画
├─ brainstorming (設計) → review
├─ writing-plans (計画書) → approval
└─ [ユーザー確認: 計画承認]

Phase 2: 実装
├─ codex-cli (コード生成) → review
├─ test-driven-development (テスト) → notification
└─ [ユーザー確認: 実装レビュー]

Phase 3: 検証
├─ systematic-debugging (デバッグ) → notification
├─ verification-before-completion (検証) → approval
└─ [ユーザー確認: 完了承認]
```

### PM ワークフローテンプレート

```
Phase 1: 立ち上げ
├─ project-charter → approval
└─ [ユーザー確認: 憲章承認]

Phase 2: 計画
├─ requirements → review
├─ risk-register → notification
└─ [ユーザー確認: 計画承認]

Phase 3: 実行・監視
├─ weekly-status → notification
├─ meeting-minutes → notification
└─ [定期確認: 週次]
```

### 調査ワークフローテンプレート

```
Phase 1: 情報収集
├─ playwright (Web調査) → notification
├─ dispatching-parallel-agents (並列調査) → review
└─ [ユーザー確認: 調査範囲確認]

Phase 2: 分析
├─ brainstorming (分析) → review
└─ [ユーザー確認: 分析方針確認]

Phase 3: レポート
├─ docx / pptx (レポート生成) → approval
└─ [ユーザー確認: 最終承認]
```

---

## 詳細リファレンス

→ `REFERENCE.md`
