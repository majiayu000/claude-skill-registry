---
name: product-ui-components
description: Componentes de UI para produtos seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para Produtos

Esta skill define os componentes Blade específicos para a gestão de produtos no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── product/
│   ├── product-card.blade.php        # Card resumido de produto
│   ├── product-details.blade.php     # Detalhes completos do produto
│   ├── product-form.blade.php        # Formulário de criação/edição
│   ├── product-status.blade.php      # Badge de status do produto
│   ├── product-inventory.blade.php   # Informações de estoque
│   ├── product-actions.blade.php     # Ações disponíveis para produto
│   ├── product-filters.blade.php     # Filtros específicos para produtos
│   ├── product-pricing.blade.php     # Informações de preço
│   ├── product-image.blade.php       # Exibição de imagem do produto
│   └── product-summary.blade.php     # Resumo do produto
└── ...
```

## 1. Product Card Component

Componente para exibição resumida de produtos em listas e dashboards.

### Uso Básico

```blade
<x-product.product-card :product="$product" :showCategory="true" :showStock="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showCategory` | `bool` | Exibir categoria do produto | `true` |
| `showStock` | `bool` | Exibir quantidade em estoque | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'product',
    'showCategory' => true,
    'showStock' => true,
    'variant' => 'primary'
])

<div class="card border-0 shadow-sm h-100">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center gap-3">
                <div class="avatar-circle bg-{{ $variant }} bg-gradient">
                    @if($product->image)
                        <img src="{{ asset('storage/' . $product->image) }}" alt="{{ $product->name }}" class="w-100 h-100 object-fit-cover rounded">
                    @else
                        <i class="bi bi-box text-white"></i>
                    @endif
                </div>
                <div>
                    <h6 class="mb-1 fw-bold">{{ $product->name }}</h6>
                    @if($product->code)
                        <small class="text-muted">Código: {{ $product->code }}</small>
                    @endif
                </div>
            </div>
            <x-product.product-status :product="$product" />
        </div>

        @if($showCategory && $product->category)
            <div class="mb-3">
                <span class="badge bg-secondary">{{ $product->category->name }}</span>
            </div>
        @endif

        <div class="mb-3">
            <small class="text-muted">Preço de Venda</small>
            <div class="fw-bold text-{{ $variant }}">
                R$ {{ number_format($product->price, 2, ',', '.') }}
            </div>
        </div>

        @if($showStock)
            <x-product.product-inventory :product="$product" />
        @endif

        <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
                <small class="text-muted">Última Atualização</small>
                <div class="fw-semibold">{{ $product->updated_at->format('d/m/Y H:i') }}</div>
            </div>

            <div class="btn-group btn-group-sm" role="group">
                <a href="{{ route('provider.products.show', $product) }}" class="btn btn-outline-primary">
                    <i class="bi bi-eye"></i> Ver
                </a>
                <a href="{{ route('provider.products.edit', $product) }}" class="btn btn-outline-secondary">
                    <i class="bi bi-pencil"></i> Editar
                </a>
            </div>
        </div>
    </div>
</div>
```

## 2. Product Details Component

Componente para exibição detalhada de informações do produto.

### Uso Básico

```blade
<x-product.product-details :product="$product" :showInventory="true" :showPricing="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showInventory` | `bool` | Exibir informações de estoque | `true` |
| `showPricing` | `bool` | Exibir informações de preço | `true` |
| `collapsible` | `bool` | Permitir colapsar seções | `false` |

### Estrutura

```blade
@props([
    'product',
    'showInventory' => true,
    'showPricing' => true,
    'collapsible' => false
])

<div class="product-details">
    <!-- Informações Básicas -->
    <div class="row g-3 mb-3">
        <div class="col-md-4">
            <div class="info-item">
                <label class="text-muted small">Nome</label>
                <div class="fw-bold">{{ $product->name }}</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="info-item">
                <label class="text-muted small">Código</label>
                <div class="fw-bold">{{ $product->code ?? 'Não definido' }}</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="info-item">
                <label class="text-muted small">Status</label>
                <x-product.product-status :product="$product" />
            </div>
        </div>
    </div>

    <!-- Descrição -->
    @if($product->description)
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Descrição</h6>
                    </div>
                    <div class="card-body">
                        <p class="mb-0">{{ $product->description }}</p>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Categoria -->
    @if($product->category)
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Categoria</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <span class="badge bg-secondary">{{ $product->category->name }}</span>
                                @if($product->category->parent)
                                    <small class="text-muted ms-2">Subcategoria de {{ $product->category->parent->name }}</small>
                                @endif
                            </div>
                            <a href="{{ route('provider.categories.show', $product->category) }}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-eye"></i> Ver Categoria
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Preço -->
    @if($showPricing)
        <x-product.product-pricing :product="$product" />
    @endif

    <!-- Estoque -->
    @if($showInventory)
        <x-product.product-inventory :product="$product" />
    @endif

    <!-- Imagem -->
    @if($product->image)
        <x-product.product-image :product="$product" />
    @endif

    <!-- Resumo -->
    <x-product.product-summary :product="$product" />
</div>
```

## 3. Product Status Component

Componente para exibição do status do produto com cores e ícones apropriados.

### Uso Básico

```blade
<x-product.product-status :product="$product" :showIcon="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showIcon` | `bool` | Exibir ícone ao lado do status | `true` |
| `size` | `string` | Tamanho do badge (sm, md, lg) | `md` |

### Estrutura

```blade
@props([
    'product',
    'showIcon' => true,
    'size' => 'md'
])

@php
    $status = $product->active ? 'active' : 'inactive';
    $color = $product->active ? '#198754' : '#6c757d';
    $icon = $product->active ? 'check-circle' : 'x-circle';
    $description = $product->active ? 'Ativo' : 'Inativo';

    $sizeClass = match($size) {
        'sm' => 'badge-sm',
        'lg' => 'badge-lg',
        default => 'badge-md'
    };
@endphp

<span class="badge modern-badge {{ $sizeClass }}"
      style="background-color: {{ $color }}20; color: {{ $color }}; border: 1px solid {{ $color }}40;">
    @if($showIcon)
        <i class="bi bi-{{ $icon }} me-1"></i>
    @endif
    {{ $description }}
</span>
```

## 4. Product Inventory Component

Componente para exibição de informações de estoque do produto.

### Uso Básico

```blade
<x-product.product-inventory :product="$product" :showMovements="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showMovements` | `bool` | Exibir movimentações recentes | `true` |
| `showAlerts` | `bool` | Exibir alertas de estoque | `true` |

### Estrutura

```blade
@props([
    'product',
    'showMovements' => true,
    'showAlerts' => true
])

<div class="product-inventory">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Controle de Estoque</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="mb-3">
                        <label class="text-muted small">Quantidade Atual</label>
                        <div class="fw-bold fs-4 text-primary">{{ $product->inventory->quantity ?? 0 }}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="mb-3">
                        <label class="text-muted small">Estoque Mínimo</label>
                        <div class="fw-bold">{{ $product->inventory->min_quantity ?? 0 }}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="mb-3">
                        <label class="text-muted small">Estoque Máximo</label>
                        <div class="fw-bold">{{ $product->inventory->max_quantity ?? 'Ilimitado' }}</div>
                    </div>
                </div>
            </div>

            @if($showAlerts)
                <!-- Alertas de Estoque -->
                @php
                    $currentStock = $product->inventory->quantity ?? 0;
                    $minStock = $product->inventory->min_quantity ?? 0;
                    $maxStock = $product->inventory->max_quantity;
                @endphp

                @if($currentStock <= $minStock)
                    <div class="alert alert-warning d-flex align-items-center" role="alert">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        <div>
                            <strong>Estoque Baixo!</strong> Quantidade atual está abaixo do mínimo recomendado.
                        </div>
                    </div>
                @elseif($maxStock && $currentStock >= $maxStock)
                    <div class="alert alert-info d-flex align-items-center" role="alert">
                        <i class="bi bi-info-circle-fill me-2"></i>
                        <div>
                            <strong>Estoque Cheio!</strong> Quantidade atual está no limite máximo.
                        </div>
                    </div>
                @endif
            @endif

            @if($showMovements && $product->inventoryMovements->isNotEmpty())
                <div class="mt-3">
                    <h6 class="mb-2">Últimas Movimentações</h6>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Data</th>
                                    <th>Tipo</th>
                                    <th>Quantidade</th>
                                    <th>Motivo</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach($product->inventoryMovements->take(5) as $movement)
                                    <tr>
                                        <td>{{ $movement->created_at->format('d/m/Y H:i') }}</td>
                                        <td>
                                            <span class="badge {{ $movement->type === 'in' ? 'bg-success' : 'bg-danger' }}">
                                                {{ $movement->type === 'in' ? 'Entrada' : 'Saída' }}
                                            </span>
                                        </td>
                                        <td class="{{ $movement->type === 'in' ? 'text-success' : 'text-danger' }}">
                                            {{ $movement->type === 'in' ? '+' : '-' }}{{ $movement->quantity }}
                                        </td>
                                        <td>{{ $movement->reason ?? 'Sem motivo' }}</td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 5. Product Pricing Component

Componente para exibição de informações de preço do produto.

### Uso Básico

```blade
<x-product.product-pricing :product="$product" :showCost="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showCost` | `bool` | Exibir preço de custo (se disponível) | `true` |
| `showProfit` | `bool` | Exibir margem de lucro | `true` |

### Estrutura

```blade
@props([
    'product',
    'showCost' => true,
    'showProfit' => true
])

<div class="product-pricing">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Informações de Preço</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="text-muted small">Preço de Venda</label>
                        <div class="fw-bold fs-3 text-primary">
                            R$ {{ number_format($product->price, 2, ',', '.') }}
                        </div>
                    </div>
                </div>

                @if($showCost)
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="text-muted small">Preço de Custo</label>
                            <div class="fw-bold">
                                R$ {{ number_format($product->cost ?? 0, 2, ',', '.') }}
                            </div>
                        </div>
                    </div>
                @endif
            </div>

            @if($showProfit && $product->cost)
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="text-muted small">Margem de Lucro</label>
                            @php
                                $cost = $product->cost ?? 0;
                                $price = $product->price;
                                $profit = $price - $cost;
                                $margin = $cost > 0 ? ($profit / $cost) * 100 : 0;
                            @endphp
                            <div class="fw-bold {{ $margin >= 20 ? 'text-success' : 'text-warning' }}">
                                {{ number_format($margin, 2, ',', '.') }}%
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="text-muted small">Lucro por Unidade</label>
                            <div class="fw-bold text-success">
                                R$ {{ number_format($profit, 2, ',', '.') }}
                            </div>
                        </div>
                    </div>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 6. Product Form Component

Componente para formulário de criação e edição de produtos.

### Uso Básico

```blade
<x-product.product-form :product="$product ?? null" :categories="$categories" :units="$units" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product|null` | Modelo do produto (para edição) | `null` |
| `categories` | `Collection` | Categorias disponíveis | Obrigatório |
| `units` | `Collection` | Unidades de medida disponíveis | Obrigatório |
| `showInventory` | `bool` | Exibir campos de estoque | `true` |

### Estrutura

```blade
@props([
    'product' => null,
    'categories' => [],
    'units' => [],
    'showInventory' => true
])

<div class="product-form">
    <form action="{{ isset($product) ? route('provider.products.update', $product) : route('provider.products.store') }}"
          method="POST"
          id="productForm"
          enctype="multipart/form-data">
        @csrf
        @if(isset($product)) @method('PUT') @endif

        <!-- Informações Básicas -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Informações Básicas</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <label class="form-label small fw-bold text-muted text-uppercase">Nome *</label>
                                <input type="text"
                                       name="name"
                                       class="form-control @error('name') is-invalid @enderror"
                                       value="{{ old('name', $product->name ?? '') }}" required>
                                @error('name')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold text-muted text-uppercase">Código</label>
                                <input type="text"
                                       name="code"
                                       class="form-control @error('code') is-invalid @enderror"
                                       value="{{ old('code', $product->code ?? '') }}">
                                @error('code')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-12">
                                <label class="form-label small fw-bold text-muted text-uppercase">Descrição</label>
                                <textarea name="description"
                                          class="form-control @error('description') is-invalid @enderror"
                                          rows="3"
                                          placeholder="Descrição do produto...">{{ old('description', $product->description ?? '') }}</textarea>
                                @error('description')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Categoria e Preço -->
        <div class="row g-3 mb-4">
            <div class="col-md-6">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Categoria</h6>
                    </div>
                    <div class="card-body">
                        <label class="form-label small fw-bold text-muted text-uppercase">Categoria *</label>
                        <select name="category_id" class="form-select @error('category_id') is-invalid @enderror">
                            <option value="">Selecione uma categoria</option>
                            @foreach($categories as $category)
                                <option value="{{ $category->id }}"
                                        {{ (old('category_id', $product->category_id ?? '') == $category->id) ? 'selected' : '' }}>
                                    {{ $category->name }}
                                </option>
                            @endforeach
                        </select>
                        @error('category_id')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Preço</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-12">
                                <label class="form-label small fw-bold text-muted text-uppercase">Preço de Venda *</label>
                                <input type="number"
                                       name="price"
                                       step="0.01"
                                       min="0"
                                       class="form-control @error('price') is-invalid @enderror"
                                       value="{{ old('price', $product->price ?? '') }}" required>
                                @error('price')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-12 mt-3">
                                <label class="form-label small fw-bold text-muted text-uppercase">Preço de Custo</label>
                                <input type="number"
                                       name="cost"
                                       step="0.01"
                                       min="0"
                                       class="form-control @error('cost') is-invalid @enderror"
                                       value="{{ old('cost', $product->cost ?? '') }}">
                                @error('cost')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Estoque -->
        @if($showInventory)
            <div class="row g-3 mb-4">
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header bg-transparent border-0">
                            <h6 class="mb-0">Controle de Estoque</h6>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Quantidade Inicial</label>
                                    <input type="number"
                                           name="initial_quantity"
                                           class="form-control @error('initial_quantity') is-invalid @enderror"
                                           value="{{ old('initial_quantity', 0) }}">
                                    @error('initial_quantity')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Estoque Mínimo</label>
                                    <input type="number"
                                           name="min_quantity"
                                           class="form-control @error('min_quantity') is-invalid @enderror"
                                           value="{{ old('min_quantity', $product->inventory->min_quantity ?? 0) }}">
                                    @error('min_quantity')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Estoque Máximo</label>
                                    <input type="number"
                                           name="max_quantity"
                                           class="form-control @error('max_quantity') is-invalid @enderror"
                                           value="{{ old('max_quantity', $product->inventory->max_quantity ?? '') }}">
                                    @error('max_quantity')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        @endif

        <!-- Imagem -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Imagem do Produto</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Imagem</label>
                                <input type="file"
                                       name="image"
                                       class="form-control @error('image') is-invalid @enderror"
                                       accept="image/*">
                                @error('image')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                                @if(isset($product) && $product->image)
                                    <div class="mt-2">
                                        <img src="{{ asset('storage/' . $product->image) }}"
                                             alt="{{ $product->name }}"
                                             class="img-thumbnail"
                                             style="max-width: 200px;">
                                        <div class="form-check mt-2">
                                            <input type="checkbox" name="remove_image" value="1" class="form-check-input">
                                            <label class="form-check-label">Remover imagem atual</label>
                                        </div>
                                    </div>
                                @endif
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Status -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Status</h6>
                    </div>
                    <div class="card-body">
                        <div class="form-check form-switch">
                            <input type="checkbox"
                                   name="active"
                                   class="form-check-input"
                                   id="productActive"
                                   {{ (old('active', $product->active ?? true)) ? 'checked' : '' }}>
                            <label class="form-check-label" for="productActive">
                                Produto Ativo
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Ações -->
        <div class="d-flex justify-content-between">
            <a href="{{ route('provider.products.index') }}" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-2"></i>Cancelar
            </a>
            <button type="submit" class="btn btn-primary">
                <i class="bi bi-check-circle me-2"></i>{{ isset($product) ? 'Atualizar' : 'Criar' }} Produto
            </button>
        </div>
    </form>
</div>

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Formatar preço
    const priceInput = document.querySelector('input[name="price"]');
    const costInput = document.querySelector('input[name="cost"]');

    function formatCurrency(input) {
        if (input) {
            input.addEventListener('input', function() {
                let value = this.value.replace(/\D/g, '');
                value = (parseInt(value) / 100).toFixed(2);
                this.value = value;
            });
        }
    }

    formatCurrency(priceInput);
    formatCurrency(costInput);
});
</script>
@endpush
```

## 7. Product Actions Component

Componente para exibição de ações disponíveis para um produto.

### Uso Básico

```blade
<x-product.product-actions :product="$product" :showInventory="true" :showEdit="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showInventory` | `bool` | Exibir botão de controle de estoque | `true` |
| `showEdit` | `bool` | Exibir botão de edição | `true` |
| `showDelete` | `bool` | Exibir botão de exclusão | `true` |

### Estrutura

```blade
@props([
    'product',
    'showInventory' => true,
    'showEdit' => true,
    'showDelete' => true
])

<div class="product-actions btn-group" role="group">
    <!-- Visualizar -->
    <a href="{{ route('provider.products.show', $product) }}"
       class="btn btn-outline-primary"
       title="Visualizar Produto">
        <i class="bi bi-eye"></i> Visualizar
    </a>

    <!-- Editar -->
    @if($showEdit)
        <a href="{{ route('provider.products.edit', $product) }}"
           class="btn btn-outline-secondary"
           title="Editar Produto">
            <i class="bi bi-pencil"></i> Editar
        </a>
    @endif

    <!-- Controle de Estoque -->
    @if($showInventory)
        <button type="button"
                class="btn btn-outline-info"
                data-bs-toggle="modal"
                data-bs-target="#inventoryModal-{{ $product->id }}"
                title="Controle de Estoque">
            <i class="bi bi-box-seam"></i> Estoque
        </button>
    @endif

    <!-- Alternar Status -->
    <button type="button"
            class="btn btn-outline-{{ $product->active ? 'warning' : 'success' }}"
            data-bs-toggle="modal"
            data-bs-target="#statusModal-{{ $product->id }}"
            title="{{ $product->active ? 'Desativar' : 'Ativar' }} Produto">
        <i class="bi bi-{{ $product->active ? 'toggle-on' : 'toggle-off' }}"></i>
        {{ $product->active ? 'Desativar' : 'Ativar' }}
    </button>

    <!-- Excluir -->
    @if($showDelete)
        <button type="button"
                class="btn btn-outline-danger"
                data-bs-toggle="modal"
                data-bs-target="#deleteModal-{{ $product->id }}"
                title="Excluir Produto">
            <i class="bi bi-trash"></i> Excluir
        </button>
    @endif
</div>
```

## 8. Product Filters Component

Componente para filtros específicos de listagem de produtos.

### Uso Básico

```blade
<x-product.product-filters :filters="$filters" :showCategory="true" :showStatus="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `filters` | `array` | Filtros atuais | `[]` |
| `showCategory` | `bool` | Exibir filtro por categoria | `true` |
| `showStatus` | `bool` | Exibir filtro por status | `true` |
| `showPriceRange` | `bool` | Exibir filtro por faixa de preço | `true` |

### Estrutura

```blade
@props([
    'filters' => [],
    'showCategory' => true,
    'showStatus' => true,
    'showPriceRange' => true
])

<div class="product-filters">
    <form action="{{ request()->url() }}" method="GET" class="row g-3">
        @if($showCategory)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Categoria</label>
                <select name="category_id" class="form-select form-select-sm">
                    <option value="">Todas as categorias</option>
                    @foreach($categories as $category)
                        <option value="{{ $category->id }}" {{ ($filters['category_id'] ?? '') == $category->id ? 'selected' : '' }}>
                            {{ $category->name }}
                        </option>
                    @endforeach
                </select>
            </div>
        @endif

        @if($showStatus)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Status</label>
                <select name="active" class="form-select form-select-sm">
                    <option value="">Todos os status</option>
                    <option value="1" {{ ($filters['active'] ?? '') == '1' ? 'selected' : '' }}>Ativos</option>
                    <option value="0" {{ ($filters['active'] ?? '') == '0' ? 'selected' : '' }}>Inativos</option>
                </select>
            </div>
        @endif

        @if($showPriceRange)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Faixa de Preço</label>
                <div class="input-group input-group-sm">
                    <input type="number"
                           name="min_price"
                           step="0.01"
                           class="form-control"
                           value="{{ $filters['min_price'] ?? '' }}"
                           placeholder="Mínimo">
                    <span class="input-group-text">até</span>
                    <input type="number"
                           name="max_price"
                           step="0.01"
                           class="form-control"
                           value="{{ $filters['max_price'] ?? '' }}"
                           placeholder="Máximo">
                </div>
            </div>
        @endif

        <div class="col-md-3">
            <label class="form-label small fw-bold text-muted text-uppercase">Busca</label>
            <input type="text"
                   name="search"
                   class="form-control form-control-sm"
                   value="{{ $filters['search'] ?? '' }}"
                   placeholder="Buscar por nome...">
        </div>

        <div class="col-12">
            <div class="d-flex justify-content-between">
                <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-primary btn-sm">
                        <i class="bi bi-search me-2"></i>Filtrar
                    </button>
                    <a href="{{ route('provider.products.index') }}" class="btn btn-outline-secondary btn-sm">
                        <i class="bi bi-x-circle me-2"></i>Limpar
                    </a>
                </div>

                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#createModal">
                        <i class="bi bi-plus-circle me-2"></i>Novo Produto
                    </button>
                </div>
            </div>
        </div>
    </form>
</div>
```

## 9. Product Image Component

Componente para exibição de imagem do produto.

### Uso Básico

```blade
<x-product.product-image :product="$product" :showThumbnail="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showThumbnail` | `bool` | Exibir miniatura | `true` |
| `size` | `string` | Tamanho da imagem (small, medium, large) | `medium` |

### Estrutura

```blade
@props([
    'product',
    'showThumbnail' => true,
    'size' => 'medium'
])

<div class="product-image">
    @if($product->image)
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-transparent border-0">
                <h6 class="mb-0">Imagem do Produto</h6>
            </div>
            <div class="card-body text-center">
                @php
                    $sizeClass = match($size) {
                        'small' => 'img-thumbnail',
                        'large' => 'img-fluid',
                        default => 'img-thumbnail'
                    };
                @endphp

                <img src="{{ asset('storage/' . $product->image) }}"
                     alt="{{ $product->name }}"
                     class="{{ $sizeClass }}"
                     style="max-width: 300px; height: auto;">

                <div class="mt-3">
                    <small class="text-muted">Última atualização: {{ $product->updated_at->format('d/m/Y H:i') }}</small>
                </div>
            </div>
        </div>
    @else
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-transparent border-0">
                <h6 class="mb-0">Imagem do Produto</h6>
            </div>
            <div class="card-body text-center">
                <div class="avatar-circle bg-secondary bg-gradient mb-3 mx-auto" style="width: 100px; height: 100px;">
                    <i class="bi bi-box text-white" style="font-size: 2rem;"></i>
                </div>
                <p class="text-muted">Nenhuma imagem cadastrada</p>
            </div>
        </div>
    @endif
</div>
```

## 10. Product Summary Component

Componente para exibição de resumo do produto.

### Uso Básico

```blade
<x-product.product-summary :product="$product" :showStats="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `showStats` | `bool` | Exibir estatísticas | `true` |
| `showCategory` | `bool` | Exibir informações da categoria | `true` |

### Estrutura

```blade
@props([
    'product',
    'showStats' => true,
    'showCategory' => true
])

<div class="product-summary">
    <div class="row g-3">
        @if($showStats)
            <!-- Estatísticas -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <div class="avatar-circle bg-primary bg-gradient mb-2 mx-auto">
                            <i class="bi bi-box-seam text-white"></i>
                        </div>
                        <div class="text-muted small">Estoque Atual</div>
                        <div class="h4 mb-0 fw-bold">{{ $product->inventory->quantity ?? 0 }}</div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <div class="avatar-circle bg-success bg-gradient mb-2 mx-auto">
                            <i class="bi bi-currency-dollar text-white"></i>
                        </div>
                        <div class="text-muted small">Preço de Venda</div>
                        <div class="h4 mb-0 fw-bold">
                            R$ {{ number_format($product->price, 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <div class="avatar-circle bg-info bg-gradient mb-2 mx-auto">
                            <i class="bi bi-graph-up text-white"></i>
                        </div>
                        <div class="text-muted small">Movimentações</div>
                        <div class="h4 mb-0 fw-bold">{{ $product->inventoryMovements->count() }}</div>
                    </div>
                </div>
            </div>
        @endif
    </div>

    @if($showCategory && $product->category)
        <div class="row mt-3">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Categoria</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-flex w-100 justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">{{ $product->category->name }}</h6>
                                <p class="mb-0 text-muted small">
                                    @if($product->category->parent)
                                        Subcategoria de {{ $product->category->parent->name }}
                                    @else
                                        Categoria principal
                                    @endif
                                </p>
                            </div>
                            <div class="text-end">
                                <span class="badge bg-secondary">{{ $product->category->products->count() }} produtos</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif
</div>
```

## 11. Integração com Padrões Existentes

### Uso em Views

```blade
{{-- Dashboard --}}
<x-product.product-card :product="$product" />

{{-- Listagem --}}
<x-product.product-details :product="$product" />

{{-- Formulários --}}
<x-product.product-form :product="$product" :categories="$categories" :units="$units" />

{{-- Ações --}}
<x-product.product-actions :product="$product" />
```

### Estilos CSS

```css
/* Product Components Styles */
.product-form .form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.product-actions .btn {
    transition: all 0.2s ease;
}

.product-actions .btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.product-summary .card {
    border-left: 4px solid #0d6efd;
}

.product-inventory .alert {
    border-left: 4px solid;
}

.product-inventory .alert-warning {
    border-left-color: #ffc107;
}

.product-inventory .alert-info {
    border-left-color: #0dcaf0;
}
```

## 12. JavaScript Interatividade

### Formulário de Produto

```javascript
// product-form.js
document.addEventListener('DOMContentLoaded', function() {
    // Formatar campos de preço
    const priceInputs = document.querySelectorAll('input[name="price"], input[name="cost"]');

    priceInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', function() {
                let value = this.value.replace(/\D/g, '');
                if (value.length > 2) {
                    value = value.replace(/(\d{2})$/, '.$1');
                }
                this.value = value;
            });
        }
    });

    // Validar estoque
    const minQuantityInput = document.querySelector('input[name="min_quantity"]');
    const maxQuantityInput = document.querySelector('input[name="max_quantity"]');

    if (minQuantityInput && maxQuantityInput) {
        minQuantityInput.addEventListener('change', function() {
            if (parseInt(this.value) > parseInt(maxQuantityInput.value)) {
                maxQuantityInput.value = this.value;
            }
        });
    }
});
```

## 13. Validação e Segurança

### Autorização

```php
// ProductPolicy.php
public function view(User $user, Product $product)
{
    return $user->tenant_id === $product->tenant_id;
}

public function update(User $user, Product $product)
{
    return $user->tenant_id === $product->tenant_id;
}

public function delete(User $user, Product $product)
{
    return $user->tenant_id === $product->tenant_id &&
           $product->budgetItems->isEmpty() &&
           $product->serviceItems->isEmpty();
}
```

### Validations

```blade
{{-- Product Card com validação de permissões --}}
@can('view', $product)
    <x-product.product-card :product="$product" />
@endcan

{{-- Product Actions com validação de status --}}
@can('update', $product)
    <x-product.product-actions :product="$product" />
@endcan
```

Este padrão de components para produtos garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
