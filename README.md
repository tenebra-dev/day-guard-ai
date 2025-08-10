# 🚀 Day Guard AI (Stack JS/TS – NestJS)

Seu assistente diário com MCP e IA generativa, agora planejado para uma stack JavaScript/TypeScript com NestJS.

![Badge](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Badge](https://img.shields.io/badge/Tech-NestJS%20%7C%20TypeScript%20%7C%20Prisma%20%7C%20Postgres-blue)

## 🔍 Visão Geral
O Day Guard AI combina Model Context Protocol (MCP) e IA generativa para organizar tarefas, enviar lembretes inteligentes e gerar resumos diários com base no contexto (localização, horário, histórico e humor). Esta versão descreve a migração/reescrita para Node.js/NestJS.

## 🛠️ Stack Técnica (proposta)
- Backend: NestJS (TypeScript)
- ORM: Prisma (migrations integradas) – DB: PostgreSQL (prod) / SQLite (dev opcional)
- Validação: class-validator + class-transformer
- Config: @nestjs/config
- Logging: nestjs-pino (pino)
- Documentação: @nestjs/swagger (OpenAPI)
- Jobs/Filas: BullMQ + Redis (para tarefas assíncronas)
- Scheduler: @nestjs/schedule (cron/interval/timeout)
- Autenticação (opcional): Passport + JWT (@nestjs/passport, @nestjs/jwt)
- Testes: Jest + Supertest
- Qualidade: ESLint + Prettier
- IA: openai, @google/generative-ai (Gemini), mistralai

## 🧱 Arquitetura sugerida (NestJS)
```
src/
  main.ts
  app.module.ts
  core/
    config/
      configuration.ts
      validation.ts
    logging/
      logger.module.ts
  prisma/
    schema.prisma
    prisma.module.ts
    prisma.service.ts
  modules/
    tasks/
      tasks.module.ts
      tasks.controller.ts
      tasks.service.ts
      tasks.repository.ts (opcional)
      dto/
        create-task.dto.ts
        update-task.dto.ts
        query-task.dto.ts
      entities/ (se usar TypeORM; com Prisma use mapeamentos)
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

test/
```

## 📚 Rotas (Tasks)
- GET `/api/v1/tasks` → lista com envelope `{ items, total, offset, limit }`
  - Query: `offset`, `limit`, `title`, `location`, `mood`, `sort_by`, `sort_dir`
- POST `/api/v1/tasks` → cria task
- GET `/api/v1/tasks/:id` → detalhe
- PUT `/api/v1/tasks/:id` → atualiza
- DELETE `/api/v1/tasks/:id` → remove

Exemplos (PowerShell/curl):
- Criar
  - `curl -X POST http://localhost:3000/api/v1/tasks -H "Content-Type: application/json" -d '{"title":"Comprar pão","location":"mercado","schedule":"18:00"}'`
- Listar com filtros e paginação
  - `curl "http://localhost:3000/api/v1/tasks?title=Comprar&offset=0&limit=10"`

## 📌 Pré-requisitos
- Node.js 18+ e pnpm (ou npm/yarn)
- Docker (opcional) para Postgres/Redis

## 🔧 Variáveis de Ambiente
Crie `.env` (base):
```
# App
PORT=3000
NODE_ENV=development

# Banco (Postgres recomendado)
DATABASE_URL=postgresql://user:password@localhost:5432/dayguard

# IA
OPENAI_API_KEY=...
GEMINI_API_KEY=...
MISTRAL_API_KEY=...

# Queue/Cache
REDIS_URL=redis://localhost:6379
```

## 🚀 Como Executar (NestJS)
1) Instale dependências:
   - `pnpm install` (ou `npm install`)
2) Banco de dados:
   - Com Docker: `docker compose up -d db redis` (compose deverá ter serviços `db` e `redis`)
   - Local: crie um Postgres e ajuste `DATABASE_URL`
3) Prisma:
   - `npx prisma migrate dev`
   - `npx prisma generate`
4) Dev server:
   - `pnpm start:dev` (Nest CLI – watch)
5) Acesse:
   - Health: http://localhost:3000/health
   - Swagger: http://localhost:3000/docs

## 🧪 Qualidade
- Lint: `pnpm lint`
- Format: `pnpm format`
- Testes: `pnpm test` | `pnpm test:e2e`

## 🐳 Docker
- Dev: `docker compose up --build`
- Produção (exemplo): multi-stage build do Nest + Postgres gerenciado + Redis gerenciado

## 🔐 Segurança (baseline)
- CORS configurado por ambiente
- Helmet
- Rate limiting (@nestjs/throttler)
- Validação com whitelist/forbidNonWhitelisted (class-validator)
- Logs estruturados (pino) + correlação de requisições

## 🧭 Roadmap curto
- Paridade de features com a versão Python
- Providers reais para IA e integrações (Calendar/Location)
- Jobs para lembretes e resumo diário (BullMQ + scheduler)
- Frontend Web (Next.js) e Mobile (React Native/Expo)
- CI (GitHub Actions)

## 📄 Licença
MIT
