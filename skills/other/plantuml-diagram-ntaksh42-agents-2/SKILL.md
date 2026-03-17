---
name: plantuml-diagram
description: Generate PlantUML diagrams including UML class, sequence, and component diagrams. Use when creating UML diagrams or system architecture visualizations.
---

# PlantUML Diagram Skill

PlantUML記法でUML図を生成するスキルです。

## 主な機能

- **クラス図**: UML class diagrams
- **シーケンス図**: Interaction diagrams
- **アクティビティ図**: Workflow diagrams
- **コンポーネント図**: Architecture diagrams

## クラス図

```plantuml
@startuml
class User {
  +String id
  +String name
  +String email
  +login()
  +logout()
}

class Order {
  +String id
  +Date createdAt
  +Float total
  +addItem()
  +checkout()
}

User "1" -- "*" Order : places
@enduml
```

## シーケンス図

```plantuml
@startuml
actor User
participant Frontend
participant Backend
database Database

User -> Frontend: Login
Frontend -> Backend: POST /api/login
Backend -> Database: SELECT user
Database --> Backend: User data
Backend --> Frontend: JWT token
Frontend --> User: Success
@enduml
```

## バージョン情報
- Version: 1.0.0
