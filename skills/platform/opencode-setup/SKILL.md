# OpenCode/OMO セットアップ確認と導入ガイド

opt-in設計のセットアップ支援スキルです。

## 使用タイミング

- OpenCodeの導入を検討している場合
- セットアップ状態を確認したい場合
- 設定ファイルの推奨値を知りたい場合

## セットアップ手順

### 1. OpenCode CLI 確認

```bash
opencode --version
```

### 2. OpenCode CLI インストール（未インストールの場合）

公式: https://github.com/opencodeorg/opencode

### 3. Oh My OpenCode (OMO) インストール（オプション）

```bash
bunx oh-my-opencode install
# または
npx oh-my-opencode install
```

### 4. 認証設定

```bash
opencode auth login
```

### 5. 設定ファイルの確認

```bash
# プロジェクト設定
cp .opencode/oh-my-opencode.json.example .opencode/oh-my-opencode.json
```

### 6. 推奨設定

```json
{
  "disabled_hooks": [],
  "disabled_agents": [],
  "ralph_loop": {
    "enabled": false,
    "default_max_iterations": 30,
    "state_dir": ".opencode/"
  }
}
```

**重要**: `ralph_loop.enabled` は既定で `false`。使う時だけ有効化。

## 関連スキル

- `/opencode-fix` - バグ修正支援
- `/opencode-ralph-loop` - 反復開発（必要時のみ）
