---
name: reusable-components
description: "Biblioteca de componentes Blade do sistema Easy Budget. Use esta skill sempre que precisar gerar interfaces (UI), formulários, tabelas, modais ou dashboards. Ela garante que o código gerado siga o padrão visual do projeto, utilizando a sintaxe <x-componente> em vez de HTML/Bootstrap puro"
---

# Diretrizes de UI do Easy Budget (Laravel Blade Components)

Você deve atuar como um especialista em Frontend para o sistema Easy Budget. **Sempre dê preferência ao uso destes componentes Blade (`<x-nome-do-componente>`)** em vez de escrever HTML ou classes Bootstrap puras.

---

## 📦 1. Componentes Base (Estrutura e Navegação)

### Botões (`x-button`)
Use para ações, links e submissões.
- **Props:** `variant` (primary, secondary, danger, success), `outline` (bool), `icon` (bi-*), `size` (sm, lg), `type` (button, link, submit), `href`, `label`.
- **Exemplo:** `<x-button variant="primary" icon="plus" label="Novo" />`

### Cabeçalho de Página (`x-page-header`)
Use no topo de todas as páginas principais.
- **Props:** `title`, `icon`, `breadcrumbItems` (array ['Nome' => 'Rota']).
- **Exemplo:**
```blade
<x-page-header title="Produtos" icon="box" :breadcrumb-items="['Dashboard' => route('dashboard'), 'Produtos' => '#']" />