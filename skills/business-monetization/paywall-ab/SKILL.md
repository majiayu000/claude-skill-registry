---
name: paywall-ab
description: "Anicca Paywall A/B テスト自動クローズドループ。RevenueCat Experiments を使い、Paywall コピーを継続改善する。新規実験セットアップ（Offering作成→Experiment作成→Cron登録）と3日ごと人間確認ループ（チェックイン送信→ユーザー返信待ち→勝者分析→新バリアント生成→Slack承認→RC新実験作成）の両方を担う。Use when: paywall a/b test, paywall experiment, CVR改善, paywall コピー, RevenueCat experiment, paywall-ab, paywall loop, check_in, analyze, create_variant."
user-invocable: true
---

# paywall-ab — Paywall A/B テスト自動クローズドループ

## 概要

RevenueCat Experiments を使った Paywall コピーの自動 A/B テストループ。
エージェントがこのスキルを読めば、セットアップから3日ごとの人間確認ループまで全て実行できる。

| モード | トリガー | やること |
|--------|---------|---------|
| `setup` | 「paywall A/B テストを開始して」 | Offering作成 → AI Paywall生成 → Daisにexperiment作成依頼 → experiment_id受取 → Cron登録 → Slack通知 |
| `check_in` | cron: 実験開始から3日ごと 7:00 JST / 「check_in」 | RC MCP で実験情報取得 → Day N メッセージを Slack に送信 → ユーザー返信を待つ |
| `analyze` | ユーザーが「A勝ち」or「B勝ち」と返信 | 勝者/敗者の Offering テキスト取得 → LLM 分析（なぜ勝ったか）→ 新コピー3パターン生成 → Slack 送信 |
| `create_variant` | ユーザーが「はい」or「1」「2」「3」で選択 | Pencil MCP でテキスト差替え → RC 新 Offering 作成 → Slack 承認ゲート → RC 新 Experiment 作成依頼 |

---

## Multi-App レジストリ（複数アプリ対応）

**このスキルは複数アプリに対応する。アプリ設定は Mac Mini の `apps.json` で管理。**

### apps.json パス
```
/Users/anicca/.openclaw/workspace/paywall-ab/apps.json
```

### 形式
```json
{
  "apps": {
    "anicca": {
      "rc_project_id": "projbb7b9d1b",
      "mixpanel_project_id": 3970220,
      "default_offering_id": "ofrng78a01eb506",
      "monthly_product_id": "prod8eb90326e4",
      "slack_channel": "C091G3PKHL2",
      "active_experiment": {
        "experiment_id": "prexpbac56abf66",
        "variant_a_offering_id": "ofrng78a01eb506",
        "variant_b_offering_id": "ofrng586631f021",
        "start_date": "2026-03-03"
      }
    }
  }
}
```

**新アプリ追加時**: `apps.json` にエントリを追加 → cronメッセージに `app_id: "new_app"` を追加するだけ。

### cronメッセージのフォーマット（アプリ名指定）
```
Run paywall-ab skill in check_in mode.
app_id: anicca
apps_config: /Users/anicca/.openclaw/workspace/paywall-ab/apps.json
```

---

## 現在稼働中の実験（2026-03-03〜）

| 項目 | 値 |
|------|-----|
| app_id | `anicca` |
| experiment_id | `prexpbac56abf66` ⚠️ RC Dashboardで作成後に確認要 |
| Variant A (現行 default) | `ofrng78a01eb506` (anicca) |
| Variant B (AI生成 v2) | `ofrng586631f021` (anicca_paywall_ai_v2) |
| Paywall v2 | `pw5d8ebd3e8a674b3e` |
| cron | 3日ごと 7:00 JST — Mac Mini 登録済み (`enabled: true`) |
| RC Dashboard | `https://app.revenuecat.com/projects/bb7b9d1b/experiments` |

**⚠️ 次のアクション（Dais）:** RC Dashboardで実験を作成してexperiment_idを確認 → cronメッセージのIDを更新

---

## 環境変数（必須）

| Key | 値の場所 |
|-----|---------|
| `REVENUECAT_V2_SECRET_KEY` | Mac Mini `.env` |
| `REVENUECAT_PROJECT_ID` | `projbb7b9d1b`（固定） |
| `OPENAI_API_KEY` | Mac Mini `.env` |
| `SLACK_BOT_TOKEN` | Mac Mini `.env` |
| `SLACK_METRICS_CHANNEL` | `C091G3PKHL2`（#metrics） |

---

## ⚠️ 必須前提：Paywall作成前にアプリコードで実機能を確認すること

**Paywall コピーに嘘を書くことは罪。存在しない機能を訴求してはいけない。**

### 確認必須ファイル（Paywall作成時に必ず読む）

| ファイル | 確認する内容 |
|---------|------------|
| `aniccaios/aniccaios/Services/FreePlanService.swift` | Free の制限（本数・時刻） |
| `aniccaios/aniccaios/Services/LLMNudgeService.swift` | Pro の AI 機能の実体 |
| `aniccaios/aniccaios/Services/NudgeStatsManager.swift` | フィードバック学習の実体 |
| `aniccaios/aniccaios/Models/SubscriptionInfo.swift` | Free/Pro の差分定義 |

### Anicca の実際の Free vs Pro 差分（コードから確認済み）

| 機能 | Free | Pro |
|------|------|-----|
| Nudgeタイプ | ルールベース（事前定義文章） | AI生成（LLMNudgeService） |
| 1日の本数 | **3本固定（8:00/12:30/20:00）** | サーバー制御・高クォータ |
| タイミング | 固定時刻3回 | プロアクティブ配信（その瞬間に必要な時） |
| パーソナライズ | 苦しみカテゴリでローテーション | その人の具体的な悩みに特化したAI生成 |
| フィードバック学習 | なし | 👍/👎で次のNudgeが改善される |

### 訴求禁止リスト（存在しない機能）

| 禁止コピー | 理由 |
|----------|------|
| "30-day insight reports" | コードに存在しない |
| "Progress growth graph" | コードに存在しない |
| "Nudge frequency & timing customization" | ユーザーが手動設定できる機能はない |
| "Streaks / goal completion rate" | 実装されていない |
| "Get full access to all features" | 意味がない |
| "Early releases" / "Premium support" | アプリが提供していない |

### 訴求すべき本物の価値（実機能のみ）

| 訴求軸 | 具体的コピー例 |
|--------|-------------|
| AI生成の深さ | "AI-written nudges, crafted for your exact struggle" |
| フィードバック学習 | "Gets smarter with every reaction you give" |
| プロアクティブ配信 | "Reaches you at the moment you need it most" |
| 仏教の智慧 | "Rooted in centuries of Buddhist wisdom" |
| パーソナライズ | "Knows your specific pain — not generic advice" |

---

## MODE 1: セットアップ（新規実験を作る時）

**現行 default Offering:** `ofrng78a01eb506` (anicca) ← Variant A に使う
**月額 product ID:** `prod8eb90326e4` (ai.anicca.app.ios.monthly、7日トライアル付き)

### Step 1. 新 Offering 作成（エージェントが MCP 実行）

```
mcp__revenuecat__mcp_RC_create_offering:
  project_id: "projbb7b9d1b"
  lookup_key: "anicca_variant_{YYYYMMDD}"
  display_name: "Anicca Variant {date}"
```

### Step 2. パッケージ + Product 紐付け（エージェントが MCP 実行）

```
mcp__revenuecat__mcp_RC_create_package:
  project_id: "projbb7b9d1b"
  offering_id: "<Step1のoffering_id>"
  lookup_key: "$rc_monthly"
  display_name: "Monthly Plan"

mcp__revenuecat__mcp_RC_attach_products_to_package:
  project_id: "projbb7b9d1b"
  package_id: "<package_id>"
  products: [{ product_id: "prod8eb90326e4", eligibility_criteria: "all" }]
```

### Step 3. AI Paywall 自動生成（エージェントが MCP 実行）

```
mcp__revenuecat__mcp_RC_create_design_system_paywall_generation_job:
  project_id: "projbb7b9d1b"
  offering_id: "<Step1のoffering_id>"
  design_system: <Anicca デザインシステム JSON（下記参照）>
→ HTTP 202: { id: "pwj...", status: "queued" }
```

**⚠️ 409エラーが出た場合 → そのOfferingに既にpaywallが存在する。新しいOfferingを作成すること。**

60秒待機後に確認:
```bash
GET https://api.revenuecat.com/v2/projects/projbb7b9d1b/paywalls
→ offering_id が一致するエントリが出たら完了。paywall_id を記録する。
```

### Step 4. Dais に Experiment 作成を依頼（RC API 非対応のため人間のみ可能）

**RC API v2 に Experiment 作成エンドポイントは存在しない（確認済み: 404 resource_missing）。Dashboard のみ。**

エージェントは Slack #metrics に以下を投稿して Dais の操作を待つ:

```
🔧 Paywall A/B テスト準備完了

新しい Paywall が RC に生成されました。
以下の手順で Experiment を作成して、experiment_id をエージェントに教えてください。

1. https://app.revenuecat.com/projects/bb7b9d1b/experiments → New Experiment
2. Variant A: ofrng78a01eb506 (anicca — 現行 default)
3. Variant B: {new_offering_id} ({lookup_key})
4. Traffic split: 50/50 → Start
5. URL に表示される experiment_id (prexpXXXXXXXX) を Claude Code に送ってください

Paywall プレビュー:
https://app.revenuecat.com/projects/projbb7b9d1b/paywalls/{paywall_id}
```

### Step 5. experiment_id 受取 → Cron 登録（エージェントが SSH で実行）

Dais から `prexpXXXXXXXX` を受け取ったら即座に実行:

```bash
# SSH: ssh anicca@100.99.82.95
# ⚠️ ファイル全体上書き禁止。python3 で部分追加のみ。
python3 -c "
import json
with open('/Users/anicca/.openclaw/cron/jobs.json', 'r') as f:
    data = json.load(f)

# 既存チェック（重複防止）
if any(j['id'] == 'paywall-ab' for j in data['jobs']):
    print('ALREADY EXISTS — skip')
    exit(0)

data['jobs'].append({
  'id': 'paywall-ab',
  'agentId': 'anicca',
  'jobId': 'paywall-ab',
  'name': 'paywall-ab',
  'schedule': {'kind': 'cron', 'expr': '0 7 */3 * *', 'tz': 'Asia/Tokyo'},
  'sessionTarget': 'isolated',
  'wakeMode': 'now',
  'payload': {
    'kind': 'agentTurn',
    'message': 'Run paywall-ab skill in check_in mode. app_id: anicca. apps_config: /Users/anicca/.openclaw/workspace/paywall-ab/apps.json'
  },
  'delivery': {'mode': 'none'},
  'enabled': True,
  'state': {}
})

with open('/Users/anicca/.openclaw/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('DONE')
"
```

### Step 6. Slack #metrics に開始通知

```
📊 Paywall A/B テスト開始 🚀

実験ID: {experiment_id}
開始日: {today}

Variant A (現行): ofrng78a01eb506 (anicca)
Variant B (新AI生成): {new_offering_id}
Traffic split: 50/50

📅 初回チェック: {3日後} 7:00 JST
3日ごと 7:00 JST にチェックインします。
```

---

## MODE 2: check_in（3日ごと 7:00 JST 自動実行）

### Step 1. 実験情報を取得

```
1. apps.json を読む → active_experiment の experiment_id, start_date を取得
2. 経過日数を計算: day_n = (today - start_date).days
3. mcp__revenuecat__mcp_RC_list_offerings で Variant A / B の詳細を取得
   → 各 Offering の display_name を取得
```

**⚠️ RC Experiments API は conversion data を返さない（404）。CVR はユーザーが RC Dashboard で確認する。**

### Step 2. Slack #metrics に Day N メッセージを送信

以下のテンプレートで Slack に投稿する:

```
📊 Paywall 実験 Day {N}

実験ID: {experiment_id}
━━━━━━━━━━━━━━━━━━━━
Variant A（現行）: {offering_a_name}
  タイトル: {title_a}
  CTA: {cta_a}

Variant B（テスト中）: {offering_b_name}
  タイトル: {title_b}
  CTA: {cta_b}
━━━━━━━━━━━━━━━━━━━━
📌 RC Dashboard で CVR を確認してください:
https://app.revenuecat.com/projects/projbb7b9d1b/experiments/{experiment_id}

結果を教えてください:
• 「A勝ち」
• 「B勝ち」
• 「まだ早い」（3日後にまた確認）
```

**⚠️ メッセージ送信後は返信を待つ（reactive モード）。急かさない。タイムアウトなし。**

### Step 3. ユーザー返信のルーティング

| 返信内容 | アクション |
|---------|-----------|
| 「まだ早い」 | 何もしない。次の cron（3日後）で同じメッセージを送る |
| 「A勝ち」 | → `analyze` モードを winner="A" で実行 |
| 「B勝ち」 | → `analyze` モードを winner="B" で実行 |

---

## MODE 3: analyze（ユーザーが「A勝ち」or「B勝ち」と返信後）

### Step 1. 勝者/敗者の Offering 詳細を取得

```
入力: winner = "A" or "B"

mcp__revenuecat__mcp_RC_list_offerings(project_id: "projbb7b9d1b")
→ Variant A と B の Offering ID に対応する paywall_id を取得

mcp__revenuecat__mcp_RC_get_app_store_config(project_id: "projbb7b9d1b")
または offering の paywall からテキストを取得
→ 勝者のタイトル・bullets・CTA
→ 敗者のタイトル・bullets・CTA
```

### Step 2. LLM 分析（なぜ勝者のコピーが響いたか）

以下のプロンプトで分析を実行する:

```
あなたは Paywall コピーアナリストです。

## 実験結果
勝者 ({winner}): {winner_offering_name}
  タイトル: {winner_title}
  bullets: {winner_bullets}
  CTA: {winner_cta}

敗者: {loser_offering_name}
  タイトル: {loser_title}
  bullets: {loser_bullets}
  CTA: {loser_cta}

## ユーザーペルソナ
25〜35歳、6〜7年同じ悪習慣が抜けられない、習慣アプリ10個全部3日で諦めた。
自己信頼ゼロ。「どうせ無理」が前提。

## 分析してください（3点）
1. なぜ勝者のコピーが響いたのか（具体的な言語的要因）
2. 敗者のどの要素が弱かったか
3. 次のバリアントで改善すべき1点
```

### Step 3. 新コピー仮説を3パターン生成

以下のプロンプトで生成する:

```
あなたは Paywall コピーライターです。

## アプリ
Anicca（習慣化・行動変容、7日間無料トライアル → $9.99/月）

## 絶対ルール
❌ 訴求禁止（コードに存在しない）:
  - "30-day insight reports", "growth graph", "streaks", "frequency customization"
  - "nudge", "reminder", "notification", "daily reminders"

✅ 訴求すべき実機能:
  - AI生成: その人の悩みに特化したAI生成（Free はルールベース）
  - 適応学習: 👍/👎で次が改善される
  - プロアクティブ: 固定時刻ではなくサーバー起点
  - 仏教の智慧: 何世紀にもわたる仏教の智慧

## 今回の分析
勝者の有効要因: {analysis_key_point}
次の改善点: {improvement_point}

## 3パターンを生成してください
それぞれ異なる訴求軸で。勝者の良い要素を保持しつつ、改善点を適用する。
フォーマット: タイトル(5語以内) + bullets×3(各20文字以内) + CTA固定

出力:
[
  { "pattern": 1, "axis": "訴求軸の説明", "title": "...", "bullets": ["...", "...", "..."], "cta": "Try Free For 1 Week" },
  { "pattern": 2, "axis": "訴求軸の説明", "title": "...", "bullets": ["...", "...", "..."], "cta": "Try Free For 1 Week" },
  { "pattern": 3, "axis": "訴求軸の説明", "title": "...", "bullets": ["...", "...", "..."], "cta": "Try Free For 1 Week" }
]

禁止ワード（含まれていたら再生成）: insight, graph, streak, nudge, reminder, notification, daily, frequency, customize
```

### Step 4. Slack #metrics に分析結果 + 3パターン送信

```
🏆 勝者分析完了

勝者: Variant {winner} ({winner_offering_name})

━━━━━━━━━━━━━━━━━━━━
📊 なぜ勝ったか:
{analysis_point_1}
{analysis_point_2}
{analysis_point_3}
━━━━━━━━━━━━━━━━━━━━

📝 次のバリアント候補（3パターン）:

【パターン 1】訴求軸: {axis_1}
タイトル: "{title_1}"
• {bullet_1_1}
• {bullet_1_2}
• {bullet_1_3}

【パターン 2】訴求軸: {axis_2}
タイトル: "{title_2}"
• {bullet_2_1}
• {bullet_2_2}
• {bullet_2_3}

【パターン 3】訴求軸: {axis_3}
タイトル: "{title_3}"
• {bullet_3_1}
• {bullet_3_2}
• {bullet_3_3}

━━━━━━━━━━━━━━━━━━━━
どのパターンで新しい実験を始めますか？
「1」「2」「3」で教えてください（「なし」で保留）
```

**⚠️ 返信を待つ。急かさない。タイムアウトなし。**

### Step 5. ユーザー返信のルーティング

| 返信 | アクション |
|------|-----------|
| 「1」「2」「3」 | → `create_variant` モードを pattern=N で実行 |
| 「なし」「保留」 | 何もしない。終了 |

---

## MODE 4: create_variant（ユーザーがパターン番号を選択後）

### Step 1. Pencil MCP でペイウォールのテキストを差し替え

**ビジュアル（色・アイコン・レイアウト）は変えない。テキストのみ差し替え。**

```
入力: pattern = 1 or 2 or 3（ユーザーが選んだパターン）
選択されたコピー: { title, bullets, cta }

1. mcp__pencil__open_document で既存ペイウォールを開く
   対象: Anicca ペイウォールの .pen ファイル
   パス: /Users/anicca/.openclaw/workspace/paywall-ab/paywall.pen（存在しない場合は作成不要 → Step 2へ）

2. mcp__pencil__batch_get でテキストノードを取得
3. mcp__pencil__batch_design でタイトル・bullets・CTA のみ差し替え
   - U("title_node_id", { text: new_title })
   - U("bullet_1_id", { text: new_bullet_1 })
   - 等
4. mcp__pencil__get_screenshot でプレビュー確認
```

**⚠️ Pencil の .pen ファイルが存在しない場合は RC AI 自動生成（MODE 1 Step 3）を使用する。**

### Step 2. RC に新 Offering 作成（エージェントが MCP 実行）

MODE 1 の Step 1〜3 を実行する:
- 新 Offering 作成（lookup_key: `anicca_variant_{YYYYMMDD}`）
- パッケージ + Product 紐付け
- AI Paywall 生成（デザインシステム JSON は下記参照）

### Step 3. Slack 承認ゲート（`.cursor/skills/slack-approval/SKILL.md` 参照）

⚠️ **タイムアウトなし。Daisが押すまで永久に待機する。急かさない。**

→ `.cursor/skills/slack-approval/SKILL.md` を読んで `requestApproval()` を実行する

```javascript
const result = await requestApproval({
  channel: 'C091G3PKHL2',
  title:   '📝 新 Paywall バリアント確認',
  detail:  `パターン${pattern}（訴求軸: ${axis}）\n\nタイトル: ${title}\nbullets:\n  • ${bullets[0]}\n  • ${bullets[1]}\n  • ${bullets[2]}\nCTA: ${cta}\n\nこの内容で新 Offering を作成し、実験を開始しますか？`
});
```

| 返答 | アクション |
|------|-----------|
| `approved` | → Step 4（Dais に Experiment 作成依頼）へ |
| `denied` | → analyze モードの Step 3（コピー再生成）に戻る（最大3回） |

### Step 4. Dais に新 Experiment 作成を依頼

**RC API v2 に Experiment 作成エンドポイントは存在しない。Dashboard のみ。**

Slack #metrics に投稿して Dais の操作を待つ:

```
🔧 新 Paywall バリアント準備完了

パターン{N}のペイウォールが RC に生成されました。
以下の手順で新しい Experiment を作成して、experiment_id をエージェントに教えてください。

1. https://app.revenuecat.com/projects/bb7b9d1b/experiments → New Experiment
2. Variant A: {前回の勝者 offering_id}（昇格済み default）
3. Variant B: {new_offering_id} ({lookup_key})
4. Traffic split: 50/50 → Start
5. URL に表示される experiment_id (prexpXXXXXXXX) を Claude Code に送ってください

Paywall プレビュー:
https://app.revenuecat.com/projects/projbb7b9d1b/paywalls/{paywall_id}
```

### Step 5. experiment_id 受取 → apps.json 更新 + cron の Day カウンターリセット

Dais から `prexpXXXXXXXX` を受け取ったら即座に実行:

```bash
# SSH: ssh anicca@100.99.82.95
# apps.json の active_experiment を更新（部分更新のみ）
python3 -c "
import json, datetime
with open('/Users/anicca/.openclaw/workspace/paywall-ab/apps.json', 'r') as f:
    data = json.load(f)

data['apps']['anicca']['active_experiment'] = {
    'experiment_id': '{NEW_EXPERIMENT_ID}',
    'variant_a_offering_id': '{WINNER_OFFERING_ID}',
    'variant_b_offering_id': '{NEW_OFFERING_ID}',
    'start_date': datetime.date.today().isoformat()
}

with open('/Users/anicca/.openclaw/workspace/paywall-ab/apps.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('DONE')
"
```

**⚠️ cron の次回実行日は自動的に「今日から3日後」となる（`0 7 */3 * *` のため手動リセット不要）。**

### Step 6. Slack #metrics に開始通知

```
🚀 新 Paywall 実験開始！

実験ID: {new_experiment_id}
開始日: {today}

Variant A (昇格): {winner_offering_name}（前回の勝者）
Variant B (新パターン{N}): {new_offering_name}
Traffic split: 50/50

訴求軸: {axis}
タイトル: "{new_title}"
• {bullet_1}
• {bullet_2}
• {bullet_3}

📅 次の check_in: {3日後} 7:00 JST
```

---

## Paywall デザインシステム JSON（確定版 — 実機能のみ）

```json
{
  "app_context": {
    "app_name": "Anicca",
    "category": "Health & Fitness / Lifestyle",
    "one_line_description": "AI-powered nudges rooted in Buddhist wisdom to help you change your behavior."
  },
  "brand_identity": {
    "brand_mission": "Reduce suffering through Buddhist wisdom.",
    "brand_personality_archetype": "Sage — wise, calm, compassionate",
    "core_values": ["compassion", "impermanence", "wisdom", "presence"]
  },
  "target_audience": {
    "primary_user_persona": "25–35yo who has struggled with the same bad habit for 6–7 years. Tried 10+ habit apps, all failed.",
    "user_pain_points": [
      "Same struggle for years — can't wake up, stay up scrolling, no willpower",
      "Every habit app failed within 3 days",
      "Deeply low self-trust: 'I know I won't stick to it'"
    ],
    "user_needs_and_goals": [
      "Someone who understands their specific pain — not generic motivation",
      "Guidance that finds them, not something they have to remember to open",
      "Words that feel like they were written for their exact situation"
    ]
  },
  "problem_solution_fit": {
    "problem_statement": "Generic apps give the same advice to everyone. Users feel unseen and give up.",
    "solution_statement": "Anicca Pro uses AI to craft nudges for your exact struggle, learns from your reactions, and reaches you proactively at the right moment.",
    "unique_selling_propositions": [
      "AI writes each nudge for YOUR specific struggle — not copy-pasted advice",
      "Gets smarter with every 👍/👎 you give — adapts to what actually helps you",
      "Reaches you proactively when you need it most — not on a fixed schedule",
      "Grounded in centuries of Buddhist wisdom on suffering and change"
    ]
  },
  "visual_language": {
    "color_palette": {
      "primary_brand_color": "#C9B382",
      "secondary_brand_color": "#2C2A28",
      "accent_cta_color": "#C9B382",
      "background_colors": ["#F5F3ED", "#EDE9E0"],
      "palette_mood": "warm sand, zen rock garden, morning light"
    },
    "typography": {
      "headline_font_family": "SF Pro Display",
      "body_font_family": "SF Pro Text"
    },
    "illustration_and_imagery_style": {
      "primary_style": "zen minimalism — stacked river stones, ripple rings in sand"
    }
  },
  "tone_of_voice": {
    "primary_tone": "calm and wise",
    "secondary_tone": "warm and deeply personal",
    "communication_style_summary": "Speak like a wise, compassionate friend who understands suffering without judgment"
  },
  "content_strategy": {
    "premium_feature_highlights": [
      "AI-written nudges, crafted for your exact struggle — not generic advice",
      "Gets smarter every time you react — 👍/👎 shapes what you receive next",
      "Reaches you at the moment you need it most — proactive, not scheduled",
      "Rooted in centuries of Buddhist wisdom, personalized to your pain"
    ],
    "free_vs_pro_honest_difference": "Free: 3 rule-based nudges/day at fixed times. Pro: AI-generated nudges tailored to your specific struggle, adaptive learning from your reactions, proactive server-triggered delivery."
  },
  "ui_patterns": {
    "button_style": "full-width rounded pill, warm gold #C9B382, white bold text",
    "overall_layout_philosophy": "breathing room — generous padding, single focal point, no clutter"
  }
}
```

### 実績

| バージョン | Offering ID | Paywall ID | 備考 |
|-----------|------------|-----------|------|
| v1 (2026-02-24) | `ofrng4c8d1f9d48` | `pwd08b47e7c59f464d` | ❌ 嘘コピー含む（廃棄） |
| **v2 (2026-02-24)** | **`ofrng586631f021`** | **`pw5d8ebd3e8a674b3e`** | ✅ 実機能のみ（現行 Variant B） |

---

## RevenueCat 接続情報

| 項目 | 値 |
|------|-----|
| Project ID | `projbb7b9d1b` |
| API Base | `https://api.revenuecat.com/v2` |
| MCP ツール | `mcp__revenuecat__mcp_RC_*` |
| RC Dashboard | `https://app.revenuecat.com/projects/bb7b9d1b/` |

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| RC Paywall 409 (already exists) | **新しい Offering を作成する。既存 paywall の上書き不可。** |
| RC Experiment 404 (resource_missing) | RC API は Experiment 作成不可。Dashboard 操作のみ。Dais に依頼。 |
| LLM が禁止ワード含むコピー生成 | 禁止ワードチェック → 再生成（最大3回） |
| Mixpanel セグメント取得失敗 | ユーザーに RC Dashboard の確認を促す |
| Pencil .pen ファイルが存在しない | RC AI 自動生成（MODE 1 Step 3）を代替で使用 |
| slack-approval が応答なし | タイムアウトなし。待つ。急かさない。 |
| 3サイクル以上有意差出ない | 別切り口の新実験を Slack で Dais に提案 |

---

## Changelog

- 2026-02-24: v1.0 初版作成
- 2026-02-24: v1.1 Figma approach 廃棄 → RC AI自動生成に一本化
- 2026-02-24: v1.2 アプリコード確認必須セクション追加。嘘コピー禁止リスト追加
- 2026-02-24: v1.3 v1 paywall廃棄。v2 paywall (`pw5d8ebd3e8a674b3e`) 再生成
- 2026-02-24: v1.4 Candle原則の嘘（30日分析/成長グラフ/頻度調整）を削除し実機能に置換。Mixpanelでのデータ取得フローを追加。slack-approvalタイムアウトなし明記。experiment_id=human操作フロー明確化。cron登録はpython3部分追加のみ（全体上書き禁止）。現在の実験状態セクション追加。
- 2026-02-24: v2.0 **3日ごと人間確認フローに全面刷新。** evaluate モード削除。check_in / analyze / create_variant モード追加。cron スケジュール変更（毎週月曜 9am → 3日ごと 7am）。Human-in-the-loop パターンに移行。
