---
name: Searching Intelligently
description: Intelligently select and use the most appropriate search tool based on search intent. Use when searching for information, whether web content, local files, locations, or specific data. Automatically chooses between WebSearch, Brave Search, Firecrawl, Desktop Commander, or other search MCPs.
---

# Searching Intelligently

このSkillは、検索対象や意図に応じて最適なSearch MCPを自動的に選択・使用します。

## 利用可能な検索ツール

### 1. Desktop Commander Search（ローカルファイル・コンテンツ検索）
**用途**: プロジェクト内のファイル名・コンテンツ検索
**MCP**: `mcp__desktop-commander__start_search`
**最適な場面**:
- ローカルファイルの検索
- コード内の特定の関数・変数名の検索
- プロジェクト内のパターン検索

### 2. Brave Web Search（一般的なWeb検索）
**用途**: 一般的な情報、ニュース、記事の検索
**MCP**: `mcp__brave-search__brave_web_search`
**最適な場面**:
- 一般的な質問への回答
- 最新ニュースの検索
- 技術記事・ドキュメントの検索
- 幅広い情報収集

### 3. Brave Local Search（場所・ビジネス検索）
**用途**: 物理的な場所、ローカルビジネスの検索
**MCP**: `mcp__brave-search__brave_local_search`
**最適な場面**:
- レストラン、店舗の検索
- "near me"系の検索
- 住所、営業時間、レビューの取得

### 4. Firecrawl Search（詳細なWeb検索＋スクレイピング）
**用途**: 複数サイトからの詳細情報抽出
**MCP**: `mcp__firecrawl__firecrawl_search`
**最適な場面**:
- 特定トピックの深堀り調査
- 複数ソースからの情報収集
- Webページの詳細コンテンツ抽出が必要な場合

### 5. WebSearch（Claude標準Web検索）
**用途**: 基本的なWeb検索（米国のみ）
**Tool**: `WebSearch`
**最適な場面**:
- Brave Searchが利用できない場合のフォールバック
- シンプルな情報検索

## 検索戦略の決定フロー

### ステップ1: 検索対象の識別

ユーザーの質問から以下を判断：

1. **ローカルファイル検索**: "このプロジェクトで"、"コード内の"、"ファイル名" → Desktop Commander
2. **場所検索**: "near me"、"レストラン"、"営業時間"、具体的な地名 → Brave Local Search
3. **一般的な情報**: "最新の"、"ニュース"、"とは"、"方法" → Brave Web Search
4. **詳細調査**: "詳しく"、"比較"、"複数の情報源" → Firecrawl Search
5. **フォールバック**: 上記以外、または他のMCPが失敗 → WebSearch

### ステップ2: 検索の実行

選択したMCPで検索を実行し、結果を評価。

### ステップ3: 必要に応じて追加検索

- 結果が不十分な場合は、別のMCPで補完
- 複数の検索ツールを組み合わせて使用することも可能

## 使用例

詳細な使用例は[examples.md](examples.md)を参照してください。

## 詳細な検索戦略

検索パターン別の詳細な戦略は[search-strategy.md](search-strategy.md)を参照してください。

## ベストプラクティス

### 1. 検索ツールの優先順位

```
ローカル検索優先:
Desktop Commander → (失敗時) 他のツール

Web検索優先:
Brave Web Search → (失敗時) Firecrawl → (失敗時) WebSearch

場所検索:
Brave Local Search → (失敗時) Brave Web Search
```

### 2. 並列検索の活用

関連性のある複数の検索は並列実行で効率化：

```markdown
例: "Next.jsの最新情報とベストプラクティス"
→ Brave Web Search（最新情報） + Firecrawl Search（ベストプラクティス記事）を並列実行
```

### 3. 検索クエリの最適化

各MCPに適した形式でクエリを調整：

- **Desktop Commander**: ファイル名やコード内の具体的なキーワード
- **Brave Web Search**: 自然言語の質問形式
- **Brave Local Search**: "場所名 near 地名"形式
- **Firecrawl Search**: 具体的なトピック・技術用語

## 一般的な検索パターン

### パターン1: 技術情報の検索

**質問例**: "React 19の新機能を教えて"

**戦略**:
1. Brave Web Search で最新情報を取得
2. 必要に応じてFirecrawl Searchで詳細記事を取得

### パターン2: ローカルコード検索

**質問例**: "このプロジェクトでgetUserData関数を使っている場所を探して"

**戦略**:
1. Desktop Commander (content search) で関数名を検索
2. 検索結果からファイル・行番号を特定

### パターン3: 場所検索

**質問例**: "渋谷駅近くのカフェを探して"

**戦略**:
1. Brave Local Search で "カフェ near 渋谷駅" を検索
2. 評価・営業時間・住所を取得

### パターン4: 複合検索

**質問例**: "TypeScriptの型安全なAPIクライアントの実装方法を調べて、このプロジェクトの既存実装も確認したい"

**戦略**:
1. Brave Web Search または Firecrawl Search で実装方法を調査（Web）
2. Desktop Commander でプロジェクト内の既存APIクライアント実装を検索（ローカル）
3. 両方の結果を統合して回答

## トラブルシューティング

### MCPが利用できない場合

1. **Brave Search失敗**: WebSearch にフォールバック
2. **Firecrawl失敗**: Brave Web Search にフォールバック
3. **Desktop Commander失敗**: Grep/Globツールで代替

### 検索結果が不十分な場合

1. **クエリを調整**: より具体的または一般的な表現に変更
2. **別のMCPを試す**: 異なる角度からアプローチ
3. **複数MCPを組み合わせ**: 情報を補完

### 検索が遅い場合

1. **並列実行を活用**: 関連性の低い検索は並列化
2. **結果数を制限**: `limit`パラメータで調整
3. **キャッシュ活用**: Firecrawlの`maxAge`パラメータを使用

## チェックリスト

検索実行前に確認：

- [ ] 検索対象が明確（ローカル/Web/場所）
- [ ] 最適なMCPを選択
- [ ] クエリが各MCPに適した形式
- [ ] 必要に応じて並列実行を計画
- [ ] フォールバック戦略を準備

## 注意事項

### CLAUDE.md グローバル設定との統合

camoneの`.claude/CLAUDE.md`には以下のルールが記載されています：

```markdown
## Web 検索時のルール
Fetch で Web 検索する際には、まず、"Brave-Search MCP サーバー" で検索し、
何らかの理由で "Brave-Search MCP サーバー" が使用できなければ、"WebFetch MCP サーバー" を使用して Web 検索するように。
```

このSkillは上記ルールを遵守し、以下の優先順位で動作します：

1. **第一選択**: Brave Search MCP（`brave_web_search` または `brave_local_search`）
2. **第二選択**: Firecrawl Search MCP（詳細調査が必要な場合）
3. **フォールバック**: WebSearch（Brave Searchが使用できない場合）

### OSS ライブラリ情報取得時の特別ルール

OSSライブラリに関する情報が必要な場合は、**Context7 MCP Server** を優先使用：

```
Context7 MCP Server
  ↓ 利用不可の場合
Brave-Search MCP Server
  ↓ 利用不可の場合
WebFetch MCP Server
```

Context7 の利点：
- 最新の公式ドキュメント
- ライブラリ特化の情報
- API リファレンス

### MCP使用時の叫び

CLAUDE.mdのルールに従い、MCPサーバー使用時は以下の形式で通知します：

```
🌟Claudeは [MCP名] を唱えた！
```

例:
- `🌟Claudeは Brave-Search MCP サーバー を唱えた！`
- `🌟Claudeは Firecrawl MCP サーバー を唱えた！`
- `🌟Claudeは Desktop Commander MCP サーバー を唱えた！`
