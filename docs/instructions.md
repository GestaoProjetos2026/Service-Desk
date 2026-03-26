# Instruções básicas

## 1) Preparar ambiente

1. Abra terminal no projeto:
   - `cd .\Service-Desk`
2. Crie e ative virtualenv (Windows PowerShell):
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
3. Instale dependências:
   - `pip install -U pip`
   - `pip install -r requirements.txt`

## 2) Configurar banco de dados

- Verifique se existe `.env` na raiz. Se não existir, crie copiando `.env.example`:
  - `copy .env.example .env` (PowerShell)
  - `cp .env.example .env` (Linux/Mac)
- No `.env`, preencha as variáveis:
  - `DB_HOST=localhost`
  - `DB_PORT=3306`
  - `DB_NAME=service_desk`
  - `DB_USER=user`
  - `DB_PASSWORD=pass`
- Não é necessário editar `app/config/config.py`, ele lê `.env` automaticamente.

## 3) Rodar Alembic (sincronizar DB)

1. Gerar migration (nova mudança de modelo):
   - `python -m alembic revision --autogenerate -m "Create tables"`
2. Aplicar migration:
   - `python -m alembic upgrade head`

⚠️ Observação: se `python -m alembic` não funcionar, verifique se o ambiente está ativado e se `alembic` está instalado (`pip install alembic`).

## 4) Iniciar aplicação

1. Executar main via uvicorn (preferido):
     - `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`

2. Executar diretamente via módulo `main.py` (só para teste rápido):
   - `python -m app.main`

3. Verifique saúde:
   - `http://127.0.0.1:8000/health`

4. Documentação Swagger (debug):
   - `http://127.0.0.1:8000/docs`

5. Se não tiver instalado `uvicorn`, instale com:
   - `pip install uvicorn[standard]` ou
   - `.venv\Scripts\python.exe -m pip install uvicorn[standard]`

## 5) Dicas rápidas

- Para ver status do banco:
  - `python -m alembic current`
- Para desfazer migration:
  - `python -m alembic downgrade -1`
- Caso o terminal não reconheça o comando python:
  - `Troque por "py" somente`
