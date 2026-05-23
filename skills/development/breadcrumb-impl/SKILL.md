---
name: breadcrumb-impl
description: Guia implementação de breadcrumb de navegação hierárquica seguindo padrões de acessibilidade WCAG e design system do Ultrathink
allowed-tools: [Read, Edit, Write]
---

# Breadcrumb Implementation Skill - Ultrathink

## Objetivo

Esta skill ativa automaticamente ao implementar **sistema de breadcrumb** (navegação hierárquica) no Ultrathink, garantindo:

- Estrutura semântica correta (HTML5 + ARIA)
- Acessibilidade WCAG 2.1 AA
- Design responsivo
- Integração com React Router (quando implementado)

## Especificação (US-061)

**User Story:** Implementar Sistema de Breadcrumb
**Complexidade:** 8 pontos
**Sprint:** 2.4
**Prioridade:** 🟠 P1

### Critérios de Aceite

✅ Posicionado no topo da página (abaixo do header)
✅ Formato: `Hub > Curso de Bash > Aula 1.1`
✅ Cada item é clicável (exceto o atual)
✅ Item atual em negrito
✅ Separador: `>` ou `/`
✅ Responsivo: colapsa em mobile para `... > Aula 1.1`
✅ Acessibilidade: `aria-label="Breadcrumb"`, `aria-current="page"`

## Estrutura HTML Semântica

```jsx
<nav aria-label="Breadcrumb" className="breadcrumb-container">
  <ol className="breadcrumb-list">
    <li className="breadcrumb-item">
      <a href="#" onClick={handleHome}>
        🏠 Hub
      </a>
    </li>
    <li className="breadcrumb-separator" aria-hidden="true">
      <span>></span>
    </li>
    <li className="breadcrumb-item">
      <a href="#" onClick={handleCourse}>
        📖 Curso de Bash
      </a>
    </li>
    <li className="breadcrumb-separator" aria-hidden="true">
      <span>></span>
    </li>
    <li className="breadcrumb-item">
      <span aria-current="page" className="current">
        📝 Aula 1.1
      </span>
    </li>
  </ol>
</nav>
```

## Componente React

**Criar:** `src/components/shared/Breadcrumb.jsx`

```jsx
import React from 'react'
import { ChevronRight } from 'lucide-react'

/**
 * Breadcrumb - Navegação hierárquica acessível
 *
 * @param {Array} items - Array de objetos: [{label, icon, onClick, current}]
 * @param {string} separator - Separador visual (default: ">")
 * @param {boolean} collapse - Colapsar em mobile (default: true)
 */
export function Breadcrumb({ items, separator = '>', collapse = true }) {
  if (!items || items.length === 0) return null

  return (
    <nav
      aria-label="Breadcrumb"
      className="px-6 py-3 bg-white/80 backdrop-blur-sm border-b border-slate-200"
    >
      <ol className="flex items-center flex-wrap gap-2 text-sm">
        {items.map((item, index) => {
          const isLast = index === items.length - 1
          const isFirst = index === 0

          // Mobile: Mostrar apenas último item se collapse ativo
          const hiddenOnMobile = collapse && !isLast && items.length > 2

          return (
            <React.Fragment key={index}>
              <li
                className={`
                  breadcrumb-item
                  ${hiddenOnMobile ? 'hidden md:flex' : 'flex'}
                  items-center gap-2
                `}
              >
                {isLast ? (
                  // Último item: não clicável, em negrito
                  <span
                    aria-current="page"
                    className="font-semibold text-slate-900"
                  >
                    {item.icon && <span className="inline-block mr-1">{item.icon}</span>}
                    {item.label}
                  </span>
                ) : (
                  // Item clicável
                  <button
                    onClick={item.onClick}
                    className="
                      flex items-center gap-1
                      text-slate-600 hover:text-purple-600
                      transition-colors duration-200
                      hover:underline
                      focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2
                      rounded-sm px-1
                    "
                    aria-label={`Navegar para ${item.label}`}
                  >
                    {item.icon && <span>{item.icon}</span>}
                    <span>{item.label}</span>
                  </button>
                )}
              </li>

              {/* Separador */}
              {!isLast && (
                <li
                  aria-hidden="true"
                  className={`
                    text-slate-400
                    ${hiddenOnMobile ? 'hidden md:block' : 'block'}
                  `}
                >
                  {typeof separator === 'string' ? (
                    <span className="text-sm">{separator}</span>
                  ) : (
                    <ChevronRight className="w-4 h-4" />
                  )}
                </li>
              )}

              {/* Mobile: Mostrar "..." antes do último item */}
              {collapse && isFirst && items.length > 2 && (
                <li className="md:hidden text-slate-400" aria-hidden="true">
                  <span>...</span>
                </li>
              )}
            </React.Fragment>
          )
        })}
      </ol>
    </nav>
  )
}
```

## Uso nos Componentes

### Nível 2: Curso (Learning System)

```jsx
// BashLearningSystem.jsx
import { Breadcrumb } from '../shared/Breadcrumb'

export function BashLearningSystem({ onBack }) {
  const breadcrumbItems = [
    {
      label: 'Hub',
      icon: '🏠',
      onClick: onBack
    },
    {
      label: 'Curso de Bash',
      icon: '📖',
      current: true
    }
  ]

  return (
    <div>
      <Breadcrumb items={breadcrumbItems} />
      {/* Resto do componente */}
    </div>
  )
}
```

### Nível 3: Aula (Notes View)

```jsx
// BashNotesView.jsx
import { Breadcrumb } from '../shared/Breadcrumb'

export function BashNotesView({
  moduleTitle,
  onBackToCourse,
  onBackToHub
}) {
  const breadcrumbItems = [
    {
      label: 'Hub',
      icon: '🏠',
      onClick: onBackToHub
    },
    {
      label: 'Curso de Bash',
      icon: '📖',
      onClick: onBackToCourse
    },
    {
      label: moduleTitle || 'Aula',
      icon: '📝',
      current: true
    }
  ]

  return (
    <div>
      <Breadcrumb items={breadcrumbItems} />
      {/* Resto do componente */}
    </div>
  )
}
```

### Nível 4: Modal Flash Cards

```jsx
// FlashcardModal.jsx
import { Breadcrumb } from '../shared/Breadcrumb'

export function FlashcardModal({
  technology,
  section,
  onClose
}) {
  const breadcrumbItems = [
    {
      label: 'Hub',
      icon: '🏠',
      onClick: () => {} // Desabilitado em modal
    },
    {
      label: `Curso de ${technology}`,
      icon: '📖',
      onClick: () => {} // Desabilitado em modal
    },
    {
      label: `Praticando: ${section}`,
      icon: '💡',
      current: true
    }
  ]

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <Breadcrumb
          items={breadcrumbItems}
          collapse={true}
        />
        {/* Cards */}
      </div>
    </div>
  )
}
```

## Variações de Design

### Com Ícone Lucide React

```jsx
import { Home, BookOpen, FileText } from 'lucide-react'

const breadcrumbItems = [
  { label: 'Hub', icon: <Home className="w-4 h-4" />, onClick: handleHome },
  { label: 'Curso', icon: <BookOpen className="w-4 h-4" />, onClick: handleCourse },
  { label: 'Aula', icon: <FileText className="w-4 h-4" />, current: true }
]
```

### Com Separador Customizado

```jsx
<Breadcrumb
  items={breadcrumbItems}
  separator={<ChevronRight className="w-3 h-3 text-slate-400" />}
/>
```

### Sem Colapso Mobile

```jsx
<Breadcrumb
  items={breadcrumbItems}
  collapse={false}
/>
```

## Acessibilidade (WCAG 2.1 AA)

### Estrutura Semântica

✅ **`<nav>` com `aria-label="Breadcrumb"`**: Identifica região de navegação
✅ **`<ol>` ao invés de `<ul>`**: Lista ordenada (sequência importa)
✅ **`<li>` para cada item**: Estrutura de lista semântica
✅ **`aria-current="page"`**: Marca item atual
✅ **`aria-hidden="true"` nos separadores**: Esconde de screen readers

### Navegação por Teclado

✅ **Tab**: Navega entre items clicáveis
✅ **Enter/Space**: Ativa link
✅ **Focus visível**: Ring de foco em botões

### Screen Readers

**NVDA/JAWS leitura esperada:**

```
"Breadcrumb navigation
Link: Home
Link: Curso de Bash
Current page: Aula 1.1"
```

## Responsividade

### Desktop (≥768px)

```
🏠 Hub > 📖 Curso de Bash > 📝 Aula 1.1: Introdução ao Shell
```

### Tablet (≥640px)

```
🏠 Hub > 📖 Bash > 📝 Aula 1.1
```

### Mobile (<640px)

```
... > 📝 Aula 1.1
```

## Testes

### Testes Unitários

```jsx
// Breadcrumb.test.jsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Breadcrumb } from './Breadcrumb'

describe('Breadcrumb', () => {
  const mockItems = [
    { label: 'Home', icon: '🏠', onClick: jest.fn() },
    { label: 'Curso', icon: '📖', onClick: jest.fn() },
    { label: 'Aula', icon: '📝', current: true }
  ]

  it('renderiza todos os items', () => {
    render(<Breadcrumb items={mockItems} />)
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Curso')).toBeInTheDocument()
    expect(screen.getByText('Aula')).toBeInTheDocument()
  })

  it('marca último item com aria-current', () => {
    render(<Breadcrumb items={mockItems} />)
    const currentItem = screen.getByText('Aula')
    expect(currentItem).toHaveAttribute('aria-current', 'page')
  })

  it('chama onClick ao clicar em item', async () => {
    const user = userEvent.setup()
    render(<Breadcrumb items={mockItems} />)

    const homeButton = screen.getByRole('button', { name: /Home/i })
    await user.click(homeButton)

    expect(mockItems[0].onClick).toHaveBeenCalledTimes(1)
  })

  it('item atual não é clicável', () => {
    render(<Breadcrumb items={mockItems} />)
    const currentItem = screen.getByText('Aula')
    expect(currentItem.tagName).toBe('SPAN')
  })

  it('exibe separadores entre items', () => {
    render(<Breadcrumb items={mockItems} separator=">" />)
    const separators = screen.getAllByText('>')
    expect(separators).toHaveLength(2) // Entre 3 items
  })
})
```

### Teste E2E com Playwright

```javascript
// breadcrumb.spec.js
test('breadcrumb navigation', async ({ page }) => {
  await page.goto('http://localhost:3000')

  // Navegar para curso
  await page.click('text=Bash')
  await expect(page.locator('nav[aria-label="Breadcrumb"]')).toBeVisible()
  await expect(page.locator('text=Hub')).toBeVisible()

  // Clicar em breadcrumb para voltar
  await page.click('nav[aria-label="Breadcrumb"] >> text=Hub')
  await expect(page).toHaveURL('http://localhost:3000')
})
```

## Integração com React Router (Futuro)

Quando US-040 (React Router) for implementado:

```jsx
import { Link, useLocation } from 'react-router-dom'

export function Breadcrumb({ items }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol>
        {items.map((item, index) => (
          <li key={index}>
            {item.current ? (
              <span aria-current="page">{item.label}</span>
            ) : (
              <Link to={item.path}>{item.label}</Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}
```

## Referências

- **PRODUCT-CENTRAL-DOCUMENT.md**: US-061 (Implementar Breadcrumb)
- **WCAG 2.1**: [Breadcrumb Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/)
- **MDN**: [aria-current](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-current)

## Ativação Automática

Esta skill ativa quando você:
- Implementa US-061 (Sistema de Breadcrumb)
- Trabalha com navegação hierárquica
- Cria componente `Breadcrumb.jsx`
- Adiciona breadcrumb a Learning Systems
- Testa acessibilidade de navegação
