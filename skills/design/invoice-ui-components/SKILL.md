---
name: invoice-ui-components
description: Componentes de UI para faturas seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para Faturas

Esta skill define os componentes Blade específicos para a gestão de faturas no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── invoice/
│   ├── invoice-card.blade.php        # Card resumido de fatura
│   ├── invoice-details.blade.php     # Detalhes completos da fatura
│   ├── invoice-form.blade.php        # Formulário de criação/edição
│   ├── invoice-status.blade.php      # Badge de status da fatura
│   ├── invoice-items.blade.php       # Lista de itens da fatura
│   ├── invoice-actions.blade.php     # Ações disponíveis para fatura
│   ├── invoice-filters.blade.php     # Filtros específicos para faturas
│   ├── invoice-payments.blade.php    # Histórico de pagamentos
│   └── invoice-totals.blade.php      # Totais e valores da fatura
└── ...
```

## 1. Invoice Card Component

Componente para exibição resumida de faturas em listas e dashboards.

### Uso Básico

```blade
<x-invoice.invoice-card :invoice="$invoice" :showCustomer="true" :showDueDate="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showCustomer` | `bool` | Exibir informações do cliente | `true` |
| `showDueDate` | `bool` | Exibir data de vencimento | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'invoice',
    'showCustomer' => true,
    'showDueDate' => true,
    'variant' => 'primary'
])

<div class="card border-0 shadow-sm h-100">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center gap-3">
                <div class="avatar-circle bg-{{ $variant }} bg-gradient">
                    <i class="bi bi-receipt text-white"></i>
                </div>
                <div>
                    <h6 class="mb-1 fw-bold">{{ $invoice->code }}</h6>
                    <small class="text-muted">{{ $invoice->created_at->format('d/m/Y') }}</small>
                </div>
            </div>
            <x-invoice.invoice-status :invoice="$invoice" />
        </div>

        @if($showCustomer && $invoice->customer)
            <div class="mb-3">
                <small class="text-muted">Cliente:</small>
                <div class="fw-semibold">{{ $invoice->customer->display_name }}</div>
            </div>
        @endif

        @if($showDueDate)
            <div class="mb-3">
                <small class="text-muted">Vencimento:</small>
                <div class="fw-bold {{ $invoice->isOverdue() ? 'text-danger' : '' }}">
                    {{ $invoice->due_date?->format('d/m/Y') ?? 'Indeterminado' }}
                    @if($invoice->isOverdue())
                        <span class="badge bg-danger ms-2">Atrasado</span>
                    @endif
                </div>
            </div>
        @endif

        <div class="d-flex justify-content-between align-items-center">
            <div>
                <small class="text-muted">Valor Total</small>
                <div class="h6 mb-0 fw-bold text-{{ $variant }}">
                    R$ {{ number_format($invoice->total, 2, ',', '.') }}
                </div>
            </div>

            <div class="btn-group btn-group-sm" role="group">
                <a href="{{ route('provider.invoices.show', $invoice) }}" class="btn btn-outline-primary">
                    <i class="bi bi-eye"></i> Ver
                </a>
                @if($invoice->status->isEditable())
                    <a href="{{ route('provider.invoices.edit', $invoice) }}" class="btn btn-outline-secondary">
                        <i class="bi bi-pencil"></i> Editar
                    </a>
                @endif
            </div>
        </div>
    </div>
</div>
```

## 2. Invoice Details Component

Componente para exibição detalhada de informações da fatura.

### Uso Básico

```blade
<x-invoice.invoice-details :invoice="$invoice" :showItems="true" :showPayments="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showItems` | `bool` | Exibir itens da fatura | `true` |
| `showPayments` | `bool` | Exibir histórico de pagamentos | `true` |
| `collapsible` | `bool` | Permitir colapsar seções | `false` |

### Estrutura

```blade
@props([
    'invoice',
    'showItems' => true,
    'showPayments' => true,
    'collapsible' => false
])

<div class="invoice-details">
    <!-- Informações Básicas -->
    <div class="row g-3 mb-3">
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Código</label>
                <div class="fw-bold">{{ $invoice->code }}</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Data de Emissão</label>
                <div class="fw-bold">{{ $invoice->created_at->format('d/m/Y H:i') }}</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Vencimento</label>
                <div class="fw-bold {{ $invoice->isOverdue() ? 'text-danger' : '' }}">
                    {{ $invoice->due_date?->format('d/m/Y') ?? 'Indeterminado' }}
                    @if($invoice->isOverdue())
                        <span class="badge bg-danger ms-2">Atrasado</span>
                    @endif
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="info-item">
                <label class="text-muted small">Status</label>
                <x-invoice.invoice-status :invoice="$invoice" />
            </div>
        </div>
    </div>

    <!-- Cliente -->
    @if($invoice->customer)
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Informações do Cliente</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-2">
                                    <label class="text-muted small">Nome</label>
                                    <div class="fw-bold">{{ $invoice->customer->display_name }}</div>
                                </div>
                                @if($invoice->customer->contact)
                                    <div class="mb-2">
                                        <label class="text-muted small">E-mail</label>
                                        <div class="fw-bold">{{ $invoice->customer->contact->email }}</div>
                                    </div>
                                    <div class="mb-2">
                                        <label class="text-muted small">Telefone</label>
                                        <div class="fw-bold">{{ $invoice->customer->contact->phone }}</div>
                                    </div>
                                @endif
                            </div>
                            <div class="col-md-6">
                                @if($invoice->customer->address)
                                    <div class="mb-2">
                                        <label class="text-muted small">Endereço</label>
                                        <div class="fw-bold">
                                            {{ $invoice->customer->address->address }}, {{ $invoice->customer->address->address_number }}
                                        </div>
                                        <div class="fw-bold">
                                            {{ $invoice->customer->address->neighborhood }} - {{ $invoice->customer->address->city }}/{{ $invoice->customer->address->state }}
                                        </div>
                                    </div>
                                @endif
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Itens da Fatura -->
    @if($showItems && $invoice->invoiceItems->isNotEmpty())
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Itens da Fatura</h6>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Descrição</th>
                                        <th>Quantidade</th>
                                        <th>Valor Unitário</th>
                                        <th>Valor Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    @foreach($invoice->invoiceItems as $item)
                                        <tr>
                                            <td>{{ $item->description }}</td>
                                            <td>{{ $item->quantity }}</td>
                                            <td>R$ {{ number_format($item->unit_price, 2, ',', '.') }}</td>
                                            <td class="fw-bold">
                                                R$ {{ number_format($item->total, 2, ',', '.') }}
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

    <!-- Histórico de Pagamentos -->
    @if($showPayments && $invoice->payments->isNotEmpty())
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Histórico de Pagamentos</h6>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Data</th>
                                        <th>Método</th>
                                        <th>Valor</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    @foreach($invoice->payments as $payment)
                                        <tr>
                                            <td>{{ $payment->transaction_date?->format('d/m/Y H:i') }}</td>
                                            <td>{{ $payment->payment_method }}</td>
                                            <td class="fw-bold">
                                                R$ {{ number_format($payment->transaction_amount, 2, ',', '.') }}
                                            </td>
                                            <td>
                                                <span class="badge bg-success">{{ $payment->status }}</span>
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
    <x-invoice.invoice-totals :invoice="$invoice" />
</div>
```

## 3. Invoice Status Component

Componente para exibição do status da fatura com cores e ícones apropriados.

### Uso Básico

```blade
<x-invoice.invoice-status :invoice="$invoice" :showIcon="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showIcon` | `bool` | Exibir ícone ao lado do status | `true` |
| `size` | `string` | Tamanho do badge (sm, md, lg) | `md` |

### Estrutura

```blade
@props([
    'invoice',
    'showIcon' => true,
    'size' => 'md'
])

@php
    $status = $invoice->status;
    $metadata = $status->getMetadata();
    $color = $metadata['color'] ?? '#6c757d';
    $icon = $metadata['icon'] ?? 'circle';
    $description = $metadata['description'] ?? $status->value;

    $sizeClass = match($size) {
        'sm' => 'badge-sm',
        'lg' => 'badge-lg',
        default => 'badge-md'
    };

    // Lógica para status de atraso
    $isOverdue = $invoice->isOverdue();
    if ($isOverdue && $invoice->status->isPending()) {
        $color = '#dc3545'; // Vermelho para faturas atrasadas
        $icon = 'exclamation-triangle';
        $description = 'Atrasada';
    }
@endphp

<span class="badge modern-badge {{ $sizeClass }}"
      style="background-color: {{ $color }}20; color: {{ $color }}; border: 1px solid {{ $color }}40;">
    @if($showIcon)
        <i class="bi {{ $icon }} me-1"></i>
    @endif
    {{ $description }}
    @if($isOverdue)
        <span class="badge bg-danger ms-1">+{{ $invoice->daysOverdue() }} dias</span>
    @endif
</span>
```

## 4. Invoice Items Component

Componente para exibição da lista de itens de uma fatura.

### Uso Básico

```blade
<x-invoice.invoice-items :invoice="$invoice" :editable="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `editable` | `bool` | Permitir edição dos itens | `false` |
| `showTotal` | `bool` | Exibir total geral | `true` |

### Estrutura

```blade
@props([
    'invoice',
    'editable' => false,
    'showTotal' => true
])

<div class="invoice-items">
    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
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
                @foreach($invoice->invoiceItems as $item)
                    <tr>
                        <td>
                            @if($editable)
                                <input type="text"
                                       name="items[{{ $item->id }}][description]"
                                       class="form-control form-control-sm"
                                       value="{{ $item->description }}"
                                       placeholder="Descrição do item">
                            @else
                                <div class="fw-bold">{{ $item->description }}</div>
                            @endif
                        </td>
                        <td class="text-center">
                            @if($editable)
                                <input type="number"
                                       name="items[{{ $item->id }}][quantity]"
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
                                       name="items[{{ $item->id }}][unit_price]"
                                       class="form-control form-control-sm text-end"
                                       value="{{ number_format($item->unit_price, 2, ',', '.') }}"
                                       style="width: 120px;">
                            @else
                                R$ {{ number_format($item->unit_price, 2, ',', '.') }}
                            @endif
                        </td>
                        <td class="text-end fw-bold">
                            R$ {{ number_format($item->total, 2, ',', '.') }}
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
                        <td colspan="{{ $editable ? 3 : 2 }}" class="text-end fw-bold">Subtotal:</td>
                        <td class="text-end fw-bold">
                            R$ {{ number_format($invoice->invoiceItems->sum('total'), 2, ',', '.') }}
                        </td>
                        @if($editable)
                            <td></td>
                        @endif
                    </tr>
                    @if($invoice->discount > 0)
                        <tr>
                            <td colspan="{{ $editable ? 3 : 2 }}" class="text-end text-muted">Desconto:</td>
                            <td class="text-end text-danger fw-bold">
                                - R$ {{ number_format($invoice->discount, 2, ',', '.') }}
                            </td>
                            @if($editable)
                                <td></td>
                            @endif
                        </tr>
                    @endif
                    <tr class="table-active">
                        <td colspan="{{ $editable ? 3 : 2 }}" class="text-end fw-bold">Total da Fatura:</td>
                        <td class="text-end fw-bold h5">
                            R$ {{ number_format($invoice->total, 2, ',', '.') }}
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

## 5. Invoice Form Component

Componente para formulário de criação e edição de faturas.

### Uso Básico

```blade
<x-invoice.invoice-form :invoice="$invoice ?? null" :customers="$customers" :services="$services" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice|null` | Modelo da fatura (para edição) | `null` |
| `customers` | `Collection` | Clientes disponíveis | Obrigatório |
| `services` | `Collection` | Serviços disponíveis | Obrigatório |
| `budget` | `Budget|null` | Orçamento vinculado | `null` |

### Estrutura

```blade
@props([
    'invoice' => null,
    'customers' => [],
    'services' => [],
    'budget' => null
])

<div class="invoice-form">
    <form action="{{ isset($invoice) ? route('provider.invoices.update', $invoice) : route('provider.invoices.store') }}"
          method="POST"
          id="invoiceForm">
        @csrf
        @if(isset($invoice)) @method('PUT') @endif

        <!-- Informações Básicas -->
        <div class="row g-3 mb-4">
            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Cliente *</label>
                <select name="customer_id" class="form-select @error('customer_id') is-invalid @enderror" required>
                    <option value="">Selecione um cliente</option>
                    @foreach($customers as $customer)
                        <option value="{{ $customer->id }}"
                                {{ (old('customer_id', $invoice->customer_id ?? '') == $customer->id) ? 'selected' : '' }}>
                            {{ $customer->display_name }}
                        </option>
                    @endforeach
                </select>
                @error('customer_id')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>

            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Data de Vencimento *</label>
                <input type="date"
                       name="due_date"
                       class="form-control @error('due_date') is-invalid @enderror"
                       value="{{ old('due_date', $invoice->due_date?->format('Y-m-d') ?? '') }}"
                       required>
                @error('due_date')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>

            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Método de Pagamento</label>
                <select name="payment_method" class="form-select @error('payment_method') is-invalid @enderror">
                    <option value="">Selecione um método</option>
                    <option value="dinheiro" {{ (old('payment_method', $invoice->payment_method ?? '') == 'dinheiro') ? 'selected' : '' }}>Dinheiro</option>
                    <option value="cartao" {{ (old('payment_method', $invoice->payment_method ?? '') == 'cartao') ? 'selected' : '' }}>Cartão</option>
                    <option value="boleto" {{ (old('payment_method', $invoice->payment_method ?? '') == 'boleto') ? 'selected' : '' }}>Boleto</option>
                    <option value="pix" {{ (old('payment_method', $invoice->payment_method ?? '') == 'pix') ? 'selected' : '' }}>PIX</option>
                    <option value="transferencia" {{ (old('payment_method', $invoice->payment_method ?? '') == 'transferencia') ? 'selected' : '' }}>Transferência</option>
                </select>
                @error('payment_method')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>

            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Observações</label>
                <textarea name="notes"
                          class="form-control @error('notes') is-invalid @enderror"
                          rows="3"
                          placeholder="Observações sobre a fatura...">{{ old('notes', $invoice->notes ?? '') }}</textarea>
                @error('notes')
                    <div class="invalid-feedback">{{ $message }}</div>
                @enderror
            </div>
        </div>

        <!-- Itens da Fatura -->
        <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-transparent border-0">
                <h6 class="mb-0">Itens da Fatura</h6>
            </div>
            <div class="card-body">
                <div id="invoiceItems">
                    @if(isset($invoice) && $invoice->invoiceItems->isNotEmpty())
                        @foreach($invoice->invoiceItems as $item)
                            <div class="row g-3 item-row mb-3" data-item-id="{{ $item->id }}">
                                <div class="col-md-6">
                                    <input type="text"
                                           name="items[{{ $item->id }}][description]"
                                           class="form-control description-input"
                                           placeholder="Descrição do item"
                                           value="{{ $item->description }}" required>
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
                                           name="items[{{ $item->id }}][unit_price]"
                                           class="form-control price-input"
                                           placeholder="Valor Unitário"
                                           value="{{ number_format($item->unit_price, 2, ',', '.') }}"
                                           required>
                                </div>
                                <div class="col-md-2">
                                    <input type="text"
                                           class="form-control item-total"
                                           placeholder="Total"
                                           value="R$ {{ number_format($item->total, 2, ',', '.') }}"
                                           readonly>
                                </div>
                            </div>
                        @endforeach
                    @else
                        <div class="row g-3 item-row mb-3">
                            <div class="col-md-6">
                                <input type="text"
                                       name="items[0][description]"
                                       class="form-control description-input"
                                       placeholder="Descrição do item" required>
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
                                       name="items[0][unit_price]"
                                       class="form-control price-input"
                                       placeholder="Valor Unitário" required>
                            </div>
                            <div class="col-md-2">
                                <input type="text"
                                       class="form-control item-total"
                                       placeholder="Total"
                                       readonly>
                            </div>
                        </div>
                    @endif
                </div>

                <div class="row">
                    <div class="col-12">
                        <button type="button"
                                class="btn btn-outline-primary btn-sm"
                                id="addInvoiceItem">
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
                                   value="{{ old('discount', $invoice->discount ?? '0') }}"
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
            <a href="{{ route('provider.invoices.index') }}" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-2"></i>Cancelar
            </a>
            <button type="submit" class="btn btn-primary">
                <i class="bi bi-check-circle me-2"></i>{{ isset($invoice) ? 'Atualizar' : 'Criar' }} Fatura
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
            const unitPrice = parseFloat(row.querySelector('.price-input').value.replace(',', '.')) || 0;
            const total = quantity * unitPrice;
            row.querySelector('.item-total').value = 'R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            subtotal += total;
        });

        const discount = parseFloat(document.getElementById('discountInput').value.replace(',', '.')) || 0;
        const total = subtotal - discount;

        document.getElementById('subtotalDisplay').textContent = 'R$ ' + subtotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        document.getElementById('totalDisplay').textContent = 'R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    }

    // Eventos
    document.getElementById('addInvoiceItem').addEventListener('click', function() {
        const itemsContainer = document.getElementById('invoiceItems');
        const itemCount = itemsContainer.children.length;

        const newRow = document.createElement('div');
        newRow.className = 'row g-3 item-row mb-3';
        newRow.innerHTML = `
            <div class="col-md-6">
                <input type="text" name="items[${itemCount}][description]" class="form-control description-input" placeholder="Descrição do item" required>
            </div>
            <div class="col-md-2">
                <input type="number" name="items[${itemCount}][quantity]" class="form-control quantity-input" placeholder="Qtd" value="1" min="1" required>
            </div>
            <div class="col-md-2">
                <input type="text" name="items[${itemCount}][unit_price]" class="form-control price-input" placeholder="Valor Unitário" required>
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control item-total" placeholder="Total" readonly>
            </div>
        `;

        itemsContainer.appendChild(newRow);
        calculateTotals();
    });

    document.getElementById('invoiceItems').addEventListener('input', calculateTotals);
    document.getElementById('discountInput').addEventListener('input', calculateTotals);

    // Inicializar cálculos
    calculateTotals();
});
</script>
@endpush
```

## 6. Invoice Actions Component

Componente para exibição de ações disponíveis para uma fatura.

### Uso Básico

```blade
<x-invoice.invoice-actions :invoice="$invoice" :showPayment="true" :showSend="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showPayment` | `bool` | Exibir botão de pagamento | `true` |
| `showSend` | `bool` | Exibir botão de envio | `true` |
| `showPrint` | `bool` | Exibir botão de impressão | `true` |

### Estrutura

```blade
@props([
    'invoice',
    'showPayment' => true,
    'showSend' => true,
    'showPrint' => true
])

<div class="invoice-actions btn-group" role="group">
    <!-- Visualizar -->
    <a href="{{ route('provider.invoices.show', $invoice) }}"
       class="btn btn-outline-primary"
       title="Visualizar Fatura">
        <i class="bi bi-eye"></i> Visualizar
    </a>

    <!-- Editar -->
    @if($invoice->status->isEditable())
        <a href="{{ route('provider.invoices.edit', $invoice) }}"
           class="btn btn-outline-secondary"
           title="Editar Fatura">
            <i class="bi bi-pencil"></i> Editar
        </a>
    @endif

    <!-- Receber Pagamento -->
    @if($showPayment && $invoice->status->isPending())
        <button type="button"
                class="btn btn-outline-success"
                data-bs-toggle="modal"
                data-bs-target="#paymentModal-{{ $invoice->id }}"
                title="Receber Pagamento">
            <i class="bi bi-cash"></i> Receber
        </button>
    @endif

    <!-- Enviar por E-mail -->
    @if($showSend)
        <button type="button"
                class="btn btn-outline-info"
                data-bs-toggle="modal"
                data-bs-target="#sendModal-{{ $invoice->id }}"
                title="Enviar por E-mail">
            <i class="bi bi-envelope"></i> Enviar
        </button>
    @endif

    <!-- Imprimir -->
    @if($showPrint)
        <a href="{{ route('provider.invoices.pdf', $invoice) }}"
           class="btn btn-outline-warning"
           target="_blank"
           title="Imprimir Fatura">
            <i class="bi bi-printer"></i> Imprimir
        </a>
    @endif

    <!-- Excluir -->
    @if($invoice->status->isDeletable())
        <button type="button"
                class="btn btn-outline-danger"
                data-bs-toggle="modal"
                data-bs-target="#deleteModal-{{ $invoice->id }}"
                title="Excluir Fatura">
            <i class="bi bi-trash"></i> Excluir
        </button>
    @endif
</div>
```

## 7. Invoice Filters Component

Componente para filtros específicos de listagem de faturas.

### Uso Básico

```blade
<x-invoice.invoice-filters :filters="$filters" :showCustomer="true" :showStatus="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `filters` | `array` | Filtros atuais | `[]` |
| `showCustomer` | `bool` | Exibir filtro por cliente | `true` |
| `showStatus` | `bool` | Exibir filtro por status | `true` |
| `showDateRange` | `bool` | Exibir filtro por período | `true` |

### Estrutura

```blade
@props([
    'filters' => [],
    'showCustomer' => true,
    'showStatus' => true,
    'showDateRange' => true
])

<div class="invoice-filters">
    <form action="{{ request()->url() }}" method="GET" class="row g-3">
        @if($showCustomer)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Cliente</label>
                <select name="customer_id" class="form-select form-select-sm">
                    <option value="">Todos os clientes</option>
                    @foreach($customers as $customer)
                        <option value="{{ $customer->id }}"
                                {{ ($filters['customer_id'] ?? '') == $customer->id ? 'selected' : '' }}>
                            {{ $customer->display_name }}
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
                    @foreach(\App\Enums\InvoiceStatus::cases() as $status)
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
                   placeholder="Buscar por código...">
        </div>

        <div class="col-12">
            <div class="d-flex justify-content-between">
                <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-primary btn-sm">
                        <i class="bi bi-search me-2"></i>Filtrar
                    </button>
                    <a href="{{ route('provider.invoices.index') }}" class="btn btn-outline-secondary btn-sm">
                        <i class="bi bi-x-circle me-2"></i>Limpar
                    </a>
                </div>

                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#createModal">
                        <i class="bi bi-plus-circle me-2"></i>Nova Fatura
                    </button>
                </div>
            </div>
        </div>
    </form>
</div>
```

## 8. Invoice Payments Component

Componente para exibição do histórico de pagamentos da fatura.

### Uso Básico

```blade
<x-invoice.invoice-payments :invoice="$invoice" :showAddPayment="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showAddPayment` | `bool` | Exibir botão para adicionar pagamento | `true` |
| `showBalance` | `bool` | Exibir saldo devedor | `true` |

### Estrutura

```blade
@props([
    'invoice',
    'showAddPayment' => true,
    'showBalance' => true
])

<div class="invoice-payments">
    <!-- Saldo Devedor -->
    @if($showBalance && $invoice->status->isPending())
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0 bg-warning bg-gradient text-white">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <div class="small">Saldo Devedor</div>
                                <div class="h4 mb-0 fw-bold">
                                    R$ {{ number_format($invoice->balance, 2, ',', '.') }}
                                </div>
                            </div>
                            <div class="col-md-4 text-end">
                                <span class="badge bg-light text-dark">{{ $invoice->status->getDescription() }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Histórico de Pagamentos -->
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Histórico de Pagamentos</h6>
        </div>
        <div class="card-body p-0">
            @if($invoice->payments->isNotEmpty())
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Método</th>
                                <th>Valor</th>
                                <th>Status</th>
                                <th class="text-end">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($invoice->payments as $payment)
                                <tr>
                                    <td>{{ $payment->transaction_date?->format('d/m/Y H:i') }}</td>
                                    <td>{{ $payment->payment_method }}</td>
                                    <td class="fw-bold">
                                        R$ {{ number_format($payment->transaction_amount, 2, ',', '.') }}
                                    </td>
                                    <td>
                                        <span class="badge bg-success">{{ $payment->status }}</span>
                                    </td>
                                    <td class="text-end">
                                        <button class="btn btn-outline-info btn-sm" title="Detalhes">
                                            <i class="bi bi-eye"></i>
                                        </button>
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @else
                <div class="text-center py-4">
                    <i class="bi bi-receipt text-muted" style="font-size: 3rem;"></i>
                    <p class="text-muted mt-2">Nenhum pagamento registrado</p>
                </div>
            @endif
        </div>
    </div>

    <!-- Adicionar Pagamento -->
    @if($showAddPayment && $invoice->status->isPending())
        <div class="row mt-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-0">Receber Pagamento</h6>
                                <small class="text-muted">Registre o pagamento da fatura</small>
                            </div>
                            <button type="button"
                                    class="btn btn-success"
                                    data-bs-toggle="modal"
                                    data-bs-target="#paymentModal-{{ $invoice->id }}">
                                <i class="bi bi-cash me-2"></i>Receber Pagamento
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif
</div>
```

## 9. Invoice Totals Component

Componente para exibição detalhada dos totais e valores da fatura.

### Uso Básico

```blade
<x-invoice.invoice-totals :invoice="$invoice" :showBreakdown="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showBreakdown` | `bool` | Exibir detalhamento dos valores | `true` |
| `variant` | `string` | Estilo visual (primary, success, etc.) | `primary` |

### Estrutura

```blade
@props([
    'invoice',
    'showBreakdown' => true,
    'variant' => 'primary'
])

<div class="invoice-totals">
    @if($showBreakdown)
        <div class="row g-3 mb-3">
            <div class="col-md-4">
                <div class="card border-0">
                    <div class="card-body text-center">
                        <div class="text-muted small">Subtotal</div>
                        <div class="h5 mb-0 fw-bold">
                            R$ {{ number_format($invoice->invoiceItems->sum('total'), 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card border-0">
                    <div class="card-body text-center">
                        <div class="text-muted small">Desconto</div>
                        <div class="h5 mb-0 fw-bold text-danger">
                            - R$ {{ number_format($invoice->discount, 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card border-0 bg-{{ $variant }} bg-gradient text-white">
                    <div class="card-body text-center">
                        <div class="small">Valor Total</div>
                        <div class="h4 mb-0 fw-bold">
                            R$ {{ number_format($invoice->total, 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pagamentos -->
        @if($invoice->payments->isNotEmpty())
            <div class="row g-3 mb-3">
                <div class="col-md-4">
                    <div class="card border-0">
                        <div class="card-body text-center">
                            <div class="text-muted small">Total Pago</div>
                            <div class="h5 mb-0 fw-bold text-success">
                                R$ {{ number_format($invoice->payments->sum('transaction_amount'), 2, ',', '.') }}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0">
                        <div class="card-body text-center">
                            <div class="text-muted small">Saldo Devedor</div>
                            <div class="h5 mb-0 fw-bold {{ $invoice->balance > 0 ? 'text-warning' : 'text-success' }}">
                                R$ {{ number_format($invoice->balance, 2, ',', '.') }}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 bg-{{ $invoice->balance > 0 ? 'warning' : 'success' }} bg-gradient text-white">
                        <div class="card-body text-center">
                            <div class="small">Status</div>
                            <div class="h4 mb-0 fw-bold">
                                {{ $invoice->status->getDescription() }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        @endif
    @else
        <div class="card border-0 bg-{{ $variant }} bg-gradient text-white">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <div class="small">Valor Total da Fatura</div>
                        <div class="h3 mb-0 fw-bold">
                            R$ {{ number_format($invoice->total, 2, ',', '.') }}
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <x-invoice.invoice-status :invoice="$invoice" />
                    </div>
                </div>
            </div>
        </div>
    @endif
</div>
```

## 10. Integração com Padrões Existentes

### Uso em Views

```blade
{{-- Dashboard --}}
<x-invoice.invoice-card :invoice="$invoice" />

{{-- Listagem --}}
<x-invoice.invoice-details :invoice="$invoice" />

{{-- Formulários --}}
<x-invoice.invoice-form :invoice="$invoice" :customers="$customers" :services="$services" />

{{-- Ações --}}
<x-invoice.invoice-actions :invoice="$invoice" />
```

### Estilos CSS

```css
/* Invoice Components Styles */
.invoice-form .price-input {
    text-align: right;
}

.invoice-form .item-total {
    background-color: #f8f9fa;
    font-weight: bold;
}

.invoice-actions .btn {
    transition: all 0.2s ease;
}

.invoice-actions .btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.invoice-payments .card {
    border-left: 4px solid #0d6efd;
}

.invoice-payments .card.bg-warning {
    border-left-color: #ffc107;
}
```

## 11. JavaScript Interatividade

### Formulário de Fatura

```javascript
// invoice-form.js
document.addEventListener('DOMContentLoaded', function() {
    // Formatar valores monetários
    document.querySelectorAll('.price-input').forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            this.value = value.replace('.', ',');
            calculateTotals();
        });
    });

    // Calcular totais
    function calculateTotals() {
        let subtotal = 0;
        document.querySelectorAll('.item-row').forEach(row => {
            const quantity = parseFloat(row.querySelector('.quantity-input').value) || 0;
            const unitPrice = parseFloat(row.querySelector('.price-input').value.replace(',', '.')) || 0;
            const total = quantity * unitPrice;
            row.querySelector('.item-total').value = 'R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
            subtotal += total;
        });

        const discount = parseFloat(document.getElementById('discountInput').value.replace(',', '.')) || 0;
        const total = subtotal - discount;

        document.getElementById('subtotalDisplay').textContent = 'R$ ' + subtotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        document.getElementById('totalDisplay').textContent = 'R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    }

    // Adicionar item
    document.getElementById('addInvoiceItem').addEventListener('click', function() {
        const itemsContainer = document.getElementById('invoiceItems');
        const itemCount = itemsContainer.children.length;

        const newRow = document.createElement('div');
        newRow.className = 'row g-3 item-row mb-3';
        newRow.innerHTML = `
            <div class="col-md-6">
                <input type="text" name="items[${itemCount}][description]" class="form-control description-input" placeholder="Descrição do item" required>
            </div>
            <div class="col-md-2">
                <input type="number" name="items[${itemCount}][quantity]" class="form-control quantity-input" placeholder="Qtd" value="1" min="1" required>
            </div>
            <div class="col-md-2">
                <input type="text" name="items[${itemCount}][unit_price]" class="form-control price-input" placeholder="Valor Unitário" required>
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control item-total" placeholder="Total" readonly>
            </div>
        `;

        itemsContainer.appendChild(newRow);
        calculateTotals();
    });

    // Eventos de cálculo
    document.getElementById('invoiceItems').addEventListener('input', calculateTotals);
    document.getElementById('discountInput').addEventListener('input', calculateTotals);

    // Inicializar cálculos
    calculateTotals();
});
```

## 12. Validação e Segurança

### Autorização

```php
// InvoicePolicy.php
public function view(User $user, Invoice $invoice)
{
    return $user->tenant_id === $invoice->tenant_id;
}

public function update(User $user, Invoice $invoice)
{
    return $user->tenant_id === $invoice->tenant_id &&
           $invoice->status->isEditable();
}

public function delete(User $user, Invoice $invoice)
{
    return $user->tenant_id === $invoice->tenant_id &&
           $invoice->status->isDeletable();
}

public function receivePayment(User $user, Invoice $invoice)
{
    return $user->tenant_id === $invoice->tenant_id &&
           $invoice->status->isPending();
}
```

### Validations

```blade
{{-- Invoice Card com validação de permissões --}}
@can('view', $invoice)
    <x-invoice.invoice-card :invoice="$invoice" />
@endcan

{{-- Invoice Actions com validação de status --}}
@can('update', $invoice)
    @if($invoice->status->isEditable())
        <x-invoice.invoice-actions :invoice="$invoice" />
    @endif
@endcan
```

Este padrão de components para faturas garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
