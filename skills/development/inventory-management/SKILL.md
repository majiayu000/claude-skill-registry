---
name: inventory-management
description: Garante o controle correto de estoque e movimentações no Easy Budget.
---

# Gestão de Estoque do Easy Budget

Esta skill define o padrão para controle de estoque, movimentações e alertas de inventário no sistema Easy Budget.

## Estrutura do Inventário

```
📦 Produtos e Estoque
├── Product (Modelo principal)
│   ├── ProductInventory (Estoque atual)
│   │   ├── quantity (quantidade atual)
│   │   ├── min_quantity (estoque mínimo)
│   │   └── max_quantity (estoque máximo)
│   └── InventoryMovements (Histórico de movimentações)
│       ├── type: 'in' | 'out'
│       ├── quantity (quantidade movimentada)
│       └── reason (motivo: venda, ajuste, transferência, etc.)
```

## Padrão de Service de Inventário

```php
<?php

declare(strict_types=1);

namespace App\Services\Domain;

use App\Models\Product;
use App\Models\ProductInventory;
use App\Models\InventoryMovement;
use App\Repositories\ProductInventoryRepository;
use App\Repositories\InventoryMovementRepository;
use App\Support\ServiceResult;
use Exception;
use Illuminate\Support\Facades\DB;

class InventoryService
{
    public function __construct(
        private ProductInventoryRepository $inventoryRepository,
        private InventoryMovementRepository $movementRepository
    ) {}

    /**
     * Inicializa o estoque de um produto.
     */
    public function initialize(Product $product, int $initialQuantity = 0): ServiceResult
    {
        try {
            // Verificar se já existe registro
            $existing = $this->inventoryRepository->findByProductId($product->id);
            if ($existing) {
                return ServiceResult::error('Inventário já inicializado para este produto.');
            }

            $inventory = $this->inventoryRepository->create([
                'tenant_id' => $product->tenant_id,
                'product_id' => $product->id,
                'quantity' => $initialQuantity,
                'min_quantity' => 0,
                'max_quantity' => null,
            ]);

            // Registrar movimento inicial se quantidade > 0
            if ($initialQuantity > 0) {
                $this->recordMovement(
                    $product,
                    'in',
                    $initialQuantity,
                    'Estoque inicial'
                );
            }

            return ServiceResult::success($inventory, 'Inventário inicializado com sucesso.');
        } catch (Exception $e) {
            return ServiceResult::error($e->getMessage());
        }
    }

    /**
     * Registra uma movimentação de estoque.
     */
    public function recordMovement(
        Product $product,
        string $type,
        int $quantity,
        ?string $reason = null
    ): ServiceResult {
        try {
            // Validar tipo
            if (!in_array($type, ['in', 'out'])) {
                return ServiceResult::error('Tipo de movimentação inválido.');
            }

            // Validar quantidade
            if ($quantity <= 0) {
                return ServiceResult::error('Quantidade deve ser maior que zero.');
            }

            return DB::transaction(function () use ($product, $type, $quantity, $reason) {
                // Criar registro de movimento
                $movement = $this->movementRepository->create([
                    'tenant_id' => $product->tenant_id,
                    'product_id' => $product->id,
                    'type' => $type,
                    'quantity' => $quantity,
                    'reason' => $reason,
                ]);

                // Atualizar quantidade
                $newQuantity = $this->calculateNewQuantity($product, $type, $quantity);
                $this->inventoryRepository->updateQuantity($product->id, $newQuantity);

                // Verificar alertas de estoque baixo
                $this->checkLowStockAlert($product, $newQuantity);

                return ServiceResult::success($movement, 'Movimentação registrada com sucesso.');
            });
        } catch (Exception $e) {
            return ServiceResult::error($e->getMessage());
        }
    }

    /**
     * Reserva produtos para um orçamento/serviço.
     */
    public function reserve(Product $product, int $quantity): ServiceResult
    {
        try {
            $inventory = $this->inventoryRepository->findByProductId($product->id);

            if (!$inventory) {
                return ServiceResult::error('Inventário não encontrado para este produto.');
            }

            if ($inventory->quantity < $quantity) {
                return ServiceResult::error(
                    "Estoque insuficiente. Disponível: {$inventory->quantity}, Solicitado: {$quantity}"
                );
            }

            // Atualizar quantidade (reserva)
            $newQuantity = $inventory->quantity - $quantity;
            $this->inventoryRepository->updateQuantity($product->id, $newQuantity);

            // Registrar movimento
            $this->recordMovement($product, 'out', $quantity, 'Reserva para orçamento');

            return ServiceResult::success(
                ['new_quantity' => $newQuantity],
                'Produtos reservados com sucesso.'
            );
        } catch (Exception $e) {
            return ServiceResult::error($e->getMessage());
        }
    }

    /**
     * Libera reserva de produtos.
     */
    public function releaseReservation(Product $product, int $quantity): ServiceResult
    {
        try {
            $inventory = $this->inventoryRepository->findByProductId($product->id);

            if (!$inventory) {
                return ServiceResult::error('Inventário não encontrado para este produto.');
            }

            $newQuantity = $inventory->quantity + $quantity;
            $this->inventoryRepository->updateQuantity($product->id, $newQuantity);

            $this->recordMovement($product, 'in', $quantity, 'Liberação de reserva');

            return ServiceResult::success(
                ['new_quantity' => $newQuantity],
                'Reserva liberada com sucesso.'
            );
        } catch (Exception $e) {
            return ServiceResult::error($e->getMessage());
        }
    }

    /**
     * Verifica alertas de estoque baixo.
     */
    protected function checkLowStockAlert(Product $product, int $currentQuantity): void
    {
        $inventory = $this->inventoryRepository->findByProductId($product->id);

        if ($inventory && $inventory->min_quantity > 0 && $currentQuantity <= $inventory->min_quantity) {
            // Log de alerta - em implementação futura pode enviar notificação
            \Log::warning('Estoque baixo detectado', [
                'product_id' => $product->id,
                'product_name' => $product->name,
                'current_quantity' => $currentQuantity,
                'min_quantity' => $inventory->min_quantity,
                'tenant_id' => $product->tenant_id,
            ]);
        }
    }

    /**
     * Calcula nova quantidade após movimentação.
     */
    protected function calculateNewQuantity(Product $product, string $type, int $quantity): int
    {
        $inventory = $this->inventoryRepository->findByProductId($product->id);
        $currentQuantity = $inventory?->quantity ?? 0;

        return $type === 'in'
            ? $currentQuantity + $quantity
            : $currentQuantity - $quantity;
    }
}
```

## Actions de Inventário

```php
<?php

declare(strict_types=1);

namespace App\Actions\Inventory;

use App\Models\Product;
use App\Services\Domain\InventoryService;
use App\Support\ServiceResult;

class ReserveProductStockAction
{
    public function __construct(private InventoryService $inventoryService) {}

    /**
     * Reserva estoque para uso em serviço.
     */
    public function reserve(Product $product, int $quantity): ServiceResult
    {
        return $this->inventoryService->reserve($product, $quantity);
    }
}
```

## Tipos de Movimentação

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `in` | Entrada de estoque | Compra, devolução, ajuste positivo |
| `out` | Saída de estoque | Venda, uso em serviço, perda, ajuste negativo |

## Regras de Negócio

1. **Validação de quantidade**: Sempre verifique se há estoque suficiente antes de remover
2. **Movimentações rastreáveis**: Toda mudança de quantidade deve ter um registro
3. **Alertas de estoque baixo**: Sistema deve logar quando atingir quantidade mínima
4. **Transações**: Use `DB::transaction()` para operações que afetam múltiplas tabelas
5. **Atomicidade**: Se uma operação falhar, o estoque não deve ser alterado
