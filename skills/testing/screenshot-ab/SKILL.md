---
name: screenshot-ab
description: App Store スクリーンショット A/B テスト自動クローズドループ。メトリクス確認 → 勝者判定 → ヘッドライン生成（生成→採点→改善ループ）→ l.md Bible（make generate-store-screenshots）でPNG生成 → visual-qa採点 → Slackにダイスへ送る → ASCアップロード → PPO実験作成。Use when running screenshot-ab, App Store screenshot experiment, screenshot loop, スクショA/Bテスト, screenshot closed loop, screenshot automation, A/B test screenshots.
---

# screenshot-ab

App Store スクリーンショット A/B テストを自動で回すクローズドループスキル。
**外部スキル依存ゼロ。このスキル1つで完結。**

## 初回セットアップ（新規ユーザー）

→ `references/setup.md` を読む

---

## PHASE 0: アプリ情報を確認する（必須 — スキップ禁止）

**App ID はハードコードしない。毎回 asc CLI で確認する。**

```bash
# App ID を取得
asc apps list --output table

# 対象アプリの App ID を確認して以降の変数に使う
APP_ID="<確認した数字のID>"  # 例: 6755129214（Anicca）

# サポートしているロケール（言語）を確認
asc localizations list --version-id "$(asc versions list --app ${APP_ID} --platform IOS --state READY_FOR_SALE --output json | python3 -c 'import sys,json; print(json.load(sys.stdin)["data"][0]["id"])')" --output table
```

**ロケール確認が最重要。**

| ロケール | やること |
|---------|---------|
| en-US のみ | en-US の英語スクショだけ生成・アップロード |
| ja のみ | ja の日本語スクショだけ生成・アップロード |
| en-US + ja 両方 | **必ず両方のロケールでスクショを生成・アップロードする** |
| それ以外 | 全ロケール分生成・アップロード |

**Anicca は en-US + ja の2ロケール。両方に対応したスクショを作ること。**

---

## パス（環境によって切り替え）

| 環境 | experiments.json |
|------|-----------------|
| **MacBook（ローカルテスト）** | `/Users/cbns03/Downloads/anicca-project/.cursor/plans/ios/1.6.3/screenshot-ab-pil/experiments.json` |
| **Mac Mini（Anicca 本番）** | `/Users/anicca/.openclaw/workspace/screenshot-ab/experiments.json` |
| **screenshots.yaml** | `docs/screenshots/config/screenshots.yaml` |
| **raw PNG 出力先** | `docs/screenshots/raw/` |
| **processed PNG 出力先** | `docs/screenshots/processed/` |

---

## PHASE 1: メトリクス確認

```bash
cat <experiments.json のパス>
```

`current.experiment_id` を取得して CVR を確認する。

```bash
asc product-pages experiments treatments list --experiment-id "{experiment_id}"
```

**判断:**

| 条件 | アクション |
|------|-----------|
| experiment_id なし | → PHASE 3（新実験を始める） |
| 経過 < 7日 | → EXIT（今日はスキップ） |
| Treatment CVR > Control CVR × 1.2 かつ 7日+ | → WINNER → PHASE 2 |
| Treatment CVR <= Control CVR かつ 14日+ | → NULL → PHASE 2 |
| 90日経過 | → NULL → PHASE 2 |

---

## PHASE 2: 実験ログ更新

`experiments.json` の `history` に追記する。

```json
{
  "current": {},
  "history": [
    {
      "experiment_id": "ppo_abc123",
      "headline": "6 Years. 10 Apps. Still Nothing Changed.",
      "result": "WINNER",
      "control_cvr": 2.1,
      "treatment_cvr": 3.2,
      "days_ran": 9,
      "ended_at": "2026-02-23"
    }
  ]
}
```

勝ちパターン・負けパターンを `winning_patterns` / `losing_patterns` に追記して PHASE 3 に渡す。

---

## PHASE 3: ヘッドライン生成（全ロケール分）

→ `references/headline-gen.md` を読んでループを実行する

**入力:** `winning_patterns`, `losing_patterns`, ペルソナ定義
**出力:** screen1/screen2/screen3 の確定ヘッドライン（8/10 以上）× **サポートするロケール数分**

**重要: ロケールごとに別のコピーを生成する。**

| ロケール | ヘッドライン言語 | サブテキスト言語 |
|---------|---------------|---------------|
| `en-US` | 英語 | 英語 |
| `ja` | 日本語 | 日本語 |

**日本語スクショを en-US Treatment にアップロードしない。** ロケールとスクショの言語を必ず一致させること。

---

## PHASE 4: スクショ生成（全ロケール分 — ロケールごとに繰り返す）

**Step 4-1: screenshots.yaml のヘッドラインをロケールごとに更新する**

→ `references/pipeline.md` の「screenshots.yaml 完全版」を参照
各ロケールのヘッドラインを `caption.title` / `caption.subtitle` に書き込む。

**Step 4-2: raw スクリーンショット確認**

```
docs/screenshots/raw/screen1.png, screen2.png, screen3.png が存在するか確認。
なければ: make capture-only で XCUITest 撮影だけ実行（UI は変えない）。
```

**Step 4-3: ロケールごとに pencil_export.py で合成**

```bash
# ja（日本語）
python3 docs/screenshots/scripts/pencil_export.py --locale ja
# → 出力: docs/screenshots/processed/ja/screen1~3.png

# en-US（英語）
python3 docs/screenshots/scripts/pencil_export.py --locale en-US
# → 出力: docs/screenshots/processed/en-US/screen1~3.png
```

**pencil_export.py がロケール引数をサポートしていない場合:**
`screens` 配列のヘッドライン・サブテキストを当該ロケールの文言に書き換えてから実行し、出力先を `processed/{locale}/` に変更する。

内部処理:
1. `raw/screen1~3.png` を PhoneMockup に配置（LANCZOS リサイズ）
2. CaptionArea に当該言語のヘッドライン・サブテキストを描画
3. PhoneMockup に角丸ボーダー追加

**出力（ロケール別）:**
```
docs/screenshots/processed/
├── ja/
│   ├── screen1.png  （780×1688 @2x → Step 7-1 で 1290×2796 にリサイズ）
│   ├── screen2.png
│   └── screen3.png
└── en-US/
    ├── screen1.png
    ├── screen2.png
    └── screen3.png
```

---

## PHASE 5: visual-qa 採点

→ `references/visual-qa.md` を読んで採点プロンプトを使う

`processed/` の PNG 3枚を vision model で採点する。

| 結果 | アクション |
|------|-----------|
| PASS（40/50+） | → PHASE 6 へ |
| FAIL（39/50以下） | → PHASE 3 に戻る（最大3回） |
| 3回連続 FAIL | → Slack に警告 → EXIT |

---

## PHASE 6: Slack 承認（ダイスが確認）

**Step 6-1: processed/ の PNG 3枚を Slack C091G3PKHL2 にアップロード**

Slack Files v2 API（BOT_TOKEN は `.env` の `SLACK_BOT_TOKEN`）:
```
1. files.getUploadURLExternal（GET, query params: filename, length）
2. PUT upload_url にファイルバイナリ送信
3. files.completeUploadExternal（POST, JSON: files=[{id, title}], channel_id）
```

**Step 6-2: slack-approval スキルで ✅/❌ 承認ボタン送信**

→ `.claude/skills/slack-approval/SKILL.md` を読んで `requestApproval()` を実行する

```javascript
const result = await requestApproval({
  channel: 'C091G3PKHL2',
  title:   '📸 App Store スクリーンショット確認',
  detail:  `ヘッドライン: {headline}\nvisual-qa: {score}/50\nASCアップロードに進みますか？`
});
```

| 返答 | アクション |
|------|-----------|
| `approved` | → PHASE 7 へ |
| `denied`   | → PHASE 3（ヘッドライン生成）に戻る |

---

## PHASE 7: ASC アップロード・実験開始

### 固定値（変えるな）

| 項目 | 値 |
|------|-----|
| **App ID** | `6755129214`（数字のみ。`1771826223384` は間違い） |
| **Platform** | `IOS` |
| **Traffic** | `50`（50/50 split） |
| **Screenshot size** | `1290x2796`（processed/ の `780x1688` は App Store 非対応 → 必ずリサイズ） |
| **Display type** | `APP_IPHONE_67`（`APP_IPHONE_69` は API に存在しない） |

### Step 7-1: PNG リサイズ（必須）

`processed/` の出力は `780x1688`。App Store は `1290x2796` を要求する。

```bash
mkdir -p docs/screenshots/resized
for i in 1 2 3; do
  sips -z 2796 1290 docs/screenshots/processed/screen${i}.png \
    --out docs/screenshots/resized/screen${i}.png
done
```

### Step 7-2: PPO 実験・Treatment 作成（asc CLI）

**重要: `asc screenshots upload` は Treatment localization に使えない（型不一致エラー）。**
**`asc product-pages custom-pages create` は CLI バグで失敗する。**
**PPO v2 experiments API を使う:**

```bash
# 1. 実験作成
asc product-pages experiments create \
  --v2 --app 6755129214 --platform IOS \
  --name "screenshot-ab-v{N}" --traffic-proportion 50

# 2. Treatment 作成
asc product-pages experiments treatments create \
  --experiment-id {EXPERIMENT_ID} \
  --name "New Screenshots v{N}"

# 3. en-US Treatment localization 作成
asc product-pages experiments treatments localizations create \
  --treatment-id {TREATMENT_ID} --locale en-US

# 4. ja Treatment localization 作成
asc product-pages experiments treatments localizations create \
  --treatment-id {TREATMENT_ID} --locale ja
```

### Step 7-3: スクリーンショットアップロード（ロケールごとに繰り返す — Apple API 直接）

**`asc screenshots upload` は `appStoreVersionLocalizations` 型のみ対応。Treatment localizations には使えない。Python スクリプトで直接 API を叩く。**

**アップロード対象: サポートする全ロケール**

```python
# ロケールと Treatment localization ID のマッピング（実験作成時に取得）
LOCALE_LOCALIZATION_MAP = {
    'en-US': '{EN_LOCALIZATION_ID}',
    'ja':    '{JA_LOCALIZATION_ID}',
    # 他のロケールがあれば追加
}

for locale, localization_id in LOCALE_LOCALIZATION_MAP.items():
    # 1. screenshotSet 取得 or 作成
    resp = requests.post(f'{BASE_URL}/appScreenshotSets', ...)
    if resp.status_code == 409:  # already exists
        # エラー文中の UUID（最後の UUID）を取得
        uuids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-...', error_detail)
        set_id = uuids[-1]
    else:
        set_id = resp.json()['data']['id']

    # 2. 既存スクリーンショットを全DELETE（必須 — これを忘れると 3枚+3枚=6枚になる）
    existing = requests.get(f'{BASE_URL}/appScreenshotSets/{set_id}/appScreenshots', ...)
    for ss in existing.json().get('data', []):
        requests.delete(f'{BASE_URL}/appScreenshots/{ss["id"]}', ...)

    # 3. そのロケールの新スクリーンショット3枚をアップロード
    # ロケール別ディレクトリ: resized/{locale}/screen1~3.png
    for path in [f'resized/{locale}/screen{i}.png' for i in range(1,4)]:
        # reserve → PUT binary → commit
        ...
```

**完全スクリプト:** `docs/screenshots/scripts/upload_treatment_screenshots.py`

### Step 7-4: 実験を審査提出（手動 — ダイスがやる）

**`reviewRequired: true` の実験は CLI/API から審査提出できない。**
`asc product-pages experiments update --started true` → `"Can't start experiment, must be reviewed!"`
`PATCH state: READY_FOR_REVIEW` → `"attribute 'state' can not be included in UPDATE request"`

**ダイスが ASC Web UI でやること:**
https://appstoreconnect.apple.com → Anicca → App Store → **Product Page Optimization** → `screenshot-ab-v{N}` → **"Start Test"** ボタンを押す

状態遷移: `PREPARE_FOR_SUBMISSION` → Apple Review → `RUNNING`

### Step 7-5: experiments.json を更新する

```json
{
  "current": {
    "id": "{EXPERIMENT_ID}",
    "name": "screenshot-ab-v{N}",
    "state": "PREPARE_FOR_SUBMISSION",
    "traffic_proportion": 50,
    "treatment_id": "{TREATMENT_ID}",
    "treatment_name": "New Screenshots v{N}",
    "en_localization_id": "{EN_LOCALIZATION_ID}",
    "ja_localization_id": "{JA_LOCALIZATION_ID}",
    "screenshots": [
      {"screen": 1, "headline": "...", "sub1": "...", "sub2": "..."},
      {"screen": 2, "headline": "...", "sub1": "...", "sub2": "..."},
      {"screen": 3, "headline": "...", "sub1": "...", "sub2": "..."}
    ],
    "created_at": "YYYY-MM-DD",
    "review_pending": true
  }
}
```

---

## experiments.json 完全フォーマット

```json
{
  "current": {
    "experiment_id": "ppo_abc123",
    "start_date": "2026-02-21",
    "queue_position": 0,
    "phase": "PIL",
    "headline": "6 Years. 10 Apps. Still Nothing Changed.",
    "before_cvr": 2.1,
    "analytics_request_id": ""
  },
  "history": [],
  "winning_patterns": [],
  "losing_patterns": []
}
```

---

## references/

| ファイル | 内容 |
|---------|------|
| `references/setup.md` | 初回セットアップ（DebugManager.swift・XCUITest テンプレート） |
| `references/pipeline.md` | Makefile + screenshots.yaml + extract/process スクリプト全文 |
| `references/headline-gen.md` | ヘッドライン生成→採点→改善ループ |
| `references/visual-qa.md` | App Store visual QA 50点採点プロンプト |
| `references/slack-approval.md` | Slack 承認コマンド |
