# Resource Lister

プロジェクトの Claude Code リソース一覧を表示するスキル。「リソース一覧」「コマンド一覧」「スキル一覧」「エージェント一覧」「何があるか確認」「作成したもの一覧」「Claude リソース」などで起動。

## スキル情報

```yaml
name: resource-lister
description: プロジェクトの Claude Code リソース一覧を表示するスキル。「リソース一覧」「コマンド一覧」「スキル一覧」「エージェント一覧」「何があるか確認」「作成したもの一覧」「Claude リソース」などで起動。
```

## Claude への指示

このスキルが起動されたら、`/shiiman-claude:list` コマンドを実行してください。

### 委譲先コマンド

`/shiiman-claude:list`

### 注意事項

- ✅ SSOT（Single Source of Truth）パターン: このスキルはコマンドへの委譲のみを行う
- ✅ ユーザーの発話から適切なオプションを判断
  - 「コマンド一覧」→ `/shiiman-claude:list --commands`
  - 「スキル一覧」→ `/shiiman-claude:list --skills`
  - 「エージェント一覧」→ `/shiiman-claude:list --agents`
  - 「フック一覧」→ `/shiiman-claude:list --hooks`
  - それ以外 → `/shiiman-claude:list`
