# PRD – Sistema de Service Desk

---

## 1. Visão Geral
O sistema de Service Desk tem como objetivo gerenciar chamados de suporte técnico, permitindo o registro, acompanhamento e resolução de tickets. A aplicação possibilita a comunicação entre usuários e equipe de suporte por meio de mensagens associadas aos tickets.

---

## 2. Objetivos
* Registrar chamados de suporte.
* Permitir acompanhamento do status dos tickets.
* Organizar atendimentos por prioridade.
* Registrar histórico de interações.
* Controlar responsáveis pelos atendimentos.

---

## 3. Usuários do Sistema
* **Usuários:** Criadores dos chamados.
* **Clientes:** Associados aos chamados.
* **Responsáveis:** Analistas que realizam o atendimento.
* **Editores:** Usuários com permissão para atualizar tickets.

---

## 4. Funcionalidades

### 🎫 Gestão de Tickets
* Criar e atualizar ticket.
* Alterar status (pending, in_process, done, canceled).
* Definir prioridade (low, normal, high, urgent).
* Atribuir responsável e encerrar ticket.

### 💬 Mensagens
* Adicionar mensagens ao ticket.
* Registrar autor da mensagem.
* Marcar mensagens como internas (visíveis apenas para a equipe de suporte).

---

## 5. Arquitetura e Implementação

### 5.1 Tecnologias Utilizadas
* **Backend:** FastAPI
* **Banco de Dados:** SQL
* **ORM/Conexão:** SQLAlchemy
* **Servidor:** Uvicorn (Leve, rápido e compatível com FastAPI)

### 5.2 Implementação Inicial
Foi implementado um servidor FastAPI com:
* Configuração via ambiente.
* Conexão com banco de dados.
* Endpoint `/health` para verificação de status da aplicação e banco.

### 5.3 Fluxo de Funcionamento
1. **Cliente:** Envia requisição via API.
2. **Controller:** Recebe a rota e valida os dados.
3. **Service:** Aplica as regras de negócio.
4. **Repository:** Persiste as informações no banco de dados.
5. **Resposta:** Retorno do status ao cliente.

### 5.4 Relação com Requisitos
* **RF01:** `POST /tickets` (Abertura)
* **RF02:** `PATCH /tickets/{id}` (Atualização)
* **RF03:** `POST /tickets/{id}/close` (Fechamento)
* **RF04:** Histórico completo na tabela `ticket_messages`

---

### 5.5 Modelo de Dados (Schema)

#### 🎫 Tabela: `tickets`
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **id** | CHAR(36) | PK - Identificador único (UUID) |
| **title** | VARCHAR(255) | Título do chamado |
| **description** | TEXT | Descrição detalhada do problema |
| **status** | ENUM | pending, in_process, done, canceled |
| **priority** | ENUM | low, normal, high, urgent |
| **user_id** | CHAR(36) | Usuário que criou o ticket |
| **client_id** | CHAR(36) | Cliente associado ao ticket |
| **assigned_to** | CHAR(36) | Responsável pelo atendimento |
| **updated_by** | CHAR(36) | Quem realizou a última atualização |
| **category** | VARCHAR(100) | Categoria do chamado |
| **closed_at** | TIMESTAMP | Data de encerramento (NULL se aberto) |
| **created_at** | TIMESTAMP | Data de criação (Default: CURRENT_TIMESTAMP) |
| **updated_at** | TIMESTAMP | Última atualização (Auto-update) |

#### 💬 Tabela: `ticket_messages`
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **id** | CHAR(36) | PK - Identificador único (UUID) |
| **ticket_id** | CHAR(36) | FK - Relacionado a `tickets(id)` (NOT NULL) |
| **author_id** | CHAR(36) | Identificador do autor da mensagem |
| **message** | TEXT | Conteúdo da interação |
| **is_internal** | BOOLEAN | Indica se a mensagem é interna (privada) |
| **created_at** | TIMESTAMP | Data de criação (Default: CURRENT_TIMESTAMP) |
| **updated_at** | TIMESTAMP | Última atualização (Auto-update) |

> **Relacionamento:** `ticket_id` referencia `tickets(id)` com regra **ON DELETE CASCADE**.

---

## 6. Considerações Finais
O sistema foi estruturado utilizando boas práticas de desenvolvimento, com separação clara de responsabilidades entre as camadas de software. A arquitetura atual permite escalabilidade e facilita futuras integrações com novos módulos.