---
name: frontend-view-pattern
description: Garante padrões consistentes de views Blade no Easy Budget (Dashboard, Index, Create, Edit, Show).
---

# Padrões de Views Blade do Easy Budget

Esta skill define os padrões obrigatórios para criação de views Blade no sistema Easy Budget, garantindo consistência visual, UX padronizada e manutenibilidade.

## Estrutura de Views por Tipo

```
resources/views/pages/[module]/
├── index.blade.php      # Listagem com filtros e tabela
├── create.blade.php     # Formulário de criação
├── edit.blade.php       # Formulário de edição
├── show.blade.php       # Visualização de detalhes
└── dashboard.blade.php  # Dashboard com métricas
```

## 1. DASHBOARD Pattern

### Cabeçalho Responsivo

```blade
<div class="mb-4">
    <div class="d-flex justify-content-between align-items-start mb-2">
        <div class="flex-grow-1">
            <h1 class="h4 h3-md mb-1">
                <i class="bi bi-[icone] me-2"></i>
                <span class="d-none d-sm-inline">Dashboard de [Módulo]</span>
                <span class="d-sm-none">[Módulo]</span>
            </h1>
        </div>
        <nav aria-label="breadcrumb" class="d-none d-md-block">
            <ol class="breadcrumb mb-0">
                <li class="breadcrumb-item"><a href="{{ route('provider.dashboard') }}">Dashboard</a></li>
                <li class="breadcrumb-item active">Dashboard de [Módulo]</li>
            </ol>
        </nav>
    </div>
    <p class="text-muted mb-0 small">Descrição contextual do dashboard</p>
</div>
```

### Cards de Métricas (4 colunas)

```blade
<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex flex-column justify-content-between">
                <div class="d-flex align-items-center mb-3">
                    <div class="avatar-circle bg-primary bg-gradient me-3">
                        <i class="bi bi-[icone] text-white"></i>
                    </div>
                    <div>
                        <h6 class="text-muted mb-1">Título da Métrica</h6>
                        <h3 class="mb-0">{{ $valor }}</h3>
                    </div>
                </div>
                <p class="text-muted small mb-0">Descrição da métrica</p>
            </div>
        </div>
    </div>
    <!-- Repetir para outras métricas (max 4) -->
</div>
```

### Cores de Avatar

| Classe | Uso |
|--------|-----|
| `bg-primary` | Métrica principal/total |
| `bg-success` | Métricas positivas/ativas |
| `bg-secondary` | Métricas neutras/inativas |
| `bg-info` | Métricas de análise/percentuais |
| `bg-warning` | Métricas de atenção |
| `bg-danger` | Métricas críticas |

### Layout 8-4 (Conteúdo + Sidebar)

```blade
<div class="row g-4">
    <!-- Conteúdo Principal (8 colunas) -->
    <div class="col-lg-8">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-transparent border-0">
                <h5 class="mb-0"><i class="bi bi-[icone] me-2"></i>Título</h5>
            </div>
            <div class="card-body p-0">
                <!-- Desktop Table -->
                <div class="desktop-view">
                    <div class="table-responsive">
                        <table class="modern-table table mb-0">
                            <!-- conteúdo da tabela -->
                        </table>
                    </div>
                </div>
                <!-- Mobile List -->
                <div class="mobile-view">
                    <div class="list-group">
                        <!-- conteúdo da lista mobile -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Sidebar (4 colunas) -->
    <div class="col-lg-4">
        <!-- Insights -->
        <div class="card border-0 shadow-sm mb-3">
            <div class="card-header bg-transparent border-0">
                <h6 class="mb-0"><i class="bi bi-lightbulb me-2"></i>Insights Rápidos</h6>
            </div>
            <div class="card-body">
                <ul class="list-unstyled mb-0 small text-muted">
                    <li class="mb-2"><i class="bi bi-[icone] text-primary me-2"></i>Dica</li>
                </ul>
            </div>
        </div>

        <!-- Atalhos -->
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-transparent border-0">
                <h6 class="mb-0"><i class="bi bi-link-45deg me-2"></i>Atalhos</h6>
            </div>
            <div class="card-body d-grid gap-2">
                <a href="{{ route('modulo.create') }}" class="btn btn-sm btn-success">
                    <i class="bi bi-plus-circle me-2"></i>Novo Item
                </a>
            </div>
        </div>
    </div>
</div>
```

## 2. INDEX (Listagem) Pattern

```blade
<x-page-container>
    <x-page-header title="[Recurso]" icon="[icone]" :breadcrumb-items="[... ]" />

    <x-filter-form ...>
        <!-- Campos de filtro -->
    </x-filter-form>

    <x-resource-list-card
        title="Lista de [Recurso]"
        mobileTitle="[Recurso]"
        icon="[icone]"
        :total="$items->total()"
    >
        <x-slot:headerActions>
            <x-table-header-actions resource="[recurso]" :filters="$filters" />
        </x-slot:headerActions>

        <x-slot:desktop>
            <x-resource-table>
                <x-slot:thead>
                    <tr><th>Coluna</th><th class="text-center">Ações</th></tr>
                </x-slot:thead>
                <x-slot:tbody>
                    @foreach($items as $item)
                        <tr>
                            <td>{{ $item->name }}</td>
                            <x-table-actions>
                                <x-action-buttons :item="$item" resource="[recurso]" />
                            </x-table-actions>
                        </tr>
                    @endforeach
                </x-slot:tbody>
            </x-resource-table>
        </x-slot:desktop>

        <x-slot:mobile>
            @foreach($items as $item)
                <x-resource-mobile-item icon="[icone]">
                    {{ $item->name }}
                    <x-slot:actions>
                        <x-table-actions mobile>
                            <x-action-buttons :item="$item" resource="[recurso]" size="sm" />
                        </x-table-actions>
                    </x-slot:actions>
                </x-resource-mobile-item>
            @endforeach
        </x-slot:mobile>

        <x-slot:footer>
            {{ $items->links() }}
        </x-slot:footer>
    </x-resource-list-card>
</x-page-container>
```

## 3. CREATE/EDIT Pattern

### Cabeçalho

```blade
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h1 class="h3 mb-0">
            <i class="bi bi-[icone-especifico] me-2"></i>{{ isset($item) ? 'Editar' : 'Novo' }} [Item]
        </h1>
        <p class="text-muted mb-0">Preencha os dados para {{ isset($item) ? 'atualizar' : 'criar' }} um [item]</p>
    </div>
    <nav aria-label="breadcrumb" class="d-none d-md-block">
        <ol class="breadcrumb mb-0">
            <li class="breadcrumb-item"><a href="{{ route('provider.dashboard') }}">Dashboard</a></li>
            <li class="breadcrumb-item"><a href="{{ route('modulo.index') }}">[Módulo]</a></li>
            <li class="breadcrumb-item active" aria-current="page">{{ isset($item) ? 'Editar' : 'Novo' }}</li>
        </ol>
    </nav>
</div>
```

### Campos de Formulário

```blade
<div class="card border-0 shadow-sm">
    <div class="card-body p-4">
        <form action="{{ isset($item) ? route('modulo.update', $item) : route('modulo.store') }}" method="POST">
            @csrf
            @if(isset($item)) @method('PUT') @endif

            <div class="mb-3">
                <label for="name" class="form-label small fw-bold text-muted text-uppercase">Nome *</label>
                <input type="text"
                    class="form-control @error('name') is-invalid @enderror"
                    id="name" name="name"
                    value="{{ old('name', $item->name ?? '') }}" required>
                @error('name')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>

            <div class="d-flex justify-content-between">
                <a href="{{ route('modulo.index') }}" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-left me-2"></i>Cancelar
                </a>
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-check-circle me-2"></i>{{ isset($item) ? 'Atualizar' : 'Criar' }}
                </button>
            </div>
        </form>
    </div>
</div>
```

## 4. Ícones por Contexto

| Contexto | Ícone Bootstrap |
|----------|----------------|
| Cliente PF | `bi-person-plus` |
| Cliente PJ | `bi-building-add` |
| Produto | `bi-bag-plus` |
| Categoria | `bi-folder-plus` |
| Orçamento | `bi-file-earmark-text` |
| Fatura | `bi-receipt` |
| Serviço | `bi-tools` |
| Dashboard | `bi-speedometer2` |
| Relatório | `bi-clipboard-data` |
| Novo/Criar | `bi-plus-circle` |

## 5. Breadcrumb Obrigatório

```blade
<nav aria-label="breadcrumb" class="d-none d-md-block">
    <ol class="breadcrumb mb-0">
        <li class="breadcrumb-item"><a href="{{ route('provider.dashboard') }}">Dashboard</a></li>
        <li class="breadcrumb-item"><a href="{{ route('modulo.index') }}">[Módulo]</a></li>
        <li class="breadcrumb-item active" aria-current="page">[Ação]</li>
    </ol>
</nav>
```

## 6. Responsividade Obrigatória

- Usar classes `d-none d-sm-inline` para mostrar em desktop
- Usar classes `d-sm-none` para ocultar em desktop
- Tables: sempre usar `table-responsive`
- Mobile: implementar `mobile-view` com `list-group`
