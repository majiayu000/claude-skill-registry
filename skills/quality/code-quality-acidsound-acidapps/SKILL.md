---
name: code-quality
description: Code quality inspection and linting commands for web audio apps. Includes detection of dead code, magic numbers, type safety issues, and naming inconsistencies.
---

# 🔍 Code Quality Skill

코드 품질 검사를 위한 명령어 및 체크리스트.

## 🎯 용도

- 사용되지 않는 코드 탐지
- 타입 안전성 확인
- 코딩 컨벤션 검증
- 리팩토링 우선순위 결정

## 📋 빠른 검사 명령어

### 1. 타입 안전성

```bash
# any 타입 사용 확인
grep -rn ": any" --include="*.ts" --include="*.tsx" src/

# 타입 에러 체크 (TypeScript)
npx tsc --noEmit
```

### 2. 사용되지 않는 코드

```bash
# TODO/FIXME 주석 찾기
grep -rn "TODO\|FIXME\|XXX" --include="*.ts" --include="*.tsx" src/

# 사용되지 않는 exports (설치 필요)
npx ts-unused-exports tsconfig.json --silent
```

### 3. 코딩 컨벤션

```bash
# 하드코딩된 색상 (Tailwind 프로젝트)
grep -rn "bg-\[#" --include="*.tsx" src/
grep -rn "text-\[#" --include="*.tsx" src/
grep -rn "border-\[#" --include="*.tsx" src/

# 매직 넘버 (2자리 이상)
grep -rn "[^0-9a-zA-Z][0-9]\{2,\}[^0-9]" --include="*.ts" --include="*.tsx" src/ | grep -v "//"

# 짧은 변수명 (1-2글자)
grep -rn "\b[a-z]\{1,2\}\b\s*=" --include="*.ts" --include="*.tsx" src/
```

### 4. 중복 코드

```bash
# Copy-Paste Detector (설치 필요)
npx jscpd --min-lines 5 --min-tokens 50 src/
```

## 📊 품질 지표

### 파일 크기 분석

```bash
# 큰 파일 순으로 정렬
find src -name "*.tsx" -o -name "*.ts" | xargs wc -l | sort -rn | head -20
```

### 권장 기준

| 지표 | 양호 | 주의 | 위험 |
|-----|-----|-----|-----|
| 파일 라인 수 | < 200 | 200-500 | > 500 |
| 함수 파라미터 | < 3 | 3-5 | > 5 |
| useEffect 개수 | < 3 | 3-5 | > 5 |
| 중첩 깊이 | < 3 | 3-4 | > 4 |

## 🛠️ 자동화 스크립트

### quick-check.sh

```bash
#!/bin/bash
# 빠른 코드 품질 체크

echo "=== Code Quality Check ==="

echo -e "\n📌 TODO/FIXME count:"
grep -rn "TODO\|FIXME" --include="*.ts" --include="*.tsx" src/ | wc -l

echo -e "\n📌 any type usage:"
grep -rn ": any" --include="*.ts" --include="*.tsx" src/ | wc -l

echo -e "\n📌 Hardcoded colors:"
grep -rn "bg-\[#\|text-\[#" --include="*.tsx" src/ | wc -l

echo -e "\n📌 Large files (>300 lines):"
find src -name "*.tsx" -o -name "*.ts" | xargs wc -l | sort -rn | awk '$1 > 300 {print}'

echo -e "\n📌 Type check:"
npx tsc --noEmit 2>&1 | tail -5

echo -e "\n=== Done ==="
```

## 📝 리팩토링 우선순위 계산

### 점수 공식

```
우선순위 = (영향도 × 5) + (빈도 × 3) + (난이도 × -2)
```

### 영향도 (1-5)
1. 코드 스타일만 영향
2. 특정 파일만 영향
3. 모듈 전체 영향
4. 여러 모듈 영향
5. 시스템 전체 영향

### 빈도 (1-5)
1. 1번만 발생
2. 2-3곳
3. 4-10곳
4. 10-50곳
5. 50곳 이상

### 난이도 (1-5)
1. 5분 이내
2. 30분 이내
3. 2시간 이내
4. 1일 이내
5. 1일 이상

## 🔗 관련 도구

### 권장 설치

```bash
# ESLint + TypeScript
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# 중복 코드 탐지
npm install -g jscpd

# 사용되지 않는 exports
npm install -g ts-unused-exports

# 복잡도 분석
npm install -g es6-plato
```

### VS Code 확장

- **SonarLint**: 실시간 코드 품질 체크
- **Code Metrics**: 복잡도 표시
- **TODO Highlight**: TODO/FIXME 강조
- **Better Comments**: 주석 분류
