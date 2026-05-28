---
name: pdf-components
description: Componentes de UI para geração e visualização de PDFs seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para PDFs

Esta skill define os componentes Blade específicos para a geração e visualização de PDFs no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── pdf/
│   ├── pdf-header.blade.php         # Cabeçalho padrão de PDFs
│   ├── pdf-footer.blade.php         # Rodapé padrão de PDFs
│   ├── pdf-document.blade.php       # Estrutura base de documentos PDF
│   ├── pdf-budget.blade.php         # Template de orçamento em PDF
│   ├── pdf-invoice.blade.php        # Template de fatura em PDF
│   ├── pdf-report.blade.php         # Template de relatório em PDF
│   ├── pdf-customer.blade.php       # Template de cliente em PDF
│   ├── pdf-product.blade.php        # Template de produto em PDF
│   ├── pdf-watermark.blade.php      # Marca d'água para PDFs
│   └── pdf-styles.blade.php         # Estilos CSS para PDFs
└── ...
```

## 1. PDF Header Component

Componente para cabeçalho padrão de documentos PDF.

### Uso Básico

```blade
<x-pdf.pdf-header :title="$title" :company="$company" :date="$date" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do documento | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `date` | `string` | Data do documento | `now()` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'title',
    'company' => [],
    'date' => null,
    'showLogo' => true
])

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title }}</title>
    <x-pdf.pdf-styles />
</head>
<body>
    <div class="pdf-container">
        <!-- Cabeçalho -->
        <header class="pdf-header">
            <div class="header-content">
                @if($showLogo && !empty($company['logo']))
                    <div class="company-logo">
                        <img src="{{ public_path('storage/' . $company['logo']) }}" alt="Logo" style="max-height: 60px;">
                    </div>
                @endif

                <div class="company-info">
                    <h1 class="company-name">{{ $company['name'] ?? 'Easy Budget' }}</h1>
                    <div class="company-details">
                        @if(!empty($company['cnpj']))
                            <div class="detail-item">
                                <strong>CNPJ:</strong> {{ $company['cnpj'] }}
                            </div>
                        @endif
                        @if(!empty($company['address']))
                            <div class="detail-item">
                                <strong>Endereço:</strong> {{ $company['address'] }}
                            </div>
                        @endif
                        @if(!empty($company['phone']))
                            <div class="detail-item">
                                <strong>Telefone:</strong> {{ $company['phone'] }}
                            </div>
                        @endif
                        @if(!empty($company['email']))
                            <div class="detail-item">
                                <strong>E-mail:</strong> {{ $company['email'] }}
                            </div>
                        @endif
                    </div>
                </div>

                <div class="document-info">
                    <h2 class="document-title">{{ $title }}</h2>
                    <div class="document-date">
                        <strong>Data:</strong> {{ $date ?? now()->format('d/m/Y') }}
                    </div>
                    @if(!empty($company['document_number']))
                        <div class="document-number">
                            <strong>Número:</strong> {{ $company['document_number'] }}
                        </div>
                    @endif
                </div>
            </div>
        </header>
```

## 2. PDF Footer Component

Componente para rodapé padrão de documentos PDF.

### Uso Básico

```blade
<x-pdf.pdf-footer :page="$page" :totalPages="$totalPages" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `page` | `int` | Número da página atual | `1` |
| `totalPages` | `int` | Total de páginas | `1` |
| `company` | `array` | Dados da empresa | `[]` |
| `showPageNumbers` | `bool` | Exibir numeração de páginas | `true` |

### Estrutura

```blade
@props([
    'page' => 1,
    'totalPages' => 1,
    'company' => [],
    'showPageNumbers' => true
])

        <!-- Rodapé -->
        <footer class="pdf-footer">
            <div class="footer-content">
                <div class="footer-left">
                    <div class="footer-text">
                        {{ $company['name'] ?? 'Easy Budget' }} - {{ $company['address'] ?? '' }}
                    </div>
                    <div class="footer-text small">
                        {{ $company['phone'] ?? '' }} | {{ $company['email'] ?? '' }}
                    </div>
                </div>

                <div class="footer-center">
                    <div class="footer-text small">
                        Documento gerado automaticamente pelo sistema Easy Budget
                    </div>
                    <div class="footer-text small">
                        {{ now()->format('d/m/Y H:i:s') }}
                    </div>
                </div>

                @if($showPageNumbers)
                    <div class="footer-right">
                        <div class="page-info">
                            Página {{ $page }} de {{ $totalPages }}
                        </div>
                    </div>
                @endif
            </div>
        </footer>
    </div>
</body>
</html>
```

## 3. PDF Document Component

Componente para estrutura base de documentos PDF.

### Uso Básico

```blade
<x-pdf.pdf-document :title="$title" :company="$company" :content="$content" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do documento | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `content` | `string` | Conteúdo do documento | Obrigatório |
| `date` | `string` | Data do documento | `now()` |

### Estrutura

```blade
@props([
    'title',
    'company' => [],
    'content',
    'date' => null
])

<x-pdf.pdf-header :title="$title" :company="$company" :date="$date" />

        <!-- Conteúdo Principal -->
        <main class="pdf-main">
            {!! $content !!}
        </main>

<x-pdf.pdf-footer :company="$company" />
```

## 4. PDF Budget Component

Componente para template de orçamento em PDF.

### Uso Básico

```blade
<x-pdf.pdf-budget :budget="$budget" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `budget` | `Budget` | Modelo do orçamento | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'budget',
    'company' => [],
    'showLogo' => true
])

<x-pdf.pdf-header
    :title="'Orçamento #' . $budget->code"
    :company="$company"
    :date="$budget->created_at->format('d/m/Y')"
    :showLogo="$showLogo" />

        <!-- Informações do Cliente -->
        <section class="pdf-section">
            <h3 class="section-title">Dados do Cliente</h3>
            <div class="client-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Nome:</strong> {{ $budget->customer->display_name }}
                    </div>
                    <div class="info-item">
                        <strong>CPF/CNPJ:</strong>
                        @if($budget->customer->type === 'pf')
                            {{ \App\Helpers\DocumentHelper::formatCpf($budget->customer->commonData->cpf) }}
                        @else
                            {{ \App\Helpers\DocumentHelper::formatCnpj($budget->customer->commonData->cnpj) }}
                        @endif
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Endereço:</strong> {{ $budget->customer->address->address }}, {{ $budget->customer->address->address_number }}
                    </div>
                    <div class="info-item">
                        <strong>Bairro:</strong> {{ $budget->customer->address->neighborhood }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Cidade:</strong> {{ $budget->customer->address->city }}/{{ $budget->customer->address->state }}
                    </div>
                    <div class="info-item">
                        <strong>CEP:</strong> {{ $budget->customer->address->cep }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>E-mail:</strong> {{ $budget->customer->contact->email }}
                    </div>
                    <div class="info-item">
                        <strong>Telefone:</strong> {{ $budget->customer->contact->phone }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Dados do Orçamento -->
        <section class="pdf-section">
            <h3 class="section-title">Dados do Orçamento</h3>
            <div class="budget-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Número:</strong> {{ $budget->code }}
                    </div>
                    <div class="info-item">
                        <strong>Data:</strong> {{ $budget->created_at->format('d/m/Y') }}
                    </div>
                    <div class="info-item">
                        <strong>Validade:</strong> {{ $budget->due_date?->format('d/m/Y') ?? 'Indeterminado' }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Status:</strong>
                        <span class="status-badge status-{{ $budget->status }}">
                            {{ ucfirst($budget->status) }}
                        </span>
                    </div>
                    <div class="info-item">
                        <strong>Desconto:</strong> R$ {{ number_format($budget->discount, 2, ',', '.') }}
                    </div>
                    <div class="info-item">
                        <strong>Total:</strong> R$ {{ number_format($budget->total, 2, ',', '.') }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Serviços -->
        @if($budget->services->isNotEmpty())
            <section class="pdf-section">
                <h3 class="section-title">Serviços</h3>
                <div class="table-container">
                    <table class="pdf-table">
                        <thead>
                            <tr>
                                <th>Código</th>
                                <th>Descrição</th>
                                <th>Valor Unitário</th>
                                <th>Desconto</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($budget->services as $service)
                                <tr>
                                    <td>{{ $service->code }}</td>
                                    <td>{{ $service->description }}</td>
                                    <td class="text-right">R$ {{ number_format($service->total, 2, ',', '.') }}</td>
                                    <td class="text-right">R$ {{ number_format($service->discount, 2, ',', '.') }}</td>
                                    <td class="text-right">R$ {{ number_format($service->total - $service->discount, 2, ',', '.') }}</td>
                                </tr>
                            @endforeach
                        </tbody>
                        <tfoot>
                            <tr class="total-row">
                                <td colspan="4" class="text-right"><strong>Total dos Serviços:</strong></td>
                                <td class="text-right"><strong>R$ {{ number_format($budget->services->sum('total'), 2, ',', '.') }}</strong></td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </section>
        @endif

        <!-- Observações -->
        @if($budget->description)
            <section class="pdf-section">
                <h3 class="section-title">Observações</h3>
                <div class="observations">
                    {{ $budget->description }}
                </div>
            </section>
        @endif

        <!-- Termos e Condições -->
        <section class="pdf-section">
            <h3 class="section-title">Termos e Condições</h3>
            <div class="terms">
                <p>
                    Este orçamento tem validade de 30 dias a partir da data de emissão.
                    O pagamento deverá ser efetuado conforme as condições acordadas.
                    Qualquer alteração neste orçamento deverá ser comunicada por escrito.
                </p>
                <p class="small">
                    Para aceitar este orçamento, assine no campo abaixo e devolva uma cópia.
                </p>
            </div>
        </section>

        <!-- Assinaturas -->
        <section class="pdf-section">
            <h3 class="section-title">Assinaturas</h3>
            <div class="signatures">
                <div class="signature-field">
                    <div class="signature-line"></div>
                    <div class="signature-label">
                        {{ $company['name'] ?? 'Easy Budget' }}
                    </div>
                </div>
                <div class="signature-field">
                    <div class="signature-line"></div>
                    <div class="signature-label">
                        Cliente
                    </div>
                </div>
            </div>
        </section>

<x-pdf.pdf-footer :company="$company" />
```

## 5. PDF Invoice Component

Componente para template de fatura em PDF.

### Uso Básico

```blade
<x-pdf.pdf-invoice :invoice="$invoice" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'invoice',
    'company' => [],
    'showLogo' => true
])

<x-pdf.pdf-header
    :title="'Fatura #' . $invoice->code"
    :company="$company"
    :date="$invoice->created_at->format('d/m/Y')"
    :showLogo="$showLogo" />

        <!-- Informações do Cliente -->
        <section class="pdf-section">
            <h3 class="section-title">Dados do Cliente</h3>
            <div class="client-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Nome:</strong> {{ $invoice->customer->display_name }}
                    </div>
                    <div class="info-item">
                        <strong>CPF/CNPJ:</strong>
                        @if($invoice->customer->type === 'pf')
                            {{ \App\Helpers\DocumentHelper::formatCpf($invoice->customer->commonData->cpf) }}
                        @else
                            {{ \App\Helpers\DocumentHelper::formatCnpj($invoice->customer->commonData->cnpj) }}
                        @endif
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Endereço:</strong> {{ $invoice->customer->address->address }}, {{ $invoice->customer->address->address_number }}
                    </div>
                    <div class="info-item">
                        <strong>Bairro:</strong> {{ $invoice->customer->address->neighborhood }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Cidade:</strong> {{ $invoice->customer->address->city }}/{{ $invoice->customer->address->state }}
                    </div>
                    <div class="info-item">
                        <strong>CEP:</strong> {{ $invoice->customer->address->cep }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Dados da Fatura -->
        <section class="pdf-section">
            <h3 class="section-title">Dados da Fatura</h3>
            <div class="invoice-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Número:</strong> {{ $invoice->code }}
                    </div>
                    <div class="info-item">
                        <strong>Data de Emissão:</strong> {{ $invoice->created_at->format('d/m/Y') }}
                    </div>
                    <div class="info-item">
                        <strong>Data de Vencimento:</strong> {{ $invoice->due_date?->format('d/m/Y') ?? 'N/A' }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Status:</strong>
                        <span class="status-badge status-{{ $invoice->status }}">
                            {{ ucfirst($invoice->status) }}
                        </span>
                    </div>
                    <div class="info-item">
                        <strong>Método de Pagamento:</strong> {{ $invoice->payment_method ?? 'N/A' }}
                    </div>
                    <div class="info-item">
                        <strong>ID do Pagamento:</strong> {{ $invoice->payment_id ?? 'N/A' }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Itens da Fatura -->
        <section class="pdf-section">
            <h3 class="section-title">Itens da Fatura</h3>
            <div class="table-container">
                <table class="pdf-table">
                    <thead>
                        <tr>
                            <th>Descrição</th>
                            <th>Quantidade</th>
                            <th>Valor Unitário</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($invoice->items as $item)
                            <tr>
                                <td>{{ $item->description }}</td>
                                <td class="text-center">{{ $item->quantity }}</td>
                                <td class="text-right">R$ {{ number_format($item->unit_price, 2, ',', '.') }}</td>
                                <td class="text-right">R$ {{ number_format($item->total, 2, ',', '.') }}</td>
                            </tr>
                        @endforeach
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="3" class="text-right"><strong>Subtotal:</strong></td>
                            <td class="text-right">R$ {{ number_format($invoice->subtotal, 2, ',', '.') }}</td>
                        </tr>
                        @if($invoice->discount > 0)
                            <tr>
                                <td colspan="3" class="text-right"><strong>Desconto:</strong></td>
                                <td class="text-right">- R$ {{ number_format($invoice->discount, 2, ',', '.') }}</td>
                            </tr>
                        @endif
                        <tr class="total-row">
                            <td colspan="3" class="text-right"><strong>Total:</strong></td>
                            <td class="text-right"><strong>R$ {{ number_format($invoice->total, 2, ',', '.') }}</strong></td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </section>

        <!-- Informações de Pagamento -->
        @if($invoice->payment_method)
            <section class="pdf-section">
                <h3 class="section-title">Informações de Pagamento</h3>
                <div class="payment-info">
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Método:</strong> {{ $invoice->payment_method }}
                        </div>
                        <div class="info-item">
                            <strong>Valor Pago:</strong> R$ {{ number_format($invoice->transaction_amount ?? $invoice->total, 2, ',', '.') }}
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Data do Pagamento:</strong> {{ $invoice->transaction_date?->format('d/m/Y H:i') ?? 'N/A' }}
                        </div>
                        <div class="info-item">
                            <strong>Status:</strong>
                            <span class="status-badge status-{{ $invoice->status }}">
                                {{ ucfirst($invoice->status) }}
                            </span>
                        </div>
                    </div>
                </div>
            </section>
        @endif

        <!-- Observações -->
        @if($invoice->notes)
            <section class="pdf-section">
                <h3 class="section-title">Observações</h3>
                <div class="observations">
                    {{ $invoice->notes }}
                </div>
            </section>
        @endif

<x-pdf.pdf-footer :company="$company" />
```

## 6. PDF Report Component

Componente para template de relatório em PDF.

### Uso Básico

```blade
<x-pdf.pdf-report :report="$report" :data="$data" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `report` | `Report` | Modelo do relatório | Obrigatório |
| `data` | `array` | Dados do relatório | `[]` |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'report',
    'data' => [],
    'company' => [],
    'showLogo' => true
])

<x-pdf.pdf-header
    :title="$report->description"
    :company="$company"
    :date="$report->generated_at?->format('d/m/Y')"
    :showLogo="$showLogo" />

        <!-- Resumo Executivo -->
        <section class="pdf-section">
            <h3 class="section-title">Resumo Executivo</h3>
            <div class="executive-summary">
                <div class="summary-grid">
                    @foreach($data['summary'] ?? [] as $key => $value)
                        <div class="summary-item">
                            <div class="summary-label">{{ ucfirst(str_replace('_', ' ', $key)) }}</div>
                            <div class="summary-value">{{ $value }}</div>
                        </div>
                    @endforeach
                </div>
            </div>
        </section>

        <!-- Dados Detalhados -->
        @if(!empty($data['details']))
            <section class="pdf-section">
                <h3 class="section-title">Dados Detalhados</h3>
                <div class="table-container">
                    <table class="pdf-table">
                        <thead>
                            <tr>
                                @foreach(array_keys($data['details'][0] ?? []) as $header)
                                    <th>{{ ucfirst(str_replace('_', ' ', $header)) }}</th>
                                @endforeach
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($data['details'] as $row)
                                <tr>
                                    @foreach($row as $value)
                                        <td>{{ $value }}</td>
                                    @endforeach
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            </section>
        @endif

        <!-- Gráficos -->
        @if(!empty($data['charts']))
            <section class="pdf-section">
                <h3 class="section-title">Análise Gráfica</h3>
                <div class="charts-container">
                    @foreach($data['charts'] as $chart)
                        <div class="chart-item">
                            <h4>{{ $chart['title'] }}</h4>
                            <!-- Gráficos em PDF geralmente são gerados como imagens -->
                            <div class="chart-placeholder">
                                Gráfico: {{ $chart['type'] }}
                            </div>
                        </div>
                    @endforeach
                </div>
            </section>
        @endif

        <!-- Conclusões -->
        @if(!empty($data['conclusions']))
            <section class="pdf-section">
                <h3 class="section-title">Conclusões</h3>
                <div class="conclusions">
                    @foreach($data['conclusions'] as $conclusion)
                        <div class="conclusion-item">
                            <strong>{{ $conclusion['title'] }}:</strong>
                            {{ $conclusion['description'] }}
                        </div>
                    @endforeach
                </div>
            </section>
        @endif

        <!-- Recomendações -->
        @if(!empty($data['recommendations']))
            <section class="pdf-section">
                <h3 class="section-title">Recomendações</h3>
                <div class="recommendations">
                    @foreach($data['recommendations'] as $recommendation)
                        <div class="recommendation-item">
                            <strong>{{ $recommendation['title'] }}:</strong>
                            {{ $recommendation['description'] }}
                        </div>
                    @endforeach
                </div>
            </section>
        @endif

<x-pdf.pdf-footer :company="$company" />
```

## 7. PDF Customer Component

Componente para template de cliente em PDF.

### Uso Básico

```blade
<x-pdf.pdf-customer :customer="$customer" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `customer` | `Customer` | Modelo do cliente | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'customer',
    'company' => [],
    'showLogo' => true
])

<x-pdf.pdf-header
    :title="'Ficha do Cliente: ' . $customer->display_name"
    :company="$company"
    :date="$customer->created_at->format('d/m/Y')"
    :showLogo="$showLogo" />

        <!-- Dados Básicos -->
        <section class="pdf-section">
            <h3 class="section-title">Dados Básicos</h3>
            <div class="customer-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Nome/Razão Social:</strong> {{ $customer->display_name }}
                    </div>
                    <div class="info-item">
                        <strong>Tipo:</strong>
                        <span class="badge bg-secondary">{{ $customer->type === 'pf' ? 'Pessoa Física' : 'Pessoa Jurídica' }}</span>
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Status:</strong>
                        <x-customer.customer-status :customer="$customer" />
                    </div>
                    <div class="info-item">
                        <strong>Data de Cadastro:</strong> {{ $customer->created_at->format('d/m/Y') }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Dados Pessoais/Empresariais -->
        @if($customer->commonData)
            <section class="pdf-section">
                <h3 class="section-title">{{ $customer->type === 'pf' ? 'Dados Pessoais' : 'Dados Empresariais' }}</h3>
                <div class="personal-info">
                    @if($customer->type === 'pf')
                        <div class="info-row">
                            <div class="info-item">
                                <strong>Nome Completo:</strong> {{ $customer->commonData->first_name }} {{ $customer->commonData->last_name }}
                            </div>
                            <div class="info-item">
                                <strong>CPF:</strong> {{ \App\Helpers\DocumentHelper::formatCpf($customer->commonData->cpf) }}
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-item">
                                <strong>Data de Nascimento:</strong> {{ $customer->commonData->birth_date?->format('d/m/Y') ?? 'N/A' }}
                            </div>
                            <div class="info-item">
                                <strong>Profissão:</strong> {{ $customer->commonData->profession?->name ?? 'N/A' }}
                            </div>
                        </div>
                    @else
                        <div class="info-row">
                            <div class="info-item">
                                <strong>Razão Social:</strong> {{ $customer->commonData->company_name }}
                            </div>
                            <div class="info-item">
                                <strong>CNPJ:</strong> {{ \App\Helpers\DocumentHelper::formatCnpj($customer->commonData->cnpj) }}
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-item">
                                <strong>CPF do Responsável:</strong> {{ \App\Helpers\DocumentHelper::formatCpf($customer->commonData->cpf) }}
                            </div>
                            <div class="info-item">
                                <strong>Área de Atuação:</strong> {{ $customer->commonData->areaOfActivity?->name ?? 'N/A' }}
                            </div>
                        </div>
                    @endif

                    @if($customer->commonData->description)
                        <div class="info-row">
                            <div class="info-item full-width">
                                <strong>Descrição:</strong> {{ $customer->commonData->description }}
                            </div>
                        </div>
                    @endif
                </div>
            </section>
        @endif

        <!-- Contato -->
        @if($customer->contact)
            <section class="pdf-section">
                <h3 class="section-title">Contato</h3>
                <div class="contact-info">
                    <div class="info-row">
                        <div class="info-item">
                            <strong>E-mail Principal:</strong> {{ $customer->contact->email }}
                        </div>
                        <div class="info-item">
                            <strong>Telefone:</strong> {{ $customer->contact->phone ?? 'N/A' }}
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-item">
                            <strong>E-mail Comercial:</strong> {{ $customer->contact->email_business ?? 'N/A' }}
                        </div>
                        <div class="info-item">
                            <strong>Telefone Comercial:</strong> {{ $customer->contact->phone_business ?? 'N/A' }}
                        </div>
                    </div>
                    @if($customer->contact->website)
                        <div class="info-row">
                            <div class="info-item full-width">
                                <strong>Website:</strong> {{ $customer->contact->website }}
                            </div>
                        </div>
                    @endif
                </div>
            </section>
        @endif

        <!-- Endereço -->
        @if($customer->address)
            <section class="pdf-section">
                <h3 class="section-title">Endereço</h3>
                <div class="address-info">
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Logradouro:</strong> {{ $customer->address->address }}, {{ $customer->address->address_number }}
                            @if($customer->address->address_complement)
                                - {{ $customer->address->address_complement }}
                            @endif
                        </div>
                        <div class="info-item">
                            <strong>Bairro:</strong> {{ $customer->address->neighborhood }}
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Cidade:</strong> {{ $customer->address->city }}/{{ $customer->address->state }}
                        </div>
                        <div class="info-item">
                            <strong>CEP:</strong> {{ $customer->address->cep }}
                        </div>
                    </div>
                    @if($customer->address->country && $customer->address->country !== 'Brasil')
                        <div class="info-row">
                            <div class="info-item">
                                <strong>País:</strong> {{ $customer->address->country }}
                            </div>
                        </div>
                    @endif
                </div>
            </section>
        @endif

        <!-- Histórico de Transações -->
        <section class="pdf-section">
            <h3 class="section-title">Histórico de Transações</h3>
            <div class="transactions-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Total de Orçamentos:</strong> {{ $customer->budgets->count() }}
                    </div>
                    <div class="info-item">
                        <strong>Total de Faturas:</strong> {{ $customer->invoices->count() }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Valor Total Faturado:</strong> R$ {{ number_format($customer->invoices->sum('total'), 2, ',', '.') }}
                    </div>
                    <div class="info-item">
                        <strong>Valor Médio por Fatura:</strong>
                        R$ {{ $customer->invoices->count() > 0 ? number_format($customer->invoices->avg('total'), 2, ',', '.') : '0,00' }}
                    </div>
                </div>
            </div>
        </section>

<x-pdf.pdf-footer :company="$company" />
```

## 8. PDF Product Component

Componente para template de produto em PDF.

### Uso Básico

```blade
<x-pdf.pdf-product :product="$product" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `product` | `Product` | Modelo do produto | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

### Estrutura

```blade
@props([
    'product',
    'company' => [],
    'showLogo' => true
])

<x-pdf.pdf-header
    :title="'Ficha do Produto: ' . $product->name"
    :company="$company"
    :date="$product->created_at->format('d/m/Y')"
    :showLogo="$showLogo" />

        <!-- Informações Básicas -->
        <section class="pdf-section">
            <h3 class="section-title">Informações Básicas</h3>
            <div class="product-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Nome:</strong> {{ $product->name }}
                    </div>
                    <div class="info-item">
                        <strong>Código:</strong> {{ $product->code ?? 'N/A' }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item">
                        <strong>Status:</strong>
                        <x-product.product-status :product="$product" />
                    </div>
                    <div class="info-item">
                        <strong>Categoria:</strong> {{ $product->category?->name ?? 'N/A' }}
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-item full-width">
                        <strong>Descrição:</strong> {{ $product->description ?? 'N/A' }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Preço -->
        <section class="pdf-section">
            <h3 class="section-title">Preço</h3>
            <div class="price-info">
                <div class="info-row">
                    <div class="info-item">
                        <strong>Preço de Venda:</strong> R$ {{ number_format($product->price, 2, ',', '.') }}
                    </div>
                    <div class="info-item">
                        <strong>Preço de Custo:</strong> R$ {{ number_format($product->cost ?? 0, 2, ',', '.') }}
                    </div>
                </div>
                @if($product->cost)
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Lucro por Unidade:</strong> R$ {{ number_format($product->price - $product->cost, 2, ',', '.') }}
                        </div>
                        <div class="info-item">
                            <strong>Margem de Lucro:</strong>
                            {{ number_format((($product->price - $product->cost) / $product->cost) * 100, 2) }}%
                        </div>
                    </div>
                @endif
            </div>
        </section>

        <!-- Estoque -->
        @if($product->inventory)
            <section class="pdf-section">
                <h3 class="section-title">Estoque</h3>
                <div class="inventory-info">
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Quantidade Atual:</strong> {{ $product->inventory->quantity }}
                        </div>
                        <div class="info-item">
                            <strong>Estoque Mínimo:</strong> {{ $product->inventory->min_quantity }}
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Estoque Máximo:</strong> {{ $product->inventory->max_quantity ?? 'Ilimitado' }}
                        </div>
                        <div class="info-item">
                            <strong>Valor Total em Estoque:</strong> R$ {{ number_format($product->inventory->quantity * $product->price, 2, ',', '.') }}
                        </div>
                    </div>
                </div>
            </section>
        @endif

        <!-- Movimentações de Estoque -->
        @if($product->inventoryMovements->isNotEmpty())
            <section class="pdf-section">
                <h3 class="section-title">Movimentações de Estoque</h3>
                <div class="table-container">
                    <table class="pdf-table">
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Tipo</th>
                                <th>Quantidade</th>
                                <th>Motivo</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($product->inventoryMovements->take(10) as $movement)
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
            </section>
        @endif

        <!-- Imagem -->
        @if($product->image)
            <section class="pdf-section">
                <h3 class="section-title">Imagem do Produto</h3>
                <div class="product-image">
                    <img src="{{ public_path('storage/' . $product->image) }}"
                         alt="{{ $product->name }}"
                         style="max-width: 200px; height: auto;">
                </div>
            </section>
        @endif

<x-pdf.pdf-footer :company="$company" />
```

## 9. PDF Watermark Component

Componente para marca d'água em PDFs.

### Uso Básico

```blade
<x-pdf.pdf-watermark :text="$text" :opacity="$opacity" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `text` | `string` | Texto da marca d'água | Obrigatório |
| `opacity` | `float` | Opacidade da marca d'água | `0.1` |
| `color` | `string` | Cor da marca d'água | `#000000` |

### Estrutura

```blade
@props([
    'text',
    'opacity' => 0.1,
    'color' => '#000000'
])

<style>
    .pdf-watermark {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: {{ $opacity }};
        pointer-events: none;
        display: flex;
        align-items: center;
        justify-content: center;
        transform: rotate(-45deg);
    }

    .watermark-text {
        font-size: 120px;
        font-weight: bold;
        color: {{ $color }};
        text-align: center;
        line-height: 1;
    }
</style>

<div class="pdf-watermark">
    <div class="watermark-text">{{ $text }}</div>
</div>
```

## 10. PDF Styles Component

Componente para estilos CSS padrão de PDFs.

### Uso Básico

```blade
<x-pdf.pdf-styles />
```

### Estrutura

```blade
<style>
    /* Reset e Configurações Básicas */
    body {
        font-family: 'DejaVu Sans', sans-serif;
        font-size: 12px;
        line-height: 1.4;
        color: #333;
        margin: 0;
        padding: 0;
    }

    .pdf-container {
        width: 210mm;
        margin: 0 auto;
        padding: 20mm;
        box-sizing: border-box;
    }

    /* Cabeçalho */
    .pdf-header {
        margin-bottom: 20px;
        border-bottom: 2px solid #0d6efd;
        padding-bottom: 15px;
    }

    .header-content {
        display: flex;
        gap: 20px;
    }

    .company-logo img {
        max-height: 60px;
    }

    .company-info {
        flex: 2;
    }

    .company-name {
        font-size: 18px;
        font-weight: bold;
        margin: 0 0 10px 0;
        color: #0d6efd;
    }

    .company-details {
        font-size: 10px;
        color: #666;
    }

    .detail-item {
        margin-bottom: 2px;
    }

    .document-info {
        flex: 1;
        text-align: right;
    }

    .document-title {
        font-size: 16px;
        font-weight: bold;
        margin: 0 0 5px 0;
        color: #333;
    }

    .document-date, .document-number {
        font-size: 11px;
        color: #666;
        margin-bottom: 2px;
    }

    /* Conteúdo Principal */
    .pdf-main {
        margin-bottom: 20px;
    }

    /* Seções */
    .pdf-section {
        margin-bottom: 20px;
        page-break-inside: avoid;
    }

    .section-title {
        font-size: 14px;
        font-weight: bold;
        color: #0d6efd;
        margin: 0 0 10px 0;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }

    /* Tabelas */
    .table-container {
        overflow-x: auto;
        margin-bottom: 15px;
    }

    .pdf-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }

    .pdf-table th,
    .pdf-table td {
        border: 1px solid #ddd;
        padding: 6px 8px;
        text-align: left;
        vertical-align: top;
    }

    .pdf-table th {
        background-color: #f8f9fa;
        font-weight: bold;
        font-size: 12px;
    }

    .pdf-table tbody tr:nth-child(even) {
        background-color: #f8f9fa;
    }

    .pdf-table .text-right {
        text-align: right;
    }

    .pdf-table .text-center {
        text-align: center;
    }

    .total-row {
        background-color: #e9ecef !important;
        font-weight: bold;
    }

    /* Informações */
    .info-row {
        display: flex;
        gap: 20px;
        margin-bottom: 10px;
    }

    .info-item {
        flex: 1;
    }

    .info-item.full-width {
        flex: 100%;
    }

    .info-item strong {
        color: #333;
        font-weight: bold;
    }

    /* Status */
    .status-badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }

    .status-active {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .status-inactive {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .status-pending {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }

    .status-approved {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .status-rejected {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .status-paid {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .status-pending-payment {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }

    .status-overdue {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    /* Rodapé */
    .pdf-footer {
        margin-top: 40px;
        border-top: 1px solid #ddd;
        padding-top: 15px;
    }

    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 10px;
        color: #666;
    }

    .footer-left, .footer-center, .footer-right {
        flex: 1;
    }

    .footer-center {
        text-align: center;
    }

    .footer-right {
        text-align: right;
    }

    .footer-text {
        margin-bottom: 2px;
    }

    .small {
        font-size: 9px;
    }

    /* Assinaturas */
    .signatures {
        display: flex;
        justify-content: space-between;
        margin-top: 30px;
    }

    .signature-field {
        width: 45%;
        text-align: center;
    }

    .signature-line {
        border-bottom: 1px solid #333;
        height: 20px;
        margin-bottom: 5px;
    }

    .signature-label {
        font-size: 11px;
        font-weight: bold;
        color: #333;
    }

    /* Observações */
    .observations {
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #0d6efd;
        border-radius: 4px;
        font-size: 11px;
        line-height: 1.6;
    }

    /* Gráficos */
    .charts-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .chart-item {
        border: 1px solid #ddd;
        padding: 15px;
        text-align: center;
    }

    .chart-item h4 {
        margin: 0 0 10px 0;
        font-size: 12px;
        color: #333;
    }

    .chart-placeholder {
        background-color: #f8f9fa;
        padding: 20px;
        border: 1px dashed #ddd;
        color: #666;
        font-size: 11px;
    }

    /* Resumo Executivo */
    .executive-summary {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 4px;
    }

    .summary-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }

    .summary-item {
        background-color: white;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #ddd;
    }

    .summary-label {
        font-size: 10px;
        color: #666;
        margin-bottom: 5px;
    }

    .summary-value {
        font-size: 14px;
        font-weight: bold;
        color: #333;
    }

    /* Conclusões e Recomendações */
    .conclusion-item, .recommendation-item {
        background-color: #f8f9fa;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
        border-left: 4px solid #0d6efd;
    }

    .conclusion-item strong, .recommendation-item strong {
        color: #0d6efd;
        font-size: 12px;
    }

    /* Classes de utilidade */
    .text-primary { color: #0d6efd; }
    .text-success { color: #198754; }
    .text-danger { color: #dc3545; }
    .text-warning { color: #ffc107; }
    .text-info { color: #0dcaf0; }
    .text-secondary { color: #6c757d; }

    .bg-primary { background-color: #0d6efd; }
    .bg-success { background-color: #198754; }
    .bg-danger { background-color: #dc3545; }
    .bg-warning { background-color: #ffc107; }
    .bg-info { background-color: #0dcaf0; }
    .bg-secondary { background-color: #6c757d; }

    /* Quebra de página */
    .page-break {
        page-break-before: always;
    }

    /* Impedir quebra de página dentro de elementos */
    .no-page-break {
        page-break-inside: avoid;
    }
</style>
```

## 11. Integração com Padrões Existentes

### Uso em Controllers

```php
// BudgetController.php
public function pdf(Budget $budget)
{
    $company = [
        'name' => tenant('name'),
        'logo' => tenant('logo'),
        'cnpj' => tenant('cnpj'),
        'address' => tenant('address'),
        'phone' => tenant('phone'),
        'email' => tenant('email'),
        'document_number' => $budget->code
    ];

    $pdf = PDF::loadView('components.pdf.pdf-budget', [
        'budget' => $budget,
        'company' => $company
    ]);

    return $pdf->stream('budget-' . $budget->code . '.pdf');
}
```

### Uso em Views

```blade
{{-- Visualização de PDF --}}
<x-pdf.pdf-budget :budget="$budget" :company="$company" />

{{-- Geração de PDF --}}
<x-pdf.pdf-document
    :title="'Relatório: ' . $report->description"
    :company="$company"
    :content="$content" />
```

### Estilos CSS

```css
/* PDF Components Styles */
.pdf-container {
    width: 210mm;
    margin: 0 auto;
    padding: 20mm;
}

.pdf-table {
    width: 100%;
    border-collapse: collapse;
}

.pdf-table th, .pdf-table td {
    border: 1px solid #ddd;
    padding: 6px 8px;
}

.status-badge {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}
```

## 12. JavaScript Interatividade

### Visualização de PDF

```javascript
// pdf-viewer.js
document.addEventListener('DOMContentLoaded', function() {
    // Botões de download de PDF
    const pdfButtons = document.querySelectorAll('.btn-pdf');
    pdfButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                window.open(url, '_blank');
            }
        });
    });

    // Impressão de PDF
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });
});
```

## 13. Validação e Segurança

### Autorização

```php
// PdfPolicy.php
public function viewBudget(User $user, Budget $budget)
{
    return $user->tenant_id === $budget->tenant_id;
}

public function viewInvoice(User $user, Invoice $invoice)
{
    return $user->tenant_id === $invoice->tenant_id;
}

public function viewReport(User $user, Report $report)
{
    return $user->tenant_id === $report->tenant_id;
}
```

### Validations

```blade
{{-- PDF Budget com validação de permissões --}}
@can('viewBudget', $budget)
    <x-pdf.pdf-budget :budget="$budget" :company="$company" />
@endcan

{{-- PDF Invoice com validação de status --}}
@can('viewInvoice', $invoice)
    <x-pdf.pdf-invoice :invoice="$invoice" :company="$company" />
@endcan
```

Este padrão de components para PDFs garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
