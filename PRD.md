<<<<<<< HEAD
# Documento de Requisitos do Produto (PRD)

Versão: 0.1

Data: 26/03/2026

Proprietário do Produto: Squad 4 - Yuri Santos 183775

Resumo Executivo
-----------------
- Objetivo do projeto: entregar um microserviço de Service Desk focado na comunicação cliente ↔ SaaS.
- Problema / oportunidade: falta de um backend de tickets leve e documentado para devs consumidores de API.
- Visão de sucesso: API de tickets aceita e utilizada por times de desenvolvimento, com documentação clara em `/docs` (Swagger) e coleção Postman disponível.

---------------
1. Visão Geral
- Contexto do negócio: empresa precisa de canal estruturado para atendimento operacional e correção de incidentes no produto SaaS.
- Público-alvo e stakeholders principais: devs integradores, times de suporte técnico, PO do produto.

--------------------------------
2. Metas e Critérios de Sucesso
- Meta 1 (SMART): disponibilizar MVP da API em 4 semanas com endpoints de criação, leitura, atualização e envio de mensagens.
- Meta 2: documentação completa em FastAPI/Swagger e Postman até a mesma entrega.
- KPIs: tempo de criação de ticket (menos de 10s), taxa de sucesso das requisições (>= 97%)

---------
3. Escopo
- Incluído no MVP / Fase 1:
	- Endpoints CRUD de tickets (criar, consultar, atualizar status, fechar).
	- Endpoints de mensagem associada ao ticket (thread de conversa).
	- Banco de dados com tabelas `tickets` e `ticket_messages`, relação 1:N entre ticket e mensagens.
	- Documentação FastAPI/Swagger em `/docs` e coleção Postman.
- Excluído desta fase:
	- UI de atendimento (apenas API).
	- Regras de SLA complexas e métricas de tempo de resposta automatizado.
	- Integração com canais externos (email/chat) nesta etapa inicial.
- Premissas:
	- Infraestrutura de banco de dados já disponível.
	- Autenticação e autorização tratadas por gateway/separa camada (não entra no escopo técnico detalhado aqui).

------------
4. Personas
- Dev de integração: cria/consulta tickets via API e espera resposta rápida e contratos estáveis.
- Atendente de suporte: consulta tickets e envia mensagens, com histórico completo.


-------------------------------
5. Jornadas / Fluxos de Usuário
- Fluxo principal:
	1. Usuário (dev ou cliente do SaaS) acessa o portal/API e abre solicitação (ticket).
	2. O atendente do Service Desk recebe notificação de novo ticket e visualiza detalhes em lista de tickets abertos.
	3. Atendente atribui prioridade e, se aplicável, categoria (crítico, alto, normal) ao ticket.
	4. Atendente inicia conversa de atendimento no chat interno e envia a primeira resposta.
	5. Usuário acompanha conversa pelo histórico de mensagens e responde sempre que necessário.
	6. Atendente verifica continuamente novos tickets e atualiza status (em progresso, aguardando cliente, resolvido).
	7. Quando a solução é confirmada, atendente fecha ticket com status "fechado" e registra observações finais.

- Fluxos alternativos / exceções:
	- Se ticket não existe ao consultar ou atualizar, retorna erro de não encontrado.
	- Se status inválido for enviado, é retornado erro de validação.
	- Se o ticket fica muito tempo sem resposta, pode ser reaberto ou escalado (workflow extra fora do MVP).

-------------------------
6. Requisitos Funcionais
- RF-001 — CRUD de ticket
	- Descrição: permitir criar, listar, obter e atualizar tickets.
	- Critérios de aceitação: dado uma requisição válida, quando chamar POST/GET/PATCH, então retornará código 200/201 e recurso esperado.
- RF-002 — Mensagens em ticket
	- Descrição: criar e listar mensagens associadas a um ticket.
	- Critérios de aceitação: dado um ticket existente, quando enviar mensagem, então ela será persistida em `ticket_messages` e vinculada a `ticket_id`.
- RF-003 — Status do ticket
	- Descrição: atualizar status (aberto, em progresso, resolvido, fechado).
	- Critérios de aceitação: status válido aceita, valor inválido rejeitado com 400.
- RF-004 — Documentação de API
	- Descrição: fornecer Swagger `/docs` e coleção Postman exportável.
	- Critérios de aceitação: todos endpoints descritos e testados manualmente.

----------------------------
7. Requisitos Não Funcionais
- Performance: resposta de 1s para operações básicas em cenário típico.
- Segurança: obrigatoriedade de token no header (aplicação de gateway).
- Disponibilidade: target de 99.5% no ambiente de produção.
- Escalabilidade: serviço stateless, com suporte a múltiplas instâncias.
- Usabilidade: API clara, validações consistentes e mensagens de erro legíveis.

---------------------
8. Regras de Negócio
- RBN-001: Ticket pode ser criado sem mensagens iniciais; mensagens são opcionais e feitas posteriormente pelo usuário/atendente.
- RBN-002: Mensagens de ticket são obrigatoriamente 1:N (um ticket pode ter múltiplas mensagens, cada mensagem pertence a um único ticket).

----------------------------------
9. Critérios de Aceitação & Testes
- Critérios mínimos do done:
	- API funcionando com endpoints e DB básico.
	- Documentação em `/docs` e Postman disponível.

-----------------
11. Arquitetura e Implementação
11.1 Tecnologias Utilizadas

* **Backend:** FastAPI
* **Banco de Dados:** SQL
* **ORM/Conexão:** SQLAlchemy
* **Servidor:** Uvicorn (Leve, rápido e compatível com FastAPI)

-----------------
11.2 Implementação Inicial

Foi implementado um servidor FastAPI com:
* Configuração via ambiente.
* Conexão com banco de dados.
* Endpoint `/health` para verificação de status da aplicação e banco.

-----------------
11.3 Fluxo de Funcionamento
1. **Cliente:** Envia requisição via API.
2. **Controller:** Recebe a rota e valida os dados.
3. **Service:** Aplica as regras de negócio.
4. **Repository:** Persiste as informações no banco de dados.
5. **Resposta:** Retorno do status ao cliente.

-----------------
11.4 Relação com Requisitos
* **RF01:** `POST /tickets` (Abertura)
* **RF02:** `PATCH /tickets/{id}` (Atualização)
* **RF03:** `POST /tickets/{id}/close` (Fechamento)
* **RF04:** Histórico completo na tabela `ticket_messages`

-----------------
11.5 Modelo de Dados (Schema)

11.5.1 Tabela: `tickets`
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
---
11.5.2 Tabela: `ticket_messages`
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

-----------------
11. Dependências
- Sistemas externos: banco de dados relacional (MySQL). 
- Equipes: infra, Equipe Core Engine.
- Recursos: acesso a ambiente de staging e dados de teste.

------------------------
12. Riscos e Mitigações
- Risco 1: atraso na infraestrutura de banco — mitigação: usar ambiente de dev local e mock inicial.
- Risco 2: gaps na documentação — mitigação: revisão com devs consumidores e ajustes rápidos em Swagger/Postman.

-----------------------
13. Cronograma e Marcos
- Marco 1: definição de requisitos e arquitetura — semana 2.
- Marco 2: implementação do MVP e testes — semanas 4-6.
- Marco 3: entrega e validação — fim da sprint 7.

---------------------------------
14. Plano de Lançamento e Operação
- Lançamento: deploy em staging, validação, então produção.
- Métricas pós-lançamento: sucesso de requisição, histórico de alterações, número de tickets criados.

------------
15. Glossário
- Ticket: solicitação registrada de atendimento.
- Ticket message: entrada de conversa vinculada a um ticket.

--------
Apêndice
- Documentos relacionados: README do projeto, arquitetura.
- Anexos: modelo de entidade `tickets` e `ticket_messages`, roteiro de uso de Postman.

=======
# PRD – Plataforma de Atendimento (Service Desk)

## 1. Propósito

### 1.1 Objetivo

Construir uma plataforma eficiente para gerenciar solicitações de suporte, centralizando comunicação, organização e resolução de problemas em um único fluxo.

### 1.2 Visão

Mais do que registrar chamados, o objetivo é melhorar a experiência de atendimento tanto para o cliente quanto para a equipe.

---

## 2. Problema

### 2.1 Situação atual

* Chamados podem se perder ou ficar sem resposta
* Falta de histórico confiável
* Falta de clareza sobre responsabilidade
* Cliente sem visibilidade do status

### 2.2 Solução proposta

Organizar todas as interações em um sistema centralizado, trazendo transparência e controle.

---

## 3. Usuários

### 3.1 Perfis

* Usuário final: busca solução rápida e clara
* Suporte técnico: precisa de contexto e organização
* Gestor: precisa de visibilidade e métricas
* Desenvolvedor integrador: precisa de API simples e documentada

---

## 4. Funcionalidades

### 4.1 Núcleo

* Criação e edição de chamados
* Controle de status e prioridade
* Atribuição de responsáveis
* Sistema de mensagens por chamado

### 4.2 Funcionalidades adicionais

* Filtros e busca
* Ordenação por prioridade ou tempo
* Marcação de urgência
* Reabertura de chamados
* Uso de categorias ou tags

---

## 5. Diferenciais do Produto

### 5.1 Comunicação

* Separação entre mensagens internas e externas

### 5.2 Controle

* Histórico de alterações
* Registro de ações por usuário

### 5.3 Produtividade

* Templates de resposta
* Possibilidade futura de sugestões automáticas

### 5.4 Eficiência

* Identificação de chamados duplicados 

---

## 6. Experiência do Usuário

### 6.1 Usuário final

* Fluxo simples de abertura
* Feedback claro após criação
* Visualização fácil do status
* Histórico organizado

### 6.2 Equipe de suporte

* Lista organizada de chamados
* Destaque para prioridades
* Acesso rápido ao histórico
* Interface objetiva

### 6.3 Recomendação

Evitar complexidade inicial. Priorizar simplicidade e rapidez.

---

## 7. Escopo (MVP)

### 7.1 Incluído

* CRUD de chamados
* Sistema de mensagens
* Controle de status e prioridade
* API documentada

### 7.2 Opcional (se houver tempo)

* Filtros básicos
* Categorias
* Reabertura de chamados

### 7.3 Fora do escopo

* Interface gráfica completa
* Integrações externas
* Automação de SLA

---

## 8. Métricas

### 8.1 Operacionais

* Tempo médio de resposta
* Tempo médio de resolução

### 8.2 Produto

* Chamados por categoria
* Taxa de reabertura
* Volume de chamados

### 8.3 Objetivo

Permitir tomada de decisão baseada em dados.

---

## 9. Arquitetura (Visão Simplificada)

### 9.1 Princípios

* Separação em camadas
* API stateless
* Banco relacional
* Logs básicos

### 9.2 Recomendação

Evitar complexidade desnecessária no início.

---

## 10. Segurança

### 10.1 Controle de acesso

* Autenticação obrigatória
* Permissões por tipo de usuário

### 10.2 Proteção de dados

* Validação de entrada
* Isolamento de mensagens internas

---

## 11. Riscos

### 11.1 Técnicos

* Crescimento desorganizado
* Falta de padronização

### 11.2 Produto

* Baixa adoção
* Experiência ruim

### 11.3 Mitigação

* Definir padrões desde o início
* Priorizar UX simples

---

## 12. Decisões Estratégicas

### 12.1 Arquitetura

* API-first ou UI-first

### 12.2 Complexidade

* Definir limite claro do MVP

### 12.3 Modelagem

* Manter status e fluxos simples

---

## 13. Evolução Futura

### 13.1 Funcionalidades

* Dashboard de métricas
* Sistema de notificações
* Integrações externas

### 13.2 Automação

* SLA
* Escalonamento automático

### 13.3 Inteligência

* Uso de IA para triagem e resposta

---

## 14. Insight Final

### 14.1 Natureza do sistema

O sistema não é apenas um CRUD de tickets.

### 14.2 Componentes principais

* Comunicação
* Organização
* Prioridade
* Suporte à decisão

### 14.3 Fator de sucesso

Clareza no fluxo, boa experiência e organização dos dados.

---

## 15. Considerações Finais

O projeto deve começar simples, mas preparado para crescimento.

O diferencial está na usabilidade e organização, não na complexidade técnica.
>>>>>>> feature/PRD_pedro
