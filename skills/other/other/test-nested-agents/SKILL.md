---
name: test-nested-agents
description: "ネストエージェントパターンの検証テスト用スキル。Use when user says テスト検証, test nested agents, verify agent pattern."
description-en: "Test skill for verifying nested agents pattern. Use when user says テスト検証, test nested agents, verify agent pattern."
description-ja: "ネストエージェントパターンの検証テスト用スキル。Use when user says テスト検証, test nested agents, verify agent pattern."
allowed-tools: ["Read", "Task", "Bash"]
user-invocable: false
metadata:
  skillport:
    category: test
    tags: [test, experimental]
    alwaysApply: false
---

# Test Nested Agents Skill

このスキルは `{skill}/agents/` フォルダにエージェントをパッケージするパターンの検証用です。

## テスト対象

1. スキル内の `agents/` フォルダにエージェントを配置
2. Task tool でそのエージェントを呼び出せるか検証

## 含まれるテストエージェント

| エージェント | 目的 |
|-------------|------|
| test-echo-agent | 入力をエコーバックして動作確認 |

## 検証手順

### パターン A: スキル内エージェントを直接参照

```
Task tool:
  subagent_type: "test-echo-agent"
  prompt: "Echo back: HELLO FROM NESTED AGENT"
```

### パターン B: 相対パスでプロンプトを読み込み

```
1. Read: ./agents/test-echo-agent.md
2. そのプロンプトを使って Task tool で general-purpose を起動
```

## 実行

このスキルが起動したら、以下を順次実行：

1. まず `agents/test-echo-agent.md` の内容を確認
2. パターン A を試行
3. パターン A が失敗したら パターン B を試行
4. 結果をレポート
