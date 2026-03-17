---
name: migrate-links
description: "vault의 [[wikilink]]를 표준 마크다운 링크로 일괄 변환"
argument-hint: ""
plugin-version: "__PLUGIN_VERSION__"
---

# Migrate Links Skill

`[[wikilink]]` → `[text](path.md)` 일괄 변환.

## CLI

```bash
node .obsidian/plugins/oh-my-til/migrate-links.mjs . scan
node .obsidian/plugins/oh-my-til/migrate-links.mjs . migrate
node .obsidian/plugins/oh-my-til/migrate-links.mjs . verify
```

## 워크플로우

1. **스캔**: `scan` 실행 → wikilink 없으면 종료, 있으면 `AskUserQuestion`으로 확인
2. **변환**: `migrate` 실행
3. **검증**: `verify` 실행 → 잔여 wikilink 안내
4. **커밋**: `♻️ refactor: [[wikilink]] → 표준 마크다운 링크 일괄 변환` (push 안 함)

## 변환 규칙

- `[[path|Display]]` → `[Display](path.md)`
- `[[path]]` → `[path](path.md)`
- 코드 블록 내부 제외, 테이블 `\|` 이스케이프 처리
