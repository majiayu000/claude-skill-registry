---
name: jwc-biome-ultracite-fixing
description: 'Biome/Ultracite 린트 경고(예: useSortedClasses)와 포맷 문제를 의미 변경 없이(safe fix)
  해결하고, 패키지 단위로 빠르게 재검증합니다.'
---

---
name: jwc-biome-ultracite-fixing
description: Biome/Ultracite 린트 경고(예: useSortedClasses)와 포맷 문제를 의미 변경 없이(safe fix) 해결하고, 패키지 단위로 빠르게 재검증합니다.
---

# Biome / Ultracite Fixing

## 언제 사용하나요?

- `biome lint --error-on-warnings`가 경고로 실패할 때
- Tailwind class 정렬(`useSortedClasses`) 경고를 안전하게 해결해야 할 때
- import 정리/포맷을 레포 규칙에 맞춰야 할 때

## 기본 원칙

- **의미 변경 없는 safe fix 우선**
- 변경 범위를 최소화: 먼저 “수정한 패키지/폴더”만 대상으로 실행
- 자동 수정 후에는 반드시 해당 패키지의 `lint`/`typecheck` 재실행

## 권장 절차(패키지 단위)

1) 실패한 패키지로 이동(예: UI):
- `pnpm -C packages/ui lint`

2) 자동 수정(필요할 때만)

- Biome 자체 safe fix 적용:
  - `pnpm -C packages/ui exec biome lint --write ./src`

3) 재검증:
- `pnpm -C packages/ui lint`
- `pnpm -C packages/ui typecheck`

## 워크스페이스 단위(마지막)

- 루트 Ultracite 체크(전체 규칙 확인):
  - `pnpm check:ultracite`

- 자동수정이 필요하면(리뷰 필수):
  - `pnpm fix:ultracite`

주의: 루트 `pnpm -w lint`는 터보 의존성 때문에 `^build`를 동반할 수 있습니다. 단순 lint 경고 수정 목적이면 패키지 단위로 먼저 해결하세요.

## 자주 나오는 케이스

### Tailwind class 정렬(useSortedClasses)

- 증상: className 문자열 순서가 규칙과 달라 경고 발생
- 해결: `biome lint --write`로 정렬만 적용하고 기능 변경이 없음을 확인

## 참고

- 레포 공통 규칙: [AGENTS.md](AGENTS.md)
- UI 패키지 규칙: [packages/ui/AGENTS.md](packages/ui/AGENTS.md)
