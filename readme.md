# API de Operadoras e Interface Web

Aplicação desenvolvida para a etapa de API e interface web do teste técnico da Intuitive Care.

O projeto possui um backend em Python com FastAPI, conectado a um banco de dados MySQL, e uma interface em Vue.js para consultar operadoras de saúde, visualizar despesas e acompanhar estatísticas agregadas.

## Sobre o projeto

O objetivo desta etapa é disponibilizar os dados das operadoras por meio de uma API e apresentar essas informações em uma interface web.

O backend consulta tabelas já existentes no banco de dados e disponibiliza rotas para:

* Listar operadoras;
* Buscar operadoras por razão social ou CNPJ;
* Consultar os detalhes de uma operadora;
* Consultar o histórico de despesas;
* Calcular estatísticas agregadas.

O frontend consome essas rotas e apresenta:

* Um dashboard de estatísticas;
* Uma tabela paginada de operadoras;
* Um campo de pesquisa;
* Uma página de detalhes;
* Um gráfico de despesas por UF.

Este repositório corresponde somente à etapa 4 do teste técnico. A criação e a importação inicial dos dados no banco pertencem a outra etapa e não são executadas por esta aplicação.

## Funcionalidades implementadas

### Backend

* API desenvolvida com FastAPI;
* Conexão com banco de dados MySQL;
* Configuração da conexão por variáveis de ambiente;
* Listagem paginada de operadoras;
* Limite padrão de 10 registros por página;
* Validação dos parâmetros de paginação;
* Busca por razão social ou CNPJ;
* Consulta de uma operadora pelo CNPJ;
* Consulta do histórico trimestral de despesas;
* Cálculo do total geral de despesas;
* Cálculo da média geral de despesas;
* Consulta das cinco operadoras com maiores despesas;
* Consulta da distribuição de despesas por UF;
* Respostas `404` para operadoras ou despesas não encontradas;
* Configuração de CORS para o frontend local.

### Frontend

* Navegação entre páginas com Vue Router;
* Dashboard com total e média de despesas;
* Tabela com as cinco operadoras com maiores despesas;
* Gráfico de barras com despesas por UF;
* Tabela paginada de operadoras;
* Pesquisa por razão social ou CNPJ;
* Página de detalhes da operadora;
* Exibição do histórico de despesas;
* Formatação de valores em reais;
* Formatação visual de CNPJ;
* Estados de carregamento;
* Mensagens para erros e dados vazios;
* Layout responsivo com CSS;
* Botões de página anterior e próxima página.

### Documentação da API

* Coleção do Postman com todas as rotas;
* Exemplos de respostas de sucesso;
* Exemplos de respostas `404`;
* Variável `base_url` configurada na coleção.


## Estrutura do projeto

```text
.
├── backend/
│   ├── banco.py
│   └── main.py
│
├── frontend/
│   └── src/
│       ├── router/
│       │   └── index.js
│       ├── services/
│       │   └── api.js
│       ├── views/
│       │   ├── DetalhesOperadoraView.vue
│       │   ├── EstatisticasView.vue
│       │   └── OperadorasView.vue
│       ├── App.vue
│       ├── main.js
│       └── style.css
│
├── API de Operadoras - Intuitive Care.postman_collection.json
└── README.md
```

### Principais arquivos

#### `backend/main.py`

Cria a aplicação FastAPI, configura o CORS e define as rotas da API.

Também contém as consultas SQL utilizadas para listar operadoras, consultar despesas e calcular estatísticas.

#### `backend/banco.py`

Centraliza a criação da conexão com o MySQL.

Os dados de acesso são lidos de variáveis de ambiente usando `python-dotenv`.

#### `frontend/src/main.js`

É o ponto de entrada do frontend.

Esse arquivo:

1. Cria a aplicação Vue;
2. Registra o Vue Router;
3. Importa o CSS global;
4. Monta a aplicação no elemento HTML com o identificador `app`.

#### `frontend/src/App.vue`

Define o cabeçalho principal e os links de navegação.

O conteúdo das páginas é exibido pelo componente `RouterView`.

#### `frontend/src/router/index.js`

Define as páginas disponíveis no frontend:

```text
/                     Dashboard
/operadoras           Lista de operadoras
/operadoras/:cnpj     Detalhes da operadora
```

O trecho `:cnpj` representa um parâmetro dinâmico da URL.

#### `frontend/src/services/api.js`

Centraliza as requisições HTTP feitas ao backend.

As funções disponíveis são:

* `listarOperadoras`;
* `exibirDetalhesOperadora`;
* `listarDespesas`;
* `exibirEstatisticas`.

#### `frontend/src/views/OperadorasView.vue`

Apresenta a tabela de operadoras, o campo de pesquisa e os controles de paginação.

#### `frontend/src/views/DetalhesOperadoraView.vue`

Consulta o CNPJ presente na URL e apresenta os dados cadastrais e o histórico de despesas da operadora.

#### `frontend/src/views/EstatisticasView.vue`

Apresenta o dashboard, os valores agregados, o top 5 de operadoras e o gráfico de despesas por UF.

#### `frontend/src/style.css`

Contém os estilos globais da aplicação, incluindo tabelas, botões, mensagens, cards, gráfico e regras de responsividade.

## Banco de dados

A aplicação depende de um banco MySQL já criado e preenchido.

As consultas existentes utilizam as seguintes tabelas:

### `operadoras`

Campos utilizados:

* `id`;
* `registro_ans`;
* `cnpj`;
* `razao_social`;
* `modalidade`;
* `uf`.

### `despesas_consolidadas`

Campos utilizados:

* `operadora_id`;
* `ano`;
* `trimestre`;
* `valor_despesas`.

### `despesas_agregadas`

Campos utilizados:

* `operadora_id`;
* `total_despesas`.

Os scripts de criação e importação dessas tabelas não foram identificados nos arquivos analisados desta etapa. Portanto, o banco precisa estar preparado antes da execução da API.

## Como executar

### 1. Pré-requisitos

Para executar o projeto, são necessários:

* Python;
* MySQL;
* Node.js;
* npm.


### 2. Configurar o banco de dados

O MySQL precisa estar em execução e conter as tabelas usadas pela aplicação.

Crie um arquivo chamado `.env` na pasta do backend:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
```

Significado das variáveis:

| Variável      | Descrição                  |
| ------------- | -------------------------- |
| `DB_HOST`     | Endereço do servidor MySQL |
| `DB_PORT`     | Porta do MySQL             |
| `DB_USER`     | Usuário do banco           |
| `DB_PASSWORD` | Senha do banco             |
| `DB_NAME`     | Nome do banco utilizado    |


### 3. Instalar as dependências do backend

Entre na pasta do backend:

```bash
cd backend
```

Instale as bibliotecas utilizadas no código:

```bash
pip install fastapi uvicorn mysql-connector-python python-dotenv
```


### 4. Executar o backend

Dentro da pasta que contém o arquivo `main.py`, execute:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

A documentação automática do FastAPI poderá ser acessada em:

```text
http://localhost:8000/docs
```

O backend precisa continuar em execução enquanto o frontend estiver sendo utilizado.

### 5. Instalar as dependências do frontend

Em outro terminal, entre na pasta do frontend:

```bash
cd frontend
```

Instale as dependências configuradas no projeto:

```bash
npm install
```

### 6. Executar o frontend

```bash
npm run dev
```

O endereço utilizado pelo projeto durante o desenvolvimento é:

```text
http://localhost:5173
```

O backend permite requisições CORS especificamente dessa origem.

### 7. Acessar a aplicação

Abra no navegador:

```text
http://localhost:5173
```

A página inicial apresenta o dashboard.

A listagem de operadoras pode ser acessada em:

```text
http://localhost:5173/operadoras
```

## Rotas da API

### Listar operadoras

```http
GET /api/operadoras
```

Parâmetros disponíveis:

| Parâmetro | Obrigatório | Valor padrão | Regra                             |
| --------- | ----------: | -----------: | --------------------------------- |
| `page`    |         Não |          `1` | Deve ser maior ou igual a 1       |
| `limit`   |         Não |         `10` | Deve estar entre 1 e 100          |
| `busca`   |         Não |        vazio | Pesquisa por razão social ou CNPJ |

Exemplo:

```http
GET /api/operadoras?page=1&limit=10&busca=Bradesco
```

Exemplo resumido de resposta:

```json
{
  "data": [
    {
      "id": 167,
      "registro_ans": "421715",
      "cnpj": "15011651000154",
      "razao_social": "BRADESCO SAÚDE - OPERADORA DE PLANOS S/A",
      "modalidade": "Medicina de Grupo",
      "uf": "SP"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

### Consultar uma operadora

```http
GET /api/operadoras/{cnpj}
```

Exemplo:

```http
GET /api/operadoras/15011651000154
```

Exemplo de resposta:

```json
{
  "data": {
    "id": 167,
    "registro_ans": "421715",
    "cnpj": "15011651000154",
    "razao_social": "BRADESCO SAÚDE - OPERADORA DE PLANOS S/A",
    "modalidade": "Medicina de Grupo",
    "uf": "SP"
  }
}
```

Quando o CNPJ não é encontrado, a API retorna:

```json
{
  "detail": "Operadora não encontrada"
}
```

Status HTTP:

```text
404 Not Found
```

### Consultar despesas da operadora

```http
GET /api/operadoras/{cnpj}/despesas
```

Exemplo:

```http
GET /api/operadoras/15011651000154/despesas
```

Exemplo resumido de resposta:

```json
{
  "data": [
    {
      "cnpj": "15011651000154",
      "razao_social": "BRADESCO SAÚDE - OPERADORA DE PLANOS S/A",
      "ano": 2026,
      "trimestre": 1,
      "valor_despesas": 1582958456.44
    }
  ]
}
```

As despesas são ordenadas do período mais recente para o mais antigo.

Quando não existem despesas para o CNPJ, a API retorna:

```json
{
  "detail": "Despesas não encontradas para a operadora"
}
```

Status HTTP:

```text
404 Not Found
```

### Consultar estatísticas

```http
GET /api/estatisticas
```

Exemplo resumido de resposta:

```json
{
  "total_despesas": 3507346773624.54,
  "media_despesas": 1587753179.549362,
  "top_operadoras": [
    {
      "cnpj": "92693118000160",
      "razao_social": "BRADESCO SAÚDE S.A.",
      "total_despesas": 426220771547.66
    }
  ],
  "distribuicao_uf": [
    {
      "uf": "SP",
      "total_despesas_uf": 1262719874370.91,
      "media_despesas_por_operadora": 4280406353.8
    }
  ]
}
```

## Coleção do Postman

A coleção está disponível no arquivo:

```text
API de Operadoras - Intuitive Care.postman_collection.json
```

Ela contém as seguintes requisições:

* Listar operadoras;
* Buscar operadoras;
* Detalhar operadora;
* Listar despesas da operadora;
* Consultar estatísticas.

A coleção também contém exemplos de:

* Respostas com status `200`;
* Operadora não encontrada;
* Despesas não encontradas.

A variável utilizada pela coleção é:

```text
base_url = http://localhost:8000
```

Para utilizar:

1. Inicie o backend;
2. Abra o Postman;
3. Escolha a opção de importar;
4. Selecione o arquivo da coleção;
5. Execute as requisições.

## Fluxo de funcionamento

1. O usuário acessa uma página pelo navegador.
2. O Vue Router identifica a URL e escolhe o componente correspondente.
3. O componente chama uma função do arquivo `services/api.js`.
4. A função utiliza `fetch` para enviar uma requisição ao backend.
5. O FastAPI recebe a requisição.
6. A rota abre uma conexão com o MySQL.
7. O backend executa uma consulta SQL com parâmetros.
8. O resultado é convertido em um objeto que pode ser retornado como JSON.
9. O cursor e a conexão com o banco são fechados.
10. O frontend recebe a resposta.
11. Os dados são armazenados em estados reativos do Vue.
12. O template atualiza a tabela, os cards ou o gráfico.

## Decisões técnicas

### Escolha do framework do backend

**Escolha:** FastAPI.

**Motivo:** a API possui poucas rotas e trabalha principalmente com consultas e respostas em JSON. O FastAPI permite declarar essas rotas de forma direta e possui recursos de validação que ajudam a manter o código simples.

**Ponto positivo:** os parâmetros `page` e `limit` podem ser validados diretamente com `Query`, e erros HTTP podem ser retornados com `HTTPException`.

**Limitação:** as rotas e consultas SQL estão concentradas no arquivo `main.py`. Caso o projeto aumente, esse arquivo poderá ficar mais difícil de organizar e manter.

### Estratégia de paginação

**Escolha:** paginação baseada em offset.

A implementação utiliza:

```sql
LIMIT
OFFSET
```

O offset é calculado com:

```text
(page - 1) * limit
```

**Motivo:** os dados são consultados em páginas numeradas, e a interface possui apenas os botões anterior e próxima. Para esse projeto, a abordagem é simples de implementar e suficiente para a navegação esperada.

**Ponto positivo:** permite acessar uma página usando apenas os parâmetros `page` e `limit`.

**Limitação:** offsets muito altos podem tornar a consulta mais lenta em bancos com uma quantidade muito maior de registros. Também pode haver alteração na posição dos registros caso os dados sejam modificados durante a navegação.

### Cache ou consultas diretas

**Escolha:** consultas diretas ao banco em cada chamada.

**Motivo:** não foi implementado um mecanismo de cache. Sempre que `/api/estatisticas` é acessada, o backend executa novamente as consultas de total, média, top 5 e distribuição por UF.

A distribuição por UF consulta a tabela `despesas_agregadas`, mas a consulta ainda é executada novamente a cada requisição.

**Ponto positivo:** o resultado apresentado corresponde ao estado atual do banco no momento da chamada.

**Limitação:** chamadas repetidas executam novamente operações de agregação no banco. Caso a rota receba muitas requisições, um cache poderia reduzir o trabalho repetido.

### Estrutura da resposta paginada

**Escolha:** dados acompanhados de metadados.

A resposta da listagem contém:

```json
{
  "data": [],
  "total": 0,
  "page": 1,
  "limit": 10
}
```

**Motivo:** o frontend precisa saber o total de registros para calcular a quantidade de páginas e desabilitar o botão de próxima página quando necessário.

**Ponto positivo:** a interface não precisa fazer uma requisição separada apenas para descobrir o total de operadoras.

**Limitação:** as respostas da API não possuem exatamente o mesmo formato em todas as rotas. As rotas de operadoras usam a propriedade `data`, enquanto a rota de estatísticas retorna seus campos diretamente no objeto principal.

### Estratégia de busca

**Escolha:** busca no servidor.

O frontend envia o conteúdo pesquisado pelo parâmetro:

```text
busca
```

O backend pesquisa nos campos `razao_social` e `cnpj` com `LIKE`.

**Motivo:** o frontend recebe somente uma página de registros. Uma busca apenas no cliente encontraria somente operadoras da página atual, e não todas as operadoras do banco.

**Ponto positivo:** a busca considera o conjunto completo de registros armazenados.

**Limitação:** o evento de digitação chama a busca novamente a cada alteração do campo. Não foi implementado debounce, portanto uma sequência rápida de digitação pode gerar várias requisições.

### Gerenciamento de estado no frontend

**Escolha:** estado local nos componentes com a Composition API do Vue.

Foram utilizados recursos como:

* `ref`;
* `computed`;
* `onMounted`.

Não foram utilizados Vuex, Pinia ou composables personalizados.

**Motivo:** as páginas possuem dados próprios e não precisam compartilhar um estado global complexo.

**Ponto positivo:** reduz a quantidade de arquivos e configurações necessárias.

**Limitação:** os dados são carregados novamente ao entrar nas páginas. O estado da listagem e da pesquisa não é mantido em um gerenciador global.

### Performance da tabela

**Escolha:** paginação no servidor e renderização somente da página atual.

O frontend solicita 10 registros por vez.

**Motivo:** não é necessário carregar todas as operadoras no navegador para exibir a tabela.

**Ponto positivo:** a quantidade de linhas renderizadas permanece pequena e não exige virtualização da tabela.

**Limitação:** cada troca de página depende de uma nova requisição ao backend.

### Tratamento de erros e loading

**Escolha:** estados locais com `try`, `catch` e `finally`.

Antes de uma chamada, o estado de loading é ativado:

```javascript
carregando.value = true
```

No `catch`, uma mensagem é definida.

No `finally`, o loading é encerrado:

```javascript
carregando.value = false
```

O arquivo `api.js` também verifica:

```javascript
resposta.ok
```

Quando a resposta não possui um status de sucesso, uma exceção é lançada.

**Motivo:** separar loading, dados e erro evita que a aplicação dependa apenas do tempo da requisição.

**Ponto positivo:** o usuário recebe uma indicação enquanto a API está sendo consultada e uma mensagem quando a operação falha.

**Limitação:** as mensagens do frontend são genéricas. O serviço não mantém o código HTTP nem o campo `detail` enviado pelo FastAPI.

Na página de detalhes existe uma tentativa de identificar um erro `404` verificando se a mensagem contém o texto `404`. Porém, as exceções criadas em `api.js` não incluem o código do status. Por esse motivo, essa diferenciação não funciona de forma confiável no estado atual.

Além disso, a variável `erroDespesas` é preenchida no componente de detalhes, mas não é exibida diretamente no template atual.

### Mensagens de dados vazios

**Escolha:** exibição de textos simples quando não existem registros para mostrar.

Exemplos presentes na interface:

```text
Nenhuma operadora encontrada.
Nenhuma estatística encontrada.
Dados não encontrados.
```

**Motivo:** uma tabela vazia sem explicação poderia parecer um erro de carregamento.

**Ponto positivo:** o usuário recebe uma indicação de que não existem dados para aquela situação.

**Limitação:** em algumas páginas, as condições de loading e vazio não fazem parte de uma única sequência de `v-if` e `v-else-if`. Por isso, uma mensagem de vazio pode aparecer junto com a mensagem de carregamento ou de erro.

### Comunicação entre frontend e backend

**Escolha:** chamadas HTTP com `fetch` centralizadas em `services/api.js`.

**Motivo:** evita repetir a URL da API e a verificação de resposta dentro de cada página.

**Ponto positivo:** as views ficam responsáveis principalmente pelos dados e pela interface.

**Limitação:** a URL do backend está escrita diretamente no código:

```javascript
const URL_BASE = "http://localhost:8000/api"
```

Para utilizar outro endereço, é necessário alterar o arquivo e gerar novamente o frontend.

### Conexão com o banco

**Escolha:** abrir e fechar uma conexão em cada rota.

**Motivo:** é uma implementação direta e fácil de compreender para uma API pequena.

**Ponto positivo:** as conexões são fechadas ao final de cada operação de sucesso.

**Limitação:** não existe pool de conexões. Também não foi identificado um bloco `try/finally` no backend para garantir o fechamento da conexão quando ocorre uma exceção durante a consulta.

## Tratamento de inconsistências

### Parâmetros de paginação inválidos

O FastAPI valida:

* `page` maior ou igual a 1;
* `limit` maior ou igual a 1;
* `limit` menor ou igual a 100.

Quando o valor não atende às regras, o FastAPI rejeita a entrada antes de executar a consulta.

### Operadora inexistente

Quando a consulta por CNPJ não encontra uma operadora, o backend retorna:

```text
404 - Operadora não encontrada
```

### Despesas inexistentes

Quando não existem despesas para o CNPJ informado, o backend retorna:

```text
404 - Despesas não encontradas para a operadora
```

### Consultas parametrizadas

Os valores recebidos pela API são enviados separadamente para o `mysql.connector`.

Exemplo:

```python
cursor.execute(
    "SELECT * FROM operadoras WHERE cnpj = %s",
    (cnpj,)
)
```

Isso evita montar a consulta SQL concatenando diretamente o valor recebido.

### Validação de CNPJ

A API pesquisa o CNPJ como texto, mas não valida os dígitos verificadores nem remove pontuação.

O frontend envia o CNPJ armazenado no banco sem formatação ao acessar a página de detalhes.

## Limitações atuais

* O banco precisa estar criado e preenchido antes da execução;
* Não existe cache para a rota de estatísticas;
* As consultas SQL estão dentro do mesmo arquivo das rotas;
* A busca pode realizar uma requisição a cada caractere digitado;
* O frontend utiliza mensagens de erro genéricas;
* O status HTTP e a mensagem `detail` da API não são preservados pelo serviço do frontend;
* Algumas mensagens de dados vazios podem aparecer durante o loading;

## Possíveis melhorias

Uma possível melhoria seria utilizar uma variável de ambiente do Vite para configurar a URL da API, evitando alterar diretamente o arquivo `api.js`.

Uma possível melhoria seria criar um erro personalizado no serviço do frontend contendo o status HTTP e o conteúdo retornado pelo backend.

O backend poderia separar rotas, consultas e acesso ao banco em arquivos diferentes caso novas funcionalidades fossem adicionadas.

O projeto poderia utilizar um pool de conexões e blocos `try/finally` para controlar melhor o fechamento de cursores e conexões.


## Autor

Ronaldo Dutra Filho
