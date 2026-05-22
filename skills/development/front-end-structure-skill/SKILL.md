---
name: Front-End Structure
description: Build Vue 3 + Ionic front-end components following Orchestrator AI's strict architecture: stores hold state only, services handle API calls with transport types, components use services and read stores. CRITICAL: Maintain view reactivity by keeping stores simple - no methods, no API calls, no business logic.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Front-End Structure Skill

**CRITICAL ARCHITECTURE RULE**: Stores hold **data only**. Services handle **API calls**. Components use **services** and read **stores**. Vue reactivity handles **UI updates automatically**.

## When to Use This Skill

Use this skill when:
- Creating new Vue components
- Creating new Pinia stores
- Creating new service files
- Working with API calls and state management
- Building requests that use transport types
- Ensuring view reactivity works correctly

**CRITICAL**: Agents often want to write methods directly on stores. This breaks reactivity and the architecture. Always redirect to the service layer.

## The Three-Layer Architecture

```
┌─────────────────────────────────────────┐
│         VIEW LAYER (Components)         │
│  - Reads from stores (computed/ref)      │
│  - Calls service methods                │
│  - Reacts to store changes automatically│
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         SERVICE LAYER                   │
│  - Builds requests with transport types  │
│  - Makes API calls                      │
│  - Updates stores with responses        │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         STORE LAYER (Pinia)             │
│  - Holds state ONLY (ref/computed)      │
│  - Simple setters                       │
│  - NO methods, NO API calls             │
└─────────────────────────────────────────┘
```

## Critical Pattern #1: Stores Are Data-Only

Stores contain **ONLY**:
- State (`ref()`)
- Computed getters (`computed()`)
- Simple setters (synchronous state updates)

Stores contain **NEVER**:
- Async methods
- API calls
- Business logic
- Complex processing

### ✅ CORRECT Store Pattern

Here's an example from `apps/web/src/stores/privacyStore.ts`:

```127:260:apps/web/src/stores/privacyStore.ts
export const usePrivacyStore = defineStore('privacy', () => {
  // ==========================================================================
  // STATE - PSEUDONYM MAPPINGS
  // ==========================================================================

  const mappings = ref<PseudonymMapping[]>([]);
  const mappingsLoading = ref(false);
  const mappingsError = ref<string | null>(null);
  const mappingsLastFetched = ref<Date | null>(null);

  const mappingFilters = ref<PseudonymMappingFilters>({
    dataType: 'all',
    context: undefined,
    search: ''
  });

  const mappingSortOptions = ref<PseudonymMappingSortOptions>({
    field: 'usageCount',
    direction: 'desc'
  });

  const mappingStats = ref<PseudonymStatsResponse['stats'] | null>(null);
  const mappingStatsLoading = ref(false);
  const mappingStatsError = ref<string | null>(null);

  // ==========================================================================
  // STATE - PSEUDONYM DICTIONARIES
  // ==========================================================================

  const dictionaries = ref<PseudonymDictionaryEntry[]>([]);
  const dictionariesLoading = ref(false);
  const dictionariesError = ref<string | null>(null);
  const dictionariesLastUpdated = ref<Date | null>(null);

  const dictionaryFilters = ref<PseudonymDictionaryFilters>({
    category: 'all',
    dataType: 'all',
    isActive: 'all',
    search: ''
  });

  const dictionarySortOptions = ref<PseudonymDictionarySortOptions>({
    field: 'category',
    direction: 'asc'
  });

  const selectedDictionaryIds = ref<string[]>([]);
  const generationResult = ref<PseudonymGenerateResponse | null>(null);
  const lookupResult = ref<PseudonymLookupResponse | null>(null);
  const isGenerating = ref(false);

  const dictionaryStats = ref<PseudonymStatsResponse | null>(null);

  const importProgress = ref<{ imported: number; total: number; errors: string[] } | null>(null);
  const isImporting = ref(false);
  const isExporting = ref(false);

  // ==========================================================================
  // STATE - PII PATTERNS
  // ==========================================================================

  const patterns = ref<PIIPattern[]>([]);
  const patternsLoading = ref(false);
  const patternsError = ref<string | null>(null);
  const patternsLastUpdated = ref<Date | null>(null);

  const patternFilters = ref<PIIPatternFilters>({
    dataType: 'all',
    enabled: 'all',
    isBuiltIn: 'all',
    category: 'all',
    search: ''
  });

  const patternSortOptions = ref<PIIPatternSortOptions>({
    field: 'name',
    direction: 'asc'
  });

  const selectedPatternIds = ref<string[]>([]);
  const testResult = ref<PIITestResponse | null>(null);
  const isTestingPII = ref(false);
  const patternStats = ref<PIIStatsResponse | null>(null);

  // ==========================================================================
  // STATE - PRIVACY INDICATORS
  // ==========================================================================

  const messageStates = ref<Map<string, MessagePrivacyState>>(new Map());
  const conversationSettings = ref<Map<string, ConversationPrivacySettings>>(new Map());

  const globalSettings = ref({
    enableGlobalRealTime: true,
    defaultUpdateInterval: 2000,
    maxStoredStates: 100,
    autoCleanupAge: 3600000, // 1 hour in ms
    debugMode: false
  });

  const indicatorsInitialized = ref(false);
  const activeUpdateTimers = ref<Map<string, NodeJS.Timeout>>(new Map());
  const lastGlobalUpdate = ref<Date | null>(null);

  // ==========================================================================
  // STATE - DASHBOARD
  // ==========================================================================

  const dashboardData = ref<PrivacyDashboardData | null>(null);
  const dashboardLoading = ref(false);
  const dashboardError = ref<string | null>(null);
  const dashboardLastUpdated = ref<Date | null>(null);
  const autoRefreshInterval = ref<NodeJS.Timeout | null>(null);

  const dashboardFilters = ref<DashboardFilters>({
    timeRange: '7d',
    dataType: ['all'],
    includeSystemEvents: true
  });

  // ==========================================================================
  // STATE - SOVEREIGN POLICY
  // ==========================================================================

  const sovereignPolicy = ref<SovereignPolicy | null>(null);
  const userSovereignMode = ref(false);
  const sovereignLoading = ref(false);
  const sovereignError = ref<string | null>(null);
  const sovereignInitialized = ref(false);

  // ==========================================================================
  // COMPUTED - PSEUDONYM MAPPINGS
  // ==========================================================================

  const totalMappings = computed(() => mappings.value.length);

  const availableDataTypes = computed(() => {
    const types = new Set(mappings.value.map(m => m.dataType));
    return Array.from(types).sort();
  });

  const availableContexts = computed(() => {
    const contexts = new Set(mappings.value.map(m => m.context).filter(Boolean));
    return Array.from(contexts).sort();
  });
```

**Key Points:**
- ✅ Only `ref()` for state
- ✅ Only `computed()` for derived state
- ✅ Simple setters (not shown here, but they exist)
- ❌ NO async methods
- ❌ NO API calls
- ❌ NO business logic

### ❌ FORBIDDEN Store Pattern

```typescript
// ❌ WRONG - This breaks the architecture
export const useMyStore = defineStore('myStore', () => {
  const data = ref(null);
  
  // ❌ FORBIDDEN - Async method in store
  async function fetchData() {
    const response = await fetch('/api/data');
    data.value = await response.json();
  }
  
  // ❌ FORBIDDEN - Business logic in store
  function processData() {
    data.value = data.value.map(/* complex logic */);
  }
  
  return { data, fetchData, processData };
});
```

## Critical Pattern #2: Services Handle API Calls with Transport Types

Services:
1. Build requests using transport types from `@orchestrator-ai/transport-types`
2. Make API calls
3. Update stores with responses

### ✅ CORRECT Service Pattern

Here's an example from `apps/web/src/services/agent2agent/api/agent2agent.api.ts`:

```106:149:apps/web/src/services/agent2agent/api/agent2agent.api.ts
  plans = {
    create: async (conversationId: string, message: string) => {
      const strictRequest = buildRequest.plan.create(
        { conversationId, userMessage: message },
        { title: '', content: message }
      );
      return this.executeStrictRequest(strictRequest);
    },

    read: async (conversationId: string) => {
      const strictRequest = buildRequest.plan.read({ conversationId });
      return this.executeStrictRequest(strictRequest);
    },

    list: async (conversationId: string) => {
      const strictRequest = buildRequest.plan.list({ conversationId });
      return this.executeStrictRequest(strictRequest);
    },

    edit: async (conversationId: string, editedContent: string, metadata?: Record<string, unknown>) => {
      const strictRequest = buildRequest.plan.edit(
        { conversationId, userMessage: 'Edit plan' },
        { editedContent, metadata }
      );
      return this.executeStrictRequest(strictRequest);
    },

    rerun: async (
      conversationId: string,
      versionId: string,
      config: {
        provider: string;
        model: string;
        temperature?: number;
        maxTokens?: number;
      },
      userMessage?: string
    ) => {
      const strictRequest = buildRequest.plan.rerun(
        { conversationId, userMessage: userMessage || 'Please regenerate this plan with the same requirements' },
        { versionId, config }
      );
      return this.executeStrictRequest(strictRequest);
    },
```

**Key Points:**
- ✅ Uses `buildRequest` to create requests with transport types
- ✅ Makes API calls (`executeStrictRequest`)
- ✅ Returns response (doesn't update store directly - that's done by the calling component/service)

### Building Requests with Transport Types

Here's how requests are built using transport types from `apps/web/src/services/agent2agent/utils/builders/build.builder.ts`:

```33:59:apps/web/src/services/agent2agent/utils/builders/build.builder.ts
export const buildBuilder = {
  /**
   * Execute build (create deliverable)
   */
  execute: (
    metadata: RequestMetadata & { userMessage: string },
    buildData?: { planId?: string; [key: string]: unknown },
  ): StrictBuildRequest => {
    validateRequired(metadata.conversationId, 'conversationId');
    validateRequired(metadata.userMessage, 'userMessage');

    return {
      jsonrpc: '2.0',
      id: crypto.randomUUID(),
      method: 'build.execute',
      params: {
        mode: 'build' as AgentTaskMode,
        action: 'execute' as BuildAction,
        conversationId: metadata.conversationId,
        userMessage: metadata.userMessage,
        messages: metadata.messages || [],
        planId: buildData?.planId,
        metadata: metadata.metadata,
        payload: buildData || {},
      },
    };
  },
```

**Key Points:**
- ✅ Imports types from `@orchestrator-ai/transport-types`
- ✅ Returns `StrictBuildRequest` (ensures type safety)
- ✅ Validates required fields
- ✅ Builds JSON-RPC 2.0 compliant request

## Critical Pattern #3: Components Use Services, Read Stores

Components:
1. Call service methods (not store methods for API calls)
2. Read from stores using `computed()` or `ref()`
3. Vue automatically reacts to store changes

### ✅ CORRECT Component Pattern

Here's an example from `apps/web/src/components/Analytics/AnalyticsDashboard.vue`:

```408:480:apps/web/src/components/Analytics/AnalyticsDashboard.vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonItem,
  IonLabel,
  IonButton,
  IonToggle,
  IonSelect,
  IonSelectOption,
  IonInput,
  IonBadge,
  IonIcon,
  IonSpinner,
  IonGrid,
  IonRow,
  IonCol,
  IonList,
  IonAvatar
} from '@ionic/vue';
import {
  analyticsOutline,
  refreshOutline,
  trendingUpOutline,
  cashOutline,
  speedometerOutline,
  checkmarkCircleOutline,
  pulseOutline,
  trophyOutline,
  timeOutline,
  pieChartOutline,
  layersOutline,
  alertCircleOutline,
  documentTextOutline,
  personOutline,
  settingsOutline,
  warningOutline
} from 'ionicons/icons';
import { useAnalyticsStore } from '@/stores/analyticsStore';
import { useLLMMonitoringStore } from '@/stores/llmMonitoringStore';

// Store integration
const analyticsStore = useAnalyticsStore();
const llmMonitoringStore = useLLMMonitoringStore();

// Computed properties
const dashboardData = computed(() => analyticsStore.dashboardData);
const systemHealthStatus = computed(() => llmMonitoringStore.systemHealth?.status || 'unknown');
const costAnalysis = computed(() => analyticsStore.costAnalysis);
const isLoading = computed(() => analyticsStore.isLoading || llmMonitoringStore.isLoading);
const hasError = computed(() => !!analyticsStore.error || !!llmMonitoringStore.error);
const firstError = computed(() => analyticsStore.error || llmMonitoringStore.error);

// Auto-refresh functionality
const isAutoRefreshEnabled = ref(false);
const toggleAutoRefresh = () => {
  isAutoRefreshEnabled.value = !isAutoRefreshEnabled.value;
};

const refreshNow = async () => {
  await refreshAll();
};

const refreshAll = async () => {
  await Promise.all([
    analyticsStore.loadDashboardData(),
    llmMonitoringStore.fetchSystemHealth()
  ]);
};

// Reactive data
const selectedTimeRange = ref('last7days');
const customStartDate = ref('');
const customEndDate = ref('');
const autoRefreshInterval = ref(30000); // 30 seconds
```

**Key Points:**
- ✅ Uses `computed()` to read from stores (maintains reactivity)
- ✅ Calls store methods for actions (like `loadDashboardData()`)
- ✅ Vue automatically re-renders when store values change
- ✅ No manual DOM updates
- ✅ No `forceUpdate()` or similar hacks

### View Reactivity in Action

Notice how the component uses `computed()`:

```typescript
// ✅ CORRECT - Computed maintains reactivity
const dashboardData = computed(() => analyticsStore.dashboardData);
const isLoading = computed(() => analyticsStore.isLoading);
const hasError = computed(() => !!analyticsStore.error);
```

When `analyticsStore.dashboardData` changes (updated by a service), Vue automatically:
1. Detects the change (because `ref()` is reactive)
2. Re-runs the computed
3. Updates the template
4. Re-renders the component

**No manual updates needed!**

## Critical Pattern #4: Response → Store → View Reactivity

The flow is **ALWAYS**:

```
Service makes API call
    ↓
Service updates store state
    ↓
Vue reactivity detects change
    ↓
Component re-renders automatically
```

### Complete Example

Here's a complete example showing the flow:

**1. Store (State Only):**
```typescript
// stores/conversationsStore.ts
export const useConversationsStore = defineStore('conversations', () => {
  const conversations = ref<Conversation[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  
  const currentConversation = computed(() => 
    conversations.value.find(c => c.id === currentConversationId.value)
  );
  
  function setConversations(newConversations: Conversation[]) {
    conversations.value = newConversations; // ← State update
  }
  
  function setLoading(loading: boolean) {
    isLoading.value = loading; // ← State update
  }
  
  function setError(errorMessage: string | null) {
    error.value = errorMessage; // ← State update
  }
  
  return { conversations, isLoading, error, currentConversation, setConversations, setLoading, setError };
});
```

**2. Service (API Calls + Store Updates):**
```typescript
// services/conversationsService.ts
import { useConversationsStore } from '@/stores/conversationsStore';
import { buildRequest } from '@/services/agent2agent/utils/builders';
import { agent2AgentApi } from '@/services/agent2agent/api/agent2agent.api';

export const conversationsService = {
  async loadConversations() {
    const store = useConversationsStore();
    
    store.setLoading(true); // ← Update store
    store.setError(null);   // ← Update store
    
    try {
      // Build request with transport types
      const request = buildRequest.plan.list({ conversationId: 'current' });
      
      // Make API call
      const response = await agent2AgentApi.executeStrictRequest(request);
      
      // Update store with response
      store.setConversations(response.result.conversations); // ← Update store
      
      return response.result;
    } catch (error) {
      store.setError(error.message); // ← Update store
      throw error;
    } finally {
      store.setLoading(false); // ← Update store
    }
  }
};
```

**3. Component (Uses Service, Reads Store):**
```vue
<template>
  <div>
    <!-- Vue automatically reacts to store changes -->
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">{{ error }}</div>
    <div v-for="conv in conversations" :key="conv.id">
      {{ conv.title }}
    </div>
    <button @click="loadData">Load Conversations</button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useConversationsStore } from '@/stores/conversationsStore';
import { conversationsService } from '@/services/conversationsService';

const store = useConversationsStore();

// Read from store using computed (maintains reactivity)
const conversations = computed(() => store.conversations);
const isLoading = computed(() => store.isLoading);
const error = computed(() => store.error);

async function loadData() {
  // Call service method (not store method)
  await conversationsService.loadConversations();
  // Store updated by service
  // Vue automatically re-renders because computed values changed
}

onMounted(() => {
  loadData();
});
</script>
```

## Common Mistakes Agents Make

### ❌ Mistake 1: API Calls in Stores

```typescript
// ❌ WRONG
export const useMyStore = defineStore('myStore', () => {
  const data = ref(null);
  
  async function fetchData() {
    const response = await fetch('/api/data');
    data.value = await response.json();
  }
  
  return { data, fetchData };
});
```

**Fix:** Move API call to service, store only holds state.

### ❌ Mistake 2: Methods on Stores

```typescript
// ❌ WRONG
function processData() {
  this.data = this.data.map(/* complex logic */);
}
```

**Fix:** Processing happens in service or component, store only holds state.

### ❌ Mistake 3: Not Using Transport Types

```typescript
// ❌ WRONG - Raw fetch without transport types
const response = await fetch('/api/plan', {
  method: 'POST',
  body: JSON.stringify({ conversationId })
});
```

**Fix:** Use `buildRequest` with transport types:
```typescript
const request = buildRequest.plan.read({ conversationId });
const response = await agent2AgentApi.executeStrictRequest(request);
```

### ❌ Mistake 4: Not Using Computed for Store Values

```typescript
// ❌ WRONG - Direct ref access loses reactivity in some cases
const data = store.data; // May not be reactive

// ✅ CORRECT - Use computed
const data = computed(() => store.data);
```

### ❌ Mistake 5: Manual UI Updates

```typescript
// ❌ WRONG - Manual DOM manipulation
function updateUI() {
  document.getElementById('data').innerHTML = this.data;
}
```

**Fix:** Let Vue reactivity handle it - just update the store.

## File Structure

```
apps/web/src/
├── stores/                    # Pinia stores (data only)
│   ├── conversationsStore.ts
│   ├── privacyStore.ts
│   ├── analyticsStore.ts
│   └── ...
├── services/                  # API calls and business logic
│   ├── agent2agent/
│   │   ├── api/
│   │   │   └── agent2agent.api.ts
│   │   └── utils/
│   │       └── builders/
│   │           ├── build.builder.ts (uses transport types)
│   │           └── plan.builder.ts
│   ├── conversationsService.ts
│   └── ...
├── components/                # Vue components
│   ├── Analytics/
│   │   └── AnalyticsDashboard.vue
│   └── ...
└── types/                     # TypeScript types
    └── ...
```

## Transport Types Reference

All requests must use transport types from `@orchestrator-ai/transport-types`:

```typescript
import type {
  StrictA2ARequest,
  StrictA2ASuccessResponse,
  StrictA2AErrorResponse,
  AgentTaskMode,
  BuildAction,
  PlanAction,
  StrictBuildRequest,
  StrictPlanRequest,
} from '@orchestrator-ai/transport-types';
```

Build requests using builders:
```typescript
import { buildRequest } from '@/services/agent2agent/utils/builders';

// Plan operations
const planRequest = buildRequest.plan.create(
  { conversationId, userMessage },
  { title, content }
);

// Build operations
const buildRequest = buildRequest.build.execute(
  { conversationId, userMessage },
  { planId }
);
```

## Checklist for Front-End Code

When writing front-end code, verify:

- [ ] Store contains ONLY state (ref/computed) and simple setters
- [ ] Store has NO async methods
- [ ] Store has NO API calls
- [ ] Store has NO complex business logic
- [ ] Service handles ALL API calls
- [ ] Service uses transport types when building requests
- [ ] Service updates store after API calls
- [ ] Component calls service methods (not store methods for API)
- [ ] Component reads from store using `computed()` for reactivity
- [ ] Vue reactivity handles UI updates automatically
- [ ] No manual DOM manipulation
- [ ] No `forceUpdate()` or similar hacks

## Related Documentation

- **Architecture Details**: [ARCHITECTURE.md](ARCHITECTURE.md) - Complete architecture patterns
- **Transport Types**: `@orchestrator-ai/transport-types` package
- **A2A Protocol**: See Back-End Structure Skill for A2A compliance

## Troubleshooting

**Problem:** Store changes don't update UI
- **Solution:** Use `computed()` when reading from store in components
- **Solution:** Ensure store uses `ref()` for state (not plain objects)

**Problem:** Agent wants to add methods to store
- **Solution:** Redirect to service layer - explain stores are data-only

**Problem:** API calls fail with type errors
- **Solution:** Use `buildRequest` builders with transport types, not raw fetch

**Problem:** Component doesn't react to store changes
- **Solution:** Check that component uses `computed()` to read from store
- **Solution:** Verify store setters update `ref()` values (not plain assignments)

