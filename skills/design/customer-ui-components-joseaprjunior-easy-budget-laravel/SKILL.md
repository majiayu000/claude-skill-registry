---
name: customer-ui-components
description: Componentes de UI para clientes seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para Clientes

Esta skill define os componentes Blade específicos para a gestão de clientes no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── customer/
│   ├── customer-card.blade.php       # Card resumido de cliente
│   ├── customer-details.blade.php    # Detalhes completos do cliente
│   ├── customer-form.blade.php       # Formulário de criação/edição
│   ├── customer-status.blade.php     # Badge de status do cliente
│   ├── customer-contact.blade.php    # Informações de contato
│   ├── customer-address.blade.php    # Endereço do cliente
│   ├── customer-actions.blade.php    # Ações disponíveis para cliente
│   ├── customer-filters.blade.php    # Filtros específicos para clientes
│   ├── customer-interactions.blade.php # Histórico de interações
│   └── customer-summary.blade.php    # Resumo do cliente
└── ...
```

## 1. Customer Card Component

Componente para exibição resumida de clientes em listas e dashboards.

### Uso Básico

```blade
<x-customer.customer-card :customer="$customer" :showType="true" :showStatus="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `showType` | `bool` | Exibir tipo de cliente (PF/PJ) | `true` |
| `showStatus` | `bool` | Exibir status do cliente | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'customer',
    'showType' => true,
    'showStatus' => true,
    'variant' => 'primary'
])

<div class="card border-0 shadow-sm h-100">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center gap-3">
                <div class="avatar-circle bg-{{ $variant }} bg-gradient">
                    @if($customer->type === 'pf')
                        <i class="bi bi-person text-white"></i>
                    @else
                        <i class="bi bi-building text-white"></i>
                    @endif
                </div>
                <div>
                    <h6 class="mb-1 fw-bold">{{ $customer->display_name }}</h6>
                    <small class="text-muted">{{ $customer->created_at->format('d/m/Y') }}</small>
                </div>
            </div>
            @if($showStatus)
                <x-customer.customer-status :customer="$customer" />
            @endif
        </div>

        @if($showType)
            <div class="mb-3">
                <span class="badge bg-secondary">{{ $customer->type === 'pf' ? 'Pessoa Física' : 'Pessoa Jurídica' }}</span>
            </div>
        @endif

        @if($customer->contact)
            <div class="mb-3">
                <small class="text-muted">E-mail:</small>
                <div class="fw-semibold">{{ $customer->contact->email }}</div>
            </div>
        @endif

        @if($customer->address)
            <div class="mb-3">
                <small class="text-muted">Endereço:</small>
                <div class="fw-semibold">{{ $customer->address->city }}/{{ $customer->address->state }}</div>
            </div>
        @endif

        <div class="d-flex justify-content-between align-items-center">
            <div>
                <small class="text-muted">Total de Orçamentos</small>
                <div class="h6 mb-0 fw-bold text-{{ $variant }}">
                    {{ $customer->budgets->count() }}
                </div>
            </div>

            <div class="btn-group btn-group-sm" role="group">
                <a href="{{ route('provider.customers.show', $customer) }}" class="btn btn-outline-primary">
                    <i class="bi bi-eye"></i> Ver
                </a>
                <a href="{{ route('provider.customers.edit', $customer) }}" class="btn btn-outline-secondary">
                    <i class="bi bi-pencil"></i> Editar
                </a>
            </div>
        </div>
    </div>
</div>
```

## 2. Customer Details Component

Componente para exibição detalhada de informações do cliente.

### Uso Básico

```blade
<x-customer.customer-details :customer="$customer" :showContact="true" :showAddress="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `showContact` | `bool` | Exibir informações de contato | `true` |
| `showAddress` | `bool` | Exibir endereço | `true` |
| `collapsible` | `bool` | Permitir colapsar seções | `false` |

### Estrutura

```blade
@props([
    'customer',
    'showContact' => true,
    'showAddress' => true,
    'collapsible' => false
])

<div class="customer-details">
    <!-- Informações Básicas -->
    <div class="row g-3 mb-3">
        <div class="col-md-4">
            <div class="info-item">
                <label class="text-muted small">Nome/Razão Social</label>
                <div class="fw-bold">{{ $customer->display_name }}</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="info-item">
                <label class="text-muted small">Tipo</label>
                <div class="fw-bold">
                    <span class="badge bg-secondary">{{ $customer->type === 'pf' ? 'Pessoa Física' : 'Pessoa Jurídica' }}</span>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="info-item">
                <label class="text-muted small">Status</label>
                <x-customer.customer-status :customer="$customer" />
            </div>
        </div>
    </div>

    <!-- Dados Pessoais/Empresariais -->
    @if($customer->commonData)
        <div class="row mb-3">
            <div class="col-12">
                <div class="card border-0">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">{{ $customer->type === 'pf' ? 'Dados Pessoais' : 'Dados Empresariais' }}</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            @if($customer->type === 'pf')
                                <div class="col-md-6">
                                    <div class="mb-2">
                                        <label class="text-muted small">Nome Completo</label>
                                        <div class="fw-bold">{{ $customer->commonData->first_name }} {{ $customer->commonData->last_name }}</div>
                                    </div>
                                    <div class="mb-2">
                                        <label class="text-muted small">Data de Nascimento</label>
                                        <div class="fw-bold">{{ $customer->commonData->birth_date?->format('d/m/Y') ?? 'Não informado' }}</div>
                                    </div>
                                    @if($customer->commonData->cpf)
                                        <div class="mb-2">
                                            <label class="text-muted small">CPF</label>
                                            <div class="fw-bold">{{ \App\Helpers\DocumentHelper::formatCpf($customer->commonData->cpf) }}</div>
                                        </div>
                                    @endif
                                </div>
                            @else
                                <div class="col-md-6">
                                    <div class="mb-2">
                                        <label class="text-muted small">Razão Social</label>
                                        <div class="fw-bold">{{ $customer->commonData->company_name }}</div>
                                    </div>
                                    @if($customer->commonData->cnpj)
                                        <div class="mb-2">
                                            <label class="text-muted small">CNPJ</label>
                                            <div class="fw-bold">{{ \App\Helpers\DocumentHelper::formatCnpj($customer->commonData->cnpj) }}</div>
                                        </div>
                                    @endif
                                    @if($customer->commonData->cpf)
                                        <div class="mb-2">
                                            <label class="text-muted small">CPF do Responsável</label>
                                            <div class="fw-bold">{{ \App\Helpers\DocumentHelper::formatCpf($customer->commonData->cpf) }}</div>
                                        </div>
                                    @endif
                                </div>
                            @endif

                            <div class="col-md-6">
                                @if($customer->commonData->areaOfActivity)
                                    <div class="mb-2">
                                        <label class="text-muted small">Área de Atuação</label>
                                        <div class="fw-bold">{{ $customer->commonData->areaOfActivity->name }}</div>
                                    </div>
                                @endif
                                @if($customer->commonData->profession)
                                    <div class="mb-2">
                                        <label class="text-muted small">Profissão</label>
                                        <div class="fw-bold">{{ $customer->commonData->profession->name }}</div>
                                    </div>
                                @endif
                                @if($customer->commonData->description)
                                    <div class="mb-2">
                                        <label class="text-muted small">Descrição</label>
                                        <div class="fw-bold">{{ $customer->commonData->description }}</div>
                                    </div>
                                @endif
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    @endif

    <!-- Contato -->
    @if($showContact && $customer->contact)
        <x-customer.customer-contact :contact="$customer->contact" />
    @endif

    <!-- Endereço -->
    @if($showAddress && $customer->address)
        <x-customer.customer-address :address="$customer->address" />
    @endif

    <!-- Resumo -->
    <x-customer.customer-summary :customer="$customer" />
</div>
```

## 3. Customer Status Component

Componente para exibição do status do cliente com cores e ícones apropriados.

### Uso Básico

```blade
<x-customer.customer-status :customer="$customer" :showIcon="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `showIcon` | `bool` | Exibir ícone ao lado do status | `true` |
| `size` | `string` | Tamanho do badge (sm, md, lg) | `md` |

### Estrutura

```blade
@props([
    'customer',
    'showIcon' => true,
    'size' => 'md'
])

@php
    $status = $customer->status;
    $color = match($status) {
        'active' => '#198754', // Verde
        'inactive' => '#6c757d', // Cinza
        'pending' => '#ffc107', // Amarelo
        default => '#6c757d'
    };

    $icon = match($status) {
        'active' => 'check-circle',
        'inactive' => 'x-circle',
        'pending' => 'clock',
        default => 'circle'
    };

    $description = match($status) {
        'active' => 'Ativo',
        'inactive' => 'Inativo',
        'pending' => 'Pendente',
        default => 'Status Desconhecido'
    };

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

## 4. Customer Contact Component

Componente para exibição de informações de contato do cliente.

### Uso Básico

```blade
<x-customer.customer-contact :contact="$contact" :showBusiness="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `contact` | `Contact` | Modelo de contato | Obrigatório |
| `showBusiness` | `bool` | Exibir contatos comerciais | `true` |
| `showWebsite` | `bool` | Exibir website | `true` |

### Estrutura

```blade
@props([
    'contact',
    'showBusiness' => true,
    'showWebsite' => true
])

<div class="customer-contact">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Informações de Contato</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="text-muted small">E-mail Principal</label>
                        <div class="fw-bold">{{ $contact->email }}</div>
                    </div>
                    @if($contact->phone)
                        <div class="mb-3">
                            <label class="text-muted small">Telefone</label>
                            <div class="fw-bold">{{ $contact->phone }}</div>
                        </div>
                    @endif
                </div>

                @if($showBusiness)
                    <div class="col-md-6">
                        @if($contact->email_business)
                            <div class="mb-3">
                                <label class="text-muted small">E-mail Comercial</label>
                                <div class="fw-bold">{{ $contact->email_business }}</div>
                            </div>
                        @endif
                        @if($contact->phone_business)
                            <div class="mb-3">
                                <label class="text-muted small">Telefone Comercial</label>
                                <div class="fw-bold">{{ $contact->phone_business }}</div>
                            </div>
                        @endif
                    </div>
                @endif
            </div>

            @if($showWebsite && $contact->website)
                <div class="row">
                    <div class="col-12">
                        <div class="mb-3">
                            <label class="text-muted small">Website</label>
                            <div class="fw-bold">
                                <a href="{{ $contact->website }}" target="_blank" class="text-decoration-none">
                                    {{ $contact->website }}
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 5. Customer Address Component

Componente para exibição de endereço do cliente.

### Uso Básico

```blade
<x-customer.customer-address :address="$address" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `address` | `Address` | Modelo de endereço | Obrigatório |

### Estrutura

```blade
@props(['address'])

<div class="customer-address">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Endereço</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <div class="mb-2">
                        <label class="text-muted small">Logradouro</label>
                        <div class="fw-bold">
                            {{ $address->address }}, {{ $address->address_number }}
                            @if($address->address_complement)
                                - {{ $address->address_complement }}
                            @endif
                        </div>
                    </div>
                    <div class="mb-2">
                        <label class="text-muted small">Bairro</label>
                        <div class="fw-bold">{{ $address->neighborhood }}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="mb-2">
                        <label class="text-muted small">CEP</label>
                        <div class="fw-bold">{{ $address->cep }}</div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-2">
                        <label class="text-muted small">Cidade</label>
                        <div class="fw-bold">{{ $address->city }}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-2">
                        <label class="text-muted small">Estado</label>
                        <div class="fw-bold">{{ $address->state }}</div>
                    </div>
                </div>
            </div>
            @if($address->country && $address->country !== 'Brasil')
                <div class="row">
                    <div class="col-12">
                        <div class="mb-2">
                            <label class="text-muted small">País</label>
                            <div class="fw-bold">{{ $address->country }}</div>
                        </div>
                    </div>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 6. Customer Form Component

Componente para formulário de criação e edição de clientes.

### Uso Básico

```blade
<x-customer.customer-form :customer="$customer ?? null" :areasOfActivity="$areasOfActivity" :professions="$professions" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer|null` | Modelo do cliente (para edição) | `null` |
| `areasOfActivity` | `Collection` | Áreas de atuação disponíveis | Obrigatório |
| `professions` | `Collection` | Profissões disponíveis | Obrigatório |
| `type` | `string` | Tipo de cliente (pf/pj) | `pf` |

### Estrutura

```blade
@props([
    'customer' => null,
    'areasOfActivity' => [],
    'professions' => [],
    'type' => 'pf'
])

<div class="customer-form">
    <form action="{{ isset($customer) ? route('provider.customers.update', $customer) : route('provider.customers.store') }}"
          method="POST"
          id="customerForm">
        @csrf
        @if(isset($customer)) @method('PUT') @endif

        <!-- Tipo de Cliente -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Tipo de Cliente *</label>
                                <div class="btn-group w-100" role="group">
                                    <input type="radio" class="btn-check" name="type" id="type_pf" value="pf"
                                           {{ (old('type', $customer->type ?? $type) == 'pf') ? 'checked' : '' }} required>
                                    <label class="btn btn-outline-primary" for="type_pf">
                                        <i class="bi bi-person me-2"></i>Pessoa Física
                                    </label>

                                    <input type="radio" class="btn-check" name="type" id="type_pj" value="pj"
                                           {{ (old('type', $customer->type ?? $type) == 'pj') ? 'checked' : '' }} required>
                                    <label class="btn btn-outline-secondary" for="type_pj">
                                        <i class="bi bi-building me-2"></i>Pessoa Jurídica
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Dados Pessoais/Empresariais -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">{{ $type === 'pf' ? 'Dados Pessoais' : 'Dados Empresariais' }}</h6>
                    </div>
                    <div class="card-body">
                        @if($type === 'pf')
                            <!-- Pessoa Física -->
                            <div class="row">
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Nome *</label>
                                    <input type="text"
                                           name="first_name"
                                           class="form-control @error('first_name') is-invalid @enderror"
                                           value="{{ old('first_name', $customer->commonData->first_name ?? '') }}" required>
                                    @error('first_name')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Sobrenome *</label>
                                    <input type="text"
                                           name="last_name"
                                           class="form-control @error('last_name') is-invalid @enderror"
                                           value="{{ old('last_name', $customer->commonData->last_name ?? '') }}" required>
                                    @error('last_name')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Data de Nascimento</label>
                                    <input type="date"
                                           name="birth_date"
                                           class="form-control @error('birth_date') is-invalid @enderror"
                                           value="{{ old('birth_date', $customer->commonData->birth_date?->format('Y-m-d') ?? '') }}">
                                    @error('birth_date')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-muted text-uppercase">CPF *</label>
                                    <input type="text"
                                           name="cpf"
                                           class="form-control @error('cpf') is-invalid @enderror"
                                           value="{{ old('cpf', $customer->commonData->cpf ?? '') }}" required>
                                    @error('cpf')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                            </div>
                        @else
                            <!-- Pessoa Jurídica -->
                            <div class="row">
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-muted text-uppercase">Razão Social *</label>
                                    <input type="text"
                                           name="company_name"
                                           class="form-control @error('company_name') is-invalid @enderror"
                                           value="{{ old('company_name', $customer->commonData->company_name ?? '') }}" required>
                                    @error('company_name')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-muted text-uppercase">CNPJ *</label>
                                    <input type="text"
                                           name="cnpj"
                                           class="form-control @error('cnpj') is-invalid @enderror"
                                           value="{{ old('cnpj', $customer->commonData->cnpj ?? '') }}" required>
                                    @error('cnpj')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-muted text-uppercase">CPF do Responsável</label>
                                    <input type="text"
                                           name="cpf"
                                           class="form-control @error('cpf') is-invalid @enderror"
                                           value="{{ old('cpf', $customer->commonData->cpf ?? '') }}">
                                    @error('cpf')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                            </div>
                        @endif

                        <div class="row mt-3">
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Área de Atuação</label>
                                <select name="area_of_activity_id" class="form-select @error('area_of_activity_id') is-invalid @enderror">
                                    <option value="">Selecione uma área</option>
                                    @foreach($areasOfActivity as $area)
                                        <option value="{{ $area->id }}"
                                                {{ (old('area_of_activity_id', $customer->commonData->area_of_activity_id ?? '') == $area->id) ? 'selected' : '' }}>
                                            {{ $area->name }}
                                        </option>
                                    @endforeach
                                </select>
                                @error('area_of_activity_id')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Profissão</label>
                                <select name="profession_id" class="form-select @error('profession_id') is-invalid @enderror">
                                    <option value="">Selecione uma profissão</option>
                                    @foreach($professions as $profession)
                                        <option value="{{ $profession->id }}"
                                                {{ (old('profession_id', $customer->commonData->profession_id ?? '') == $profession->id) ? 'selected' : '' }}>
                                            {{ $profession->name }}
                                        </option>
                                    @endforeach
                                </select>
                                @error('profession_id')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>

                        <div class="row mt-3">
                            <div class="col-12">
                                <label class="form-label small fw-bold text-muted text-uppercase">Descrição</label>
                                <textarea name="description"
                                          class="form-control @error('description') is-invalid @enderror"
                                          rows="3"
                                          placeholder="Descrição do cliente...">{{ old('description', $customer->commonData->description ?? '') }}</textarea>
                                @error('description')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contato -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Informações de Contato</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">E-mail Principal *</label>
                                <input type="email"
                                       name="email"
                                       class="form-control @error('email') is-invalid @enderror"
                                       value="{{ old('email', $customer->contact->email ?? '') }}" required>
                                @error('email')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Telefone</label>
                                <input type="tel"
                                       name="phone"
                                       class="form-control @error('phone') is-invalid @enderror"
                                       value="{{ old('phone', $customer->contact->phone ?? '') }}">
                                @error('phone')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">E-mail Comercial</label>
                                <input type="email"
                                       name="email_business"
                                       class="form-control @error('email_business') is-invalid @enderror"
                                       value="{{ old('email_business', $customer->contact->email_business ?? '') }}">
                                @error('email_business')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Telefone Comercial</label>
                                <input type="tel"
                                       name="phone_business"
                                       class="form-control @error('phone_business') is-invalid @enderror"
                                       value="{{ old('phone_business', $customer->contact->phone_business ?? '') }}">
                                @error('phone_business')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Website</label>
                                <input type="url"
                                       name="website"
                                       class="form-control @error('website') is-invalid @enderror"
                                       value="{{ old('website', $customer->contact->website ?? '') }}">
                                @error('website')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Endereço -->
        <div class="row g-3 mb-4">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Endereço</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <label class="form-label small fw-bold text-muted text-uppercase">Logradouro *</label>
                                <input type="text"
                                       name="address"
                                       class="form-control @error('address') is-invalid @enderror"
                                       value="{{ old('address', $customer->address->address ?? '') }}" required>
                                @error('address')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold text-muted text-uppercase">Número *</label>
                                <input type="text"
                                       name="address_number"
                                       class="form-control @error('address_number') is-invalid @enderror"
                                       value="{{ old('address_number', $customer->address->address_number ?? '') }}" required>
                                @error('address_number')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Complemento</label>
                                <input type="text"
                                       name="address_complement"
                                       class="form-control @error('address_complement') is-invalid @enderror"
                                       value="{{ old('address_complement', $customer->address->address_complement ?? '') }}">
                                @error('address_complement')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">Bairro *</label>
                                <input type="text"
                                       name="neighborhood"
                                       class="form-control @error('neighborhood') is-invalid @enderror"
                                       value="{{ old('neighborhood', $customer->address->neighborhood ?? '') }}" required>
                                @error('neighborhood')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold text-muted text-uppercase">CEP *</label>
                                <input type="text"
                                       name="cep"
                                       class="form-control @error('cep') is-invalid @enderror"
                                       value="{{ old('cep', $customer->address->cep ?? '') }}" required>
                                @error('cep')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold text-muted text-uppercase">Cidade *</label>
                                <input type="text"
                                       name="city"
                                       class="form-control @error('city') is-invalid @enderror"
                                       value="{{ old('city', $customer->address->city ?? '') }}" required>
                                @error('city')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold text-muted text-uppercase">Estado *</label>
                                <input type="text"
                                       name="state"
                                       class="form-control @error('state') is-invalid @enderror"
                                       value="{{ old('state', $customer->address->state ?? '') }}" required>
                                @error('state')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold text-muted text-uppercase">País</label>
                                <input type="text"
                                       name="country"
                                       class="form-control @error('country') is-invalid @enderror"
                                       value="{{ old('country', $customer->address->country ?? 'Brasil') }}">
                                @error('country')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Ações -->
        <div class="d-flex justify-content-between">
            <a href="{{ route('provider.customers.index') }}" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-2"></i>Cancelar
            </a>
            <button type="submit" class="btn btn-primary">
                <i class="bi bi-check-circle me-2"></i>{{ isset($customer) ? 'Atualizar' : 'Criar' }} Cliente
            </button>
        </div>
    </form>
</div>

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Formatar CPF/CNPJ
    const cpfInput = document.querySelector('input[name="cpf"]');
    const cnpjInput = document.querySelector('input[name="cnpj"]');

    if (cpfInput) {
        cpfInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            if (value.length > 3) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
            }
            if (value.length > 7) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
            }
            if (value.length > 11) {
                value = value.replace(/(\d{3})(\d{1})$/, '$1-$2');
            }
            this.value = value;
        });
    }

    if (cnpjInput) {
        cnpjInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 14) value = value.slice(0, 14);
            if (value.length > 2) {
                value = value.replace(/(\d{2})(\d)/, '$1.$2');
            }
            if (value.length > 6) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
            }
            if (value.length > 10) {
                value = value.replace(/(\d{3})(\d)/, '$1/$2');
            }
            if (value.length > 15) {
                value = value.replace(/(\d{4})(\d{1})$/, '$1-$2');
            }
            this.value = value;
        });
    }

    // Formatar CEP
    const cepInput = document.querySelector('input[name="cep"]');
    if (cepInput) {
        cepInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 8) value = value.slice(0, 8);
            if (value.length > 5) {
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            }
            this.value = value;
        });
    }
});
</script>
@endpush
```

## 7. Customer Actions Component

Componente para exibição de ações disponíveis para um cliente.

### Uso Básico

```blade
<x-customer.customer-actions :customer="$customer" :showBudget="true" :showInvoice="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `showBudget` | `bool` | Exibir botão de novo orçamento | `true` |
| `showInvoice` | `bool` | Exibir botão de nova fatura | `true` |
| `showSendEmail` | `bool` | Exibir botão de envio de e-mail | `true` |

### Estrutura

```blade
@props([
    'customer',
    'showBudget' => true,
    'showInvoice' => true,
    'showSendEmail' => true
])

<div class="customer-actions btn-group" role="group">
    <!-- Visualizar -->
    <a href="{{ route('provider.customers.show', $customer) }}"
       class="btn btn-outline-primary"
       title="Visualizar Cliente">
        <i class="bi bi-eye"></i> Visualizar
    </a>

    <!-- Editar -->
    <a href="{{ route('provider.customers.edit', $customer) }}"
       class="btn btn-outline-secondary"
       title="Editar Cliente">
        <i class="bi bi-pencil"></i> Editar
    </a>

    <!-- Novo Orçamento -->
    @if($showBudget)
        <a href="{{ route('provider.budgets.create') }}?customer_id={{ $customer->id }}"
           class="btn btn-outline-info"
           title="Novo Orçamento">
            <i class="bi bi-file-earmark-text"></i> Orçamento
        </a>
    @endif

    <!-- Nova Fatura -->
    @if($showInvoice)
        <a href="{{ route('provider.invoices.create') }}?customer_id={{ $customer->id }}"
           class="btn btn-outline-success"
           title="Nova Fatura">
            <i class="bi bi-receipt"></i> Fatura
        </a>
    @endif

    <!-- Enviar E-mail -->
    @if($showSendEmail)
        <button type="button"
                class="btn btn-outline-warning"
                data-bs-toggle="modal"
                data-bs-target="#emailModal-{{ $customer->id }}"
                title="Enviar E-mail">
            <i class="bi bi-envelope"></i> E-mail
        </button>
    @endif

    <!-- Excluir -->
    <button type="button"
            class="btn btn-outline-danger"
            data-bs-toggle="modal"
            data-bs-target="#deleteModal-{{ $customer->id }}"
            title="Excluir Cliente">
        <i class="bi bi-trash"></i> Excluir
    </button>
</div>
```

## 8. Customer Filters Component

Componente para filtros específicos de listagem de clientes.

### Uso Básico

```blade
<x-customer.customer-filters :filters="$filters" :showType="true" :showStatus="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `filters` | `array` | Filtros atuais | `[]` |
| `showType` | `bool` | Exibir filtro por tipo | `true` |
| `showStatus` | `bool` | Exibir filtro por status | `true` |
| `showDateRange` | `bool` | Exibir filtro por período | `true` |

### Estrutura

```blade
@props([
    'filters' => [],
    'showType' => true,
    'showStatus' => true,
    'showDateRange' => true
])

<div class="customer-filters">
    <form action="{{ request()->url() }}" method="GET" class="row g-3">
        @if($showType)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Tipo</label>
                <select name="type" class="form-select form-select-sm">
                    <option value="">Todos os tipos</option>
                    <option value="pf" {{ ($filters['type'] ?? '') == 'pf' ? 'selected' : '' }}>Pessoa Física</option>
                    <option value="pj" {{ ($filters['type'] ?? '') == 'pj' ? 'selected' : '' }}>Pessoa Jurídica</option>
                </select>
            </div>
        @endif

        @if($showStatus)
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Status</label>
                <select name="status" class="form-select form-select-sm">
                    <option value="">Todos os status</option>
                    <option value="active" {{ ($filters['status'] ?? '') == 'active' ? 'selected' : '' }}>Ativo</option>
                    <option value="inactive" {{ ($filters['status'] ?? '') == 'inactive' ? 'selected' : '' }}>Inativo</option>
                    <option value="pending" {{ ($filters['status'] ?? '') == 'pending' ? 'selected' : '' }}>Pendente</option>
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
                   placeholder="Buscar por nome...">
        </div>

        <div class="col-12">
            <div class="d-flex justify-content-between">
                <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-primary btn-sm">
                        <i class="bi bi-search me-2"></i>Filtrar
                    </button>
                    <a href="{{ route('provider.customers.index') }}" class="btn btn-outline-secondary btn-sm">
                        <i class="bi bi-x-circle me-2"></i>Limpar
                    </a>
                </div>

                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#createModal">
                        <i class="bi bi-plus-circle me-2"></i>Novo Cliente
                    </button>
                </div>
            </div>
        </div>
    </form>
</div>
```

## 9. Customer Interactions Component

Componente para exibição do histórico de interações do cliente.

### Uso Básico

```blade
<x-customer.customer-interactions :customer="$customer" :showRecent="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `showRecent` | `bool` | Exibir apenas interações recentes | `true` |
| `limit` | `int` | Limite de interações a exibir | `10` |

### Estrutura

```blade
@props([
    'customer',
    'showRecent' => true,
    'limit' => 10
])

<div class="customer-interactions">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Histórico de Interações</h6>
        </div>
        <div class="card-body p-0">
            @if($customer->activities->isNotEmpty())
                <div class="list-group list-group-flush">
                    @foreach($customer->activities->take($limit) as $activity)
                        <div class="list-group-item">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">{{ $activity->description }}</h6>
                                <small class="text-muted">{{ $activity->created_at->diffForHumans() }}</small>
                            </div>
                            <p class="mb-1 text-muted small">{{ $activity->metadata }}</p>
                            <small class="text-muted">{{ $activity->action_type }}</small>
                        </div>
                    @endforeach
                </div>
            @else
                <div class="text-center py-4">
                    <i class="bi bi-chat-dots text-muted" style="font-size: 3rem;"></i>
                    <p class="text-muted mt-2">Nenhuma interação registrada</p>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 10. Customer Summary Component

Componente para exibição de resumo do cliente.

### Uso Básico

```blade
<x-customer.customer-summary :customer="$customer" :showStats="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `showStats` | `bool` | Exibir estatísticas | `true` |
| `showLastInteraction` | `bool` | Exibir última interação | `true` |

### Estrutura

```blade
@props([
    'customer',
    'showStats' => true,
    'showLastInteraction' => true
])

<div class="customer-summary">
    <div class="row g-3">
        @if($showStats)
            <!-- Estatísticas -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <div class="avatar-circle bg-primary bg-gradient mb-2 mx-auto">
                            <i class="bi bi-file-earmark-text text-white"></i>
                        </div>
                        <div class="text-muted small">Orçamentos</div>
                        <div class="h4 mb-0 fw-bold">{{ $customer->budgets->count() }}</div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <div class="avatar-circle bg-success bg-gradient mb-2 mx-auto">
                            <i class="bi bi-receipt text-white"></i>
                        </div>
                        <div class="text-muted small">Faturas</div>
                        <div class="h4 mb-0 fw-bold">{{ $customer->invoices->count() }}</div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card border-0 shadow-sm">
                    <div class="card-body text-center">
                        <div class="avatar-circle bg-info bg-gradient mb-2 mx-auto">
                            <i class="bi bi-currency-dollar text-white"></i>
                        </div>
                        <div class="text-muted small">Valor Total</div>
                        <div class="h4 mb-0 fw-bold">
                            R$ {{ number_format($customer->invoices->sum('total'), 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </div>
        @endif
    </div>

    @if($showLastInteraction && $customer->activities->isNotEmpty())
        <div class="row mt-3">
            <div class="col-12">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-transparent border-0">
                        <h6 class="mb-0">Última Interação</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-flex w-100 justify-content-between">
                            <div>
                                <h6 class="mb-1">{{ $customer->activities->first()->description }}</h6>
                                <p class="mb-0 text-muted small">{{ $customer->activities->first()->metadata }}</p>
                            </div>
                            <div class="text-end">
                                <small class="text-muted">{{ $customer->activities->first()->created_at->format('d/m/Y H:i') }}</small>
                                <br>
                                <small class="text-muted">{{ $customer->activities->first()->action_type }}</small>
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
<x-customer.customer-card :customer="$customer" />

{{-- Listagem --}}
<x-customer.customer-details :customer="$customer" />

{{-- Formulários --}}
<x-customer.customer-form :customer="$customer" :areasOfActivity="$areasOfActivity" :professions="$professions" />

{{-- Ações --}}
<x-customer.customer-actions :customer="$customer" />
```

### Estilos CSS

```css
/* Customer Components Styles */
.customer-form .btn-check:checked + .btn {
    background-color: #0d6efd;
    border-color: #0d6efd;
    color: white;
}

.customer-form .btn-check:checked + .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
}

.customer-actions .btn {
    transition: all 0.2s ease;
}

.customer-actions .btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.customer-summary .card {
    border-left: 4px solid #0d6efd;
}
```

## 12. JavaScript Interatividade

### Formulário de Cliente

```javascript
// customer-form.js
document.addEventListener('DOMContentLoaded', function() {
    // Alternar campos conforme tipo de cliente
    const typeRadios = document.querySelectorAll('input[name="type"]');
    const cpfField = document.querySelector('input[name="cpf"]');
    const cnpjField = document.querySelector('input[name="cnpj"]');

    function toggleFields() {
        const selectedType = document.querySelector('input[name="type"]:checked').value;

        if (selectedType === 'pf') {
            cnpjField.closest('.row').style.display = 'none';
            cpfField.closest('.row').style.display = 'block';
        } else {
            cnpjField.closest('.row').style.display = 'block';
            cpfField.closest('.row').style.display = 'block';
        }
    }

    typeRadios.forEach(radio => {
        radio.addEventListener('change', toggleFields);
    });

    // Inicializar campos
    toggleFields();
});
```

## 13. Validação e Segurança

### Autorização

```php
// CustomerPolicy.php
public function view(User $user, Customer $customer)
{
    return $user->tenant_id === $customer->tenant_id;
}

public function update(User $user, Customer $customer)
{
    return $user->tenant_id === $customer->tenant_id;
}

public function delete(User $user, Customer $customer)
{
    return $user->tenant_id === $customer->tenant_id &&
           $customer->budgets->isEmpty() &&
           $customer->invoices->isEmpty();
}
```

### Validations

```blade
{{-- Customer Card com validação de permissões --}}
@can('view', $customer)
    <x-customer.customer-card :customer="$customer" />
@endcan

{{-- Customer Actions com validação de status --}}
@can('update', $customer)
    <x-customer.customer-actions :customer="$customer" />
@endcan
```

Este padrão de components para clientes garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
