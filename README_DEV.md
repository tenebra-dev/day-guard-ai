# Day Guard AI - Guia de Desenvolvimento (Migração para NestJS + TypeORM)

Este guia descreve a reescrita/migração da API de Python/FastAPI para uma stack TypeScript com NestJS, TypeORM e PostgreSQL. Mantemos paridade de funcionalidades (Tasks, filtros, paginação, integrações e schedulers) e evoluímos a base para web/mobile.

## Stack alvo
- Backend: NestJS 10+ (TypeScript)
- ORM: TypeORM 0.3+ (DataSource), DB: PostgreSQL (prod) / SQLite (dev opcional)
- Validação: class-validator + class-transformer
- Config: @nestjs/config (dotenv)
- Logs: nestjs-pino (pino)
- Swagger: @nestjs/swagger
- Jobs/Filas: BullMQ + Redis (opcional)
- Scheduler: @nestjs/schedule
- Testes: Jest + Supertest
- Segurança: helmet, @nestjs/throttler (rate-limit), CORS por ambiente

## Estratégia de migração
- Strangler pattern: subir NestJS em `/api/v2` e portar endpoints aos poucos, compartilhando o mesmo banco (ou migrando dados). Quando a paridade estiver ok, desativar a versão Python.
- Big bang é possível, porém menos seguro para produção.

## Estrutura proposta
```
src/
  main.ts
  app.module.ts
  core/
    config/
      configuration.ts        # Le .env + tipagem
      validation.ts           # Joi/Zod para validar env
    logging/
      logger.module.ts        # nestjs-pino
    database/
      data-source.ts          # TypeORM DataSource
      typeorm.config.ts       # Factory para @nestjs/typeorm
  modules/
    tasks/
      tasks.module.ts
      tasks.controller.ts
      tasks.service.ts
      tasks.repository.ts     # opcional (custom repo)
      dto/
        create-task.dto.ts
        update-task.dto.ts
        query-task.dto.ts
      entities/
        task.entity.ts
    integrations/
      calendar/
      location/
    ai/
      ai.module.ts
      providers/
        openai.provider.ts
        gemini.provider.ts
        mistral.provider.ts
  jobs/
    scheduler.module.ts
    scheduler.service.ts
migrations/
```

## Modelo de dados (Tasks)
- Tabela: `tasks`
- Campos: `id (uuid)`, `title (varchar)`, `location (varchar|null)`, `mood (varchar|null)`, `schedule (varchar|timestamptz|null)`, `created_at`, `updated_at`
- Índices recomendados: `title` (btree), `location`, `(created_at)`; futuramente FTS em Postgres para busca textual.

## Endpoints (paridade v1 → v2)
- GET `/api/v2/tasks` → `{ items, total, offset, limit }` com filtros `title`, `location`, `mood`, `sort_by`, `sort_dir`
- POST `/api/v2/tasks`
- GET `/api/v2/tasks/:id`
- PUT `/api/v2/tasks/:id`
- DELETE `/api/v2/tasks/:id`

## Variáveis de ambiente (.env)
```
# App
PORT=3000
NODE_ENV=development

# DB (Postgres)
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=dayguard
DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Redis (opcional)
REDIS_URL=redis://localhost:6379

# IA
OPENAI_API_KEY=...
GEMINI_API_KEY=...
MISTRAL_API_KEY=...
```

## Scripts (sugestão package.json)
- start:dev → `nest start --watch`
- build → `nest build`
- test → `jest`
- lint → `eslint .`
- format → `prettier --write .`
- typeorm CLI (TS):
  - `typeorm`: `ts-node -r tsconfig-paths/register node_modules/typeorm/cli.js -d src/core/database/data-source.ts`
  - `db:migrate`: `npm run typeorm -- migration:run`
  - `db:revert`: `npm run typeorm -- migration:revert`
  - `db:gen`: `npm run typeorm -- migration:generate ./migrations/<name>`

## Próximos passos (checklist)
1) Bootstrap do projeto NestJS
   - npx @nestjs/cli new backend (ou pasta `server/` no monorepo)
   - Adicionar libs: `@nestjs/typeorm typeorm pg @nestjs/config @nestjs/swagger swagger-ui-express class-validator class-transformer nestjs-pino @nestjs/schedule @nestjs/throttler helmet`
   - Dev: `ts-node tsconfig-paths @types/node eslint prettier`
2) Configuração
   - `core/config/configuration.ts` para mapear `.env`
   - `core/config/validation.ts` (Joi) para validar env (ports, DB_URL, etc.)
   - Habilitar ValidationPipe global (whitelist, forbidNonWhitelisted)
   - Pino logger e Helmet + Throttler
3) Banco e ORM
   - `core/database/data-source.ts` (TypeORM DataSource baseado em env)
   - `typeorm.config.ts` para `TypeOrmModule.forRootAsync`
   - Entidade `Task` e primeira migration `InitTasks`
   - Scripts de migração (run/revert/generate)
4) Módulo `tasks`
   - DTOs (create/update/query) com class-validator
   - Controller (rotas v2) e Service
   - Repositório com filtros/paginação/sorting seguros (whitelist de campos)
   - Swagger decorators nos DTOs e endpoints
   - Testes unitários (service) e e2e (controller com Supertest)
5) Scheduler / Jobs
   - `jobs/scheduler.module.ts` com exemplos de cron/interval
   - (Opcional) BullMQ + Redis para lembretes/notificações
6) IA Providers
   - Interfaces e providers para OpenAI/Gemini/Mistral com timeouts e retries
   - Configurar chaves via env e expor serviço `AIService`
7) Docker Compose (dev)
   - Serviços: `db` (Postgres), `redis` (opcional)
   - Rede e volumes nomeados; healthchecks
8) Observabilidade e Segurança
   - Logs estruturados com correlação
   - Rate limit por rota sensível
   - CORS por ambiente
   - (Opcional) OpenTelemetry
9) Integração Frontend
   - OpenAPI JSON em `/docs-json` para gerar cliente (openapi-typescript)
   - Preparar CORS para Next.js/Expo
10) CI (GitHub Actions)
    - Lint + Test + Migrations dry-run + Build docker

## Comandos úteis (PowerShell)
- Instalação deps (exemplo com pnpm): `pnpm add @nestjs/typeorm typeorm pg @nestjs/config @nestjs/swagger swagger-ui-express class-validator class-transformer nestjs-pino @nestjs/schedule @nestjs/throttler helmet`
- Dev server: `pnpm start:dev`
- Migrations:
  - Gerar: `pnpm typeorm migration:generate ./migrations/InitTasks -d ./src/core/database/data-source.ts`
  - Rodar: `pnpm typeorm migration:run -d ./src/core/database/data-source.ts`
  - Reverter: `pnpm typeorm migration:revert -d ./src/core/database/data-source.ts`

## Migração de dados (se necessário)
- Exportar do SQLite atual (Python) para CSV/SQL e importar no Postgres novo.
- Alternativa: escrever um script Nest que leia o SQLite com `better-sqlite3` e grave no Postgres via TypeORM (one-off).

## Limitações e cuidados
- TypeORM + TS requer configurar corretamente paths/ts-node para CLI de migrações.
- Pool de conexões: configure `max` e `idleTimeoutMillis` para evitar exaustão.
- Filtros/sorting: whitelists para prevenir SQL injection via ordenação dinâmica.
- Scheduler não é “tempo real”; use jobs idempotentes e monitore atrasos.
- Integrações Google podem exigir verificação e têm quotas; implemente retries/backoff.

## Estado anterior (Python)
- A API FastAPI continua disponível em `/api/v1` até concluirmos a paridade em `/api/v2` (NestJS).
- Alembic não será reutilizado; migrações passam a ser do TypeORM.
