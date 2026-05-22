---
name: dependency-security
description: Enforce dependency security scanning and SBOM generation. Use when adding dependencies, reviewing package.json, or during security audits. Covers OWASP dependency check, npm audit, and supply chain security.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Dependency Security

의존성 보안 스캔 및 SBOM(Software Bill of Materials) 생성을 강제하는 스킬입니다.

## 2025 Context

> **OWASP Top 10 2025에서 "Vulnerable and Outdated Components"가 A03으로 상승**
> **EU Cyber Resilience Act: 2024년부터 SBOM 의무화 시작**
> **Supply Chain 공격 급증: 2024년 대비 300% 증가**

## Core Rules

| 규칙 | 상태 | 설명 |
|------|------|------|
| npm audit 통과 | 🔴 필수 | high/critical 취약점 0개 |
| 의존성 최신화 | 🟡 권장 | 주요 보안 패치 적용 |
| SBOM 생성 | 🟡 권장 | 의존성 목록 문서화 |
| lockfile 커밋 | 🔴 필수 | 재현 가능한 빌드 |

## Security Audit

### npm audit

```bash
# 취약점 검사
npm audit

# 자동 수정 (가능한 경우)
npm audit fix

# 강제 수정 (major 버전 업데이트 포함)
npm audit fix --force  # ⚠️ 주의: 호환성 문제 가능

# JSON 출력 (CI용)
npm audit --json
```

### 결과 해석

```
Severity levels:
- critical: 🔴 즉시 수정 필수
- high:     🔴 즉시 수정 필수
- moderate: 🟡 조속히 수정
- low:      🟢 다음 업데이트 시 수정
```

### CI 통합 예시

```yaml
# GitHub Actions
- name: Security Audit
  run: |
    npm audit --audit-level=high
    if [ $? -ne 0 ]; then
      echo "Security vulnerabilities found!"
      exit 1
    fi
```

## Dependency Management

### 의존성 업데이트 확인

```bash
# 오래된 패키지 확인
npm outdated

# 업데이트 가능한 패키지
npx npm-check-updates

# 대화형 업데이트
npx npm-check-updates -i
```

### 안전한 업데이트 전략

```bash
# 1. 현재 상태 기록
npm outdated > outdated-$(date +%Y%m%d).txt

# 2. patch 버전만 업데이트 (가장 안전)
npx npm-check-updates -u --target patch

# 3. minor 버전 업데이트
npx npm-check-updates -u --target minor

# 4. 테스트 실행
npm test

# 5. lockfile 커밋
git add package-lock.json
git commit -m "chore: update dependencies (security patch)"
```

## SBOM (Software Bill of Materials)

### SBOM 생성

```bash
# CycloneDX 형식 (권장)
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# SPDX 형식
npx spdx-sbom-generator
```

### SBOM 포함 정보

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "name": "react",
      "version": "18.2.0",
      "purl": "pkg:npm/react@18.2.0",
      "licenses": [{ "license": { "id": "MIT" } }]
    }
  ]
}
```

### CI에서 SBOM 자동 생성

```yaml
# GitHub Actions
- name: Generate SBOM
  run: npx @cyclonedx/cyclonedx-npm --output-file sbom.json

- name: Upload SBOM
  uses: actions/upload-artifact@v3
  with:
    name: sbom
    path: sbom.json
```

## Supply Chain Security

### Lockfile 보안

```bash
# package-lock.json 항상 커밋
git add package-lock.json

# CI에서 정확한 버전 설치
npm ci  # (npm install이 아님!)
```

### .npmrc 보안 설정

```ini
# .npmrc
# 스크립트 자동 실행 금지
ignore-scripts=true

# 엄격한 SSL
strict-ssl=true

# 레지스트리 고정
registry=https://registry.npmjs.org/
```

### 의심스러운 패키지 확인

```bash
# 패키지 정보 확인
npm info <package-name>

# 다운로드 수, 유지보수 상태 확인
npx npm-check <package-name>

# 라이선스 확인
npx license-checker
```

## Detection Patterns

### 위험 신호

```
🔴 위험:
- critical/high 취약점 존재
- 1년 이상 업데이트 없는 의존성
- deprecated 패키지 사용
- 알 수 없는 출처의 패키지

🟡 주의:
- moderate 취약점
- 6개월 이상 업데이트 없음
- 낮은 다운로드 수
```

### 검사 명령어

```bash
# deprecated 패키지 확인
npm ls 2>&1 | grep -i deprecated

# 라이선스 문제 확인
npx license-checker --failOn "GPL;AGPL"

# 의존성 트리 확인
npm ls --depth=0
```

## Workflow

### 1. 새 의존성 추가 시

```
추가 전 체크:
1. npm info로 패키지 정보 확인
2. 다운로드 수 및 유지보수 상태 확인
3. 라이선스 호환성 확인
4. 대안 패키지 검토

추가 후:
1. npm audit 실행
2. lockfile 커밋
```

### 2. 정기 보안 점검 (주간/월간)

```bash
# 1. 취약점 검사
npm audit

# 2. 오래된 패키지 확인
npm outdated

# 3. SBOM 업데이트
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# 4. 결과 기록
```

### 3. CI/CD 파이프라인

```yaml
name: Security Check

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Security audit
        run: npm audit --audit-level=high

      - name: Check outdated
        run: npm outdated || true

      - name: Generate SBOM
        run: npx @cyclonedx/cyclonedx-npm --output-file sbom.json
```

## 도구 추천

| 도구 | 용도 | 명령어 |
|------|------|--------|
| npm audit | 취약점 스캔 | `npm audit` |
| Snyk | 고급 취약점 분석 | `npx snyk test` |
| OWASP Dependency-Check | OWASP 표준 스캔 | CLI 도구 |
| CycloneDX | SBOM 생성 | `npx @cyclonedx/cyclonedx-npm` |
| npm-check-updates | 의존성 업데이트 | `npx ncu` |

## Checklist

### 새 프로젝트

- [ ] .npmrc 보안 설정 적용
- [ ] package-lock.json 커밋
- [ ] npm audit 통과 확인
- [ ] CI에 보안 검사 추가

### 의존성 추가 시

- [ ] 패키지 신뢰성 확인
- [ ] 라이선스 호환성 확인
- [ ] npm audit 재실행
- [ ] lockfile 커밋

### 정기 점검

- [ ] npm audit 실행
- [ ] npm outdated 확인
- [ ] SBOM 업데이트
- [ ] 보안 패치 적용

## References

- [OWASP Top 10 2025](https://owasp.org/Top10/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [CycloneDX](https://cyclonedx.org/)
- [npm audit documentation](https://docs.npmjs.com/cli/v10/commands/npm-audit)
