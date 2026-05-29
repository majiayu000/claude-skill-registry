# OpenCode Ralph Loop - 反復開発支援

**opt-in、既定OFF、乱用禁止**の反復開発スキルです。

## 使用前チェック（すべて満たすこと）

1. **仕様が明確に固まっている**
2. **反復可能なタスク**
3. **上限設定が可能**
4. **コスト許容範囲内**

## 実行手順

### 1. 一時的に有効化

`.opencode/oh-my-opencode.json`:
```json
{
  "ralph_loop": {
    "enabled": true,
    "default_max_iterations": 10
  }
}
```

### 2. ディレクトリ準備

```bash
mkdir -p .opencode/state .opencode/runs
```

### 3. Ralph Loop 実行

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
opencode /ralph-loop "Implement feature X" \
  --max-iterations=10 \
  --completion-promise="All tests pass and coverage > 80%" \
  > .opencode/runs/ralph_${TIMESTAMP}.log 2>&1
```

### 4. ログ退避（memory_add）

```
memory_add で .opencode/runs/ralph_${TIMESTAMP}.log を保存
→ referenceId を取得
```

### 5. 設定を元に戻す（重要）

```json
{
  "ralph_loop": {
    "enabled": false
  }
}
```

## 禁止事項

- **無制限実行** - 必ず max-iterations を設定
- **曖昧な仕様** - completion-promise が不明確な場合
- **常時有効化** - 使用後は必ず無効化
- **大量ログの投稿** - 会話/Issueに全文を貼る

## 推奨運用

1. **最初は小さく** - max-iterations=5 から開始
2. **監視しながら** - ログを tail -f で確認
3. **使用後は無効化** - enabled: false に戻す
4. **ログは退避** - memory_add で保存
5. **要約のみ投稿** - refId 運用を徹底
