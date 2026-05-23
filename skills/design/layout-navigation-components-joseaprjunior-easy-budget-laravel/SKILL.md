---
name: layout-navigation-components
description: Componentes de UI para layout e navegação seguindo o padrão de components do Easy Budget.
---

# Componentes de UI para Layout e Navegação

Esta skill define os componentes Blade específicos para layout e navegação no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── layout/
│   ├── app.blade.php               # Layout principal do sistema
│   ├── admin.blade.php             # Layout para área administrativa
│   ├── auth.blade.php              # Layout para páginas de autenticação
│   ├── dashboard.blade.php         # Layout para dashboard
│   ├── sidebar.blade.php           # Barra lateral de navegação
│   ├── navbar.blade.php            # Barra de navegação superior
│   ├── breadcrumbs.blade.php       # Breadcrumb de navegação
│   ├── footer.blade.php            # Rodapé do sistema
│   ├── theme-switcher.blade.php    # Troca de tema
│   └── notifications.blade.php     # Sistema de notificações
└── ...
```

## 1. App Layout Component

Componente para layout principal do sistema.

### Uso Básico

```blade
<x-layout.app :title="$title" :sidebar="$sidebar" :navbar="$navbar" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título da página | Obrigatório |
| `sidebar` | `bool` | Exibir barra lateral | `true` |
| `navbar` | `bool` | Exibir barra superior | `true` |
| `theme` | `string` | Tema do sistema | `auto` |

### Estrutura

```blade
@props([
    'title',
    'sidebar' => true,
    'navbar' => true,
    'theme' => 'auto'
])

<!DOCTYPE html>
<html lang="pt-BR" data-theme="{{ $theme }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ $title }} - {{ tenant('name') ?? 'Easy Budget' }}</title>

    <!-- Favicon -->
    <link rel="icon" href="{{ asset('favicon.ico') }}" type="image/x-icon">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

    <!-- Scripts -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])

    <!-- Custom Styles -->
    @stack('styles')

    <!-- Meta Tags -->
    <meta name="description" content="Sistema de gestão empresarial completo">
    <meta name="keywords" content="gestão, orçamentos, faturas, clientes, estoque">
    <meta name="author" content="Easy Budget">

    <!-- Open Graph -->
    <meta property="og:title" content="{{ $title }}">
    <meta property="og:description" content="Sistema de gestão empresarial">
    <meta property="og:type" content="website">

    <!-- CSRF Token -->
    <script>
        window.Laravel = {
            csrfToken: '{{ csrf_token() }}',
            baseUrl: '{{ url('/') }}'
        };
    </script>
</head>
<body class="font-sans antialiased">
    <div class="min-h-screen bg-gray-100">
        @if($navbar)
            <x-layout.navbar />
        @endif

        <div class="flex">
            @if($sidebar)
                <x-layout.sidebar />
            @endif

            <main class="flex-1 overflow-x-hidden overflow-y-auto">
                <div class="container mx-auto px-6 py-8">
                    {{ $slot }}
                </div>
            </main>
        </div>
    </div>

    <!-- Flash Messages -->
    @if(session('success'))
        <div id="flash-message" class="fixed top-4 right-4 z-50" data-message="{{ session('success') }}" data-type="success"></div>
    @elseif(session('error'))
        <div id="flash-message" class="fixed top-4 right-4 z-50" data-message="{{ session('error') }}" data-type="error"></div>
    @endif

    <!-- Scripts -->
    @stack('scripts')

    <!-- Flash Message Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const flashMessage = document.getElementById('flash-message');
            if (flashMessage) {
                const message = flashMessage.getAttribute('data-message');
                const type = flashMessage.getAttribute('data-type');
                showFlashMessage(message, type);
            }
        });
    </script>
</body>
</html>
```

## 2. Admin Layout Component

Componente para layout da área administrativa.

### Uso Básico

```blade
<x-layout.admin :title="$title" :breadcrumbs="$breadcrumbs" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título da página | Obrigatório |
| `breadcrumbs` | `array` | Breadcrumb da página | `[]` |
| `sidebar` | `bool` | Exibir barra lateral | `true` |

### Estrutura

```blade
@props([
    'title',
    'breadcrumbs' => [],
    'sidebar' => true
])

<!DOCTYPE html>
<html lang="pt-BR" data-theme="admin">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ $title }} - Administração - {{ tenant('name') ?? 'Easy Budget' }}</title>

    <!-- Favicon -->
    <link rel="icon" href="{{ asset('favicon.ico') }}" type="image/x-icon">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

    <!-- Admin Styles -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">

    <!-- Custom Admin Styles -->
    <style>
        :root {
            --admin-bg: #f8f9fa;
            --admin-sidebar: #2c3e50;
            --admin-sidebar-active: #34495e;
            --admin-primary: #3498db;
            --admin-danger: #e74c3c;
            --admin-warning: #f39c12;
            --admin-success: #27ae60;
        }

        .admin-layout {
            min-height: 100vh;
            background-color: var(--admin-bg);
        }

        .admin-sidebar {
            background-color: var(--admin-sidebar);
            min-height: 100vh;
            border-right: 1px solid #dee2e6;
        }

        .admin-sidebar .nav-link {
            color: #bdc3c7;
            border-radius: 0;
            padding: 1rem 1.5rem;
            transition: all 0.3s ease;
        }

        .admin-sidebar .nav-link:hover {
            background-color: var(--admin-sidebar-active);
            color: #fff;
        }

        .admin-sidebar .nav-link.active {
            background-color: var(--admin-primary);
            color: #fff;
            border-left: 4px solid #fff;
        }

        .admin-header {
            background-color: #fff;
            border-bottom: 1px solid #dee2e6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .admin-content {
            padding: 2rem;
        }

        .admin-card {
            background: #fff;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .admin-stat-card {
            background: linear-gradient(135deg, var(--admin-primary), #2980b9);
            color: white;
            border: none;
        }

        .admin-stat-card .stat-value {
            font-size: 2rem;
            font-weight: bold;
        }

        .admin-stat-card .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>

    <!-- Scripts -->
    @stack('styles')
</head>
<body class="admin-layout">
    <!-- Header -->
    <header class="admin-header">
        <div class="container-fluid">
            <div class="row align-items-center">
                <div class="col-md-6">
                    <h1 class="h4 mb-0 text-dark">{{ $title }}</h1>
                </div>
                <div class="col-md-6 text-end">
                    <div class="dropdown">
                        <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            <i class="bi bi-person-circle me-2"></i>{{ auth()->user()->name }}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{{ route('profile.edit') }}"><i class="bi bi-person me-2"></i>Perfil</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <form method="POST" action="{{ route('logout') }}">
                                    @csrf
                                    <button type="submit" class="dropdown-item"><i class="bi bi-box-arrow-right me-2"></i>Sair</button>
                                </form>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <div class="container-fluid">
        <div class="row">
            @if($sidebar)
                <x-layout.sidebar />
            @endif

            <main class="col {{ $sidebar ? 'col-md-9' : 'col-md-12' }} ms-sm-auto px-md-4">
                <div class="admin-content">
                    <!-- Breadcrumb -->
                    @if(!empty($breadcrumbs))
                        <x-layout.breadcrumbs :breadcrumbs="$breadcrumbs" />
                    @endif

                    <!-- Content -->
                    {{ $slot }}
                </div>
            </main>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    @stack('scripts')
</body>
</html>
```

## 3. Auth Layout Component

Componente para layout de páginas de autenticação.

### Uso Básico

```blade
<x-layout.auth :title="$title" :showLogo="$showLogo" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título da página | Obrigatório |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |
| `background` | `string` | Imagem de fundo | `null` |

### Estrutura

```blade
@props([
    'title',
    'showLogo' => true,
    'background' => null
])

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ $title }} - {{ tenant('name') ?? 'Easy Budget' }}</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

    <!-- Styles -->
    <style>
        :root {
            --auth-bg: #f8f9fa;
            --auth-card: #ffffff;
            --auth-border: #e9ecef;
            --auth-primary: #0d6efd;
            --auth-text: #333333;
            --auth-muted: #6c757d;
        }

        body {
            background-color: var(--auth-bg);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }

        .auth-container {
            width: 100%;
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
        }

        .auth-card {
            background: var(--auth-card);
            border: 1px solid var(--auth-border);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }

        .auth-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--auth-primary), #6610f2);
        }

        .auth-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .auth-logo {
            margin-bottom: 1rem;
        }

        .auth-logo img {
            max-height: 60px;
        }

        .auth-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--auth-text);
            margin: 0;
        }

        .auth-subtitle {
            color: var(--auth-muted);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }

        .auth-form {
            margin-top: 2rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--auth-text);
            font-size: 0.875rem;
        }

        .form-control {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--auth-border);
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            background-color: #fff;
        }

        .form-control:focus {
            border-color: var(--auth-primary);
            box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
            outline: none;
        }

        .form-control.is-invalid {
            border-color: #dc3545;
        }

        .invalid-feedback {
            display: block;
            width: 100%;
            margin-top: 0.25rem;
            font-size: 0.875em;
            color: #dc3545;
        }

        .btn-auth {
            width: 100%;
            padding: 0.75rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-primary {
            background-color: var(--auth-primary);
            color: white;
        }

        .btn-primary:hover {
            background-color: #0b5ed7;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
        }

        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background-color: #5c636a;
            transform: translateY(-1px);
        }

        .auth-links {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.9rem;
            color: var(--auth-muted);
        }

        .auth-links a {
            color: var(--auth-primary);
            text-decoration: none;
            font-weight: 500;
        }

        .auth-links a:hover {
            text-decoration: underline;
        }

        .auth-footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: var(--auth-muted);
            border-top: 1px solid var(--auth-border);
            padding-top: 1.5rem;
        }

        /* Responsive */
        @media (max-width: 480px) {
            .auth-container {
                padding: 1rem;
            }

            .auth-card {
                padding: 1.5rem;
            }
        }
    </style>

    @stack('styles')
</head>
<body>
    <div class="auth-container">
        <div class="auth-card">
            <!-- Header -->
            <div class="auth-header">
                @if($showLogo && tenant('logo'))
                    <div class="auth-logo">
                        <img src="{{ asset('storage/' . tenant('logo')) }}" alt="{{ tenant('name') }}">
                    </div>
                @endif

                <h1 class="auth-title">{{ $title }}</h1>
                <p class="auth-subtitle">Bem-vindo ao {{ tenant('name') ?? 'Easy Budget' }}</p>
            </div>

            <!-- Content -->
            <div class="auth-form">
                {{ $slot }}
            </div>

            <!-- Footer -->
            <div class="auth-footer">
                <p>© {{ date('Y') }} {{ tenant('name') ?? 'Easy Budget' }}. Todos os direitos reservados.</p>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    @stack('scripts')
</body>
</html>
```

## 4. Dashboard Layout Component

Componente para layout de dashboard.

### Uso Básico

```blade
<x-layout.dashboard :title="$title" :stats="$stats" :charts="$charts" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do dashboard | Obrigatório |
| `stats` | `array` | Estatísticas do dashboard | `[]` |
| `charts` | `array` | Gráficos do dashboard | `[]` |
| `filters` | `bool` | Exibir filtros | `true` |

### Estrutura

```blade
@props([
    'title',
    'stats' => [],
    'charts' => [],
    'filters' => true
])

<x-layout.app :title="$title">
    <div class="dashboard-container">
        <!-- Header -->
        <div class="dashboard-header">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h1 class="h2 mb-0">{{ $title }}</h1>
                    <p class="text-muted mb-0">Visão geral do seu negócio</p>
                </div>

                @if($filters)
                    <div class="dashboard-filters">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-outline-primary btn-sm active" data-filter="today">Hoje</button>
                            <button type="button" class="btn btn-outline-primary btn-sm" data-filter="week">Semana</button>
                            <button type="button" class="btn btn-outline-primary btn-sm" data-filter="month">Mês</button>
                            <button type="button" class="btn btn-outline-primary btn-sm" data-filter="year">Ano</button>
                        </div>
                    </div>
                @endif
            </div>
        </div>

        <!-- Stats -->
        @if(!empty($stats))
            <div class="dashboard-stats">
                <div class="row g-4">
                    @foreach($stats as $stat)
                        <div class="col-md-3">
                            <div class="stat-card">
                                <div class="stat-icon {{ $stat['icon_color'] ?? 'bg-primary' }}">
                                    <i class="bi {{ $stat['icon'] }}"></i>
                                </div>
                                <div class="stat-content">
                                    <div class="stat-value">{{ $stat['value'] }}</div>
                                    <div class="stat-label">{{ $stat['label'] }}</div>
                                    @if(isset($stat['trend']))
                                        <div class="stat-trend {{ $stat['trend'] >= 0 ? 'trend-up' : 'trend-down' }}">
                                            <i class="bi {{ $stat['trend'] >= 0 ? 'bi-arrow-up' : 'bi-arrow-down' }}"></i>
                                            {{ abs($stat['trend']) }}%
                                        </div>
                                    @endif
                                </div>
                            </div>
                        </div>
                    @endforeach
                </div>
            </div>
        @endif

        <!-- Charts -->
        @if(!empty($charts))
            <div class="dashboard-charts">
                <div class="row g-4">
                    @foreach($charts as $chart)
                        <div class="col-md-6">
                            <div class="chart-card">
                                <div class="chart-header">
                                    <h5 class="mb-0">{{ $chart['title'] }}</h5>
                                </div>
                                <div class="chart-body">
                                    <canvas id="{{ $chart['id'] }}" width="400" height="200"></canvas>
                                </div>
                            </div>
                        </div>
                    @endforeach
                </div>
            </div>
        @endif

        <!-- Content -->
        <div class="dashboard-content">
            {{ $slot }}
        </div>
    </div>

    @push('scripts')
    <script>
        // Dashboard interactivity
        document.addEventListener('DOMContentLoaded', function() {
            const filterButtons = document.querySelectorAll('.dashboard-filters .btn');
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');

                    // Trigger filter change
                    const filter = this.getAttribute('data-filter');
                    applyDashboardFilter(filter);
                });
            });

            // Initialize charts
            @foreach($charts as $chart)
                initChart('{{ $chart['id'] }}', @json($chart['data']));
            @endforeach
        });

        function applyDashboardFilter(filter) {
            // Implement filter logic
            console.log('Applying filter:', filter);
        }

        function initChart(canvasId, data) {
            const ctx = document.getElementById(canvasId).getContext('2d');
            new Chart(ctx, {
                type: data.type || 'line',
                data: data,
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
        }
    </script>
    @endpush
</x-layout.app>
```

## 5. Sidebar Component

Componente para barra lateral de navegação.

### Uso Básico

```blade
<x-layout.sidebar :menu="$menu" :active="$active" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `menu` | `array` | Estrutura do menu | `[]` |
| `active` | `string` | Item ativo | `''` |
| `user` | `User` | Usuário logado | `null` |

### Estrutura

```blade
@props([
    'menu' => [],
    'active' => '',
    'user' => null
])

<aside class="sidebar" id="sidebar">
    <!-- Logo -->
    <div class="sidebar-header">
        <div class="sidebar-logo">
            @if(tenant('logo'))
                <img src="{{ asset('storage/' . tenant('logo')) }}" alt="{{ tenant('name') }}" class="logo-img">
            @else
                <div class="logo-text">{{ tenant('name') ?? 'Easy Budget' }}</div>
            @endif
        </div>
        <button class="sidebar-toggle" id="sidebarToggle">
            <i class="bi bi-list"></i>
        </button>
    </div>

    <!-- User Info -->
    @if($user)
        <div class="sidebar-user">
            <div class="user-avatar">
                @if($user->avatar)
                    <img src="{{ asset('storage/' . $user->avatar) }}" alt="{{ $user->name }}">
                @else
                    <div class="avatar-placeholder">{{ substr($user->name, 0, 2) }}</div>
                @endif
            </div>
            <div class="user-info">
                <div class="user-name">{{ $user->name }}</div>
                <div class="user-role">{{ $user->role ?? 'Usuário' }}</div>
            </div>
        </div>
    @endif

    <!-- Navigation -->
    <nav class="sidebar-nav">
        <ul class="nav flex-column">
            @foreach($menu as $item)
                @if(isset($item['divider']))
                    <li class="nav-divider">{{ $item['divider'] }}</li>
                @elseif(isset($item['header']))
                    <li class="nav-header">{{ $item['header'] }}</li>
                @else
                    <li class="nav-item">
                        @if(isset($item['children']))
                            <a class="nav-link nav-dropdown {{ in_array($active, $item['children']) ? 'active' : '' }}" href="#" data-bs-toggle="collapse" data-bs-target="#collapse-{{ Str::slug($item['label']) }}">
                                <i class="bi {{ $item['icon'] }}"></i>
                                <span>{{ $item['label'] }}</span>
                                <i class="bi bi-chevron-down dropdown-icon"></i>
                            </a>
                            <div class="collapse {{ in_array($active, $item['children']) ? 'show' : '' }}" id="collapse-{{ Str::slug($item['label']) }}">
                                <ul class="nav flex-column sub-menu">
                                    @foreach($item['children'] as $child)
                                        <li class="nav-item">
                                            <a class="nav-link {{ $active === $child ? 'active' : '' }}" href="{{ route($child) }}">
                                                <i class="bi bi-circle"></i>
                                                <span>{{ $item['labels'][$child] ?? $child }}</span>
                                            </a>
                                        </li>
                                    @endforeach
                                </ul>
                            </div>
                        @else
                            <a class="nav-link {{ $active === $item['route'] ? 'active' : '' }}" href="{{ route($item['route']) }}">
                                <i class="bi {{ $item['icon'] }}"></i>
                                <span>{{ $item['label'] }}</span>
                            </a>
                        @endif
                    </li>
                @endif
            @endforeach
        </ul>
    </nav>

    <!-- Footer -->
    <div class="sidebar-footer">
        <div class="sidebar-version">
            <small class="text-muted">Versão {{ config('app.version', '1.0.0') }}</small>
        </div>
        <div class="sidebar-actions">
            <a href="{{ route('profile.edit') }}" class="sidebar-action" title="Perfil">
                <i class="bi bi-person"></i>
            </a>
            <a href="{{ route('settings.index') }}" class="sidebar-action" title="Configurações">
                <i class="bi bi-gear"></i>
            </a>
            <form method="POST" action="{{ route('logout') }}" class="sidebar-action" title="Sair">
                @csrf
                <button type="submit" class="btn-sidebar-action">
                    <i class="bi bi-box-arrow-right"></i>
                </button>
            </form>
        </div>
    </div>
</aside>

@push('styles')
<style>
    .sidebar {
        width: 250px;
        background-color: #fff;
        border-right: 1px solid #e9ecef;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        transition: transform 0.3s ease;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }

    .sidebar-header {
        padding: 20px;
        border-bottom: 1px solid #e9ecef;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .logo-img {
        max-height: 40px;
        width: auto;
    }

    .logo-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #0d6efd;
    }

    .sidebar-toggle {
        display: none;
        background: none;
        border: none;
        font-size: 1.2rem;
        color: #6c757d;
        cursor: pointer;
    }

    .sidebar-user {
        padding: 20px;
        border-bottom: 1px solid #e9ecef;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .user-avatar img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
    }

    .avatar-placeholder {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #0d6efd;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1rem;
    }

    .user-info {
        flex: 1;
    }

    .user-name {
        font-weight: 600;
        font-size: 1rem;
    }

    .user-role {
        font-size: 0.8rem;
        color: #6c757d;
    }

    .sidebar-nav {
        padding: 20px;
        flex: 1;
        overflow-y: auto;
    }

    .nav-link {
        color: #333;
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 5px;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }

    .nav-link:hover {
        background-color: #f8f9fa;
        color: #0d6efd;
    }

    .nav-link.active {
        background-color: #e7f1ff;
        color: #0d6efd;
        border-left: 4px solid #0d6efd;
    }

    .nav-link i {
        font-size: 1.1rem;
        width: 20px;
        text-align: center;
    }

    .nav-dropdown {
        position: relative;
    }

    .dropdown-icon {
        margin-left: auto;
        transition: transform 0.2s ease;
    }

    .nav-dropdown[aria-expanded="true"] .dropdown-icon {
        transform: rotate(180deg);
    }

    .sub-menu {
        padding-left: 30px;
    }

    .sub-menu .nav-link {
        padding: 8px 15px;
        font-size: 0.9rem;
        border-left: 2px solid transparent;
    }

    .sub-menu .nav-link.active {
        border-left-color: #0d6efd;
        background-color: transparent;
    }

    .nav-divider {
        padding: 10px 20px;
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #6c757d;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .nav-header {
        padding: 15px 20px;
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 600;
        border-bottom: 1px solid #e9ecef;
    }

    .sidebar-footer {
        padding: 20px;
        border-top: 1px solid #e9ecef;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .sidebar-actions {
        display: flex;
        gap: 10px;
    }

    .sidebar-action {
        background: none;
        border: none;
        color: #6c757d;
        cursor: pointer;
        padding: 8px;
        border-radius: 6px;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }

    .sidebar-action:hover {
        background-color: #f8f9fa;
        color: #0d6efd;
    }

    .btn-sidebar-action {
        background: none;
        border: none;
        color: #6c757d;
        cursor: pointer;
        padding: 8px;
        border-radius: 6px;
        transition: all 0.2s ease;
        width: 100%;
        text-align: left;
    }

    .btn-sidebar-action:hover {
        background-color: #f8f9fa;
        color: #0d6efd;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .sidebar {
            transform: translateX(-100%);
        }

        .sidebar.show {
            transform: translateX(0);
        }

        .sidebar-toggle {
            display: block;
        }

        main {
            margin-left: 0 !important;
        }
    }
</style>
@endpush

@push('scripts')
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');

        // Toggle sidebar
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('show');
            });
        }

        // Close sidebar on mobile when clicking outside
        document.addEventListener('click', function(event) {
            if (window.innerWidth <= 768) {
                const isClickInsideSidebar = sidebar.contains(event.target);
                const isClickOnToggle = sidebarToggle.contains(event.target);

                if (!isClickInsideSidebar && !isClickOnToggle) {
                    sidebar.classList.remove('show');
                }
            }
        });

        // Handle dropdowns
        const dropdowns = document.querySelectorAll('.nav-dropdown');
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', function(e) {
                e.preventDefault();
                const target = this.getAttribute('data-bs-target');
                const collapse = document.querySelector(target);

                if (collapse) {
                    const isExpanded = collapse.classList.contains('show');

                    // Close all other dropdowns
                    document.querySelectorAll('.sub-menu.show').forEach(other => {
                        if (other !== collapse) {
                            other.classList.remove('show');
                        }
                    });

                    // Toggle current dropdown
                    if (isExpanded) {
                        collapse.classList.remove('show');
                    } else {
                        collapse.classList.add('show');
                    }
                }
            });
        });
    });
</script>
@endpush
```

## 6. Navbar Component

Componente para barra de navegação superior.

### Uso Básico

```blade
<x-layout.navbar :user="$user" :notifications="$notifications" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `user` | `User` | Usuário logado | Obrigatório |
| `notifications` | `array` | Notificações | `[]` |
| `search` | `bool` | Exibir campo de busca | `true` |

### Estrutura

```blade
@props([
    'user',
    'notifications' => [],
    'search' => true
])

<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
    <div class="container-fluid">
        <!-- Brand -->
        <a class="navbar-brand d-flex align-items-center" href="{{ route('dashboard') }}">
            @if(tenant('logo'))
                <img src="{{ asset('storage/' . tenant('logo')) }}" alt="{{ tenant('name') }}" class="brand-logo">
            @else
                <span class="brand-text">{{ tenant('name') ?? 'Easy Budget' }}</span>
            @endif
        </a>

        <!-- Toggler -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
            <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Content -->
        <div class="collapse navbar-collapse" id="navbarContent">
            <!-- Search -->
            @if($search)
                <form class="d-flex me-auto" style="max-width: 400px;">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Buscar..." aria-label="Buscar">
                        <button class="btn btn-outline-secondary" type="button">
                            <i class="bi bi-search"></i>
                        </button>
                    </div>
                </form>
            @endif

            <!-- Right Menu -->
            <ul class="navbar-nav ms-auto align-items-center">
                <!-- Notifications -->
                <li class="nav-item dropdown me-3">
                    <a class="nav-link position-relative" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="bi bi-bell fs-5"></i>
                        @if(count($notifications) > 0)
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                {{ count($notifications) }}
                            </span>
                        @endif
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><h6 class="dropdown-header">Notificações</h6></li>
                        @forelse($notifications as $notification)
                            <li>
                                <a class="dropdown-item" href="{{ $notification['url'] }}">
                                    <div class="d-flex w-100 justify-content-between">
                                        <div>
                                            <strong>{{ $notification['title'] }}</strong>
                                            <div class="small text-muted">{{ $notification['message'] }}</div>
                                        </div>
                                        <small class="text-muted">{{ $notification['time'] }}</small>
                                    </div>
                                </a>
                            </li>
                        @empty
                            <li><span class="dropdown-item text-muted">Nenhuma notificação</span></li>
                        @endforelse
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item text-primary" href="{{ route('notifications.index') }}">Ver todas</a></li>
                    </ul>
                </li>

                <!-- User Menu -->
                <li class="nav-item dropdown">
                    <a class="nav-link d-flex align-items-center" href="#" role="button" data-bs-toggle="dropdown">
                        @if($user->avatar)
                            <img src="{{ asset('storage/' . $user->avatar) }}" alt="{{ $user->name }}" class="rounded-circle me-2" style="width: 32px; height: 32px; object-fit: cover;">
                        @else
                            <div class="avatar-circle me-2">{{ substr($user->name, 0, 2) }}</div>
                        @endif
                        <span class="d-none d-md-inline">{{ $user->name }}</span>
                        <i class="bi bi-chevron-down ms-1"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="{{ route('profile.edit') }}"><i class="bi bi-person me-2"></i>Perfil</a></li>
                        <li><a class="dropdown-item" href="{{ route('settings.index') }}"><i class="bi bi-gear me-2"></i>Configurações</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <form method="POST" action="{{ route('logout') }}">
                                @csrf
                                <button type="submit" class="dropdown-item"><i class="bi bi-box-arrow-right me-2"></i>Sair</button>
                            </form>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>

@push('styles')
<style>
    .navbar {
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .brand-logo {
        max-height: 30px;
        margin-right: 10px;
    }

    .brand-text {
        font-weight: bold;
        color: #0d6efd;
        font-size: 1.2rem;
    }

    .avatar-circle {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #0d6efd;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
    }

    .navbar-nav .nav-link {
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    }

    .navbar-nav .nav-link:hover {
        background-color: #f8f9fa;
        color: #0d6efd;
    }

    .dropdown-menu {
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .dropdown-item {
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }

    .dropdown-item:hover {
        background-color: #f8f9fa;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .brand-text {
            display: none;
        }

        .navbar-nav {
            margin-top: 1rem;
        }

        .navbar-nav .nav-link {
            padding: 0.75rem 1rem;
        }
    }
</style>
@endpush
```

## 7. Breadcrumbs Component

Componente para breadcrumb de navegação.

### Uso Básico

```blade
<x-layout.breadcrumbs :breadcrumbs="$breadcrumbs" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `breadcrumbs` | `array` | Estrutura do breadcrumb | Obrigatório |

### Estrutura

```blade
@props(['breadcrumbs'])

@if(!empty($breadcrumbs))
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            @foreach($breadcrumbs as $breadcrumb)
                @if($loop->last)
                    <li class="breadcrumb-item active" aria-current="page">
                        @if(isset($breadcrumb['icon']))
                            <i class="bi {{ $breadcrumb['icon'] }} me-2"></i>
                        @endif
                        {{ $breadcrumb['label'] }}
                    </li>
                @else
                    <li class="breadcrumb-item">
                        <a href="{{ $breadcrumb['url'] }}">
                            @if(isset($breadcrumb['icon']))
                                <i class="bi {{ $breadcrumb['icon'] }} me-2"></i>
                            @endif
                            {{ $breadcrumb['label'] }}
                        </a>
                    </li>
                @endif
            @endforeach
        </ol>
    </nav>
@endif

@push('styles')
<style>
    .breadcrumb {
        background-color: transparent;
        padding: 0;
        margin-bottom: 1.5rem;
        border-radius: 0;
    }

    .breadcrumb-item {
        font-size: 0.9rem;
        color: #6c757d;
    }

    .breadcrumb-item a {
        color: #0d6efd;
        text-decoration: none;
        transition: color 0.2s ease;
    }

    .breadcrumb-item a:hover {
        color: #0b5ed7;
        text-decoration: underline;
    }

    .breadcrumb-item.active {
        color: #333;
        font-weight: 500;
    }

    .breadcrumb-item + .breadcrumb-item::before {
        color: #6c757d;
    }
</style>
@endpush
```

## 8. Footer Component

Componente para rodapé do sistema.

### Uso Básico

```blade
<x-layout.footer :links="$links" :social="$social" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `links` | `array` | Links do rodapé | `[]` |
| `social` | `array` | Links sociais | `[]` |
| `showCopyright` | `bool` | Exibir copyright | `true` |

### Estrutura

```blade
@props([
    'links' => [],
    'social' => [],
    'showCopyright' => true
])

<footer class="footer bg-light border-top">
    <div class="container">
        <div class="row">
            <!-- Company Info -->
            <div class="col-md-4 mb-3 mb-md-0">
                <div class="footer-logo">
                    @if(tenant('logo'))
                        <img src="{{ asset('storage/' . tenant('logo')) }}" alt="{{ tenant('name') }}" class="footer-logo-img">
                    @else
                        <h5 class="footer-title">{{ tenant('name') ?? 'Easy Budget' }}</h5>
                    @endif
                </div>
                <p class="footer-description text-muted">
                    {{ tenant('description') ?? 'Sua solução de gestão empresarial completa.' }}
                </p>
            </div>

            <!-- Quick Links -->
            @if(!empty($links))
                <div class="col-md-2 mb-3 mb-md-0">
                    <h6 class="footer-heading">Links Rápidos</h6>
                    <ul class="list-unstyled">
                        @foreach($links as $link)
                            <li><a href="{{ $link['url'] }}" class="footer-link">{{ $link['label'] }}</a></li>
                        @endforeach
                    </ul>
                </div>
            @endif

            <!-- Support -->
            <div class="col-md-3 mb-3 mb-md-0">
                <h6 class="footer-heading">Suporte</h6>
                <ul class="list-unstyled">
                    <li><a href="{{ route('support.create') }}" class="footer-link">Centro de Ajuda</a></li>
                    <li><a href="{{ route('docs.index') }}" class="footer-link">Documentação</a></li>
                    <li><a href="{{ route('contact.index') }}" class="footer-link">Contato</a></li>
                </ul>
            </div>

            <!-- Social -->
            @if(!empty($social))
                <div class="col-md-3">
                    <h6 class="footer-heading">Siga-nos</h6>
                    <div class="social-links">
                        @foreach($social as $socialLink)
                            <a href="{{ $socialLink['url'] }}" class="social-link" target="_blank" rel="noopener noreferrer">
                                <i class="bi bi-{{ $socialLink['icon'] }}"></i>
                            </a>
                        @endforeach
                    </div>
                </div>
            @endif
        </div>

        <!-- Bottom Bar -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="footer-bottom">
                    @if($showCopyright)
                        <div class="copyright">
                            © {{ date('Y') }} {{ tenant('name') ?? 'Easy Budget' }}. Todos os direitos reservados.
                        </div>
                    @endif
                    <div class="footer-links">
                        <a href="{{ route('terms.index') }}" class="footer-link small">Termos de Uso</a>
                        <a href="{{ route('privacy.index') }}" class="footer-link small">Política de Privacidade</a>
                        <a href="{{ route('cookies.index') }}" class="footer-link small">Cookies</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</footer>

@push('styles')
<style>
    .footer {
        margin-top: auto;
    }

    .footer-logo-img {
        max-height: 40px;
        margin-bottom: 10px;
    }

    .footer-title {
        color: #0d6efd;
        margin-bottom: 10px;
    }

    .footer-description {
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .footer-heading {
        font-size: 1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
        position: relative;
        padding-bottom: 10px;
    }

    .footer-heading::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 2px;
        background-color: #0d6efd;
    }

    .footer-link {
        color: #6c757d;
        text-decoration: none;
        font-size: 0.9rem;
        transition: color 0.2s ease;
    }

    .footer-link:hover {
        color: #0d6efd;
        text-decoration: none;
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
        transition: all 0.2s ease;
    }

    .social-link:hover {
        background-color: #0b5ed7;
        transform: translateY(-1px);
    }

    .footer-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 20px;
        border-top: 1px solid #e9ecef;
        margin-top: 20px;
    }

    .copyright {
        font-size: 0.8rem;
        color: #6c757d;
    }

    .footer-links {
        display: flex;
        gap: 15px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .footer-bottom {
            flex-direction: column;
            gap: 10px;
            text-align: center;
        }

        .footer-links {
            justify-content: center;
        }
    }
</style>
@endpush
```

## 9. Theme Switcher Component

Componente para troca de tema.

### Uso Básico

```blade
<x-layout.theme-switcher :currentTheme="$currentTheme" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `currentTheme` | `string` | Tema atual | `auto` |
| `themes` | `array` | Temas disponíveis | `[]` |

### Estrutura

```blade
@props([
    'currentTheme' => 'auto',
    'themes' => [
        'auto' => ['name' => 'Automático', 'icon' => 'bi-circle-half'],
        'light' => ['name' => 'Claro', 'icon' => 'bi-sun'],
        'dark' => ['name' => 'Escuro', 'icon' => 'bi-moon']
    ]
])

<div class="theme-switcher" id="themeSwitcher">
    <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
        <i class="{{ $themes[$currentTheme]['icon'] }} me-2"></i>
        {{ $themes[$currentTheme]['name'] }}
    </button>
    <ul class="dropdown-menu">
        @foreach($themes as $key => $theme)
            <li>
                <button class="dropdown-item theme-option" type="button" data-theme="{{ $key }}">
                    <i class="{{ $theme['icon'] }} me-2"></i>
                    {{ $theme['name'] }}
                </button>
            </li>
        @endforeach
    </ul>
</div>

@push('styles')
<style>
    .theme-switcher {
        display: inline-block;
    }

    .theme-option {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        padding: 8px 16px;
        border: none;
        background: none;
        cursor: pointer;
        text-align: left;
        font-size: 0.9rem;
        color: #333;
        transition: all 0.2s ease;
    }

    .theme-option:hover {
        background-color: #f8f9fa;
        color: #0d6efd;
    }

    .theme-option.active {
        background-color: #e7f1ff;
        color: #0d6efd;
        font-weight: 500;
    }
</style>
@endpush

@push('scripts')
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const themeSwitcher = document.getElementById('themeSwitcher');
        const themeOptions = document.querySelectorAll('.theme-option');
        const currentTheme = localStorage.getItem('theme') || 'auto';

        // Apply initial theme
        applyTheme(currentTheme);

        // Handle theme changes
        themeOptions.forEach(option => {
            option.addEventListener('click', function() {
                const theme = this.getAttribute('data-theme');
                applyTheme(theme);
                localStorage.setItem('theme', theme);
            });
        });

        function applyTheme(theme) {
            // Update data-theme attribute
            document.documentElement.setAttribute('data-theme', theme);

            // Update button text and icon
            const button = themeSwitcher.querySelector('button');
            const icon = button.querySelector('i');
            const text = button.querySelector('span');

            // Update button content based on theme
            const themeData = getThemeData(theme);
            icon.className = themeData.icon + ' me-2';

            // Update dropdown items
            themeOptions.forEach(option => {
                option.classList.remove('active');
                if (option.getAttribute('data-theme') === theme) {
                    option.classList.add('active');
                }
            });

            // Dispatch theme change event
            window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
        }

        function getThemeData(theme) {
            const themes = @json($themes);
            return themes[theme] || themes.auto;
        }

        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
            if (currentTheme === 'auto') {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    });
</script>
@endpush
```

## 10. Notifications Component

Componente para sistema de notificações.

### Uso Básico

```blade
<x-layout.notifications :notifications="$notifications" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `notifications` | `array` | Notificações | `[]` |
| `maxVisible` | `int` | Máximo de notificações visíveis | `5` |

### Estrutura

```blade
@props([
    'notifications' => [],
    'maxVisible' => 5
])

<div class="notifications-container" id="notificationsContainer">
    @foreach($notifications as $notification)
        <div class="notification-item {{ $notification['type'] }}" data-id="{{ $notification['id'] }}">
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="bi {{ $notification['icon'] }}"></i>
                </div>
                <div class="notification-body">
                    <div class="notification-title">{{ $notification['title'] }}</div>
                    <div class="notification-message">{{ $notification['message'] }}</div>
                    <div class="notification-time">{{ $notification['time'] }}</div>
                </div>
                <button class="notification-close" type="button" data-id="{{ $notification['id'] }}">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    @endforeach
</div>

@push('styles')
<style>
    .notifications-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1050;
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 350px;
    }

    .notification-item {
        background: white;
        border: 1px solid #e9ecef;
        border-left: 4px solid;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    }

    .notification-item.show {
        transform: translateX(0);
    }

    .notification-item.success {
        border-left-color: #27ae60;
    }

    .notification-item.error {
        border-left-color: #e74c3c;
    }

    .notification-item.warning {
        border-left-color: #f39c12;
    }

    .notification-item.info {
        border-left-color: #3498db;
    }

    .notification-content {
        display: flex;
        gap: 12px;
        padding: 15px;
        position: relative;
    }

    .notification-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        color: white;
        flex-shrink: 0;
    }

    .notification-item.success .notification-icon {
        background-color: #27ae60;
    }

    .notification-item.error .notification-icon {
        background-color: #e74c3c;
    }

    .notification-item.warning .notification-icon {
        background-color: #f39c12;
    }

    .notification-item.info .notification-icon {
        background-color: #3498db;
    }

    .notification-body {
        flex: 1;
        min-width: 0;
    }

    .notification-title {
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 4px;
        color: #333;
    }

    .notification-message {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 8px;
        line-height: 1.4;
    }

    .notification-time {
        font-size: 0.75rem;
        color: #999;
    }

    .notification-close {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        color: #999;
        cursor: pointer;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }

    .notification-close:hover {
        background-color: #f8f9fa;
        color: #333;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .notification-item.removing {
        animation: slideOut 0.3s ease forwards;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .notifications-container {
            right: 15px;
            left: 15px;
            max-width: none;
        }

        .notification-item {
            max-width: none;
        }
    }
</style>
@endpush

@push('scripts')
<script>
    class NotificationManager {
        constructor() {
            this.container = document.getElementById('notificationsContainer');
            this.notifications = new Map();
        }

        show(notification) {
            const id = notification.id || Date.now();
            const element = this.createNotificationElement(notification, id);

            this.container.appendChild(element);
            this.notifications.set(id, element);

            // Auto-hide after 5 seconds
            setTimeout(() => {
                this.hide(id);
            }, 5000);

            return id;
        }

        hide(id) {
            const element = this.notifications.get(id);
            if (element) {
                element.classList.add('removing');
                setTimeout(() => {
                    element.remove();
                    this.notifications.delete(id);
                }, 300);
            }
        }

        createNotificationElement(notification, id) {
            const item = document.createElement('div');
            item.className = `notification-item ${notification.type || 'info'} show`;
            item.setAttribute('data-id', id);

            item.innerHTML = `
                <div class="notification-content">
                    <div class="notification-icon">
                        <i class="bi ${notification.icon || 'bi-info-circle'}"></i>
                    </div>
                    <div class="notification-body">
                        <div class="notification-title">${notification.title}</div>
                        <div class="notification-message">${notification.message}</div>
                        <div class="notification-time">${notification.time || new Date().toLocaleTimeString()}</div>
                    </div>
                    <button class="notification-close" type="button" data-id="${id}">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            `;

            // Add close button event
            const closeButton = item.querySelector('.notification-close');
            closeButton.addEventListener('click', () => {
                this.hide(id);
            });

            return item;
        }
    }

    // Initialize notification manager
    window.notificationManager = new NotificationManager();

    // Handle existing notifications
    document.addEventListener('DOMContentLoaded', function() {
        const notifications = @json($notifications);
        notifications.forEach(notification => {
            window.notificationManager.show(notification);
        });
    });

    // Global function to show notifications
    window.showNotification = function(notification) {
        if (window.notificationManager) {
            return window.notificationManager.show(notification);
        }
    };
</script>
@endpush
```

## 11. Integração com Padrões Existentes

### Uso em Views

```blade
{{-- Layout Principal --}}
<x-layout.app :title="'Dashboard - ' . tenant('name')">
    <x-layout.breadcrumbs :breadcrumbs="[
        ['label' => 'Dashboard', 'url' => route('dashboard')],
        ['label' => 'Visão Geral']
    ]" />

    <div class="dashboard-content">
        <!-- Conteúdo da página -->
    </div>
</x-layout.app>

{{-- Dashboard --}}
<x-layout.dashboard
    :title="'Visão Geral do Negócio'"
    :stats="$stats"
    :charts="$charts"
/>

{{-- Autenticação --}}
<x-layout.auth :title="'Login'">
    <form method="POST" action="{{ route('login') }}">
        @csrf
        <!-- Campos do formulário -->
    </form>
</x-layout.auth>
```

### Estilos CSS

```css
/* Layout Components Styles */
.sidebar {
    width: 250px;
    background-color: #fff;
    border-right: 1px solid #e9ecef;
}

.navbar {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.footer {
    margin-top: auto;
    background-color: #f8f9fa;
    border-top: 1px solid #e9ecef;
}

.notification-item {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
```

## 12. JavaScript Interatividade

### Sistema de Layout

```javascript
// layout-system.js
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Theme switcher
    const themeSwitcher = document.getElementById('themeSwitcher');
    if (themeSwitcher) {
        // Theme switching logic
    }

    // Responsive navigation
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('show');
        }
    });
});
```

## 13. Validação e Segurança

### Autorização

```php
// LayoutPolicy.php
public function viewSidebar(User $user)
{
    return $user->tenant_id === tenant('id');
}

public function viewNotifications(User $user)
{
    return $user->tenant_id === tenant('id');
}

public function changeTheme(User $user)
{
    return $user->can('manage-settings');
}
```

### Validations

```blade
{{-- Sidebar com validação de permissões --}}
@can('viewSidebar')
    <x-layout.sidebar :menu="$menu" :active="$active" />
@endcan

{{-- Theme Switcher com validação de permissões --}}
@can('changeTheme')
    <x-layout.theme-switcher :currentTheme="$currentTheme" />
@endcan
```

Este padrão de components para layout e navegação garante consistência visual, reutilização de código e manutenibilidade, seguindo os mesmos princípios estabelecidos nos outros components do sistema.
