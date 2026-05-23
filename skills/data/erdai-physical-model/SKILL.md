---
name: erdai-physical-model
description: Convert ERDAI logical model into physical schema docs with table/column types, PK/FK/index/comments.
---

# ERDAI Physical Modeling Skill

## Read first
- docs/modeling/logical-model.md
- docs/modeling/physical-model.md
- docs/modeling/naming-rules.md
- docs/erd/erd-physical.md
- docs/db-connection.md

## Do in order
1. 엔티티→테이블 매핑
2. 컬럼/타입/NULL/PK/FK/INDEX 정의
3. table_comment/column_comment 보강
4. DBMS 차이 메모 갱신
5. 체크리스트 점검

## Constraints
- 기존 이름 변경 금지
- 민감정보 평문 저장 금지
