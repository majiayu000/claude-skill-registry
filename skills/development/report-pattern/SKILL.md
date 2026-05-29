---
name: report-pattern
description: Garante padrões consistentes para relatórios no Easy Budget (filtros, exportação, visualização).
---

# Padrão de Relatórios do Easy Budget

Esta skill define os padrões obrigatórios para criação de relatórios no sistema Easy Budget, incluindo filtros de data, exportação e visualização.

## Estrutura de Relatório

```
resources/views/pages/[module]/
└── report.blade.php   # Página de relatório com filtros
```

## 1. Report Pattern - Estrutura Base

### Cabeçalho do Relatório

```blade
<x-page-header
    title="Relatório de [Módulo]"
    icon="clipboard-data"
    :breadcrumb-items="[
        '[Módulo]' => route('provider.[modulo].index'),
        'Relatório' => '#'
    ]">
    <p class="text-muted mb-0">Resumo e detalhes conforme filtros aplicados</p>
</x-page-header>
```

### Card de Filtros (Estado Inicial)

O relatório deve iniciar **vazio** (`isInitial`).

```blade
<div class="card border-0 shadow-sm mb-4">
    <div class="card-body">
        <form action="{{ route('provider.[modulo].report') }}" method="GET" id="reportForm">
            <div class="row g-3">
                <!-- Filtro de Tipo -->
                <div class="col-md-4">
                    <label for="type" class="form-label small fw-bold text-muted text-uppercase">Tipo</label>
                    <select name="type" id="type" class="form-select tom-select">
                        <option value="">Todos</option>
                        <option value="type_a">Tipo A</option>
                        <option value="type_b">Tipo B</option>
                    </select>
                </div>

                <!-- Data Inicial -->
                <div class="col-md-4">
                    <label for="start_date" class="form-label small fw-bold text-muted text-uppercase">
                        {{ $isFinancialReport ? 'Período Inicial' : 'Cadastro Inicial' }}
                    </label>
                    <input type="text" id="start_date" name="start_date"
                        class="form-control"
                        value="{{ old('start_date') }}"
                        inputmode="numeric" placeholder="DD/MM/AAAA" required>
                </div>

                <!-- Data Final -->
                <div class="col-md-4">
                    <label for="end_date" class="form-label small fw-bold text-muted text-uppercase">
                        {{ $isFinancialReport ? 'Período Final' : 'Cadastro Final' }}
                    </label>
                    <input type="text" id="end_date" name="end_date"
                        class="form-control"
                        value="{{ old('end_date') }}"
                        inputmode="numeric" placeholder="DD/MM/AAAA" required>
                </div>
            </div>

            <div class="d-flex gap-2 mt-3">
                <x-button type="submit" variant="primary" icon="search" label="Filtrar" class="flex-grow-1" id="btnFilter" />
                <x-button type="link" :href="route('provider.[modulo].report')" variant="outline-secondary" icon="x" label="Limpar" />
            </div>
        </form>
    </div>
</div>
```

### Estado Inicial (Aguardando Filtros)

```blade
@if($isInitial)
    <div class="card border-0 shadow-sm">
        <div class="card-body text-center py-5">
            <i class="bi bi-funnel text-muted" style="font-size: 3rem;"></i>
            <h5 class="mt-3 text-muted">Aguardando Filtros</h5>
            <p class="text-muted">Selecione os parâmetros acima e clique em Filtrar para gerar o relatório.</p>
        </div>
    </div>
@else
    <!-- Resultados do Relatório -->
    <div class="card border-0 shadow-sm">
        <!-- ... conteúdo dos resultados ... -->
    </div>
@endif
```

## 2. Campos de Data - Padrão Obrigatório

### Labels por Contexto

| Tipo de Relatório | Label Data Inicial | Label Data Final |
|-------------------|-------------------|------------------|
| Registros (Produtos, Categorias) | "Cadastro Inicial" | "Cadastro Final" |
| Movimentação/Financeiro | "Período Inicial" | "Período Final" |

### Implementação JavaScript de Validação

```javascript
const parseDate = (str) => {
    if (!str) return null;
    const parts = str.split('/');
    if (parts.length === 3) {
        const d = new Date(parts[2], parts[1] - 1, parts[0]);
        return isNaN(d.getTime()) ? null : d;
    }
    return null;
};

const validateDates = () => {
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');
    if (!startDate || !endDate || !startDate.value || !endDate.value) return true;

    const start = parseDate(startDate.value);
    const end = parseDate(endDate.value);

    if (start && end && start > end) {
        const message = 'A data inicial não pode ser maior que a data final.';
        if (window.easyAlert) {
            window.easyAlert.warning(message);
        } else {
            alert(message);
        }
        return false;
    }
    return true;
};

// No submit do formulário
document.getElementById('reportForm').addEventListener('submit', function(e) {
    if (!validateDates()) {
        e.preventDefault();
        return;
    }

    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;

    if (startDate && !endDate) {
        e.preventDefault();
        const message = 'Para filtrar por período, informe as datas inicial e final.';
        if (window.easyAlert) window.easyAlert.error(message);
        document.getElementById('end_date').focus();
    } else if (!startDate && endDate) {
        e.preventDefault();
        const message = 'Para filtrar por período, informe as datas inicial e final.';
        if (window.easyAlert) window.easyAlert.error(message);
        document.getElementById('start_date').focus();
    }
});
```

## 3. Tabela de Resultados

### Desktop (modern-table)

```blade
<div class="desktop-view">
    <div class="table-responsive">
        <table class="modern-table table mb-0">
            <thead>
                <tr>
                    <th>Coluna 1</th>
                    <th>Coluna 2</th>
                    <th class="text-end">Valor</th>
                    <th class="text-center">Ações</th>
                </tr>
            </thead>
            <tbody>
                @foreach($reportData as $item)
                    <tr>
                        <td>{{ $item->field1 }}</td>
                        <td>{{ $item->field2 }}</td>
                        <td class="text-end">{{ formatCurrency($item->value) }}</td>
                        <td class="text-center">
                            <a href="#" class="btn btn-sm btn-outline-secondary">
                                <i class="bi bi-eye"></i>
                            </a>
                        </td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    </div>
</div>
```

### Mobile (list-group)

```blade
<div class="mobile-view">
    <div class="list-group list-group-flush">
        @foreach($reportData as $item)
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <div class="fw-semibold">{{ $item->field1 }}</div>
                        <div class="text-muted small">{{ $item->field2 }}</div>
                    </div>
                    <div class="text-end">
                        <div class="fw-semibold">{{ formatCurrency($item->value) }}</div>
                    </div>
                </div>
            </div>
        @endforeach
    </div>
</div>
```

## 4. Exportação

### Botões de Exportação

```blade
<div class="d-flex gap-2 mb-3">
    <x-button variant="outline-success" icon="file-earmark-excel"
        :href="route('provider.[modulo].export', array_merge(request()->all(), ['format' => 'xlsx']))"
        label="Excel" />
    <x-button variant="outline-danger" icon="file-earmark-pdf"
        :href="route('provider.[modulo].export', array_merge(request()->all(), ['format' => 'pdf']))"
        label="PDF" />
</div>
```

### Regras de Exportação

- **Formato**: Sempre disponibilizar **PDF** e **Excel**
- **CSV**: Remover opção CSV (conforme padrão)
- **Filtros**: Exportação deve respeitar filtros aplicados
- **Dados**: Exportar apenas resultados filtrados (não estado inicial)

## 5. Integração com Backend

### Service - Processamento de Relatório

```php
public function getReportData(array $filters = []): ServiceResult
{
    return $this->safeExecute(function () use ($filters) {
        // 1. Definir parâmetros
        $startDate = $filters['start_date'] ?? null;
        $endDate = $filters['end_date'] ?? null;
        $type = $filters['type'] ?? null;

        // 2. Verificar Estado Inicial
        $isInitial = empty($startDate) && empty($endDate) && empty($type);

        if ($isInitial) {
            return [
                'reportData' => new \Illuminate\Pagination\LengthAwarePaginator([], 0, 10),
                'isInitial' => true,
                'summary' => null,
                'filters' => $filters,
            ];
        }

        // 3. Validar e processar
        $query = $this->buildReportQuery($filters);

        $data = $query->paginate(20);
        $summary = $this->calculateSummary($filters);

        return [
            'reportData' => $data,
            'isInitial' => false,
            'summary' => $summary,
            'filters' => $filters,
        ];
    });
}
```

## 6. Checklist de Implementação

- [ ] Page header com icon e breadcrumb
- [ ] Card de filtros com estado inicial vazio
- [ ] Labels corretos (Cadastro/Período)
- [ ] Inputs de data com máscara DD/MM/AAAA
- [ ] Validação JavaScript de datas
- [ ] Botões Filtrar/Limpar padronizados
- [ ] Tabela desktop com modern-table
- [ ] Lista mobile com list-group
- [ ] Exportação PDF e Excel
- [ ] Service com processamento de filtros
