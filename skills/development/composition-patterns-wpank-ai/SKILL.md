---
name: react-composition-patterns
model: standard
---

# React Composition Patterns

Build flexible, maintainable React components using compound components, context providers, and explicit variants. Avoid boolean prop proliferation.

## WHAT

Composition patterns that scale:
- Compound components with shared context
- State/actions/meta context interface for dependency injection
- Explicit variant components over boolean props
- Lifted state in provider components
- Children composition over render props

## WHEN

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible component APIs
- Creating compound components (Card, Dialog, Form, etc.)
- Components need shared state across sibling elements

## KEYWORDS

composition, compound components, context, provider, boolean props, variants, react patterns, component architecture, render props, children

**Source:** Vercel Engineering


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install composition-patterns
```


---

## Core Principle

**Avoid boolean prop proliferation.** Each boolean doubles possible states.

```tsx
// BAD: 4 booleans = 16 possible states
<Composer isThread isDMThread isEditing isForwarding />

// GOOD: Explicit variants, clear intent
<ThreadComposer channelId="abc" />
<EditComposer messageId="xyz" />
```

---

## Pattern 1: Compound Components

Structure complex components with shared context. Consumers compose what they need.

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

// Provider handles state
function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return (
    <ComposerContext value={{ state, actions, meta }}>
      {children}
    </ComposerContext>
  )
}

// Subcomponents access context
function ComposerInput() {
  const { state, actions: { update }, meta: { inputRef } } = use(ComposerContext)
  return (
    <TextInput
      ref={inputRef}
      value={state.input}
      onChangeText={(text) => update(s => ({ ...s, input: text }))}
    />
  )
}

function ComposerSubmit() {
  const { actions: { submit } } = use(ComposerContext)
  return <Button onPress={submit}>Send</Button>
}

// Export as namespace
const Composer = {
  Provider: ComposerProvider,
  Frame: ComposerFrame,
  Input: ComposerInput,
  Submit: ComposerSubmit,
  Header: ComposerHeader,
  Footer: ComposerFooter,
}
```

**Usage:**

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

---

## Pattern 2: Generic Context Interface

Define a contract any provider can implement: `state`, `actions`, `meta`.

```tsx
interface ComposerState {
  input: string
  attachments: Attachment[]
  isSubmitting: boolean
}

interface ComposerActions {
  update: (updater: (state: ComposerState) => ComposerState) => void
  submit: () => void
}

interface ComposerMeta {
  inputRef: React.RefObject<TextInput>
}

interface ComposerContextValue {
  state: ComposerState
  actions: ComposerActions
  meta: ComposerMeta
}
```

**Same UI, different providers:**

```tsx
// Local state provider
function ForwardMessageProvider({ children }) {
  const [state, setState] = useState(initialState)
  return (
    <ComposerContext value={{
      state,
      actions: { update: setState, submit: useForwardMessage() },
      meta: { inputRef: useRef(null) },
    }}>
      {children}
    </ComposerContext>
  )
}

// Global synced state provider  
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)
  return (
    <ComposerContext value={{
      state,
      actions: { update, submit },
      meta: { inputRef: useRef(null) },
    }}>
      {children}
    </ComposerContext>
  )
}
```

Both work with the same `<Composer.Input />` component.

---

## Pattern 3: Explicit Variants

Create named components for each use case instead of boolean modes.

```tsx
// BAD: What does this render?
<Composer
  isThread
  isEditing={false}
  channelId="abc"
  showAttachments
/>

// GOOD: Self-documenting
<ThreadComposer channelId="abc" />
```

**Implementation:**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditComposer({ messageId }: { messageId: string }) {
  return (
    <EditProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditProvider>
  )
}
```

---

## Pattern 4: Lifted State

Components outside the visual hierarchy can access state via provider.

```tsx
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        {/* Composer UI */}
        <Composer.Frame>
          <Composer.Input placeholder="Add a message" />
          <Composer.Footer>
            <Composer.Formatting />
          </Composer.Footer>
        </Composer.Frame>

        {/* Preview OUTSIDE composer but reads its state */}
        <MessagePreview />

        {/* Actions OUTSIDE composer but can submit */}
        <DialogActions>
          <CancelButton />
          <ForwardButton />
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

// Can access context despite being outside Composer.Frame
function ForwardButton() {
  const { actions: { submit } } = use(ComposerContext)
  return <Button onPress={submit}>Forward</Button>
}

function MessagePreview() {
  const { state } = use(ComposerContext)
  return <Preview message={state.input} attachments={state.attachments} />
}
```

**Key insight:** Provider boundary matters, not visual nesting.

---

## Pattern 5: Children Over Render Props

Use children for composition, render props only when passing data.

```tsx
// BAD: Render props for structure
<Composer
  renderHeader={() => <CustomHeader />}
  renderFooter={() => <Formatting />}
  renderActions={() => <Submit />}
/>

// GOOD: Children for structure
<Composer.Frame>
  <CustomHeader />
  <Composer.Input />
  <Composer.Footer>
    <Formatting />
    <Submit />
  </Composer.Footer>
</Composer.Frame>
```

**When render props ARE appropriate:**

```tsx
// Passing data to children
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

---

## Pattern 6: Decouple State from UI

Only the provider knows how state is managed. UI consumes the interface.

```tsx
// BAD: UI coupled to state implementation
function ChannelComposer({ channelId }) {
  const state = useGlobalChannelState(channelId)  // Knows about global state
  const { submit } = useChannelSync(channelId)    // Knows about sync
  
  return <Composer.Input value={state.input} onChange={...} />
}

// GOOD: State isolated in provider
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)
  
  return (
    <Composer.Provider
      state={state}
      actions={{ update, submit }}
      meta={{ inputRef: useRef(null) }}
    >
      {children}
    </Composer.Provider>
  )
}

// UI only knows the interface
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />  {/* Works with any provider */}
      <Composer.Submit />
    </Composer.Frame>
  )
}
```

---

## Quick Reference

| Anti-Pattern | Solution |
|--------------|----------|
| Boolean props | Explicit variant components |
| Render props for structure | Children composition |
| State in component | Lift to provider |
| Coupled to state impl | Generic context interface |
| Many conditional renders | Compose pieces explicitly |

---

## Files

- `rules/architecture-avoid-boolean-props.md` - Detailed boolean prop guidance
- `rules/architecture-compound-components.md` - Compound component pattern
- `rules/state-context-interface.md` - Context interface design
- `rules/state-decouple-implementation.md` - State isolation
- `rules/state-lift-state.md` - Provider pattern
- `rules/patterns-explicit-variants.md` - Variant components
- `rules/patterns-children-over-render-props.md` - Composition over callbacks

---

## NEVER

- Add boolean props to customize behavior (use composition)
- Create components with more than 2-3 boolean mode props
- Couple UI components to specific state implementations
- Use render props when children would work
- Trap state inside components when siblings need access
