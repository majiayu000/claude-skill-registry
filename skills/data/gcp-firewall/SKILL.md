---
name: gcp-firewall
description: "GCP 방화벽 규칙 관리"
---

# GCP Firewall Rules

VPC 방화벽 규칙을 조회, 생성, 관리합니다.

## 사용법

```
/gcp-firewall                      # 규칙 목록 조회
/gcp-firewall allow 8080           # TCP 8080 허용 규칙 생성
/gcp-firewall allow 80,443         # 여러 포트 허용
/gcp-firewall delete my-rule       # 규칙 삭제
```

## Workflow

### 1. 방화벽 규칙 목록

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud compute firewall-rules list --project=$PROJECT_ID \
  --format="table(name,network.basename(),direction,priority,allowed[].map().firewall_rule().list():label=ALLOW,sourceRanges.list():label=SRC_RANGES,targetTags.list():label=TARGET_TAGS)"
```

### 2. 규칙 상세 조회

```bash
gcloud compute firewall-rules describe RULE_NAME
```

### 3. 규칙 생성

#### 기본 HTTP/HTTPS 허용

```bash
gcloud compute firewall-rules create allow-http \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:80 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server
```

#### 특정 포트 허용

```bash
gcloud compute firewall-rules create allow-custom-port \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8080 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=custom-server
```

#### 특정 IP만 SSH 허용

```bash
gcloud compute firewall-rules create allow-ssh-office \
  --direction=INGRESS \
  --priority=900 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=1.2.3.4/32 \
  --target-tags=ssh-allowed
```

### 4. VM에 태그 추가

```bash
gcloud compute instances add-tags VM_NAME \
  --zone=ZONE \
  --tags=http-server,custom-server
```

### 5. 규칙 삭제

```bash
gcloud compute firewall-rules delete RULE_NAME
```

## 자주 쓰는 규칙 템플릿

| 용도 | 포트 | 명령어 |
|------|------|--------|
| HTTP | 80 | `--rules=tcp:80 --target-tags=http-server` |
| HTTPS | 443 | `--rules=tcp:443 --target-tags=https-server` |
| SSH | 22 | `--rules=tcp:22 --target-tags=ssh-allowed` |
| MySQL | 3306 | `--rules=tcp:3306 --target-tags=db-server` |
| PostgreSQL | 5432 | `--rules=tcp:5432 --target-tags=db-server` |
| Redis | 6379 | `--rules=tcp:6379 --target-tags=cache-server` |
| Node.js | 3000 | `--rules=tcp:3000 --target-tags=node-server` |
| Flask/Django | 5000,8000 | `--rules=tcp:5000,tcp:8000` |

## 출력 형식

```
## 방화벽 규칙 목록

| 규칙 이름 | 방향 | 허용 | 소스 | 대상 태그 |
|-----------|------|------|------|-----------|
| default-allow-ssh | INGRESS | tcp:22 | 0.0.0.0/0 | - |
| default-allow-http | INGRESS | tcp:80 | 0.0.0.0/0 | http-server |
| allow-custom | INGRESS | tcp:8080 | 0.0.0.0/0 | custom-server |

---
총 3개 규칙
```

## 보안 모범 사례

1. **최소 권한 원칙**: 필요한 포트만 열기
2. **소스 IP 제한**: 가능하면 `0.0.0.0/0` 대신 특정 IP
3. **태그 사용**: 규칙을 특정 VM에만 적용
4. **우선순위**: 거부 규칙은 낮은 숫자 (높은 우선순위)
5. **정기 감사**: 미사용 규칙 정리

## 주의사항

- `0.0.0.0/0`은 전체 인터넷에 노출
- SSH(22)는 가능하면 IAP 터널 사용 권장
- 규칙 삭제 시 연결 끊김 주의
- 같은 우선순위면 거부가 우선
