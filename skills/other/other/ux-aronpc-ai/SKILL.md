---
name: ux
description: >-
  Otimiza UX com Laravel Precognition, Prompts e Turbo para interações fluidas. Use quando precisar melhorar experiência do usuário, adicionar validação em tempo real, ou implementar Turbo/HTMX.
compatibility: PHP 8.2+, Laravel 11+
metadata:
  author: aronpc
  version: 1.0.0
  category: laravel
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# ux

## Resumo
Melhora UX com Precognition, Prompts interativos e HMR para Inertia.js.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `ui-ux` | Para identificar melhorias de UX |
| `i18n` | Para UX com traduções |
| `mcp` | Para validar UX visualmente |
| `testing` | Para testar flows de UX |

## Quando usar

Use esta skill sempre que:
- Implementar validação preemptiva com Precognition
- Criar Artisan commands interativos com Prompts
- Configurar HMR para Inertia.js
- Criar CLI user experience otimizada
- Melhorar feedback visual em forms
- Configurar Vite para desenvolvimento

## Laravel Precognition

### Instalação

```bash
composer require laravel/precognition
npm install laravel-precognition-react
```

### Configuração Backend

```php
<?php

// app/Http/Middleware/HandlePrecognition.php
namespace App\Http\Middleware;

use Illuminate\Http\Request;
use Laravel\Precognition\Concerns\HandlesPrecognition;

final class HandlePrecognition
{
    use HandlesPrecognition;

    public function handle(Request $request, Closure $next)
    {
        if ($this->isPrecognitionRequest($request)) {
            $request->setPrecognitive();
        }

        return $next($request);
    }
}
```

### Configurar Route

```php
<?php

// routes/web.php
use App\Http\Controllers\ProductController;

Route::middleware(['web', HandlePrecognition::class])
    ->group(function () {
        Route::post('/products', [ProductController::class, 'store']);
    });
```

### Frontend React

```typescript
// resources/js/components/ProductForm.tsx
import { precognition } from 'laravel-precognition-react';

interface ProductForm {
    name: string;
    price: number;
    category_id: number;
}

export function ProductForm() {
    const form = precognition<FormType>(
        '/products',
        'post',
        {
            name: '',
            price: 0,
            category_id: 0,
        }
    );

    return (
        <form onSubmit={form.submit}>
            <input
                type="text"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && (
                <span>{form.errors.name}</span>
            )}

            <input
                type="number"
                value={form.data.price}
                onChange={(e) => form.setData('price', parseFloat(e.target.value))}
                onBlur={() => form.validate('price')}
            />
            {form.invalid('price') && (
                <span>{form.errors.price}</span>
            )}

            <button type="submit" disabled={form.processing}>
                Save
            </button>
        </form>
    );
}
```

### Integração com Inertia

```typescript
// resources/js/pages/Products/Create.tsx
import { useForm } from '@inertiajs/react';
import { precognition } from 'laravel-precognition-react/inertia';

export default function CreateProduct() {
    const { data, setData, errors, processing, post } = precognition(
        useForm({
            name: '',
            price: 0,
            category_id: 0,
        })
    );

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        post('/products');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={data.name}
                onChange={(e) => setData('name', e.target.value)}
                onBlur={() => validate('name')}
            />
            {errors.name && <span className="error">{errors.name}</span>}

            <button type="submit" disabled={processing}>
                Save
            </button>
        </form>
    );
}
```

## Laravel Prompts

### Instalação

```bash
composer require laravel/prompts
```

### Command Básico

```bash
php artisan make:command ImportProducts
```

```php
<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Actions\Product\ImportProductsAction;
use Illuminate\Console\Command;
use Laravel\Prompts\Prompt;

final class ImportProducts extends Command
{
    protected $signature = 'products:import';

    protected $description = 'Import products from CSV';

    public function handle(): int
    {
        // Confirm
        if (! $this->confirm('Do you want to import products?')) {
            return Command::SUCCESS;
        }

        // Select
        $source = $this->choice(
            'Select import source',
            ['csv', 'api', 'xml'],
            'csv'
        );

        // Text input
        $file = $this->ask('Enter file path', 'products.csv');

        // Password/Secret
        $apiKey = $this->secret('Enter API key');

        // Search/Select
        $category = $this->anticipate(
            'Select category',
            ['Electronics', 'Clothing', 'Food'],
            'Electronics'
        );

        // Multi-select
        $fields = $this->choice(
            'Select fields to import',
            ['name', 'price', 'description', 'category'],
            multiple: true
        );

        // Progress bar
        $this->info('Importing products...');

        $products = $this->importFromFile($file);

        $progress = $this->output->createProgressBar($products->count());
        $progress->start();

        foreach ($products as $product) {
            ImportProductsAction::dispatch($product);
            $progress->advance();
        }

        $progress->finish();
        $this->newLine(2);

        $this->info("Successfully imported {$products->count()} products!");

        return Command::SUCCESS;
    }
}
```

### Prompts Avançados

```php
<?php

use Laravel\Prompts\{
    confirm,
    info,
    note,
    alert,
    warning,
    error,
    spin,
    table,
    search,
    multisearch,
    suggest,
    text,
    textarea,
    password,
    select,
    multiselect,
};

// Info/Warning/Error
info('Process started successfully');
note('Remember to backup your data');
warning('This action cannot be undone');
alert('Something went wrong');
error('Failed to process');

// Table
table(
    ['ID', 'Name', 'Price', 'Status'],
    [
        [1, 'Product 1', 'R$ 100,00', 'Active'],
        [2, 'Product 2', 'R$ 200,00', 'Inactive'],
        [3, 'Product 3', 'R$ 150,00', 'Active'],
    ]
);

// Search
$search = search(
    label: 'Search for a product',
    options: fn (string $value) => $this->searchProducts($value),
    placeholder: 'Type to search...',
);

// Multi-search
$categories = multisearch(
    label: 'Select categories',
    options: fn (string $value) => Category::where('name', 'like', "%{$value}%")
        ->pluck('name', 'id')
        ->toArray(),
);

// Suggest
$name = suggest(
    label: 'Product name',
    options: ['Product A', 'Product B', 'Product C'],
    placeholder: 'Start typing...',
);

// Spinner
$result = spin(
    fn () => $this->longRunningTask(),
    'Processing...'
);

// Textarea
$description = textarea(
    label: 'Product description',
    placeholder: 'Enter detailed description...',
    required: true,
    rows: 5,
);
```

## Laravel Turbo (HMR)

### Configurar Vite + Inertia HMR

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.ts'],
            refresh: true,
        }),
    ],
    server: {
        hmr: {
            host: 'localhost',
        },
    },
});
```

### Configuração React Fast Refresh

```bash
npm install @vitejs/plugin-react
```

```javascript
// vite.config.js
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        react(),
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.tsx'],
            refresh: true,
        }),
    ],
});
```

### Hot Module Replacement

```typescript
// resources/js/app.tsx
import { createInertiaApp } from '@inertiajs/react';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
    resolve: (name) =>
        resolvePageComponent(
            `./Pages/${name}.tsx`,
            import.meta.glob('./Pages/**/*.tsx')
        ),
    setup({ el, App }) {
        // HMR aceito por padrão
        createRoot(el).render(<App />);
    },
});
```

## Performance Tuning

### Vite Configurações

```javascript
// vite.config.js
export default defineConfig({
    build: {
        cssCodeSplit: true,
        sourcemap: true,
        rollupOptions: {
            output: {
                manualChunks: {
                    'vendor': ['react', 'react-dom', '@inertiajs/react'],
                    'filament': ['@filament/support'],
                },
            },
        },
    },
    optimizeDeps: {
        include: ['react', 'react-dom', '@inertiajs/react'],
    },
});
```

### Lazy Loading de Componentes

```typescript
// resources/js/components/LazyComponent.tsx
import { lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

export function Page() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <HeavyComponent />
        </Suspense>
    );
}
```

### Precognition com Throttle

```typescript
// Reduzir requests de validação
const form = precognition(
    '/products',
    'post',
    initialData,
    {
        throttle: 500, // esperar 500ms
    }
);
```

## Casos de Uso

### Form Multi-step com Precognition

```typescript
interface Step1Data { name: string; }
interface Step2Data { price: number; }
interface Step3Data { description: string; }

export function MultiStepForm() {
    const [step, setStep] = useState(1);
    const step1 = precognition<Step1Data>('/products/step1', 'post', {});
    const step2 = precognition<Step2Data>('/products/step2', 'post', {});
    const step3 = precognition<Step3Data>('/products/step3', 'post', {});

    const nextStep = async () => {
        const form = [step1, step2, step3][step - 1];
        await form.validate();
        if (form.valid) setStep(step + 1);
    };

    return (
        <form>
            {step === 1 && <Step1Form form={step1} onNext={nextStep} />}
            {step === 2 && <Step2Form form={step2} onNext={nextStep} />}
            {step === 3 && <Step3Form form={step3} onNext={handleSubmit} />}
        </form>
    );
}
```

### Command Interativo com Prompts

```php
<?php

final class SetupTenant extends Command
{
    protected $signature = 'tenant:setup';

    public function handle(): int
    {
        $this->info('Welcome to Tenant Setup!');

        // Step 1: Basic info
        $name = text('Tenant name', required: true);
        $email = text('Admin email', required: true)
            ->validate('email');

        // Step 2: Plan selection
        $plan = select(
            'Select plan',
            [
                'basic' => 'Basic - R$ 99/mês',
                'pro' => 'Pro - R$ 199/mês',
                'enterprise' => 'Enterprise - Custom',
            ]
        );

        // Step 3: Features
        $features = multiselect(
            'Select features',
            ['inventory', 'pos', 'reports', 'api'],
        );

        // Step 4: Confirm
        if (! $this->confirm("Create tenant '{$name}' with {$plan} plan?", true)) {
            return Command::FAILURE;
        }

        // Create tenant
        $progress = $this->output->createProgressBar(4);
        $progress->start();

        $progress->advance();
        $tenant = CreateTenantAction::run($name, $email, $plan, $features);

        $progress->advance();
        $this->run('db:seed', ['--class' => 'TenantSeeder']);

        $progress->advance();
        $this->run('storage:link');

        $progress->finish();
        $this->newLine();

        $this->info("Tenant {$name} created successfully!");
        table(
            ['Setting', 'Value'],
            [
                ['Tenant ID', $tenant->id],
                ['Name', $tenant->name],
                ['Plan', $tenant->plan->name],
                ['Login URL', route('tenant.login', $tenant->id)],
            ]
        );

        return Command::SUCCESS;
    }
}
```

## Melhores Práticas

### ✅ FAÇA

- Use Precognition para forms complexos
- Throttle requests de validação
    - Forneça feedback visual imediato
    - Use Prompts para commands interativos
    - Implemente progress bars para tarefas longas
    - Configure HMR para desenvolvimento
    - Lazy load componentes pesados
    - Teste UX em múltiplos dispositivos
    - Use table() para dados tabulares

### ❌ NÃO FAÇA

    - Não implemente validação duplicada
    - Não ignore feedback visual
    - Não crie commands sem feedback
    - Não use Prompts para automação (sem interação)
    - Não esqueça de tratar erros
    - Não sobrecarregue o usuário com opções
    - Não use HMR em produção

## Checklist de UX

Antes de finalizar feature com UX:

- [ ] Precognition configurado para forms
- [ ] Throttle de validação implementado
- [ ] Feedback visual para todos estados
- [ ] Commands com Prompts criados
- [ ] Progress bars para tarefas longas
- [ ] HMR configurado e funcionando
- [ ] Lazy loading de componentes
- [ ] Tratamento de erros amigável
- [ ] Testes de UX realizados
- [ ] Acessibilidade verificada

## Referências Cruzadas

- **Validation**: Integrado com Form Requests de `laravel-architecture`
- **i18n**: Mensagens de `laravel-i18n` em Prompts e forms
- **Actions**: Commands usam Actions de `laravel-actions-events`
- **Testing**: Testar UX com `laravel-testing-pest`

## Referências

- [Laravel Precognition](https://laravel.com/docs/precognition) - Documentação oficial
- [Laravel Prompts](https://laravel.com/docs/prompts) - Documentação oficial
- [Vite HMR](https://vitejs.dev/guide/api-hmr.html) - API Hot Module Replacement
- [Inertia.js](https://inertiajs.com/) - Documentação Inertia
