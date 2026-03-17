---
name: mobileapp-builder
description: Builds and ships a Swift/SwiftUI iOS app to the App Store from a natural language idea. Handles all phases autonomously: trend research (X + TikTok + App Store) → SDD spec → Xcode scaffold → SwiftUI implementation → landing page → ASC subscription setup → IAP 175-territory pricing → app icon + App Store screenshots → build → TestFlight → App Store submission. Three human stops: (1) spec approval before build, (2) TestFlight testing before submission, (3) App Privacy manual setup. Use when told to "build an app", "ship an iOS app", "make money with apps", or when triggered by app-factory cron.
---

# mobileapp-builder

Given a `spec.md`, autonomously build and ship a Swift/SwiftUI iOS app to the App Store.

**Full spec:** `.cursor/plans/ios/1.6.3/mobileapp-builder-spec.md`

---

## INPUT

```
spec.md path (required fields: app_name, bundle_id, version, price_monthly_usd,
price_annual_usd, output_dir, concept, screens, paywall, metadata)
```

See `references/spec-template.md` for the full spec.md format.

---

## OUTPUT

`asc review submissions-list` → state = `WAITING_FOR_REVIEW`

---

## SELF-IMPROVEMENT RULE

**失敗 → 即この SKILL.md に正しい CLI コマンドを書き込む → git push → 書き込み前に次フェーズへ進むのは禁止。**

| トリガー | アクション |
|---------|-----------|
| Apple リジェクット | 原因分析 → 該当 PHASE に修正ルール追記 → git push |
| CLI コマンドがエラー | 正しいコマンドを発見したら即 SKILL.md を修正 → git push |
| 「手動が必要」と思った | まず `--help` で確認する。CLI にある可能性が高い。確認前に「手動」と言うのは禁止 |
| 想定外のことが起きた | 修正せずに進むのは禁止。SKILL.md を直してから次へ |

**書き方ルール（具体例 + CLI コマンド必須）:**
```
❌ 禁止: 「IAP は手動でASC Webから追加が必要」
✅ 必須: 「`asc subscriptions submit --subscription-id <ID> --confirm` で CLI から直接 submit できる。
         2026-02-25 実機確認済み（実機確認済み。自分のサブスク ID は `asc subscriptions list --app <APP_ID>` で取得）」
```

**禁止:**
- 確認せずに「手動が必要」と言う → 必ず `asc <subcommand> --help` で確認してから判断
- 「次は気をつける」だけで終わらせる → 具体的な CLI コマンドを SKILL.md に追記すること
- git push せずに進む → `git add -A && git commit && git push` まで完了させる
- セッション注入コンテキスト（`projectSettings:mobileapp-builder`）だけを信用する
  → **必ず `Read` ツールで実ファイル（`/Users/cbns03/Downloads/mobileapp-builder/SKILL.md`）を確認する**
  → セッション注入は古いキャッシュ版の可能性がある。実ファイルが SSOT。

---

## CRITICAL RULES (違反 = リジェクト確定)

| # | ルール |
|---|--------|
| 1 | **提出前に全サブスクが READY_TO_SUBMIT**。MISSING_METADATA のまま提出 → Guideline 2.1 拒否 |
| 2 | **IAP pricing は全175カ国**。US のみは Guideline 2.1 拒否 |
| 3 | **Superwall 使用禁止**。RevenueCat のみ |
| 4 | **ビルドは Fastlane gym のみ。ビルド後（upload/submit/metadata/screenshots）は ASC CLI のみ**。Fastlane の deliver/produce/pilot は禁止 |
| 5 | **PHASE 8 が STOP ゲート**。blocking=0 + READY_TO_SUBMIT でなければ絶対に次に進まない |
| 6 | **availability set は pricing の前**。順序を逆にすると全pricing call が Apple 500エラーで失敗する |
| 7 | **Privacy Policy URL は en-US AND ja 両方必須**。片方だけでは submit 時にエラー |
| 8 | **RC Offerings は TestFlight 前に設定必須**。未設定だと「Apple IAP key is invalid」エラーで課金不可 |
| 9 | **locale は `ja`（`ja-JP` は無効）**。ASC API は `ja-JP` を拒否する |
| 10 | **IAP key は同一 Apple Developer アカウントで使い回し**。新規作成不要。`<AuthKey_XXXXXXXX.p8>` を流用 |
| 11 | **Paywall コピーは必ずコードから実機能を確認してから書く**。存在しない機能を訴求するのは罪（Apple レビュー違反 + ユーザー詐欺）。`FreePlanService.swift`, `SubscriptionManager.swift` を必ず読め |
| 12 | **Mixpanel 必須**。全新規アプリに Mixpanel SDK を組み込み、`paywall_viewed`（`offering_id` プロパティ付き）を送信すること。Mixpanel なしでは paywall-ab スキルによる A/B 評価が不可能 |
| 13 | **RevenueCat → Mixpanel 連携必須**。RC Dashboard で「Send data to Mixpanel」を有効化し、`presented_offering_id` が `rc_trial_started_event` に含まれることを確認すること。未設定 = A/B 変換追跡ゼロ |
| 14 | **スクショ撮影シミュレータは iPhone SE 3rd gen 必須**。iPhone 14+ は Dynamic Island（黒い丸）が写り込む。`xcrun simctl list devices | grep "SE (3rd"` で UDID を確認して使う |
| 15 | **Pencil テキストノードに `width: "fill_container"` 必須**。未設定だとテキストがフレーム外にはみ出す。日本語ヘッドラインの `fontSize` は **22以下**（28は14文字でオーバーフロー） |
| 16 | **Pencil 画像キャッシュ問題**。同じパスのファイルを上書きしても Pencil はキャッシュした旧版を使い続ける。画像差し替え時は**必ず新しいファイル名**を使うこと |
| 17 | **`mcp__pencil__get_screenshot` はディスクに保存しない**。返ってくるのは MCP レスポンス内の base64 のみ。ASC アップロード用ファイルは別途シミュレータから `xcrun simctl io` で取得すること |
| 18 | **App Privacy（データの使用方法）は ASC API で設定不可**。`/v1/apps/{id}/appDataUsages` は 404 を返す。PHASE 12 の前にユーザーに手動設定させること。設定手順は PHASE 11.5 参照 |
| 19 | **ISSUER_ID は ASC_ISSUER_ID 環境変数から取得**。間違った ID は全 curl 呼び出しが 401 を返す。ASC → Users and Access → Integrations → Keys 画面の上部に表示されている UUID が ISSUER_ID。キー一覧の「キー ID」欄の値（短い英数字）と混同しない |
| 20 | **アイコンはビルド前に配置する**。ビルド後にアイコンを変更した場合は `CURRENT_PROJECT_VERSION` をバンプして再ビルドが必要。「The bundle version must be higher than the previously uploaded version」エラーが出たらバンプして再アップロード |
| 21 | **Playwright + Chrome 競合**。Chrome 起動中に Playwright を実行すると「既存のブラウザセッションで開いています」エラー。先に `pkill -f "Google Chrome"` で Chrome を終了してから Playwright を起動 |
| 22 | **`asc submit create --confirm` が正解の提出方法**。`PATCH reviewSubmissions.state` は 409 を返す。`asc review submissions-list` で確認できる ID は `appStoreVersionSubmissions` とは別物 |
| 23 | **RevenueCat delegate 名前衝突**。`SubscriptionManager.swift` の内部クラス名を `PurchasesDelegate` にすると同名プロトコルと衝突してビルドエラー。必ず `RCPurchasesDelegate: NSObject, PurchasesDelegate` と命名する（2026-02-26 実機確認済み） |
| 24 | **iOS 15 ターゲット: `Locale.current.language.languageCode` 使用禁止**。iOS 16+ API。iOS 15 ターゲットでは `Locale.current.languageCode` を使う（deprecated だが iOS 15 互換）。2026-02-26 実機確認済み |
| 25 | **iOS 15 ターゲット: `scrollContentBackground` 使用禁止**。iOS 16+ API。ZStack + Color で背景色を設定する workaround を使う。`Form` の背景を透明にしたい場合: `ZStack { Color(hex:"#0f0f1a").ignoresSafeArea(); Form { ... } }` |
| 26 | **Fastfile シミュレータ destination は名前でなく UDID**。`"iPhone SE (3rd generation)"` は not found エラーになる。`xcrun simctl list devices available \| grep SE` で UDID を取得して `id=<UDID>` 形式で指定する |
| 27 | **`asc apps create` は Apple ID + パスワード必須（API Key 不可）**。`asc apps create --apple-id <email> --password <pass>` が必要。パスワード不明時はユーザーに事前確認。`APPLE_ID_PASSWORD` を `.env` に事前設定しておくこと。2026-02-27 実機確認済み |
| 27b | **RC v1 `platform_product_identifier` は v2 product-package 変更で自動更新されない**。RC SDK v5 は v1 offerings API (`/v1/subscribers/{id}/offerings`) を使い、`platform_product_identifier` を StoreKit に渡す。v2 で products を attach しても v1 の値は変わらない。**修正手順**: (1) `DELETE /v2/projects/{project_id}/packages/{package_id}` でパッケージ削除（⚠️ offering path を含めると 404 — `/packages/{id}` のみ正しい）→ (2) `POST /offerings/{id}/packages` で再作成 → (3) `attach_products` で正しい product を attach → v1 API が正しい `platform_product_identifier` を返すようになる。2026-02-27 実機確認済み |
| 28 | **ASC REST API `/v1/apps` POST は禁止操作**。`GET_COLLECTION, GET_INSTANCE, UPDATE` のみ許可。アプリ作成は必ず `asc apps create` を使う（Apple ID 必須）|
| 28b | **RC v1 offerings API での platform_product_identifier 確認方法（診断必須）**。`curl -H "Authorization: Bearer <iOS_API_KEY>" https://api.revenuecat.com/v1/subscribers/\$RCAnonymousID:test/offerings -H "X-Platform: ios"` で `platform_product_identifier` を確認。ASC の Product ID（例: `com.bundle.premium.monthly`）と一致してなければ「プランの取得に失敗しました」エラーが出る。v2 ダッシュボードでは正しく見えていても v1 が古い値を返し続けることがある |
| 29 | **Netlify は GitHub App Webhook なしで push に反応しない**。`aniccaai.com` は Netlify ホスト済みだが GitHub App Webhook がないため、push してもビルドされない。Netlify デプロイには `NETLIFY_AUTH_TOKEN` + `NETLIFY_SITE_ID` が必須。これらを `.env` および GitHub Secrets に必ず事前設定すること。2026-02-27 実機確認済み |
| 29b | **初回 IAP は `asc subscriptions submit` で単独 submit 禁止**。`STATE_ERROR.FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION` エラーが出る。これは Apple ルール: **初回 IAP は必ずアプリバージョンと同時提出**。PHASE 11.6 の `asc subscriptions submit` はスキップして、PHASE 12 で `asc publish appstore --submit --confirm` を実行すれば IAP も自動的に review に含まれる。2026-02-27 実機確認済み |
| 30 | **アプリ作成前に必要なクレデンシャルを PHASE 0 で確認する**。`APPLE_ID_PASSWORD`（Apple ID パスワード）と `NETLIFY_AUTH_TOKEN` が PHASE 0 STEP 3 の ENV チェックに追加必須。これらなしに PHASE 3.5/4 は完了不可。|
| 31 | **ImageMagick v7 では `convert` コマンドは非推奨**。`magick` コマンドを使う。`magick -size 1024x1024 gradient:... icon.png` が正解。|
| 32 | **iPad 13" スクショ（APP_IPAD_PRO_3GEN_129）は Submit 必須（2026-02-28 実機確認）**。iPhone スクショだけでは `asc submit create` が失敗する。**正しいサイズ: 2048×2732**（2064×2752 は IMAGE_INCORRECT_DIMENSIONS エラー）。iPhone スクショを `sips -z 2732 2048` でリサイズして流用可。PHASE 9 Step 3b を参照 |
| 33 | **copyright + contentRightsDeclaration + app pricing の3つは Submit 必須（2026-02-28 実機確認）**。いずれか未設定で `asc submit create` → `App is not eligible for submission` エラー。copyright は `asc versions update --copyright`、content rights は curl PATCH で `contentRightsDeclaration: DOES_NOT_USE_THIRD_PARTY_CONTENT`、pricing は `appPriceSchedules` POST で設定。PHASE 9 Step 5 を参照 |
| 34 | **iPad スクショのサイズ: 2048×2732 が正解（2026-02-28 実機確認）**。Apple の `APP_IPAD_PRO_3GEN_129` display type は 2048×2732。`sips -z 2732 2048 input.png` で変換（`-z height width` の順序に注意）。2064×2752 は誤り |
| 35 | **`primaryCategory` 未設定 → `INVALID_BINARY` になる（2026-02-28 実機確認）**。`asc submit create` 後に version が `INVALID_BINARY` になる主原因。PHASE 4 で必ず `appInfos` の `primaryCategory` relationship を設定する。コマンド: `curl -X PATCH /v1/appInfos/<ID>` で `relationships.primaryCategory.data.id = "UTILITIES"` 等を設定。確認: `curl /v1/appInfos/<ID>/primaryCategory` → id が返れば OK。`INVALID_BINARY` になってしまった場合の回復手順: `canceled: true` で既存提出をキャンセル → version 状態が `PREPARE_FOR_SUBMISSION` に戻る → `asc submit create` で再提出。2026-02-28 実機確認済み |
| 36 | **`usesIdfa: None`（未設定）→ `INVALID_BINARY` になる（2026-02-28 実機確認）**。Apple の自動バイナリ検証が `usesIdfa` 未設定を検出して `INVALID_BINARY` に自動変換し、提出が UNRESOLVED_ISSUES+REJECTED になる。PHASE 9 Step 5（または PHASE 4）で必ず `usesIdfa: false` を設定する。コマンド: `curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID" -d '{"data":{"type":"appStoreVersions","id":"$VERSION_ID","attributes":{"usesIdfa":false}}}'`。設定後 `appStoreState` が即座に `INVALID_BINARY` → `READY_FOR_REVIEW` に回復する。`INVALID_BINARY` 回復手順: (1) 既存 UNRESOLVED_ISSUES 提出を `canceled: true` でキャンセル → (2) `usesIdfa: false` を PATCH → (3) 新規 reviewSubmission を作成 → (4) version item を追加 → (5) `submitted: true` で提出。2026-02-28 実機確認済み |
| 37 | **Distribution 証明書が REVOKED → ITMS-90035: Invalid Signature（2026-02-28 実機確認）**。Keychain の Distribution 証明書が全て REVOKED になると、どのプロビジョニングプロファイルを使っても `error: exportArchive Signing certificate is invalid` が出る。**根本原因**: `openssl req` で CSR を作成しても Apple API が 409 で拒否する。**正解**: `asc certificates csr generate` → `asc certificates create --certificate-type IOS_DISTRIBUTION` の順で新証明書を発行。**回復手順**: (1) `asc certificates csr generate ~/Downloads/.signing/dist.csr` でCSR生成 → (2) `asc certificates create --certificate-type IOS_DISTRIBUTION --csr ~/Downloads/.signing/dist.csr` で証明書発行 → (3) ダウンロードした `.cer` と秘密鍵 `.pem` をKeychain にインポート → (4) REVOKED 証明書を Keychain から削除 → (5) `asc profiles create --profile-type IOS_APP_STORE` で新 Provisioning Profile 作成 → (6) Fastfile で `signingStyle: "manual"` + `provisioningProfiles: { "bundle.id" => "profile-uuid" }` を指定してビルド。REVOKED cert が embedded.mobileprovision に残ったまま Xcode 管理プロファイルを使い続けると何度やっても失敗する。2026-02-28 実機確認済み |
| 38 | **`asc submit create` で `appStoreVersions already added to another reviewSubmission` エラー → キャンセルしてから新規作成（2026-02-28 実機確認）**。同じバージョンが既存の submission に紐付いている場合、新規 `submit create` が失敗する。**回復手順**: (1) `asc submit cancel --id <problematic-submission-id> --confirm` でキャンセル → (2) `asc submit create` を再実行。READY_FOR_REVIEW 状態の submission はキャンセル不可だが、UNRESOLVED_ISSUES や PREPARING は `canceled: true` でキャンセル可能。キャンセル後も新規 `asc submit create` を実行すれば、古い READY_FOR_REVIEW は無視して正しく新規提出が作られる。2026-02-28 実機確認済み |

---

## 🏭 工場ルール（FACTORY RULES — 違反 = ファクトリー停止）

| # | ルール | 詳細 |
|---|--------|------|
| F1 | **承認待ち禁止** | フェーズ間で人間の承認を待つな。Slack に報告して即次フェーズへ。 |
| F2 | **詰まったら SKILL.md を必ず修正** | エラー・失敗・想定外 → 修正して git commit/push → 次の実行で自動修正される。修正せずに進むのは禁止。 |
| F3 | **クローズドループ強制** | 今日の失敗は明日の成功のソース。全ての例外・エラー・ハマりポイントを即座にこの SKILL.md に書き込め。 |
| F4 | **オリジナル禁止** | 判断する前に既存ベストプラクティスを検索する。ソース引用なき判断行は削除。 |
| F5 | **TDD 強制（PHASE 3）** | ralph-autonomous-dev は tdd-workflow スキルと組み合わせて使う。テストなし実装 = ビルドはできても品質がない。 |
| F6 | **Worktree 必須** | 全作業は git worktree で隔離する。dev に直接コミットしない。TestFlight 承認後に dev にマージする。詳細は PHASE 0 PRE-FLIGHT STEP 0 参照。 |

---

## ⚠️ Paywall コピー作成ルール（必読）

**Paywall に書く機能は全てコードに実在すること。存在しない機能を訴求してはいけない。**

Paywall 作成・更新の前に以下を確認する（Anicca の場合）:

| ファイル | 確認する内容 |
|---------|------------|
| `FreePlanService.swift` | Free の制限（本数・時刻・ルールベース） |
| `LLMNudgeService.swift` | Pro の AI 機能 |
| `NudgeStatsManager.swift` | フィードバック学習の仕組み |
| `SubscriptionInfo.swift` | Free/Pro の差分定義 |

新規アプリの場合: `PaywallView` がある画面と `SubscriptionManager` 相当のファイルを読んで、
Free と Pro の実際の差分を確認してからコピーを書く。

**禁止パターン（実在しないのに書く）:**
- ❌ "30-day insight reports" — 分析機能がなければ書くな
- ❌ "Progress tracking" — 進捗画面がなければ書くな
- ❌ "Premium support" — サポートチームがなければ書くな
- ❌ "All features unlocked" — 意味がない。何が解禁されるか具体的に書け

---

## 14 PHASES

### PHASE 0: PRE-FLIGHT（セットアップウィザード）

PRE-FLIGHT はサイレントチェックではなくガイド付きウィザードとして実行する。
問題が1つでも見つかれば、ユーザーに解決手順を提示し、確認を取ってから次の項目へ進む。
全 STEP が PASS になるまで PHASE 0 TREND RESEARCH に進まない。

---

#### STEP 0: Git Worktree セットアップ（必須 — devを汚さない）

**全作業は git worktree で dev から隔離する。dev に直接コミット禁止。**

理由: 複数のファクトリーエージェントが同時に dev で作業すると競合が起きる。TestFlight テスト前のコードが dev に混入するとデプロイが汚れる。

```bash
# slug を spec.md から取得（例: breath-calm）
SLUG=$(python3 -c "import re; s=open('.cursor/app-factory/<SLUG>/02-spec.md').read(); print(re.search(r'output_dir.*?([a-z-]+)-app', s).group(1))" 2>/dev/null || echo "<SLUG>")

# worktree 作成（~/Downloads/ 直下）
WORKTREE_PATH="$HOME/Downloads/anicca-${SLUG}"
git worktree add "$WORKTREE_PATH" -b "app-factory/${SLUG}"
echo "✅ Worktree 作成: $WORKTREE_PATH (branch: app-factory/${SLUG})"

# 以降の全作業はこの worktree 内で行う
cd "$WORKTREE_PATH"
```

**TestFlight 承認後のマージ手順（PHASE 10 完了後）:**

```bash
# 1. worktree から dev にマージ
cd /Users/cbns03/Downloads/anicca-project  # メインリポジトリ
git checkout dev
git merge app-factory/${SLUG} --no-ff -m "feat(app-factory): merge ${SLUG} → dev (TestFlight approved)"
git push origin dev

# 2. worktree クリーンアップ
git worktree remove "$HOME/Downloads/anicca-${SLUG}"
git branch -d app-factory/${SLUG}
```

---

#### STEP 1: Sub-skills（自動インストール）

```bash
# まずすべてのスキルをチェックし、足りなければ自動インストール
required_skills=(x-research tiktok-research apify-trend-analysis ralph-autonomous-dev screenshot-creator slack-approval)
for skill in "${required_skills[@]}"; do
  if ! npx skills list 2>/dev/null | grep -q "$skill"; then
    echo "⏳ Installing: $skill"
    npx skills add Daisuke134/anicca-products@$skill -g -y
  fi
done
if ! npx skills list 2>/dev/null | grep -q "app-icon"; then
  npx skills add code-with-beto/skills@app-icon -g -y
fi
echo "✅ All sub-skills ready."
```

---

#### STEP 2: CLI Tools

```bash
check_tool() {
  local name="$1"; local cmd="$2"; local install="$3"
  if eval "$cmd" &>/dev/null 2>&1; then echo "✅ $name"
  else echo "❌ $name → $install"; return 1; fi
}

TOOL_FAIL=0
check_tool "asc"         "asc --version"            "brew install nickvdyck/tap/asc"      || TOOL_FAIL=1
check_tool "fastlane"    "fastlane --version"        "brew install fastlane"               || TOOL_FAIL=1
check_tool "greenlight"  "greenlight --version"      "cd /tmp && git clone https://github.com/RevylAI/greenlight.git && cd greenlight && make build && sudo cp build/greenlight /usr/local/bin/" || TOOL_FAIL=1
check_tool "imagemagick" "convert --version"         "brew install imagemagick"            || TOOL_FAIL=1
check_tool "snapai"      "npx snapai --version"      "npm install -g snapai"               || TOOL_FAIL=1
check_tool "ios-deploy"  "ios-deploy --version"      "brew install ios-deploy"             || TOOL_FAIL=1
check_tool "Pillow"      "python3 -c 'import PIL'"   "pip3 install Pillow"                 || TOOL_FAIL=1
check_tool "PyJWT"       "python3 -c 'import jwt'"   "pip3 install PyJWT"                  || TOOL_FAIL=1
check_tool "requests"    "python3 -c 'import requests'" "pip3 install requests"            || TOOL_FAIL=1

if [ "$TOOL_FAIL" -ne 0 ]; then
  echo ""
  echo "⚠️  上記の CLI ツールが不足しています。インストール後「完了」と入力してください。"
  # ← ユーザー入力待ち。「完了」を受けたら STEP 2 を再実行し PASS になったら STEP 3 へ
fi
```

---

#### STEP 3: 環境変数

```bash
ENV_FILE="$HOME/.config/mobileapp-builder/.env"
[ -f "$ENV_FILE" ] && source "$ENV_FILE"

ENV_FAIL=0
check_env() {
  local name="$1"; local link="$2"; local hint="$3"
  if [ -n "${!name:-}" ]; then echo "✅ $name"
  else echo "❌ $name → $link ($hint)"; ENV_FAIL=1; fi
}

check_env ASC_KEY_ID              "https://appstoreconnect.apple.com → Users and Access → Integrations → Keys" "キーID（例: ABC123DEFG）"
check_env ASC_ISSUER_ID           "同上"                                                                        "Issuer ID（UUID形式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx）"
check_env ASC_KEY_PATH            "上記ページで .p8 ダウンロード → ~/Downloads/ に保存（1度しかダウンロードできない）" "例: ~/Downloads/AuthKey_XXXXXX.p8"
check_env REVENUECAT_API_KEY      "https://app.revenuecat.com → Project Settings → API Keys"                   "sk_ で始まるキー"
check_env MIXPANEL_TOKEN          "https://mixpanel.com → Project Settings → Project Token"                    "英数字トークン"
check_env X_BEARER_TOKEN          "https://developer.twitter.com → App → Bearer Token"                        "AAAA... で始まる"
check_env APIFY_TOKEN             "https://console.apify.com → Settings → Integrations"                       "apify_api_ で始まる"
check_env GEMINI_API_KEY          "https://console.cloud.google.com → APIs & Services → Credentials"           "AIza... で始まる"
check_env OPENAI_API_KEY          "https://platform.openai.com → API keys"                                    "sk- で始まる"
check_env SLACK_BOT_TOKEN         "https://api.slack.com/apps → OAuth & Permissions"                          "xoxb- で始まる"
check_env SLACK_APP_TOKEN         "https://api.slack.com/apps → Basic Information → App-Level Tokens"         "xapp- で始まる"
check_env SLACK_CHANNEL_ID        "Slack でチャンネル右クリック → リンクをコピー → 末尾 C... 部分"             "例: C0123456789"
check_env PRIVACY_POLICY_DOMAIN   "自分が所有するドメイン（Privacy Policy と Landing Page をホストする）"       "例: example.com（https://は含めない）"
check_env NETLIFY_AUTH_TOKEN      "https://app.netlify.com → User Settings → Applications → Personal access tokens → New access token" "tok_ で始まるトークン（PHASE 3.5 で必須）"
check_env NETLIFY_SITE_ID         "https://app.netlify.com → サイト選択 → Site settings → General → Site ID" "UUID形式（PHASE 3.5 で必須）"
check_env APPLE_ID_PASSWORD       "keiodaisuke@gmail.com の Apple ID パスワード"                             "PHASE 4 の asc apps create で必須"

if [ "$ENV_FAIL" -ne 0 ]; then
  echo ""
  echo "⚠️  環境変数が不足しています。設定方法:"
  echo "   1. mkdir -p ~/.config/mobileapp-builder"
  echo "   2. 上のリンクから各キーを取得"
  echo "   3. ~/.config/mobileapp-builder/.env に: export 変数名=値"
  echo "   4. source ~/.config/mobileapp-builder/.env"
  echo "   設定が完了したら「完了」と入力してください。"
  # ← ユーザー入力待ち。「完了」を受けたら STEP 3 を再実行し PASS になったら STEP 4 へ
fi
```

---

#### STEP 4: ASC API Key (.p8)

```bash
if ls ~/Downloads/AuthKey_*.p8 &>/dev/null 2>&1; then
  echo "✅ ASC API Key (.p8) 確認済み"
else
  echo "❌ .p8 ファイルが ~/Downloads に見つかりません"
  echo ""
  echo "   取得手順:"
  echo "   1. https://appstoreconnect.apple.com を開く"
  echo "   2. Users and Access → Integrations → Keys → + ボタン"
  echo "   3. 名前: mobileapp-builder / アクセス: App Manager"
  echo "   4. ダウンロード → ~/Downloads/ に保存"
  echo "   5. ASC_KEY_ID と ASC_KEY_PATH を .env に追記"
  echo "   完了したら「完了」と入力してください。"
  # ← ユーザー入力待ち
fi
```

---

#### STEP 5: snapai 設定

```bash
[ -n "${OPENAI_API_KEY:-}" ] && npx snapai config --openai-api-key "$OPENAI_API_KEY" && echo "✅ snapai 設定済み"
```

---

#### PRE-FLIGHT 完了

```bash
echo "✅ PRE-FLIGHT 完了。全チェック通過。PHASE 0 TREND RESEARCH を開始します。"
```

---

### PHASE 0: TREND RESEARCH
```
x-research + tiktok-research + apify-trend-analysis スキルを並列実行

[x-research]
  X (Twitter) でバズってるキーワード・トレンドトピックを調査
  → 「今週 JP/EN でバズってるメンタル・健康・生産性系のキーワード TOP5」

[tiktok-research]
  TikTok で伸びているショート動画のテーマ・フック・視聴者の悩みを調査
  → 「今週バズってる動画のテーマ TOP5 + 共通するペイン」

[apify-trend-analysis]
  App Store カテゴリ別ランキング + Google Trends を調査
  → 「今上位に入っているアプリジャンル + 検索ボリューム増加中のトピック」

3つの結果を統合して判断:
  - 共通して出てくるテーマ = 今作るべきアプリのジャンル
  - アプリアイデアを1つに絞る（選択肢提示禁止。1つに決める）

OUTPUT → .cursor/app-factory/{slug}/01-trend.md
  - 決定したアプリアイデア（タイトル仮 + 一言説明）
  - 根拠（どのトレンドデータから判断したか）
  - slug（例: sleep-tracker、breath-calm 等）
  - 【必須】なぜこれが人間の苦しみを解決するか: 実データ + ソースURL 付き3点
    例: "不安障害は世界2.8億人（WHO: https://who.int/news-room/fact-sheets/detail/anxiety-disorders）"
  - 【必須】なぜバイラルになるか（実測数値）: 各ツールの実測データを引用
    例: "Apify実測: 9D Breathwork TikTok 動画 平均2.3M再生 / 月"
    例: "Google Trends実測: 日本式ウォーキング 2,986% YoY増"
    ※ LLM の推測 = 禁止。実ツール（Apify/X/Google Trends）の実数値のみ
```

### PHASE 0.5: SPEC 生成（SDD）
```
01-trend.md を読んで spec.md を自動生成する
スラッシュコマンド不要。以下の手順をそのまま実行する。

Step 1: spec.md の全フィールドを埋める（PHASE 1 の必須フィールドを全部）
  - app_name, bundle_id, version, output_dir
  - price_monthly_usd: 9.99, price_annual_usd: 49.99（デフォルト）
  - paywall.cta_text_en / paywall.cta_text_ja
  - metadata: title_en/ja, subtitle_en/ja, description_en/ja, keywords_en/ja
  - urls.privacy_en: "https://$PRIVACY_POLICY_DOMAIN/{slug}/privacy/en"
  - urls.privacy_ja: "https://$PRIVACY_POLICY_DOMAIN/{slug}/privacy/ja"
  - urls.terms: "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
  - urls.landing: "https://$PRIVACY_POLICY_DOMAIN/{slug}"
  - localization: "os_language"
  - supported_locales: ["en", "ja"]
  - concept: （1行説明。スクショヘッドライン生成に使う）
  - 画面構成（Onboarding / Main / Paywall / Settings）

Step 2: plan.md を生成（技術設計）
  - アーキテクチャ（SwiftUI MVC）
  - ファイル構成
  - API / RevenueCat 設計

Step 3: tasks.md を生成（実装タスクリスト）
  - 依存順に並んだチェックボックス形式
  - PHASE 2〜12 の各フェーズに対応するタスクを網羅

OUTPUT →
  .cursor/app-factory/{slug}/02-spec.md   ← PHASE 1 が読む
  .cursor/app-factory/{slug}/03-plan.md
  .cursor/app-factory/{slug}/04-tasks.md
```

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 PHASE 0.5 完了 — Slack 報告して即 PHASE 1 へ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ 承認を待つな。Slack に投稿したら返信を待たずに即 PHASE 1 を開始する。

Slack (#metrics / SLACK_CHANNEL_ID) に以下を投稿:

🏭 {app_name} のビルドを開始します

💊 なぜこれが人間の苦しみを解決するか:
  [01-trend.md の「コアペイン」セクションから3点引用 — 実データ・ソースURL付き]
  例: "不安障害は世界2.8億人（WHO）。薬なし6分で解決できる呼吸法は科学的証拠あり"

📈 なぜバイラルになるか（実測データ）:
  [x-research・tiktok-research・apify-trend-analysis の実測数値を3点引用]
  例: "TikTok: 9D Breathwork が2026年明示的にバイラル（Apify実測）"
  例: "日本式ウォーキング 2,986% YoY増（Google Trends実測）"
  例: "日本市場 CAGR 16.31% → $822M by 2035（GlobeNewswire）"

💰 {price_monthly_usd}/月 | {price_annual_usd}/年 | EN+JA

📁 SDD ファイル（フルパス）:
  .cursor/app-factory/{slug}/01-trend.md
  .cursor/app-factory/{slug}/02-spec.md
  .cursor/app-factory/{slug}/03-plan.md
  .cursor/app-factory/{slug}/04-tasks.md

Phase 1→12 を自律実行します。完了時に報告します。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### PHASE 1: VALIDATE INPUT
```
spec.md の必須フィールド確認（全項目 MUST — 1つでも欠ければ STOP）

■ 技術
  - app_name, bundle_id, version, output_dir

■ 課金
  - price_monthly_usd, price_annual_usd
  - paywall.cta_text_en, paywall.cta_text_ja

■ App Store メタデータ（EN + JA 両方必須）
  - metadata.title_en, metadata.title_ja
  - metadata.subtitle_en, metadata.subtitle_ja
  - metadata.description_en, metadata.description_ja
  - metadata.keywords_en, metadata.keywords_ja

■ URL（アプリ専用 URL 必須 — 全アプリ共通 URL 禁止）
  - urls.privacy_en   例: "https://example.com/myapp/privacy/en"（PRIVACY_POLICY_DOMAIN + slug で構成）
  - urls.privacy_ja   例: "https://example.com/myapp/privacy/ja"
  - urls.terms        固定値: "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
  - urls.landing      例: "https://example.com/myapp"

■ ローカライズ方針
  - localization: "os_language"  （日本語OS→日本語、その他→英語）
  - supported_locales: ["en", "ja"]

■ コンセプト
  - concept  （1行説明。スクショヘッドライン生成に使う）

欠けていれば STOP + 不足フィールドを報告
```

### PHASE 2: SCAFFOLD
```bash
# 新規 Xcode プロジェクトを output_dir に作成
mkdir -p <output_dir>/<app_name>ios
# Bundle ID / バージョン / チーム ID を project.pbxproj に設定
# RevenueCat SDK を SPM で追加
# PrivacyInfo.xcprivacy を追加（必須）
```

### PHASE 3: BUILD
```
【TDD 強制】tdd-workflow スキルを起動してから ralph-autonomous-dev でループ実行。
手順:
  1. `tdd-workflow` スキルを読み込む（テストファースト実装の強制）
  2. 各機能について RED → GREEN → REFACTOR を必ず通す
  3. ralph-autonomous-dev が fix_plan.md を読み → 実装 → テスト → ✅ のループを回す
  4. 全タスク `[x]` → EXIT_SIGNAL: true → PHASE 3 完了

ralph-autonomous-dev で SwiftUI 実装

■ 必須実装（1つでも欠ければ PHASE 11 で STOP）

  コア機能:
  - spec の画面構成・コア機能を実装
  - 通知: UserNotifications で APNs 登録 + 通知カタログ
  - Paywall: RevenueCat SDK のみ（Superwall 禁止）
  - Paywall の accessibilityIdentifier（必須 5要素）:
      paywall_plan_monthly / paywall_plan_yearly
      paywall_cta / paywall_skip / paywall_restore

  ローカライズ（OS言語対応 — 必須）:
  - Localizable.strings を EN + JA 両方作成
  - 表示言語は OS 言語に自動追従（Locale.current で判定）
  - 日本語 OS → 日本語 UI、その他 OS → 英語 UI
  - Paywall コピーも EN/JA 両対応（spec.md の paywall.cta_text_en/ja を使う）
  - ハードコード日本語・英語テキスト禁止。全て Localizable.strings 経由

  Settings 画面（必須）:
  - Privacy Policy リンク → spec.md の urls.privacy_en / urls.privacy_ja（OS言語で切替）
  - Terms of Use リンク → spec.md の urls.terms（Apple 標準 EULA 固定）
    URL: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/

  ■ PHASE 9 スクショパイプラインの前提セットアップ（必須 — これがないと PHASE 9 Step 2 が動かない）

  1. ScreenshotTests.swift を作成
     ファイル: <output_dir>/<slug>UITests/ScreenshotTests.swift
     内容: XCUITest でアプリを起動し、各画面をスクロール・遷移してスクショを撮影するテストケース
     テストケース:
       - testScreenshot_Main   : メイン画面
       - testScreenshot_Streak : カレンダー/ストリーク画面（存在する場合）
       - testScreenshot_Paywall: Paywall 画面（paywall_skip で到達可能にすること）
     accessibilityIdentifier を使って各画面に確実に到達すること

  2. Makefile に generate-store-screenshots ターゲットを追加
     場所: <output_dir>/Makefile
     コマンド:
       generate-store-screenshots:
         xcodebuild test -project <app_name>.xcodeproj -scheme <app_name>UITests \
           -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 16 Pro Max' \
           -resultBundlePath docs/screenshots/output.xcresult
         python3 docs/screenshots/scripts/extract_screenshots.py
         python3 docs/screenshots/scripts/process_screenshots.py

  3. extract_screenshots.py + process_screenshots.py を docs/screenshots/scripts/ に配置
     - extract_screenshots.py: xcresulttool で output.xcresult から PNG を抽出 → docs/screenshots/raw/
     - process_screenshots.py: PIL で 1290×2796 に合成（ヘッドラインを screenshots.yaml から読む）
     - screenshots.yaml: 各画面のヘッドライン + カラー設定

  ⚠️ これらのセットアップが完了してから PHASE 9 Step 2 に進む。スキップ禁止。
```

### PHASE 3.5: PRIVACY POLICY & LANDING PAGE デプロイ
```
$PRIVACY_POLICY_DOMAIN/{slug}/ のページを作成してデプロイする。
PHASE 4 の前に必須（URL が死んでいると ASC Privacy URL 設定が通らない）。

■ 必要なページ（4つ）

  1. https://$PRIVACY_POLICY_DOMAIN/{slug}/             ← ランディングページ
     - アプリ名・コンセプト・App Store リンク（EN のみ可）

  2. https://$PRIVACY_POLICY_DOMAIN/{slug}/privacy/en  ← Privacy Policy（英語）
     - 収集データ: Device ID（Analytics）、Usage Data（Analytics）
     - RevenueCat: Purchase History（サブスク管理）
     - 収集しないデータ: 日記内容・アファメーション（ローカル保存のみ）

  3. https://$PRIVACY_POLICY_DOMAIN/{slug}/privacy/ja  ← Privacy Policy（日本語）
     - 同上の日本語版

  4. https://$PRIVACY_POLICY_DOMAIN/{slug}/terms       ← Terms（EULA リダイレクト）
     - https://www.apple.com/legal/internet-services/itunes/dev/stdeula/ へリダイレクト

■ 推奨デプロイ方法（3択 — 自分のインフラに合わせて選ぶ）

  オプション A: GitHub Pages（無料・ドメイン持ちであれば最速）
    1. リポジトリに docs/ フォルダを作成して HTML ファイルを追加
    2. GitHub Settings → Pages → /docs を公開
    3. カスタムドメインを設定 → $PRIVACY_POLICY_DOMAIN を向ける

  オプション B: Vercel / Netlify（Next.js や静的サイトがあれば）
    1. プロジェクトに pages/{slug}/privacy/en.html 等を追加
    2. push → 自動デプロイ

  オプション C: 既存サーバー（VPS/Nginx/Apache）
    1. /var/www/html/{slug}/ にファイルを配置
    2. Nginx で location /{slug}/ { root /var/www/html; } を設定

■ Privacy Policy の最小テンプレート（EN）

  ```html
  <!DOCTYPE html><html><body>
  <h1>{app_name} Privacy Policy</h1>
  <p>We collect: Device identifiers (for analytics), usage data.</p>
  <p>We use RevenueCat for subscription management (purchase history).</p>
  <p>We do NOT collect: journal entries, affirmations, or any personal content.</p>
  <p>Contact: {your_email}</p>
  </body></html>
  ```

■ デプロイ後の確認（必須 — URL が死んでいると PHASE 11 GATE 4 で STOP）

  SLUG="{slug}"
  DOMAIN="$PRIVACY_POLICY_DOMAIN"
  curl -I "https://$DOMAIN/$SLUG/privacy/en" -s -o /dev/null -w "%{http_code}" | grep -q "200\|301\|302" \
    && echo "✅ EN privacy URL 生きています" || echo "❌ STOP: EN privacy URL が死んでいます"
  curl -I "https://$DOMAIN/$SLUG/privacy/ja" -s -o /dev/null -w "%{http_code}" | grep -q "200\|301\|302" \
    && echo "✅ JA privacy URL 生きています" || echo "❌ STOP: JA privacy URL が死んでいます"
  # 200/301/302 でなければ STOP。デプロイを確認してから PHASE 4 へ

■ ⚠️ Netlify CI クラッシュ警告（F6違反時 — 2026-02-26 実機確認）

  **F6ルール違反（worktree 未使用で main/dev に直接作業）すると Netlify CI が完全クラッシュする。**

  原因: aniccaai.com の Next.js プロジェクトは `.worktrees/main/apps/landing/` にある。
  worktree を使わず main ブランチや dev ブランチで作業すると、Netlify が
  Next.js ビルドを実行できず CI が失敗する。

  リカバリ手順（CI クラッシュ時）:
  ```bash
  cd /Users/cbns03/Downloads/anicca-project/.worktrees/main/apps/landing
  next build
  npx netlify deploy --dir=out --prod
  # → 手動で本番デプロイして CI をバイパスする
  ```

  予防: **必ず F6 に従い `git worktree add ~/Downloads/anicca-{slug} -b app-factory/{slug}` で隔離すること。**
```

### PHASE 4: ASC APP SETUP

> **✅ アプリ作成は `asc apps create` + `asc bundle-ids create` で全自動（ASC CLI 0.34.0 — 2026-02-26 更新）**
>
> fastlane produce は不要。ASC CLI 0.34.0 で `asc apps create` が追加された。

# Step 0: Bundle ID を作成（Apple Developer Portal に登録）
asc bundle-ids create --identifier "<bundle_id>" --name "<app_name>" --platform IOS

# Step 1: asc apps create でアプリを作成（App Store Connect に登録）
asc apps create --name "<app_name>" --bundle-id "<bundle_id>" --sku "<slug>" --primary-locale en-US
# ⚠️ fastlane produce create は使わない（CRITICAL RULE 4 — 禁止）
# 過去に試したが PRODUCE_USERNAME が必要で Spaceship が Apple ID ログインを要求する。
# ASC CLI 0.34.0 で asc apps create が追加されたため fastlane produce は不要になった。

# Step 2: 作成されたアプリの APP_ID を取得
APP_ID=$(asc apps list --bundle-id "<bundle_id>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")
echo "APP_ID: $APP_ID"

# Privacy Policy URL を en-US AND ja 両方に設定（片方だけでは submit 時にエラー）
# locale は必ず "ja"（"ja-JP" は ASC で無効）
APP_INFO_ID=$(asc apps info list --app "<APP_ID>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

TOKEN=$(python3 -c "
import jwt,time,os,pathlib
key=pathlib.Path(os.environ['ASC_KEY_PATH']).read_text()
payload={'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1200,'aud':'appstoreconnect-v1'}
print(jwt.encode(payload,key,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'}))
")

# en-US Privacy URL（spec.md の urls.privacy_en を使う）
PRIVACY_EN="<urls.privacy_en>"   # 例: https://example.com/myapp/privacy/en
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://api.appstoreconnect.apple.com/v1/appInfoLocalizations/<EN_LOC_ID>" \
  -d "{\"data\":{\"type\":\"appInfoLocalizations\",\"id\":\"<EN_LOC_ID>\",\"attributes\":{\"privacyPolicyUrl\":\"$PRIVACY_EN\"}}}"

# ja Privacy URL（locale = "ja" 確認必須 / spec.md の urls.privacy_ja を使う）
PRIVACY_JA="<urls.privacy_ja>"   # 例: https://example.com/myapp/privacy/ja
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://api.appstoreconnect.apple.com/v1/appInfoLocalizations/<JA_LOC_ID>" \
  -d "{\"data\":{\"type\":\"appInfoLocalizations\",\"id\":\"<JA_LOC_ID>\",\"attributes\":{\"privacyPolicyUrl\":\"$PRIVACY_JA\"}}}"

asc subscriptions groups create --app "<APP_ID>" --reference-name "Premium"

asc subscriptions create --group "<GROUP_ID>" --name "Monthly" \
  --product-id "<bundle_id>.premium.monthly" --period ONE_MONTH --level 2

asc subscriptions create --group "<GROUP_ID>" --name "Annual" \
  --product-id "<bundle_id>.premium.yearly" --period ONE_YEAR --level 1

# ★ availability を pricing の前に必ず設定（これなしでpricingは全件Apple 500エラー）
asc subscriptions availability set --id "<MONTHLY_ID>" \
  --available-in-new-territories --territory USA,JPN

asc subscriptions availability set --id "<ANNUAL_ID>" \
  --available-in-new-territories --territory USA,JPN

# ★★ primaryCategory 設定（CRITICAL RULE 35 — 未設定で INVALID_BINARY になる）
APP_INFO_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.appstoreconnect.apple.com/v1/apps/<APP_ID>/appInfos" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['id'])")

# カテゴリ設定（アプリ内容に応じて変更: UTILITIES / PRODUCTIVITY / SOCIAL_NETWORKING / EDUCATION）
curl -s -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.appstoreconnect.apple.com/v1/appInfos/$APP_INFO_ID" \
  -d "{\"data\":{\"type\":\"appInfos\",\"id\":\"$APP_INFO_ID\",\"relationships\":{\"primaryCategory\":{\"data\":{\"type\":\"appCategories\",\"id\":\"UTILITIES\"}}}}}"

# 確認（id が返れば OK）
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.appstoreconnect.apple.com/v1/appInfos/$APP_INFO_ID/primaryCategory" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('primaryCategory:', d.get('data',{}).get('id','NOT SET'))"
```

### PHASE 4.5: RC OFFERINGS SETUP（TestFlight 前に必須）
```
RC Dashboard → <app_name> プロジェクト（または新規作成）
  → Offerings → New Offering → identifier: "default"
  → Packages を追加:
      $rc_annual  → Apple Product ID: <bundle_id>.premium.yearly
      $rc_monthly → Apple Product ID: <bundle_id>.premium.monthly
  → Offering を Current に設定

確認: Offerings が "current" に設定されていること
未設定 = TestFlight で「Apple IAP key is invalid」エラー

IAP Key: $ASC_KEY_ID（同一 Apple Developer アカウントで全アプリ共通、新規作成不要）
p8 file: $ASC_KEY_PATH を RC にアップロード済みであること確認

【RC プロジェクトが未作成の場合】
RevenueCat Dashboard → Projects → New Project → App name を <app_name> に設定
→ Add iOS App → Bundle ID: <bundle_id>
→ App Store Connect App-Specific Shared Secret は ASC → My Apps → App Information から取得
```

### PHASE 5: IAP PRICING ★最重要
```bash
# US 価格ポイント ID を取得してから scripts/add_prices.py を実行
python3 ~/.claude/skills/mobileapp-builder/scripts/add_prices.py \
  --annual-sub "<ANNUAL_ID>" \
  --annual-pp "<ANNUAL_US_PP_ID>" \
  --monthly-sub "<MONTHLY_ID>" \
  --monthly-pp "<MONTHLY_US_PP_ID>"

# 確認（175 でなければ STOP）
asc subscriptions prices list --id "<MONTHLY_ID>" --paginate | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d['data']))"
```

詳細手順 → `references/iap-bible.md` の「価格ポイント ID の取得方法」

### PHASE 6: IAP LOCALIZATION
```bash
asc subscriptions localizations create --subscription-id "<MONTHLY_ID>" \
  --locale "en-US" --name "<app_name> Monthly" \
  --description "Unlock all features with monthly subscription."

asc subscriptions localizations create --subscription-id "<MONTHLY_ID>" \
  --locale "ja" --name "<app_name> 月額プラン" \
  --description "月額プランで全機能を解放します。"

# Annual も同様（en-US + ja）
```

### PHASE 7: IAP REVIEW SCREENSHOT

> **⚠️ 絶対ルール（2026-02-24 実機検証済み）**
>
> | ルール | 理由 |
> |--------|------|
> | **リサイズ禁止** | `900×1956` 等の任意リサイズ → Apple「寸法が正しくありません」エラーで即拒否 |
> | **ネイティブ解像度をそのまま使う** | iPhone 16 Pro Max シミュレータ = **1320×2868**。これが Apple 標準サイズ |
> | **JPEG変換のみ** | `sips -s format jpeg`（`-z` フラグ使用禁止） |
> | **CLI が full upload** | `asc subscriptions review-screenshots create --file` = reserve+PUT+commit を内部で全実行 |
> | **width=0 は正常** | upload 直後は常に `imageAsset.width=0`。Apple 非同期処理中。再アップロード不要 |
> | **`asc subscriptions images create` は使わない** | プロモーショナル広告用。IAP review screenshot とは別物 |

**ステップ 1: Booted シミュレータの UDID を取得**
```bash
xcrun simctl list devices | grep Booted
# 例: iPhone 16 Pro Max (AF68C54D-D527-4A19-B4D1-5DEF182D8DE5) (Booted)
# UDID をメモする
```

**ステップ 2: Maestro MCP でアプリを起動しペイウォール画面まで遷移**

Maestro MCP（`mcp__maestro__launch_app` + `mcp__maestro__run_flow`）を使う。
CLI（`maestro test`）は禁止。MCP 経由のみ。

```
# 2-1. アプリ起動
mcp__maestro__launch_app(device_id="<UDID>", appId="<BUNDLE_ID>")

# 2-2. オンボーディング → ペイウォールまで遷移（順番通りに実行）
# Anicca の場合の実証済みフロー:
mcp__maestro__run_flow(device_id="<UDID>", flow_yaml="""
appId: <BUNDLE_ID>
---
- tapOn:
    id: "onboarding-welcome-cta"
""")

# 苦しみ選択画面: 何か1つ選んで「次へ」
mcp__maestro__run_flow(device_id="<UDID>", flow_yaml="""
appId: <BUNDLE_ID>
---
- tapOn: "夜更かし"
- waitForAnimationToEnd
- tapOn: "次へ"
""")

# ライブデモ画面: primary action をタップ
mcp__maestro__run_flow(device_id="<UDID>", flow_yaml="""
appId: <BUNDLE_ID>
---
- tapOn:
    id: "nudge-primary-action"
- waitForAnimationToEnd
""")

# 通知許可画面: 許可ボタンをタップ → ペイウォール表示
mcp__maestro__run_flow(device_id="<UDID>", flow_yaml="""
appId: <BUNDLE_ID>
---
- tapOn:
    id: "onboarding-notifications-allow"
- waitForAnimationToEnd
""")
```

別アプリで画面構成が異なる場合は `mcp__maestro__inspect_view_hierarchy` でペイウォール画面の要素を確認してから遷移する。

**ステップ 3: ペイウォール画面のスクリーンショットを撮影 → JPEG変換**
```bash
# PNG 撮影（ネイティブ解像度: iPhone 16 Pro Max = 1320×2868）
xcrun simctl io "<UDID>" screenshot /tmp/paywall-review.png

# JPEG変換のみ（-z リサイズフラグは絶対に使わない）
sips -s format jpeg /tmp/paywall-review.png --out /tmp/paywall-review.jpg

# サイズ確認（1320×2868 であることを確認）
identify /tmp/paywall-review.jpg 2>/dev/null || sips -g pixelWidth -g pixelHeight /tmp/paywall-review.jpg
```

**ステップ 4: Monthly と Annual 両方にアップロード**
```bash
# Monthly
asc subscriptions review-screenshots create \
  --subscription-id "<MONTHLY_SUB_ID>" \
  --file /tmp/paywall-review.jpg

# Annual
asc subscriptions review-screenshots create \
  --subscription-id "<ANNUAL_SUB_ID>" \
  --file /tmp/paywall-review.jpg

# 成功判定: JSON レスポンスに fileSize > 0 があれば OK
# width=0, height=0 は正常（Apple が非同期で処理中）
```

**エラーハンドリング**

| エラー | 原因 | 対処 |
|--------|------|------|
| `寸法が正しくありません` | リサイズした | 削除して正しいサイズで再アップロード |
| `Screenshot already exists` | 既に存在する | 既存を削除してから再アップロード |
| `Element not found` (Maestro) | 画面遷移が違う | `inspect_view_hierarchy` で現在の画面を確認 |

```bash
# 既存削除（"already exists" 時）
# まず既存 ID を取得
python3 -c "
import os, time, json, requests
import jwt as pyjwt
KEY_ID='<KEY_ID>'; ISSUER_ID='<ISSUER_ID>'
PRIVATE_KEY=open(os.path.expanduser('~/.asc/private_keys/AuthKey_<KEY_ID>.p8')).read()
payload={'iss':ISSUER_ID,'iat':int(time.time()),'exp':int(time.time())+1200,'aud':'appstoreconnect-v1'}
token=pyjwt.encode(payload,PRIVATE_KEY,algorithm='ES256',headers={'kid':KEY_ID})
h={'Authorization':f'Bearer {token}','Content-Type':'application/json'}
r=requests.get('https://api.appstoreconnect.apple.com/v1/subscriptions/<SUB_ID>/appStoreReviewScreenshot',headers=h)
print(r.json()['data']['id'])
"
# → ID を取得したら削除
asc subscriptions review-screenshots delete --id "<EXISTING_ID>" --confirm
# その後 ステップ 4 を再実行
```

### PHASE 8: IAP VALIDATE ★STOP GATE
```bash
# blocking=0 確認
asc validate subscriptions --app "<APP_ID>"
# blocking > 0 なら PHASE 5-7 に戻る

# READY_TO_SUBMIT 確認（両方必須）
asc subscriptions get --id "<MONTHLY_ID>"  # state = READY_TO_SUBMIT ?
asc subscriptions get --id "<ANNUAL_ID>"   # state = READY_TO_SUBMIT ?
# どちらかが MISSING_METADATA なら絶対に次に進まない
```

### PHASE 9: APP ASSETS

#### Step 1: アイコン生成（`app-icon` スキルを使う）

**スキル:** `code-with-beto/skills@app-icon`（インストール: `npx skills add code-with-beto/skills@app-icon -g -y`）

```bash
# Step 1-A: SnapAI の設定確認（OpenAI key が必要）
npx snapai config --show
# → "Not configured" ならユーザーに OpenAI key を要求して設定:
#   npx snapai config --openai-api-key sk-xxxxxxxx

# Step 1-B: SnapAI で 1024×1024 PNG を生成（透過背景）
npx snapai icon \
  --prompt "<app_name> iOS app icon. Minimalist design. <concept_1_line>. Central symbol fills 70% of canvas. No text. Premium, App Store ready." \
  --background transparent \
  --output-format png \
  --style minimalism \
  --quality high
# → ./assets/icon-[timestamp].png に保存される
# ⚠️ 重要: SnapAI は --background transparent を指定しても白背景で出力する。
#   プロンプトで "gradient background" を指定しても無視される。
#   必ず Step 1-C で ImageMagick を使って背景を追加する。

# ⛔ SnapAI 未設定の場合はここで停止。フォールバックなし。
# → ユーザーに「OpenAI API key が必要です: npx snapai config --openai-api-key sk-xxxx」と伝える

# Step 1-C: ImageMagick でグラデーション背景を追加（必須 — App Store は透過NG）
# brew install imagemagick  # 未インストールの場合
ICON_SRC="./assets/icon-[timestamp].png"

# 1. 白背景をアルファ透過に変換
convert "$ICON_SRC" -fuzz 5% -transparent white /tmp/icon-transparent.png

# 2. グラデーション背景を作成してアイコンと合成
convert -size 1024x1024 \
  gradient:"#F5A623-#E8563A" \
  /tmp/icon-transparent.png \
  -compose over -composite \
  /tmp/icon-final.png

# 3. 結果をユーザーに見せて確認（必須 — OKが出るまで色変更して繰り返す）
open /tmp/icon-final.png

# Step 1-D: Xcode xcassets に配置（Swift/Xcode プロジェクト用）
cp /tmp/icon-final.png \
  <output_dir>/<app_name>ios/<app_name>/Assets.xcassets/AppIcon.appiconset/icon.png
# ※ Contents.json の "filename": "icon.png" と一致していること確認
```

**注意: app-icon スキルは本来 Expo 向け（Step 4 以降の iOS 26 .icon フォルダ / app.json は Swift/Xcode では不要）。PNG 生成（Step 3）だけを使う。**

#### Step 2: スクショ生成（screenshot-creator スキル）

→ `.claude/skills/screenshot-creator/SKILL.md` を読んで Step 0〜7 を実行する
  （A/B テストではなく新規生成のため、screenshot-ab の PHASE 1/2 はスキップ）

**⚠️ Pencil 設計の絶対ルール（違反 = テキスト崩れ / 画像表示バグ）:**

| ルール | 理由 |
|--------|------|
| テキストノードに必ず `width: "fill_container"` | 未設定だとフレーム外にはみ出す |
| 日本語ヘッドラインは `fontSize: 22` 以下 | 28px × 14文字でオーバーフロー確認済み |
| 親フレームに `layout: "vertical"` を明記 | 省略すると CaptionArea/MockupArea が横並びになる |
| 画像差し替えは**必ず新しいファイル名** | 同じパスの上書きはPencilキャッシュで反映されない |
| `get_screenshot` = MCP base64のみ（ファイル保存されない） | ASC用ファイルはシミュレータ撮影で別途取得 |

```
[シミュレータ準備（Dynamic Island 除去）]
0. iPhone SE 3rd gen を使う（Dynamic Island/ノッチなし）
   UDID: xcrun simctl list devices | grep "SE (3rd"
   → CBA51D41-D404-4843-AA18-738C5068FFE4 等

   iPhone 14+ を使う場合、Dynamic Island 除去が必要:
   xcrun simctl io "<UDID>" screenshot /tmp/screen_raw.png
   python3 -c "
   from PIL import Image
   img = Image.open('/tmp/screen_raw.png')
   crop = img.crop((0, 185, img.width, img.height))
   crop.save('/tmp/screen_home_v2.png')  # ★新しいファイル名で保存
   "

[EN スクショ]
1. screenshot-creator Step 1: ヒアリング（アプリ名・機能・ターゲット・言語=英語）

2. screenshot-creator Step 2〜3: スタイルガイド取得 + 英語コピー作成
   出力: screen1/2/3 の英語キャプション（採点 8/10 以上で確定）

3. screenshot-creator Step 4: Pencil .pen ファイルにデザイン構築
   raw スクリーンショット確認: docs/screenshots/raw/screen1~3.png が存在するか
   なければ: make capture-only で XCUITest 撮影のみ実行

4. screenshot-creator Step 5〜6: spec-validator（10項目 PASS）→ quality-reviewer（7/10+）

5. screenshot-creator Step 7: PNG 書き出し

   **⚠️ ファイル保存パス絶対ルール（2026-02-24 確定）**

   | 禁止 | 正しいパス |
   |------|-----------|
   | `/tmp/screen1.png` など `/tmp/` 以下 | 禁止。再起動で消える |
   | Node.js スクリプト自作 | 禁止 |
   | HTTP API 直接叩く | 禁止 |

   **正しいパス（プロジェクト内に必ず保存）:**
   ```
   {output_dir}/docs/screenshots/raw/screen1~3.png       ← シミュレータ生PNG（iPhone SE推奨）
   {output_dir}/docs/screenshots/processed/screen1~3.png ← Pencil合成済み
   {output_dir}/docs/screenshots/resized/screen1~3.png   ← ASCアップロード用（1290×2796）
   ```

   **ASC アップロード用ファイルの確保手順（get_screenshot ではなく以下を使う）:**
   ```bash
   # 1. シミュレータから直接 PNG を取得
   xcrun simctl io "<SE_UDID>" screenshot docs/screenshots/raw/screen1.png

   # 2. PIL で DI クロップ（iPhone SE は不要）
   # python3 -c "from PIL import Image; img=Image.open('raw/screen1.png'); img.crop((0,185,img.width,img.height)).save('processed/screen1.png')"

   # 3. App Store 必須サイズにリサイズ
   sips -z 2796 1290 docs/screenshots/processed/screen1.png \
     --out docs/screenshots/resized/en-US/screen1.png
   ```

   出力確認: docs/screenshots/resized/en-US/screen1~3.png（プロジェクト内）

6. Slack 承認（slack-approval スキル）:
   → .claude/skills/slack-approval/SKILL.md を読んで requestApproval() を実行
   → title: "📸 App Store スクリーンショット確認 [EN]"
   → approved → Step 7 へ / denied → Step 1 から再実行

⚠️ ハードゲート（絶対ルール）:
   processed/ の画像を open コマンドで実際に開いて、ヘッドラインテキストが入っているか目視確認する。
   ヘッドラインなし → ASC アップロード禁止。Step 1 から再実行。

[JA スクショ]
7. screenshot-creator Step 1〜7 を日本語コピーで再実行
   出力: docs/screenshots/resized/ja/screen1~3.png（JA 版）

8. Slack 承認（slack-approval スキル）:
   → title: "📸 App Store スクリーンショット確認 [JA]"
   → approved → ASC アップロードへ / denied → Step 7 から再実行

⚠️ ハードゲート（JA も同じ）:
   resized/ja/ の画像を open コマンドで実際に開いて日本語ヘッドラインが入っているか確認。
   入っていない場合は ASC アップロード禁止。
```

#### Step 3: ASC アップロード（EN + JA）

**⚠️ リサイズ必須（スキップ禁止）**
`pencil_export.py` の出力は 780×1688。App Store は **1290×2796** を要求する。

```bash
# ★ リサイズ（必須 — これなしでアップロードすると "invalid screenshot dimensions" で却下）
mkdir -p docs/screenshots/resized/en-US docs/screenshots/resized/ja

for i in 1 2 3; do
  sips -z 2796 1290 docs/screenshots/processed/en/screen${i}.png \
    --out docs/screenshots/resized/en-US/screen${i}.png
  sips -z 2796 1290 docs/screenshots/processed/ja/screen${i}.png \
    --out docs/screenshots/resized/ja/screen${i}.png
done

# EN スクショ（locale: en-US）
asc screenshots upload --app-id "<APP_ID>" --locale en-US \
  --files docs/screenshots/resized/en-US/screen1.png \
          docs/screenshots/resized/en-US/screen2.png \
          docs/screenshots/resized/en-US/screen3.png

# JA スクショ（locale: ja）
asc screenshots upload --app-id "<APP_ID>" --locale ja \
  --files docs/screenshots/resized/ja/screen1.png \
          docs/screenshots/resized/ja/screen2.png \
          docs/screenshots/resized/ja/screen3.png
```

**注意:** `asc screenshots upload` は version localization（初回提出時）用。PPO Treatment localization に使う場合は `screenshot-ab` スキルの Step 7-3 を参照（Apple API 直接呼び出しが必要）。

#### Step 3b: iPad 13" スクショアップロード（Submit に必須 — 2026-02-28 実機確認）

**⚠️ iPad スクショなしでは `asc submit create` が失敗する。必ずアップロードする。**

```bash
# ⚠️ 正しいサイズ: 2048×2732（2064×2752 は IMAGE_INCORRECT_DIMENSIONS エラーで拒否される）
TOKEN=$(python3 -c "
import jwt,time,os,pathlib
key=pathlib.Path(os.path.expanduser(os.environ['ASC_KEY_PATH'])).read_text()
payload={'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1200,'aud':'appstoreconnect-v1'}
print(jwt.encode(payload,key,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'}))
")

VERSION_ID=$(asc versions list --app "<APP_ID>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

EN_LOC_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID/appStoreVersionLocalizations" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['id']) for x in d['data'] if x['attributes']['locale']=='en-US']")

JA_LOC_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID/appStoreVersionLocalizations" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['id']) for x in d['data'] if x['attributes']['locale']=='ja']")

# iPhone 6.7" スクショを iPad サイズ（2048×2732）にリサイズ
mkdir -p /tmp/ipad/en-US /tmp/ipad/ja

for i in 1 2 3; do
  sips -z 2732 2048 docs/screenshots/resized/en-US/screen${i}.png \
    --out /tmp/ipad/en-US/screen${i}.png
  sips -z 2732 2048 docs/screenshots/resized/ja/screen${i}.png \
    --out /tmp/ipad/ja/screen${i}.png
done

# EN iPad アップロード
asc screenshots upload \
  --version-localization "$EN_LOC_ID" \
  --display-type APP_IPAD_PRO_3GEN_129 \
  --files /tmp/ipad/en-US/screen1.png \
          /tmp/ipad/en-US/screen2.png \
          /tmp/ipad/en-US/screen3.png

# JA iPad アップロード
asc screenshots upload \
  --version-localization "$JA_LOC_ID" \
  --display-type APP_IPAD_PRO_3GEN_129 \
  --files /tmp/ipad/ja/screen1.png \
          /tmp/ipad/ja/screen2.png \
          /tmp/ipad/ja/screen3.png

# 確認（3件 APP_IPAD_PRO_3GEN_129 が出ればOK）
asc screenshots list --version-localization "$EN_LOC_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['attributes']['screenshotDisplayType']) for x in d['data']]"
```

#### Step 4: App Store メタデータ入力
```bash
# VERSION_ID を取得
VERSION_ID=$(asc versions list --app "<APP_ID>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

# localizations ディレクトリに .strings ファイルを作成
mkdir -p /tmp/locs/en-US /tmp/locs/ja

# EN metadata
cat > /tmp/locs/en-US/description.txt << 'EOF'
<metadata.description_en>

Terms of Use: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
EOF

cat > /tmp/locs/en-US/keywords.txt << 'EOF'
<metadata.keywords_en>
EOF

cat > /tmp/locs/en-US/title.txt << 'EOF'
<metadata.title_en>
EOF

cat > /tmp/locs/en-US/subtitle.txt << 'EOF'
<metadata.subtitle_en>
EOF

# JA metadata（locale は "ja"。"ja-JP" は無効）
cat > /tmp/locs/ja/description.txt << 'EOF'
<metadata.description_ja>

利用規約: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
EOF

cat > /tmp/locs/ja/keywords.txt << 'EOF'
<metadata.keywords_ja>
EOF

cat > /tmp/locs/ja/title.txt << 'EOF'
<metadata.title_ja>
EOF

cat > /tmp/locs/ja/subtitle.txt << 'EOF'
<metadata.subtitle_ja>
EOF

# upload（App Description に Terms URL が含まれる — Guideline 3.1.2 対応）
asc localizations upload --version "$VERSION_ID" --path /tmp/locs
```

**⚠️ Guideline 3.1.2（2026-02-25 実機確認）:**
- App Description に Terms URL を必ず含める
- アプリ内（Settings 画面）に Terms + Privacy リンクがあれば Paywall には不要
- `asc localizations upload` で CLI から直接更新できる（手動不要）

#### Step 5: copyright + content rights + app pricing 設定（Submit に必須 — 2026-02-28 実機確認）

**⚠️ 3つ全て未設定だと `asc submit create` が `App is not eligible for submission` で失敗する。**

```bash
TOKEN=$(python3 -c "
import jwt,time,os,pathlib
key=pathlib.Path(os.path.expanduser(os.environ['ASC_KEY_PATH'])).read_text()
payload={'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1200,'aud':'appstoreconnect-v1'}
print(jwt.encode(payload,key,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'}))
")

VERSION_ID=$(asc versions list --app "<APP_ID>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

# 1. copyright（著作権）
asc versions update --version-id "$VERSION_ID" --copyright "2025 <Your Name>"
# 確認
asc versions get --version-id "$VERSION_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data']['attributes'].get('copyright','NOT SET'))"

# 2. content rights（コンテンツ配信権 — サードパーティコンテンツなし）
curl -s -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID" \
  -d "{\"data\":{\"type\":\"appStoreVersions\",\"id\":\"$VERSION_ID\",\"attributes\":{\"contentRightsDeclaration\":\"DOES_NOT_USE_THIRD_PARTY_CONTENT\"}}}" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('data',{}).get('attributes',{}).get('contentRightsDeclaration','ERROR'))"
# → DOES_NOT_USE_THIRD_PARTY_CONTENT ✅

# 3. app pricing（無料アプリの場合）
# まず既存の価格設定を確認
asc apps prices list --app "<APP_ID>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print('設定済み:', len(d['data']), '件' if d['data'] else '未設定')"

# 未設定（0件）の場合のみ実行
FREE_PP_ID=$(curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.appstoreconnect.apple.com/v1/appPriceTiers/0/pricePoints?filter[territory]=USA" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.appstoreconnect.apple.com/v1/appPriceSchedules" \
  -d "{\"data\":{\"type\":\"appPriceSchedules\",\"attributes\":{},\"relationships\":{\"app\":{\"data\":{\"type\":\"apps\",\"id\":\"<APP_ID>\"}},\"baseTerritory\":{\"data\":{\"type\":\"territories\",\"id\":\"USA\"}},\"manualPrices\":{\"data\":[{\"type\":\"appPrices\",\"id\":\"freePrice\"}]}},\"included\":[{\"type\":\"appPrices\",\"id\":\"freePrice\",\"attributes\":{\"customerPrice\":\"0\",\"proceeds\":\"0\"},\"relationships\":{\"appPricePoint\":{\"data\":{\"type\":\"appPricePoints\",\"id\":\"$FREE_PP_ID\"}}}}]}}" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(json.dumps(d,ensure_ascii=False)[:200])"
```

#### Step 6: usesIdfa 設定（CRITICAL — 未設定で INVALID_BINARY — 2026-02-28 実機確認）

**⚠️ `usesIdfa: None`（未設定）のまま提出すると Apple の自動バイナリ検証で `INVALID_BINARY` になる。**
**必ず Step 5 の直後に実行する。**

```bash
TOKEN=$(python3 -c "
import jwt,time,os,pathlib
key=pathlib.Path(os.path.expanduser(os.environ['ASC_KEY_PATH'])).read_text()
payload={'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1200,'aud':'appstoreconnect-v1'}
print(jwt.encode(payload,key,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'}))
")

VERSION_ID=$(asc versions list --app "<APP_ID>" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

# usesIdfa を false に設定（IDFA を使わないアプリは false 固定）
curl -s -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID" \
  -d "{\"data\":{\"type\":\"appStoreVersions\",\"id\":\"$VERSION_ID\",\"attributes\":{\"usesIdfa\":false}}}" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print('usesIdfa:', d.get('data',{}).get('attributes',{}).get('usesIdfa','ERROR'))"
# → usesIdfa: False ✅

# 確認: appStoreState が READY_FOR_REVIEW になっていること
asc versions get --version-id "$VERSION_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data']['attributes']['appStoreState'])"
# → READY_FOR_SUBMISSION または PREPARE_FOR_SUBMISSION ✅（INVALID_BINARY でなければOK）
```

**注意:**
- IDFA（IDentifier for Advertisers）を使うアプリは `usesIdfa: true` + 用途申告が必要
- 通常のアプリ（RevenueCat + Mixpanel のみ）は `false` で問題ない
- この設定は提出後に変更不可。変更が必要な場合は再ビルド・再提出が必要

### PHASE 10: BUILD & UPLOAD
```bash
cd <output_dir>/<app_name>ios

# Step 1: Fastlane gym でビルド + IPA 生成（gym = xcodebuild のラッパー。署名/export を自動処理）
FASTLANE_SKIP_UPDATE_CHECK=1 fastlane set_version version:<version>
FASTLANE_SKIP_UPDATE_CHECK=1 FASTLANE_OPT_OUT_CRASH_REPORTING=1 \
  fastlane gym --scheme "<app_name>" --export_method app-store --output_directory ./build
# → ./build/<app_name>.ipa が生成される

# Step 2: ASC CLI でアップロード + バージョン作成（fastlane deliver/pilot は使わない）
asc publish appstore \
  --app "$APP_ID" \
  --ipa "./build/<app_name>.ipa" \
  --version "<version>" \
  --wait \
  --poll-interval 30s
# → processingState = VALID になるまで自動待機

# Step 3: TestFlight ベータグループに配布
BUILD_ID=$(asc builds list --app "$APP_ID" --sort -uploadedDate --limit 1 --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

asc beta-groups list --app "$APP_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);[print(g['id']) for g in d['data']]" | \
  xargs -I{} asc builds add-groups --build "$BUILD_ID" --group {}
# → "Successfully added 1 group(s)" が各グループ分出ればOK
```

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛑 STOP 2 — TestFlight テスト（PHASE 10 完了）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TestFlight にビルドをプッシュ済み。テスターを招待してテストしてください:
  1. TestFlight アプリから {app_name} を入手
  2. 動作・Paywall・購入フローを確認
  3. 問題なければ「OK」と入力 → PHASE 11 に進む
     修正が必要な場合はフィードバックを入力 → PHASE 3 から再実行
slack-approval スキルで承認待ち:
  title: "🧪 TestFlight 確認 — {app_name} v{version}"
  → ✅ 承認 → PHASE 11 に進む
  → ❌ 拒否 → フィードバックを元に修正 → PHASE 3 から再実行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### PHASE 11: PREFLIGHT GATE
```bash
# GATE 1: Greenlight
greenlight preflight <app_dir>  # CRITICAL = 0 でなければ STOP

# GATE 2: IAP（D6-D10）
# D6: prices 175件 / D7: screenshot 存在 / D8: en-US localization
# D9: READY_TO_SUBMIT / D10: validate blocking=0
asc validate subscriptions --app "$APP_ID"

# GATE 3: ASC Validate（メタデータ/ビルド/価格/スクショ/年齢レーティングの API レベル検証 — ASC CLI 0.34.0 新機能）
asc validate --app "$APP_ID" --version "<version>" --strict
# → blocking issues があれば STOP。メタデータ長/必須フィールド/カテゴリ/ビルド添付/価格/スクショ互換性を検証
asc validate iap --app "$APP_ID"
# → IAP のレビュー準備状況を検証

# GATE 4: コード品質チェック（自動）
grep -r "Lorem\|lorem\|placeholder\|TODO\|FIXME" <app_dir>/Sources/ && echo "FAIL" || echo "PASS"

# GATE 5: 外部リンク生死確認（自動）
curl -I "<urls.privacy_en>" -o /dev/null -s -w "%{http_code}" | grep -q "200\|301\|302" || echo "FAIL: privacy_en URL dead"
curl -I "<urls.privacy_ja>" -o /dev/null -s -w "%{http_code}" | grep -q "200\|301\|302" || echo "FAIL: privacy_ja URL dead"
curl -I "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" -o /dev/null -s -w "%{http_code}" | grep -q "200" || echo "FAIL: EULA URL dead"

# GATE 6: スクショ確認（iPhone 6.7" + iPad 13" 両方必須 — 2026-02-28 実機確認）
VERSION_ID_GATE=$(asc versions list --app "$APP_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")
TOKEN_GATE=$(python3 -c "
import jwt,time,os,pathlib
key=pathlib.Path(os.path.expanduser(os.environ['ASC_KEY_PATH'])).read_text()
payload={'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1200,'aud':'appstoreconnect-v1'}
print(jwt.encode(payload,key,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'}))
")
# iPhone 6.7" スクショ確認
asc screenshots list --app "$APP_ID" --locale en-US | python3 -c "import sys,json;d=json.load(sys.stdin);print('PASS' if len(d['data'])>=3 else 'FAIL: EN screenshots <3')"
asc screenshots list --app "$APP_ID" --locale ja | python3 -c "import sys,json;d=json.load(sys.stdin);print('PASS' if len(d['data'])>=3 else 'FAIL: JA screenshots <3')"
# iPad 13" スクショ確認（APP_IPAD_PRO_3GEN_129）
EN_LOC_ID_GATE=$(curl -s -H "Authorization: Bearer $TOKEN_GATE" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID_GATE/appStoreVersionLocalizations" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['id']) for x in d['data'] if x['attributes']['locale']=='en-US']")
curl -s -H "Authorization: Bearer $TOKEN_GATE" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/$EN_LOC_ID_GATE/appScreenshotSets" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);types=[x['attributes']['screenshotDisplayType'] for x in d['data']];print('PASS: iPad set exists' if 'APP_IPAD_PRO_3GEN_129' in types else 'FAIL: iPad 13\" screenshots missing')"

# GATE 7: copyright 確認（2026-02-28 実機確認）
asc versions get --version-id "$VERSION_ID_GATE" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);v=d['data']['attributes'].get('copyright','');print('PASS: copyright set' if v else 'FAIL: copyright not set')"

# GATE 8: content rights 確認（2026-02-28 実機確認）
curl -s -H "Authorization: Bearer $TOKEN_GATE" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID_GATE" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);v=d['data']['attributes'].get('contentRightsDeclaration','');print('PASS: content rights set' if v else 'FAIL: contentRightsDeclaration not set')"

# GATE 9: app pricing 確認（2026-02-28 実機確認）
asc apps prices list --app "$APP_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print('PASS: pricing set' if d['data'] else 'FAIL: app pricing not set')"

# GATE 10: primaryCategory 確認（2026-02-28 実機確認 — 未設定で INVALID_BINARY になる）
APP_INFO_ID_GATE=$(curl -s -H "Authorization: Bearer $TOKEN_GATE" \
  "https://api.appstoreconnect.apple.com/v1/apps/$APP_ID/appInfos" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['id'])")
curl -s -H "Authorization: Bearer $TOKEN_GATE" \
  "https://api.appstoreconnect.apple.com/v1/appInfos/$APP_INFO_ID_GATE/primaryCategory" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);cat=d.get('data',{}).get('id','');print('PASS: primaryCategory=' + cat if cat else 'FAIL: primaryCategory not set → INVALID_BINARY になる')"

# GATE 11: usesIdfa 確認（2026-02-28 実機確認 — 未設定で INVALID_BINARY になる）
curl -s -H "Authorization: Bearer $TOKEN_GATE" \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersions/$VERSION_ID_GATE" | \
  python3 -c "import sys,json;d=json.load(sys.stdin);v=d['data']['attributes'].get('usesIdfa');print('PASS: usesIdfa=' + str(v) if v is not None else 'FAIL: usesIdfa not set → INVALID_BINARY になる。PHASE 9 Step 6 を実行してから再確認')"

# GATE 1〜11 全て PASS でなければ STOP。1つでも FAIL → 修正して再実行
```

### PHASE 11.6: IAP 事前確認（Guideline 2.1）

**🚨 CRITICAL（2026-02-28 実機確認）: `asc subscriptions submit` は初回提出で絶対に使うな。STATE_ERROR になる。**

**IAP は READY_TO_SUBMIT のまま放置してよい。`asc submit create`（PHASE 12）を実行すると自動的に審査に含まれる。これが唯一の正解。**

ソース: Apple 公式ドキュメント「For the first version of an app that includes in-app purchases, you must submit the in-app purchase product at the same time as you submit the version.」

| コマンド | 結果 |
|---------|------|
| `asc subscriptions submit` | ❌ STATE_ERROR.FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION |
| `asc submit create --confirm`（PHASE 12） | ✅ READY_TO_SUBMIT の IAP が自動で含まれ WAITING_FOR_REVIEW |

```bash
# READY_TO_SUBMIT であることを確認するだけ（submitコマンドは一切不要）
asc subscriptions get --id "<MONTHLY_ID>" --output json | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data']['attributes']['state'])"
# → READY_TO_SUBMIT ✅

asc subscriptions get --id "<ANNUAL_ID>" --output json | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data']['attributes']['state'])"
# → READY_TO_SUBMIT ✅

# READY_TO_SUBMIT であれば → 即 PHASE 11.5 へ。asc subscriptions submit は絶対に実行しない。
```

**READY_TO_SUBMIT でなければ STOP → PHASE 5-8 に戻る。**

---

### PHASE 11.5: APP PRIVACY 手動設定（PHASE 12 の前に必須 — API で設定不可）

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛑 STOP 3 — App Privacy 手動設定（PHASE 11.5）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASC API は App Privacy 設定に対応していない（404を返す）。
ユーザーが ASC Web で手動設定する必要がある。
下記の【ユーザー作業】を案内し、「完了」と言われたら PHASE 12 を即実行。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **⚠️ 重要（2026-02-24 実機検証）: App Privacy は ASC API で設定できない**
> `/v1/apps/{id}/appDataUsages` は 404 を返す。ユーザーが ASC Web で手動設定するまで先に進まない。

ユーザーに以下を伝えてから待機する:

```
【ユーザー作業】App Privacy の設定（App Store Connect Web — 所要2分）

1. https://appstoreconnect.apple.com → My Apps → <app_name> を開く
2. 左メニュー「App Privacy」をクリック
3.「データの使用方法を編集」ボタンをクリック
4. 収集するデータカテゴリを選択:
   □ Identifiers（Device ID → Third-Party Advertising, Analytics, App Functionality）
   □ Usage Data（Product Interaction → Analytics）
   ※ 日記エントリー・アファメーションは収集しない（ローカル保存のみ）
5. 各カテゴリで「このデータをユーザーのアカウントやデバイスにリンクしているか？」→「いいえ」
6.「完了」→「保存」
7. 完了したらエージェントに「App Privacy 設定完了」と伝える

設定できるカテゴリの例（アプリによって異なる）:
  - 分析（Identifiers, Usage Data）
  - RevenueCat（Purchase History）
  - 収集しない（Health/Fitness, Sensitive Info など）
```

ユーザーが「完了」と言ったら PHASE 12 に進む。

### PHASE 12: SUBMIT
```bash
# ビルド済みの場合: asc submit create で提出（READY_TO_SUBMIT の IAP が自動的に含まれる）
# 2026-02-28 実機確認: --build は必須フラグ

BUILD_ID=$(asc builds list --app "$APP_ID" --sort -uploadedDate --limit 1 --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

VERSION_ID=$(asc versions list --app "$APP_ID" --output json | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['id'])")

asc submit create \
  --app "$APP_ID" \
  --version-id "$VERSION_ID" \
  --build "$BUILD_ID" \
  --confirm
# → {"submissionId":"...","state":"WAITING_FOR_REVIEW"} ✅
# → READY_TO_SUBMIT の IAP が自動的に審査に含まれる（Apple 公式仕様）

# 確認
asc review submissions-list --app "$APP_ID"
# → state: WAITING_FOR_REVIEW ✅

# ⚠️ asc publish appstore --submit も使えるが upload から全部やり直す（アップロード不要なら submit create が速い）
```

### PHASE 13: REJECTION LOOP（ASC CLI 0.34.0 新機能 — EXPERIMENTAL）
```bash
# リジェクトされた場合の自動対応ループ
# ⚠️ EXPERIMENTAL: Apple 非公式 API（/iris endpoints）を使用。壊れる可能性あり。

# Step 1: リジェクション理由を取得
asc review details-get --app "$APP_ID"
# → 審査詳細（理由・ガイドライン番号）を取得（v0.35.3 確認済み — 2026-02-28）

asc web review list --app "$APP_ID"
# → submission ID を取得（EXPERIMENTAL）

asc web review show --app "$APP_ID" --id "<SUBMISSION_ID>"
# → リジェクション理由 + スレッド + メッセージ + スクショが自動DLされる（EXPERIMENTAL）

# Step 2: 理由に基づいてコード/メタデータを修正
# （修正内容はリジェクション理由による — ガイドライン番号で判断）

# Step 3: 再ビルド → 再提出
FASTLANE_SKIP_UPDATE_CHECK=1 FASTLANE_OPT_OUT_CRASH_REPORTING=1 \
  fastlane gym --scheme "<app_name>" --export_method app-store --output_directory ./build

asc publish appstore \
  --app "$APP_ID" \
  --ipa "./build/<app_name>.ipa" \
  --version "<version>" \
  --wait --submit --confirm

# Step 4: このSKILL.mdにリジェクション原因と修正方法を記録 → git push
# （SELF-IMPROVEMENT RULE に従う）
```

---

## asc workflow（PHASE 9〜12 の一括実行 — オプション）

リポジトリに `.asc/workflow.json` を配置すると、後半フェーズを1コマンドで実行できる:

```bash
# 提出前トリプルチェック
APP_ID=<APP_ID> VERSION=<version> asc workflow run validate-only

# メタデータ + スクショ + validate + publish を一括実行
APP_ID=<APP_ID> VERSION=<version> IPA_PATH=./build/<app_name>.ipa asc workflow run ship
```

workflow.json テンプレート → `references/workflow-template.json`

## 参照ファイル

| ファイル | いつ読む |
|---------|---------|
| `references/iap-bible.md` | PHASE 4-8 の詳細手順・価格ポイント取得方法 |
| `references/spec-template.md` | PHASE 1 の INPUT 確認 |
| `references/submission-checklist.md` | PHASE 11 のゲートチェック全項目 |
| `references/workflow-template.json` | asc workflow の定義テンプレート |
| `scripts/add_prices.py` | PHASE 5 の価格設定実行 |
