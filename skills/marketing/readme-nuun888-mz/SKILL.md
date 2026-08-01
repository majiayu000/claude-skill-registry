---
name: readme-nuun888-mz
description: Archived skill guidance for readme-nuun888-mz.
---

# [設置型スキル](https://raw.githubusercontent.com/nuun888/MZ/master/NUUN_StationarySkill.js)
# Ver.1.1.1
[ダウンロード](https://raw.githubusercontent.com/nuun888/MZ/master/NUUN_StationarySkill.js)
#### 必須、前提プラグイン
[共通処理](https://github.com/nuun888/MZ/blob/master/README/Base.md)

対象のバトラーの指定のステートが自動解除されたときにそのバトラーに対してスキルを発動します。
スキルのステータスは設置型スキルのステートを付加させたバトラーのステータスになります。

## 設定
ステートのメモ欄
`<StationarySkill:[id]>` ステートのターン経過による解除で指定のIDのスキルを発動します。
`[id]`:プラグインパラメータの設置型スキル設定のID。

## 更新履歴
2024/1/2 Ver.1.1.1
設置型スキルが発動したときにコマンドを選択するとエラーが出る問題を修正。
設置型スキルでステートを付加させたときに、ターン制でターン終了処理を実行できない問題を修正。
TPB制で設置型スキル発動時にTPBゲージが消費されてしまう問題を修正。
2023/6/17 Ver.1.1.0
通常のスキル発動メッセージとは別に、対象名も設定できる発動時のメッセージを設定できる機能を追加。
カウンター、反射を考慮しないように修正。
2023/6/15 Ver.1.0.0
初版。
