# Setup do Ambiente - ChatLLM Lab

Este documento descreve como configurar o ambiente de desenvolvimento do ChatLLM Lab.

## Stack Base

1. Backend: FastAPI (Python).
2. Frontend: React com JSX compilado em runtime (Babel no navegador, sem build complexo).
3. Persistencia: SQLite.

## Setup Inicial

1. Clone seu fork e entre no diretorio do projeto.
2. Instale as dependencias, configure o ambiente virtual `.venv` e extraia o `.env`:

Linux/Mac:

```bash
bash ./setup.sh
```

Windows:

```bat
setup.bat
```

3. O arquivo `.env` e extraido pelo script de setup a partir de um arquivo protegido por senha incluido no repositorio. Quando o script pedir, **digite a senha fornecida pelo professor**:
   - Os caracteres nao aparecem enquanto voce digita; isso e normal.
   - Se a senha estiver errada, o setup para com erro. Confirme a senha com o professor e execute o setup novamente.
   - A extracao usa ferramentas do proprio sistema: `unzip` no Linux/Mac (se faltar: `sudo apt install unzip`) e `tar.exe` no Windows 10 (versao 1803+) ou 11.
   - Se o `.env` ja existir na raiz do projeto, a extracao e ignorada.
   - O `.env` extraido contem `OPENROUTER_API_KEY` e `OPENROUTER_MODEL`. Nunca faca commit dele (ja esta no `.gitignore`).

4. Abra `http://127.0.0.1:8000` no navegador para usar o chat.

## Endpoints da API

1. `GET /health` retorna status da API.
2. `POST /api/chat` envia mensagem para o modelo e retorna resposta.
3. `POST /api/chat/stream` envia mensagem e retorna a resposta em streaming (SSE), com renderizacao progressiva no chat.

Exemplo de request:

```json
{
  "message": "Explique o que e um LLM em uma frase.",
  "history": [
    { "role": "user", "content": "Oi" },
    { "role": "assistant", "content": "Oi!" }
  ]
}
```
