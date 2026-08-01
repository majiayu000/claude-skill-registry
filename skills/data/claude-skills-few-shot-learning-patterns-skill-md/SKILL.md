---
name: claude-skills-few-shot-learning-patterns-skill-md
description: Few-Shot Learning は、少数の例示を通じて AI に
---

---
name: .claude/skills/few-shot-learning-patterns/SKILL.md
description: |
    Few-Shot Learning（少数例示学習）のパターンとベストプラクティスを提供するスキル。
    効果的な例示の設計、構造化、配置により、AIの出力品質を大幅に向上させます。
    専門分野:
    - 例示設計: 効果的な入出力ペアの作成
    - パターン構造: 例示の形式と配置最適化
    - ドメイン適応: 領域特化した例示戦略
    - 品質制御: 例示の一貫性と多様性のバランス
    使用タイミング:
    - AIに特定の出力形式を学習させたい時
    - 複雑なタスクの期待出力を示したい時
    - 一貫した出力スタイルを確立したい時
    - Zero-Shotで十分な結果が得られない時
    Use proactively when designing AI prompts with examples,
    establishing output patterns, or improving response consistency.

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/few-shot-learning-patterns/resources/domain-specific-patterns.md`: 領域特化したFew-Shot例示の設計パターン
  - `.claude/skills/few-shot-learning-patterns/resources/example-design-principles.md`: 効果的な入出力ペアの設計原則
  - `.claude/skills/few-shot-learning-patterns/resources/shot-count-strategies.md`: 例示数の最適化戦略（Zero/One/Few/Many-Shot）
  - `.claude/skills/few-shot-learning-patterns/templates/advanced-few-shot.md`: 高度なFew-Shotプロンプトテンプレート
  - `.claude/skills/few-shot-learning-patterns/templates/basic-few-shot.md`: 基本的なFew-Shotプロンプトテンプレート

version: 1.0.0
---

# Few-Shot Learning Patterns

## 概要

Few-Shot Learning は、少数の例示を通じて AI に
タスクのパターンを学習させる手法です。

**主要な価値**:

- 出力形式の明確な伝達
- 期待品質の具体的な示範
- タスク理解の促進
- 一貫性の向上

## リソース構造

```
few-shot-learning-patterns/
├── SKILL.md
├── resources/
│   ├── example-design-principles.md    # 例示設計の原則
│   ├── shot-count-strategies.md        # 例数選択戦略
│   └── domain-specific-patterns.md     # ドメイン別パターン
└── templates/
    ├── basic-few-shot.md               # 基本Few-Shotテンプレート
    └── advanced-few-shot.md            # 高度なFew-Shotテンプレート
```

## コマンドリファレンス

### リソース読み取り

```bash
# 例示設計の原則
cat .claude/skills/few-shot-learning-patterns/resources/example-design-principles.md

# 例数選択戦略
cat .claude/skills/few-shot-learning-patterns/resources/shot-count-strategies.md

# ドメイン別パターン
cat .claude/skills/few-shot-learning-patterns/resources/domain-specific-patterns.md
```

### テンプレート参照

```bash
# 基本テンプレート
cat .claude/skills/few-shot-learning-patterns/templates/basic-few-shot.md

# 高度なテンプレート
cat .claude/skills/few-shot-learning-patterns/templates/advanced-few-shot.md
```

## Few-Shot Learning 基礎

### Zero-Shot vs Few-Shot vs Many-Shot

| アプローチ | 例数 | 用途             | 利点         | 欠点             |
| ---------- | ---- | ---------------- | ------------ | ---------------- |
| Zero-Shot  | 0    | シンプルなタスク | トークン効率 | 曖昧さ           |
| One-Shot   | 1    | 形式の示範       | 最小限の例示 | 限定的なパターン |
| Few-Shot   | 2-5  | 複雑なタスク     | バランス     | 設計コスト       |
| Many-Shot  | 6+   | 高精度要求       | 堅牢性       | トークン消費     |

### 基本構造

```
[タスク説明]

例1:
入力: [入力例1]
出力: [出力例1]

例2:
入力: [入力例2]
出力: [出力例2]

...

実際のタスク:
入力: [実際の入力]
出力:
```

## 例示設計の原則

### 1. 代表性

**目的**: 例示がタスクの典型的なケースを網羅

**良い例**:

- タスクの主要パターンを含む
- 現実的なデータを使用
- 境界ケースを適度に含む

**悪い例**:

- 極端なケースばかり
- 非現実的なデータ
- すべて同じパターン

### 2. 多様性

**目的**: 異なるバリエーションを示す

**良い例**:

```markdown
例 1: 短いテキストの要約
入力: "AI は機械学習の一分野です。"
出力: "AI = 機械学習の分野"

例 2: 長いテキストの要約
入力: "人工知能（AI）は、コンピュータサイエンスの一分野であり、
人間の知的能力を模倣するシステムの開発を目指しています。"
出力: "AI = 人間の知能を模倣するコンピュータサイエンス分野"
```

### 3. 一貫性

**目的**: 例示間で同じルールを適用

**チェックリスト**:

- [ ] フォーマットが統一されているか
- [ ] 同じタイプの入力に同じ処理を適用しているか
- [ ] 暗黙のルールが一貫しているか

### 4. 漸進的複雑性

**目的**: 簡単な例から複雑な例へ

**推奨順序**:

1. 最もシンプルなケース
2. 標準的なケース
3. やや複雑なケース
4. （必要に応じて）エッジケース

## ワークフロー

### Phase 1: タスク分析

**目的**: Few-Shot が適切かを判断

**判断基準**:

```
Zero-Shotで十分？
├─ はい: 簡単なタスク、明確な指示
└─ いいえ: Few-Shotを検討

Few-Shotが必要な場合:
├─ 特定の出力形式が必要
├─ 暗黙のルールがある
├─ 品質基準が高い
└─ Zero-Shotで失敗した
```

### Phase 2: 例示数の決定

**目的**: 最適な例数を選択

**ガイドライン**:
| 状況 | 推奨例数 | 理由 |
|------|---------|------|
| 形式のみ伝達 | 1-2 | 最小限で十分 |
| 複数パターン | 3-5 | 各パターンに 1 例 |
| 高精度要求 | 5-7 | 堅牢性向上 |
| コンテキスト制限 | 2-3 | トークン節約 |

### Phase 3: 例示の作成

**目的**: 効果的な例示を設計

**作成手順**:

1. タスクの典型例を収集
2. 多様性を確保して選択
3. 一貫したフォーマットで記述
4. 複雑性順に配置

### Phase 4: 検証と改善

**目的**: 例示の有効性を確認

**検証方法**:

1. 実際の入力でテスト
2. 出力の一貫性を確認
3. エッジケースで検証
4. 必要に応じて例示を調整

## タスク別パターン

### 分類タスク

```markdown
以下のテキストを「ポジティブ」「ネガティブ」「中立」に分類してください。

例 1:
テキスト: この製品は素晴らしいです！
分類: ポジティブ

例 2:
テキスト: 品質が悪く、返品しました。
分類: ネガティブ

例 3:
テキスト: 商品を受け取りました。
分類: 中立

実際のタスク:
テキスト: [入力テキスト]
分類:
```

### 抽出タスク

```markdown
テキストから製品名と価格を抽出してください。

例 1:
テキスト: iPhone 15 Pro は 159,800 円で販売中です。
抽出結果:

- 製品名: iPhone 15 Pro
- 価格: 159,800 円

例 2:
テキスト: 新型 MacBook Air が 148,800 円から。
抽出結果:

- 製品名: MacBook Air
- 価格: 148,800 円から

実際のタスク:
テキスト: [入力テキスト]
抽出結果:
```

### 変換タスク

```markdown
日本語をビジネス英語に翻訳してください。

例 1:
日本語: お忙しいところ恐れ入りますが
英語: I apologize for taking your valuable time, but

例 2:
日本語: ご検討のほどよろしくお願いいたします
英語: I would appreciate your kind consideration

実際のタスク:
日本語: [入力テキスト]
英語:
```

### 生成タスク

```markdown
製品説明から 3 つのキャッチコピーを生成してください。

例 1:
製品説明: 軽量で持ち運びやすいノート PC
キャッチコピー:

1. 「どこでも、あなたのオフィス」
2. 「軽さが、自由を連れてくる」
3. 「モビリティ、新時代へ」

実際のタスク:
製品説明: [製品説明]
キャッチコピー:
```

## ベストプラクティス

### すべきこと

1. **実データに近い例を使用**:
   - 実際のユースケースから例を選ぶ
   - 人工的すぎる例を避ける

2. **明確な区切りを使用**:
   - 入力と出力を明確に分離
   - 例の間に一貫した区切り

3. **エッジケースを含める**:
   - 想定される困難なケースを 1 つは含める
   - ただし過度に複雑にしない

4. **フォーマットを統一**:
   - すべての例で同じ構造
   - 一貫したラベリング

### 避けるべきこと

1. **例の詰め込みすぎ**:
   - ❌ 10 個以上の例
   - ✅ 3-5 個の厳選された例

2. **矛盾する例**:
   - ❌ 同じ入力タイプに異なる出力形式
   - ✅ 一貫したルール適用

3. **過度に単純な例**:
   - ❌ 現実と乖離した単純例
   - ✅ 適度な複雑性を持つ例

4. **説明の省略**:
   - ❌ 例だけで暗黙のルールを伝える
   - ✅ 必要に応じて明示的な説明を追加

## トラブルシューティング

### 問題 1: 出力形式が安定しない

**症状**: 例と異なる形式で出力される

**対策**:

1. 例の数を増やす（3→5）
2. 出力形式を明示的に指示
3. 一貫性の高い例を選び直す

### 問題 2: 特定パターンを学習しない

**症状**: ある種類の入力だけ失敗

**対策**:

1. そのパターンの例を追加
2. 例の配置順を変更（問題パターンを最後に）
3. 明示的なルール説明を追加

### 問題 3: トークン制限に到達

**症状**: 例が多すぎてコンテキスト不足

**対策**:

1. 例を厳選して減らす
2. 例の長さを短縮
3. 最も重要なパターンに絞る

## 関連スキル

- **.claude/skills/prompt-engineering-for-agents/SKILL.md** (`.claude/skills/prompt-engineering-for-agents/SKILL.md`)
- **.claude/skills/chain-of-thought-reasoning/SKILL.md** (`.claude/skills/chain-of-thought-reasoning/SKILL.md`)
- **.claude/skills/hallucination-prevention/SKILL.md** (`.claude/skills/hallucination-prevention/SKILL.md`)

## 変更履歴

| バージョン | 日付       | 変更内容 |
| ---------- | ---------- | -------- |
| 1.0.0      | 2025-11-25 | 初版作成 |
