---
name: tailwind-expert
description: Estilização de interfaces com Tailwind CSS incluindo componentes responsivos, dark mode, customização de tema, e padrões de design system. Usar para criar layouts responsivos, estilizar componentes Laravel/Blade, implementar design systems, e converter designs em código Tailwind.
---

# Tailwind Expert

Skill para estilização com Tailwind CSS em projetos Laravel.

## Setup Laravel + Tailwind

```bash
# Instalar
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./resources/**/*.blade.php",
    "./resources/**/*.js",
    "./resources/**/*.vue",
  ],
  darkMode: 'class', // ou 'media'
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```css
/* resources/css/app.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Componentes Comuns

### Card

```html
<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
    <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Título do Card
        </h3>
        <p class="mt-2 text-gray-600 dark:text-gray-300">
            Descrição do card com conteúdo relevante.
        </p>
    </div>
    <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-100 dark:border-gray-600">
        <button class="text-blue-600 dark:text-blue-400 hover:underline">
            Ver mais
        </button>
    </div>
</div>
```

### Botões

```html
<!-- Primary -->
<button class="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg
               hover:bg-blue-700 focus:outline-none focus:ring-2 
               focus:ring-blue-500 focus:ring-offset-2 
               transition-colors duration-200
               disabled:opacity-50 disabled:cursor-not-allowed">
    Salvar
</button>

<!-- Secondary -->
<button class="px-4 py-2 bg-gray-200 text-gray-800 font-medium rounded-lg
               hover:bg-gray-300 focus:outline-none focus:ring-2 
               focus:ring-gray-500 focus:ring-offset-2 transition-colors">
    Cancelar
</button>

<!-- Danger -->
<button class="px-4 py-2 bg-red-600 text-white font-medium rounded-lg
               hover:bg-red-700 focus:outline-none focus:ring-2 
               focus:ring-red-500 focus:ring-offset-2 transition-colors">
    Excluir
</button>

<!-- Outline -->
<button class="px-4 py-2 border-2 border-blue-600 text-blue-600 font-medium 
               rounded-lg hover:bg-blue-50 focus:outline-none focus:ring-2 
               focus:ring-blue-500 focus:ring-offset-2 transition-colors">
    Outline
</button>

<!-- Icon Button -->
<button class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 
               rounded-full transition-colors">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
    </svg>
</button>
```

### Form Inputs

```html
<!-- Text Input -->
<div class="space-y-1">
    <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        Email
    </label>
    <input type="email" id="email" name="email"
           class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                  dark:bg-gray-700 dark:border-gray-600 dark:text-white
                  placeholder:text-gray-400"
           placeholder="seu@email.com">
    <p class="text-sm text-red-600">Mensagem de erro</p>
</div>

<!-- Select -->
<div class="space-y-1">
    <label for="status" class="block text-sm font-medium text-gray-700">
        Status
    </label>
    <select id="status" name="status"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                   bg-white">
        <option value="">Selecione...</option>
        <option value="active">Ativo</option>
        <option value="inactive">Inativo</option>
    </select>
</div>

<!-- Textarea -->
<textarea rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm
                 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                 resize-none"
          placeholder="Observações..."></textarea>

<!-- Checkbox -->
<label class="flex items-center space-x-2 cursor-pointer">
    <input type="checkbox" 
           class="w-4 h-4 text-blue-600 border-gray-300 rounded
                  focus:ring-blue-500 focus:ring-2">
    <span class="text-sm text-gray-700">Aceito os termos</span>
</label>
```

### Table

```html
<div class="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 
                           dark:text-gray-400 uppercase tracking-wider">
                    Cliente
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 
                           uppercase tracking-wider">
                    Valor
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 
                           uppercase tracking-wider">
                    Status
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 
                           uppercase tracking-wider">
                    Ações
                </th>
            </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
            <tr class="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">
                        João Silva
                    </div>
                    <div class="text-sm text-gray-500">joao@email.com</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    R$ 5.000,00
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 text-xs font-medium rounded-full
                                 bg-green-100 text-green-800">
                        Ativo
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm space-x-2">
                    <button class="text-blue-600 hover:text-blue-900">Editar</button>
                    <button class="text-red-600 hover:text-red-900">Excluir</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### Alert/Badge

```html
<!-- Success Alert -->
<div class="p-4 rounded-lg bg-green-50 border border-green-200">
    <div class="flex items-center">
        <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        <span class="text-green-800 font-medium">Operação realizada com sucesso!</span>
    </div>
</div>

<!-- Error Alert -->
<div class="p-4 rounded-lg bg-red-50 border border-red-200">
    <span class="text-red-800">Erro ao processar requisição.</span>
</div>

<!-- Badges -->
<span class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">Novo</span>
<span class="px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">Pendente</span>
<span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">Ativo</span>
<span class="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800">Cancelado</span>
```

### Modal

```html
<!-- Overlay -->
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <!-- Modal -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4
                transform transition-all">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Título do Modal
            </h3>
            <button class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        </div>
        <!-- Body -->
        <div class="p-4">
            <p class="text-gray-600 dark:text-gray-300">
                Conteúdo do modal aqui.
            </p>
        </div>
        <!-- Footer -->
        <div class="flex justify-end gap-2 p-4 border-t dark:border-gray-700">
            <button class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                Cancelar
            </button>
            <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Confirmar
            </button>
        </div>
    </div>
</div>
```

## Layout Responsivo

```html
<!-- Grid Responsivo -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    <!-- Cards -->
</div>

<!-- Sidebar Layout -->
<div class="flex min-h-screen">
    <!-- Sidebar (hidden on mobile) -->
    <aside class="hidden md:flex md:flex-col md:w-64 bg-gray-800">
        <!-- Nav items -->
    </aside>
    
    <!-- Main Content -->
    <main class="flex-1 p-6">
        <!-- Content -->
    </main>
</div>

<!-- Breakpoints Reference -->
<!-- sm: 640px | md: 768px | lg: 1024px | xl: 1280px | 2xl: 1536px -->
```

## Customização de Tema

```javascript
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        brand: '#FF5722',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
}
```

## Blade Components

```php
{{-- resources/views/components/button.blade.php --}}
@props([
    'variant' => 'primary',
    'size' => 'md',
])

@php
$variants = [
    'primary' => 'bg-blue-600 text-white hover:bg-blue-700',
    'secondary' => 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    'danger' => 'bg-red-600 text-white hover:bg-red-700',
];

$sizes = [
    'sm' => 'px-3 py-1.5 text-sm',
    'md' => 'px-4 py-2',
    'lg' => 'px-6 py-3 text-lg',
];
@endphp

<button {{ $attributes->merge([
    'class' => "rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 {$variants[$variant]} {$sizes[$size]}"
]) }}>
    {{ $slot }}
</button>

{{-- Uso --}}
<x-button variant="primary" size="lg">Salvar</x-button>
<x-button variant="danger">Excluir</x-button>
```
