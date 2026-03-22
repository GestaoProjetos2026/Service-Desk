# Commit Guidelines (.github)

Este arquivo tem como objetivo padronizar os commits no repositório Service-Desk.

## 1. Objetivo

- Garantir histórico limpo e compreensível
- Ajudar revisões e geração de changelog automatizado
- Facilitar comunicação entre equipe

## 2. Convenção recomendada (Conventional Commits)

Formato:

`<tipo>[escopo opcional]: descrição breve`

Corpo opcional:

- Explica o motivo
- Enumera alterações importantes
- URL de issue ou PR (se houver)

Exemplo:

`fix(auth): corrige token expirado para refresh automático`

### Tipos e quando usar

- `feat`: nova funcionalidade / melhoria visível
  - Quando adicionar um novo endpoint, UI, fluxo de negócio

- `fix`: correção de bug
  - Quando resolver defeito reportado ou falha de integração

- `docs`: alteração em documentação
  - README, comentários, help, guia de usuário

- `style`: formatação, lint, espaços, sem lógica alterada
  - Ajuste de formatação, ordem de imports, etc

- `refactor`: refatoração de código
  - Mudar estrutura ou legibilidade sem novo comportamento

- `perf`: otimização de performance
  - Reduzir tempo de resposta, uso de CPU/memória

- `test`: adicionar/ajustar testes
  - Testes unitários, integração ou e2e

- `chore`: manutenção de infra e configuração
  - Atualizar dependência, scripts, pipeline CI

- `build`: alterações no processo de build
  - Dockerfile, pipeline, scripts de compilação

- `ci`: mudanças em CI/CD sem alteração de código fonte
  - .github/workflows, GitLab CI, etc

## 3. Exemplo de fluxo de commit

1. `git checkout -b feature/nome-da-funcionalidade`
2. Fazer alterações no código
3. `git add .`
4. Exemplo de commit:
   - `git commit -m "feat: adicionar filtro por categoria" -m "Adiciona opção na UI e backend"`
5. `git push -u origin feature/nome-da-funcionalidade`
6. Abrir PR e referenciar issue (se houver)

## 4. Ajustes de commits locais

- `git commit --amend` (editar último commit)
- `git reset --soft HEAD~1` (desfazer último commit, manter alterações)
- `git rebase -i HEAD~n` (editar histórico antes do merge)

## 5. Regras no repositório

- Commits devem ter escopo se aplicável: `feat(login):`, `fix(api):`, etc.
- Mensagem em inglês (padrão obrigatório)
- 72 caracteres por linha no título recomendados
- Body do commit (quando necessário) com 1 linha em branco após título

---


