# Documento de Requisitos do Produto (PRD) - Módulo de Gestão de Atendimentos

Versão: 1.0 | Data: 26 de Maio de 2026 | Proprietário: Gestor de Projetos - TCC

---

## Resumo Executivo

**Objetivo:** Implementar um módulo centralizado de gestão de atendimentos (Help Desk) com API RESTful para criação, atualização, encerramento e rastreamento de tickets de suporte.

**Problema:** Ausência de plataforma centralizada causa gargalos no atendimento, dificultando rastreamento de chamados e cumprimento de SLAs.

**Solução Entregue:** API RESTful com endpoints para CRUD de tickets, filtros avançados e auditoria completa.

---

## 1. Escopo Funcional

### Requisitos Implementados (v1.0)

| ID | Requisito | Endpoint | Status |
|----|-----------|----------|--------|
| RF01 | Abertura de Chamado | `POST /tickets` | ✅ Completo |
| RF02 | Atualização de Status | `PATCH /tickets/{id}` | ✅ Completo |
| RF03 | Encerramento de Chamado | `POST /tickets/{id}/close` | ✅ Completo |
| RF04 | Rastreabilidade e Histórico | `GET /tickets/{id}` | ✅ Completo |
| - | Listagem com Filtros | `GET /tickets` | ✅ Completo |

### Excluído de v1.0
- Base de Conhecimento (Knowledge Base) - adiado para v2.0
- Notificações em tempo real - adiado para v1.1
- Dashboards avançados - adiado para v1.1

---

## 2. Especificação da API

### Endpoints Implementados

#### POST /tickets
Cria um novo ticket de suporte.

**Request:**
```json
{
  "title": "Sistema lento ao gerar relatórios",
  "description": "A partir das 14h o sistema está muito lento...",
  "status": "pending",
  "priority": "high",
  "category": "Performance",
  "user_id": "uuid-reporter",
  "client_id": "uuid-cliente",
  "assigned_to": null
}
```

**Response:** 201 Created
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Sistema lento ao gerar relatórios",
  "description": "A partir das 14h...",
  "status": "pending",
  "priority": "high",
  "category": "Performance",
  "user_id": "uuid-reporter",
  "client_id": "uuid-cliente",
  "assigned_to": null,
  "created_at": "2026-05-26T10:00:00Z",
  "updated_at": "2026-05-26T10:00:00Z",
  "closed_at": null
}
```

#### GET /tickets
Lista tickets com suporte a paginação e filtros.

**Query Parameters:**
- `skip`: Offset para paginação (padrão: 0)
- `limit`: Limite de resultados (padrão: 50, máx: 100)
- `status`: Filtrar por status (pending, in_process, done, canceled)
- `priority`: Filtrar por prioridade (low, normal, high, urgent)
- `user_id`: Filtrar por criador
- `client_id`: Filtrar por cliente
- `category`: Filtrar por categoria

**Response:** 200 OK
```json
{
  "total": 150,
  "items": [
    {
      "id": "550e8400-...",
      "title": "Sistema lento...",
      "status": "in_process",
      "priority": "high",
      "created_at": "2026-05-26T10:00:00Z",
      "updated_at": "2026-05-26T14:30:00Z",
      "closed_at": null
    }
  ]
}
```

#### GET /tickets/{ticket_id}
Retorna detalhes completos de um ticket.

**Response:** 200 OK - Retorna objeto ticket completo

#### PATCH /tickets/{ticket_id}
Atualiza propriedades de um ticket.

**Request:**
```json
{
  "status": "in_process",
  "assigned_to": "uuid-analista",
  "priority": "urgent"
}
```

**Response:** 200 OK - Retorna ticket atualizado

#### POST /tickets/{ticket_id}/close
Encerra um ticket com resolução.

**Request:**
```json
{
  "description": "Problema resolvido após otimização de índices...",
  "updated_by": "uuid-analista"
}
```

**Response:** 200 OK - Retorna ticket com status='done' e closed_at preenchido

---

## 3. Modelo de Dados

### Tabela: tickets

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | VARCHAR(36) | UUID único do ticket |
| `title` | VARCHAR(255) | Título resumido |
| `description` | TEXT | Descrição detalhada |
| `status` | ENUM | pending, in_process, done, canceled |
| `priority` | ENUM | low, normal, high, urgent |
| `category` | VARCHAR(100) | Categoria do incidente |
| `user_id` | VARCHAR(36) FK | Quem criou o ticket |
| `client_id` | VARCHAR(36) FK | Cliente solicitante |
| `assigned_to` | VARCHAR(36) FK | Analista responsável |
| `updated_by` | VARCHAR(36) FK | Último atualizador |
| `created_at` | TIMESTAMP | Data/hora de criação (automático) |
| `updated_at` | TIMESTAMP | Data/hora última atualização (automático) |
| `closed_at` | TIMESTAMP | Data/hora de fechamento (automático ao status=done) |

### Tabela: ticket_messages (Future)
Registrará interações (mensagens internas e externas) entre analistas e clientes.

---

## 4. Stack Técnico

- **Framework:** FastAPI 0.115.0
- **ORM:** SQLModel 0.0.21
- **Banco de Dados:** MySQL 8.0+
- **Migrações:** Alembic 1.13.3
- **Validação:** Pydantic (via SQLModel)
- **Server:** Uvicorn 0.30.6
- **Python:** 3.10+

---

## 5. Fluxo de Estados

```
PENDING → IN_PROCESS → DONE
                    ↘
                      CANCELED
```

- **PENDING:** Ticket aberto, aguardando atribuição
- **IN_PROCESS:** Analista está trabalhando
- **DONE:** Ticket resolvido e fechado (closed_at preenchido automaticamente)
- **CANCELED:** Ticket cancelado sem resolução

---

## 6. Regras de Negócio

- ✅ Tickets criados com status padrão `pending`
- ✅ Transição de status é linear (sem regressão)
- ✅ `created_at`, `updated_at`, `closed_at` são preenchidos automaticamente
- ✅ Ticket em `in_process` deve ter `assigned_to` preenchido
- ✅ Apenas status `done` ou `canceled` encerram um ticket
- ✅ Não é permitido reabrir tickets fechados

---

## 7. Critérios de Aceitação

- ✅ Todos os 5 endpoints funcionando sem exceções
- ✅ Validação de schema sem erros não capturados
- ✅ Paginação e filtros retornam resultados corretos
- ✅ Timestamps preenchidos e atualizados automaticamente
- ✅ Integração com MySQL sem erros
- ✅ Documentação OpenAPI gerada automaticamente (GET /docs)

---

## 8. Estrutura do Projeto

```
app/
├── __init__.py
├── main.py                    # Criação da app FastAPI e registro de rotas
├── config/
│   ├── config.py             # Variáveis de configuração
│   └── database.py           # Sessão SQLModel
└── modules/
    └── tickets/
        ├── __init__.py
        ├── model.py          # SQLModel com Ticket e TicketMessage
        ├── schema.py         # Pydantic schemas (Request/Response)
        ├── repository.py     # Operações de BD (CRUD)
        └── routes.py         # Endpoints da API
```

---

## 9. Como Usar

### Instalação
```bash
pip install -r requirements.txt
```

### Executar Migrações
```bash
alembic upgrade head
```

### Iniciar Servidor
```bash
python -m app.main
```

Acesse documentação em: `http://localhost:8000/docs`

---

## 10. Fases

| Versão | Escopo | Data Estimada |
|--------|--------|---------------|
| v1.0 | API com 5 endpoints | 31/05/2026 |

---

**Versão:** 1.0 | **Data:** 26/05/2026 | **Status:** Em Desenvolvimento

