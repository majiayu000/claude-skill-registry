---
name: subtask-detection
description: 親IssueからSubtaskを検出し、依存関係を考慮した実行順序（トポロジカルソート）を決定するロジック
---

# Subtask検出 & 依存関係解決

> **参照元**: implement-issues.md から分離されたSubtask検出・依存関係解決ロジック

---

## 概要

親IssueからSubtaskを検出し、依存関係を考慮した実行順序を決定する。

**検出パターン（優先順）**:
1. Issue bodyの `- [ ] #N` チェックリスト形式
2. Issue bodyの `Subtask of #N` 逆参照（子→親）
3. Issue commentsの Subtask作成記録

> **Note**: GitHub Sub-issues API (`trackedInIssues`) は gh CLI では取得不可のため使用しない

---

## Subtask検出

```python
def detect_subtasks(parent_issue_id: int) -> list[int]:
    """親IssueからSubtaskを検出"""
    
    result = bash(f"gh issue view {parent_issue_id} --json body,comments,number,title")
    if not result or result.exit_code != 0:
        report_to_user(f"Issue #{parent_issue_id} の取得に失敗")
        return []
    
    issue_data = json.loads(result.stdout)
    subtask_ids = []
    
    # 1. Issue body からチェックリスト形式を検出
    body = issue_data.get("body", "") or ""
    checkbox_patterns = [
        r"- \[[ x]\] #(\d+)",  # チェックボックス形式
        r"- #(\d+)",           # シンプルなリスト形式
        r"\* #(\d+)",          # アスタリスク形式
    ]
    for pattern in checkbox_patterns:
        matches = re.findall(pattern, body)
        subtask_ids.extend([int(m) for m in matches])
    
    if subtask_ids:
        return list(set(subtask_ids))
    
    # 2. Comments から Subtask作成記録を検出
    comments = issue_data.get("comments", []) or []
    for comment in comments:
        comment_body = comment.get("body", "") or ""
        if any(kw in comment_body for kw in ["Subtask", "subtask", "Sub-issue", "Created #"]):
            matches = re.findall(r"#(\d+)", comment_body)
            subtask_ids.extend([int(m) for m in matches if int(m) != parent_issue_id])
    
    # 3. 逆参照検索
    if not subtask_ids:
        # Note: jq内でPython変数を使うため、f-stringで展開
        search_result = bash(f'''
            gh issue list --state all --limit 100 --json number,body \
            | jq '[.[] | select(.body != null) | select(.body | test("Subtask of #{parent_issue_id}|Parent: #{parent_issue_id}")) | .number]'
        '''.replace('{parent_issue_id}', str(parent_issue_id)))
        if search_result.exit_code == 0 and search_result.stdout.strip():
            subtask_ids.extend(json.loads(search_result.stdout))
    
    return list(set(subtask_ids))
```

---

## Issue解決（Subtask展開）

```python
def resolve_issues(issue_ids: list[int]) -> list[int]:
    """Issue番号リストを解決し、必要に応じてSubtaskを展開"""
    
    if len(issue_ids) == 1:
        parent_id = issue_ids[0]
        subtasks = detect_subtasks(parent_id)
        
        if subtasks:
            report_to_user(f"親Issue #{parent_id} から {len(subtasks)}件のSubtaskを検出")
            return subtasks
        return issue_ids
    
    # 複数指定 → そのまま使用
    return issue_ids
```

---

## 依存関係チェック

```python
def check_subtask_dependencies(subtask_ids: list[int]) -> list[int]:
    """Subtask間の依存関係をチェックし、実行順序を決定"""
    
    dependencies = {}
    
    for issue_id in subtask_ids:
        result = bash(f"gh issue view {issue_id} --json body,title")
        body = json.loads(result.stdout).get("body", "") or ""
        
        # 依存関係パターン: "Depends on #N", "Blocked by #N", "After #N", "Requires #N"
        dep_patterns = [
            r"[Dd]epends on #(\d+)",
            r"[Bb]locked by #(\d+)",
            r"[Aa]fter #(\d+)",
            r"[Rr]equires #(\d+)",
        ]
        
        deps = []
        for pattern in dep_patterns:
            matches = re.findall(pattern, body)
            deps.extend([int(m) for m in matches if int(m) in subtask_ids])
        
        dependencies[issue_id] = list(set(deps))
    
    return topological_sort(subtask_ids, dependencies)
```

---

## トポロジカルソート

```python
def topological_sort(ids: list[int], deps: dict[int, list[int]]) -> list[int]:
    """依存関係を考慮してソート（循環依存検出付き）"""
    
    in_degree = {id: 0 for id in ids}
    for id, dep_list in deps.items():
        for dep in dep_list:
            if dep in in_degree:
                in_degree[id] += 1
    
    sorted_ids = []
    remaining = set(ids)
    
    while remaining:
        ready = [id for id in remaining if in_degree.get(id, 0) == 0]
        
        if not ready:
            raise ValueError(f"循環依存を検出: {remaining}")
        
        for id in ready:
            sorted_ids.append(id)
            remaining.remove(id)
            for other_id in remaining:
                if id in deps.get(other_id, []):
                    in_degree[other_id] -= 1
    
    return sorted_ids
```

---

## 検出結果に応じた処理

| 検出結果 | 処理 |
|---------|------|
| Subtask検出（N件） | 依存関係チェック → 順次実装 |
| Subtaskなし + 200行以下 | 単体実装 |
| Subtaskなし + 200行超 | `/decompose-issue` を案内 |

---

## 依存パターン

| パターン | 検出キーワード |
|---------|---------------|
| 明示的依存 | `Depends on #N`, `Blocked by #N` |
| 順序指定 | `After #N`, `Requires #N` |
| 暗黙的依存 | （検出不可 → 失敗時に報告） |
