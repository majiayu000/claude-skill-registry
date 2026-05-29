---
name: report-ui-components
description: Componentes de UI para relatórios seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para Relatórios

Esta skill define os componentes Blade específicos para a gestão de relatórios no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── report/
│   ├── report-card.blade.php        # Card resumido de relatório
│   ├── report-filters.blade.php     # Filtros específicos para relatórios
│   ├── report-chart.blade.php       # Gráficos e visualizações
│   ├── report-table.blade.php       # Tabelas de dados
│   ├── report-summary.blade.php     # Resumo e métricas
│   ├── report-actions.blade.php     # Ações disponíveis para relatórios
│   ├── report-date-range.blade.php  # Seleção de período
│   ├── report-export.blade.php      # Opções de exportação
│   ├── report-metrics.blade.php     # Métricas e KPIs
│   └── report-dashboard.blade.php   # Dashboard de relatórios
└── ...
```

## 1. Report Card Component

Componente para exibição resumida de relatórios em listas e dashboards.

### Uso Básico

```blade
<x-report.report-card :report="$report" :showType="true" :showDate="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `report` | `Report` | Modelo do relatório | Obrigatório |
| `showType` | `bool` | Exibir tipo de relatório | `true` |
| `showDate` | `bool` | Exibir data de geração | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'report',
    'showType' => true,
    'showDate' => true,
    'variant' => 'primary'
])

<div class="card border-0 shadow-sm h-100">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center gap-3">
                <div class="avatar-circle bg-{{ $variant }} bg-gradient">
                    @switch($report->type)
                        @case('financial')
                            <i class="bi bi-currency-dollar text-white"></i>
                            @break
                        @case('sales')
                            <i class="bi bi-graph-up text-white"></i>
                            @break
                        @case('inventory')
                            <i class="bi bi-box-seam text-white"></i>
                            @break
                        @case('customer')
                            <i class="bi bi-people text-white"></i>
                            @break
                        @default
                            <i class="bi bi-file-earmark-text text-white"></i>
                    @endswitch
                </div>
                <div>
                    <h6 class="mb-1 fw-bold">{{ $report->description }}</h6>
                    <small class="text-muted">{{ $report->type }}</small>
                </div>
            </div>
            <x-report.report-status :report="$report" />
        </div>

        @if($showType)
            <div class="mb-3">
                <span class="badge bg-secondary">{{ ucfirst($report->type) }}</span>
                @if($report->format)
                    <span class="badge bg-info ms-2">{{ strtoupper($report->format) }}</span>
                @endif
            </div>
        @endif

        @if($showDate)
            <div class="mb-3">
                <small class="text-muted">Gerado em</small>
                <div class="fw-semibold">{{ $report->generated_at?->format('d/m/Y H:i') ?? 'Não gerado' }}</div>
            </div>
        @endif

        @if($report->filters)
            <div class="mb-3">
                <small class="text-muted">Período</small>
                <div class="fw-semibold">
                    {{ $report->filters['start_date'] ?? 'N/A' }} até {{ $report->filters['end_date'] ?? 'N/A' }}
                </div>
            </div>
        @endif

        <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
                <small class="text-muted">Tamanho do Arquivo</small>
                <div class="fw-semibold">{{ $report->size ? number_format($report->size, 2) . ' KB' : 'Não disponível' }}</div>
            </div>

            <div class="btn-group btn-group-sm" role="group">
                @if($report->file_path)
                    <a href="{{ asset('storage/' . $report->file_path) }}"
                       class="btn btn-outline-primary"
                       target="_blank"
                       title="Visualizar Relatório">
                        <i class="bi bi-eye"></i> Ver
                    </a>
                @endif
                <button type="button"
                        class="btn btn-outline-secondary"
                        data-bs-toggle="modal"
                        data-bs-target="#generateModal-{{ $report->id }}"
                        title="Gerar Novamente">
                    <i class="bi bi-arrow-repeat"></i> Gerar
                </button>
            </div>
        </div>
    </div>
</div>
```

## 2. Report Filters Component

Componente para filtros específicos de geração de relatórios.

### Uso Básico

```blade
<x-report.report-filters :reportType="$reportType" :filters="$filters" :showDateRange="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `reportType` | `string` | Tipo de relatório | Obrigatório |
| `filters` | `array` | Filtros atuais | `[]` |
| `showDateRange` | `bool` | Exibir filtro de período | `true` |
| `showExportOptions` | `bool` | Exibir opções de exportação | `true` |

### Estrutura

```blade
@props([
    'reportType',
    'filters' => [],
    'showDateRange' => true,
    'showExportOptions' => true
])

<div class="report-filters">
    <form action="{{ route('provider.reports.generate') }}" method="POST" class="row g-3">
        @csrf
        <input type="hidden" name="type" value="{{ $reportType }}">

        <!-- Período -->
        @if($showDateRange)
            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Período</label>
                <div class="input-group">
                    <input type="date"
                           name="start_date"
                           class="form-control @error('start_date') is-invalid @enderror"
                           value="{{ $filters['start_date'] ?? '' }}" required>
                    <span class="input-group-text">até</span>
                    <input type="date"
                           name="end_date"
                           class="form-control @error('end_date') is-invalid @enderror"
                           value="{{ $filters['end_date'] ?? '' }}" required>
                    @error('start_date')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                    @error('end_date')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>
            </div>
        @endif

        <!-- Filtros Específicos por Tipo -->
        @switch($reportType)
            @case('financial')
                <div class="col-md-6">
                    <label class="form-label small fw-bold text-muted text-uppercase">Status de Faturas</label>
                    <select name="invoice_status" class="form-select">
                        <option value="">Todos os status</option>
                        <option value="paid" {{ ($filters['invoice_status'] ?? '') == 'paid' ? 'selected' : '' }}>Pagas</option>
                        <option value="pending" {{ ($filters['invoice_status'] ?? '') == 'pending' ? 'selected' : '' }}>Pendentes</option>
                        <option value="overdue" {{ ($filters['invoice_status'] ?? '') == 'overdue' ? 'selected' : '' }}>Vencidas</option>
                    </select>
                </div>
                @break

            @case('sales')
                <div class="col-md-6">
                    <label class="form-label small fw-bold text-muted text-uppercase">Status de Orçamentos</label>
                    <select name="budget_status" class="form-select">
                        <option value="">Todos os status</option>
                        <option value="approved" {{ ($filters['budget_status'] ?? '') == 'approved' ? 'selected' : '' }}>Aprovados</option>
                        <option value="pending" {{ ($filters['budget_status'] ?? '') == 'pending' ? 'selected' : '' }}>Pendentes</option>
                        <option value="rejected" {{ ($filters['budget_status'] ?? '') == 'rejected' ? 'selected' : '' }}>Rejeitados</option>
                    </select>
                </div>
                @break

            @case('inventory')
                <div class="col-md-6">
                    <label class="form-label small fw-bold text-muted text-uppercase">Status de Produtos</label>
                    <select name="product_status" class="form-select">
                        <option value="">Todos os status</option>
                        <option value="active" {{ ($filters['product_status'] ?? '') == 'active' ? 'selected' : '' }}>Ativos</option>
                        <option value="inactive" {{ ($filters['product_status'] ?? '') == 'inactive' ? 'selected' : '' }}>Inativos</option>
                    </select>
                </div>
                @break

            @case('customer')
                <div class="col-md-6">
                    <label class="form-label small fw-bold text-muted text-uppercase">Status de Clientes</label>
                    <select name="customer_status" class="form-select">
                        <option value="">Todos os status</option>
                        <option value="active" {{ ($filters['customer_status'] ?? '') == 'active' ? 'selected' : '' }}>Ativos</option>
                        <option value="inactive" {{ ($filters['customer_status'] ?? '') == 'inactive' ? 'selected' : '' }}>Inativos</option>
                    </select>
                </div>
                @break
        @endswitch

        <!-- Opções de Exportação -->
        @if($showExportOptions)
            <div class="col-md-6">
                <label class="form-label small fw-bold text-muted text-uppercase">Formato de Exportação</label>
                <div class="btn-group w-100" role="group">
                    <input type="radio" class="btn-check" name="format" id="format_pdf" value="pdf" checked>
                    <label class="btn btn-outline-primary" for="format_pdf">
                        <i class="bi bi-file-pdf me-2"></i>PDF
                    </label>

                    <input type="radio" class="btn-check" name="format" id="format_excel" value="excel">
                    <label class="btn btn-outline-success" for="format_excel">
                        <i class="bi bi-file-earmark-excel me-2"></i>Excel
                    </label>

                    <input type="radio" class="btn-check" name="format" id="format_csv" value="csv">
                    <label class="btn btn-outline-info" for="format_csv">
                        <i class="bi bi-file-earmark-text me-2"></i>CSV
                    </label>
                </div>
            </div>
        @endif

        <!-- Ações -->
        <div class="col-12">
            <div class="d-flex justify-content-between">
                <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-file-earmark-plus me-2"></i>Gerar Relatório
                    </button>
                    <button type="button" class="btn btn-outline-secondary" onclick="window.history.back()">
                        <i class="bi bi-arrow-left me-2"></i>Voltar
                    </button>
                </div>

                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-warning" onclick="location.reload()">
                        <i class="bi bi-arrow-clockwise me-2"></i>Limpar Filtros
                    </button>
                </div>
            </div>
        </div>
    </form>
</div>
```

## 3. Report Chart Component

Componente para exibição de gráficos e visualizações de dados.

### Uso Básico

```blade
<x-report.report-chart :chartData="$chartData" :chartType="$chartType" :title="$title" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `chartData` | `array` | Dados para o gráfico | Obrigatório |
| `chartType` | `string` | Tipo de gráfico (line, bar, pie, doughnut) | `bar` |
| `title` | `string` | Título do gráfico | `''` |
| `height` | `string` | Altura do gráfico | `400px` |

### Estrutura

```blade
@props([
    'chartData',
    'chartType' => 'bar',
    'title' => '',
    'height' => '400px'
])

<div class="report-chart">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">{{ $title }}</h6>
        </div>
        <div class="card-body">
            <div class="chart-container" style="height: {{ $height }}">
                <canvas id="chart-{{ Str::random(8) }}" data-chart-type="{{ $chartType }}" data-chart-data='@json($chartData)'></canvas>
            </div>
        </div>
    </div>
</div>

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.querySelector('canvas[data-chart-data]');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        const chartType = canvas.dataset.chartType;
        const chartData = JSON.parse(canvas.dataset.chartData);

        const config = {
            type: chartType,
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: canvas.closest('.card').querySelector('.card-header h6').textContent
                    }
                },
                scales: chartType === 'line' || chartType === 'bar' ? {
                    y: {
                        beginAtZero: true
                    }
                } : {}
            }
        };

        new Chart(ctx, config);
    }
});
</script>
@endpush
```

## 4. Report Table Component

Componente para exibição de tabelas de dados em relatórios.

### Uso Básico

```blade
<x-report.report-table :headers="$headers" :data="$data" :showPagination="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `headers` | `array` | Cabeçalhos da tabela | Obrigatório |
| `data` | `array` | Dados da tabela | Obrigatório |
| `showPagination` | `bool` | Exibir paginação | `true` |
| `perPage` | `int` | Itens por página | `10` |

### Estrutura

```blade
@props([
    'headers',
    'data',
    'showPagination' => true,
    'perPage' => 10
])

<div class="report-table">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <div class="d-flex justify-content-between align-items-center">
                <h6 class="mb-0">Dados do Relatório</h6>
                <div class="text-muted small">
                    Total: {{ count($data) }} registros
                </div>
            </div>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            @foreach($headers as $header)
                                <th>{{ $header }}</th>
                            @endforeach
                        </tr>
                    </thead>
                    <tbody>
                        @forelse($data as $row)
                            <tr>
                                @foreach($headers as $key => $header)
                                    <td>
                                        @if(is_array($row))
                                            {{ $row[$key] ?? '' }}
                                        @else
                                            {{ $row->$key ?? '' }}
                                        @endif
                                    </td>
                                @endforeach
                            </tr>
                        @empty
                            <tr>
                                <td colspan="{{ count($headers) }}" class="text-center text-muted py-4">
                                    <i class="bi bi-file-earmark-text me-2"></i>
                                    Nenhum dado encontrado
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>

            @if($showPagination && count($data) > $perPage)
                <div class="card-footer bg-transparent border-0">
                    <nav aria-label="Paginação do relatório">
                        <ul class="pagination pagination-sm justify-content-end mb-0">
                            <li class="page-item disabled">
                                <span class="page-link">Página 1 de {{ ceil(count($data) / $perPage) }}</span>
                            </li>
                        </ul>
                    </nav>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 5. Report Summary Component

Componente para exibição de resumo e métricas do relatório.

### Uso Básico

```blade
<x-report.report-summary :metrics="$metrics" :showKPIs="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `metrics` | `array` | Métricas do relatório | Obrigatório |
| `showKPIs` | `bool` | Exibir KPIs principais | `true` |
| `variant` | `string` | Estilo do resumo (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'metrics',
    'showKPIs' => true,
    'variant' => 'primary'
])

<div class="report-summary">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Resumo do Relatório</h6>
        </div>
        <div class="card-body">
            @if($showKPIs)
                <div class="row g-3 mb-4">
                    @foreach($metrics as $metric)
                        <div class="col-md-3">
                            <div class="card border-0 bg-{{ $variant }} bg-gradient text-white">
                                <div class="card-body text-center">
                                    <div class="avatar-circle bg-white bg-gradient mb-2 mx-auto" style="width: 50px; height: 50px;">
                                        <i class="bi bi-{{ $metric['icon'] ?? 'graph-up' }} text-{{ $variant }}"></i>
                                    </div>
                                    <div class="fw-bold fs-4">{{ $metric['value'] }}</div>
                                    <div class="small">{{ $metric['label'] }}</div>
                                </div>
                            </div>
                        </div>
                    @endforeach
                </div>
            @endif

            <!-- Detalhes do Relatório -->
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="text-muted small">Tipo de Relatório</label>
                        <div class="fw-bold">{{ ucfirst($metrics['type'] ?? 'N/A') }}</div>
                    </div>
                    <div class="mb-3">
                        <label class="text-muted small">Período</label>
                        <div class="fw-bold">
                            {{ $metrics['start_date'] ?? 'N/A' }} até {{ $metrics['end_date'] ?? 'N/A' }}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="text-muted small">Formato</label>
                        <div class="fw-bold">{{ strtoupper($metrics['format'] ?? 'N/A') }}</div>
                    </div>
                    <div class="mb-3">
                        <label class="text-muted small">Gerado em</label>
                        <div class="fw-bold">{{ $metrics['generated_at'] ?? 'N/A' }}</div>
                    </div>
                </div>
            </div>

            <!-- Observações -->
            @if(isset($metrics['observations']))
                <div class="row mt-3">
                    <div class="col-12">
                        <div class="alert alert-info" role="alert">
                            <i class="bi bi-info-circle me-2"></i>
                            <strong>Observações:</strong> {{ $metrics['observations'] }}
                        </div>
                    </div>
                </div>
            @endif
        </div>
    </div>
</div>
```

## 6. Report Actions Component

Componente para exibição de ações disponíveis para relatórios.

### Uso Básico

```blade
<x-report.report-actions :report="$report" :showDownload="true" :showShare="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `report` | `Report` | Modelo do relatório | Obrigatório |
| `showDownload` | `bool` | Exibir botão de download | `true` |
| `showShare` | `bool` | Exibir botão de compartilhamento | `true` |
| `showDelete` | `bool` | Exibir botão de exclusão | `true` |

### Estrutura

```blade
@props([
    'report',
    'showDownload' => true,
    'showShare' => true,
    'showDelete' => true
])

<div class="report-actions btn-group" role="group">
    <!-- Visualizar -->
    @if($report->file_path)
        <a href="{{ asset('storage/' . $report->file_path) }}"
           class="btn btn-outline-primary"
           target="_blank"
           title="Visualizar Relatório">
            <i class="bi bi-eye"></i> Visualizar
        </a>
    @endif

    <!-- Download -->
    @if($showDownload && $report->file_path)
        <a href="{{ route('provider.reports.download', $report) }}"
           class="btn btn-outline-success"
           title="Download Relatório">
            <i class="bi bi-download"></i> Download
        </a>
    @endif

    <!-- Compartilhar -->
    @if($showShare)
        <button type="button"
                class="btn btn-outline-info"
                data-bs-toggle="modal"
                data-bs-target="#shareModal-{{ $report->id }}"
                title="Compartilhar Relatório">
            <i class="bi bi-share"></i> Compartilhar
        </button>
    @endif

    <!-- Gerar Novamente -->
    <button type="button"
            class="btn btn-outline-warning"
            data-bs-toggle="modal"
            data-bs-target="#generateModal-{{ $report->id }}"
            title="Gerar Novamente">
        <i class="bi bi-arrow-repeat"></i> Regenerar
    </button>

    <!-- Excluir -->
    @if($showDelete)
        <button type="button"
                class="btn btn-outline-danger"
                data-bs-toggle="modal"
                data-bs-target="#deleteModal-{{ $report->id }}"
                title="Excluir Relatório">
            <i class="bi bi-trash"></i> Excluir
        </button>
    @endif
</div>
```

## 7. Report Date Range Component

Componente para seleção de período em relatórios.

### Uso Básico

```blade
<x-report.report-date-range :startDate="$startDate" :endDate="$endDate" :showPresets="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `startDate` | `string` | Data inicial | `''` |
| `endDate` | `string` | Data final | `''` |
| `showPresets` | `bool` | Exibir períodos predefinidos | `true` |
| `namePrefix` | `string` | Prefixo para nomes dos campos | `''` |

### Estrutura

```blade
@props([
    'startDate' => '',
    'endDate' => '',
    'showPresets' => true,
    'namePrefix' => ''
])

<div class="report-date-range">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Selecione o Período</h6>
        </div>
        <div class="card-body">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label small fw-bold text-muted text-uppercase">Data Inicial</label>
                    <input type="date"
                           name="{{ $namePrefix }}start_date"
                           class="form-control @error($namePrefix . 'start_date') is-invalid @enderror"
                           value="{{ $startDate }}" required>
                    @error($namePrefix . 'start_date')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>
                <div class="col-md-6">
                    <label class="form-label small fw-bold text-muted text-uppercase">Data Final</label>
                    <input type="date"
                           name="{{ $namePrefix }}end_date"
                           class="form-control @error($namePrefix . 'end_date') is-invalid @enderror"
                           value="{{ $endDate }}" required>
                    @error($namePrefix . 'end_date')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>
            </div>

            @if($showPresets)
                <div class="row mt-3">
                    <div class="col-12">
                        <label class="form-label small fw-bold text-muted text-uppercase">Períodos Rápidos</label>
                        <div class="btn-group w-100" role="group">
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="setDateRange('today')">
                                Hoje
                            </button>
                            <button type="button" class="btn btn-outline-secondary btn-sm" onclick="setDateRange('this_week')">
                                Esta Semana
                            </button>
                            <button type="button" class="btn btn-outline-info btn-sm" onclick="setDateRange('this_month')">
                                Este Mês
                            </button>
                            <button type="button" class="btn btn-outline-warning btn-sm" onclick="setDateRange('last_month')">
                                Mês Passado
                            </button>
                            <button type="button" class="btn btn-outline-success btn-sm" onclick="setDateRange('this_year')">
                                Este Ano
                            </button>
                        </div>
                    </div>
                </div>
            @endif
        </div>
    </div>
</div>

@push('scripts')
<script>
function setDateRange(period) {
    const today = new Date();
    const startInput = document.querySelector('input[name="{{ $namePrefix }}start_date"]');
    const endInput = document.querySelector('input[name="{{ $namePrefix }}end_date"]');

    let startDate, endDate;

    switch(period) {
        case 'today':
            startDate = endDate = today.toISOString().split('T')[0];
            break;
        case 'this_week':
            const dayOfWeek = today.getDay();
            const diffToMonday = today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
            startDate = new Date(today.setDate(diffToMonday)).toISOString().split('T')[0];
            endDate = new Date(today.setDate(diffToMonday + 6)).toISOString().split('T')[0];
            break;
        case 'this_month':
            startDate = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0];
            endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0).toISOString().split('T')[0];
            break;
        case 'last_month':
            startDate = new Date(today.getFullYear(), today.getMonth() - 1, 1).toISOString().split('T')[0];
            endDate = new Date(today.getFullYear(), today.getMonth(), 0).toISOString().split('T')[0];
            break;
        case 'this_year':
            startDate = new Date(today.getFullYear(), 0, 1).toISOString().split('T')[0];
            endDate = new Date(today.getFullYear(), 11, 31).toISOString().split('T')[0];
            break;
    }

    if (startInput) startInput.value = startDate;
    if (endInput) endInput.value = endDate;
}
</script>
@endpush
```

## 8. Report Export Component

Componente para opções de exportação de relatórios.

### Uso Básico

```blade
<x-report.report-export :formats="$formats" :report="$report" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `formats` | `array` | Formatos disponíveis | `['pdf', 'excel', 'csv']` |
| `report` | `Report` | Modelo do relatório | Obrigatório |

### Estrutura

```blade
@props([
    'formats' => ['pdf', 'excel', 'csv'],
    'report'
])

<div class="report-export">
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-transparent border-0">
            <h6 class="mb-0">Opções de Exportação</h6>
        </div>
        <div class="card-body">
            <div class="row g-3">
                @foreach($formats as $format)
                    <div class="col-md-4">
                        <div class="card border-0 h-100">
                            <div class="card-body text-center">
                                <div class="avatar-circle bg-{{ $format === 'pdf' ? 'danger' : ($format === 'excel' ? 'success' : 'info') }} bg-gradient mb-3 mx-auto">
                                    <i class="bi bi-file-{{ $format === 'pdf' ? 'pdf' : ($format === 'excel' ? 'earmark-excel' : 'earmark-text') }} text-white"></i>
                                </div>
                                <h6 class="mb-2">{{ ucfirst($format) }}</h6>
                                <p class="text-muted small mb-3">
                                    @switch($format)
                                        @case('pdf')
                                            Formato ideal para impressão e visualização
                                            @break
                                        @case('excel')
                                            Planilha para análise e manipulação de dados
                                            @break
                                        @case('csv')
                                            Arquivo texto para importação em outros sistemas
                                            @break
                                    @endswitch
                                </p>
                                <a href="{{ route('provider.reports.export', ['report' => $report, 'format' => $format]) }}"
                                   class="btn btn-outline-{{ $format === 'pdf' ? 'danger' : ($format === 'excel' ? 'success' : 'info') }} btn-sm">
                                    <i class="bi bi-download me-2"></i>Exportar {{ ucfirst($format) }}
                                </a>
                            </div>
                        </div>
                    </div>
                @endforeach
            </div>
        </div>
    </div>
</div>
```

## 9. Report Metrics Component

Componente para exibição de métricas e KPIs.

### Uso Básico

```blade
<x-report.report-metrics :metrics="$metrics" :showTrends="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `metrics` | `array` | Métricas a serem exibidas | Obrigatório |
| `showTrends` | `bool` | Exibir tendências | `true` |
| `variant` | `string` | Estilo dos cards (primary, secondary, etc.) | `primary` |

### Estrutura

```blade
@props([
    'metrics',
    'showTrends' => true,
    'variant' => 'primary'
])

<div class="report-metrics">
    <div class="row g-3">
        @foreach($metrics as $metric)
            <div class="col-md-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <div class="avatar-circle bg-{{ $variant }} bg-gradient mb-2">
                                    <i class="bi bi-{{ $metric['icon'] ?? 'graph-up' }} text-white"></i>
                                </div>
                                <div class="text-muted small">{{ $metric['label'] }}</div>
                                <div class="fw-bold fs-4">{{ $metric['value'] }}</div>
                            </div>

                            @if($showTrends && isset($metric['trend']))
                                <div class="text-end">
                                    <div class="badge {{ $metric['trend'] >= 0 ? 'bg-success' : 'bg-danger' }}">
                                        {{ $metric['trend'] >= 0 ? '+' : '' }}{{ number_format($metric['trend'], 1) }}%
                                    </div>
                                    <div class="text-muted small mt-1">vs período anterior</div>
                                </div>
                            @endif
                        </div>

                        @if(isset($metric['description']))
                            <div class="mt-2">
                                <small class="text-muted">{{ $metric['description'] }}</small>
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        @endforeach
    </div>
</div>
```

## 10. Report Dashboard Component

Componente para dashboard de relatórios.

### Uso Básico

```blade
<x-report.report-dashboard :reports="$reports" :metrics="$metrics" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `reports` | `Collection` | Relatórios recentes | Obrigatório |
| `metrics` | `array` | Métricas do dashboard | `[]` |

### Estrutura

```blade
@props([
    'reports',
    'metrics' => []
])

<div class="report-dashboard">
    <!-- Métricas Principais -->
    @if(!empty($metrics))
        <x-report.report-metrics :metrics="$metrics" />
    @endif

    <!-- Relatórios Recentes -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-transparent border-0">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">Relatórios Recentes</h6>
                        <a href="{{ route('provider.reports.index') }}" class="btn btn-outline-primary btn-sm">
                            <i class="bi bi-list me-2"></i>Ver Todos
                        </a>
                    </div>
                </div>
                <div class="card-body">
                    @if($reports->isNotEmpty())
                        <div class="row g-3">
                            @foreach($reports as $report)
                                <div class="col-md-6 col-lg-4">
                                    <x-report.report-card :report="$report" />
                                </div>
                            @endforeach
                        </div>
                    @else
                        <div class="text-center py-4">
                            <i class="bi bi-file-earmark-text text-muted" style="font-size: 3rem;"></i>
                            <p class="text-muted mt-2">Nenhum relatório encontrado</p>
                            <a href="{{ route('provider.reports.create') }}" class="btn btn-primary">
                                <i class="bi bi-file-earmark-plus me-2"></i>Gerar Novo Relatório
                            </a>
                        </div>
                    @endif
                </div>
            </div>
        </div>
    </div>

    <!-- Tipos de Relatórios Disponíveis -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-transparent border-0">
                    <h6 class="mb-0">Tipos de Relatórios Disponíveis</h6>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-md-3">
                            <div class="card border-0 h-100">
                                <div class="card-body text-center">
                                    <div class="avatar-circle bg-primary bg-gradient mb-3 mx-auto">
                                        <i class="bi bi-currency-dollar text-white"></i>
                                    </div>
                                    <h6 class="mb-2">Financeiro</h6>
                                    <p class="text-muted small mb-3">Relatórios de receitas, despesas e lucratividade</p>
                                    <a href="{{ route('provider.reports.create', ['type' => 'financial']) }}" class="btn btn-outline-primary btn-sm">
                                        <i class="bi bi-file-earmark-plus me-2"></i>Gerar
                                    </a>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-3">
                            <div class="card border-0 h-100">
                                <div class="card-body text-center">
                                    <div class="avatar-circle bg-success bg-gradient mb-3 mx-auto">
                                        <i class="bi bi-graph-up text-white"></i>
                                    </div>
                                    <h6 class="mb-2">Vendas</h6>
                                    <p class="text-muted small mb-3">Relatórios de orçamentos, faturas e performance</p>
                                    <a href="{{ route('provider.reports.create', ['type' => 'sales']) }}" class="btn btn-outline-success btn-sm">
                                        <i class="bi bi-file-earmark-plus me-2"></i>Gerar
                                    </a>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-3">
                            <div class="card border-0 h-100">
                                <div class="card-body text-center">
                                    <div class="avatar-circle bg-info bg-gradient mb-3 mx-auto">
                                        <i class="bi bi-box-seam text-white"></i>
                                    </div>
                                    <h6 class="mb-2">Estoque</h6>
                                    <p class="text-muted small mb-3">Relatórios de controle de estoque e movimentações</p>
                                    <a href="{{ route('provider.reports.create', ['type' => 'inventory']) }}" class="btn btn-outline-info btn-sm">
                                        <i class="bi bi-file-earmark-plus me-2"></i>Gerar
                                    </a>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-3">
                            <div class="card border-0 h-100">
                                <div class="card-body text-center">
                                    <div class="avatar-circle bg-warning bg-gradient mb-3 mx-auto">
                                        <i class="bi bi-people text-white"></i>
                                    </div>
                                    <h6 class="mb-2">Clientes</h6>
                                    <p class="text-muted small mb-3">Relatórios de base de clientes e interações</p>
                                    <a href="{{ route('provider.reports.create', ['type' => 'customer']) }}" class="btn btn-outline-warning btn-sm">
                                        <i class="bi bi-file-earmark-plus me-2"></i>Gerar
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

## 11. Integração com Padrões Existentes

### Uso em Views

```blade
{{-- Dashboard --}}
<x-report.report-dashboard :reports="$reports" :metrics="$metrics" />

{{-- Listagem --}}
<x-report.report-card :report="$report" />

{{-- Geração --}}
<x-report.report-filters :reportType="$reportType" :filters="$filters" />

{{-- Visualização --}}
<x-report.report-summary :metrics="$metrics" />
<x-report.report-chart :chartData="$chartData" :chartType="'bar'" :title="'Vendas Mensais'" />
<x-report.report-table :headers="$headers" :data="$data" />
```

### Estilos CSS

```css
/* Report Components Styles */
.report-chart .chart-container {
    position: relative;
    height: 400px;
    width: 100%;
}

.report-metrics .card {
    border-left: 4px solid #0d6efd;
}

.report-metrics .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.report-actions .btn {
    transition: all 0.2s ease;
}

.report-actions .btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.report-date-range .btn-group .btn {
    flex: 1;
}
```

## 12. JavaScript Interatividade

### Dashboard de Relatórios

```javascript
// report-dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar gráficos dinamicamente
    const charts = document.querySelectorAll('canvas[data-chart-data]');
    charts.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        const chartType = canvas.dataset.chartType;
        const chartData = JSON.parse(canvas.dataset.chartData);

        new Chart(ctx, {
            type: chartType,
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    });

    // Filtros de data rápidos
    const dateRangeButtons = document.querySelectorAll('.btn-group .btn');
    dateRangeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Implementar lógica de filtros rápidos
        });
    });
});
```

## 13. Validação e Segurança

### Autorização

```php
// ReportPolicy.php
public function view(User $user, Report $report)
{
    return $user->tenant_id === $report->tenant_id;
}

public function generate(User $user)
{
    return $user->can('manage-reports');
}

public function delete(User $user, Report $report)
{
    return $user->tenant_id === $report->tenant_id &&
           $user->can('delete-reports');
}
```

### Validations

```blade
{{-- Report Card com validação de permissões --}}
@can('view', $report)
    <x-report.report-card :report="$report" />
@endcan

{{-- Report Actions com validação de status --}}
@can('generate')
    <x-report.report-actions :report="$report" />
@endcan
```

Este padrão de components para relatórios garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
