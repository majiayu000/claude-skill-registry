---
name: service-ui-components
description: Componentes de UI para serviços seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para Serviços

Esta skill define os componentes Blade específicos para a gestão de serviços no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── service/
│   ├── service-card.blade.php         # Card resumido de serviço
│   ├── service-details.blade.php     # Detalhes completos do serviço
│   ├── service-form.blade.php        # Formulário de criação/edição
│   ├── service-status.blade.php      # Badge de status do serviço
│   ├── service-items.blade.php       # Lista de itens do serviço
│   ├── service-actions.blade.php     # Ações disponíveis para serviço
│   ├── service-filters.blade.php     # Filtros específicos para serviços
│   └── service-totals.blade.php      # Totais e valores do serviço
└── ...
```

## 1. Service Card Component

Componente para exibição resumida de serviços em listas e dashboards.

### Uso Básico

```blade
<x-service.service-card :service="$service" :showCategory="true" :showBudget="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service` | Modelo do serviço | Obrigatório |
| `showCategory` | `bool` | Exibir categoria do serviço | `true` |
| `showBudget` | `bool` | Exibir orçamento vinculado | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'service',
    'showCategory' => true,
    'showBudget' => true,
    'variant' => 'primary'
])

<div class="card border-0 shadow-sm h-100">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center gap-3">
                <div class="avatar-circle bg-{{ $variant }} bg-gradient">
                    <i class="bi bi-tools text-white"></i>
                </div>
                <div>
                    <h6 class="mb-1 fw-bold">{{ $service->category->name }}</h6>
                    <small class="text-muted">{{ $service->created_at->format('d/m/Y') }}</small>
                </div>
            </div>
            <x-service.service-status :service="$service" />
        </div>

        @if($showCategory && $service->category)
            <div class="mb-3">
                <small class="text-muted">Categoria:</small>
                <div class="badge bg-secondary">{{ $service->category->name }}</div>
            </div>
        @endif

        @if($showBudget && $service->budget)
            <div class="mb-3">
                <small class="text-muted">Orçamento:</small>
                <div class="fw-semibold">{{ $service->budget->code }}</div>
            </div>
        @endif

        <div class="d-flex justify-content-between align-items-center">
            <div>
                <small class="text-muted">Valor Total</small>
                <div class="h6 mb-0 fw-bold text-{{ $variant }}">
                    R$ {{ number_format($service->total, 2, ',', '.') }}
                </div>
            </div>

            <div class="btn-group btn-group-sm" role="group">
                <a href="{{ route('provider.services.show', $service) }}" class="btn btn-outline-primary">
                    <i class="bi bi-eye"></i> Ver
                </a>
                <a href="{{ route('provider.services.edit', $service) }}" class="btn btn-outline-secondary">
                    <i class="bi bi-pencil"></i> Editar
                </a>
            </div>
        </div>
    </div>
</div>
```

## 2. Service Details Component

Componente para exibição detalhada de informações do serviço.

### Uso Básico

```blade
<x-service.service-details :service="$service" :showItems="true" :showTotals="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service` | Modelo do serviço | Obrigatório |
| `showItems` | `bool` | Exibir itens do serviço | `true` |
| `showTotals` | `bool` | Exibir totais detalhados | `true` |
| `collapsible` | `bool` | Permitir colapsar seções | `false` |

### Estrutura

```blade
@props([
    'service',
    'showItems' => true,
    'showTotals' => true,
    'collapsible' => false
])

<div class="service-details">
    <!-- Informações Básicas -->
    <div class="row g-3 mb-3">
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Código</label>
                <div class="fw-bold">{{ $service->code }}</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Categoria</label>
                <div class="fw-bold">{{ $service->category->name }}</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Data</label>
                <div class="fw-bold">{{ $service->created_at->format('d/m/Y H:i') }}</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Status</label>
                <x-service.service-status :service="$service" />
            </div>
        </div>
    </div>

    <!-- Descrição -->
    @if($service->description)
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-body">
                        <label class="text-muted small">Descrição</label>
                        <p class="mb-0">{{ $service->description }}</p>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Itens do Serviço -->
    @if($showItems && $service->serviceItems->isNotEmpty())
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Itens do Serviço</h6>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Produto</th>
                                        <th>Quantidade</th>
                                        <th>Valor Unitário</th>
                                        <th>Valor Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    @foreach($service->serviceItems as $item)
                                        <tr>
                                            <td>{{ $item->product->name }}</td>
                                            <td>{{ $item->quantity }}</td>
                                            <td>R$ {{ number_format($item->unit_value, 2, ',', '.') }}</td>
                                            <td class="fw-bold">
                                                R$ {{ number_format($item->quantity * $item->unit_value, 2, ',', '.') }}
                                            </td>
                                        </tr>
                                    @endforeach
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Totais -->
    @if($showTotals)
        <x-service.service-totals :service="$service" />
    @endif
</div>
```

## 3. Service Status Component

Componente para exibição do status do serviço com cores e ícones apropriados.

### Uso Básico

```blade
<x-service.service-status :service="$service" :showIcon="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service` | Modelo do serviço | Obrigatório |
| `showIcon` | `bool` | Exibir ícone ao lado do status | `true` |
| `size` | `string` | Tamanho do badge (sm, md, lg) | `md` |

### Estrutura

```blade
@props([
    'service',
    'showIcon' => true,
    'size' => 'md'
])

@php
    $status = $service->status;
    $metadata = $status->getMetadata();
    $color = $metadata['color'] ?? '#6c757d';
    $icon = $metadata['icon'] ?? 'circle';
    $description = $metadata['description'] ?? $status->value;

    $sizeClass = match($size) {
        'sm' => 'badge-sm',
        'lg' => 'badge-lg',
        default => 'badge-md'
    };
@endphp

<span class="badge modern-badge {{ $sizeClass }}"
      style="background-color: {{ $color }}20; color: {{ $color }}; border: 1px solid {{ $color }}40;">
    @if($showIcon)
        <i class="bi {{ $icon }} me-1"></i>
    @endif
    {{ $description }}
</span>
```

## 4. Service Items Component

Componente para exibição da lista de itens de um serviço.

### Uso Básico

```blade
<x-service.service-items :service="$service" :editable="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service` | Modelo do serviço | Obrigatório |
| `editable` | `bool` | Permitir edição dos itens | `false` |
| `showTotal` | `bool` | Exibir total geral | `true` |

### Estrutura

```blade
@props([
    'service',
    'editable' => false,
    'showTotal' => true
])

<div class="service-items">
    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Descrição</th>
                    <th class="text-center">Quantidade</th>
                    <th class="text-end">Valor Unitário</th>
                    <th class="text-end">Valor Total</th>
                    @if($editable)
                        <th class="text-center">Ações</th>
                    @endif
                </tr>
            </thead>
            <tbody>
                @foreach($service->serviceItems as $item)
                    <tr>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="avatar-circle bg-light me-2">
                                    <i class="bi bi-box text-dark"></i>
                                </div>
                                <div>
                                    <div class="fw-bold">{{ $item->product->name }}</div>
                                    <small class="text-muted">{{ $item->product->code }}</small>
                                </div>
                            </div>
                        </td>
                        <td>
                            <small class="text-muted">{{ $item->product->description ?? 'Sem descrição' }}</small>
                        </td>
                        <td class="text-center">
                            @if($editable)
                                <input type="number"
                                       class="form-control form-control-sm text-center"
                                       value="{{ $item->quantity }}"
                                       min="1"
                                       style="width: 80px;">
                            @else
                                {{ $item->quantity }}
                            @endif
                        </td>
                        <td class="text-end">
                            @if($editable)
                                <input type="text"
                                       class="form-control form-control-sm text-end"
                                       value="{{ number_format($item->unit_value, 2, ',', '.') }}"
                                       style="width: 120px;">
                            @else
                                R$ {{ number_format($item->unit_value, 2, ',', '.') }}
                            @endif
                        </td>
                        <td class="text-end fw-bold">
                            R$ {{ number_format($item->quantity * $item->unit_value, 2, ',', '.') }}
                        </td>
                        @if($editable)
                            <td class="text-center">
                                <button class="btn btn-outline-danger btn-sm" title="Remover item">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </td>
                        @endif
                    </tr>
                @endforeach
            </tbody>
            @if($showTotal)
                <tfoot>
                    <tr class="table-active">
                        <td colspan="{{ $editable ? 4 : 3 }}" class="text-end fw-bold">Total do Serviço:</td>
                        <td class="text-end fw-bold h5">
                            R$ {{ number_format($service->total, 2, ',', '.') }}
                        </td>
                        @if($editable)
                            <td></td>
                        @endif
                    </tr>
                </tfoot>
            @endif
        </table>
    </div>
</div>
```

## 5. Service Form Component

Componente para formulário de criação e edição de serviços.

### Uso Básico

```blade
<x-service.service-form :service="$service ?? null" :categories="$categories" :products="$products" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service|null` | Modelo do serviço (para edição) | `null` |
| `categories` | `Collection` | Categorias disponíveis | Obrigatório |
| `products` | `Collection` | Produtos disponíveis | Obrigatório |
| `budget` | `Budget|null` | Orçamento vinculado | `null` |

### Estrutura

```blade
@props([
    'service' => null,
    'categories' => [],
    'products' => [],
    'budget' => null
])

<div class="service-form">
    <form action="{{ isset($service) ? route('provider.services.update', $service) : route('provider.services.store') }}"
          method="POST"
          id="serviceForm">
        @csrf
        @if(isset($service)) @method('PUT') @endif

        <!-- Informações Básicas -->
        <div class="row g-3 mb-4">
            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Categoria *</label>
                <select name="category_id" class="form-select @error('category_id') is-invalid @enderror" required>
                    <option value="">Selecione uma categoria</option>
                    @foreach($categories as $category)
                        <option value="{{ $category->id }}"
                                {{ (old('category_id', $service->category_id ?? '') == $category->id) ? 'selected' : '' }}>
                            {{ $category->name }}
                        </option>
                    @endforeach
                </select>
                @error('category_id')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>

            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Data de Vencimento</label>
                <input type="date"
                       name="due_date"
                       class="form-control @error('due_date') is-invalid @enderror"
                       value="{{ old('due_date', $service->due_date?->format('Y-m-d') ?? '') }}">
                @error('due_date')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>

            <div class="col-12">
                <label class="form-label small fw-bold text-muted text-uppercase">Descrição</label>
                <textarea name="description"
                          class="form-control @error('description') is-invalid @enderror"
                          rows="3"
                          placeholder="Descreva o serviço...">{{ old('description', $service->description ?? '') }}</textarea>
                @error('description')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>
        </div>

        <!-- Itens do Serviço -->
        <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-transparent border-0">
                <h6 class="mb-0">Itens do Serviço</h6>
            </div>
            <div class="card-body">
                <div id="serviceItems">
                    @if(isset($service) && $service->serviceItems->isNotEmpty())
                        @foreach($service->serviceItems as $item)
                            <div class="row g-3 item-row mb-3" data-item-id="{{ $item->id }}">
                                <div class="col-md-4">
                                    <select name="items[{{ $item->id }}][product_id]"
                                            class="form-select product-select" required>
                                        <option value="">Selecione um produto</option>
                                        @foreach($products as $product)
                                            <option value="{{ $product->id }}"
                                                    {{ $item->product_id == $product->id ? 'selected' : '' }}
                                                    data-price="{{ $product->price }}">
                                                {{ $product->name }} - R$ {{ number_format($product->price, 2, ',', '.') }}
                                            </option>
                                        @endforeach
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <input type="number"
                                           name="items[{{ $item->id }}][quantity]"
                                           class="form-control quantity-input"
                                           placeholder="Qtd"
                                           value="{{ $item->quantity }}"
                                           min="1" required>
                                </div>
                                <div class="col-md-2">
                                    <input type="text"
                                           name="items[{{ $item->id }}][unit_value]"
                                           class="form-control price-input"
                                           placeholder="Valor Unitário"
                                           value="{{ number_format($item->unit_value, 2, ',', '.') }}"
                                           required>
                                </div>
                                <div class="col-md-2">
                                    <input type="text"
                                           class="form-control item-total"
                                           placeholder="Total"
                                           value="R$ {{ number_format($item->quantity * $item->unit_value, 2, ',', '.') }}"
                                           readonly>
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button type="button"
                                            class="btn btn-outline-danger remove-item"
                                            title="Remover item">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </div>
                        @endforeach
                    @else
                        <div class="row g-3 item-row mb-3">
                            <div class="col-md-4">
                                <select name="items[0][product_id]"
                                        class="form-select product-select" required>
                                    <option value="">Selecione um produto</option>
                                    @foreach($products as $product)
                                        <option value="{{ $product->id }}"
                                                data-price="{{ $product->price }}">
                                            {{ $product->name }} - R$ {{ number_format($product->price, 2, ',', '.') }}
                                        </option>
                                    @endforeach
                                </select>
                            </div>
                            <div class="col-md-2">
                                <input type="number"
                                       name="items[0][quantity]"
                                       class="form-control quantity-input"
                                       placeholder="Qtd"
                                       value="1"
                                       min="1" required>
                            </div>
                            <div class="col-md-2">
                                <input type="text"
                                       name="items[0][unit_value]"
                                       class="form-control price-input"
                                       placeholder="Valor Unitário"
                                       required>
                            </div>
                            <div class="col-md-2">
                                <input type="text"
                                       class="form-control item-total"
                                       placeholder="Total"
                                       readonly>
                            </div>
                            <div class="col-md-2 d-flex align-items-end">
                                <button type="button"
                                        class="btn btn-outline-danger remove-item"
                                        title="Remover item">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </div>
                    @endif
                </div>

                <div class="row">
                    <div class="col-12">
                        <button type="button"
                                class="btn btn-outline-primary btn-sm"
                                id="addServiceItem">
                            <i class="bi bi-plus-circle me-2"></i>Adicionar Item
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Totais -->
        <div class="row mb-4">
            <div class="col-md-8"></div>
            <div class="col-md-4">
                <div class="card border-0 bg-light">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="text-muted">Subtotal:</span>
                            <span id="subtotalDisplay">R$ 0,00</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="text-muted">Desconto:</span>
                            <input type="text"
                                   name="discount"
                                   class="form-control form-control-sm text-end"
                                   id="discountInput"
                                   value="{{ old('discount', $service->discount ?? '0') }}"
                                   style="width: 120px; display: inline-block;">
                        </div>
                        <div class="d-flex justify-content-between fw-bold">
                            <span>Total:</span>
                            <span id="totalDisplay" class="h5">R$ 0,00</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Ações -->
        <div class="d-flex justify-content-between">
            <a href="{{ route('provider.services.index') }}" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-2"></i>Cancelar
            </a>
            <button type="submit" class="btn btn-primary">
                <i class="bi bi-check-circle me-2"></i>{{ isset($service) ? 'Atualizar' : 'Criar' }} Serviço
            </button>
        </div>
    </form>
</div>

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Lógica para cálculo de totais
    function calculateTotals() {
        let subtotal = 0;
        document.querySelectorAll('.item-row').forEach(row => {
            const quantity = parseFloat(row.querySelector('.quantity-input').value) || 0;
            const unitValue = parseFloat(row.querySelector('.price-input').value.replace(',', '.')) || 0;
            const total = quantity * unitValue;
            row.querySelector('.item-total').value = 'R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            subtotal += total;
        });

        const discount = parseFloat(document.getElementById('discountInput').value.replace(',', '.')) || 0;
        const total = subtotal - discount;

        document.getElementById('subtotalDisplay').textContent = 'R$ ' + subtotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        document.getElementById('totalDisplay').textContent = 'R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    }

    // Eventos
    document.getElementById('addServiceItem').addEventListener('click', function() {
        const itemsContainer = document.getElementById('serviceItems');
        const itemCount = itemsContainer.children.length;

        const newRow = document.createElement('div');
        newRow.className = 'row g-3 item-row mb-3';
        newRow.innerHTML = `
            <div class="col-md-4">
                <select name="items[${itemCount}][product_id]" class="form-select product-select" required>
                    <option value="">Selecione um produto</option>
                    @foreach($products as $product)
                        <option value="{{ $product->id }}" data-price="{{ $product->price }}">
                            {{ $product->name }} - R$ {{ number_format($product->price, 2, ',', '.') }}
                        </option>
                    @endforeach
                </select>
            </div>
            <div class="col-md-2">
                <input type="number" name="items[${itemCount}][quantity]" class="form-control quantity-input" placeholder="Qtd" value="1" min="1" required>
            </div>
            <div class="col-md-2">
                <input type="text" name="items[${itemCount}][unit_value]" class="form-control price-input" placeholder="Valor Unitário" required>
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control item-total" placeholder="Total" readonly>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="button" class="btn btn-outline-danger remove-item" title="Remover item">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        `;

        itemsContainer.appendChild(newRow);
        calculateTotals();
    });

    document.getElementById('serviceItems').addEventListener('input', calculateTotals);
    document.getElementById('discountInput').addEventListener('input', calculateTotals);

    // Inicializar cálculos
    calculateTotals();
});
</script>
@endpush
```

## 6. Service Actions Component

Componente para exibição de ações disponíveis para um serviço.

### Uso Básico

```blade
<x-service.service-actions :service="$service" :showSchedule="true" :showInvoice="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service` | Modelo do serviço | Obrigatório |
| `showSchedule` | `bool` | Exibir botão de agendamento | `true` |
| `showInvoice` | `bool` | Exibir botão de fatura | `true` |
| `showPrint` | `bool` | Exibir botão de impressão | `true` |

### Estrutura

```blade
@props([
    'service',
    'showSchedule' => true,
    'showInvoice' => true,
    'showPrint' => true
])

<div class="service-actions btn-group" role="group">
    <!-- Visualizar -->
    <a href="{{ route('provider.services.show', $service) }}"
       class="btn btn-outline-primary"
       title="Visualizar Serviço">
        <i class="bi bi-eye"></i> Visualizar
    </a>

    <!-- Editar -->
    @if($service->status->isEditable())
        <a href="{{ route('provider.services.edit', $service) }}"
           class="btn btn-outline-secondary"
           title="Editar Serviço">
            <i class="bi bi-pencil"></i> Editar
        </a>
    @endif

    <!-- Agendar -->
    @if($showSchedule && $service->status->canSchedule())
        <button type="button"
                class="btn btn-outline-info"
                data-bs-toggle="modal"
                data-bs-target="#scheduleModal-{{ $service->id }}"
                title="Agendar Serviço">
            <i class="bi bi-calendar-plus"></i> Agendar
        </button>
    @endif

    <!-- Faturar -->
    @if($showInvoice && $service->status->canInvoice())
        <button type="button"
                class="btn btn-outline-success"
                data-bs-toggle="modal"
                data-bs-target="#invoiceModal-{{ $service->id }}"
                title="Faturar Serviço">
            <i class="bi bi-receipt"></i> Faturar
        </button>
    @endif

    <!-- Imprimir -->
    @if($showPrint)
        <a href="{{ route('provider.services.pdf', $service) }}"
           class="btn btn-outline-warning"
           target="_blank"
           title="Imprimir Serviço">
            <i class="bi bi-printer"></i> Imprimir
        </a>
    @endif

    <!-- Excluir -->
    @if($service->status->isDeletable())
        <button type="button"
                class="btn btn-outline-danger"
                data-bs-toggle="modal"
                data-bs-target="#deleteModal-{{ $service->id }}"
                title="Excluir Serviço">
            <i class="bi bi-trash"></i> Excluir
        </button>
    @endif
</div>
```

## 7. Service Filters Component

Componente para filtros específicos de listagem de serviços.

### Uso Básico

```blade
<x-service.service-filters :filters="$filters" :showCategory="true" :showStatus="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `filters` | `array` | Filtros atuais | `[]` |
| `showCategory` | `bool` | Exibir filtro por categoria | `true` |
| `showStatus` | `bool` | Exibir filtro por status | `true` |
| `showDateRange` | `bool` | Exibir filtro por período | `true` |

### Estrutura

```blade
@props([
    'filters' => [],
    'showCategory' => true,
    'showStatus' => true,
    'showDateRange' => true
])

<div class="service-filters">
    <form action="{{ request()->url() }}" method="GET" class="row g-3">
        @if($showCategory)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Categoria</label>
                <select name="category_id" class="form-select form-select-sm">
                    <option value="">Todas as categorias</option>
                    @foreach($categories as $category)
                        <option value="{{ $category->id }}"
                                {{ ($filters['category_id'] ?? '') == $category->id ? 'selected' : '' }}>
                            {{ $category->name }}
                        </option>
                    @endforeach
                </select>
            </div>
        @endif

        @if($showStatus)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Status</label>
                <select name="status" class="form-select form-select-sm">
                    <option value="">Todos os status</option>
                    @foreach(\App\Enums\ServiceStatus::cases() as $status)
                        @php $metadata = $status->getMetadata(); @endphp
                        <option value="{{ $status->value }}"
                                {{ ($filters['status'] ?? '') == $status->value ? 'selected' : '' }}>
                            {{ $metadata['description'] }}
                        </option>
                    @endforeach
                </select>
            </div>
        @endif

        @if($showDateRange)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Período</label>
                <div class="input-group input-group-sm">
                    <input type="date"
                           name="start_date"
                           class="form-control"
                           value="{{ $filters['start_date'] ?? '' }}">
                    <span class="input-group-text">até</span>
                    <input type="date"
                           name="end_date"
                           class="form-control"
                           value="{{ $filters['end_date'] ?? '' }}">
                </div>
            </div>
        @endif

        <div class="col-md-3">
            <label class="form-label small fw-bold text-muted text-uppercase">Busca</label>
            <input type="text"
                   name="search"
                   class="form-control form-control-sm"
                   value="{{ $filters['search'] ?? '' }}"
                   placeholder="Buscar por descrição...">
        </div>

        <div class="col-12">
            <div class="d-flex justify-content-between">
                <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-primary btn-sm">
                        <i class="bi bi-search me-2"></i>Filtrar
                    </button>
                    <a href="{{ route('provider.services.index') }}" class="btn btn-outline-secondary btn-sm">
                        <i class="bi bi-x-circle me-2"></i>Limpar
                    </a>
                </div>

                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#createModal">
                        <i class="bi bi-plus-circle me-2"></i>Novo Serviço
                    </button>
                </div>
            </div>
        </div>
    </form>
</div>
```

## 8. Service Totals Component

Componente para exibição detalhada dos totais e valores do serviço.

### Uso Básico

```blade
<x-service.service-totals :service="$service" :showBreakdown="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `service` | `Service` | Modelo do serviço | Obrigatório |
| `showBreakdown` | `bool` | Exibir detalhamento dos valores | `true` |
| `variant` | `string` | Estilo visual (primary, success, etc.) | `primary` |

### Estrutura

```blade
@props([
    'service',
    'showBreakdown' => true,
    'variant' => 'primary'
])

<div class="service-totals">
    @if($showBreakdown)
        <div class="row g-3 mb-3">
            <div class="col-md-4">
                <div class="card border-0">
                    <div class="card-body text-center">
                        <div class="text-muted small">Subtotal</div>
                        <div class="h5 mb-0 fw-bold">
                            R$ {{ number_format($service->serviceItems->sum(fn($item) => $item->quantity * $item->unit_value), 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card border-0">
                    <div class="card-body text-center">
                        <div class="text-muted small">Desconto</div>
                        <div class="h5 mb-0 fw-bold text-danger">
                            - R$ {{ number_format($service->discount, 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card border-0 bg-{{ $variant }} bg-gradient text-white">
                    <div class="card-body text-center">
                        <div class="small">Valor Total</div>
                        <div class="h4 mb-0 fw-bold">
                            R$ {{ number_format($service->total, 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @else
        <div class="card border-0 bg-{{ $variant }} bg-gradient text-white">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <div class="small">Valor Total do Serviço</div>
                        <div class="h3 mb-0 fw-bold">
                            R$ {{ number_format($service->total, 2, ',', '.') }}
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <x-service.service-status :service="$service" />
                    </div>
                </div>
            </div>
        </div>
    @endif
</div>
```

## 9. Integração com Padrões Existentes

### Uso em Views

```blade
{{-- Dashboard --}}
<x-service.service-card :service="$service" />

{{-- Listagem --}}
<x-service.service-details :service="$service" />

{{-- Formulários --}}
<x-service.service-form :service="$service" :categories="$categories" :products="$products" />

{{-- Ações --}}
<x-service.service-actions :service="$service" />
```

### Estilos CSS

```css
/* Service Components Styles */
.service-form .product-select {
    background-image: linear-gradient(45deg, transparent 50%, gray 50%), linear-gradient(135deg, gray 50%, transparent 50%), linear-gradient(to right, #ccc, #ccc);
    background-position: calc(100% - 20px) calc(1px), calc(100% - 15px) calc(1px), calc(100% - 2.5em) 0.5em;
    background-size: 5px 5px, 5px 5px, 1px 1.5em;
    background-repeat: no-repeat;
}

.service-form .price-input {
    text-align: right;
}

.service-form .item-total {
    background-color: #f8f9fa;
    font-weight: bold;
}

.service-actions .btn {
    transition: all 0.2s ease;
}

.service-actions .btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

## 10. JavaScript Interatividade

### Formulário de Serviço

```javascript
// service-form.js
document.addEventListener('DOMContentLoaded', function() {
    // Autocompletar valor unitário baseado no produto selecionado
    document.querySelectorAll('.product-select').forEach(select => {
        select.addEventListener('change', function() {
            const price = this.options[this.selectedIndex].dataset.price;
            const row = this.closest('.item-row');
            const priceInput = row.querySelector('.price-input');
            if (price) {
                priceInput.value = parseFloat(price).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
                // Recalcular totais
                calculateTotals();
            }
        });
    });

    // Remover item
    document.getElementById('serviceItems').addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const row = e.target.closest('.item-row');
            row.remove();
            calculateTotals();
        }
    });

    // Formatar valores monetários
    document.querySelectorAll('.price-input').forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            this.value = value.replace('.', ',');
            calculateTotals();
        });
    });
});
```

## 11. Validação e Segurança

### Autorização

```php
// ServicePolicy.php
public function view(User $user, Service $service)
{
    return $user->tenant_id === $service->tenant_id;
}

public function update(User $user, Service $service)
{
    return $user->tenant_id === $service->tenant_id &&
           $service->status->isEditable();
}

public function delete(User $user, Service $service)
{
    return $user->tenant_id === $service->tenant_id &&
           $service->status->isDeletable();
}

public function createInvoice(User $user, Service $service)
{
    return $user->tenant_id === $service->tenant_id &&
           $service->status->canInvoice();
}
```

### Validations

```blade
{{-- Service Card com validação de permissões --}}
@can('view', $service)
    <x-service.service-card :service="$service" />
@endcan

{{-- Service Actions com validação de status --}}
@can('update', $service)
    @if($service->status->isEditable())
        <x-service.service-actions :service="$service" />
    @endif
@endcan
```

Este padrão de components para serviços garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
