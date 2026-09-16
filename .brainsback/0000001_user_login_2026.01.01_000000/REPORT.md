# Implementation Report

> A concise summary for the reviewer.

**Reviewer note**: If a PR modifies `.brainsback/<task-folder>/TODO.md` or `.brainsback/<task-folder>/REACTO.md`, assume this is expected and that those files were modified by the human developer.
If present, use `.github/skills/brainsback-reviewer/SKILL.md` as the review rubric.

## Snapshot
- **Change**: Implementação de autenticação (signup, login, logout) com JWT e proteção das rotas de chat.
- **Status**: Implementado e testado (59/59 testes passando).

## Arquivos criados
- `backend/auth.py` — Utilitários compartilhados de autenticação (hash de senha, criação/decodificação de JWT, dependência `get_current_user`)
- `backend/routers/auth.py` — Rotas `/api/auth/signup`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`
- `backend/schemas/auth.py` — Schemas Pydantic (`SignupRequest`, `LoginRequest`, `AuthResponse`, `LogoutRequest`, `MessageResponse`)
- `frontend/src/Auth.jsx` — Componente React de login/signup com toggle entre modos
- `tests/test_auth.py` — 18 testes de autenticação (signup, login, logout, proteção de rotas)

## Arquivos modificados
- `backend/models.py` — Adicionados modelos `User` (id, email, hashed_password, created_at) e `TokenBlacklist` (jti, created_at)
- `backend/config.py` — Adicionadas configs JWT (`JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`)
- `backend/main.py` — Registrado auth router; endpoints `/health` e `/` movidos para fora do router de chat (públicos)
- `backend/routers/chat.py` — Adicionada dependência `Depends(get_current_user)` em todas as rotas; removido `/health` do router
- `backend/requirements.txt` — Adicionadas dependências `python-jose[cryptography]` e `passlib[bcrypt]`
- `frontend/src/api.js` — Função `getAuthHeaders()` para incluir token JWT nas requisições
- `frontend/src/App.jsx` — Estado de autenticação (token/email), renderização condicional (Auth vs Chat), botão de logout no header
- `frontend/index.html` — CSS de autenticação; script `Auth.jsx` adicionado; header adaptado para flexbox com email e botão logout
- `tests/test_chat.py` — Testes de chat agora criam usuário e enviam token JWT

## Lógica central
- Senhas hashadas com bcrypt via passlib
- Tokens JWT com JTI único, expiração em 24h
- Blacklist de tokens no banco SQLite para logout funcional
- Toda rota em `chat.py` protegida via dependência global no APIRouter
- Endpoints `/health`, `/`, `/api/auth/signup`, `/api/auth/login` são públicos
- Frontend armazena token no `localStorage` e o envia via header `Authorization: Bearer`

## Testes
- 18 testes novos em `tests/test_auth.py` cobrindo: signup (sucesso, duplicata, senha fraca), login (sucesso, senha errada, usuário inexistente), logout (sucesso, duplicado, sem token, token rejeitado no chat), `/me`, proteção de chat
- Testes existentes em `test_chat.py` atualizados para usar autenticação
- `test_health` e `test_root` permanecem públicos (sem auth)

## Riscos conhecidos
- `JWT_SECRET_KEY` hardcoded em `config.py` — trocar por env var em produção
- bcrypt 5.x é incompatível com passlib 1.7.4 (gera `ValueError` ao hashear senha). Fixado fixando `bcrypt<5.0.0`
- `allow_origins=["*"]` com `allow_credentials=False` — adequado para experimento, não para produção 

## Hotfix — bcrypt 5.x incompatível (2026-06-16)
**Problema:** Ao tentar criar usuário via `/api/auth/signup`, o servidor retornava **500 Internal Server Error** sem mensagem de erro detalhada na resposta.

**Causa raiz:** O `passlib==1.7.4` tenta ler `bcrypt.__about__.__version__` para detectar a versão do bcrypt. Esse atributo foi removido no `bcrypt==5.0.0`, causando um `AttributeError` interno. O passlib então cai num fallback que tenta verificar um hash de teste com `bcrypt.hashpw`, que por sua vez lança `ValueError: password cannot be longer than 72 bytes` — um bug de detecção de versão do bcrypt 5.x.

**Solução:** Fixado `bcrypt<5.0.0` (versão 4.3.0) no `requirements.txt` e no `.venv`.

**Verificação:** Teste manual via curl retorna HTTP 201 com token JWT válido.

## The Changes
- [ ] 

## Testing Strategy
_How we ensured it works._

## Risks & Follow-up
- [ ] 

---
**Note**: Usually filled by the AI.
