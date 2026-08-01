---
name: nestjs-architect
description: Guia arquitetural para desenvolvimento NestJS com DDD, Clean Architecture
  e padrões avançados. Use quando codificar serviços, módulos, agregados, use cases
  ou refatorar código NestJS.
---

# NestJS Architect – Lite

**Uso:** tarefas rápidas de domínio/NestJS que cabem em uma única interação. Máx. 200 linhas; vá para `SKILL.md` para padrões avançados.

## ⚠️ PASSO 0: CARREGAR MÓDULOS OBRIGATÓRIOS (SEMPRE PRIMEIRO!)

**ANTES DE FAZER QUALQUER COISA, execute:**

```bash
# 🔴 OBRIGATÓRIOS: Carregar sempre no início
Read .claude/skills/nestjs-architect/sections/activation.md
Read .claude/skills/nestjs-architect/sections/architecture.md
Read .claude/skills/nestjs-architect/sections/aggregates.md
Read .claude/skills/nestjs-architect/sections/use-cases.md
Read .claude/skills/nestjs-architect/sections/repositories.md

# 🟡 SOB DEMANDA: Carregar se necessário
# - sections/testing.md (quando escrever testes)
# - sections/anti-patterns.md (quando revisar código)
# - sections/typescript-clean-code.md (quando otimizar TS)
# - sections/infra-observability.md (quando adicionar logs/métricas)
# - checklists/interactive-validation.md (validação final)
```

**Sem estes módulos obrigatórios, você NÃO tem informação suficiente para arquitetar com DDD/Clean Architecture.**

**Nota:** Caminhos são relativos à raiz do projeto (onde `.claude/` está localizado).

---

## 1) Regras de ativação

- Use somente se trabalhar com NestJS + DDD/Clean.
- **SEMPRE confirme início exibindo este disclaimer:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏗️ NESTJS ARCHITECT SKILL ATIVADA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Padrões: DDD, Clean Architecture, Repository Pattern
Notification Pattern, Domain Events
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 2) Estrutura mínima

```
src/
├─ core/
│  └─ <context>/
│     ├─ domain/            # entidades, aggregates, VOs, events, repos (interfaces)
│     ├─ application/       # use-cases, validations
│     └─ infra/             # repos impl (prisma/orm), mappers
└─ nest-modules/
   └─ <context>-module/     # controllers finos, providers, DTOs, presenters
```

- Domínio não importa `@nestjs/*` nem libs de infra.

## 3) Aggregate (template curto)

```ts
export class Order extends AggregateRoot {
  private constructor(
    readonly id: OrderId,
    private items: OrderItem[],
    private status: OrderStatus
  ) { super(id); }

  static create(props: CreateOrderProps): Order {
    const notification = new Notification();
    const order = new Order(props.id, props.items, OrderStatus.created());
    order.validate(notification);
    if (notification.hasErrors()) throw new EntityValidationError(notification.messages());
    order.apply(new OrderCreatedEvent(order.id));
    return order;
  }

  private validate(notification: Notification) {
    if (!this.items?.length) notification.addError('Order must have items');
  }
}
```

Checklist: construtor privado; fábrica `create`; valida com Notification Pattern; eventos aplicados; sem decorators NestJS; VOs imutáveis.

## 4) Use case (template curto)

```ts
export class CreateOrderUseCase implements IUseCase<Input, Output> {
  constructor(private repo: IOrderRepository) {}
  async execute(input: Input): Promise<Output> {
    const order = Order.create(mapToDomain(input));
    await this.repo.insert(order);
    return OrderPresenter.toOutput(order);
  }
}
```

Checklist: orquestra lógica; recebe repo via construtor; usa mapper para output; sem regras de negócio no controller.

## 5) Repository Pattern

- Interface no domínio: `IOrderRepository` com operações do agregado.
- Implementação na infra (Prisma/TypeORM/in-memory) usando mapper.
- Providers em `nest-modules/<context>-module/<context>.providers.ts`:

```ts
export const REPOSITORIES = {
  ORDER_REPOSITORY: {
    provide: 'IOrderRepository',
    useFactory: (prisma: PrismaService) => new OrderPrismaRepository(prisma),
    inject: [PrismaService]
  }
};
```

## 6) Controller fino

```ts
@Controller('orders')
export class OrderController {
  constructor(@Inject(CreateOrderUseCase) private createOrder: CreateOrderUseCase) {}
  @Post()
  async create(@Body() dto: CreateOrderDto) {
    return OrderPresenter.toHttp(await this.createOrder.execute(dto));
  }
}
```

## 7) DTOs e validação

- Use `class-validator`; um DTO por rota.
- Converta tipos primitivos para VOs no use case, não no controller.

## 8) Anti-patterns críticos

- Decorators NestJS no domínio.
- Value Objects mutáveis ou com setters públicos.
- Validação comentada ou lançando exception genérica.
- Controllers gordos com regra de negócio.
- Repos retornando modelos ORM diretamente ao domínio.

## 9) Testes mínimos

- Builders fake para aggregates/VOs.
- Testes de use case sem framework (mocks de repo).
- Integration test de controller usando módulo NestJS configurado.

## 10) Quick steps (para nova feature)

1. Criar dirs em `core/<context>/domain|application|infra` e `nest-modules/<context>-module`.
2. Escrever aggregate + VOs + events.
3. Interface de repo no domínio; impl prisma/in-memory.
4. Use case(s) chamando aggregate e repo.
5. Providers + controller + DTO + presenter.
6. Testes unitários (domínio e use case) e integração de controller.

## 11) Se precisar de mais

- Regras complexas → Specification Pattern (ver `SKILL.md`).
- Pipelines de validação → Chain of Responsibility (ver `SKILL.md`).
- Migrações grandes → Architecture Migrator Agent (se existir).

## 12) Referências rápidas

- Domínio puro: sem imports de framework.
- Aggregates aplicam eventos, não retornam `void` silencioso.
- Use case retorna DTO de saída via mapper/presenter.
- Providers agrupados em constantes (REPOSITORIES, USE_CASES, VALIDATIONS).

## 13) Recursos Modulares

### 🔴 Módulos OBRIGATÓRIOS (carregar sempre no PASSO 0):
- `sections/activation.md` → Gatilhos, persona, formato de saída
- `sections/architecture.md` → Estrutura completa de diretórios DDD/Clean
- `sections/aggregates.md` → Padrões avançados de aggregates
- `sections/use-cases.md` → Orquestração e patterns de use cases
- `sections/repositories.md` → Repository pattern com Prisma/TypeORM

### 🟡 Módulos SOB DEMANDA (carregar quando necessário):
- `sections/testing.md` → Builders fake, in-memory repos, testes E2E
- `sections/anti-patterns.md` → Lista completa de código para evitar
- `sections/typescript-clean-code.md` → Boas práticas TS avançadas
- `sections/infra-observability.md` → Logs estruturados, métricas, tracing
- `sections/nest-integration.md` → Módulos NestJS, guards, interceptors
- `checklists/interactive-validation.md` → Checklist de qualidade final

**Quando carregar módulos sob demanda:**
- Testing: quando implementar testes unitários/integração/E2E
- Anti-patterns: quando revisar código existente ou fazer code review
- TypeScript: quando otimizar tipos complexos ou generics
- Observability: quando adicionar logs estruturados ou métricas
- Integration: quando configurar guards, pipes, interceptors personalizados

## 14) Manutenção

- **Versão:** 2.0.0
- **Criado:** 2025-12-05
- **Atualizado:** 2025-12-12
  - v1.0.0: Versão inicial Lite com templates inline
  - v2.0.0: Adicionado carregamento obrigatório de módulos + disclaimer visível
- **Revisar quando:** NestJS atualizar versão major ou padrões DDD evoluírem
