---
name: streaming-expert
description: 영상 스트리밍 전문가. "CCTV", "HLS", "WHEP", "스트리밍", "영상" 관련 질문 시 사용.
allowed-tools: Read, Write, Glob, Grep
---

# 영상 스트리밍 전문가

$ARGUMENTS 영상 스트리밍 관련 질문에 답변하고 구현을 도와드립니다.

---

## @pf-dev/cctv 패키지 구조

```
packages/cctv/src/
├── components/
│   └── CCTVPlayer.tsx       # Headless 플레이어
├── hooks/
│   ├── useHLSStream.ts      # HLS 스트리밍
│   └── useWHEPStream.ts     # WHEP 스트리밍
├── stores/
│   ├── useHLSStore.ts       # HLS 상태
│   └── useWHEPStore.ts      # WHEP 상태
└── types/
    └── index.ts
```

---

## 프로토콜 비교

| 프로토콜 | 지연시간 | 장점 | 단점 |
|----------|----------|------|------|
| **HLS** | 1-3초 | 안정적, 널리 지원 | 지연 있음 |
| **WHEP** | ~1초 | 초저지연 (WebRTC) | 서버 구성 복잡 |

---

## HLS 스트리밍

### 기본 사용

```tsx
import { useHLSStream } from "@pf-dev/cctv";

function CCTVView({ streamUrl }: { streamUrl: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);

  const { isPlaying, error, play, pause, destroy } = useHLSStream({
    url: streamUrl,
    videoRef,
    autoPlay: true,
    onError: (err) => console.error("HLS Error:", err),
  });

  return (
    <div>
      <video ref={videoRef} muted playsInline />
      {error && <p className="text-red-500">{error.message}</p>}
      <button onClick={isPlaying ? pause : play}>
        {isPlaying ? "일시정지" : "재생"}
      </button>
    </div>
  );
}
```

### LL-HLS (Low-Latency HLS)

```tsx
const { ... } = useHLSStream({
  url: streamUrl,
  videoRef,
  hlsConfig: {
    lowLatencyMode: true,
    liveSyncDurationCount: 3,
    liveMaxLatencyDurationCount: 10,
  },
});
```

---

## WHEP 스트리밍 (WebRTC)

### 기본 사용

```tsx
import { useWHEPStream } from "@pf-dev/cctv";

function LowLatencyCCTV({ whepUrl }: { whepUrl: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);

  const { isConnected, error, connect, disconnect } = useWHEPStream({
    url: whepUrl,
    videoRef,
    autoConnect: true,
    onConnectionChange: (connected) => {
      console.log("Connection:", connected);
    },
  });

  return (
    <div>
      <video ref={videoRef} muted playsInline />
      {!isConnected && <p>연결 중...</p>}
      {error && <p className="text-red-500">{error.message}</p>}
    </div>
  );
}
```

### 자동 재연결

```tsx
const { ... } = useWHEPStream({
  url: whepUrl,
  videoRef,
  reconnect: true,
  reconnectInterval: 3000,  // 3초 후 재시도
  maxReconnectAttempts: 5,
});
```

---

## CCTVPlayer (Headless)

```tsx
import { CCTVPlayer } from "@pf-dev/cctv";

function CustomPlayer({ url, protocol }) {
  return (
    <CCTVPlayer
      url={url}
      protocol={protocol} // "hls" | "whep"
      autoPlay
      muted
      className="w-full h-full object-cover"
      onReady={() => console.log("Ready")}
      onError={(err) => console.error(err)}
      onLatencyChange={(latency) => console.log(`Latency: ${latency}ms`)}
    />
  );
}
```

---

## 자주 묻는 질문

### Q: 영상이 안 나와요

**A: 체크리스트**
1. URL 확인 (CORS, 인증)
2. 네트워크 탭에서 m3u8/segment 요청 확인
3. 브라우저 콘솔 에러 확인
4. HTTPS 여부 확인 (WHEP는 HTTPS 필수)

```tsx
// 디버깅용 로깅
useHLSStream({
  url,
  videoRef,
  hlsConfig: {
    debug: true,  // HLS.js 디버그 로그
  },
});
```

### Q: 지연이 너무 커요

**A: HLS 최적화**
```tsx
hlsConfig: {
  lowLatencyMode: true,
  liveSyncDurationCount: 2,     // 동기화할 세그먼트 수 감소
  liveMaxLatencyDurationCount: 5,
  maxBufferLength: 10,          // 버퍼 크기 감소
}
```

**A: WHEP로 전환**
```tsx
// WHEP는 ~1초 지연
<CCTVPlayer protocol="whep" url={whepUrl} />
```

### Q: 끊김이 심해요

**A: 버퍼 설정**
```tsx
hlsConfig: {
  maxBufferLength: 30,           // 버퍼 증가
  maxMaxBufferLength: 60,
  maxBufferHole: 0.5,
}
```

### Q: 여러 CCTV를 동시에 보고 싶어요

**A: 그리드 레이아웃**
```tsx
function CCTVGrid({ streams }: { streams: StreamInfo[] }) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {streams.map(stream => (
        <CCTVPlayer
          key={stream.id}
          url={stream.url}
          protocol={stream.protocol}
          muted  // 여러 개일 때 음소거 필수
        />
      ))}
    </div>
  );
}
```

**주의:** 동시 스트림 수는 4-6개 이하 권장 (브라우저 성능)

---

## 환경변수

```env
VITE_MEDIA_API_URL=https://media.example.com
VITE_MEDIA_WHEP_URL=https://media.example.com/whep
```

---

## 서버 요구사항

### HLS
- Nginx + nginx-rtmp-module
- 또는 FFmpeg + HLS 출력

### WHEP
- MediaMTX (권장)
- 또는 Janus Gateway
- 또는 Pion WebRTC

---

## 성능 모니터링

```tsx
const { stats } = useHLSStream({ ... });

// stats 내용
{
  currentTime: 123.45,
  bufferedDuration: 10.2,
  latency: 2.5,         // 실시간과의 지연 (초)
  bandwidth: 5000000,   // bps
  droppedFrames: 0,
}
```
