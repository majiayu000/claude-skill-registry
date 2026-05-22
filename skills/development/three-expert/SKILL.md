---
name: three-expert
description: Three.js/React Three Fiber 전문가. "3D", "Three.js", "R3F", "모델" 관련 질문 시 사용.
allowed-tools: Read, Write, Glob, Grep, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__query-docs
---

# Three.js/R3F 전문가

$ARGUMENTS Three.js 관련 질문에 답변하고 구현을 도와드립니다.

---

## @pf-dev/three 패키지 구조

```
packages/three/src/
├── components/
│   ├── Canvas.tsx           # R3F Canvas 래퍼
│   ├── SceneLighting.tsx    # 조명 설정
│   ├── SceneGrid.tsx        # 그리드 헬퍼
│   ├── Stats.tsx            # 성능 통계
│   ├── GLTFModel.tsx        # GLTF 로더
│   └── FBXModel.tsx         # FBX 로더
├── stores/
│   ├── useFacilityStore.ts  # 시설물 상태
│   ├── useAssetStore.ts     # 에셋 상태
│   └── useFeatureStore.ts   # Feature 상태
├── hooks/
│   ├── useModel.ts          # 모델 로딩
│   └── useInteraction.ts    # 인터랙션
└── utils/
    └── instancing.ts        # GPU Instancing
```

---

## 주요 패턴

### 기본 씬 설정

```tsx
import { Canvas, SceneLighting, SceneGrid, Stats } from "@pf-dev/three";

function Scene() {
  return (
    <Canvas
      camera={{ position: [10, 10, 10], fov: 50 }}
      shadows
    >
      <SceneLighting />
      <SceneGrid size={100} />
      <Stats />

      {/* 3D 오브젝트들 */}
      <MyModel />
    </Canvas>
  );
}
```

### GLTF 모델 로딩

```tsx
import { GLTFModel } from "@pf-dev/three";

function Building() {
  return (
    <GLTFModel
      url="/models/building.glb"
      position={[0, 0, 0]}
      scale={1}
      onLoad={(gltf) => {
        console.log("Model loaded:", gltf);
      }}
      onClick={(event) => {
        console.log("Clicked:", event.object.name);
      }}
    />
  );
}
```

### 인터랙션 (Hover, Select)

```tsx
import { useInteraction } from "@pf-dev/three";

function InteractiveModel({ url }) {
  const { hovered, selected, bind } = useInteraction();

  return (
    <GLTFModel
      url={url}
      {...bind()}
      onPointerOver={() => console.log("hover")}
      onPointerOut={() => console.log("out")}
      onClick={() => console.log("click")}
    >
      {hovered && <Outline color="yellow" />}
      {selected && <Outline color="blue" />}
    </GLTFModel>
  );
}
```

---

## GPU Instancing (대량 오브젝트)

```tsx
import { useMemo } from "react";
import { InstancedMesh } from "three";

function Trees({ positions }: { positions: [number, number, number][] }) {
  const mesh = useMemo(() => {
    const temp = new THREE.Object3D();
    return positions.map((pos, i) => {
      temp.position.set(...pos);
      temp.updateMatrix();
      return temp.matrix.clone();
    });
  }, [positions]);

  return (
    <instancedMesh args={[undefined, undefined, positions.length]}>
      <cylinderGeometry args={[0.5, 0.5, 3]} />
      <meshStandardMaterial color="brown" />
      {mesh.map((matrix, i) => (
        <primitive key={i} object={matrix} attach={`instanceMatrix-${i}`} />
      ))}
    </instancedMesh>
  );
}

// 또는 @pf-dev/three의 유틸리티 사용
import { createInstances } from "@pf-dev/three";

const instances = createInstances(geometry, material, transforms);
```

---

## 자주 묻는 질문

### Q: 성능이 느려요

**A: 최적화 방법**
1. GPU Instancing 사용 (동일 오브젝트 100개 이상)
2. LOD (Level of Detail) 설정
3. Frustum Culling 확인
4. 텍스처 압축 (KTX2)
5. Draco 압축 모델 사용

```tsx
<Canvas
  gl={{
    antialias: false,       // 안티앨리어싱 끄기
    powerPreference: "high-performance",
  }}
  frameloop="demand"        // 필요할 때만 렌더
>
```

### Q: 모델이 안 보여요

**A: 체크리스트**
1. 경로 확인 (`/public` 폴더)
2. 스케일 확인 (너무 작거나 큼)
3. 카메라 위치 확인
4. 조명 확인

```tsx
// 디버깅용 박스 추가
<mesh position={[0, 0, 0]}>
  <boxGeometry args={[1, 1, 1]} />
  <meshBasicMaterial color="red" wireframe />
</mesh>
```

### Q: 클릭이 안 돼요

**A: raycaster 설정**
```tsx
<Canvas
  raycaster={{
    params: {
      Mesh: { threshold: 0.1 },
      Line: { threshold: 0.1 },
      Points: { threshold: 0.1 },
    },
  }}
>
```

### Q: 그림자가 이상해요

**A: 그림자 설정**
```tsx
<Canvas shadows>
  <directionalLight
    castShadow
    shadow-mapSize={[2048, 2048]}
    shadow-camera-far={50}
    shadow-camera-left={-10}
    shadow-camera-right={10}
    shadow-camera-top={10}
    shadow-camera-bottom={-10}
  />

  <mesh receiveShadow castShadow>
    {/* ... */}
  </mesh>
</Canvas>
```

---

## 카메라 제어

```tsx
import { OrbitControls, PerspectiveCamera } from "@react-three/drei";

function Scene() {
  const cameraRef = useRef();

  const flyTo = (position: [number, number, number]) => {
    // GSAP 또는 spring 애니메이션
    gsap.to(cameraRef.current.position, {
      x: position[0],
      y: position[1],
      z: position[2],
      duration: 2,
    });
  };

  return (
    <>
      <PerspectiveCamera ref={cameraRef} makeDefault position={[10, 10, 10]} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        minDistance={5}
        maxDistance={100}
      />
    </>
  );
}
```

---

## 애니메이션

```tsx
import { useFrame } from "@react-three/fiber";

function RotatingBox() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}
```

---

## Context7 참고

Three.js, React Three Fiber 최신 API가 필요하면 Context7로 조회하세요.
