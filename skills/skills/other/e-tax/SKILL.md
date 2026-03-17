---
name: e-tax
description: >
  This skill should be used when the user wants to file their tax return
  electronically via the 確定申告書等作成コーナー (NTA Tax Return Preparation
  Corner) using Claude in Chrome, Antigravity Browser Sub-Agent, or Playwright CLI (fallback). It guides the
  browser-based input of calculated tax data. Trigger phrases include:
  "e-Tax提出", "電子申告", "e-Taxで申告", "作成コーナーに入力",
  "確定申告書等作成コーナー", "作成コーナー", "申告書を提出".
---

# e-Tax 電子申告 — ブラウザ自動化による確定申告書等作成コーナー入力

shinkoku で計算した確定申告データを、確定申告書等作成コーナー（https://www.keisan.nta.go.jp/）に
Claude in Chrome を使ってブラウザ上で入力・提出するためのスキル。

## 前提条件

- `/income-tax` スキルで所得税の計算が完了していること
- `/settlement` スキルで決算書（PL/BS）の作成が完了していること
- `/consumption-tax` スキルで消費税の計算が完了していること（該当者のみ）
- `shinkoku.config.yaml` が設定済みであること
- **ブラウザ自動化ツール**がいずれか利用可能であること（下記「ブラウザ自動化方式の選択」参照）

## ブラウザ自動化方式の選択

確定申告書等作成コーナーへの入力には、以下の3つの方式がある。

### 方式 A: Claude in Chrome（推奨）

| 項目 | 内容 |
|-----|------|
| 対象環境 | Windows / macOS のネイティブ Chrome |
| 前提 | Claude in Chrome 拡張機能がインストール済み |
| 利点 | OS 検出の問題なし。追加設定不要 |

### 方式 B: Antigravity Browser Sub-Agent

| 項目 | 内容 |
|-----|------|
| 対象環境 | Windows / macOS / Linux（Antigravity IDE） |
| 前提 | Antigravity IDE がインストール済みで `browser_subagent` ツールが利用可能 |
| 利点 | ネイティブ Chrome を使用するため OS 偽装不要。Linux でも動作 |

### 方式 C: Playwright CLI（フォールバック）

| 項目 | 内容 |
|-----|------|
| 対象環境 | WSL / Linux、または Claude in Chrome・Antigravity が利用できない環境 |
| 前提 | `@playwright/cli` + Playwright CLI スキル + `etax-stealth.js`（OS 偽装スクリプト） |
| 制限 | headed モード必須（QR コード認証に物理操作が必要） |

### 判定ロジック

```
1. Claude in Chrome のツール（browser_navigate 等）が利用可能か？
   → はい: 方式 A を使用
   → いいえ: 次へ

2. Antigravity の browser_subagent ツールが利用可能か？
   → はい: 方式 B を使用
   → いいえ: 次へ

3. Bash ツールで `playwright-cli` コマンドが利用可能か？
   → はい: 方式 C を使用（headed モードで起動）
   → いいえ: エラー表示

   エラーメッセージ:
   「確定申告書等作成コーナーへの入力には、Claude in Chrome、
    Antigravity Browser Sub-Agent、または Playwright CLI が必要です。
    セットアップ方法は README.md の『ブラウザ自動化』セクションを参照してください。」
```

### 方式 B 使用時の操作方法

Antigravity の `browser_subagent` は高レベルなタスク記述で操作する。
各ステップの入力操作を自然言語で記述し、`browser_subagent` に委任する。

例:
- 「https://www.keisan.nta.go.jp/kyoutu/ky/sm/top_web#bsctrl を開く」
- 「『マイナンバーカードをお持ちですか』で『はい』のラジオボタンをクリック」
- 「name='sonekiKeisansyoFromMonth' の入力欄に '1' を入力」

※ Antigravity はネイティブ Chrome を使用するため、`etax-stealth.js` による OS 偽装は不要。

### 方式 C 使用時のセッション開始手順

Playwright CLI でブラウザを開く際の手順:

1. 環境変数を設定: `PLAYWRIGHT_MCP_INIT_SCRIPT=skills/e-tax/scripts/etax-stealth.js`
2. ブラウザ起動: `playwright-cli -s=etax open <url> --headed --browser=chrome`
3. 以降のコマンドは `-s=etax` セッション指定で実行

## 設定の読み込み（最初に実行）

1. `shinkoku.config.yaml` を Read ツールで読み込む
2. ファイルが存在しない場合は `/setup` スキルの実行を案内して終了する
3. 設定値を把握する:
   - 納税者プロファイル（氏名・住所・マイナンバー等）
   - 事業情報（屋号・業種等）
   - 申告方法（e-Tax/郵送/窓口）

## 進捗情報の読み込み

1. `.shinkoku/progress/progress-summary.md` を Read ツールで読み込む（存在する場合）
2. 以下の引継書を Read ツールで読み込む（存在する場合）:
   - `.shinkoku/progress/06-settlement.md` — 決算結果（PL/BS データ）
   - `.shinkoku/progress/07-income-tax.md` — 所得税計算結果
   - `.shinkoku/progress/08-consumption-tax.md` — 消費税計算結果
   - `.shinkoku/progress/02-assess.md` — 課税判定結果
3. `.shinkoku/progress/10-etax.md` の `status` を確認する:
   - `status: interrupted` の場合 → 下記「中断・再開プロトコル」の **再開手順** に従う
   - `status: completed` の場合 → ユーザーに完了済みである旨を伝え、再実行の意図を確認する
4. 計算結果がまだ存在しない場合は、先に `/income-tax` や `/settlement` の実行を案内する

## 中断・再開プロトコル

全ステップ共通のルール。ユーザーが中断を要求した場合（「中断したい」「今日はここまで」「また続きから」等）、以下の手順に従う。

### 中断手順

1. **現在のステップの入力内容を確認する** — 未保存の入力がないか確認
2. **.data ファイルのダウンロードを案内する** — AskUserQuestion で以下を表示:

```
作成コーナーの入力データを .data ファイルとして保存することを推奨します。
画面上部の「入力データの一時保存」ボタン（またはページ下部の「ここまでの入力データを保存する」リンク）
をクリックし、ファイルをダウンロードしてください。

ダウンロードが完了したら「ダウンロード済み」を選択してください。
```

- 選択肢: 「ダウンロード済み」 / 「スキップ（保存しない）」
- 「スキップ」が選ばれた場合は、次回は最初からやり直しになる可能性がある旨を警告する

3. **進捗ファイルを記録する** — `.shinkoku/progress/10-etax.md` に以下の形式で Write ツールで出力:

```
---
step: 10
skill: e-tax
status: interrupted
last_completed_step: "{最後に完了したステップ番号（例: 3）}"
last_url: "{中断時のブラウザURL}"
data_file_saved: {true/false}
interrupted_at: "{当日日付 YYYY-MM-DD}"
fiscal_year: {tax_year}
---

# e-Tax 電子申告（中断）

## 中断時点の状況

- 最後に完了したステップ: ステップ{N}
- 中断時のURL: {URL}
- .data ファイル保存: {済/未}

## 次回の再開方法

1. `/e-tax` スキルを再実行する
2. .data ファイルがある場合は「保存データを利用して作成」から再開する
3. .data ファイルがない場合はステップ0からやり直す
```

4. **ユーザーに中断完了を報告** — 次回の再開方法を案内して終了する

### 再開手順

`.shinkoku/progress/10-etax.md` で `status: interrupted` を検出した場合:

1. 中断時の情報（`last_completed_step`, `data_file_saved`）を読み取る
2. AskUserQuestion で以下を表示:

```
前回の e-Tax 入力はステップ{N}で中断されています。

再開方法を選択してください。
```

- 選択肢:
  - 「.data ファイルから再開する」（`data_file_saved: true` の場合のみ表示）
  - 「最初からやり直す」
  - 「中断記録を破棄して終了する」

3. **.data ファイルから再開する場合**:
   - 確定申告書等作成コーナーのトップページにアクセス
   - 「保存データを利用して作成」→「作成再開」を選択
   - `.data` ファイルのアップロードを案内
   - 読み込み完了後、`last_completed_step` の次のステップから再開する

4. **最初からやり直す場合**:
   - ステップ0 から通常通り開始する

## ステップ0: 必須データの検証

確定申告書等作成コーナーへの入力に必要なデータが揃っているか検証する。

### 検証項目

```
[1] 税額計算済み
    - .shinkoku/progress/07-income-tax.md が存在し、status: completed であること

[2] プロファイル完備
    - 氏名（姓・名）が登録されているか
    - 住所が登録されているか
    - 所轄税務署名が登録されているか

[3] 決算書データ
    - PL/BS の計算結果が取得可能であること

[4] 消費税（該当者のみ）
    - .shinkoku/progress/08-consumption-tax.md が存在し、status: completed であること

[5] サニティチェック
    - `tax_calc.py sanity-check` を実行する
    - error > 0 の場合: 入力を中止し、`/income-tax` スキルで修正を促す
    - warning > 0 の場合: ユーザーに確認してから続行する
```

---

## 画面遷移フロー全体像

```
┌─────────────────────────────────────────────────────┐
│ CC-AA-010 税務署への提出方法の選択                      │
│   マイナンバーカード: はい → スマホ: はい               │
│   → 「スマートフォンを使用する」                        │
└──────────────┬──────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────┐
│ CC-AE-090 作成する申告書等の選択                        │
│   「決算書・収支内訳書（＋所得税）」を選択              │
│   → doSubmitCMW0900(2,'25')                           │
│                                                         │
│   ※ 消費税のみ別途作成する場合:                        │
│   → doSubmitCMW0900(3,'25')                           │
└──────────────┬──────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────┐
│ CC-AE-600 マイナポータル連携の選択                      │
│   → 「マイナポータル連携を利用しない」                  │
└──────────────┬──────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────┐
│ CC-AA-024 e-Taxを行う前の確認                           │
│   → 「利用規約に同意して次へ」                          │
└──────────────┬──────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────┐
│ CC-AA-440 QRコード認証                                  │
│   ★ ユーザーの物理的認証が必要                         │
│   スマートフォンでQRコード読み取り                      │
│   → マイナンバーカード認証完了後、自動遷移              │
└──────────────┬──────────────────────────────────────┘
               ▼
       ┌───────┴───────┐
       ▼               ▼
  決算書コーナー    所得税コーナー
  (事業所得あり)    (給与のみ等)
```

### 決算書コーナーのフロー

```
/kessan/ac/r7/top → ac0300（種類選択）→ aa0200（P/L入力）
  → aa0100（青色特別控除）→ preAoiroCalc（B/S入力）
  → aa0700（所得確認）→ ac0500（住所氏名）→ 印刷/保存
  → 所得税コーナーへ遷移
```

### 所得税コーナーのフロー

```
SS-AA-010a（所得選択）→ SS-AA-050（収入入力ハブ）
  → SS-CA-010（給与入力） / SS-CB-xxx（事業所得） / 雑所得
  → SS-AA-070a（控除1/2）→ SS-AA-080（控除2/2）
  → SS-AA-090（計算結果確認）
  → SS-AC-010a（納付方法）→ SS-AC-020a（住民税等）
  → SS-AC-030（基本情報）→ SS-AC-040（マイナンバー）
  → ステップ5.5（意思決定ゲート）→ ステップ6（電子署名・送信プロトコル）
```

### 消費税コーナーのフロー（所得税完了後）

```
所得税完了 → 「消費税の申告書作成はこちら」

2割特例:
  ac0100(条件判定) → ac0250(所得区分選択) → 売上入力hub → 売上入力detail
  → 売上入力hub → 中間納付 → ac0300(計算結果) → 納税地等
  → ステップ6.5（電子署名・送信プロトコル）

簡易課税:
  ac0100(条件判定) → ac0250(所得区分・事業区分選択) → 売上入力hub → 売上入力detail
  → 売上入力hub → ak2140(仕入税額控除方式選択)※ → 中間納付 → ac0300(計算結果)
  → 納税地等 → ステップ6.5（電子署名・送信プロトコル）
  ※ 2種以上の事業がある場合のみ

一般課税:
  ac0100(条件判定) → ac0250(所得区分選択) → 売上・仕入入力hub → 売上入力detail
  → ai3610(決算額テーブル)※ → 売上・仕入入力hub → 中間納付 → ac0300(計算結果)
  → 納税地等 → ステップ6.5（電子署名・送信プロトコル）
  ※ 積上げ計算選択時のみ
```

---

## ステップ1: 確定申告書等作成コーナーへのアクセス

### 開始URL

**https://www.keisan.nta.go.jp/kyoutu/ky/sm/top_web#bsctrl**

### CC-AA-010: 税務署への提出方法の選択

画面番号: CC-AA-010

1. 「マイナンバーカードをお持ちですか」→ **「はい」** ラジオボタンをクリック
2. 「マイナンバーカード読み取りに対応したスマートフォン又はICカードリーダライタをお持ちですか」→ **「はい」** をクリック
3. **「スマートフォンを使用する」** をクリック
   - JS: `doSubmitCSW0100('1','3','/ky/sm/csw0100_myno_qr')`

### CC-AE-090: 作成する申告書等の選択

画面番号: CC-AE-090

選択肢（令和7年分）:
- **所得税** → `doSubmitCMW0900(1,'25')`
- **決算書・収支内訳書（＋所得税）** → `doSubmitCMW0900(2,'25')` ← 事業所得ありの場合
- **消費税** → `doSubmitCMW0900(3,'25')`
- **贈与税** → `doSubmitCMW0900(4,'25')`

**判断基準**:
- 事業所得あり → 「決算書・収支内訳書（＋所得税）」
- 事業所得なし（給与のみ等）→ 「所得税」
- 消費税は所得税完了後に別途作成

### CC-AE-600: マイナポータル連携の選択

→ **「マイナポータル連携を利用しない」** をクリック

### CC-AA-024: e-Taxを行う前の確認

→ **「利用規約に同意して次へ」** をクリック

※ 環境チェック `termnalInfomationCheckOS_myNumberLinkage()` が実行される。
Windows/macOS の Chrome/Edge であれば問題なし。

### CC-AA-440: QRコード認証

**★ ユーザー操作待ち — ブラウザ操作を一時停止**

この画面ではエージェントがブラウザを操作してはならない。
**AskUserQuestion ツールで一時停止**し、ユーザーが認証完了を報告するまで**絶対に次のステップに進まない**こと。

AskUserQuestion で以下を表示する:

```
QRコード認証画面が表示されました。
スマートフォンのマイナポータルアプリでQRコードを読み取り、
マイナンバーカードで認証してください。

認証が完了したら「認証完了」を選択してください。
```

- 選択肢: 「認証完了」 / 「QRコードが表示されない」
- 「QRコードが表示されない」が選ばれた場合は下記の ⚠️ Playwright CLI 使用時の注意 を参照して対処する
- **ユーザーが「認証完了」を選択するまで、一切のブラウザ操作・画面遷移を行わない**

認証完了後、自動的に次の画面に遷移する。

**⚠️ Playwright CLI 使用時の注意**: `PLAYWRIGHT_MCP_INIT_SCRIPT` 環境変数で `etax-stealth.js` を指定することで
サーバーベイク関数パッチが自動適用されるが、QR コードが表示されない場合はコンソールで `getClientOS()` の
戻り値を確認し、`'Windows'` でなければ以下を手動実行する:
```javascript
window.getClientOS = function() { return 'Windows'; };
displayQrcode();
```

---

## ステップ2: 青色申告決算書の入力（事業所得がある場合）

> ⚠️ **ネイティブダイアログ注意**: 「次へ」クリック後に画面が遷移しない場合、ネイティブダイアログ（alert/confirm）が表示されている可能性がある。技術的な知見の「ネイティブダイアログの検知と対処」を参照。

### /kessan/ac/pre/ac0300: 決算書の種類選択

ラジオボタン:
- **青色申告決算書** ← 青色申告の場合
- 収支内訳書（白色申告の場合）
- 青色申告決算書（現金主義用）

### /kessan/ac/aa0200: 損益計算書（P/L）の入力

URL: `https://www.keisan.nta.go.jp/kessan/ac/aa0200#bsctrl`

#### 期間の入力

| フィールド | name | デフォルト |
|-----------|------|-----------|
| 開始月 | `sonekiKeisansyoFromMonth` | 1 |
| 開始日 | `sonekiKeisansyoFromDay` | 1 |
| 終了月 | `sonekiKeisansyoToMonth` | 12 |
| 終了日 | `sonekiKeisansyoToDay` | 31 |

#### 売上（収入）金額

「入力」ボタン → `/kessan/ac/aa0201` 売上仕入月別入力サブページに遷移。

aa0201 のフィールド:
- `uriageKingaku1`〜`uriageKingaku12`: 月別売上
- `siireKingaku1`〜`siireKingaku12`: 月別仕入
- `kajisyohi`: 家事消費等
- `zatusyunyu`: 雑収入

合計: `uriageKingakuGokei`, `siireKingakuGokei`

#### 経費（行8〜31）

| 行 | 科目 | name（直接入力） | 備考 |
|----|------|-------------------|------|
| 8 | 租税公課 | `sozeiKoka` | |
| 9 | 荷造運賃 | `nidukuriUntin` | |
| 10 | 水道光熱費 | `suidoKonetuhi` | |
| 11 | 旅費交通費 | `ryohiKotuhi` | |
| 12 | 通信費 | `tusinhi` | |
| 13 | 広告宣伝費 | `kokokuSendenhi` | |
| 14 | 接待交際費 | `settaiKosaihi` | |
| 15 | 損害保険料 | `songaiHokenryo` | |
| 16 | 修繕費 | `syuzenhi` | |
| 17 | 消耗品費 | `syomohinhi` | |
| 18 | 減価償却費 | — | 「入力」→ `/kessan/ac/init/aa0203` |
| 19 | 福利厚生費 | `fukuriKoseihi` | |
| 20 | 給料賃金 | — | 「入力」→ `/kessan/ac/aa0205` |
| 21 | 外注工賃 | `gaichukotin` | |
| 22 | 利子割引料 | — | 「入力」→ `/kessan/ac/aa0206` |
| 23 | 地代家賃 | — | 「入力」→ `/kessan/ac/aa0207` |
| 24 | 貸倒金 | `kasidaorekin` | |
| 25 | 税理士等の報酬 | `keihiNiniKingaku1` | 科目名: `keihiNiniKamoku1` |
| 26 | 震災関連経費 | `keihiNiniKingaku2` | 科目名: `keihiNiniKamoku2` |
| 27-30 | 任意科目 | `keihiNiniKingaku3`〜`6` | 科目名: `keihiNiniKamoku3`〜`6` |
| 31 | 雑費 | `zappi` | |

集計 hidden フィールド: `keihiSannyugakuGokei`, `kyuryoTinginTotalGokei`, `risiWaribikiryoGokei`, `tidaiYatinGokei`

#### 繰戻額等

- `kurimodosiNiniKamoku1`/`kurimodosiNiniKingaku1`
- `kurimodosiNiniKamoku2`/`kurimodosiNiniKingaku2`

#### 専従者給与

- `senjusyaKyuyoTotalGokei` (hidden、「入力」ボタンで別画面)
- `kasidaoreKuriireGokei` (hidden)

#### 計算結果（自動）

- `disp_aoiroKojomaeSyotokuKingaku` = 売上 - 売上原価 - 経費 + 繰戻額 - 専従者給与等

### /kessan/ac/submit/aa0100: 青色申告特別控除

Q&A形式で控除額を選択:

| 選択肢 | value | 条件 |
|--------|-------|------|
| 10万円 | 2 | |
| 55万円 | 3 | |
| 65万円 | 1 | **e-Tax送信が必須**。書面提出ではエラー KS-E10089 |

フィールド: `aoiroTokubetuKojoSentakugaku`

65万円を選択する場合、電子帳簿保存または e-Tax 送信が条件。

> ⚠️ **ネイティブダイアログ注意**: 65万円を選択して次へ進むと、書面提出の場合は **KS-E10089**（e-Tax送信が必要）のネイティブダイアログが表示される。画面が遷移しない場合はダイアログの有無をユーザーに確認すること。

### 貸借対照表（B/S）の入力

URL: `/kessan/ac/preAoiroCalc`

#### 資産の部

配列形式: `sisannobuTaisyohyoDetailDataList[N].kisyuKingaku` / `.kimatuKingaku`

| index | 勘定科目 |
|-------|----------|
| 0 | 現金 |
| 1 | 当座預金 |
| 2 | 定期預金 |
| 3 | その他の預金 |
| 4 | 受取手形 |
| 5 | 売掛金 |
| 6 | 有価証券 |
| 7 | 棚卸資産 |
| 8 | 前払金 |
| 9 | 貸付金 |
| 10 | 建物 |
| 11 | 建物附属設備 |
| 12 | 機械装置 |
| 13 | 車両運搬具 |
| 14 | 工具器具備品 |
| 15 | 土地 |
| 16-23 | 任意科目 |

#### 負債・資本の部

配列形式: `fusainobuTaisyohyoDetailDataList[N].kisyuKingaku` / `.kimatuKingaku`

| index | 勘定科目 |
|-------|----------|
| 0 | 支払手形 |
| 1 | 買掛金 |
| 2 | 借入金 |
| 3 | 未払金 |
| 4 | 前受金 |
| 5 | 預り金 |
| 6 | 貸倒引当金 |
| 7-15 | 任意科目 |
| 16 | 元入金 |
| 17 | 事業主借 |
| 18 | 事業主貸 |
| 19 | 青色申告特別控除前の所得金額（P/Lから自動） |

**重要**: 資産期末合計 = 負債期末合計 が必須（KS-E40003）

> ⚠️ **ネイティブダイアログ注意**: 資産期末合計と負債期末合計が一致しない状態で「次へ」を押すと、**KS-E40003** のネイティブダイアログが表示される。画面が遷移しない場合はダイアログの有無をユーザーに確認すること。

### /kessan/ac/ac0500: 住所・氏名等の入力

| フィールド | name |
|-----------|------|
| 郵便番号 | `jitakuZip` |
| 都道府県 | `jitakuPrefectureId` |
| 市区町村以下 | `jitakuAddress` |
| 事業所住所（該当者） | `jimusyoAddress` |
| 提出先税務署 | `zeimusyoName` |
| 氏名漢字（姓） | `nameKanjiSei` |
| 氏名漢字（名） | `nameKanjiMei` |
| 業種名 | `gyosyuName` |
| 屋号 | `yago` |
| 提出年月日 | `teisyutuYear`/`teisyutuMonth`/`teisyutuDay` |

### 決算書完了 → 所得税コーナーへ

印刷・データ保存画面（`/kessan/ac/submit/ac0600`）の
「所得税の申告書作成はこちら」ボタンで所得税コーナーに遷移（住所氏名引継ぎ）。

> ⚠️ **ネイティブダイアログ注意**: このボタンをクリックすると **KS-W10035**（印刷を確認したか）のネイティブダイアログが表示される場合がある。画面が遷移しない場合はダイアログの有無をユーザーに確認し、「OK」をクリックするよう案内すること。

---

## ステップ3: 所得税の申告書入力

> ⚠️ **ネイティブダイアログ注意**: 「次へ」クリック後に画面が遷移しない場合、ネイティブダイアログ（alert/confirm）が表示されている可能性がある。技術的な知見の「ネイティブダイアログの検知と対処」を参照。

### SS-AA-010a: 申告する所得の選択等

URL: `https://www.keisan.nta.go.jp/r7/syotoku/taM010a40_doInitialDisplay#bbctrl`

#### 生年月日

| フィールド | name |
|-----------|------|
| 年 | `inOutDto.shnkkBirthymdYy` |
| 月 | `inOutDto.shnkkBirthymdMm` |
| 日 | `inOutDto.shnkkBirthymdDd` |

#### 所得種類の選択（チェックボックス）

| 所得 | name | 典型的な選択 |
|------|------|-------------|
| 給与 | `inOutDto.kyuy` | 会社員: checked |
| 事業（営業等） | `inOutDto.jgyoEgyoTo` | 個人事業主: checked |
| 事業（農業） | `inOutDto.jgyoNogyo` | |
| 不動産 | `inOutDto.fdosn` | |
| 雑（業務・その他） | `inOutDto.ztsGyomSnt` | 暗号資産等: checked |
| 公的年金等 | `inOutDto.kotkNnknKgyoNnknEtc` | |
| 退職金 | `inOutDto.tasyku` | |
| 株式等 | `inOutDto.hatoKbshkJyotRsh` | |
| 先物取引 | `inOutDto.skmnTrhk` | |
| 一時 | `inOutDto.ichj` | |

**shinkoku 対象の典型パターン**:
- 会社員＋副業（事業所得）: `kyuy` + `jgyoEgyoTo` + `ztsGyomSnt`（暗号資産あれば）
- 給与所得のみ: `kyuy`

### SS-AA-050: 収入・所得の入力ハブ

選択した所得種類ごとに入力リンクが表示される。各リンクをクリックして個別入力画面へ遷移。

### SS-CA-010: 給与所得の源泉徴収票の入力

URL: `https://www.keisan.nta.go.jp/r7/syotoku/taS510a10_doAdd_nncyzm#bbctrl`

#### 主要入力フィールド

| ラベル | name | 備考 |
|--------|------|------|
| A: 支払金額 | `inOutDto.shhraKngk` | 必須 |
| D: 源泉徴収税額 | `inOutDto.gnsnTyosyuZegk` | |
| 社会保険料等の金額 | `inOutDto.sykaHknryoToKngk` | |
| G: 支払者の住所 | `inOutDto.shhrasyJysyKysyOrSyzach` | 28文字以内 |
| H: 支払者の氏名又は名称 | `inOutDto.shhrasyNameOrMesyo` | 28文字以内 |

#### 条件付きフィールド（ラジオで「記載あり」選択時に表示）

| ラベル | name | 表示条件 |
|--------|------|----------|
| 生命保険料控除額 | `inOutDto.semeHknryoKojygk` | `semeHknryoKojygkKsaUm=1` |
| 新生命保険料金額 | `inOutDto.shnSemeHknryoKngk` | 上記あり |
| 旧生命保険料金額 | `inOutDto.kyuSemeHknryoKngk` | 上記あり |
| 介護医療保険料金額 | `inOutDto.kagIryoHknryoKngk` | 上記あり |
| 新個人年金保険料金額 | `inOutDto.shnKjnNnknHknryoKngk` | 上記あり |
| 旧個人年金保険料金額 | `inOutDto.kyuKjnNnknHknryoKngk` | 上記あり |
| 地震保険料控除額 | `inOutDto.jshnHknryoKojygk` | `jshnHknryoKojygkKsaUm=1` |
| 住宅借入金等特別控除額 | `inOutDto.jyutkKrirknToTkbtsKojyGk` | `jyutkKrirknToTkbtsKojyGkKsaUm=1` |

#### ラジオボタン（記載有無の選択）

| フィールド | name | 値 |
|-----------|------|-----|
| 控除対象配偶者の記載 | `inOutDto.kojyTashoHagsyKsaUm` | 1(あり)/2(なし) |
| 控除対象扶養親族の記載 | `inOutDto.kojyTashoFyoShnzkKsaUm` | 1(あり)/2(なし) |
| 生命保険料控除額の記載 | `inOutDto.semeHknryoKojygkKsaUm` | 1(あり)/2(なし) |
| 地震保険料控除額の記載 | `inOutDto.jshnHknryoKojygkKsaUm` | 1(あり)/2(なし) |
| 住宅借入金等特別控除額の記載 | `inOutDto.jyutkKrirknToTkbtsKojyGkKsaUm` | 1(あり)/0(なし) |

### SS-AA-070a: 控除の入力（1/2）— 支出系控除

入力リンクのハブ画面。各控除をクリックして個別入力画面に遷移。

対応控除:
- 社会保険料控除（源泉徴収票入力済みの場合「入力あり」表示）
- 小規模企業共済等掛金控除（iDeCo等）
- 生命保険料控除
- 地震保険料控除
- 雑損控除・災害減免
- 医療費控除
- 寄附金控除（ふるさと納税含む — ワンストップ特例分も要入力）

### SS-AA-080: 控除の入力（2/2）— 人的控除・住宅控除等

対応控除:
- 配偶者（特別）控除
- 扶養控除・特定親族特別控除
- 寡婦・ひとり親控除
- 勤労学生控除
- 障害者控除
- 基礎控除（自動計算表示）
- 住宅借入金等特別控除
- 住宅耐震改修特別控除等
- 予定納税額
- 繰越損失額

### SS-AA-090: 計算結果の確認

入力内容から計算された所得税額の確認画面。

表示項目:
- 収入金額・所得金額（所得種類別）
- 所得控除合計
- 課税される所得金額（1,000円未満切捨て）
- 上記に対する税額（速算表適用）
- 差引所得税額
- 復興特別所得税額（基準所得税額の2.1%）
- 所得税及び復興特別所得税の額
- 源泉徴収税額
- 申告納税額（100円未満切捨て）/ 還付される税金

**ここで shinkoku の計算結果と照合する**（後述「ステップ5: 申告内容の確認」参照）。

各セクションに「訂正する」ボタンがあり、前画面に戻れる。

### SS-AC-010a: 納付方法等の入力

納付金額が発生した場合に表示。還付の場合は還付口座入力画面（SS-AB-010a）が表示される。

| フィールド | type | name | 備考 |
|-----------|------|------|------|
| 延納を届け出る | checkbox | — | 利子税がかかる旨の注意あり |
| 納付方法 | select | `inOutDto.nofHoho` | 必須 |

納付方法の選択肢:

| value | 方法 |
|-------|------|
| 1 | 振替納税（期限内申告の場合に利用可） |
| 2 | 電子納税（ダイレクト納付/インターネットバンキング） |
| 3 | クレジットカード納付 |
| 5 | コンビニ納付 |
| 6 | 金融機関等での窓口納付 |

還付の場合は還付口座情報の入力:
- 金融機関名、支店名、口座番号、口座名義

### SS-AC-020a: 財産債務・住民税等

住民税に関する設定（給与からの特別徴収 or 自分で納付 等）。

### SS-AC-030: 基本情報の入力

| ラベル | name | 備考 |
|--------|------|------|
| 氏名フリガナ（姓） | `inOutDto.nameKnSe` | 11文字以内 |
| 氏名フリガナ（名） | `inOutDto.nameKnMe` | |
| 氏名漢字（姓） | `inOutDto.nameKnjSe` | 10文字以内 |
| 氏名漢字（名） | `inOutDto.nameKnjMe` | |
| 電話番号（種別） | `inOutDto.rnrkSkKbn` | 自宅/勤務先/携帯 |
| 電話番号（市外） | `inOutDto.shgaKykbn` | |
| 電話番号（市内） | `inOutDto.shnaKykbn` | |
| 電話番号（番号） | `inOutDto.knyusyBngo` | |
| 納税地区分 | `inOutDto.nozeCh` | 1=住所地, 2=事業所等 |
| 郵便番号 | `inOutDto.yubnBngoGnzaAddress` | 7桁 |
| 都道府県 | `inOutDto.tdofknGnzaAddress` | select |
| 市区町村 | `inOutDto.shkcyosnGnzaAddress` | 都道府県連動 select |
| 丁目番地等 | `inOutDto.cyomBnchToGnzaAddress` | 28文字以内 |
| 建物名 | `inOutDto.ttmnMeGoshtsGnzaAddress` | 28文字以内 |
| 提出先税務署（県） | `inOutDto.tesytSkZemsyTdofkn` | select |
| 提出先税務署 | `inOutDto.tesytSkZemsyZemsy` | 県連動 select |
| 職業 | `inOutDto.job` | 11文字以内 |
| 屋号・雅号 | `inOutDto.ygoGgo` | 30文字以内 |
| 世帯主の氏名 | `inOutDto.stanshNameKnj` | |
| 続柄 | `inOutDto.stanshKrTsdkgr` | select |
| 提出年月日 | `inOutDto.tesytYmdYy`/`Mm`/`Dd` | |

### SS-AC-040: マイナンバーの入力

マイナンバー（12桁）を入力する画面。チェックディジットアルゴリズムによる検証あり。

---

## ステップ4: 消費税の申告書入力（該当者のみ）

> ⚠️ **ネイティブダイアログ注意**: 「次へ」クリック後に画面が遷移しない場合、ネイティブダイアログ（alert/confirm）が表示されている可能性がある。技術的な知見の「ネイティブダイアログの検知と対処」を参照。

所得税申告書の完了後、「他の申告書等を作成する」→ `doSubmitCSW0900(3,'25')` で消費税コーナーに遷移。

### ac0100: 条件判定等

URL: `https://www.keisan.nta.go.jp/syouhi/ac0100/submit.htmj#bsctrl`

| フィールド | name | 備考 |
|-----------|------|------|
| 基準期間の課税売上高 | `kijunKazeiUriage` | R5年分 |
| インボイス発行事業者 | `invoice` | true/false |
| 簡易課税制度選択 | `kani` | true/false |
| 経理方式 | `zeikomi` | 税込/税抜 |

#### インボイス=はい の場合に追加表示

| フィールド | name | 備考 |
|-----------|------|------|
| 新たに課税事業者か | `newKazeiJigyosya` | true/false |
| 2割特例を適用するか | `niwariTokurei` | true/false |

#### 一般課税の場合に追加表示

| フィールド | name | 備考 |
|-----------|------|------|
| 仕入税額の計算方法 | `siireKeisanHouhou` | warimodosi/tumiage |

#### 条件判定画面の表示ロジック（基準期間による分岐）

`kijunKazeiUriage`（基準期間の課税売上高）の値によって表示される選択肢が変化する:

| 条件 | 新規課税事業者? | 2割特例? | 簡易課税? |
|------|---------------|---------|---------|
| 基準期間=0, invoice=はい | 表示 | 表示 | 非表示 |
| 基準期間=3,000,000, invoice=はい | 表示 | 表示 | 表示 |
| 基準期間=60,000,000, invoice=はい | 非表示 | 非表示 | 表示 |

**一般課税のみ**: 「税額の計算方法として積上げ計算を選択する方」ボタン（折りたたみセクション内）

#### 分岐ロジック

| 条件 | 遷移先ルート |
|------|-------------|
| インボイス=はい & 2割特例=はい | **2割特例** |
| 簡易課税=はい | **簡易課税** |
| 上記以外 | **一般課税** |

### ac0250: 所得区分の選択

URL: `https://www.keisan.nta.go.jp/syouhi/ac0250/submit.htmj#bsctrl`

該当する所得区分を全て選択する。ヘッダに課税方式（一般課税/簡易課税）と経理方式（税込/税抜）が表示される。

| ラベル | name | 備考 |
|--------|------|------|
| 事業所得（営業等） | `jigyoSyotokuEigyo` | メインターゲット |
| 事業所得（農業） | `jigyoSyotokuNogyo` | |
| 不動産所得 | `fudosanSyotoku` | |
| 雑所得（原稿料等） | `zatuSyotoku` | |
| 業務用固定資産等の譲渡所得 | `jotoSyotoku` | 一般課税のみ表示 |

#### 簡易課税のみ: 事業区分の選択

簡易課税の場合、各所得区分に対して事業区分（第1種〜第6種）のサブ選択がある:

| フィールド | name | 備考 |
|-----------|------|------|
| 事業区分（第1種） | `jigyoSyotokuEigyoJigyoKubun1` | 卸売業 |
| 事業区分（第2種） | `jigyoSyotokuEigyoJigyoKubun2` | 小売業 |
| 事業区分（第3種） | `jigyoSyotokuEigyoJigyoKubun3` | 製造業等 |
| 事業区分（第4種） | `jigyoSyotokuEigyoJigyoKubun4` | その他 |
| 事業区分（第5種） | `jigyoSyotokuEigyoJigyoKubun5` | サービス業等 |
| 事業区分（第6種） | `jigyoSyotokuEigyoJigyoKubun6` | 不動産業 |

#### 一般課税のみ: 業務用固定資産等

| フィールド | name | 備考 |
|-----------|------|------|
| 業務用固定資産等の購入がある | `gyomuyosisanKonyu` | checkbox |

### 売上入力（全ルート共通フォーム）

URL パターン:
- 2割特例: `/syouhi/at3600/inputEigyo.htmj`
- 簡易課税: `/syouhi/ak3600/inputEigyo.htmj`
- 一般課税: `/syouhi/ai3600/inputEigyo.htmj`

| フィールド | name | 備考 |
|-----------|------|------|
| 売上（収入）金額 | `uriageWari` | 必須。税込総額 |
| 免税売上 | `menzeiUriageWari` | |
| 非課税売上 | `hikazeiUriageWari` | |
| 不課税取引 | `jigyoFukazeiUriageWari` | |
| 軽減税率（6.24%）適用分 | `kazeiUriage624PercentWari` | |
| 返還等対価（軽減） | `uriageTaikaKeigen.uriageTaika624Percent` | |
| 返還等対価（標準） | `uriageTaikaKeigen.uriageTaika78Percent` | |
| 貸倒れ発生（軽減） | `kasidaoreKeigen.occurredKasidaore624Percent` | 2割特例・簡易課税のみ |
| 貸倒れ発生（標準） | `kasidaoreKeigen.occurredKasidaore78Percent` | 2割特例・簡易課税のみ |
| 貸倒れ回収（軽減） | `kasidaoreKeigen.recoveredKasidaore624Percent` | 2割特例・簡易課税のみ |
| 貸倒れ回収（標準） | `kasidaoreKeigen.recoveredKasidaore78Percent` | 2割特例・簡易課税のみ |
| 貸倒れ発生有無 | `kasidaore.occurredKasidaoreAns` | 2割特例・簡易課税のみ (radio) |

#### 一般課税のみの追加フィールド

| フィールド | name | 備考 |
|-----------|------|------|
| 非課税返還 | `uriageTaikaKeigen.hikazeiHenkan` | |
| 非課税資産の輸出等返還 | `uriageTaikaKeigen.hikazeiSisanHenkan` | |

### 中間納付税額等の入力（全ルート共通）

| name | 備考 |
|------|------|
| `chukanNofuZei` | 中間納付消費税額 |
| `chukanNofuJotoWari` | 中間納付譲渡割額 |

### 一般課税（積上げ計算）専用: 決算額テーブル

URL: `/syouhi/ai3610/submit.htmj`

積上げ計算選択時のみ表示される大規模フォーム（194項目）。
青色申告決算書の各勘定科目に対して、決算額・課税取引金額・軽減税率分・免税事業者等取引分を入力。

フィールド名パターン: `{科目略称}{列略称}Wari` (割戻し) / `{科目略称}{列略称}Tumi` (積上げ)

列略称: `Kessan`(決算額), `KazeiIgai`(課税取引にならないもの), `Keigen624`(軽減税率分), `MenzeiKeigen`(免税事業者等/軽減), `Menzei`(免税事業者等/標準)

| 科目 | プレフィックス |
|------|---------------|
| 仕入金額 | `siire` |
| 租税公課 | `sozeiKoka` |
| 荷造運賃 | `nidukuri` |
| 水道光熱費 | `suido` |
| 旅費交通費 | `ryohi` |
| 通信費 | `tusin` |
| 広告宣伝費 | `kokoku` |
| 接待交際費 | `settai` |
| 損害保険料 | `songai` |
| 修繕費 | `syuzen` |
| 消耗品費 | `syomohin` |
| 減価償却費 | `genkasyokyaku` |
| 福利厚生費 | `fukurikosei` |
| 給料賃金 | `kyuryo` |
| 外注工賃 | `gaichu` |
| 利子割引料 | `risiWaribiki` |
| 地代家賃 | `jidai` |
| 貸倒金 | `kasidaore` |
| 任意科目 | `niniKamoku25`〜`30` |
| 雑費 | `zappi` |

#### テーブル下の Yes/No 質問（一般課税のみ）

| フィールド | name | 内容 |
|-----------|------|------|
| 発生した貸倒金 | `kasidaoreKeigen.occurredKasidaoreAns` | radio |
| 回収した貸倒金 | `kasidaoreKeigen.recoveredKasidaoreAns` | radio |
| 保税地域からの引取貨物 | `hozeiKeigenIppan.hozeiAns` | radio |
| 課税仕入れに係る対価の返還等 | `siireTaikaKeigenIppan.siireTaikaAns` | radio |
| 課税事業者になった方の棚卸高調整 | `tanaorosiKeigenIppan.oldMenzeiJigyoshaAns` | radio |
| 免税事業者になる方の棚卸高調整 | `tanaorosiKeigenIppan.newMenzeiJigyoshaAns` | radio |

### 簡易課税のみ: 仕入税額控除の控除方式の選択

URL: `/syouhi/ak2140/submit.htmj`

2種以上の事業を営む場合に表示される。以下から選択:
- 原則計算
- 特例計算（2種特例/3種特例/75%特例）

### ac0300: 消費税計算結果の確認

全ルート共通の結果画面。ヘッダ部で「2割特例」「簡易課税」「一般課税」を表示。

表示項目:
- 課税標準額
- 消費税額
- 控除税額小計
- **差引税額**（100円未満切捨て）
- 中間納付税額
- 納付税額
- **地方消費税 譲渡割額**（= 差引税額 × 22/78、100円未満切捨て）
- 中間納付譲渡割額
- **合計納付税額**

#### 一般課税のみの追加表示項目

- 「控除過大調整税額」
- 「課税売上割合」セクション（課税資産の譲渡等の対価の額 / 資産の譲渡等の対価の額）

### 消費税 納税地等の入力

URL パターン（ルートごとに異なる）:
- 2割特例: `/syouhi/at1400/submit.htmj`
- 簡易課税: `/syouhi/ak1400/submit.htmj`
- 一般課税: `/syouhi/ai1400/submit.htmj`

画面は全ルートで同一構造（pageId=ac0400）。

| フィールド | name | type | 備考 |
|-----------|------|------|------|
| 納付方法 | `nofuHohoType` | select | |
| 納税地区分 | `nozeitiKubun` | radio | |
| 郵便番号1 | `nozeitiZipCode1` | text | |
| 郵便番号2 | `nozeitiZipCode2` | text | |
| 都道府県 | `nozeitiPrefectureCode` | select | **住所用コード: 13=東京都** |
| 市区町村 | `municipalityCode` | select | |
| 丁目番地等 | `nozeiti1ElaseMunicipal` | text | |
| 税務署都道府県 | `prefectureCode` | select | **税務署用コード: 15=東京都** ← 住所と異なるコード体系! |
| 税務署 | `sinkokuZeimusyoCode` | select | |
| 氏名カナ（姓） | `simeiKanaSei` | text | |
| 氏名カナ（名） | `simeiKanaMei` | text | |
| 氏名漢字（姓） | `simeiKanjiSei` | text | |
| 氏名漢字（名） | `simeiKanjiMei` | text | |
| マイナンバー1 | `myNumber1` | password | |
| マイナンバー2 | `myNumber2` | password | |
| マイナンバー3 | `myNumber3` | password | |
| 電話番号1 | `telNumber1` | text | |
| 電話番号2 | `telNumber2` | text | |
| 電話番号3 | `telNumber3` | text | |

**⚠️ 注意**: 住所の都道府県コード（`nozeitiPrefectureCode`: 13=東京都）と税務署の都道府県コード（`prefectureCode`: 15=東京都）で**異なるコード体系**が使用されている。

### 消費税 計算結果のテストデータ

| 項目 | 2割特例 (売上5M) | 簡易課税 第5種 (売上5M) | 一般課税 (売上66M, 仕入0) |
|-----|----------------|----------------------|------------------------|
| 課税標準額 | 4,545,000円 | 4,545,000円 | 60,000,000円 |
| 消費税額 | 354,510円 | 354,510円 | 4,680,000円 |
| 控除税額 | 283,608円 (×80%) | 177,255円 (×50%) | 0円 |
| 差引税額 | 70,900円 | 177,200円 | 4,680,000円 |
| 地方消費税譲渡割額 | 19,900円 | 49,900円 | 1,320,000円 |
| **合計納付** | **90,800円** | **227,100円** | **6,000,000円** |

### 3ルートの計算方式の違い

| 項目 | 2割特例 | 簡易課税 | 一般課税 |
|------|---------|----------|----------|
| 控除税額 | 消費税額×80% | みなし仕入率 | 実額（割戻し or 積上げ） |
| 仕入入力 | 不要 | 不要 | 割戻し: 不要 / 積上げ: 決算額テーブル |
| URL prefix | /at**** | /ak**** | /ai**** |

> ⚠️ **ネイティブダイアログ注意**: 消費税コーナー終了時は **2段階のネイティブダイアログ**が表示される — `#otherTax`（他の申告書等を作成しますか？）と `#end`（終了してもよろしいですか？）。画面が遷移しない場合はダイアログの有無をユーザーに確認し、それぞれ適切にクリックするよう案内すること。

---

## ステップ5: 申告内容の確認

作成コーナーの確認画面で、shinkoku の計算結果と一致しているか検証する。

### 検証項目

```
□ 合計所得金額が一致するか
□ 所得控除合計が一致するか
□ 課税所得金額が一致するか
□ 算出税額が一致するか
□ 税額控除が一致するか
□ 復興特別所得税が一致するか
□ 申告納税額（または還付額）が一致するか
□ 消費税の納付税額が一致するか（該当者のみ）
```

不一致がある場合は、差異の原因を調査し、ユーザーに報告する。

---

## ステップ5.5: .data ファイルの保存と次ステップの選択（意思決定ゲート）

**★ ユーザー確認待ち — 明示的な指示なくステップ6（電子署名・送信）に進んではならない**

> **2段階ゲート構造**: ステップ5.5 は「送信フェーズに進むかどうかの意思決定ゲート」。
> ステップ6-3 は「送信ボタン直前の操作ゲート（AI は送信しない、ユーザーが手動で送信する）」。
> 両方のゲートを通過しない限り、送信は実行されない。

申告内容の確認が完了した時点で、以下の手順を実行する。

### .data ファイルのダウンロード案内

ユーザーに .data ファイルの保存を案内する:

```
申告内容の入力と確認が完了しました。

電子署名・送信に進む前に、入力データを .data ファイルとして保存することを強く推奨します。
画面上部の「入力データの一時保存」ボタン（またはページ下部の「ここまでの入力データを保存する」リンク）
をクリックし、ファイルをダウンロードしてください。
```

### 次の操作の選択

AskUserQuestion で以下を表示する:

```
次の操作を選択してください。
```

- 選択肢:
  - 「電子署名・送信に進む」→ ステップ6 へ
  - 「入力内容を見直す」→ 見直したいステップを確認し、該当ステップに戻る
  - 「ここで中断する」→ 中断・再開プロトコルの中断手順に従い終了する

**重要**: ユーザーが「電子署名・送信に進む」を明示的に選択するまで、絶対にステップ6に進まないこと。

---

## ステップ6: 電子署名と送信（所得税）

**前提**: ステップ5.5 でユーザーが「電子署名・送信に進む」を選択済みであること。この前提が満たされていない場合はステップ5.5 に戻る。

### 6-1: 電子署名（ユーザーの手動操作）

マイナンバーカードで電子署名する。署名用パスワード（6〜16桁の英数字）が必要。

**★ ユーザー操作待ち — ブラウザ操作を一時停止**

AskUserQuestion で以下を表示する:

```
電子署名の画面に進みます。
マイナンバーカードで電子署名を行ってください。

署名が完了したら「署名完了」を選択してください。
```

- 選択肢: 「署名完了」 / 「署名で問題が発生した」
- **ユーザーが「署名完了」を選択するまで、一切のブラウザ操作を行わない**

### 6-2: 送信前確認ページでの一次確認

電子署名完了後、送信前の最終確認ページが表示される。

1. ブラウザ上の確認ページの内容を読み取る
2. 主要項目をユーザーに報告する（収入・所得・税額・納付/還付額など）
3. shinkoku の計算結果との照合結果を報告する

### 6-3: ブラウザ操作の一時停止（送信はユーザー操作）

**★★★ 絶対に AI が送信ボタンをクリックしてはならない ★★★**
**★★★ ユーザーが「送信完了」を選択するまで、一切のブラウザ操作を行わない ★★★**

**★ ユーザー操作待ち — ブラウザ操作を一時停止**

AskUserQuestion で以下を表示する:

```
送信前の申告内容確認ページが表示されています。
上記の内容をご確認ください。

問題がなければ、ご自身の操作で画面上の「送信を実行する」ボタンを
クリックしてください。

送信が完了したら「送信完了」を選択してください。
```

- 選択肢: 「送信完了」 / 「入力内容を見直したい」
- 「入力内容を見直したい」が選ばれた場合は、見直したい箇所を確認し、該当ステップに戻る

### 6-4: 送信後の処理（Claude 再開）

ユーザーが「送信完了」を選択したら:

1. **受付番号の記録** — 画面から受付番号を読み取って記録する
2. **受信通知の確認** — メッセージボックスで受信通知を確認する
3. **消費税の申告** — 消費税の申告が必要な場合はステップ6.5 に進む。不要な場合はステップ7 に進む

### 注意事項

- 送信後の修正は「修正申告」として再提出が必要
- ★★★ 送信操作は必ずユーザーの手動操作で行う — エージェントが送信ボタンを自動クリックすることは絶対に禁止 ★★★

## ステップ6.5: 消費税の電子署名と送信（該当者のみ）

消費税の申告が必要な場合、所得税の送信完了後に消費税コーナーで申告書を作成する（ステップ4）。
消費税の入力・確認が完了したら、以下の送信プロトコルに従う。

### 6.5-1: 消費税の送信フェーズに進む前の確認

消費税の計算結果確認（ac0300）と納税地等の入力が完了した時点で、以下を実行する。

**★ ユーザー確認待ち — 明示的な指示なく電子署名・送信に進んではならない**

AskUserQuestion で以下を表示する:

```
消費税の申告内容の入力と確認が完了しました。

電子署名・送信に進む前に、入力データを .data ファイルとして保存することを強く推奨します。
画面上部の「入力データの一時保存」ボタンをクリックし、ファイルをダウンロードしてください。

次の操作を選択してください。
```

- 選択肢:
  - 「電子署名・送信に進む」→ 6.5-2 へ
  - 「入力内容を見直す」→ 見直したい箇所を確認し、該当ステップに戻る
  - 「ここで中断する」→ 中断・再開プロトコルの中断手順に従い終了する

**重要**: ユーザーが「電子署名・送信に進む」を明示的に選択するまで、絶対に送信フェーズに進まないこと。

### 6.5-2: 電子署名（ユーザーの手動操作）

マイナンバーカードで電子署名する。

**★ ユーザー操作待ち — ブラウザ操作を一時停止**

AskUserQuestion で以下を表示する:

```
消費税の電子署名の画面に進みます。
マイナンバーカードで電子署名を行ってください。

署名が完了したら「署名完了」を選択してください。
```

- 選択肢: 「署名完了」 / 「署名で問題が発生した」
- **ユーザーが「署名完了」を選択するまで、一切のブラウザ操作を行わない**

### 6.5-3: 送信前確認ページでの一次確認

電子署名完了後、送信前の最終確認ページが表示される。

1. ブラウザ上の確認ページの内容を読み取る
2. 主要項目をユーザーに報告する（課税標準額・消費税額・差引税額・地方消費税・合計納付税額など）
3. shinkoku の計算結果との照合結果を報告する

### 6.5-4: ブラウザ操作の一時停止（送信はユーザー操作）

**★★★ 絶対に AI が送信ボタンをクリックしてはならない ★★★**
**★★★ ユーザーが「送信完了」を選択するまで、一切のブラウザ操作を行わない ★★★**

**★ ユーザー操作待ち — ブラウザ操作を一時停止**

AskUserQuestion で以下を表示する:

```
消費税の送信前確認ページが表示されています。
上記の内容をご確認ください。

問題がなければ、ご自身の操作で画面上の「送信を実行する」ボタンを
クリックしてください。

送信が完了したら「送信完了」を選択してください。
```

- 選択肢: 「送信完了」 / 「入力内容を見直したい」
- 「入力内容を見直したい」が選ばれた場合は、見直したい箇所を確認し、該当ステップに戻る

### 6.5-5: 送信後の処理（Claude 再開）

ユーザーが「送信完了」を選択したら:

1. **受付番号の記録** — 画面から受付番号を読み取って記録する
2. **受信通知の確認** — メッセージボックスで受信通知を確認する
3. ステップ7 の .data ファイル保存案内に進む

---

## ステップ7: .data ファイルの保存案内

作成コーナーでは申告データを `.data` ファイルとして保存できる。

### 送信後の .data ファイル再保存（推奨）

送信完了後の `.data` ファイルには受付番号・送信日時等の追加情報が含まれる。
ステップ5.5 で保存済みであっても、**送信後に改めて .data ファイルを再保存する**ことを推奨する。

AskUserQuestion で以下を表示する:

```
送信が完了しました。送信後の .data ファイルには受付番号等の情報が追加されています。
「入力データを保存する」で .data ファイルを再度ダウンロードすることを推奨します。

ダウンロードが完了したら「ダウンロード済み」を選択してください。
```

- 選択肢: 「ダウンロード済み」 / 「スキップ」

### .data ファイルの用途

- `.data` ファイルがあれば、次回は「保存データを利用して作成」から途中再開できる
- 控えとしても有用（来年の申告時に前年データとして参照可能）
- 修正申告が必要になった場合、`.data` ファイルから入力データを復元できる

---

## 技術的な知見

### SPA構造

- jQuery 3 + jQuery UI ベース
- ページ遷移はフォーム POST（`document.forms[formName].submit()`）
- ハッシュ `#bsctrl`（決算書コーナー）/ `#bbctrl`（所得税コーナー）はページ管理用
- `<input type="button">` が多用されており、`id="input_xxx"` で JS `.click()` 操作

### URL体系

| コーナー | URL パターン |
|---------|-------------|
| 共通（認証等） | `/kyoutu/ky/sm/***` |
| 決算書 | `/kessan/ac/***` |
| 所得税 | `/r7/syotoku/***` |
| 消費税（共通） | `/syouhi/ac****` |
| 消費税（2割特例） | `/syouhi/at****` |
| 消費税（一般課税） | `/syouhi/ai****` |
| 消費税（簡易課税） | `/syouhi/ak****` |

### 主要ナビゲーション関数

- `doSubmitCSW0100(qrCodeReadingFlag, reportType, url)` — 認証方法選択
- `doSubmitCMW0900(zeimokuType, year)` — 申告書種類選択（1=所得税, 2=決算書, 3=消費税, 4=贈与税）

### 確認ダイアログ

| コード | 内容 | 対応 |
|--------|------|------|
| KS-W90011 | 入力データが初期化される | OK で続行 |
| KS-W90006 | 入力データをクリアする | OK で続行 |
| KS-W10035 | 印刷を確認したか | OK で続行 |
| KS-E10089 | e-Tax送信が必要（65万円控除） | e-Tax ルートで再実行 |
| KS-E10001 | 必須入力チェック | 入力漏れを修正 |
| KS-E40003 | B/S 資産期末合計 ≠ 負債期末合計 | 金額を修正 |

### 終了ダイアログフロー

消費税コーナー終了時は2段階のダイアログが表示される:
1. `#otherTax` — 「他の申告書等を作成しますか？」
2. `#end` — 「終了してもよろしいですか？」

※ 書面提出選択時はサーベイダイアログが毎回表示される（セッション間で記憶されない）

### ネイティブダイアログの検知と対処

Claude in Chrome は `alert()` / `confirm()` / `prompt()` によるネイティブダイアログを**検知できない**。
ダイアログが表示されている間、ブラウザの DOM 操作はブロックされるため、エージェントの操作が無応答になる。

#### 検知ヒューリスティック

ボタンクリック後に以下の状態が続く場合、ネイティブダイアログが表示されている可能性がある:

- URL が変化しない
- DOM の内容が変化しない（新しい画面に遷移しない）
- ボタンのクリックが何も起こさないように見える

#### 対処手順

1. ダイアログの可能性を検知したら、AskUserQuestion で以下を表示する:

```
ボタンをクリックしましたが、画面が遷移しません。
ブラウザにポップアップ（確認ダイアログ）が表示されていませんか？

表示されている場合は、ダイアログの内容（コード番号がある場合はそれも）を教えてください。
```

- 選択肢: 「ダイアログが表示されている」 / 「ダイアログは表示されていない」

2. ダイアログが表示されている場合:
   - ユーザーにダイアログのメッセージ内容を確認する
   - 既知のコード（上記「確認ダイアログ」テーブルの KS-W*, KS-E* 等）に該当するか照合する
   - KS-W 系（警告）: ユーザーに「OK」をクリックするよう案内
   - KS-E 系（エラー）: エラー内容に応じた修正を案内
   - 不明なダイアログ: ユーザーにメッセージ全文を共有してもらい、対処を判断

3. ダイアログが表示されていない場合:
   - ネットワークエラーやページ読み込み中の可能性を調査する
   - ページの再読み込みを試みる

#### ダイアログが発生しやすい操作

| 操作 | 想定ダイアログ | ステップ |
|------|--------------|---------|
| 「次へ進む」クリック全般 | KS-E10001（必須入力チェック） | 2, 3, 4 |
| 65万円控除の選択 | KS-E10089（e-Tax送信必須） | 2 |
| B/S 入力後の「次へ」 | KS-E40003（資産≠負債） | 2 |
| 決算書完了→所得税遷移 | KS-W10035（印刷確認） | 2→3 |
| 消費税コーナー終了 | `#otherTax` + `#end`（2段階） | 4 |
| データクリア・初期化操作 | KS-W90011, KS-W90006 | 全般 |

### 環境チェック（参考）

確定申告書等作成コーナーの推奨環境:
- Windows 11 + Chrome / Edge
- macOS + Safari

Linux は公式非対応。OS 検出は **2層** で行われるため、回避にも2層の偽装が必要:

1. **クライアントサイド検出**: CC-AA-024 の画面遷移時に `termnalInfomationCheckOS_myNumberLinkage()` が
   `navigator.platform` / `navigator.userAgent` を検査し、Linux 環境では `isTransition=false` となり
   QR コード認証画面（CC-AA-440）への遷移がブロックされる。

2. **サーバーサイド OS ベイク**: サーバーが HTTP リクエストの `User-Agent` / `sec-ch-ua-platform` ヘッダ
   から OS を判定し、レスポンス内の `getClientOS()` 関数に `const os = "Linux"` のようにハードコードする
   （サーバーサイドレンダリング）。`addInitScript` による navigator プロパティ偽装ではこのベイク値は変わらない。
   CC-AA-440 の `displayQrcode()` でも `getClientOS()` が呼ばれ、`oStUseType` を決定する
   （Win=`'3'`, Mac=`'4'`）。Linux だと `undefined` になり QR コードが描画されない。

#### `etax-stealth.js` の2層偽装

`PLAYWRIGHT_MCP_INIT_SCRIPT` 環境変数で `etax-stealth.js` を指定して回避可能:

```bash
PLAYWRIGHT_MCP_INIT_SCRIPT=skills/e-tax/scripts/etax-stealth.js \
  playwright-cli -s=etax open https://www.keisan.nta.go.jp/ --headed --browser=chrome
```

**層 1: navigator プロパティ偽装**（`addInitScript` で実行、ページ読み込み前）

| プロパティ | 偽装値 |
|-----------|--------|
| `navigator.platform` | `'Win32'` |
| `navigator.userAgent` | Windows Chrome 131 UA |
| `navigator.userAgentData` | Windows Chrome Client Hints |
| `navigator.webdriver` | `false` |
| `navigator.plugins` | Chrome 標準プラグイン |
| `navigator.languages` | `['ja', 'en-US', 'en']` |

**層 2: サーバーベイク関数のパッチ**（`DOMContentLoaded` で実行、ページスクリプト後）

| パッチ対象 | 偽装値 | 目的 |
|-----------|--------|------|
| `getClientOS()` | `'Windows'` | サーバーベイク値の上書き |
| `getClientOSVersionAsync()` | `'Windows 11'` | OS バージョン判定の回避 |
| `isRecommendedOsAsEtaxAsync()` | `true` | 推奨 OS 判定の回避 |
| `isRecommendedBrowserAsEtaxAsync()` | `'OK'` | 推奨ブラウザ判定の回避 |

#### トラブルシューティング: QR コードが表示されない

CC-AA-440 で QR コードが表示されない場合、`displayQrcode()` 内で `getClientOS()` が `'Linux'` 等を返し、
`oStUseType` が `undefined` になっている可能性がある。

**確認方法**: ブラウザコンソールで `getClientOS()` の戻り値を確認。`'Windows'` でなければパッチが適用されていない。

**手動対処**（Playwright CLI の場合）:
```bash
playwright-cli -s=etax run-code 'window.getClientOS = function() { return "Windows"; }; displayQrcode();'
```

#### 検証済み画面遷移フロー

CC-AA-010 → CC-AE-090 → CC-AE-600 → CC-AA-024 → CC-AA-440（QR 表示確認済み）

詳細は `docs/wsl-os-detection-workaround.md` を参照。

---

## 引継書の出力

全ステップ完了後、以下のファイルを Write ツールで出力する。

### ステップ別ファイルの出力

`.shinkoku/progress/10-etax.md` に以下の形式で出力する:

```
---
step: 10
skill: e-tax
status: completed
completed_at: "{当日日付 YYYY-MM-DD}"
fiscal_year: {tax_year}
---

# e-Tax 電子申告の結果

## 提出方法

- 確定申告書等作成コーナー（Claude in Chrome 入力代行）

## 税額サマリー

- 事業所得: {金額}円
- 課税所得: {金額}円
- 所得税額: {金額}円
- 申告納税額: {金額}円（{納付/還付}）
- 消費税納付額: {金額}円（該当者のみ）

## 送信結果

- 受付番号: {受付番号}
- 送信日時: {日時}

## 次のステップ

/submit で提出後のチェックリストを確認する
```

### 進捗サマリーの更新

`.shinkoku/progress/progress-summary.md` を更新する（存在しない場合は新規作成）:

- YAML frontmatter: fiscal_year、last_updated（当日日付）、current_step: e-tax
- テーブル: 全ステップの状態を更新（e-tax を completed に）

---

## 免責事項

- 確定申告書等作成コーナーの画面構成・フォーム要素は国税庁の更新により変更される可能性がある
- Claude in Chrome の入力代行はユーザーの目視確認を前提とする — 自動送信は行わない
- マイナンバーカードの操作（電子署名）はユーザーの手動操作が必要
- 最終的な申告内容は税理士等の専門家に確認することを推奨する

## 調査資料

詳細なセレクタ情報・スクリーンショットは `skills/e-tax/research/` ディレクトリを参照:
- `00-screen-flow-summary.md` — 画面遷移マップ
- `01`〜`05` — 認証フロー画面
- `06`〜`14` — 決算書コーナー画面
- `30`〜`41` — 所得税コーナー画面
- `50`〜`55` — 消費税コーナー画面（初期調査）
- `84`〜`87` — 消費税 2割特例（条件判定、売上入力、計算結果）
- `89`〜`93` — 消費税 簡易課税（条件判定、事業区分、売上入力、控除方式、計算結果）
- `94`〜`98` — 消費税 一般課税（条件判定、所得区分、売上入力、決算額テーブル、計算結果）
