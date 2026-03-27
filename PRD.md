PRD — Service Desk Microservice

🎯 Objetivo
Centralizar a comunicação entre usuários e equipe de suporte dentro do ERP modular.

👤 User Stories
- Como usuário, quero abrir um ticket para resolver problemas.
- Como agente de suporte, quero responder tickets.
- Como gestor, quero acompanhar status e métricas.
- 
⚙️ Requisitos Funcionais
- Criar tickets
- Listar tickets
- Atualizar status
- Enviar mensagens
- Atribuir responsáveis
  
🚀 Requisitos Não Funcionais
- Escalabilidade
- Segurança com autenticação
- Alta disponibilidade
- Baixa latência
  
🗄️ Modelo de Dados
Tabela: tickets
Campos principais: id, title, description, status_id, priority_id, user_id, client_id

💬 Mensagens
Tabela: ticket_messages
Campos: id, ticket_id, author_id, message, is_internal

🔄 Fluxo da API
1. Usuário envia requisição
2. API valida autenticação
3. Cria ticket
4. Retorna resposta

✅ Definition of Done
- API funcional
- Testes realizados
- Documentação atualizada
- Deploy em ambiente de teste
