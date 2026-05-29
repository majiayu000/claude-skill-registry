# LP Generator (統合ランディングページ生成)

## Description
通常LP、漫画LP、その他のLPタイプを統合した万能LP生成スキル。

## LP Types

### 1. 通常LP (PASCOLA構成)
- Problem (問題提起)
- Agitation (問題の深刻化)
- Solution (解決策)
- Credibility (信頼性)
- Offer (オファー)
- Limitation (限定性)
- Action (行動喚起)

### 2. 漫画LP (8コマ形式)
- 8コマストーリー構成
- キャラクター設計
- ビジュアル重視

### 3. ストーリー型LP
- 共感を呼ぶストーリー
- 感情的なつながり
- 自然な導線

### 4. タイムライン型LP
- ビフォーアフター
- 変化の可視化

## Usage

```
/lp-generator [type] [options]

Types:
  normal  - 通常LP (PASCOLA)
  manga   - 漫画LP (8コマ)
  story   - ストーリー型
  timeline - タイムライン型

Options:
  --product [name]    - 商品/サービス名
  --target [persona]  - ターゲットペルソナ
  --cta [action]      - CTA文言
```

## Examples

```
# 通常LP作成
/lp-generator normal --product "オンラインスクール" --target "30代会社員"

# 漫画LP作成
/lp-generator manga --product "ダイエットサプリ" --target "40代女性"
```

## Output
- HTML/CSSコード
- コピー文案
- 画像プロンプト（gemini-image-generator連携）
