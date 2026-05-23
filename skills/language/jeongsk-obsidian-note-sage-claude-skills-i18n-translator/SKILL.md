---
name: i18n-translator
description: "Manage i18n translations for Note Sage plugin. Use when: (1) Adding new translation keys, (2) Updating existing translations, (3) Maintaining consistency across 11 languages (en, ko, ja, es, fr, de, pt, zh, ar, ru, hi), (4) Finding missing translations"
allowed-tools: Read, Edit, Glob, Grep, Bash
---

# i18n Translator Skill

Note Sage Obsidian 플러그인의 다국어(i18n) 번역 관리 전담 스킬입니다.

## 지원 언어 (11개)

| 코드 | 언어 | 방향 | 파일 |
|------|------|------|------|
| `en` | English | LTR | 기준 언어, 타입 정의 포함 |
| `ko` | 한국어 | LTR | |
| `ja` | 日本語 | LTR | |
| `es` | Español | LTR | |
| `fr` | Français | LTR | |
| `de` | Deutsch | LTR | |
| `pt` | Português | LTR | |
| `zh` | 简体中文 | LTR | |
| `ar` | العربية | RTL | 오른쪽에서 왼쪽 |
| `ru` | Русский | LTR | |
| `hi` | हिन्दी | LTR | |

## 파일 구조

```
src/i18n/
├── index.ts                 # i18n 핵심 모듈 (t() 함수, setLanguage() 등)
└── locales/
    ├── en.ts               # 영어 (기준) - TranslationKeys 인터페이스 정의
    ├── ko.ts               # 한국어
    ├── ja.ts               # 일본어
    ├── es.ts               # 스페인어
    ├── fr.ts               # 프랑스어
    ├── de.ts               # 독일어
    ├── pt.ts               # 포르투갈어
    ├── zh.ts               # 중국어 (간체)
    ├── ar.ts               # 아랍어
    ├── ru.ts               # 러시아어
    └── hi.ts               # 힌디어
```

## 번역 키 구조

영어 파일(`en.ts`)에 정의된 `TranslationKeys` 인터페이스를 기준으로 합니다:

```typescript
export interface TranslationKeys {
  appTitle: string;
  quickAction: QuickActionTranslations;    // 빠른 액션 버튼
  commands: CommandsTranslations;           // 명령어 팔레트
  prompts: PromptsTranslations;             // 빠른 프롬프트
  settings: SettingsTranslations;           // 설정 탭
  // ... 기타 키
}
```

**주요 섹션:**
- `quickAction` - 채팅 입력창 위 빠른 액션 버튼
- `commands` - Obsidian 명령어 팔레트
- `prompts` - AI 프롬프트 템플릿
- `settings` - 플러그인 설정
  - `settings.builtinTools` - 내장 도구
  - `settings.agentOptions` - Agent SDK 옵션
  - `settings.mcp` - MCP 서버 설정

## 워크플로우

### 1. 새 번역 키 추가

**단계 1: 영어 파일에 인터페이스 및 값 추가**

```typescript
// src/i18n/locales/en.ts

// 1. 인터페이스에 새 키 추가 (중첩된 경우)
interface NewFeatureTranslations {
  title: string;
  description: string;
}

// 2. TranslationKeys 또는 SettingsTranslations에 추가
interface SettingsTranslations {
  // ... 기존 키
  newFeature: NewFeatureTranslations;  // 새로 추가
}

// 3. 영어 값 추가
export const en: TranslationKeys = {
  settings: {
    // ... 기존 값
    newFeature: {
      title: 'New Feature',
      description: 'Description of the new feature',
    },
  },
};
```

**단계 2: 다른 언어 파일에 동일한 구조로 번역 추가**

```typescript
// src/i18n/locales/ko.ts
export const ko: TranslationKeys = {
  settings: {
    // ... 기존 값
    newFeature: {
      title: '새 기능',
      description: '새 기능에 대한 설명',
    },
  },
};
```

**중요:** 모든 11개 언어 파일에 동일한 구조로 추가해야 합니다!

### 2. 기존 번역 수정

1. 먼저 영어 파일에서 해당 키 확인
2. 필요한 언어 파일을 열어 값 수정
3. 다른 언어와 일관성 유지 확인

### 3. 누락된 번역 탐지

```bash
# 검증 스크립트 실행
python .claude/skills/i18n-translator/scripts/validate_translations.py
```

## 코드에서 번역 사용

```typescript
import { t, setLanguage, getLanguage } from './i18n';

// 번역 텍스트 가져오기
const title = t('appTitle');                    // 단순 키
const apiKey = t('settings.apiKey');            // 중첩 키
const webSearch = t('settings.builtinTools.webSearch');  // 깊은 중첩

// 언어 변경
setLanguage('ko');

// 현재 언어 확인
const currentLang = getLanguage();  // 'ko'
```

## 체크리스트

새 번역 작업 시:

- [ ] 영어(`en.ts`)에 키와 인터페이스 추가 (기준)
- [ ] 한국어(`ko.ts`)에 번역 추가
- [ ] 일본어(`ja.ts`)에 번역 추가
- [ ] 스페인어(`es.ts`)에 번역 추가
- [ ] 프랑스어(`fr.ts`)에 번역 추가
- [ ] 독일어(`de.ts`)에 번역 추가
- [ ] 포르투갈어(`pt.ts`)에 번역 추가
- [ ] 중국어(`zh.ts`)에 번역 추가
- [ ] 아랍어(`ar.ts`)에 번역 추가
- [ ] 러시아어(`ru.ts`)에 번역 추가
- [ ] 힌디어(`hi.ts`)에 번역 추가
- [ ] 검증 스크립트로 누락 확인

## 주의사항

1. **영어가 기준**: 항상 영어 파일을 먼저 수정하고 다른 언어에 적용
2. **타입 안전성**: 인터페이스 수정 시 TypeScript 컴파일 오류 확인
3. **RTL 지원**: 아랍어는 오른쪽에서 왼쪽 텍스트 방향
4. **중첩 구조**: 점(`.`) 표기법으로 깊은 키 접근 가능
5. **Fallback**: 키를 찾지 못하면 키 경로 자체가 반환됨

## 참조 문서

- [번역 구조 상세](references/TRANSLATION_STRUCTURE.md)
