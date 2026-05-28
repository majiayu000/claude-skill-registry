---
name: react-component-design
description: Design React components following Tetris architecture guidelines. Use when creating new components, refactoring components, optimizing performance, or improving component structure. Auto-triggers on phrases like "create a component", "refactor this component", "optimize rendering", or "improve component design". Emphasizes component consolidation, unified patterns, and efficient hook usage.
allowed-tools: Read, Edit, Grep, Glob
---

# React Component Design Guide

Design patterns for React components in the Tetris project.

## Core Principles

1. **Component Consolidation**: Prefer unified components over excessive fragmentation
2. **Functional Components**: No class components
3. **Custom Hooks**: Extract reusable logic
4. **Type Aliases**: Use `type` instead of `interface` for props
5. **Dynamic IDs**: Use `useId()` hook for accessibility
6. **Optimized Patterns**: Minimize re-renders and prop drilling

## Component Structure

### Basic Component Template

```typescript
import { useId } from 'react'
import { useTranslation } from 'react-i18next'

type GameButtonProps = {
  onClick: () => void
  label: string
  disabled?: boolean
}

export const GameButton = ({ onClick, label, disabled = false }: GameButtonProps) => {
  const { t } = useTranslation()
  const id = useId()

  return (
    <button
      id={id}
      onClick={onClick}
      disabled={disabled}
      className="game-button"
    >
      {t(label)}
    </button>
  )
}
```

### Component with Custom Hook

```typescript
// Custom hook for game logic
const useGameState = () => {
  const [board, setBoard] = useState<Board>(createBoard())
  const [currentPiece, setCurrentPiece] = useState<Piece | null>(null)
  const [score, setScore] = useState(0)

  const placePiece = useCallback((position: Position) => {
    if (!currentPiece) return

    const result = tryPlacePiece(board, currentPiece, position)
    if (result.ok) {
      setBoard(result.value.board)
      setScore((s) => s + result.value.points)
    }
  }, [board, currentPiece])

  return { board, currentPiece, score, placePiece }
}

// Component using the hook
export const GameBoard = () => {
  const { board, currentPiece, score, placePiece } = useGameState()

  return (
    <div className="game-board">
      <Board data={board} currentPiece={currentPiece} />
      <Score value={score} />
    </div>
  )
}
```

## Design Patterns

### 1. Component Consolidation

```typescript
// ❌ Excessive fragmentation
const Header = () => <div className="header">...</div>
const HeaderTitle = () => <h1>...</h1>
const HeaderSubtitle = () => <p>...</p>
const HeaderActions = () => <div>...</div>

// ✅ Consolidated component
type GameHeaderProps = {
  title: string
  subtitle: string
  actions: ReactNode
}

export const GameHeader = ({ title, subtitle, actions }: GameHeaderProps) => (
  <header className="game-header">
    <div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    <div className="actions">{actions}</div>
  </header>
)
```

### 2. Composition over Props Drilling

```typescript
// ❌ Props drilling
<Game>
  <Board score={score} level={level} />
  <Controls score={score} level={level} />
  <Stats score={score} level={level} />
</Game>

// ✅ Context for shared state
const GameStateContext = createContext<GameState | null>(null)

export const GameProvider = ({ children }: { children: ReactNode }) => {
  const gameState = useGameState()
  return (
    <GameStateContext.Provider value={gameState}>
      {children}
    </GameStateContext.Provider>
  )
}

// Usage
<GameProvider>
  <Board />
  <Controls />
  <Stats />
</GameProvider>
```

### 3. Memoization for Performance

```typescript
// ✅ Memoize expensive components
export const Board = memo(({ cells, currentPiece }: BoardProps) => {
  return (
    <div className="board">
      {cells.map((row, y) => (
        <Row key={y} cells={row} y={y} currentPiece={currentPiece} />
      ))}
    </div>
  )
})

// ✅ Memoize callbacks
const GameControls = () => {
  const { movePiece, rotatePiece } = useGame()

  const handleLeft = useCallback(() => {
    movePiece('LEFT')
  }, [movePiece])

  const handleRotate = useCallback(() => {
    rotatePiece()
  }, [rotatePiece])

  return (
    <div>
      <button onClick={handleLeft}>{t('controls.left')}</button>
      <button onClick={handleRotate}>{t('controls.rotate')}</button>
    </div>
  )
}
```

### 4. Type-safe Props

```typescript
// ✅ Use type aliases (not interface)
type ButtonVariant = 'primary' | 'secondary' | 'danger'

type ButtonProps = {
  variant: ButtonVariant
  size?: 'small' | 'medium' | 'large'
  onClick: () => void
  children: ReactNode
  disabled?: boolean
}

export const Button = ({
  variant,
  size = 'medium',
  onClick,
  children,
  disabled = false
}: ButtonProps) => {
  const className = cn(
    'button',
    `button--${variant}`,
    `button--${size}`,
    disabled && 'button--disabled'
  )

  return (
    <button className={className} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  )
}
```

### 5. Dynamic IDs for Accessibility

```typescript
// ❌ Static IDs
export const FormField = ({ label }: FormFieldProps) => (
  <div>
    <label htmlFor="game-input">{label}</label>
    <input id="game-input" />
  </div>
)

// ✅ Dynamic IDs with useId()
export const FormField = ({ label }: FormFieldProps) => {
  const id = useId()

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} />
    </div>
  )
}
```

## Custom Hooks Best Practices

### 1. Extract Reusable Logic

```typescript
// useKeyPress hook
export const useKeyPress = (targetKey: string, callback: () => void) => {
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === targetKey) {
        callback()
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => {
      window.removeEventListener('keydown', handleKeyPress)
    }
  }, [targetKey, callback])
}

// Usage in component
const GameControls = () => {
  const { movePiece } = useGame()

  useKeyPress('ArrowLeft', () => movePiece('LEFT'))
  useKeyPress('ArrowRight', () => movePiece('RIGHT'))
  useKeyPress(' ', () => movePiece('DROP'))

  return <div>...</div>
}
```

### 2. State Management Hooks

```typescript
// useLocalStorage hook
export const useLocalStorage = <T,>(
  key: string,
  initialValue: T
): [T, (value: T) => void] => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    const item = localStorage.getItem(key)
    return item ? JSON.parse(item) : initialValue
  })

  const setValue = useCallback((value: T) => {
    setStoredValue(value)
    localStorage.setItem(key, JSON.stringify(value))
  }, [key])

  return [storedValue, setValue]
}

// Usage
const [highScore, setHighScore] = useLocalStorage('tetris:highScore', 0)
```

## Component Checklist

- [ ] Functional component (no classes)
- [ ] Type alias for props (not interface)
- [ ] i18n for all user-facing strings
- [ ] useId() for dynamic IDs
- [ ] Custom hooks for reusable logic
- [ ] Memoization where appropriate
- [ ] Minimal prop drilling (use context)
- [ ] Consolidated (not overly fragmented)

## Performance Optimization

```typescript
// ✅ Optimize with memo and useMemo
export const ExpensiveComponent = memo(({ data }: Props) => {
  const processedData = useMemo(() => {
    return expensiveCalculation(data)
  }, [data])

  return <div>{processedData}</div>
})

// ✅ Optimize callbacks with useCallback
const Parent = () => {
  const [count, setCount] = useState(0)

  const increment = useCallback(() => {
    setCount((c) => c + 1)
  }, [])

  return <Child onIncrement={increment} />
}
```

## When This Skill Activates

- "Create a new component"
- "Refactor this component"
- "Optimize component performance"
- "Improve component structure"
- "Extract logic to custom hook"
- "Reduce re-renders"

