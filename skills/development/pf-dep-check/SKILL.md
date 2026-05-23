---
name: pf-dep-check
description: 의존성 검사 및 업데이트. "의존성 체크", "패키지 업데이트", "dep check" 요청 시 사용.
allowed-tools: Read, Bash, Glob
---

# PF 의존성 검사

$ARGUMENTS 의존성을 검사하고 업데이트를 제안합니다.

---

## 검사 항목

### 1. Catalog 버전 확인

```bash
# pnpm-workspace.yaml의 catalog 확인
cat pnpm-workspace.yaml | grep -A 50 "catalog:"
```

### 2. 업데이트 가능한 패키지

```bash
# 전체 업데이트 확인
pnpm outdated

# 특정 패키지만
pnpm outdated react
```

### 3. 보안 취약점

```bash
pnpm audit
```

### 4. 중복 패키지

```bash
pnpm why react
pnpm dedupe --check
```

---

## 주요 패키지 업데이트 가이드

### React 업데이트

```yaml
# pnpm-workspace.yaml
catalog:
  react: ^19.2.0        # 현재
  react-dom: ^19.2.0
  @types/react: ^19.0.0
  @types/react-dom: ^19.0.0
```

**주의사항:**
- React 19는 forwardRef 불필요
- 새 Hooks (use, useOptimistic 등) 사용 가능
- React Compiler 호환성 확인

### Vite 업데이트

```yaml
catalog:
  vite: ^7.3.0
  @vitejs/plugin-react: ^4.5.0
```

**주의사항:**
- vite.config.ts 변경사항 확인
- 플러그인 호환성 확인

### TypeScript 업데이트

```yaml
catalog:
  typescript: ^5.9.0
```

**주의사항:**
- tsconfig.json 새 옵션 확인
- 타입 에러 발생 가능성

### Tailwind CSS 업데이트

```yaml
catalog:
  tailwindcss: ^4.1.0
```

**주의사항:**
- v4는 설정 방식 변경됨
- postcss 설정 확인

---

## 업데이트 절차

### 1. Minor/Patch 업데이트 (안전)

```bash
# catalog 수정 후
pnpm install
pnpm build
pnpm test
```

### 2. Major 업데이트 (주의)

```bash
# 1. 변경사항 확인
# 공식 마이그레이션 가이드 읽기

# 2. 별도 브랜치에서 진행
git checkout -b chore/upgrade-react-19

# 3. catalog 수정
# pnpm-workspace.yaml 편집

# 4. 의존성 설치
pnpm install

# 5. 빌드 테스트
pnpm build

# 6. 타입 에러 수정

# 7. 런타임 테스트
pnpm dev

# 8. PR 생성
```

---

## 버전 범위 규칙

```yaml
# pnpm-workspace.yaml
catalog:
  # ^ (caret) - minor 업데이트 허용 (권장)
  react: ^19.2.0      # 19.2.0 ~ 19.x.x

  # ~ (tilde) - patch만 허용 (안정성 중시)
  cesium: ~1.120.0    # 1.120.0 ~ 1.120.x

  # 정확한 버전 (외부 라이브러리)
  three: 0.170.0      # 정확히 0.170.0
```

---

## 의존성 충돌 해결

### 피어 의존성 충돌

```bash
# 경고 확인
pnpm install

# 강제 해결 (.npmrc)
auto-install-peers=true
resolve-peers-from-workspace-root=true
```

### 버전 불일치

```bash
# 어디서 사용되는지 확인
pnpm why 패키지명

# 특정 버전 강제 (pnpm-workspace.yaml)
pnpm:
  overrides:
    패키지명: ^1.0.0
```

---

## 정기 점검 체크리스트

- [ ] `pnpm outdated` 실행
- [ ] `pnpm audit` 보안 취약점 확인
- [ ] Major 업데이트 마이그레이션 가이드 확인
- [ ] CI/CD에서 빌드 성공 확인
- [ ] 주요 기능 수동 테스트

---

## Context7 참고

패키지 마이그레이션 가이드가 필요하면 Context7로 최신 문서를 조회하세요.
