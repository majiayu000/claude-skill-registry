---
name: developer
description: 기능 개발 스킬. 타입 정의, Storage API, 비즈니스 로직. 코드 작성 시 사용.
---

# Developer Skill

## 기술 스택

React + TypeScript + Vite + Tailwind CSS + Chrome Storage API + Vitest

## 코드 철학 (Kent Beck Style)

### OOP + FP 하이브리드
```
구조 = 인터페이스/타입 (TypeScript)
로직 = 순수 함수 (FP)
```

| 원칙 | 적용 |
|------|------|
| **SRP** | 하나의 함수 = 하나의 책임 |
| **순수 함수** | 입력 → 출력만, 사이드 이펙트는 경계에서 |
| **불변성** | 객체 수정 대신 새 객체 반환 |
| **명확한 의도** | 이름이 곧 문서, 주석 최소화 |

### YAGNI + KISS + 미래지향
- **YAGNI**: 지금 필요없는 기능은 만들지 않음
- **KISS**: 가장 단순한 해결책 선택
- **미래지향**: 확장 포인트(인터페이스)는 미리 설계
- **성능**: 측정 가능한 병목은 즉시 최적화

## Storage 패턴

Chrome Storage API 직접 호출 금지. 반드시 Storage 유틸리티 통해 접근:

```
src/
├── shared/
│   ├── types/           # 타입 정의
│   │   ├── link.types.ts
│   │   └── settings.types.ts
│   ├── storage/         # Storage 래퍼
│   │   ├── link.storage.ts
│   │   └── settings.storage.ts
│   └── utils/           # 유틸리티 함수
│       ├── search.ts
│       └── export.ts
```

### Storage 유틸리티 패턴

```typescript
// link.storage.ts
import type { Link } from '../types/link.types';

const STORAGE_KEY = 'linkhub_links';

export async function getLinks(): Promise<Link[]> {
  const result = await chrome.storage.local.get(STORAGE_KEY);
  return result[STORAGE_KEY] || [];
}

export async function saveLink(link: Link): Promise<void> {
  const links = await getLinks();
  const updated = [...links, link];
  await chrome.storage.local.set({ [STORAGE_KEY]: updated });
}

export async function deleteLink(id: string): Promise<void> {
  const links = await getLinks();
  const filtered = links.filter(l => l.id !== id);
  await chrome.storage.local.set({ [STORAGE_KEY]: filtered });
}
```

## 태스크 프로세스

1. **분석**: 영향받는 파일 식별, 기존 패턴 파악
2. **구현**: 코드 읽고 확인 후 수정, 추측 금지
3. **테스트**: 필요한 테스트만 작성
4. **검토**: YAGNI/KISS 위반 확인
5. **커밋**: Conventional Commits, Claude 마킹 금지

## 타입 정의 규칙

```typescript
// 엔터티 타입
export interface Link {
  id: string;
  url: string;
  title: string;
  favicon?: string;
  tags: string[];
  memo?: string;
  isReadLater: boolean;
  createdAt: number;
  updatedAt: number;
}

// 입력 타입 (생성/수정용)
export type CreateLinkInput = Omit<Link, 'id' | 'createdAt' | 'updatedAt'>;
export type UpdateLinkInput = Partial<CreateLinkInput>;
```

## 체크리스트

- [ ] 타입 정의 완료
- [ ] Storage 유틸리티 사용 (직접 호출 X)
- [ ] 순수 함수로 로직 구현
- [ ] 에러 처리 적절
- [ ] YAGNI/KISS 준수

> 상세 구현은 기존 코드베이스 분석
