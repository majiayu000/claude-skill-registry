---
name: root-cause-challenge-pattern
description: "Use when evaluating whether a new feature, dependency, or abstraction is truly needed. 5-step root cause challenge."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Root Cause Challenge Pattern - 機能要求の真の動機を問う

**Extracted:** 2026-02-09
**Context:** 新機能・アーキテクチャ変更・依存追加などの意思決定時

## Problem

表面的な理由で機能追加・アーキテクチャ変更を進めると:
- 真の価値を見誤る
- 技術的好奇心やサンクコストに引きずられる
- より高いROIの代替案を見逃す
- 長期的なメンテナンス負債を作る

## Solution: 5ステップの根本原因チャレンジ

### Step 1: 論理的矛盾を探す

提案されたアーキテクチャ判断に矛盾がないかチェック:
- "なぜAは却下でBは承認なのか？"
- "基準は一貫しているか？"
- "コスト効率は合理的か？"

**例（このセッションより）:**
```
Batch API: $5節約のために250行 → ❌却下
OpenAI Provider: $10活用のために750行 → ✅承認

矛盾: LOC/$ 比率が OpenAI Provider の方が悪いのに承認されている
→ 表面的理由（$10クレジット）が本当の動機ではない可能性
```

### Step 2: 根本的な問いを投げる

実装方法でなく、**存在意義**を問う:
- "そもそもこの機能は必要か？"
- "誰が本当に求めているか？"
- "解決しようとしている問題は実在するか？"
- "ツールは既に動いている。これは本当に足りない機能か？"

### Step 3: Architectに忌憚ない評価を求める

**重要:** 単なる実装判断でなく、**本質的価値の評価**を依頼:

```markdown
## Your Task

Answer the fundamental question: Should we build this feature at all?

Be brutally honest. The user wants candid feedback for growth, not validation.

### Evaluate:

1. **True ROI** - Is the return worth the investment?
   - Investment: Code complexity, maintenance burden
   - Return: Concrete value (NOT time estimates)

2. **Real motivations** - What's driving this? (be honest)
   - Stated reason vs actual reason
   - Technical curiosity? Architecture appeal? Sunk cost?

3. **Alternative uses of effort** - What else could be built?
   - Focus on value delivered, not time estimates

4. **Honest scenarios** - Will this actually be used?
   - Usage frequency: Every time? Sometimes? Rarely?

### Important
- Challenge the premise
- Consider opportunity cost
- Check for YAGNI violations
- DO NOT base ROI on time estimates (they're unreliable)
```

### Step 4: 代替案と比較

同じ複雑性レベルで何ができるか列挙:
- より高い価値を提供する機能
- 既知のバグ修正
- UX改善
- 技術的負債の返済

**価値比較表を作る（時間見積もりは使わない）:**
| 機能 | 複雑性 | 価値 | 使用頻度 | 新機能 or 改善 |
|------|--------|------|----------|---------------|
| 提案機能 | 高 | ？ | 低 | 新機能 |
| 代替案A | 高 | 高 | 毎回 | 新機能 |
| 代替案B | 中 | 中 | 時々 | 改善 |
| 代替案C | 低 | 低 | 毎回 | バグ修正 |

**評価基準:**
- **複雑性**: 低/中/高（コード量、依存、テスト負荷）
- **価値**: 解決する問題の大きさ
- **使用頻度**: 毎回/時々/稀（どれだけ恩恵を受けるか）
- **種別**: 新機能/改善/バグ修正

### Step 5: サンクコストを切り捨てる

既に投資した労力（リサーチ、ドキュメント作成）は判断材料にしない:
- "既に調査したから実装しないともったいない" ← サンクコストの罠
- 正しい問い: "今ゼロから始めるとして、これを優先するか？"

## Example (from pdf2anki OpenAI support session)

### 状況
- OpenAI API対応を計画（$10クレジット活用のため）
- 実装規模: ~1,000行、テスト移行209箇所

### Step 1: 矛盾発見
- ユーザー: "Batch APIは$5で却下なのに、OpenAIは$10で承認？矛盾してない？"

### Step 2: 根本を問う
- "そもそもOpenAI対応自体をやるべきか？"

### Step 3: Architectに評価依頼
- "忌憚ない意見をもらうことが私を最も成長させる"
- Architect評価:
  - 投資: ~1,000行、複雑な抽象化層、永続的なメンテナンス負債
  - リターン: $10クレジット消費（一度きり）
  - 真の動機: 技術的好奇心、アーキテクチャの美しさ、サンクコスト
  - 使用頻度予測: 1-2回試して終わり（Claudeの方が日本語で優秀）
  - 判定: **やるべきでない**

### Step 4: 代替案

| 機能 | 複雑性 | 価値 | 頻度 |
|------|--------|------|------|
| OpenAI対応 | 高（1,000行） | 低（$10消費） | 稀（1-2回） |
| 画像認識カード | 高（新API統合） | 高（新カテゴリ対応） | 毎回（図表PDF） |
| インタラクティブTUI | 中（UI実装） | 中（UX改善） | 毎回（全セッション） |
| プロンプト評価FW | 中（eval実装） | 中（品質向上） | 時々（改善時） |
| トークン推定修正 | 低（ロジック修正） | 低（精度向上） | 毎回（日本語） |

**明らかに優先度の高い代替案が複数存在**

### Step 5: 決断
- OpenAI対応をスキップ
- 4つの高価値機能に投資
- サンクコスト（3つのドキュメント、数時間のリサーチ）を切り捨て

**結果:** 同じ複雑性レベルで遥かに高い価値を獲得

## When to Use

以下の場面で**必ず**このパターンを適用:

1. **新機能の追加** - "これ欲しい"と思った時
2. **アーキテクチャ変更** - "きれいにリファクタリングしたい"と思った時
3. **依存の追加** - "このライブラリ便利そう"と思った時
4. **抽象化の導入** - "将来拡張できるように..."と思った時

**特に警戒すべきトリガーワード:**
- "将来のために..."（YAGNI違反の可能性）
- "きれいな設計..."（過剰設計の可能性）
- "せっかく調査したから..."（サンクコスト）
- "$Xのクレジットが余ってる..."（アンカリング効果）
- "すぐできる"（時間見積もりは当てにならない）

## Key Insight: 時間見積もりは使わない

**重要:** AIアシスタントの時間見積もりは不正確なため、ROI計算に使用しない。

代わりに評価すべき指標:
- **コード量**: 行数、ファイル数（複雑性の指標）
- **テスト負荷**: テスト数、モック箇所（保守コスト）
- **依存追加**: 新しい外部依存の数（リスク）
- **具体的価値**: 金額、ユーザー数、使用頻度（測定可能な価値）
- **問題の実在性**: 既存のバグ？ユーザー要望？推測？

## Related Patterns

- YAGNI (You Aren't Gonna Need It)
- Sunk Cost Fallacy
- Opportunity Cost Analysis
- "Don't Import the Warehouse for a Single Wheel"

## Anti-Patterns to Avoid

1. **"Architectural Vanity"** - きれいな抽象化のために実装
2. **"Feature Completionism"** - 使われない機能を完全性のために追加
3. **"Credit Anchoring"** - 無料クレジットを使い切ることが目的化
4. **"Research Justification"** - 調査コストを正当化するための実装
5. **"Time-Based ROI"** - 不確実な時間見積もりでROIを計算

## Success Story

このパターンを適用したpdf2ankiプロジェクトでは:
- ❌ 削減: OpenAI対応（~1,000行、低価値、稀な使用）
- ✅ 選択: 画像認識、TUI、評価FW、バグ修正（同等の複雑性、高価値、頻繁な使用）
- 結果: プロジェクトの価値を最大化する正しい意思決定
