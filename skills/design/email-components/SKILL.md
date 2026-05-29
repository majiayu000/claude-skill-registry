---
name: email-components
description: Componentes de UI para geração e visualização de e-mails seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para E-mails

Esta skill define os componentes Blade específicos para a geração e visualização de e-mails no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── email/
│   ├── email-header.blade.php        # Cabeçalho padrão de e-mails
│   ├── email-footer.blade.php        # Rodapé padrão de e-mails
│   ├── email-layout.blade.php        # Layout base de e-mails
│   ├── email-budget.blade.php        # Template de e-mail de orçamento
│   ├── email-invoice.blade.php       # Template de e-mail de fatura
│   ├── email-reminder.blade.php      # Template de e-mail de lembrete
│   ├── email-welcome.blade.php       # Template de e-mail de boas-vindas
│   ├── email-verification.blade.php  # Template de e-mail de verificação
│   ├── email-password.blade.php      # Template de e-mail de senha
│   ├── email-support.blade.php       # Template de e-mail de suporte
│   └── email-styles.blade.php        # Estilos CSS para e-mails
└── ...
```

## 1. Email Header Component

Componente para cabeçalho padrão de e-mails.

### Uso Básico

```blade
<x-email.email-header :title="$title" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do e-mail | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'title',
    'company' => [],
    'showLogo' => true
])

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title }}</title>
    <x-email.email-styles />
</head>
<body>
    <div class="email-container">
        <!-- Cabeçalho -->
        <header class="email-header">
            <div class="header-content">
                @if($showLogo && !empty($company['logo']))
                    <div class="company-logo">
                        <img src="{{ $company['logo_url'] ?? asset('storage/' . $company['logo']) }}"
                             alt="{{ $company['name'] ?? 'Easy Budget' }}"
                             style="max-height: 60px;">
                    </div>
                @endif

                <div class="company-info">
                    <h1 class="company-name">{{ $company['name'] ?? 'Easy Budget' }}</h1>
                    <div class="company-tagline">{{ $company['tagline'] ?? 'Sua solução de gestão empresarial' }}</div>
                </div>
            </div>
        </header>
```

## 2. Email Footer Component

Componente para rodapé padrão de e-mails.

### Uso Básico

```blade
<x-email.email-footer :company="$company" :unsubscribeUrl="$unsubscribeUrl" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `company` | `array` | Dados da empresa | `[]` |
| `unsubscribeUrl` | `string` | URL para cancelamento de inscrição | `null` |
| `showSocial` | `bool` | Exibir links sociais | `true` |

### Estrutura

```blade
@props([
    'company' => [],
    'unsubscribeUrl' => null,
    'showSocial' => true
])

        <!-- Rodapé -->
        <footer class="email-footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{{ $company['name'] ?? 'Easy Budget' }}</h3>
                    <p class="footer-description">
                        {{ $company['description'] ?? 'Sua solução de gestão empresarial completa.' }}
                    </p>
                </div>

                <div class="footer-section">
                    <h4>Contato</h4>
                    <div class="contact-info">
                        @if(!empty($company['email']))
                            <div class="contact-item">
                                <i class="bi bi-envelope"></i>
                                <a href="mailto:{{ $company['email'] }}">{{ $company['email'] }}</a>
                            </div>
                        @endif
                        @if(!empty($company['phone']))
                            <div class="contact-item">
                                <i class="bi bi-telephone"></i>
                                <span>{{ $company['phone'] }}</span>
                            </div>
                        @endif
                        @if(!empty($company['website']))
                            <div class="contact-item">
                                <i class="bi bi-globe"></i>
                                <a href="{{ $company['website'] }}" target="_blank">{{ $company['website'] }}</a>
                            </div>
                        @endif
                    </div>
                </div>

                @if($showSocial && !empty($company['social']))
                    <div class="footer-section">
                        <h4>Siga-nos</h4>
                        <div class="social-links">
                            @foreach($company['social'] as $social)
                                <a href="{{ $social['url'] }}" target="_blank" class="social-link">
                                    <i class="bi bi-{{ $social['icon'] }}"></i>
                                </a>
                            @endforeach
                        </div>
                    </div>
                @endif
            </div>

            <div class="footer-bottom">
                <div class="footer-text">
                    © {{ date('Y') }} {{ $company['name'] ?? 'Easy Budget' }}. Todos os direitos reservados.
                </div>

                @if($unsubscribeUrl)
                    <div class="footer-text">
                        <a href="{{ $unsubscribeUrl }}" class="unsubscribe-link">Cancelar inscrição</a>
                    </div>
                @endif
            </div>
        </footer>
    </div>
</body>
</html>
```

## 3. Email Layout Component

Componente para layout base de e-mails.

### Uso Básico

```blade
<x-email.email-layout :title="$title" :company="$company" :content="$content" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do e-mail | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `content` | `string` | Conteúdo do e-mail | Obrigatório |
| `showHeader` | `bool` | Exibir cabeçalho | `true` |
| `showFooter` | `bool` | Exibir rodapé | `true` |

### Estrutura

```blade
@props([
    'title',
    'company' => [],
    'content',
    'showHeader' => true,
    'showFooter' => true
])

<x-email.email-header :title="$title" :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            {!! $content !!}
        </main>

<x-email.email-footer :company="$company" />
```

## 4. Email Budget Component

Componente para template de e-mail de orçamento.

### Uso Básico

```blade
<x-email.email-budget :budget="$budget" :customer="$customer" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `budget` | `Budget` | Modelo do orçamento | Obrigatório |
| `customer` | `Customer` | Cliente do orçamento | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `actionUrl` | `string` | URL de ação (visualizar orçamento) | `null` |

### Estrutura

```blade
@props([
    'budget',
    'customer',
    'company' => [],
    'actionUrl' => null
])

<x-email.email-header
    :title="'Orçamento #' . $budget->code . ' - ' . $customer->display_name"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero">
                <h2 class="hero-title">Novo Orçamento Disponível</h2>
                <p class="hero-subtitle">Olá {{ $customer->display_name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>Detalhes do Orçamento</h3>
                    <div class="budget-details">
                        <div class="detail-row">
                            <span class="detail-label">Número:</span>
                            <span class="detail-value">{{ $budget->code }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Data:</span>
                            <span class="detail-value">{{ $budget->created_at->format('d/m/Y') }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Validade:</span>
                            <span class="detail-value">{{ $budget->due_date?->format('d/m/Y') ?? 'Indeterminado' }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Status:</span>
                            <span class="status-badge status-{{ $budget->status }}">
                                {{ ucfirst($budget->status) }}
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Total:</span>
                            <span class="detail-value total-amount">
                                R$ {{ number_format($budget->total, 2, ',', '.') }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Serviços -->
                @if($budget->services->isNotEmpty())
                    <div class="content-section">
                        <h3>Serviços Incluídos</h3>
                        <div class="services-list">
                            @foreach($budget->services as $service)
                                <div class="service-item">
                                    <div class="service-info">
                                        <div class="service-code">{{ $service->code }}</div>
                                        <div class="service-description">{{ $service->description }}</div>
                                    </div>
                                    <div class="service-price">
                                        R$ {{ number_format($service->total - $service->discount, 2, ',', '.') }}
                                    </div>
                                </div>
                            @endforeach
                        </div>
                    </div>
                @endif

                <!-- Observações -->
                @if($budget->description)
                    <div class="content-section">
                        <h3>Observações</h3>
                        <div class="observations">
                            {{ $budget->description }}
                        </div>
                    </div>
                @endif

                <!-- Ações -->
                @if($actionUrl)
                    <div class="content-section">
                        <h3>Próximos Passos</h3>
                        <div class="action-buttons">
                            <a href="{{ $actionUrl }}" class="btn-primary">
                                Visualizar Orçamento
                            </a>
                            <a href="{{ route('provider.budgets.index') }}" class="btn-secondary">
                                Ver Todos os Orçamentos
                            </a>
                        </div>
                    </div>
                @endif

                <!-- Termos -->
                <div class="content-section">
                    <h3>Termos e Condições</h3>
                    <div class="terms">
                        <p>
                            Este orçamento tem validade de 30 dias a partir da data de emissão.
                            Para aceitar este orçamento, por favor entre em contato conosco.
                        </p>
                    </div>
                </div>
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 5. Email Invoice Component

Componente para template de e-mail de fatura.

### Uso Básico

```blade
<x-email.email-invoice :invoice="$invoice" :customer="$customer" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `customer` | `Customer` | Cliente da fatura | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `paymentUrl` | `string` | URL de pagamento | `null` |

### Estrutura

```blade
@props([
    'invoice',
    'customer',
    'company' => [],
    'paymentUrl' => null
])

<x-email.email-header
    :title="'Fatura #' . $invoice->code . ' - ' . $customer->display_name"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero">
                <h2 class="hero-title">Nova Fatura Disponível</h2>
                <p class="hero-subtitle">Olá {{ $customer->display_name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>Detalhes da Fatura</h3>
                    <div class="invoice-details">
                        <div class="detail-row">
                            <span class="detail-label">Número:</span>
                            <span class="detail-value">{{ $invoice->code }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Data de Emissão:</span>
                            <span class="detail-value">{{ $invoice->created_at->format('d/m/Y') }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Data de Vencimento:</span>
                            <span class="detail-value">{{ $invoice->due_date?->format('d/m/Y') ?? 'N/A' }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Status:</span>
                            <span class="status-badge status-{{ $invoice->status }}">
                                {{ ucfirst($invoice->status) }}
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Total:</span>
                            <span class="detail-value total-amount">
                                R$ {{ number_format($invoice->total, 2, ',', '.') }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Itens da Fatura -->
                @if($invoice->items->isNotEmpty())
                    <div class="content-section">
                        <h3>Itens da Fatura</h3>
                        <div class="invoice-items">
                            @foreach($invoice->items as $item)
                                <div class="item-row">
                                    <div class="item-description">{{ $item->description }}</div>
                                    <div class="item-quantity">{{ $item->quantity }}</div>
                                    <div class="item-price">R$ {{ number_format($item->unit_price, 2, ',', '.') }}</div>
                                    <div class="item-total">R$ {{ number_format($item->total, 2, ',', '.') }}</div>
                                </div>
                            @endforeach
                        </div>

                        <div class="invoice-summary">
                            <div class="summary-row">
                                <span class="summary-label">Subtotal:</span>
                                <span class="summary-value">R$ {{ number_format($invoice->subtotal, 2, ',', '.') }}</span>
                            </div>
                            @if($invoice->discount > 0)
                                <div class="summary-row">
                                    <span class="summary-label">Desconto:</span>
                                    <span class="summary-value">- R$ {{ number_format($invoice->discount, 2, ',', '.') }}</span>
                                </div>
                            @endif
                            <div class="summary-row total-row">
                                <span class="summary-label">Total:</span>
                                <span class="summary-value">R$ {{ number_format($invoice->total, 2, ',', '.') }}</span>
                            </div>
                        </div>
                    </div>
                @endif

                <!-- Informações de Pagamento -->
                @if($paymentUrl)
                    <div class="content-section">
                        <h3>Formas de Pagamento</h3>
                        <div class="payment-info">
                            <p>Para efetuar o pagamento, utilize um dos métodos abaixo:</p>
                            <div class="payment-buttons">
                                <a href="{{ $paymentUrl }}" class="btn-primary">
                                    Pagar Agora
                                </a>
                                <a href="{{ route('provider.invoices.show', $invoice) }}" class="btn-secondary">
                                    Ver Fatura
                                </a>
                            </div>
                        </div>
                    </div>
                @endif

                <!-- Avisos de Atraso -->
                @if($invoice->status === 'overdue')
                    <div class="content-section warning-section">
                        <h3>Atenção: Fatura Vencida</h3>
                        <div class="warning-message">
                            <p>Esta fatura está vencida há {{ $invoice->due_date->diffInDays(now()) }} dias.</p>
                            <p>Entre em contato conosco para regularizar sua situação.</p>
                        </div>
                    </div>
                @endif

                <!-- Observações -->
                @if($invoice->notes)
                    <div class="content-section">
                        <h3>Observações</h3>
                        <div class="observations">
                            {{ $invoice->notes }}
                        </div>
                    </div>
                @endif
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 6. Email Reminder Component

Componente para template de e-mail de lembrete.

### Uso Básico

```blade
<x-email.email-reminder :type="$type" :entity="$entity" :customer="$customer" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `type` | `string` | Tipo de lembrete (invoice, budget, etc.) | Obrigatório |
| `entity` | `mixed` | Entidade do lembrete | Obrigatório |
| `customer` | `Customer` | Cliente do lembrete | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `actionUrl` | `string` | URL de ação | `null` |

### Estrutura

```blade
@props([
    'type',
    'entity',
    'customer',
    'company' => [],
    'actionUrl' => null
])

@php
    $reminderType = match($type) {
        'invoice' => 'Fatura',
        'budget' => 'Orçamento',
        'payment' => 'Pagamento',
        default => 'Lembrete'
    };

    $reminderMessage = match($type) {
        'invoice' => 'Está quase vencendo! Não perca tempo e efetue o pagamento.',
        'budget' => 'Está quase expirando! Aproveite enquanto está válido.',
        'payment' => 'Lembre-se de efetuar o pagamento para evitar juros.',
        default => 'Não perca esta oportunidade!'
    };
@endphp

<x-email.email-header
    :title="'Lembrete: ' . $reminderType . ' #' . $entity->code"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero reminder-hero">
                <h2 class="hero-title">Lembrete Importante</h2>
                <p class="hero-subtitle">Olá {{ $customer->display_name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>{{ $reminderType }} em Destaque</h3>
                    <div class="reminder-content">
                        <p>{{ $reminderMessage }}</p>

                        <div class="entity-details">
                            <div class="detail-row">
                                <span class="detail-label">Número:</span>
                                <span class="detail-value">{{ $entity->code }}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Data:</span>
                                <span class="detail-value">{{ $entity->created_at->format('d/m/Y') }}</span>
                            </div>
                            @if($type === 'invoice' && $entity->due_date)
                                <div class="detail-row">
                                    <span class="detail-label">Vencimento:</span>
                                    <span class="detail-value">{{ $entity->due_date->format('d/m/Y') }}</span>
                                </div>
                            @endif
                            <div class="detail-row">
                                <span class="detail-label">Valor:</span>
                                <span class="detail-value total-amount">
                                    R$ {{ number_format($entity->total, 2, ',', '.') }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Ações -->
                @if($actionUrl)
                    <div class="content-section">
                        <h3>Próximos Passos</h3>
                        <div class="action-buttons">
                            <a href="{{ $actionUrl }}" class="btn-primary">
                                {{ $type === 'invoice' ? 'Efetuar Pagamento' : 'Visualizar ' . $reminderType }}
                            </a>
                            <a href="{{ $type === 'invoice' ? route('provider.invoices.index') : route('provider.budgets.index') }}"
                               class="btn-secondary">
                                Ver Todos
                            </a>
                        </div>
                    </div>
                @endif

                <!-- Contato -->
                <div class="content-section">
                    <h3>Precisa de Ajuda?</h3>
                    <div class="contact-reminder">
                        <p>Entre em contato conosco para mais informações:</p>
                        <div class="contact-info">
                            @if(!empty($company['email']))
                                <div class="contact-item">
                                    <i class="bi bi-envelope"></i>
                                    <a href="mailto:{{ $company['email'] }}">{{ $company['email'] }}</a>
                                </div>
                            @endif
                            @if(!empty($company['phone']))
                                <div class="contact-item">
                                    <i class="bi bi-telephone"></i>
                                    <span>{{ $company['phone'] }}</span>
                                </div>
                            @endif
                        </div>
                    </div>
                </div>
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 7. Email Welcome Component

Componente para template de e-mail de boas-vindas.

### Uso Básico

```blade
<x-email.email-welcome :user="$user" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `user` | `User` | Usuário recém-cadastrado | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `loginUrl` | `string` | URL de login | `null` |

### Estrutura

```blade
@props([
    'user',
    'company' => [],
    'loginUrl' => null
])

<x-email.email-header
    :title="'Bem-vindo ao ' . ($company['name'] ?? 'Easy Budget')"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero welcome-hero">
                <h2 class="hero-title">Bem-vindo ao {{ $company['name'] ?? 'Easy Budget' }}!</h2>
                <p class="hero-subtitle">Olá {{ $user->name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>Sua Jornada Começa Aqui</h3>
                    <div class="welcome-content">
                        <p>
                            Seja muito bem-vindo(a) ao {{ $company['name'] ?? 'Easy Budget' }}!
                            Estamos entusiasmados em tê-lo(a) como parte da nossa comunidade.
                        </p>

                        <p>
                            Aqui você encontrará tudo o que precisa para gerenciar seu negócio de forma simples e eficiente.
                        </p>
                    </div>
                </div>

                <!-- Benefícios -->
                <div class="content-section">
                    <h3>O que você pode fazer</h3>
                    <div class="benefits-list">
                        <div class="benefit-item">
                            <i class="bi bi-check-circle"></i>
                            <div class="benefit-content">
                                <h4>Gestão de Clientes</h4>
                                <p>Cadastre e organize seus clientes de forma simples e rápida.</p>
                            </div>
                        </div>
                        <div class="benefit-item">
                            <i class="bi bi-check-circle"></i>
                            <div class="benefit-content">
                                <h4>Emissão de Orçamentos</h4>
                                <p>Crie e envie orçamentos profissionais em minutos.</p>
                            </div>
                        </div>
                        <div class="benefit-item">
                            <i class="bi bi-check-circle"></i>
                            <div class="benefit-content">
                                <h4>Controle de Estoque</h4>
                                <p>Gerencie seu estoque e acompanhe movimentações em tempo real.</p>
                            </div>
                        </div>
                        <div class="benefit-item">
                            <i class="bi bi-check-circle"></i>
                            <div class="benefit-content">
                                <h4>Relatórios e Analytics</h4>
                                <p>Acompanhe o desempenho do seu negócio com relatórios completos.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Primeiros Passos -->
                @if($loginUrl)
                    <div class="content-section">
                        <h3>Primeiros Passos</h3>
                        <div class="steps-list">
                            <div class="step-item">
                                <div class="step-number">1</div>
                                <div class="step-content">
                                    <h4>Faça login</h4>
                                    <p>Acesse sua conta usando seu e-mail e senha.</p>
                                </div>
                            </div>
                            <div class="step-item">
                                <div class="step-number">2</div>
                                <div class="step-content">
                                    <h4>Configure seu perfil</h4>
                                    <p>Complete seu perfil para personalizar sua experiência.</p>
                                </div>
                            </div>
                            <div class="step-item">
                                <div class="step-number">3</div>
                                <div class="step-content">
                                    <h4>Comece a usar</h4>
                                    <p>Explore as funcionalidades e comece a gerenciar seu negócio.</p>
                                </div>
                            </div>
                        </div>

                        <div class="action-buttons">
                            <a href="{{ $loginUrl }}" class="btn-primary">
                                Fazer Login
                            </a>
                            <a href="{{ route('provider.dashboard') }}" class="btn-secondary">
                                Explorar Sistema
                            </a>
                        </div>
                    </div>
                @endif

                <!-- Suporte -->
                <div class="content-section">
                    <h3>Precisa de Ajuda?</h3>
                    <div class="support-content">
                        <p>Estamos aqui para ajudar você a tirar o máximo proveito do nosso sistema.</p>

                        <div class="support-info">
                            <div class="support-item">
                                <i class="bi bi-question-circle"></i>
                                <div class="support-content">
                                    <h4>Central de Ajuda</h4>
                                    <p>Acesse nossa documentação completa.</p>
                                </div>
                            </div>
                            <div class="support-item">
                                <i class="bi bi-chat-dots"></i>
                                <div class="support-content">
                                    <h4>Suporte ao Cliente</h4>
                                    <p>Entre em contato com nossa equipe.</p>
                                </div>
                            </div>
                            <div class="support-item">
                                <i class="bi bi-book"></i>
                                <div class="support-content">
                                    <h4>Tutoriais</h4>
                                    <p>Assista a vídeos explicativos.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 8. Email Verification Component

Componente para template de e-mail de verificação.

### Uso Básico

```blade
<x-email.email-verification :user="$user" :verificationUrl="$verificationUrl" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `user` | `User` | Usuário que precisa verificar | Obrigatório |
| `verificationUrl` | `string` | URL de verificação | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `expiresAt` | `string` | Data de expiração do token | `null` |

### Estrutura

```blade
@props([
    'user',
    'verificationUrl',
    'company' => [],
    'expiresAt' => null
])

<x-email.email-header
    :title="'Verifique seu E-mail - ' . ($company['name'] ?? 'Easy Budget')"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero verification-hero">
                <h2 class="hero-title">Verifique seu E-mail</h2>
                <p class="hero-subtitle">Olá {{ $user->name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>Confirme seu Endereço de E-mail</h3>
                    <div class="verification-content">
                        <p>
                            Obrigado por se cadastrar no {{ $company['name'] ?? 'Easy Budget' }}!
                            Para concluir seu cadastro, precisamos verificar seu endereço de e-mail.
                        </p>

                        <p>
                            Clique no botão abaixo para confirmar seu e-mail:
                        </p>
                    </div>
                </div>

                <!-- Botão de Verificação -->
                <div class="content-section">
                    <div class="verification-action">
                        <a href="{{ $verificationUrl }}" class="btn-primary verification-btn">
                            Verificar E-mail
                        </a>
                    </div>
                </div>

                <!-- Informações Importantes -->
                <div class="content-section">
                    <h3>Informações Importantes</h3>
                    <div class="verification-info">
                        <ul>
                            <li>Este link expira em {{ $expiresAt ?? '24 horas' }}</li>
                            <li>Se você não se cadastrou no {{ $company['name'] ?? 'Easy Budget' }}, ignore este e-mail</li>
                            <li>Este é um e-mail automático, não é necessário respondê-lo</li>
                        </ul>
                    </div>
                </div>

                <!-- Alternativa -->
                <div class="content-section">
                    <h3>Problemas com o Botão?</h3>
                    <div class="alternative-info">
                        <p>Se o botão acima não funcionar, copie e cole este link no seu navegador:</p>
                        <div class="verification-link">{{ $verificationUrl }}</div>
                    </div>
                </div>

                <!-- Contato -->
                <div class="content-section">
                    <h3>Precisa de Ajuda?</h3>
                    <div class="contact-info">
                        <p>Se você tiver algum problema com a verificação de e-mail, entre em contato conosco:</p>
                        @if(!empty($company['email']))
                            <div class="contact-item">
                                <i class="bi bi-envelope"></i>
                                <a href="mailto:{{ $company['email'] }}">{{ $company['email'] }}</a>
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 9. Email Password Component

Componente para template de e-mail de senha.

### Uso Básico

```blade
<x-email.email-password :type="$type" :user="$user" :resetUrl="$resetUrl" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `type` | `string` | Tipo de e-mail (reset, changed) | Obrigatório |
| `user` | `User` | Usuário que solicitou | Obrigatório |
| `resetUrl` | `string` | URL de redefinição | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `expiresAt` | `string` | Data de expiração do token | `null` |

### Estrutura

```blade
@props([
    'type',
    'user',
    'resetUrl',
    'company' => [],
    'expiresAt' => null
])

@php
    $emailType = match($type) {
        'reset' => 'Redefinição de Senha',
        'changed' => 'Senha Alterada',
        default => 'Alteração de Senha'
    };

    $emailMessage = match($type) {
        'reset' => 'Recebemos uma solicitação para redefinir a senha da sua conta.',
        'changed' => 'Sua senha foi alterada com sucesso.',
        default => 'Sua senha foi alterada recentemente.'
    };
@endphp

<x-email.email-header
    :title="$emailType . ' - ' . ($company['name'] ?? 'Easy Budget')"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero password-hero">
                <h2 class="hero-title">{{ $emailType }}</h2>
                <p class="hero-subtitle">Olá {{ $user->name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>{{ $emailType }}</h3>
                    <div class="password-content">
                        <p>{{ $emailMessage }}</p>

                        @if($type === 'reset')
                            <p>
                                Para redefinir sua senha, clique no botão abaixo:
                            </p>
                        @endif
                    </div>
                </div>

                <!-- Ação -->
                @if($type === 'reset')
                    <div class="content-section">
                        <div class="password-action">
                            <a href="{{ $resetUrl }}" class="btn-primary password-btn">
                                Redefinir Senha
                            </a>
                        </div>
                    </div>
                @endif

                <!-- Informações -->
                <div class="content-section">
                    <h3>Informações Importantes</h3>
                    <div class="password-info">
                        @if($type === 'reset')
                            <ul>
                                <li>Este link expira em {{ $expiresAt ?? '1 hora' }}</li>
                                <li>Se você não solicitou a redefinição de senha, ignore este e-mail</li>
                                <li>Sua senha permanecerá a mesma até que você acesse o link acima</li>
                            </ul>
                        @else
                            <ul>
                                <li>Se você não fez esta alteração, entre em contato conosco imediatamente</li>
                                <li>Recomendamos usar uma senha forte e única</li>
                                <li>Nunca compartilhe sua senha com terceiros</li>
                            </ul>
                        @endif
                    </div>
                </div>

                <!-- Segurança -->
                <div class="content-section">
                    <h3>Dicas de Segurança</h3>
                    <div class="security-tips">
                        <ul>
                            <li>Use senhas fortes e únicas</li>
                            <li>Ative a autenticação de dois fatores</li>
                            <li>Nunca compartilhe suas credenciais</li>
                            <li>Altere sua senha periodicamente</li>
                        </ul>
                    </div>
                </div>

                <!-- Contato -->
                <div class="content-section">
                    <h3>Precisa de Ajuda?</h3>
                    <div class="contact-info">
                        <p>Se você tiver algum problema ou suspeitar de atividade não autorizada:</p>
                        @if(!empty($company['email']))
                            <div class="contact-item">
                                <i class="bi bi-envelope"></i>
                                <a href="mailto:{{ $company['email'] }}">{{ $company['email'] }}</a>
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 10. Email Support Component

Componente para template de e-mail de suporte.

### Uso Básico

```blade
<x-email.email-support :ticket="$ticket" :customer="$customer" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `ticket` | `Support` | Ticket de suporte | Obrigatório |
| `customer` | `Customer` | Cliente do ticket | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `ticketUrl` | `string` | URL do ticket | `null` |

### Estrutura

```blade
@props([
    'ticket',
    'customer',
    'company' => [],
    'ticketUrl' => null
])

<x-email.email-header
    :title="'Ticket de Suporte #' . $ticket->id . ' - ' . $ticket->subject"
    :company="$company" />

        <!-- Conteúdo Principal -->
        <main class="email-main">
            <div class="email-hero support-hero">
                <h2 class="hero-title">Ticket de Suporte</h2>
                <p class="hero-subtitle">Olá {{ $customer->display_name }},</p>
            </div>

            <div class="email-content">
                <div class="content-section">
                    <h3>Detalhes do Ticket</h3>
                    <div class="ticket-details">
                        <div class="detail-row">
                            <span class="detail-label">Número:</span>
                            <span class="detail-value">#{{ $ticket->id }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Assunto:</span>
                            <span class="detail-value">{{ $ticket->subject }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Status:</span>
                            <span class="status-badge status-{{ $ticket->status }}">
                                {{ ucfirst($ticket->status) }}
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Prioridade:</span>
                            <span class="detail-value">{{ ucfirst($ticket->priority) }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Data:</span>
                            <span class="detail-value">{{ $ticket->created_at->format('d/m/Y H:i') }}</span>
                        </div>
                    </div>
                </div>

                <!-- Mensagem -->
                <div class="content-section">
                    <h3>Mensagem</h3>
                    <div class="ticket-message">
                        <p>{{ $ticket->message }}</p>
                    </div>
                </div>

                <!-- Resposta -->
                @if($ticket->response)
                    <div class="content-section">
                        <h3>Resposta da Equipe</h3>
                        <div class="ticket-response">
                            <p>{{ $ticket->response }}</p>
                            <div class="response-meta">
                                <span class="response-date">{{ $ticket->updated_at->format('d/m/Y H:i') }}</span>
                                <span class="response-agent">{{ $ticket->agent?->name ?? 'Equipe de Suporte' }}</span>
                            </div>
                        </div>
                    </div>
                @endif

                <!-- Ações -->
                @if($ticketUrl)
                    <div class="content-section">
                        <h3>Próximos Passos</h3>
                        <div class="action-buttons">
                            <a href="{{ $ticketUrl }}" class="btn-primary">
                                Ver Ticket
                            </a>
                            <a href="{{ route('provider.support.index') }}" class="btn-secondary">
                                Ver Todos os Tickets
                            </a>
                        </div>
                    </div>
                @endif

                <!-- Prazo de Resposta -->
                <div class="content-section">
                    <h3>Prazo de Resposta</h3>
                    <div class="response-time">
                        <p>
                            Responderemos ao seu ticket em até 24 horas úteis.
                            Agradecemos a sua paciência.
                        </p>
                    </div>
                </div>

                <!-- Contato Alternativo -->
                <div class="content-section">
                    <h3>Contato Alternativo</h3>
                    <div class="alternative-contact">
                        <p>Para questões urgentes, você também pode entrar em contato:</p>
                        <div class="contact-info">
                            @if(!empty($company['phone']))
                                <div class="contact-item">
                                    <i class="bi bi-telephone"></i>
                                    <span>{{ $company['phone'] }}</span>
                                </div>
                            @endif
                            @if(!empty($company['email']))
                                <div class="contact-item">
                                    <i class="bi bi-envelope"></i>
                                    <a href="mailto:{{ $company['email'] }}">{{ $company['email'] }}</a>
                                </div>
                            @endif
                        </div>
                    </div>
                </div>
            </div>
        </main>

<x-email.email-footer :company="$company" />
```

## 11. Email Styles Component

Componente para estilos CSS padrão de e-mails.

### Uso Básico

```blade
<x-email.email-styles />
```

### Estrutura

```blade
<style>
    /* Reset e Configurações Básicas */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
    }

    .email-container {
        max-width: 600px;
        margin: 0 auto;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Cabeçalho */
    .email-header {
        background: linear-gradient(135deg, #0d6efd 0%, #007bff 100%);
        color: white;
        padding: 30px;
        text-align: center;
    }

    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
    }

    .company-logo img {
        max-height: 60px;
        filter: brightness(0) invert(1);
    }

    .company-info {
        text-align: left;
    }

    .company-name {
        font-size: 24px;
        font-weight: bold;
        margin: 0 0 5px 0;
        letter-spacing: 1px;
    }

    .company-tagline {
        font-size: 14px;
        opacity: 0.9;
        margin: 0;
    }

    /* Conteúdo Principal */
    .email-main {
        padding: 30px;
    }

    /* Heróis */
    .email-hero {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        border-radius: 8px;
    }

    .hero-title {
        font-size: 28px;
        font-weight: bold;
        margin: 0 0 10px 0;
        color: #333;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #666;
        margin: 0;
    }

    .reminder-hero {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
    }

    .welcome-hero {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }

    .verification-hero {
        background-color: #cff4fc;
        border: 1px solid #b6effb;
    }

    .password-hero {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }

    .support-hero {
        background-color: #e2e3e5;
        border: 1px solid #d6d8db;
    }

    /* Seções de Conteúdo */
    .content-section {
        margin-bottom: 30px;
    }

    .content-section h3 {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin: 0 0 15px 0;
        border-bottom: 2px solid #0d6efd;
        padding-bottom: 10px;
    }

    .content-section p {
        margin: 0 0 15px 0;
        line-height: 1.6;
    }

    /* Detalhes */
    .budget-details, .invoice-details, .entity-details, .ticket-details {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    .detail-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #e9ecef;
    }

    .detail-row:last-child {
        border-bottom: none;
    }

    .detail-label {
        font-weight: bold;
        color: #666;
    }

    .detail-value {
        font-weight: 600;
        color: #333;
    }

    .total-amount {
        font-size: 20px;
        color: #0d6efd;
    }

    /* Status */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }

    .status-active, .status-approved, .status-paid {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .status-inactive, .status-rejected, .status-overdue {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .status-pending, .status-pending-payment {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }

    /* Listas */
    .services-list, .invoice-items {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    .service-item, .item-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #e9ecef;
    }

    .service-item:last-child, .item-row:last-child {
        border-bottom: none;
    }

    .service-info {
        flex: 1;
    }

    .service-code {
        font-weight: bold;
        color: #0d6efd;
    }

    .service-description, .item-description {
        font-size: 14px;
        color: #666;
        margin-top: 2px;
    }

    .service-price, .item-price, .item-total {
        font-weight: bold;
        color: #333;
    }

    /* Resumo */
    .invoice-summary {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-top: 15px;
    }

    .summary-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #e9ecef;
    }

    .summary-row:last-child {
        border-bottom: none;
    }

    .summary-label {
        font-weight: bold;
        color: #666;
    }

    .summary-value {
        font-weight: bold;
        color: #333;
    }

    .total-row {
        background-color: #e9ecef;
        font-size: 18px;
    }

    /* Benefícios */
    .benefits-list {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
    }

    .benefit-item {
        display: flex;
        gap: 15px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    .benefit-item i {
        font-size: 24px;
        color: #0d6efd;
        flex-shrink: 0;
    }

    .benefit-content h4 {
        margin: 0 0 5px 0;
        font-size: 16px;
    }

    .benefit-content p {
        margin: 0;
        font-size: 14px;
        color: #666;
    }

    /* Passos */
    .steps-list {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }

    .step-item {
        display: flex;
        gap: 15px;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    .step-number {
        width: 40px;
        height: 40px;
        background-color: #0d6efd;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        flex-shrink: 0;
    }

    .step-content h4 {
        margin: 0 0 5px 0;
        font-size: 16px;
    }

    .step-content p {
        margin: 0;
        font-size: 14px;
        color: #666;
    }

    /* Listas */
    .verification-info ul, .password-info ul, .security-tips ul {
        padding-left: 20px;
        margin: 15px 0;
    }

    .verification-info li, .password-info li, .security-tips li {
        margin-bottom: 8px;
        line-height: 1.5;
    }

    /* Botões */
    .action-buttons, .payment-buttons, .verification-action, .password-action {
        display: flex;
        gap: 15px;
        margin: 20px 0;
    }

    .btn-primary, .btn-secondary {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        text-align: center;
        transition: all 0.3s ease;
    }

    .btn-primary {
        background-color: #0d6efd;
        color: white;
        border: 1px solid #0d6efd;
    }

    .btn-primary:hover {
        background-color: #0b5ed7;
        border-color: #0b5ed7;
        transform: translateY(-1px);
    }

    .btn-secondary {
        background-color: #6c757d;
        color: white;
        border: 1px solid #6c757d;
    }

    .btn-secondary:hover {
        background-color: #5c636a;
        border-color: #5c636a;
        transform: translateY(-1px);
    }

    .verification-btn, .password-btn {
        width: 100%;
        display: block;
        text-align: center;
    }

    /* Rodapé */
    .email-footer {
        background-color: #f8f9fa;
        padding: 30px;
        border-top: 1px solid #e9ecef;
    }

    .footer-content {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 30px;
        margin-bottom: 20px;
    }

    .footer-section h3, .footer-section h4 {
        margin: 0 0 10px 0;
        font-size: 16px;
        color: #333;
    }

    .footer-section p {
        margin: 0 0 10px 0;
        font-size: 14px;
        color: #666;
        line-height: 1.5;
    }

    .contact-info {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .contact-item {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        color: #666;
    }

    .contact-item i {
        color: #0d6efd;
        font-size: 16px;
    }

    .contact-item a {
        color: #0d6efd;
        text-decoration: none;
    }

    .contact-item a:hover {
        text-decoration: underline;
    }

    .social-links {
        display: flex;
        gap: 10px;
    }

    .social-link {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background-color: #0d6efd;
        color: white;
        border-radius: 50%;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .social-link:hover {
        background-color: #0b5ed7;
        transform: translateY(-1px);
    }

    .footer-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #e9ecef;
        padding-top: 20px;
    }

    .footer-text {
        font-size: 12px;
        color: #666;
    }

    .unsubscribe-link {
        color: #6c757d;
        text-decoration: none;
        font-size: 12px;
    }

    .unsubscribe-link:hover {
        text-decoration: underline;
    }

    /* Classes de utilidade */
    .warning-section {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 20px;
        border-radius: 8px;
    }

    .warning-message {
        background-color: #fff8d6;
        padding: 15px;
        border-radius: 6px;
        border-left: 4px solid #ffc107;
    }

    .support-info {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 15px;
    }

    .support-item {
        display: flex;
        gap: 15px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    .support-item i {
        font-size: 24px;
        color: #0d6efd;
        flex-shrink: 0;
    }

    .support-content h4 {
        margin: 0 0 5px 0;
        font-size: 16px;
    }

    .support-content p {
        margin: 0;
        font-size: 14px;
        color: #666;
    }

    .verification-link {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #e9ecef;
        font-family: monospace;
        font-size: 12px;
        word-break: break-all;
    }

    /* Responsividade */
    @media (max-width: 600px) {
        .email-container {
            width: 100%;
            margin: 0;
        }

        .header-content {
            flex-direction: column;
            text-align: center;
        }

        .benefits-list, .steps-list, .support-info {
            grid-template-columns: 1fr;
        }

        .footer-content {
            grid-template-columns: 1fr;
        }

        .action-buttons, .payment-buttons {
            flex-direction: column;
        }

        .detail-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 5px;
        }

        .service-item, .item-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 10px;
        }
    }
</style>
```

## 12. Integração com Padrões Existentes

### Uso em Mailables

```php
// BudgetNotificationMail.php
class BudgetNotificationMail extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(public Budget $budget, public Customer $customer)
    {
        //
    }

    public function build()
    {
        $company = [
            'name' => tenant('name'),
            'logo' => tenant('logo'),
            'email' => tenant('email'),
            'phone' => tenant('phone'),
            'website' => tenant('website'),
        ];

        return $this->subject("Orçamento #{$this->budget->code} - {$this->customer->display_name}")
                    ->view('components.email.email-budget', [
                        'budget' => $this->budget,
                        'customer' => $this->customer,
                        'company' => $company,
                        'actionUrl' => route('provider.budgets.show', $this->budget)
                    ]);
    }
}
```

### Uso em Controllers

```php
// EmailController.php
public function previewBudget(Budget $budget)
{
    $customer = $budget->customer;
    $company = [
        'name' => tenant('name'),
        'logo' => tenant('logo'),
        'email' => tenant('email'),
        'phone' => tenant('phone'),
        'website' => tenant('website'),
    ];

    return view('components.email.email-budget', [
        'budget' => $budget,
        'customer' => $customer,
        'company' => $company,
        'actionUrl' => route('provider.budgets.show', $budget)
    ]);
}
```

### Estilos CSS

```css
/* Email Components Styles */
.email-container {
    max-width: 600px;
    margin: 0 auto;
    background-color: #ffffff;
}

.email-header {
    background: linear-gradient(135deg, #0d6efd 0%, #007bff 100%);
    color: white;
}

.btn-primary {
    background-color: #0d6efd;
    color: white;
    padding: 12px 24px;
    border-radius: 6px;
    text-decoration: none;
}

.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}
```

## 13. JavaScript Interatividade

### Visualização de E-mails

```javascript
// email-preview.js
document.addEventListener('DOMContentLoaded', function() {
    // Botões de visualização de e-mail
    const emailPreviewButtons = document.querySelectorAll('.btn-email-preview');
    emailPreviewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                window.open(url, '_blank', 'width=800,height=600');
            }
        });
    });

    // Botões de envio de e-mail
    const emailSendButtons = document.querySelectorAll('.btn-email-send');
    emailSendButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
});
```

## 14. Validação e Segurança

### Autorização

```php
// EmailPolicy.php
public function sendBudget(User $user, Budget $budget)
{
    return $user->tenant_id === $budget->tenant_id;
}

public function sendInvoice(User $user, Invoice $invoice)
{
    return $user->tenant_id === $invoice->tenant_id;
}

public function sendSupport(User $user, Support $ticket)
{
    return $user->tenant_id === $ticket->tenant_id;
}
```

### Validations

```blade
{{-- Email Budget com validação de permissões --}}
@can('sendBudget', $budget)
    <x-email.email-budget :budget="$budget" :customer="$customer" :company="$company" />
@endcan

{{-- Email Invoice com validação de status --}}
@can('sendInvoice', $invoice)
    <x-email.email-invoice :invoice="$invoice" :customer="$customer" :company="$company" />
@endcan
```

Este padrão de components para e-mails garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
