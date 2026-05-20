---
name: task
description: 복잡한 다단계 작업의 진행 상황 추적 및 관리
enabled: true
---

## 작업 큐 도구

복잡하거나 오래 걸리는 작업의 진행 상황을 SQLite에 기록하여 추적합니다.

### 사용 가능한 도구

- **task_create**: 새 작업 항목 생성 (상태: running으로 시작)
- **task_list**: 작업 목록 조회 (전체 또는 상태별 필터링)
- **task_complete**: 작업을 완료(completed)로 표시하고 결과 기록
- **task_fail**: 작업을 실패(failed)로 표시하고 이유 기록

### 사용법

- 여러 단계가 필요한 복잡한 작업을 시작할 때 task_create로 추적 항목을 만드세요.
- 작업 완료 또는 실패 시 반드시 상태를 업데이트하세요.
- /tasks 명령으로 사용자가 현재 진행 중인 작업을 확인할 수 있습니다.
