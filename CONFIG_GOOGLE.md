# Configuração do Google para o experimento

Este procedimento altera temporariamente o mecanismo de pesquisa padrão do Google no Chrome para evitar que as pesquisas realizadas pela barra de endereços exibam respostas geradas por IA.

Ao final do experimento, a configuração poderá ser revertida.

## Antes do experimento — desativar respostas de IA

### 1. Abra as configurações de mecanismos de pesquisa

Na barra de endereços do Chrome, digite:

```text
chrome://settings/searchEngines
```

e pressione **Enter**.

### 2. Vá até "Pesquisa no site"

Localize a seção **Pesquisa no site** (*Site search*).

Clique em **Adicionar** (*Add*).

### 3. Crie um mecanismo de pesquisa sem IA

Preencha os campos da seguinte forma:

**Nome:**

```text
Google sem IA
```

**Atalho:**

```text
google-sem-ia
```

**URL com %s no lugar da consulta:**

```text
https://www.google.com/search?q=%s&udm=14
```

Clique em **Salvar** (*Save*).

### 4. Defina "Google sem IA" como padrão

Na lista de mecanismos de pesquisa, localize:

```text
Google sem IA
```

Clique nos **três pontos** ao lado dele.

Selecione:

**Definir como padrão** (*Make default*).

### 5. Verifique se funcionou

Abra uma nova aba.

Na barra de endereços, pesquise, por exemplo:

```text
por que o céu é azul
```

A pesquisa deverá abrir os resultados da aba **Web**, sem a seção **"Visão geral criada por IA"**.

### Importante durante o experimento

Utilize a pesquisa normalmente pela barra de endereços do Chrome.

A configuração acima não autoriza o uso de outros recursos de IA. Durante o experimento, não utilize:

* Modo IA do Google;
* Gemini;
* ChatGPT;
* GitHub Copilot;
* Claude;
* Codex;
* outros assistentes ou ferramentas de IA generativa.

---

# Depois do experimento — voltar o Google ao normal

## Opção recomendada

### 1. Abra novamente

```text
chrome://settings/searchEngines
```

### 2. Localize o Google original

Na seção de mecanismos de pesquisa, localize o mecanismo chamado:

```text
Google
```

Clique nos **três pontos** ao lado dele.

Selecione:

**Definir como padrão** (*Make default*).

### 3. Remova o mecanismo temporário

Localize:

```text
Google sem IA
```

Clique nos **três pontos** ao lado dele e selecione:

**Excluir** (*Delete*).

### 4. Teste

Abra uma nova aba e faça uma pesquisa normalmente.

A URL não deverá mais conter:

```text
udm=14
```

---

# Se as respostas de IA não voltarem depois do experimento

Caso o Google tenha voltado a ser o mecanismo padrão, mas as respostas de IA não apareçam mais quando normalmente apareceriam, crie um mecanismo de pesquisa normal manualmente.

Em:

```text
chrome://settings/searchEngines
```

clique em **Adicionar**.

Preencha:

**Nome:**

```text
Google Normal
```

**Atalho:**

```text
google-normal
```

**URL:**

```text
https://www.google.com/search?q=%s
```

Salve e escolha **Definir como padrão**.

Faça novamente uma pesquisa.

A URL deverá ter o formato:

```text
https://www.google.com/search?q=sua+pesquisa
```

Depois disso, o Google volta a decidir normalmente quando exibir recursos como **Visão geral criada por IA**.
