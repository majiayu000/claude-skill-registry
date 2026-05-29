---
name: workthrough
description: "Use this skill proactively and automatically after completing ANY development work. AI agent summarizes: what was done, what was changed/improved, and suggests future additions/improvements - all concisely in Korean."
license: MIT
---

**AI 에이전트가 개발 작업을 간략하게 요약하고 추가/개선 제안을 작성합니다.**

## ⚡ 핵심

1. **자동 실행**: 개발 완료 시 자동 실행
2. **간략 요약**: AI가 작업 내용 간단히 정리
3. **제안 포함**: 추가/개선할 내용 제안
4. **한국어**: 모든 문서 한국어
5. **위치**: `<project-root>/workthrough/YYYY-MM-DD_HH_MM_description.md`

## 📝 문서 내용 (간결하게!)

```markdown
# [작업 제목]

## 개요
2-3문장으로 무엇을 했는지 요약

## 주요 변경사항
- 개발한 것: XXX 기능 추가
- 수정한 것: YYY 버그 수정
- 개선한 것: ZZZ 성능 향상

## 핵심 코드 (필요시만)
`​``typescript
// 핵심 로직만 간단히
const key = value
`​``

## 결과
- ✅ 빌드 성공
- ✅ 테스트 통과

## 다음 단계
- 다음에 구현해야 할 기능
- 다음에 수정해야 할 부분
```

## 🚀 VitePress 처리

### 첫 실행시 (workthrough 폴더 없을 때)
1. VitePress 초기 설정
2. `pnpm install && pnpm dev` 테스트

### 이후 실행시 (workthrough 폴더 있을 때)
1. 새 워크스루 문서만 생성
2. `pnpm build`로 빌드 확인만

## ⚠️ 중요

- **간결**: 긴 설명 ❌
- **핵심만**: 중요 코드만 발췌
- **요약**: 무엇을 개발/수정/개선했는지
- **다음 단계**: 다음에 해야 할 작업 제안

끝.
