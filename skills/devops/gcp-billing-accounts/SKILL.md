---
name: gcp-billing-accounts
description: "GCP 결제 계정 목록"
---

# GCP 결제 계정 목록

사용 가능한 GCP 결제 계정 목록을 조회합니다.

## 실행할 명령어

```bash
gcloud billing accounts list
```

## 출력 형식

```
## 결제 계정 목록

| ACCOUNT_ID | NAME | OPEN | 용도 |
|------------|------|------|------|
| 0142CF-B4119B-FAE5BD | REPACT-MAIN | True | 메인 (유료) |
| 01BE16-87467F-4D3098 | INKEUN-PERSONAL | True | 개인 (백업) |

---
현재 기본 결제 계정: [프로젝트별로 다름]
```

## 추가 정보

특정 결제 계정의 상세 정보:
```bash
gcloud billing accounts describe ACCOUNT_ID
```

결제 계정에 연결된 프로젝트 보기:
```
/gcp-billing-projects ACCOUNT_ID
```
