---
name: omt-setup
description: "oh-my-til 통합 설정 — 배포 설정"
plugin-version: "__PLUGIN_VERSION__"
---

# OMT Setup Skill

oh-my-til 설정을 한 곳에서 관리. 서브커맨드로 동작.

## 서브커맨드

### `/omt-setup` (인수 없음)

`oh-my-til.json` 읽어서 현재 설정 표시 + 서브커맨드 안내:
- `deploy` — GitHub Pages 배포 설정

### `/omt-setup deploy`

GitHub Pages 배포 설정:
1. `.git/` 확인 (없으면 안내 후 종료)
2. `.github/workflows/deploy-til.yml` 확인 (있으면 수정 필요 여부 질문)
3. `oh-my-til.json` deploy 섹션 설정 (제목, 부제목, GitHub URL)
4. 워크플로우 YAML 생성
5. 완료 안내 (Settings → Pages → GitHub Actions 선택, 커밋·push 명령어)

## 규칙

- 한국어 출력
- `oh-my-til.json`의 기존 설정 보존, 해당 섹션만 추가/수정
- 커밋은 하지 않음 (사용자에게 명령어 안내만)
