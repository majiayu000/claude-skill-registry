---
name: sub-issue-maker
description: Provide the task granularity for cutting subissues.
---

## Conditions

### もし何かを実装する必要があるなら

DDDをプロジェクトに採用しているため、下記の観点でSub-issueに切れないか検討してください。

- Frontend
  - constantsの修正
  - domainの修正
  - infrastructureの修正（APIを定義・修正したりする場合のみ）
- Backend
  - controllerの修正
  - domainの修正
  - use caseの修正
  - infrastructureの修正（外部APIを新たに定義・修正したり、table schemaを新たに定義・修正したりする必要がある場合のみ）

要件を読んで、他に必要そうなタスクがあれば適宜切ってください（Dockerfileの修正等）

### 他の要件に関して

要件に応じて適切なサイズでtaskを切ってください
