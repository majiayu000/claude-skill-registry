---
name: note-research
description: note.comのリサーチツール - 非公式API + MCP + WebSearchでゼロコストリサーチ
disable-model-invocation: false
allowed-tools:
  - Bash
  - Read
  - Write
  - WebSearch
  - WebFetch
  - Grep
  - Glob
---

# note-research - ゼロコストnoteリサーチシステム

## 概要

note.comの記事・ユーザー情報を**コストゼロ**で取得するリサーチツール。

```
┌─────────────────────────────────────────────────────────────────────┐
│                NOTE RESEARCH SYSTEM v1.0                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐       │
│  │  note.com     │    │   WebSearch   │    │   WebFetch    │       │
│  │  非公式API    │    │  (Anthropic)  │    │  (直接取得)   │       │
│  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘       │
│          │                    │                    │               │
│          └────────────────────┼────────────────────┘               │
│                               ▼                                    │
│                    ┌─────────────────┐                             │
│                    │   データ統合    │                             │
│                    │   ・記事情報    │                             │
│                    │   ・ユーザー情報│                             │
│                    │   ・トレンド    │                             │
│                    └────────┬────────┘                             │
│                             ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    出力形式                                  │   │
│  │  ・ジャンル別レポート   ・ユーザー別レポート                 │   │
│  │  ・売れ筋分析           ・構成テンプレート抽出               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ✅ APIキー不要  ✅ コストゼロ  ✅ 即座に利用可能                  │
└─────────────────────────────────────────────────────────────────────┘
```

## 使い方

```bash
# ジャンル別リサーチ
/note-research ジャンル=副業

# ユーザー別リサーチ
/note-research ユーザー=@username

# キーワード検索
/note-research キーワード=ChatGPT 活用法

# 売れ筋分析
/note-research 売れ筋 ジャンル=マーケティング

# 構成テンプレート抽出
/note-research テンプレート ジャンル=ビジネス
```

## note.com 非公式API エンドポイント

### 1. ユーザー情報取得

```
GET https://note.com/api/v2/creators/{username}
```

**レスポンス例**:
```json
{
  "data": {
    "id": 12345,
    "urlname": "username",
    "name": "表示名",
    "noteCount": 150,
    "followerCount": 5000,
    "followingCount": 200,
    "profile": "プロフィール文"
  }
}
```

### 2. 記事情報取得

```
GET https://note.com/api/v1/notes/{note_key}
```

**note_keyの取得方法**: URLから抽出
- `https://note.com/username/n/n1234567890ab` → `n1234567890ab`

### 3. タグ別記事一覧

```
GET https://note.com/api/v3/articles?tag={tag_name}&page=1
```

### 4. ユーザーの記事一覧

```
GET https://note.com/api/v2/creators/{username}/contents?kind=note&page=1
```

### 5. 人気記事（トレンド）

```
GET https://note.com/api/v3/trending/notes
```

## 実行フロー

### ジャンル別リサーチ

```
1. WebSearch で note.com 内の記事を検索
   → "site:note.com {ジャンル} 有料記事"
   → "site:note.com {ジャンル} 人気"

2. 上位記事のURLを抽出

3. 各記事の非公式APIで詳細取得
   → スキ数、コメント数、価格

4. WebFetch で記事ページから構成を分析

5. レポート生成
```

### ユーザー別リサーチ

```
1. 非公式API でユーザー情報取得
   → /api/v2/creators/{username}

2. ユーザーの記事一覧取得
   → /api/v2/creators/{username}/contents

3. 各記事の詳細分析

4. ユーザーの強み・パターン分析

5. レポート生成
```

## 実装スクリプト

### Pythonスクリプト（scripts/note_api.py）

```python
import requests
import json
from typing import Optional, List, Dict
import time

class NoteResearcher:
    """note.com 非公式APIリサーチャー"""

    BASE_URL = "https://note.com/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Accept": "application/json",
        })

    def get_user(self, username: str) -> Optional[Dict]:
        """ユーザー情報を取得"""
        url = f"{self.BASE_URL}/v2/creators/{username}"
        try:
            resp = self.session.get(url)
            if resp.status_code == 200:
                return resp.json().get("data")
        except Exception as e:
            print(f"Error: {e}")
        return None

    def get_user_notes(self, username: str, page: int = 1) -> List[Dict]:
        """ユーザーの記事一覧を取得"""
        url = f"{self.BASE_URL}/v2/creators/{username}/contents"
        params = {"kind": "note", "page": page}
        try:
            resp = self.session.get(url, params=params)
            if resp.status_code == 200:
                return resp.json().get("data", {}).get("contents", [])
        except Exception as e:
            print(f"Error: {e}")
        return []

    def get_note(self, note_key: str) -> Optional[Dict]:
        """記事詳細を取得"""
        url = f"{self.BASE_URL}/v1/notes/{note_key}"
        try:
            resp = self.session.get(url)
            if resp.status_code == 200:
                return resp.json().get("data")
        except Exception as e:
            print(f"Error: {e}")
        return None

    def get_trending(self) -> List[Dict]:
        """トレンド記事を取得"""
        url = f"{self.BASE_URL}/v3/trending/notes"
        try:
            resp = self.session.get(url)
            if resp.status_code == 200:
                return resp.json().get("data", [])
        except Exception as e:
            print(f"Error: {e}")
        return []

    def search_by_tag(self, tag: str, page: int = 1) -> List[Dict]:
        """タグで記事を検索"""
        url = f"{self.BASE_URL}/v3/articles"
        params = {"tag": tag, "page": page}
        try:
            resp = self.session.get(url)
            if resp.status_code == 200:
                return resp.json().get("data", [])
        except Exception as e:
            print(f"Error: {e}")
        return []


def research_genre(genre: str) -> Dict:
    """ジャンル別リサーチ"""
    researcher = NoteResearcher()
    results = {
        "genre": genre,
        "trending": [],
        "by_tag": [],
    }

    # トレンド取得
    results["trending"] = researcher.get_trending()

    # タグ検索
    results["by_tag"] = researcher.search_by_tag(genre)

    return results


def research_user(username: str) -> Dict:
    """ユーザー別リサーチ"""
    researcher = NoteResearcher()
    results = {
        "username": username,
        "user_info": None,
        "notes": [],
    }

    # ユーザー情報
    results["user_info"] = researcher.get_user(username)

    # 記事一覧（最大3ページ）
    for page in range(1, 4):
        notes = researcher.get_user_notes(username, page)
        if not notes:
            break
        results["notes"].extend(notes)
        time.sleep(0.5)  # レート制限対策

    return results
```

## レポートテンプレート

### ジャンル別レポート（templates/genre_report.md）

```markdown
# {ジャンル} ジャンル リサーチレポート

**調査日**: {date}
**調査対象**: note.com内 {ジャンル} 関連記事

---

## 概要

- **分析記事数**: {count}件
- **平均スキ数**: {avg_likes}
- **有料記事比率**: {paid_ratio}%

---

## トップ記事

| 順位 | タイトル | 著者 | スキ | 価格 |
|------|---------|------|------|------|
{top_articles_table}

---

## 売れ筋パターン

### タイトルパターン
{title_patterns}

### 価格帯分布
{price_distribution}

### 文字数分布
{char_count_distribution}

---

## 構成テンプレート

### パターン1: 問題解決型
{template_1}

### パターン2: ノウハウ提供型
{template_2}

---

## 推奨アクション

1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}
```

## WebSearch検索パターン

### ジャンル別

```
site:note.com {ジャンル} 有料記事 人気
site:note.com {ジャンル} 売れてる
site:note.com {ジャンル} ベストセラー
site:note.com {ジャンル} おすすめ
```

### 構成・テンプレート

```
site:note.com note 構成 テンプレート
site:note.com 売れる note 書き方
site:note.com note 有料記事 コツ
note記事 構成 黄金パターン
note 書き方 売れる コツ
```

### ユーザー分析

```
site:note.com @{username}
"{username}" note 人気
```

## 出力ディレクトリ

```
research/note/<timestamp>__<query>/
├── input.yaml       # 入力パラメータ
├── raw_data.json    # 取得した生データ
├── analysis.json    # 分析結果
├── report.md        # 最終レポート
└── templates/       # 抽出したテンプレート
```

## 制限事項

1. **レート制限**: 非公式APIは過度なアクセスを避ける（1秒間隔）
2. **認証**: ログイン必須のデータは取得不可
3. **価格情報**: 有料記事の本文は取得不可（メタデータのみ）

## 関連スキル

- `research-free` - 汎用WebSearchリサーチ
- `mega-research` - API統合リサーチ（要APIキー）
- `keyword-free` - キーワード抽出
