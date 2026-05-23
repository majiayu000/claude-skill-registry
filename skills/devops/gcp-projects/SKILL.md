---
name: gcp-projects
description: "GCP 프로젝트 목록 조회 및 현재 설정 확인"
---

# GCP 프로젝트 조회

현재 GCP 프로젝트 목록과 설정 상태를 조회합니다.

## 수행 작업

1. 현재 활성 계정 확인
2. 현재 기본 프로젝트 확인
3. 접근 가능한 프로젝트 목록 조회
4. 결과를 테이블 형태로 정리

## 실행할 명령어

```bash
# 현재 설정 확인
gcloud config get-value account
gcloud config get-value project

# 프로젝트 목록
gcloud projects list
```

## 출력 형식

조회 결과를 다음 형식으로 정리:

```
현재 설정:
- 계정: xxx@xxx.com
- 기본 프로젝트: project-id

프로젝트 목록:
| PROJECT_ID | NAME | 상태 |
|------------|------|------|
| ... | ... | 현재 선택됨 / - |
```
