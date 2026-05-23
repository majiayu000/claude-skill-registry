---
name: suno-analyze
description: 曲を設計視点で分析し、analysis/{slug}.mdに保存。曲の本質、構造、コード進行、アレンジメントを言語化する。
allowed-tools: Read Write WebFetch WebSearch
---

# Song Analyzer

曲を設計視点で分析し、再利用可能なテクニックを抽出します。

## 入力

アーティスト名と曲名

例: `YOASOBI アイドル`

## 手順

### 1. 分析ガイドを読む（必須）
```
Read: /Users/takish/Development/music-factory/prompts/analysis-guide.md
```

### 2. 情報を収集する

可能であれば以下を参照:
- 曲のコード進行分析（楽譜サイト、分析ブログ）
- BPM情報
- 曲の構成情報

**情報源の優先順位:**
1. 実際の分析サイト・楽譜サイト
2. WebSearchで見つかる情報
3. LLMの知識（補助）

### 3. 曲を設計視点で分析する

以下のセクションを必ず含める:

1. **曲の本質** - この曲を特別にしている核心（3点）
2. **Music Structure** - 曲展開、Energy Curve、設計意図
3. **Harmony / Chord Progression** - Key、各セクションのコード（ローマ数字）
4. **Arrangement** - ジャンル、楽器構成、密度設計
5. **Lyrics Design** - 視点、主題、言語密度、感情
6. **設計のポイント** - 再利用可能なテクニック
7. **概念キーワード** - 5-7個

### 4. 分析の質を確保する

**良い分析:**
```markdown
## 曲の本質
- **二重構造**: 表層（完璧なアイドル像）/ 内面（虚構・孤独）
- **最大のフック**: 構造そのもの（明るさと不穏さの同居）
- **感情設計**: 語るが、救わない
```

**悪い分析:**
```markdown
- ジャンル: J-Pop
- コード: Am - F - C - G
- 特徴: キャッチーなメロディ
```

→ **なぜそう設計されているか**を言語化する

### 5. 不確かな情報は明記する
```markdown
- **パターン**: i – VI – III – VII（推定）
- **BPM**: 130程度（推定）
```

### 6. slugを決定する

`{artist}_{title}` のASCII形式

例:
- YOASOBI アイドル → `yoasobi_idol`
- あいみょん マリーゴールド → `aimyon_marigold`

### 7. 保存する
```
Write: /Users/takish/Development/music-factory/data/analysis/{slug}.md
```

### 8. 完了報告

- 保存先パス
- 分析した曲の概要（曲の本質の要約）
- 次のアクション: `/suno-pack {slug}`

## 著作権配慮

- コード進行はローマ数字（機能和声）で記述
- 歌詞の直接引用禁止
- メロディの採譜なし
