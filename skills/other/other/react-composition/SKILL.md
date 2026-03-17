---
name: react-composition
model: standard
description:
  React composition patterns for scalable component architecture. Use when
  refactoring components with boolean prop proliferation, building flexible
  component libraries, designing reusable component APIs, or working with
  compound components and context providers.
version: "1.0"
---

# React Composition Patterns

Composition patterns for building flexible, maintainable React components. Avoid
boolean prop proliferation by using compound components, lifting state, and
composing internals. These patterns make codebases easier to work with as they
scale.

## When to Apply

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible component APIs
- Working with compound components or context providers

## Pattern Overview

| # | Pattern                    | Impact   |
|---|----------------------------|----------|
| 1 | Avoid Boolean Props        | CRITICAL |
| 2 | Compound Components        | HIGH     |
| 3 | Context Interface (DI)     | HIGH     |
| 4 | State Lifting              | HIGH     |
| 5 | Explicit Variants          | MEDIUM   |
| 6 | Children Over Render Props | MEDIUM   |


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-composition
```


---

## 1. Avoid Boolean Prop Proliferation

Don't add boolean props like `isThread`, `isEditing`, `isDMThread` to customize
behavior. Each boolean doubles possible states and creates unmaintainable
conditional logic. Use composition instead.

```tsx
// BAD — boolean props create exponential complexity
function Composer({ isThread, isDMThread, isEditing, isForwarding }: Props) {
  return (
    <form>
      <Input />
      {isDMThread ? <AlsoSendToDMField /> : isThread ? <AlsoSendToChannelField /> : null}
      {isEditing ? <EditActions /> : isForwarding ? <ForwardActions /> : <DefaultActions />}
    </form>
  )
}

// GOOD — composition eliminates conditionals
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer><Composer.Attachments /><Composer.Submit /></Composer.Footer>
    </Composer.Frame>
  )
}

function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer><Composer.Submit /></Composer.Footer>
    </Composer.Frame>
  )
}
```

Each variant is explicit about what it renders. Shared internals without a
monolithic parent.

## 2. Compound Components

Structure complex components with shared context. Each subcomponent accesses
state via context, not props. Export as a namespace object.

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return <ComposerContext value={{ state, actions, meta }}>{children}</ComposerContext>
}
function ComposerInput() {
  const { state, actions: { update }, meta: { inputRef } } = use(ComposerContext)
  return <TextInput ref={inputRef} value={state.input}
    onChangeText={(t) => update((s) => ({ ...s, input: t }))} />
}

const Composer = {
  Provider: ComposerProvider, Frame: ComposerFrame,
  Input: ComposerInput, Submit: ComposerSubmit, Footer: ComposerFooter,
}

// Consumers compose exactly what they need
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Footer><Composer.Formatting /><Composer.Submit /></Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

## 3. Generic Context Interface (Dependency Injection)

Define a generic interface with `state`, `actions`, and `meta`. Any provider
implements this contract — enabling the same UI to work with different state
implementations. The provider is the only place that knows how state is managed.

```tsx
interface ComposerContextValue {
  state: { input: string; attachments: Attachment[]; isSubmitting: boolean }
  actions: { update: (fn: (s: ComposerState) => ComposerState) => void; submit: () => void }
  meta: { inputRef: React.RefObject<TextInput> }
}

// Provider A: Local state for ephemeral forms
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  return (
    <ComposerContext value={{ state, actions: { update: setState, submit: useForwardMessage() },
      meta: { inputRef: useRef(null) } }}>{children}</ComposerContext>
  )
}

// Provider B: Global synced state for channels
function ChannelProvider({ channelId, children }: Props) {
  const { state, update, submit } = useGlobalChannel(channelId)
  return (
    <ComposerContext value={{ state, actions: { update, submit },
      meta: { inputRef: useRef(null) } }}>{children}</ComposerContext>
  )
}
```

Swap the provider, keep the UI. Same `Composer.Input` works with both.

## 4. Lift State into Providers

Move state into dedicated provider components so sibling components outside the
main UI can access and modify state without prop drilling or refs.

```tsx
// BAD — state trapped inside component; siblings can't access it
function ForwardMessageComposer() {
  const [state, setState] = useState(initialState)
  return <Composer.Frame><Composer.Input /><Composer.Footer /></Composer.Frame>
}
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview />        {/* Can't access composer state */}
      <ForwardButton />         {/* Can't call submit */}
    </Dialog>
  )
}

// GOOD — state lifted to provider; any descendant can access it
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const submit = useForwardMessage()
  return (
    <Composer.Provider state={state} actions={{ update: setState, submit }}
      meta={{ inputRef: useRef(null) }}>{children}</Composer.Provider>
  )
}
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview />       {/* Reads state from context */}
        <ForwardButton />        {/* Calls submit from context */}
      </Dialog>
    </ForwardMessageProvider>
  )
}
function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>Forward</Button>
}
```

**Key insight:** Components that need shared state don't have to be visually
nested — they just need to be within the same provider.

## 5. Explicit Variant Components

Instead of one component with many boolean props, create explicit variants.
Each composes the pieces it needs — self-documenting, no impossible states.

```tsx
// BAD — what does this render?
<Composer isThread isEditing={false} channelId="abc" showAttachments showFormatting={false} />

// GOOD — immediately clear
<ThreadComposer channelId="abc" />
<EditMessageComposer messageId="xyz" />
<ForwardMessageComposer messageId="123" />
```

Each variant is explicit about its provider/state, UI elements, and actions.

## 6. Children Over Render Props

Use `children` for composition instead of `renderX` props. Children are more
readable and compose naturally.

```tsx
// BAD — render props
<Composer
  renderHeader={() => <CustomHeader />}
  renderFooter={() => <><Formatting /><Emojis /></>}
/>

// GOOD — children composition
<Composer.Frame>
  <CustomHeader />
  <Composer.Input />
  <Composer.Footer><Composer.Formatting /><SubmitButton /></Composer.Footer>
</Composer.Frame>
```

**When render props are appropriate:** When the parent needs to pass data back
(e.g., `renderItem={({ item, index }) => ...}`).

## Decision Guide

1. **Component has 3+ boolean props?** → Extract explicit variants (1, 5)
2. **Component has render props?** → Convert to compound components (2, 6)
3. **Siblings need shared state?** → Lift state to provider (4)
4. **Same UI, different data sources?** → Generic context interface (3)
5. **Building a component library?** → Apply all patterns together
