---
name: module-scaffold
description: Scaffold a new NestJS domain module for PMTL_VN following project conventions. Creates the correct file structure with module, controller, service, repository, schemas, mapper, and policy files. Use when starting to implement a new domain module from the design.
disable-model-invocation: true
argument-hint: <module-name>
---

# Module Scaffold (Tạo khung Module NestJS)

Tạo đầy đủ file structure cho domain module **$ARGUMENTS** theo chuẩn PMTL_VN.

## Bước 1: Đọc design contracts

Trước khi tạo bất kỳ file nào, đọc:
1. `design/<module-number>-$ARGUMENTS/module-map.md` — hiểu objectives và boundaries
2. `design/<module-number>-$ARGUMENTS/contracts.md` — hiểu routes, input schemas, rules
3. `design/<module-number>-$ARGUMENTS/schema.dbml` — hiểu DB schema
4. `design/<module-number>-$ARGUMENTS/use-cases/` — đọc tất cả use-case files
5. `design/baseline/nest-baseline.md` — chuẩn NestJS của project
6. `design/01-identity/PERMISSION_MATRIX.md` — per-module permission scope cho module này

Nếu không tìm thấy module trong design/, hỏi lại tên chính xác trước khi tiếp tục.

## Bước 2: Xác nhận trước khi tạo

Tóm tắt cho user:
- Module này sở hữu collections nào
- Routes sẽ được tạo
- Permission scope cho từng role
- Dependencies vào module khác

Hỏi: "Xác nhận tạo scaffold cho module này không?"

## Bước 3: Tạo file structure

Target path: `apps/api/src/modules/$ARGUMENTS/`

### File structure cần tạo:

```
apps/api/src/modules/$ARGUMENTS/
├── $ARGUMENTS.module.ts          # NestJS module definition
├── $ARGUMENTS.controller.ts      # HTTP layer — thin, chỉ validate + delegate
├── $ARGUMENTS.service.ts         # Business logic
├── $ARGUMENTS.repository.ts      # Prisma queries — không có business logic
├── $ARGUMENTS.schemas.ts         # Zod schemas cho tất cả inputs
├── $ARGUMENTS.mapper.ts          # Entity → DTO mapping (không expose raw DB)
├── $ARGUMENTS.policy.ts          # Authorization rules (role + business rule)
└── dto/
    ├── create-$ARGUMENTS.dto.ts  # Response DTOs
    └── $ARGUMENTS-response.dto.ts
```

### Rules cho mỗi file:

**`$ARGUMENTS.module.ts`**
- Import PrismaModule, AuditModule, platform modules cần thiết
- Exports service nếu module khác cần đọc

**`$ARGUMENTS.controller.ts`**
- `@UseGuards(JwtAuthGuard, RolesGuard)` trên routes cần auth
- `@RateLimit(...)` trên auth/write/upload endpoints
- Chỉ validate input (dùng schema từ `.schemas.ts`) + gọi service
- Không có business logic trong controller
- Mỗi route return DTO đã mapped, không phải raw Prisma entity

**`$ARGUMENTS.service.ts`**
- Inject repository, auditService, feature flags
- Mọi write operation phải:
  1. Validate business invariants
  2. Execute canonical write (qua repository)
  3. `auditService.append(...)` với actor + action + entityId
  4. Return mapped DTO
- Side effects async (outbox phase 2+ / inline sync phase 1)

**`$ARGUMENTS.repository.ts`**
- Chỉ Prisma queries
- Không có business logic
- Trả về Prisma entity — mapping xảy ra ở service/mapper
- Tên method rõ ràng: `findByPublicId`, `createOne`, `updateStatus`, etc.

**`$ARGUMENTS.schemas.ts`**
- Zod schema cho **mọi** input: request body, query params, path params
- Export const theo tên: `CreateXxxSchema`, `UpdateXxxSchema`, `XxxQuerySchema`
- Không dùng `z.any()` hoặc `z.unknown()` trừ khi có lý do rõ

**`$ARGUMENTS.mapper.ts`**
- `toResponseDto(entity: PrismaEntity): XxxResponseDto`
- Không expose: password_hash, raw tokens, internal IDs, sensitive fields
- publicId thay cho id trong responses

**`$ARGUMENTS.policy.ts`**
- `canRead(actor: AuthUser, entity: Xxx): boolean`
- `canWrite(actor: AuthUser, entity?: Xxx): boolean`
- `canDelete(actor: AuthUser, entity: Xxx): boolean`
- Tách rõ: role check vs business rule vs deletion policy

## Bước 4: Thêm placeholder comments

Mỗi file phải có comment ở đầu:
```typescript
/**
 * @module $ARGUMENTS
 * @owner PMTL_VN $ARGUMENTS module
 * @ref design/<number>-$ARGUMENTS/contracts.md
 *
 * Canonical collections: [list từ module-map.md]
 * Does NOT own: [list từ module-map.md]
 */
```

## Bước 5: Tạo migration placeholder

Tạo file `prisma/migrations/PLACEHOLDER_$ARGUMENTS/README.md` với:
- Schema tables cần tạo (từ schema.dbml)
- Reminder: phải có migration thật trước khi implement

## Bước 6: Báo cáo kết quả

Liệt kê tất cả file đã tạo và:
- Những gì cần implement tiếp (business logic chưa có)
- Use-case files cần đọc trước khi code từng feature
- Audit events bắt buộc cho module này (từ tracking/audit-policy.md)

---

## Quan trọng

- **Không** tạo file nếu chưa đọc design contracts
- **Không** implement business logic thật — chỉ scaffold structure và comments
- **Không** bỏ qua `.schemas.ts` — mọi input phải có Zod schema
- **Không** để controller có business logic
- **Không** expose raw Prisma entity trong response — phải qua mapper
