---
name: gcp-billing-projects
description: "GCP 결제 계정 프로젝트 목록"
---

# GCP 결제 계정 프로젝트 목록

특정 결제 계정에 연결된 프로젝트 목록을 조회합니다.

## 사용법

```
/gcp-billing-projects                    # REPACT-MAIN (기본)
/gcp-billing-projects 0142CF-B4119B-FAE5BD  # 특정 결제 계정
```

## 결제 계정 ID

| 이름 | ACCOUNT_ID |
|------|------------|
| REPACT-MAIN | 0142CF-B4119B-FAE5BD |
| INKEUN-PERSONAL | 01BE16-87467F-4D3098 |

## 실행할 명령어

```bash
# 기본: REPACT-MAIN
gcloud billing projects list --billing-account=0142CF-B4119B-FAE5BD

# 또는 인자로 받은 결제 계정
gcloud billing projects list --billing-account=ACCOUNT_ID
```

## 출력 형식

```
## [BILLING_ACCOUNT_NAME] 연결된 프로젝트

| PROJECT_ID | NAME | BILLING_ENABLED |
|------------|------|-----------------|
| patent-481206 | patent | yes |
| seo-knowledge-hub | Seo Knowledge Hub | yes |
| ... | ... | ... |

---
총 N개 프로젝트
```

## 관련 스킬

| 스킬 | 용도 |
|------|------|
| `/gcp-billing-accounts` | 결제 계정 목록 |
| `/gcp-project-status [project-id]` | 프로젝트 리소스 상태 |
| `/gcp-billing` | 비용 조회 (Billing Export 필요) |
