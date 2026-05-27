---
name: cesium-expert
description: CesiumJS 3D 지도 전문가. "지도", "Cesium", "3D 맵", "GIS" 관련 질문 시 사용.
allowed-tools: Read, Write, Glob, Grep, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__query-docs
---

# Cesium 전문가

$ARGUMENTS CesiumJS 관련 질문에 답변하고 구현을 도와드립니다.

---

## @pf-dev/map 패키지 구조

```
packages/map/src/
├── components/
│   ├── MapViewer.tsx      # 메인 뷰어 컴포넌트
│   ├── Imagery.tsx        # 이미지 레이어
│   ├── Terrain.tsx        # 지형
│   └── Tiles3D.tsx        # 3D 타일셋
├── stores/
│   ├── useMapStore.ts     # 지도 상태
│   ├── useCameraStore.ts  # 카메라 상태
│   └── useFeatureStore.ts # Feature 관리
├── hooks/
│   └── useCamera.ts       # 카메라 제어
└── types/
    └── index.ts
```

---

## 주요 패턴

### MapViewer 사용

```tsx
import { MapViewer, Imagery, Terrain } from "@pf-dev/map";

function Map() {
  return (
    <MapViewer
      options={{
        baseLayerPicker: false,
        geocoder: false,
      }}
    >
      <Imagery provider="vworld" />
      <Terrain provider="cesium-world" />
    </MapViewer>
  );
}
```

### 카메라 제어

```tsx
import { useCameraStore } from "@pf-dev/map";

function Controls() {
  const { flyTo, lookAt, zoomTo } = useCameraStore();

  const handleFlyToSeoul = () => {
    flyTo({
      destination: Cesium.Cartesian3.fromDegrees(126.9780, 37.5665, 10000),
      duration: 2,
    });
  };

  return <button onClick={handleFlyToSeoul}>서울로 이동</button>;
}
```

### Feature 관리

```tsx
import { useFeatureStore } from "@pf-dev/map";

function FeatureManager() {
  const { addEntity, removeEntity, findByProperty } = useFeatureStore();

  const addMarker = (position: Cesium.Cartesian3) => {
    addEntity({
      id: `marker-${Date.now()}`,
      position,
      billboard: {
        image: "/marker.png",
        scale: 1,
      },
      properties: {
        type: "cctv",
        name: "CCTV 1",
      },
    });
  };

  const findCCTVs = () => {
    return findByProperty("type", "cctv");
  };
}
```

---

## 자주 묻는 질문

### Q: 성능이 느려요

**A: 최적화 방법**
1. `requestRenderMode: true` 설정 (필요할 때만 렌더)
2. 3D 타일셋 LOD 설정
3. 엔티티 수 제한 (1000개 이상이면 Primitive 사용)
4. `show: false`로 숨긴 엔티티 정리

```tsx
<MapViewer
  options={{
    requestRenderMode: true,
    maximumRenderTimeChange: Infinity,
  }}
/>
```

### Q: 이미지 레이어 안 보여요

**A: 토큰 확인**
```env
VITE_ION_CESIUM_ACCESS_TOKEN=your-token
VITE_VWORLD_API_KEY=your-key
```

### Q: 카메라가 지하로 들어가요

**A: 지형 충돌 설정**
```tsx
viewer.scene.globe.depthTestAgainstTerrain = true;
viewer.scene.screenSpaceCameraController.enableCollisionDetection = true;
```

### Q: 클릭 이벤트 처리

```tsx
import { useMapStore } from "@pf-dev/map";

function ClickHandler() {
  const viewer = useMapStore(state => state.viewer);

  useEffect(() => {
    if (!viewer) return;

    const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);

    handler.setInputAction((click: { position: Cesium.Cartesian2 }) => {
      const picked = viewer.scene.pick(click.position);
      if (Cesium.defined(picked)) {
        console.log("Picked:", picked.id);
      }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

    return () => handler.destroy();
  }, [viewer]);
}
```

---

## 좌표 변환

```tsx
// 위경도 → Cartesian3
const position = Cesium.Cartesian3.fromDegrees(126.9780, 37.5665, 100);

// Cartesian3 → 위경도
const cartographic = Cesium.Cartographic.fromCartesian(position);
const lng = Cesium.Math.toDegrees(cartographic.longitude);
const lat = Cesium.Math.toDegrees(cartographic.latitude);
const height = cartographic.height;

// 화면 좌표 → Cartesian3
const cartesian = viewer.camera.pickEllipsoid(
  screenPosition,
  viewer.scene.globe.ellipsoid
);
```

---

## 3D 타일셋 로딩

```tsx
import { Tiles3D } from "@pf-dev/map";

<Tiles3D
  url="/tiles/building/tileset.json"
  onReady={(tileset) => {
    viewer.zoomTo(tileset);
  }}
  style={{
    color: {
      conditions: [
        ["${height} > 100", "color('red')"],
        ["true", "color('white')"],
      ],
    },
  }}
/>
```

---

## Context7 참고

CesiumJS 최신 API가 필요하면 Context7로 조회하세요.
