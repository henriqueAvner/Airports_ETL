# ✈️ Brazilian Airports ETL

Boas-vindas ao projeto **Brazilian Airports ETL**!

Neste projeto, você irá desenvolver de forma autônoma um pipeline de Engenharia de Dados responsável por **extrair dados públicos de aeroportos brasileiros, transformar e validar os registros, armazenar os dados processados em CSV e carregá-los em um banco PostgreSQL**.

> ⚠️ **Importante:** este é um projeto-exercício. O README descreve **o que deve ser desenvolvido e os critérios que sua solução deve atender**, mas não define a implementação completa. Decisões de código, bibliotecas auxiliares e organização interna fazem parte do exercício.

---

## 🎯 Objetivo do projeto

O objetivo é consolidar os principais conhecimentos trabalhados no primeiro projeto da trilha de Engenharia de Dados:

- consumo de dados de uma fonte externa;
- organização de um pipeline ETL;
- manipulação de JSON e CSV;
- transformação de dados com Python;
- validação e Data Quality;
- separação de registros válidos e rejeitados;
- carregamento em PostgreSQL;
- modelagem básica de tabela;
- carga idempotente;
- consultas SQL analíticas;
- logging e tratamento de erros;
- organização e documentação de um projeto de dados.

Ao final, o pipeline deverá seguir conceitualmente este fluxo:

```text
Fonte pública de aeroportos
            │
            ▼
        EXTRACT
            │
            ▼
      Raw Data (JSON)
            │
            ▼
       TRANSFORM
       /       \
      /         \
 válidos      inválidos
    │             │
    ▼             ▼
Processed       Rejected
  (CSV)          (JSON)
    │
    ▼
   LOAD
    │
    ▼
PostgreSQL
    │
    ▼
Consultas SQL
```

---

## 📝 Habilidades a serem trabalhadas

Neste projeto, será verificado se você é capaz de:

- estruturar um pipeline ETL em Python;
- consumir e persistir dados de uma fonte pública;
- preservar uma camada de dados brutos;
- transformar registros para um schema definido;
- validar dados antes de carregá-los;
- registrar motivos de rejeição;
- gerar arquivos CSV corretamente;
- modelar e criar uma tabela PostgreSQL;
- implementar uma estratégia de carga idempotente;
- utilizar SQL para análise dos dados;
- implementar logs úteis para acompanhamento do pipeline;
- separar responsabilidades entre Extract, Transform e Load;
- documentar decisões técnicas.

---

# 📦 Entregáveis

Ao finalizar o projeto, o repositório deverá possuir:

```text
Brazilian_Airports_ETL/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── logs/
│
├── sql/
│   ├── create_tables.sql
│   └── analysis.sql
│
├── src/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   └── utils/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

Essa estrutura é uma **referência**, não uma obrigação absoluta. Você pode adaptá-la desde que mantenha uma separação clara de responsabilidades.

---

# 🗃️ Organização dos dados

O projeto deverá trabalhar com três áreas principais.

### Raw

```text
data/raw/
```

Deve conter os dados obtidos da fonte **antes das transformações principais**.

O formato recomendado é JSON.

Exemplo conceitual:

```json
[
  {
    "id": "ABC",
    "name": "Aeroporto Exemplo",
    "city": "Cidade Exemplo",
    "state": "MG",
    "latitude": "-19.0000",
    "longitude": "-44.0000"
  }
]
```

> A estrutura real dependerá da fonte escolhida por você.

### Processed

```text
data/processed/
```

Deve conter apenas registros considerados válidos após transformação e Data Quality.

Formato obrigatório:

```text
CSV
```

O arquivo deverá possuir:

- cabeçalho;
- encoding UTF-8;
- estrutura consistente entre os registros.

### Rejected

```text
data/rejected/
```

Deve armazenar registros que não atendam às regras de qualidade ou que não possam ser transformados.

Formato esperado:

```json
{
  "reasons": [
    "Motivo da rejeição"
  ],
  "record": {
    "...": "..."
  }
}
```

Você pode armazenar vários objetos desse formato dentro de uma lista JSON.

---

# ⚙️ Antes de começar

## 1. Crie o projeto

Crie um novo diretório:

```bash
mkdir Brazilian_Airports_ETL
cd Brazilian_Airports_ETL
```

## 2. Crie um ambiente virtual

Windows:

```bash
python -m venv .venv
```

CMD:

```bash
.venv\Scripts\activate
```

Git Bash:

```bash
source .venv/Scripts/activate
```

Linux:

```bash
source .venv/bin/activate
```

## 3. Crie seu `requirements.txt`

Adicione somente dependências externas realmente utilizadas pelo projeto.

Bibliotecas da Standard Library, como:

```text
json
csv
logging
datetime
pathlib
```

não precisam ser adicionadas.

## 4. Configure o Git

Crie um `.gitignore` que impeça o versionamento de, no mínimo:

```text
.venv/
.env
__pycache__/
logs gerados
dados gerados pelo pipeline
```

Você pode utilizar `.gitkeep` caso queira preservar diretórios vazios no repositório.

---

# 📋 Requisitos do projeto

## 1. Escolha e documente uma fonte pública de aeroportos brasileiros

<details>
<summary><strong>O que deverá ser desenvolvido</strong></summary>

<br />

Você deverá localizar uma fonte pública que forneça dados de aeroportos brasileiros.

A fonte poderá ser, por exemplo:

- uma API REST;
- um dataset público em JSON;
- um dataset público em CSV.

A escolha da fonte faz parte do exercício.

No seu README final, documente:

- nome da fonte;
- endereço ou referência de onde os dados são obtidos;
- formato original;
- principais campos utilizados;
- qualquer limitação relevante encontrada.

### O que será avaliado

- **1.1** — Se a fonte utilizada contém dados reais de aeroportos brasileiros.
- **1.2** — Se a fonte está documentada.
- **1.3** — Se é possível entender como os dados chegam ao pipeline.
- **1.4** — Se a solução não depende de dados inventados como fonte principal.

</details>

---

## 2. Implemente a etapa de Extract

> **Sugestão de local:** `src/extract/`

<details>
<summary><strong>Extraia os dados e preserve uma cópia Raw</strong></summary>

<br />

A etapa de Extract deverá obter os registros da fonte escolhida.

Os dados extraídos deverão ser persistidos em:

```text
data/raw/
```

O formato recomendado para a camada Raw é:

```text
JSON
```

A Raw deve representar os dados **antes da transformação para o schema final**.

A extração também deverá possuir tratamento de erros apropriado para a fonte escolhida.

Caso utilize HTTP, considere situações como:

- falha de conexão;
- timeout;
- resposta HTTP inválida;
- resposta vazia.

### O que será avaliado

- **2.1** — Se os dados são obtidos corretamente.
- **2.2** — Se existe uma cópia Raw.
- **2.3** — Se o Raw não contém apenas o resultado final já transformado.
- **2.4** — Se erros inesperados não são silenciosamente ignorados.
- **2.5** — Se a quantidade de registros extraídos é registrada em log.

</details>

---

## 3. Implemente a transformação dos aeroportos

> **Sugestão de local:** `src/transform/`

<details>
<summary><strong>Transforme os dados para o schema esperado</strong></summary>

<br />

Cada aeroporto válido deverá resultar, no mínimo, nos seguintes campos:

```text
airport_id
airport_name
city
state_code
latitude
longitude
```

Exemplo conceitual:

```json
{
  "airport_id": "SBCF",
  "airport_name": "Aeroporto Internacional de Confins",
  "city": "Confins",
  "state_code": "MG",
  "latitude": -19.6244,
  "longitude": -43.9719
}
```

> Os valores acima são apenas uma demonstração de formato. Utilize os dados provenientes da sua fonte.

Se a fonte possuir campos adicionais que você considere relevantes, você pode incluí-los.

Durante a transformação, normalize os tipos necessários. Por exemplo, latitude e longitude devem estar adequadas para operações numéricas.

### O que será avaliado

- **3.1** — Se todos os campos mínimos estão presentes.
- **3.2** — Se latitude e longitude são representadas numericamente nos dados processados.
- **3.3** — Se a transformação está separada da extração.
- **3.4** — Se a solução suporta múltiplos registros.
- **3.5** — Se campos adicionais, quando utilizados, possuem propósito claro.

</details>

---

## 4. Implemente Data Quality e registros rejeitados

<details>
<summary><strong>Valide os registros antes de enviá-los para a camada Processed</strong></summary>

<br />

Um registro deverá ser rejeitado quando apresentar, no mínimo, uma das seguintes condições:

```text
airport_id ausente
airport_name vazio
state_code vazio
state_code inválido
latitude ausente
longitude ausente
latitude não convertível para número
longitude não convertível para número
```

Você deverá pensar na diferença entre:

```text
erro de transformação
```

e:

```text
violação de regra de qualidade
```

Um único registro inválido **não deve interromper todo o processamento do lote**.

Os registros rejeitados deverão ser armazenados em:

```text
data/rejected/
```

Cada rejeição deverá informar:

```json
{
  "reasons": [
    "Motivo 1",
    "Motivo 2"
  ],
  "record": {
    "...": "..."
  }
}
```

### O que será avaliado

- **4.1** — Se registros sem identificador são rejeitados.
- **4.2** — Se registros sem nome são rejeitados.
- **4.3** — Se UF vazia ou inválida é rejeitada.
- **4.4** — Se coordenadas ausentes são rejeitadas.
- **4.5** — Se coordenadas não numéricas são tratadas.
- **4.6** — Se um registro ruim não interrompe o lote inteiro.
- **4.7** — Se os motivos de rejeição são preservados.
- **4.8** — Se a quantidade de válidos e rejeitados aparece nos logs.

</details>

---

## 5. Gere a camada Processed em CSV

<details>
<summary><strong>Persista somente registros aprovados pela validação</strong></summary>

<br />

Os registros válidos deverão ser armazenados em:

```text
data/processed/
```

Formato obrigatório:

```text
CSV
```

O arquivo deverá possuir cabeçalho.

Exemplo:

```csv
airport_id,airport_name,city,state_code,latitude,longitude
ABC,Aeroporto Exemplo,Cidade Exemplo,MG,-19.0000,-44.0000
```

Utilize encoding:

```text
UTF-8
```

Você pode escolher o delimitador do CSV, mas deverá utilizá-lo consistentemente e documentá-lo.

### O que será avaliado

- **5.1** — Se somente registros válidos são gravados.
- **5.2** — Se o arquivo possui cabeçalho.
- **5.3** — Se os campos mínimos estão presentes.
- **5.4** — Se caracteres acentuados são preservados corretamente.
- **5.5** — Se o formato escolhido está documentado.

</details>

---

## 6. Modele e crie a tabela PostgreSQL

> **Crie o script em:** `sql/create_tables.sql`

<details>
<summary><strong>Crie uma tabela adequada para armazenar os aeroportos</strong></summary>

<br />

Você deverá definir a modelagem da tabela.

Ela precisa suportar, no mínimo:

```text
airport_id
airport_name
city
state_code
latitude
longitude
```

O identificador proveniente da fonte deverá possuir uma restrição que impeça aeroportos duplicados.

Você deverá escolher tipos PostgreSQL coerentes para cada coluna.

Exemplo conceitual:

```text
airport_id      → identificador
airport_name    → texto
city            → texto
state_code      → código da UF
latitude        → número decimal
longitude       → número decimal
```

Não copie automaticamente tipos de exemplos anteriores: avalie o dado que sua fonte realmente fornece.

### O que será avaliado

- **6.1** — Se existe um script de criação da tabela.
- **6.2** — Se os tipos utilizados são coerentes.
- **6.3** — Se os campos obrigatórios possuem restrições apropriadas.
- **6.4** — Se `airport_id` não pode ser duplicado.
- **6.5** — Se o script pode ser utilizado para preparar um banco novo.

</details>

---

## 7. Implemente a etapa de Load

> **Sugestão de local:** `src/load/`

<details>
<summary><strong>Carregue os registros válidos no PostgreSQL</strong></summary>

<br />

A etapa Load deverá utilizar os dados processados e persistir os aeroportos no PostgreSQL.

A carga deverá possuir logs indicando:

```text
início da carga
quantidade processada
fim da carga
falhas inesperadas
```

Credenciais do banco **não devem ser escritas diretamente no código-fonte**.

Utilize variáveis de ambiente quando necessário.

### O que será avaliado

- **7.1** — Se os dados processados chegam ao PostgreSQL.
- **7.2** — Se os campos são carregados corretamente.
- **7.3** — Se erros do banco são tratados e registrados.
- **7.4** — Se credenciais sensíveis não são versionadas.
- **7.5** — Se Extract, Transform e Load continuam com responsabilidades separadas.

</details>

---

## 8. Garanta idempotência da carga

<details>
<summary><strong>Executar o pipeline novamente não pode duplicar aeroportos</strong></summary>

<br />

Seu pipeline deverá poder ser executado mais de uma vez.

Cenário:

```text
1ª execução
    ↓
500 aeroportos no banco

2ª execução com os mesmos dados
    ↓
500 aeroportos no banco
```

O resultado **não** poderá ser:

```text
1000 aeroportos
```

Você deverá escolher e implementar uma estratégia apropriada.

A estratégia utilizada deverá ser explicada no README final do projeto.

> Não será fornecida aqui a instrução SQL que resolve o requisito. A escolha da estratégia faz parte da avaliação.

### O que será avaliado

- **8.1** — Se a segunda execução não gera duplicações.
- **8.2** — Se existe proteção também no banco de dados.
- **8.3** — Se a estratégia utilizada está documentada.
- **8.4** — Se o comportamento continua correto caso um aeroporto já existente apareça novamente.

</details>

---

## 9. Implemente logging do pipeline

> **Sugestão de local:** `src/utils/logger.py`

<details>
<summary><strong>Faça com que a execução possa ser acompanhada</strong></summary>

<br />

O pipeline deverá registrar pelo menos:

```text
início da extração
fim da extração
quantidade extraída

quantidade válida
quantidade rejeitada

início da carga
fim da carga

erros inesperados
```

Os logs deverão ser suficientemente claros para responder perguntas como:

```text
A extração funcionou?

Quantos registros chegaram?

Quantos foram rejeitados?

A carga terminou?

Em qual módulo ocorreu uma falha?
```

É recomendado que os logs sejam enviados tanto para o terminal quanto para:

```text
logs/pipeline.log
```

### O que será avaliado

- **9.1** — Se os principais estágios possuem logs.
- **9.2** — Se quantidades relevantes são registradas.
- **9.3** — Se exceções inesperadas preservam informações úteis para diagnóstico.
- **9.4** — Se o logging não está configurado repetidamente sem necessidade em todos os módulos.

</details>

---

<br />

## 10. Crie consultas SQL analíticas

> **Crie em:** `sql/analysis.sql`

<details>
<summary><strong>Crie consultas analíticas utilizando os dados armazenados no PostgreSQL.</strong></summary>

<br />

Agora que os dados dos aeroportos já estão armazenados no PostgreSQL, você deverá criar consultas SQL que permitam analisar o dataset.
---
O objetivo desta etapa é praticar SQL utilizando dados reais e revisar conceitos importantes para Engenharia de Dados, incluindo:

- filtros;
- agregações;
- `GROUP BY`;
- `HAVING`;
- `CASE`;
- subqueries;
- CTEs;
- múltiplas CTEs;
- Window Functions;
- `PARTITION BY`;
- `ROW_NUMBER`;
- `RANK`;
- `DENSE_RANK`;
- `LAG` / `LEAD`;
- agregações como Window Functions;
- combinação de CTE + Window Function.

> ⚠️ Não utilize Pandas para responder às perguntas desta seção. As análises devem ser realizadas em SQL diretamente sobre o PostgreSQL.

---

## Consulta 1 — Quantidade de aeroportos por estado

Descubra quantos aeroportos existem em cada estado.

O resultado deverá apresentar:

```text
estado
quantidade_aeroportos
```

Ordene do estado com maior quantidade para o estado com menor quantidade.

### Conceitos trabalhados

```text
SELECT
COUNT
GROUP BY
ORDER BY
```

---

## Consulta 2 — Altitude média dos aeroportos por estado

Calcule a altitude média dos aeroportos de cada estado.

Apresente:

```text
estado
quantidade_aeroportos
altitude_media
```

Ordene os estados pela maior altitude média.

### Conceitos trabalhados

```text
COUNT
AVG
GROUP BY
ORDER BY
```

---

## Consulta 3 — Estados com vários aeroportos

Utilizando o resultado de uma agregação, retorne somente estados que possuam uma quantidade mínima de aeroportos.

Escolha e documente qual limite você utilizou.

Exemplo conceitual:

```text
Somente estados com 10 ou mais aeroportos.
```

### Conceitos trabalhados

```text
GROUP BY
COUNT
HAVING
```

### Objetivo adicional

Entenda a diferença entre:

```text
WHERE
```

e:

```text
HAVING
```

e por que `HAVING` é apropriado para filtrar o resultado de uma agregação.

---

## Consulta 4 — Classificação dos aeroportos por altitude

Crie uma classificação utilizando `CASE`.

Classifique cada aeroporto em categorias definidas por você de acordo com sua altitude.

Exemplo conceitual:

```text
airport_name | altitude | altitude_category
```

Você deverá definir e documentar os intervalos utilizados.

### Conceitos trabalhados

```text
CASE
WHEN
THEN
ELSE
END
```

---

# 🔎 SUBQUERIES

## Consulta 5 — Aeroportos acima da altitude média nacional

Descubra primeiro a altitude média considerando todos os aeroportos.

Depois retorne somente os aeroportos cuja altitude esteja acima dessa média.

Apresente pelo menos:

```text
airport_name
city
state
altitude
```

### Requisito

A média utilizada para comparação deverá ser calculada dinamicamente.

Não coloque manualmente no SQL um valor previamente calculado.

### Conceitos trabalhados

```text
Subquery
AVG
WHERE
```

---

## Consulta 6 — Aeroporto ou aeroportos de maior altitude

Encontre o maior valor de altitude existente no dataset e retorne o aeroporto associado a ele.

Sua consulta deve continuar funcionando corretamente caso dois aeroportos possuam exatamente a mesma altitude máxima.

### Conceitos trabalhados

```text
Subquery
MAX
```

---

# 🧱 CTE — Common Table Expression

## Consulta 7 — Estados com quantidade de aeroportos acima da média

Primeiro calcule:

```text
quantidade de aeroportos de cada estado
```

Depois calcule:

```text
média da quantidade de aeroportos entre os estados
```

Por fim, retorne somente os estados cuja quantidade esteja acima dessa média.

### Requisito

Utilize pelo menos uma:

```sql
WITH ...
```

### Conceitos trabalhados

```text
CTE
GROUP BY
COUNT
AVG
```

---

## Consulta 8 — Estados com altitude média acima da média nacional

Utilize uma CTE para calcular a altitude média por estado.

Depois compare a média de cada estado com a altitude média geral dos aeroportos.

Retorne somente os estados que estejam acima da média nacional.

### Conceitos trabalhados

```text
CTE
AVG
GROUP BY
Subquery ou segunda CTE
```

---

# 🧱🧱 MÚLTIPLAS CTEs

## Consulta 9 — Análise estatística dos estados

Construa uma consulta utilizando pelo menos **duas CTEs**.

Uma CTE deverá calcular estatísticas por estado, como:

```text
quantidade de aeroportos
altitude média
menor altitude
maior altitude
```

Outra CTE deverá calcular alguma referência geral do dataset.

Na consulta final, combine essas informações para responder uma pergunta analítica.

Você deverá definir e documentar a pergunta respondida.

### Conceitos trabalhados

```text
WITH
múltiplas CTEs
COUNT
AVG
MIN
MAX
```

---

# 🪟 WINDOW FUNCTIONS

## Consulta 10 — Ranking nacional de aeroportos por altitude

Crie um ranking de todos os aeroportos brasileiros utilizando a altitude.

Apresente:

```text
airport_name
state
altitude
ranking
```

O aeroporto de maior altitude deverá ocupar a primeira posição.

### Requisito

Utilize uma Window Function.

### Conceitos trabalhados

```text
RANK()
OVER()
ORDER BY
```

---

## Consulta 11 — Ranking de aeroportos dentro de cada estado

Agora o ranking deverá ser independente para cada estado.

Exemplo conceitual:

```text
Minas Gerais
1 → Aeroporto A
2 → Aeroporto B
3 → Aeroporto C

São Paulo
1 → Aeroporto D
2 → Aeroporto E
3 → Aeroporto F
```

O ranking deverá reiniciar quando o estado mudar.

### Conceitos trabalhados

```text
RANK()
OVER()
PARTITION BY
ORDER BY
```

---

## Consulta 12 — Comparando ROW_NUMBER, RANK e DENSE_RANK

Crie uma consulta que utilize simultaneamente:

```text
ROW_NUMBER()
RANK()
DENSE_RANK()
```

Utilize a altitude como critério de ordenação.

Apresente as três classificações lado a lado.

Exemplo estrutural:

```text
airport_name
altitude
row_number_position
rank_position
dense_rank_position
```

Depois analise o resultado e tente identificar o comportamento das três funções quando existem valores empatados.

### Conceitos trabalhados

```text
ROW_NUMBER()
RANK()
DENSE_RANK()
OVER()
ORDER BY
```

### Pergunta de estudo

Após executar a consulta, explique no README ou em comentários SQL:

> Qual é a diferença entre `ROW_NUMBER`, `RANK` e `DENSE_RANK` quando existem empates?

---

# 🪟 AGREGAÇÕES COMO WINDOW FUNCTIONS

## Consulta 13 — Comparação do aeroporto com a média de seu estado

Para cada aeroporto, apresente:

```text
airport_name
state
altitude
state_avg_altitude
```

A média do estado deverá aparecer ao lado de cada aeroporto **sem transformar todos os aeroportos daquele estado em uma única linha**.

### Restrição

Não resolva este requisito utilizando apenas:

```text
GROUP BY
```

### Conceitos trabalhados

```text
AVG() OVER()
PARTITION BY
```

### Objetivo de estudo

Entender a diferença entre:

```text
GROUP BY
```

que normalmente reduz várias linhas em grupos, e:

```text
Window Function
```

que pode preservar as linhas originais enquanto calcula informações sobre um conjunto delas.

---

## Consulta 14 — Quantidade de aeroportos do estado em cada registro

Para cada aeroporto, apresente também quantos aeroportos existem naquele mesmo estado.

Exemplo conceitual:

```text
airport_name | state        | airports_in_state
-------------|--------------|------------------
Aeroporto A  | Minas Gerais | 20
Aeroporto B  | Minas Gerais | 20
Aeroporto C  | São Paulo    | 30
```

### Conceitos trabalhados

```text
COUNT() OVER()
PARTITION BY
```

---

# ↔️ LAG E LEAD

## Consulta 15 — Comparação de altitude entre aeroportos consecutivos

Ordene os aeroportos pela altitude e apresente, para cada registro:

```text
airport_name
altitude
previous_airport_altitude
next_airport_altitude
```

### Conceitos trabalhados

```text
LAG()
LEAD()
OVER()
ORDER BY
```

### Objetivo de estudo

Entender como acessar valores de linhas anteriores e posteriores sem realizar `JOIN` da tabela com ela mesma.

---

## Consulta 16 — Diferença de altitude para o aeroporto anterior

Partindo da ideia da consulta anterior, calcule também a diferença entre:

```text
altitude atual
-
altitude do aeroporto anterior
```

Apresente:

```text
airport_name
altitude
previous_altitude
altitude_difference
```

### Conceitos trabalhados

```text
LAG()
Window Functions
operações aritméticas
```

---

# 🧩 CTE + WINDOW FUNCTION

## Consulta 17 — Aeroportos mais altos de cada estado

Retorne apenas os aeroportos que ocupam as primeiras posições de altitude dentro de cada estado.

Por exemplo:

```text
3 aeroportos mais altos de cada estado
```

### Requisitos

A solução deverá utilizar:

```text
CTE
+
Window Function
+
PARTITION BY
```

A quantidade de posições retornadas pode ser definida por você.

### Conceitos trabalhados

```text
WITH
RANK / DENSE_RANK / ROW_NUMBER
OVER
PARTITION BY
WHERE
```

> Pense em por que pode ser necessário calcular o ranking primeiro e filtrá-lo posteriormente.

---

## Consulta 18 — Estado de cada aeroporto comparado com o cenário nacional

Construa uma CTE contendo estatísticas por estado.

Depois utilize Window Functions ou outras operações SQL para comparar cada estado com o restante do dataset.

Sua análise deverá apresentar pelo menos:

```text
state
airports_count
avg_altitude
```

e alguma medida comparativa definida por você.

### Conceitos trabalhados

```text
CTE
GROUP BY
Window Functions
Agregações
```

---

# 🌎 ANÁLISE GEOGRÁFICA

## Consulta 19 — Extremos geográficos dos aeroportos

Utilizando:

```text
latgeopoint
longeopoint
```

determine aeroportos que representem extremos geográficos do dataset.

Investigue pelo menos dois dos seguintes:

```text
mais ao norte
mais ao sul
mais a leste
mais a oeste
```

### Conceitos trabalhados

```text
MIN
MAX
ORDER BY
LIMIT
interpretação de latitude/longitude
```

> ⚠️ Antes de implementar, pesquise e entenda como valores positivos e negativos de latitude e longitude representam posições geográficas. Não assuma que "menor número = norte" ou algo semelhante sem compreender o sistema de coordenadas.

---

# 🧠 DESAFIO FINAL — Consulta livre

## Consulta 20 — Crie sua própria análise

Agora formule uma pergunta sobre o dataset sem receber a lógica pronta.

Sua consulta deverá combinar **pelo menos três conceitos** estudados nesta etapa.

Você poderá escolher entre:

```text
GROUP BY
HAVING
CASE
Subquery
CTE
Window Function
PARTITION BY
ROW_NUMBER
RANK
DENSE_RANK
LAG
LEAD
AVG
COUNT
MIN
MAX
```

Antes da consulta, escreva um comentário contendo a pergunta que você pretende responder.

Exemplo:

```sql
-- Pergunta:
-- <escreva aqui o que você quer descobrir>

-- Consulta:
```

Não replique exatamente uma das 19 consultas anteriores.

---

# ✅ Checklist de SQL

Ao terminar esta etapa, verifique se você consegue explicar, sem apenas reproduzir o código:

- [ ] Como funciona `GROUP BY`;
- [ ] A diferença entre `WHERE` e `HAVING`;
- [ ] Como utilizar `CASE`;
- [ ] O que é uma Subquery;
- [ ] O que é uma CTE;
- [ ] Por que utilizar CTEs;
- [ ] Como utilizar múltiplas CTEs;
- [ ] O que é uma Window Function;
- [ ] Para que serve `OVER()`;
- [ ] Para que serve `PARTITION BY`;
- [ ] A diferença entre `GROUP BY` e `PARTITION BY`;
- [ ] A diferença entre `ROW_NUMBER`, `RANK` e `DENSE_RANK`;
- [ ] Como utilizar agregações como `AVG()` e `COUNT()` como Window Functions;
- [ ] Para que servem `LAG` e `LEAD`;
- [ ] Como combinar CTEs e Window Functions;
- [ ] Como utilizar SQL para responder perguntas analíticas sobre dados reais.

---

# 🗂️ Organização sugerida do `analysis.sql`

Organize seu arquivo utilizando comentários:

```sql
-- =====================================================
-- CONSULTA 01
-- Quantidade de aeroportos por estado
-- Conceitos: GROUP BY, COUNT, ORDER BY
-- =====================================================

-- implementação


-- =====================================================
-- CONSULTA 02
-- Altitude média por estado
-- Conceitos: AVG, GROUP BY
-- =====================================================

-- implementação


-- =====================================================
-- CONSULTA 03
-- Estados com vários aeroportos
-- Conceitos: HAVING
-- =====================================================

-- implementação
```

Continue seguindo o mesmo padrão para as demais consultas.

---

# 🎯 Critério de conclusão

Esta etapa não será considerada concluída apenas porque as consultas executam sem erros.

Você deverá conseguir explicar:

```text
O que a consulta responde?

Por que escolheu essa abordagem?

Em qual ordem lógica as operações acontecem?

Por que uma CTE ou Subquery foi utilizada?

Por que GROUP BY ou PARTITION BY foi utilizado?

O que a Window Function está calculando?

O que aconteceria se existissem empates?
```

O objetivo é sair desta etapa sabendo **construir e interpretar SQL analítico**, e não apenas copiar sua sintaxe.

---

# 🧩 Orquestração

O arquivo:

```text
main.py
```

deverá funcionar como ponto de entrada do pipeline.

Conceitualmente:

```text
main
 │
 ├── Extract
 │
 ├── Transform
 │
 └── Load
```

Evite concentrar dentro da `main` toda a lógica de:

- requisições;
- transformação;
- validação;
- SQL;
- escrita de arquivos.

A função principal deve principalmente **orquestrar as etapas**.

---

# 🧪 Validação final do projeto

Quando acreditar que terminou, execute o seguinte teste manual.

## Primeira execução

```bash
python main.py
```

Verifique:

```text
✓ dados foram extraídos
✓ Raw foi gerada
✓ registros foram transformados
✓ inválidos foram separados
✓ CSV Processed foi criado
✓ dados chegaram ao PostgreSQL
✓ logs foram gerados
```

Consulte o banco:

```sql
SELECT COUNT(*)
FROM sua_tabela;
```

Anote a quantidade.

## Segunda execução

Execute novamente:

```bash
python main.py
```

Consulte:

```sql
SELECT COUNT(*)
FROM sua_tabela;
```

A execução não deverá criar duplicações.

---

# 🔍 Testes de Data Quality

Não dependa somente dos dados reais da fonte para descobrir se sua validação funciona.

Crie testes controlados durante o desenvolvimento com situações como:

```text
airport_id = None

airport_name = ""

state_code = "XX"

latitude = None

longitude = None

latitude = "ABC"
```

Confirme que os registros são rejeitados e que o restante do lote continua sendo processado.

Esses dados artificiais são para **testar sua implementação**, não para substituir a fonte real do pipeline.

---

# 📊 Critérios de conclusão

O projeto será considerado concluído quando:

- [ ] uma fonte pública real estiver sendo utilizada;
- [ ] a etapa Extract estiver funcionando;
- [ ] os dados Raw estiverem sendo preservados;
- [ ] a transformação gerar o schema esperado;
- [ ] Data Quality estiver implementada;
- [ ] registros inválidos forem armazenados em Rejected;
- [ ] registros válidos forem gravados em CSV;
- [ ] PostgreSQL estiver configurado;
- [ ] a tabela possuir proteção contra duplicações;
- [ ] a etapa Load estiver funcionando;
- [ ] duas execuções consecutivas não duplicarem dados;
- [ ] logging estiver funcionando;
- [ ] existirem pelo menos cinco consultas analíticas;
- [ ] `requirements.txt` estiver correto;
- [ ] `.gitignore` não permitir dados sensíveis ou arquivos desnecessários;
- [ ] README final documentar arquitetura, fonte e decisões;
- [ ] o projeto estiver versionado no Git.

---

# 🧠 O que você pode pesquisar?

Este é um exercício de Engenharia de Dados, não um teste de memorização.

Você **pode e deve pesquisar**:

- documentação oficial;
- sintaxe Python;
- sintaxe SQL;
- documentação PostgreSQL;
- funcionamento das bibliotecas;
- mensagens de erro;
- formas de consumir a fonte escolhida;
- Pandas;
- boas práticas.

Pandas também é permitido como ferramenta auxiliar.

Entretanto, tente não transformar o exercício inteiro em uma sequência como:

```python
df = pd.read_csv(...)
df.dropna(...)
df.to_sql(...)
```

O objetivo é praticar explicitamente:

```text
Extract
Transform
Data Quality
Rejected Records
CSV
Load
PostgreSQL
Idempotência
SQL
Logging
```

Se Pandas esconder completamente esses conceitos, você estará deixando de praticar justamente o que o projeto pretende avaliar.

---

# 🆘 Como pedir ajuda durante o projeto

Quando encontrar um problema, envie:

```text
1. O requisito em que está trabalhando
2. O código que você escreveu
3. O comportamento esperado
4. O comportamento obtido
5. O erro completo, caso exista
```

Durante este exercício, a ajuda deverá priorizar:

```text
entender o problema
       ↓
identificar onde investigar
       ↓
formular hipóteses
       ↓
corrigir sua própria implementação
```

em vez de simplesmente fornecer a solução completa.

---

# ⭐ Bônus — somente depois dos requisitos obrigatórios

Depois que o projeto estiver completamente funcional, você pode adicionar melhorias opcionais.

Algumas possibilidades:

- testes automatizados com `pytest`;
- Docker Compose para PostgreSQL;
- validação adicional de coordenadas geográficas;
- timestamps de criação/atualização;
- execução via CLI;
- mais consultas SQL;
- geração de relatório analítico;
- CI com GitHub Actions.

> Os bônus não substituem nenhum requisito obrigatório.

---

# 🚀 Fluxo esperado ao final

```text
                    ┌───────────────────────┐
                    │ Fonte pública de dados│
                    └───────────┬───────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │   Extract   │
                         └──────┬──────┘
                                │
                                ▼
                         data/raw/*.json
                                │
                                ▼
                         ┌─────────────┐
                         │  Transform  │
                         └──────┬──────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
               Dados válidos          Dados inválidos
                    │                       │
                    ▼                       ▼
          data/processed/*.csv    data/rejected/*.json
                    │
                    ▼
                         ┌─────────────┐
                         │    Load     │
                         └──────┬──────┘
                                │
                                ▼
                           PostgreSQL
                                │
                                ▼
                        sql/analysis.sql
```

---

# 👨‍💻 Projeto de avaliação prática

Este projeto faz parte da trilha prática de estudos em **Engenharia de Dados**.

A proposta é implementar o pipeline de forma autônoma, utilizando os projetos anteriores como referência conceitual, mas tomando as próprias decisões de implementação.

**Boa implementação! 🚀**
