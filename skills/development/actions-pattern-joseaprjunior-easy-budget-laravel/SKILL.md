---
name: actions-pattern
description: Garante que novas Actions sigam o padrão de classes actions reutilizáveis do Easy Budget.
---

# Padrão de Actions do Easy Budget

Esta skill define o padrão arquitetural para criação de Actions no sistema Easy Budget. Actions são classes focadas em uma única responsabilidade de negócio, reutilizáveis e composáveis.

## Estrutura Padrão

```php
<?php

declare(strict_types=1);

namespace App\Actions\ModuleName;

use App\Support\ServiceResult;
use Exception;

class ActionName
{
    public function __construct(
        private DependencyA $dependencyA,
        private DependencyB $dependencyB
    ) {}

    /**
     * Descrição do que a action executa.
     */
    public function execute(ParamType $param): ServiceResult
    {
        try {
            // 1. Validações de pré-condição
            if (!$this->isValid($param)) {
                return ServiceResult::error('Mensagem de erro específica.');
            }

            // 2. Operações de banco em transação (se necessário)
            return DB::transaction(function () use ($param) {
                // Lógica de negócio
                $result = $this->performAction($param);

                // Registro de histórico (se aplicável)
                $this->logAction($param, $result);

                return ServiceResult::success($result, 'Mensagem de sucesso.');
            });
        } catch (Exception $e) {
            return ServiceResult::error($e->getMessage());
        }
    }

    private function isValid(ParamType $param): bool
    {
        // Lógica de validação
        return true;
    }

    private function performAction(ParamType $param): mixed
    {
        // Implementação da ação
        return $result;
    }

    private function logAction(ParamType $param, mixed $result): void
    {
        // Registro de histórico se o modelo suportar
        if (method_exists($param, 'actionHistory')) {
            $param->actionHistory()->create([
                'tenant_id' => tenant('id'),
                'action' => 'action_name',
                'description' => 'Descrição da ação realizada.',
                'user_id' => auth()->id(),
            ]);
        }
    }
}
```

## Regras de Composição

1. **Dependências via Constructor Injection**: Sempre injete dependências no construtor
2. **Método `execute` único**: Cada Action deve ter um único ponto de entrada
3. **ServiceResult obrigatório**: Sempre retorne `ServiceResult` para operações que podem falhar
4. **Transação de banco**: Use `DB::transaction()` para operações que modificam dados
5. **Tratamento de exceções**: Use try-catch e retorne erros via `ServiceResult::error()`
6. **Registro de histórico**: Use `actionHistory()` quando disponível

## Exemplo de Composição de Actions

```php
class ComplexBusinessAction
{
    public function __construct(
        private ActionA $actionA,
        private ActionB $actionB,
        private ActionC $actionC
    ) {}

    public function execute(Context $context): ServiceResult
    {
        // Compõe múltiplas actions em um fluxo de negócio
        $resultA = $this->actionA->execute($context);
        if ($resultA->isError()) {
            return $resultA;
        }

        return $this->actionB->execute($context);
    }
}
```

## Quando Criar uma Nova Action

- Quando a lógica de negócio é reutilizável em múltiplos controllers
- Quando o fluxo envolve múltiplas operações transacionais
- Quando há necessidade de composição com outras actions
- Quando a lógica é complexa o suficiente para justificar separação

## Quando NÃO Criar uma Action

- Operações simples de CRUD que podem ir direto no Service
- Lógica que só é usada em um único lugar
- Operações que são apenas wrapper de repository
