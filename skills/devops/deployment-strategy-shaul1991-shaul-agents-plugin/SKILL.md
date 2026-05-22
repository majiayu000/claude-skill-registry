---
name: deployment-strategy
description: Deployment Strategy Agent. Feature Flag, Canary/Blue-Green 배포, 롤백 전략을 담당합니다. 안전한 배포와 점진적 롤아웃을 관리합니다.
allowed-tools: Bash(npm:*, kubectl:*, docker:*), Read, Write, Edit, Grep, Glob
---

# Deployment Strategy Agent

## 역할

안전하고 신뢰할 수 있는 배포 전략을 수립하고 실행합니다.

## 배포 전략 유형

```
┌─────────────────────────────────────────────────────────────────┐
│                        배포 전략 비교                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Big Bang (권장하지 않음)                                         │
│  ┌──────────┐     ┌──────────┐                                  │
│  │  v1.0    │ ──► │  v2.0    │  한 번에 100% 전환                │
│  └──────────┘     └──────────┘  리스크: 높음                     │
│                                                                 │
│  Blue-Green                                                     │
│  ┌──────────┐     ┌──────────┐                                  │
│  │  Blue    │     │  Green   │  두 환경 유지                     │
│  │  (v1.0)  │ ──► │  (v2.0)  │  트래픽 즉시 전환                 │
│  └──────────┘     └──────────┘  롤백: 즉시 가능                  │
│                                                                 │
│  Canary                                                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ v1.0: 100% ──► 90% ──► 50% ──► 0%                    │       │
│  │ v2.0:   0% ──► 10% ──► 50% ──► 100%                  │       │
│  └──────────────────────────────────────────────────────┘       │
│  점진적 롤아웃, 리스크 최소화                                      │
│                                                                 │
│  Feature Flag                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ 코드는 배포됨, 기능은 비활성                            │       │
│  │ Flag ON: 특정 사용자/그룹만 활성화                      │       │
│  │ 문제 시 Flag OFF로 즉시 비활성화                        │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Feature Flag 설정

### LaunchDarkly 설정

```typescript
// src/lib/feature-flags.ts
import * as LaunchDarkly from 'launchdarkly-js-client-sdk';

const client = LaunchDarkly.initialize(
  process.env.LAUNCHDARKLY_CLIENT_ID!,
  {
    key: 'user-id',
    email: 'user@example.com',
    custom: {
      plan: 'premium',
      beta: true,
    },
  }
);

export const isFeatureEnabled = async (flagKey: string): Promise<boolean> => {
  await client.waitForInitialization();
  return client.variation(flagKey, false);
};

// 사용 예시
if (await isFeatureEnabled('new-checkout-flow')) {
  // 새 체크아웃 플로우
} else {
  // 기존 체크아웃 플로우
}
```

### 자체 구현 Feature Flag

```typescript
// src/lib/feature-flags.ts
interface FeatureFlag {
  key: string;
  enabled: boolean;
  percentage: number;
  allowedUsers: string[];
  allowedGroups: string[];
  killSwitch: boolean;
}

const flags: Record<string, FeatureFlag> = {
  'new-feature': {
    key: 'new-feature',
    enabled: true,
    percentage: 10,           // 10% 사용자에게 노출
    allowedUsers: ['admin'],  // 특정 사용자는 항상 활성화
    allowedGroups: ['beta'],  // 베타 그룹은 항상 활성화
    killSwitch: false,        // 긴급 비활성화 스위치
  },
};

export const isEnabled = (
  flagKey: string,
  userId: string,
  userGroups: string[] = []
): boolean => {
  const flag = flags[flagKey];

  if (!flag || !flag.enabled || flag.killSwitch) {
    return false;
  }

  // 특정 사용자 체크
  if (flag.allowedUsers.includes(userId)) {
    return true;
  }

  // 특정 그룹 체크
  if (userGroups.some(g => flag.allowedGroups.includes(g))) {
    return true;
  }

  // 퍼센티지 기반 롤아웃
  const hash = hashUserId(userId);
  return hash < flag.percentage;
};

const hashUserId = (userId: string): number => {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = ((hash << 5) - hash) + userId.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash) % 100;
};
```

### React Hook

```tsx
// src/hooks/useFeatureFlag.ts
import { useEffect, useState } from 'react';
import { isEnabled } from '@/lib/feature-flags';
import { useUser } from '@/hooks/useUser';

export const useFeatureFlag = (flagKey: string): boolean => {
  const [enabled, setEnabled] = useState(false);
  const { user } = useUser();

  useEffect(() => {
    if (user) {
      setEnabled(isEnabled(flagKey, user.id, user.groups));
    }
  }, [flagKey, user]);

  return enabled;
};

// 사용 예시
const MyComponent = () => {
  const showNewFeature = useFeatureFlag('new-feature');

  return showNewFeature ? <NewFeature /> : <OldFeature />;
};
```

## Canary 배포

### Kubernetes Canary

```yaml
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
spec:
  replicas: 1  # 전체의 10%
  selector:
    matchLabels:
      app: myapp
      version: canary
  template:
    metadata:
      labels:
        app: myapp
        version: canary
    spec:
      containers:
      - name: app
        image: myapp:v2.0
        ports:
        - containerPort: 3000

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-stable
spec:
  replicas: 9  # 전체의 90%
  selector:
    matchLabels:
      app: myapp
      version: stable
  template:
    metadata:
      labels:
        app: myapp
        version: stable
    spec:
      containers:
      - name: app
        image: myapp:v1.0
        ports:
        - containerPort: 3000

---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp  # 두 버전 모두 선택
  ports:
  - port: 80
    targetPort: 3000
```

### Canary 롤아웃 스크립트

```bash
#!/bin/bash
# canary-rollout.sh

CANARY_PERCENTAGE=$1
TOTAL_REPLICAS=10

CANARY_REPLICAS=$((TOTAL_REPLICAS * CANARY_PERCENTAGE / 100))
STABLE_REPLICAS=$((TOTAL_REPLICAS - CANARY_REPLICAS))

echo "Rolling out canary: $CANARY_PERCENTAGE%"
echo "Canary replicas: $CANARY_REPLICAS"
echo "Stable replicas: $STABLE_REPLICAS"

# Canary 스케일
kubectl scale deployment app-canary --replicas=$CANARY_REPLICAS

# Stable 스케일
kubectl scale deployment app-stable --replicas=$STABLE_REPLICAS

# 상태 확인
kubectl rollout status deployment/app-canary
kubectl rollout status deployment/app-stable
```

### Canary 롤아웃 단계

```markdown
## Canary 배포 체크리스트

### Stage 1: 10% (1시간)
- [ ] Canary 배포 완료
- [ ] 에러율 < 1%
- [ ] 응답 시간 정상
- [ ] 로그 확인

### Stage 2: 25% (2시간)
- [ ] 트래픽 증가
- [ ] 메트릭 정상
- [ ] 사용자 피드백 없음

### Stage 3: 50% (4시간)
- [ ] 절반 트래픽
- [ ] 성능 저하 없음
- [ ] DB 부하 정상

### Stage 4: 100% (전체 롤아웃)
- [ ] 모든 트래픽 전환
- [ ] 이전 버전 제거
- [ ] 문서 업데이트
```

## Blue-Green 배포

```yaml
# blue-green.yaml
# Blue (현재 프로덕션)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      color: blue
  template:
    metadata:
      labels:
        app: myapp
        color: blue
    spec:
      containers:
      - name: app
        image: myapp:v1.0

---
# Green (새 버전)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      color: green
  template:
    metadata:
      labels:
        app: myapp
        color: green
    spec:
      containers:
      - name: app
        image: myapp:v2.0

---
# Service (트래픽 전환용)
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    color: blue  # green으로 변경하여 전환
  ports:
  - port: 80
    targetPort: 3000
```

### 전환 스크립트

```bash
#!/bin/bash
# switch-traffic.sh

CURRENT_COLOR=$(kubectl get svc app-service -o jsonpath='{.spec.selector.color}')

if [ "$CURRENT_COLOR" == "blue" ]; then
  NEW_COLOR="green"
else
  NEW_COLOR="blue"
fi

echo "Switching from $CURRENT_COLOR to $NEW_COLOR"

# 트래픽 전환
kubectl patch svc app-service -p '{"spec":{"selector":{"color":"'$NEW_COLOR'"}}}'

# 확인
kubectl get svc app-service -o jsonpath='{.spec.selector.color}'
```

## 롤백 전략

### 자동 롤백 조건

```yaml
# rollback-conditions.yaml
rollback:
  automatic: true
  conditions:
    - metric: error_rate
      threshold: 5%
      duration: 5m

    - metric: latency_p99
      threshold: 2000ms
      duration: 5m

    - metric: cpu_usage
      threshold: 90%
      duration: 10m

  actions:
    - type: alert
      channels: [slack, pagerduty]

    - type: rollback
      target: previous_stable

    - type: scale_down
      target: canary
      replicas: 0
```

### 롤백 스크립트

```bash
#!/bin/bash
# rollback.sh

echo "Starting rollback..."

# Kubernetes 롤백
kubectl rollout undo deployment/app

# 또는 특정 버전으로
kubectl rollout undo deployment/app --to-revision=2

# Feature Flag 비활성화
curl -X PATCH https://api.launchdarkly.com/api/v2/flags/project/flag-key \
  -H "Authorization: api-key" \
  -H "Content-Type: application/json" \
  -d '{"patch":[{"op":"replace","path":"/environments/production/on","value":false}]}'

# 상태 확인
kubectl rollout status deployment/app

echo "Rollback completed"
```

## 배포 체크리스트

```markdown
## 배포 전 체크리스트

### 코드 준비
- [ ] 모든 테스트 통과
- [ ] 코드 리뷰 완료
- [ ] 보안 스캔 통과
- [ ] 문서 업데이트

### 환경 준비
- [ ] 환경 변수 설정
- [ ] Secret 업데이트
- [ ] DB 마이그레이션 준비
- [ ] Feature Flag 설정

### 배포 준비
- [ ] 롤백 계획 수립
- [ ] 모니터링 대시보드 준비
- [ ] 알림 채널 확인
- [ ] 온콜 담당자 확인

### 배포 후 체크리스트
- [ ] 헬스체크 통과
- [ ] 에러율 정상
- [ ] 성능 정상
- [ ] 로그 확인
```

## 모니터링 대시보드

```markdown
## 배포 모니터링 지표

### 핵심 지표
| 지표 | 임계값 | 현재 | 상태 |
|------|--------|------|------|
| Error Rate | < 1% | 0.2% | ✅ |
| P99 Latency | < 500ms | 320ms | ✅ |
| CPU Usage | < 80% | 45% | ✅ |
| Memory Usage | < 80% | 62% | ✅ |

### 비즈니스 지표
| 지표 | 기준 | 현재 | 변화 |
|------|------|------|------|
| 전환율 | 3.2% | 3.1% | -0.1% |
| 이탈률 | 45% | 46% | +1% |
| 페이지뷰 | 10K/h | 9.8K/h | -2% |
```

## 산출물 위치

- 배포 계획: `docs/features/<기능명>/implementation/deployment-plan.md`
- 롤백 계획: `docs/features/<기능명>/implementation/rollback-plan.md`
- 배포 체크리스트: `docs/features/<기능명>/gates/gate-6-checklist.md`
