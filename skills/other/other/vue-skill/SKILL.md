---
name: vue-skill
description: Vue/TypeScriptの実装に関するAgent
tools: Bash, Read, Edit, MultiEdit
---

あなたはVue 3 + TypeScriptプロジェクトのAIアシスタントです。

単独での実行、他のSubagentからの呼び出し、どちらのケースでも適切に動作し、明確な結果を返します。

# Vue/TypeScript実装ガイドライン

このガイドラインは、AI実装で発生しがちな問題パターンとその解決方法をまとめたものです。

## プロジェクト概要

このプロジェクト（pedaru-vue）は、React/Next.jsベースのPDFビューワーアプリ「pedaru」をVue3/Nuxtに移植するものです。

**目的:**
- Vue3の仕組みを効果的に使った実装
- 単なる機能移植ではなく、Vue3のベストプラクティスに沿った設計

**技術スタック:**
- Vue 3 + Composition API（`<script setup>`）
- Nuxt 3
- TypeScript
- Pinia（状態管理）

---

## React から Vue3 への変換ガイド

### React Hooks → Vue3 Composition API マッピング

| React | Vue 3 | 備考 |
|-------|-------|------|
| `useState` | `ref` / `reactive` | プリミティブはref、オブジェクトはreactive |
| `useEffect` | `watch` / `watchEffect` / `onMounted` | 依存配列の有無で使い分け |
| `useCallback` | 通常の関数 | Vueでは不要（必要に応じてcomputed） |
| `useMemo` | `computed` | |
| `useRef` | `ref` / `useTemplateRef` | DOM参照はuseTemplateRef |
| `useContext` | `provide` / `inject` または Pinia | グローバルはPinia推奨 |
| `useReducer` | Pinia store | |

### 変換例

**React (useState + useEffect):**

```tsx
const [count, setCount] = useState(0);
const [doubled, setDoubled] = useState(0);

useEffect(() => {
  setDoubled(count * 2);
}, [count]);
```

**Vue3 (ref + computed):**

```typescript
const count = ref(0);
const doubled = computed(() => count.value * 2);
```

### useEffectの変換パターン

**依存配列なし（マウント時のみ）:**

```tsx
// React
useEffect(() => {
  console.log('mounted');
}, []);
```

```typescript
// Vue3
onMounted(() => {
  console.log('mounted');
});
```

**依存配列あり（値の変更を監視）:**

```tsx
// React
useEffect(() => {
  fetchData(id);
}, [id]);
```

```typescript
// Vue3
watch(() => id.value, (newId) => {
  fetchData(newId);
}, { immediate: true });
```

**クリーンアップあり:**

```tsx
// React
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  return () => clearInterval(timer);
}, []);
```

```typescript
// Vue3
onMounted(() => {
  const timer = setInterval(() => {}, 1000);
  onUnmounted(() => clearInterval(timer));
});
```

### 移植しない機能

以下に該当するものは移植対象外とする：

- **Electron/Tauri固有の処理**: デスクトップアプリ固有のAPI呼び出し
- **不要な互換性維持コード**: 後方互換のためだけのコード
- **過剰なエラーハンドリング**: 発生し得ないケースの処理

---

## 注意！！！

- 当ファイルを読む際は必ず全文読み込んでください。断片的に読んでも良い作業はできません。

## 目次

1. [プロジェクト概要](#プロジェクト概要)
2. [React から Vue3 への変換ガイド](#react-から-vue3-への変換ガイド)
3. [Composables設計のベストプラクティス](#composables設計のベストプラクティス)
4. [既存コンポーネントへの影響を最小化する設計](#既存コンポーネントへの影響を最小化する設計)
5. [コンポーネント設計のベストプラクティス](#コンポーネント設計のベストプラクティス)
6. [TypeScript型安全性のベストプラクティス](#typescript型安全性のベストプラクティス)
7. [テスト戦略とベストプラクティス](#テスト戦略とベストプラクティス)
8. [実装チェックリスト](#実装チェックリスト)
9. [まとめ](#まとめ)

---

### pages/配下のコンポーネント肥大化防止

**原則:** pages/配下のコンポーネントを修正する際は、Atomic Designの考えに基づき、新規コンポーネントを作成してロジックを分離する。

```
pedaru-vue/
├── components/
│   ├── atoms/      # 基本的なUI要素
│   ├── molecules/  # 複合コンポーネント
│   └── organisms/  # 複雑な機能
├── composables/    # ビジネスロジック（型定義も同じファイルに配置）
├── pages/          # ルートコンポーネント（薄く保つ）
└── stores/         # Pinia stores
```

---

## Composables設計のベストプラクティス

### 単一責任の原則

**ガイドライン:**
- 1つのcomposableは1つの関心事のみを扱う
- ファイル名はその責任を明確に表す（`use*`で始まる）
- 50〜100行を目安とし、それを超える場合は分割を検討
- **複数のcomposableを組み合わせて使用する設計を推奨（Compose）**

**❌ Bad: 複数の責任を持つ巨大なComposable**

```typescript
// useVideoManagement.ts（悪い例）
export function useVideoManagement() {
  // ポーリング、時間計算、セッション記録、Zoom SDK操作が混在
  // 100行以上の複雑なロジック...
}
```

**✅ Good: 責任を分離**

```typescript
// useVideoStatus.ts - ビデオステータスのポーリング専用
export function useVideoStatus() {
  const videoStatus = ref<VideoStageStatusResponse | null>(null);
  const fetchVideoStatus = async (id: number) => { /* ... */ };
  const startPolling = (id: number) => { /* ... */ };
  const stopPolling = () => { /* ... */ };
  return { videoStatus, fetchVideoStatus, startPolling, stopPolling };
}

// useSessionElapsedTime.ts - 時間計算専用
export function useSessionElapsedTime(sessionStartTime: Ref<string | null>) {
  const elapsedTime = computed(() => { /* ... */ });
  return { elapsedTime };
}
```

**✅ Good: 複数のComposableを組み合わせる（Compose）**

**重要な判断基準：責任範囲の正しい分離**

例：症状選択機能で「選択」と「送信履歴管理」を1つのcomposableに混在させてはいけません。

```typescript
// ❌ Bad: 責任範囲が混在
// useSymptomSelection.ts
export function useSymptomSelection() {
  // 症状選択の責任
  const toggleSymptomSelection = (key: SymptomItemKeyType) => { /* ... */ };

  // 送信履歴管理の責任（別の関心事！）
  const markAsSent = (key: SymptomItemKeyType) => { /* ... */ };
  const onSendSuccess = () => { /* 混在している */ };

  return { toggleSymptomSelection, markAsSent, onSendSuccess };
}
```

**正しい設計：各関心事を独立したcomposableに分離し、組み合わせて使用**

```typescript
// useSymptomSelection.ts - 症状選択のみに集中
export function useSymptomSelection() {
  const selectedSymptomItems = ref<Set<SymptomItemKeyType>>(new Set());
  const toggleSymptomSelection = (key: SymptomItemKeyType) => { /* ... */ };
  const resetSelectedSymptoms = () => { /* ... */ };
  const selectedSymptoms = computed(() => { /* ... */ });

  return { selectedSymptomItems, selectedSymptoms, toggleSymptomSelection, resetSelectedSymptoms };
}

// useSymptomSendHistory.ts - 送信履歴管理専用（新規ファイル）
export function useSymptomSendHistory() {
  const sentSymptomItems = ref<Set<SymptomItemKeyType>>(new Set());
  const markAsSent = (keys: SymptomItemKeyType[]) => {
    keys.forEach(key => sentSymptomItems.value.add(key));
  };
  const isSent = (key: SymptomItemKeyType): boolean => {
    return sentSymptomItems.value.has(key);
  };

  return { sentSymptomItems, markAsSent, isSent };
}

// useChatMessageGenerator.ts - メッセージ生成専用（新規ファイル）
export function useChatMessageGenerator() {
  const generateSymptomMessage = (symptoms: SymptomItem[]): string => {
    const mainMessage = '症状に合わせたホームケアのPDFをお送りします。';
    const contents = symptoms.map((s) => `・${s.title}\n${s.url}\n`).join('\n');
    return `${mainMessage}\n${contents}`;
  };

  return { generateSymptomMessage };
}

// ChatAttachedPdfSelect.vue - 複数のcomposableを組み合わせる（Compose）
const { selectedSymptoms, resetSelectedSymptoms } = useSymptomSelection();
const { markAsSent } = useSymptomSendHistory();
const { generateSymptomMessage } = useChatMessageGenerator();

const handleSendChat = async () => {
  const message = generateSymptomMessage(selectedSymptoms.value);
  const success = await props.onSendChat(message);

  if (success) {
    markAsSent(selectedSymptoms.value.map(s => s.key));
    resetSelectedSymptoms();
    await showToast();
  }
};
```

**メリット:**
- ✅ **単一責任の原則**: 各composableが1つの関心事のみ
- ✅ **Composeの原則**: 複数のcomposableを組み合わせて使用
- ✅ **テスト容易性**: 各関心事を独立してテスト可能
- ✅ **再利用性**: 送信履歴管理は他の機能でも再利用可能
- ✅ **明確な責任範囲**: ファイル名から役割が明確

### レイヤー分離（技術層とビジネス層）

**ガイドライン:**
- **技術層**: 外部ライブラリ（Zoom SDK、Twilio）の操作のみ
- **アプリケーション層**: ビジネスロジック、Pinia操作、DB記録
- 依存方向は常に「アプリケーション層 → 技術層」
- コメントで設計意図を明示（`// NOTE: Piniaにアクセスしない`など）

**❌ Bad: 技術的な詳細とビジネスロジックが混在**

```typescript
// useZoomVideoSession.ts（悪い例）
export function useZoomVideoSession() {
  const startSession = async () => {
    // Zoom SDKの初期化
    zoomClient.value = ZoomVideo.createClient();
    await zoomClient.value.init('ja-JP', 'Global');

    // ビジネスロジック（DB記録）が混在
    await videoStageRepository.create({ status: 'active' });

    // Piniaへのアクションも混在
    pdfStore.updateStatus('active');
  };
}
```

**✅ Good: レイヤーを明確に分離**

```typescript
// useZoomVideo.ts - 技術層（Zoom SDK操作のみ）
export function useZoomVideo() {
  const createSession = async (sessionId: string) => { /* Zoom SDKのみ */ };
  const joinSession = async (sessionId: string) => { /* Zoom SDKのみ */ };
  // NOTE: Piniaにアクセスしない
  return { createSession, joinSession };
}

// useOnlineReservationVideoSession.ts - アプリケーション層
export function useOnlineReservationVideoSession() {
  const { createSession, joinSession } = useZoomVideo();

  const startTalking = async (sessionId: string, id: number) => {
    await createSession(sessionId);              // 1. Zoom SDK
    await videoStageRepository.create({ id });   // 2. DB記録
    pdfStore.updateStatus({ ... });               // 3. Pinia
    await joinSession(sessionId);                // 4. Zoom SDK
  };

  return { startTalking };
}
```

### 状態管理とスコープ

**ガイドライン:**
- **個別インスタンスが必要**: composable内でstateを定義
- **親子間で共有が必要**: Provide/Injectパターン
- **アプリ全体で共有が必要**: Pinia
- テストでは常に独立したインスタンスを使用できるようにする

**❌ Bad: グローバルなステート共有（シングルトン）**

```typescript
// composable外でstateを定義
const isVideoSessionActive = ref(false);

export function useVideoStatus() {
  // 複数のコンポーネントで同じインスタンスを共有
  return { isVideoSessionActive };
}
```

**✅ Good: composable内でstateを定義（個別インスタンス）**

```typescript
export function useVideoStatus() {
  // composable内でstateを定義（呼び出しごとに新しいインスタンス）
  const isVideoSessionActive = ref(false);
  const preparationState = reactive({
    onlineReservationId: null as number | null,
  });
  return { isVideoSessionActive, preparationState };
}
```

### クリーンアップ処理

**ガイドライン:**
- タイマー、イベントリスナー、WebSocketなどは必ずクリーンアップ
- `getCurrentInstance()`でコンポーネント外での使用を考慮
- `onUnmounted`でリソース解放を保証
- 手動停止メソッドも提供して柔軟性を確保

**❌ Bad: クリーンアップ処理の欠如**

```typescript
export function useVideoStatus() {
  let pollingTimer: number | null = null;

  const startPolling = (id: number) => {
    pollingTimer = window.setInterval(() => { /* ... */ }, 10000);
  };

  // クリーンアップ処理がない！
  return { startPolling };
}
```

**✅ Good: 適切なクリーンアップ処理**

```typescript
export function useVideoStatus() {
  let pollingTimer: number | null = null;

  const startPolling = (id: number) => {
    if (pollingTimer !== null) return; // 重複防止
    pollingTimer = window.setInterval(() => { /* ... */ }, 10000);
  };

  const stopPolling = () => {
    if (pollingTimer !== null) {
      clearInterval(pollingTimer);
      pollingTimer = null;
    }
  };

  // コンポーネント外で使用される可能性を考慮
  const instance = getCurrentInstance();
  if (instance) {
    onUnmounted(() => stopPolling());
  }

  return { startPolling, stopPolling };
}
```

### データ駆動設計

**ガイドライン:**
- **マスターデータは`as const`で定義**し、型推論を活用
- **UIはデータから自動生成**する（`map`/`filter`を使用）
- **ビジネスロジックは汎用的に**設計（特定の値に依存しない）
- **新規追加はデータ定義のみ**で完結するようにする
- **URLなどの派生データは関数で生成**

**❌ Bad: UIとロジックが密結合**

```typescript
export function useBadSymptomSelection() {
  const selectedSymptoms = ref<string[]>([]);

  // 症状ごとにメソッドを追加する必要がある
  const addCough = () => { selectedSymptoms.value.push('咳'); };
  const addFever = () => { selectedSymptoms.value.push('発熱'); };

  return { selectedSymptoms, addCough, addFever };
}
```

**✅ Good: マスターデータから自動生成**

```typescript
// 1. マスターデータの定義（as constで型推論）
const symptomItems = {
  seki: { title: '咳', category: '咳' },
  netsu_jyunyu: { title: '発熱(授乳期)', category: '発熱' },
  hanamizu: { title: '鼻水', category: '鼻水' },
} as const;

// 2. 型の自動生成
export type SymptomItemKeyType = keyof typeof symptomItems;

// 3. データからUI構造を自動生成
const symptoms = categories.map((category) => ({
  category,
  items: Object.entries(symptomItems)
    .filter(([, item]) => item.category === category)
    .map(([key, { title }]) => ({
      key: key as SymptomItemKeyType,
      title,
      url: generateUrl(key as SymptomItemKeyType),
    })),
}));

// 4. 汎用的なビジネスロジック
export const toggleSymptomSelection = (key: SymptomItemKeyType) => {
  if (selectedSymptomItems.value.has(key)) {
    selectedSymptomItems.value.delete(key);
  } else {
    selectedSymptomItems.value.add(key);
  }
};
```

**拡張性の実例:**

```typescript
// ✅ 新しい症状を追加（データ定義のみ、1箇所の変更）
const symptomItems = {
  // ... 既存の定義
  atopy: { title: 'アトピー性皮膚炎', category: '皮膚トラブル' }, // 追加
} as const;
// → UIは自動的に更新される
```

---

## 既存コンポーネントへの影響を最小化する設計

**ガイドライン:**
- **新機能は新規コンポーネントに隔離**する
- **親コンポーネントへの変更は最小限**に（10行以内を目標）
- **既存のメソッドを再利用**できる場合はコールバック関数Propsを使う
- **Props/Emitsはシンプルに**保つ（2〜3個まで）
- **ビジネスロジックはComposableに委譲**する
- **UIロジックは新規コンポーネント内で完結**させる

### 影響範囲の比較

| 項目 | Bad Pattern | Good Pattern |
|------|-------------|--------------|
| 親コンポーネントの変更行数 | 300行以上 | 10行以内 |
| 新規Import | なし（全て親に実装） | 1行のみ |
| 既存メソッドの変更 | 複数のメソッド修正 | 変更なし（再利用） |
| 新規dataの追加 | 5個以上 | 0個 |
| テスト対象 | 親コンポーネント全体 | 新規コンポーネントのみ |

### シンプルなPropsインターフェース

```typescript
interface Props {
  onSendChat: (message: string) => void; // コールバック関数
  isDoctorPage: boolean;                 // 表示制御フラグ
}
```

**なぜEmitではなくコールバック関数を使うのか:**

```typescript
// ❌ Bad: Emitを使う場合（親側の変更が必要）
// 親コンポーネント（新規メソッドが必要）
<ChatAttachedPdfSelect @send-chat="handleSymptomChatSend" />
methods: {
  handleSymptomChatSend(message) {
    this.handleChatSend(message); // 既存メソッドを呼ぶだけ
  }
}

// ✅ Good: コールバック関数を使う場合（親側の変更不要）
// 親コンポーネント（既存メソッドをそのまま渡す）
<ChatAttachedPdfSelect :onSendChat="handleChatSend" />
// 新規メソッド不要！
```

---

## コンポーネント設計のベストプラクティス

### Atomic Design

**ガイドライン:**
- **pages/**: ルーティングとメタ情報のみ（50行以内）
- **organisms/**: 複雑な機能の統合（100〜200行）
- **molecules/**: 複合コンポーネント（50〜100行）
- **atoms/**: 基本的なUI要素（30〜50行）
- **composables/**: ビジネスロジックと状態管理

**ディレクトリ構造:**

```
pedaru-vue/
├── pages/
│   └── index.vue           # 薄いルートコンポーネント（50行以内）
├── components/
│   ├── organisms/
│   │   └── PdfViewer.vue   # PDFビューワー全体
│   ├── molecules/
│   │   ├── PdfToolbar.vue  # ツールバー
│   │   └── PdfPageNav.vue  # ページナビゲーション
│   └── atoms/
│       ├── BaseButton.vue  # ボタン
│       └── BaseIcon.vue    # アイコン
├── composables/
│   ├── usePdfViewer.ts     # 型定義もこのファイル内に配置
│   └── usePdfNavigation.ts
└── stores/
    └── pdf.ts              # Pinia store（型定義も同じファイル内）
```

### Props/Emitsの型安全な定義

**ガイドライン:**
- **Propsは必ずTypeScriptのinterfaceで定義**
- **必須とオプショナルを明示的に区別**（`?`を使う）
- **Emitsも型定義する**（ペイロードの型を明確に）
- **シンプルな通知はEmit**、**複雑な処理フローはコールバック関数**
- **コールバック関数を使う理由をコメントで明示**

**✅ Good: 型安全なProps/Emits定義**

```vue
<script setup lang="ts">
// Props定義をinterfaceで明示
interface Props {
  isOnCamera: boolean;
  isOnAudio: boolean;
  nurseName: string;
  patientName?: string;  // オプショナルは明示的に
}

const props = defineProps<Props>();

// Emits定義も型安全に
interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'leave', reason: 'user-action' | 'timeout'): void;
}

const emit = defineEmits<Emits>();
</script>
```

**コールバック vs Emit の使い分け:**

```vue
<!-- パターン1: Emitを使う（シンプルな通知） -->
<script setup lang="ts">
interface Emits {
  (e: 'close'): void;
  (e: 'submit', data: FormData): void;
}
const emit = defineEmits<Emits>();
</script>

<!-- パターン2: コールバック関数を使う（複雑な処理フロー） -->
<script setup lang="ts">
interface Props {
  isDisplayVideoWindow: boolean;
  leaveSession: () => Promise<void>;  // 関数を直接渡す
}

const props = defineProps<Props>();

const onLeaveClick = async () => {
  // NOTE: 親コンポーネントで定義した処理を利用する必要がある
  // 理由：親のVideoStatusPanelで表示制御のフラグ更新とZoomのビデオ退出を行う
  await props.leaveSession();
};
</script>
```

### コンポーネント肥大化の防止

**ガイドライン:**
- **コンポーネントは100行以内を目標**
- **ロジックはcomposablesに分離**
- **UIはAtomic Designに基づいて分割**
- **テンプレートも100行を超えたら分割を検討**
- **1ファイル200行を超えたら必ず分割**

---

## TypeScript型安全性のベストプラクティス

### 型定義の配置方針

**ガイドライン:**
- **型定義はロジックに近い場所に配置する**（専用の`types/`ディレクトリは作らない）
- composableで使う型はそのcomposableファイル内に定義
- storeで使う型はそのstoreファイル内に定義
- 複数ファイルで共有する型のみ、関連するcomposableからexport

**❌ Bad: 別ディレクトリに型定義を分離**

```
composables/
└── usePdfViewer.ts
types/
└── pdf.ts          # 型定義が離れている
```

**✅ Good: ロジックと型定義を同じファイルに配置**

```typescript
// composables/usePdfViewer.ts

// 型定義（このcomposableで使用する型）
export interface PdfViewerState {
  currentPage: number;
  totalPages: number;
  scale: number;
}

export type PdfLoadStatus = 'idle' | 'loading' | 'loaded' | 'error';

// ロジック
export function usePdfViewer() {
  const state = reactive<PdfViewerState>({
    currentPage: 1,
    totalPages: 0,
    scale: 1.0,
  });
  const status = ref<PdfLoadStatus>('idle');

  // ...
  return { state, status };
}
```

**メリット:**
- 型とロジックが近いため、変更時の影響範囲が明確
- ファイルを開くだけで型の定義がわかる
- 不要な型が残りにくい（ロジック削除時に型も一緒に削除される）

### as constとUnion型の活用

**ガイドライン:**
- **定数はas constで定義**してUnion型を自動生成
- **文字列リテラル型を活用**して型安全性を確保
- **Template Literal Type**で命名規則を型で表現
- **keyof typeof**でオブジェクトからUnion型を生成

**❌ Bad: 文字列リテラルを直接使用**

```typescript
const status = ref<string>('notYetStarted');
const updateStatus = (newStatus: string) => {
  status.value = newStatus; // 任意の文字列を許容してしまう
};
updateStatus('typo-status'); // コンパイルエラーにならない
```

**✅ Good: as constとUnion型の活用**

```typescript
// 定数オブジェクトをas constで定義
export const OnlineReservationVideoSessionStatus = {
  notYetStarted: 'notYetStarted',
  sessionCreating: 'sessionCreating',
  sessionCreated: 'sessionCreated',
  sessionStarted: 'sessionStarted',
} as const;

// Union型を自動生成
export type OnlineReservationVideoSessionStatusType =
  (typeof OnlineReservationVideoSessionStatus)[keyof typeof OnlineReservationVideoSessionStatus];

// 使用例
const status = ref<OnlineReservationVideoSessionStatusType>(
  OnlineReservationVideoSessionStatus.notYetStarted
);

updateStatus(OnlineReservationVideoSessionStatus.sessionStarted); // ✅ OK
updateStatus('typo-status'); // ❌ コンパイルエラー
```

**Template Literal Typeの活用:**

```typescript
// 命名規則を型レベルで表現
type ZoomRoomNameType = `online_reservation_${number}`;

const createRoomName = (id: number): ZoomRoomNameType => {
  return `online_reservation_${id}`;
};
```

### Type Guardと型の絞り込み

**ガイドライン:**
- **unknownからの型変換には必ずType Guardを使用**
- **anyは絶対に使わない**
- **Type Guard関数は`is`演算子を使って定義**
- **複数の型を扱う場合はそれぞれType Guardを定義**

**❌ Bad: unknownをanyにキャスト**

```typescript
const onErrorOccur = (e: unknown) => {
  const error = e as any; // anyにキャストして型チェックを回避
  if (error.errorCode) {
    Sentry.captureMessage(`Error code: ${error.errorCode}`);
  }
};
```

**✅ Good: Type Guardで安全に型を絞り込む**

```typescript
// Type Guardの定義
interface ZoomErrorObject {
  type?: string;
  reason?: string;
  errorCode?: number;
}

export const isZoomErrorObject = (error: unknown): error is ZoomErrorObject => {
  return (
    error !== null &&
    typeof error === 'object' &&
    ('type' in error || 'reason' in error || 'errorCode' in error)
  );
};

// 使用例
const onErrorOccur = (e: unknown) => {
  if (isZoomErrorObject(e)) {
    // この中ではeはZoomErrorObject型として扱える
    Sentry.captureMessage(`Zoom Error: ${e.errorCode}`);
  } else {
    Sentry.captureException(e);
  }
};
```

---

## テスト戦略とベストプラクティス

### 価値のあるテストのみ

**ガイドライン:**
- **振る舞いをテスト**し、実装の詳細はテストしない
- **正常系とエラー系の両方をカバー**
- **単純なgetter/setterはテスト不要**
- **ビジネスロジックの正しさを検証**

**❌ Bad: 実装の詳細をテスト**

```typescript
describe('useVideoStatus', () => {
  it('videoStatusはrefである', () => {
    const { videoStatus } = useVideoStatus();
    expect(isRef(videoStatus)).toBe(true); // 価値が低い
  });

  it('isLoadingの初期値はfalseである', () => {
    const { isLoading } = useVideoStatus();
    expect(isLoading.value).toBe(false); // 価値が低い
  });
});
```

**✅ Good: 振る舞いをテスト**

```typescript
describe('useVideoStatus', () => {
  it('API から VideoStage 情報を取得して videoStatus に設定する', async () => {
    const mockResponse = { data: { video_stages: [{ id: 1, status: 'active' }] } };
    mockVideoStageRepository.fetchStatus.mockResolvedValue(mockResponse);

    const { videoStatus, fetchVideoStatus } = useVideoStatus();
    await fetchVideoStatus(123);

    expect(mockVideoStageRepository.fetchStatus).toHaveBeenCalledWith(123);
    expect(videoStatus.value).toMatchObject({ valid_status: true });
  });

  it('API エラー時に error メッセージを設定する', async () => {
    mockVideoStageRepository.fetchStatus.mockRejectedValue(new Error('Network error'));

    const { error, fetchVideoStatus } = useVideoStatus();
    await fetchVideoStatus(123);

    expect(error.value).toBe('状態の取得に失敗しました');
  });
});
```

### タイマーとポーリングのテスト

**ガイドライン:**
- **`vi.useFakeTimers()`でタイマーを制御可能に**
- **`vi.advanceTimersByTimeAsync()`で時間を進める**
- **Luxon使用時は`Settings.now`も設定**
- **afterEachで必ず`vi.useRealTimers()`を呼ぶ**
- **ポーリングの開始・停止・間隔を検証**

**❌ Bad: 実際の時間を待つ**

```typescript
it('1秒後に経過時間が更新される', async () => {
  const { elapsedTime } = useSessionElapsedTime(sessionStartTime);
  await new Promise(resolve => setTimeout(resolve, 1000)); // テストが遅い
  expect(elapsedTime.value).toBe('00:00:01');
});
```

**✅ Good: Fake Timersを使用**

```typescript
describe('useSessionElapsedTime', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    Settings.now = () => Date.now(); // Luxonの時刻もリセット
  });

  it('HH:mm:ss形式で経過時間を返す', () => {
    const now = new Date('2025-01-07T10:30:00');
    vi.setSystemTime(now);
    Settings.now = () => now.getTime();

    const startTime = DateTime.fromISO('2025-01-07T09:00:00');
    const sessionStartTime = ref(startTime.toISO());

    const { elapsedTime } = useSessionElapsedTime(sessionStartTime);

    expect(elapsedTime.value).toBe('01:30:00');
  });
});

describe('startPolling', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('10秒間隔でポーリングが実行される', async () => {
    mockVideoStageRepository.fetchStatus.mockResolvedValue({ data: {} });
    const { startPolling } = useVideoStatus();

    startPolling(123);
    await vi.advanceTimersByTimeAsync(0);
    expect(mockVideoStageRepository.fetchStatus).toHaveBeenCalledTimes(1);

    await vi.advanceTimersByTimeAsync(10000); // 10秒後
    expect(mockVideoStageRepository.fetchStatus).toHaveBeenCalledTimes(2);
  });
});
```

---

## 実装チェックリスト

新しい機能を実装する際は、以下をチェックしてください：

### 設計段階

- [ ] **Vue2とVue3のどちらで実装するか確認したか？**（新規は必ずVue3）
- [ ] pages/配下のコンポーネントは薄く保てるか？（50行以内）
- [ ] **既存コンポーネントへの影響を最小限にできるか？**（10行以内の変更を目標）
- [ ] ロジックをcomposablesに分離できるか？
- [ ] **データ駆動設計を適用できるか？**（マスターデータから自動生成）
- [ ] Atomic Designに基づいてコンポーネントを分割できるか？
- [ ] **1つのcomposableが複数の責任を持っていないか？**
- [ ] **複数の関心事を持つcomposableを、独立した複数のcomposableに分離しているか？**（Composeパターン）
- [ ] 技術層とビジネス層を分離できるか？
- [ ] **将来の拡張性を考慮した設計か？**（データ追加で自動的にUIが更新される）

### 実装段階

- [ ] **`<script setup>`とTypeScriptを使用しているか？**
- [ ] **型定義はロジックに近い場所に配置しているか？**（専用の`types/`ディレクトリは作らない）
- [ ] Props/Emitsに型定義を付けているか？
- [ ] **既存メソッドを再利用できる場合はコールバック関数Propsを使っているか？**
- [ ] **マスターデータを`as const`で定義しているか？**
- [ ] as constとUnion型を活用しているか？
- [ ] Type Guardで安全に型を絞り込んでいるか？
- [ ] anyを使っていないか？
- [ ] **v-forでUIを自動生成しているか？**（ハードコードを避ける）
- [ ] **keyには一意なID（item.id、item.key）を使用しているか？**（indexを使っていないか）
- [ ] タイマーやイベントリスナーのクリーンアップ処理を実装したか？
- [ ] `getCurrentInstance()`でコンポーネント外での使用を考慮したか？
- [ ] 複雑な処理フローではコールバック関数を使っているか？
- [ ] コメントで設計意図を明示しているか？

### テスト段階

- [ ] 振る舞いをテストしているか？（実装の詳細ではなく）
- [ ] 正常系とエラー系の両方をカバーしているか？
- [ ] タイマーテストでFake Timersを使っているか？
- [ ] モックは外部依存のみに限定しているか？
- [ ] テストの独立性を保っているか？

---

## まとめ

AIに実装を依頼する際は、以下を意識してください：

### 基本原則

1. **Vue3 Composition API + TypeScriptを使用**: 常に`<script setup>`を使用
2. **単一責任の原則を守る**: 1つのcomposable/コンポーネントは1つの関心事のみ
3. **レイヤーを分離する**: 技術層とビジネス層を明確に分ける
4. **Atomic Designを適用する**: pages → organisms → molecules → atoms
5. **型安全性を確保する**: as const、Union型、Type Guardを活用
6. **クリーンアップ処理を実装**: タイマー、イベントリスナーは必ず解放
7. **データ駆動設計を推進**: マスターデータからUIを自動生成（DRY原則）
8. **既存コンポーネントへの影響を最小化**: 新機能は新規コンポーネントに隔離

### 実装のポイント

- **Composables**: 50〜100行、単一責任、技術層とビジネス層を分離、データ駆動設計、**複数のcomposableを組み合わせる（Compose）**
- **コンポーネント**: 100行以内、ロジックはcomposablesに委譲、v-forで動的生成
- **Props/Emits**: 必ずTypeScriptで型定義、既存メソッド再利用時はコールバック関数
- **TypeScript**: as const、Union型、Type Guard、Template Literal Type
- **テスト**: 振る舞いをテスト、Fake Timers、モック最小化

### 特に重要：pages/配下のコンポーネント肥大化防止

- **pages/**: 50行以内の薄いルートコンポーネント
- **organisms/**: 100〜200行の機能統合
- **molecules/**: 50〜100行の複合コンポーネント
- **composables/**: ビジネスロジックと状態管理

### 特に重要：データ駆動設計と拡張性

- **マスターデータ定義**: `as const`で型推論、1箇所で管理
- **UIは自動生成**: v-forでデータから動的に生成
- **新規追加は容易**: データ定義のみで完結（UIコードの修正不要）
- **型安全性の確保**: TypeScriptの型チェックで誤りを防止
- **テストの独立性**: データ変更でUIが正しく更新されるかを検証

### 特に重要：既存コンポーネントへの影響最小化

- **親コンポーネントへの変更は10行以内**を目標
- **既存メソッドの再利用**: コールバック関数Propsで疎結合
- **新機能は新規コンポーネントに隔離**: リグレッションリスク最小化
- **Props/Emitsはシンプルに**: 2〜3個まで
- **レビューしやすい差分**: 変更箇所を最小限に

これらの原則に従うことで、保守性が高く、テストしやすく、拡張性のある、品質の高いVue/TypeScriptコードを実装できます。

---

## 参考

- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Vue 3 TypeScript](https://vuejs.org/guide/typescript/overview.html)
- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Atomic Design](https://atomicdesign.bradfrost.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
