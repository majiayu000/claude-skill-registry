---
name: discord-send-file
description: |
  Claude Gateway Discord 환경에서 파일을 Discord 채널로 첨부 업로드합니다.
  응답에 FILE: /절대경로/파일명 형식으로 파일 경로를 포함하면 게이트웨이가 자동으로 감지하여 Discord로 전송합니다.
argument-hint: "[파일경로]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash
---

# Discord 센드 파일

## 개요

Claude Gateway Discord에서 작업한 파일을 자동으로 Discord 채널에 첨부로 전송합니다.

## 사용 방법

### 기본 형식

응답 본문에 다음 형식으로 파일 경로를 명시합니다:

```
FILE: /절대경로/파일명
```

### 예제

**단일 파일 전송:**
```
스크린샷을 캡처했습니다.

FILE: /home/joungwoolee/discord_homepage.png
```

**여러 파일 전송:**
```
3개의 파일을 생성했습니다.

FILE: /home/joungwoolee/report1.pdf
FILE: /home/joungwoolee/report2.xlsx
FILE: /home/joungwoolee/image.png
```

## 주의사항

- ✅ **절대경로 필수**: `/home/username/filename` 형식으로 작성
- ✅ **파일 존재 확인**: 전송 전 파일이 실제로 존재하는지 확인
- ✅ **한 줄 한 파일**: 여러 파일은 각각 다른 줄에 작성
- ✅ **게이트웨이 자동 감지**: FILE: 패턴을 감지하면 자동 전송

## 기술 사항

게이트웨이는 응답을 줄 단위로 스캔하며 다음 패턴을 찾습니다:
- **정규표현식**: `FILE:\s+(/[^\s]+)`
- **동작**: 첫 번째 캡쳐 그룹(파일 경로)을 Discord 첨부로 전송
- **호환성**: 일반 텍스트와 혼합되어도 정상 작동

---

**환경**: `claude-gateway-discord` 전용
