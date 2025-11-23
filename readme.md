# Sistema de Gerenciamento de Eventos Cientificos (GECi)

**Universidade Federal de Santa Catarina (UFSC) - Campus Araranguá**

**Disciplina:** DEC7588 - Banco de Dados (2025.2)

**Professor:** Dr. Alexandre Leopoldo Gonçalves

---

**Equipe de Desenvolvimento:**
* **Arthur Bauer Cardoso** (Matrícula: 24103788)
* **Diva Moreira de Souza Hennemann** (Matrícula: 24102022)
* **Luís Antônio Scarabelot Fiabani** (Matrícula: 24102006)

---

## 1. Introdução e Objetivos

Este projeto consiste no desenvolvimento de uma aplicação voltada ao domínio de **Gerenciamento de Eventos Científicos**, elaborada como requisito parcial para aprovação na disciplina de Banco de Dados.

O objetivo principal é a aplicação prática dos fundamentos de projeto e implementação de bancos de dados relacionais. O sistema foi projetado para gerenciar o fluxo de informações de um evento científico, contemplando o cadastro de instituições, a gestão de usuários (professores, alunos e avaliadores), a submissão de projetos (artigos completos e resumos) e o processo de avaliação.

Além das operações transacionais padrão, o sistema integra funcionalidades de análise de dados com visualização gráfica e recursos de Inteligência Artificial Generativa para auxílio na tomada de decisão.

## 2. Tecnologias e Ferramentas Utilizadas

A arquitetura do sistema foi construída utilizando as seguintes tecnologias:

* **Linguagem de Programação:** Python 3.
* **Sistema Gerenciador de Banco de Dados (SGBD):** MySQL 8.0.
* **Interface de Conexão:** Biblioteca `mysql-connector-python`.
* **Visualização de Dados:** Biblioteca `Matplotlib` para geração de gráficos estatísticos.
* **Inteligência Artificial:** Integração com APIs de LLMs (OpenAI GPT e Google Gemini) para processamento de linguagem natural.
* **Segurança e Configuração:** Biblioteca `python-dotenv` para gerenciamento de variáveis de ambiente sensíveis.

## 3. Arquitetura do Banco de Dados

O projeto de banco de dados foi estruturado seguindo as etapas rigorosas de modelagem conceitual e lógica, garantindo a normalização e integridade referencial dos dados. O esquema relacional abrange as seguintes macro-entidades:

1.  **Institucional:** Tabelas dedicadas a *Instituições* e *Áreas Temáticas*.
2.  **Atores:** Gerenciamento de *Usuários*, com especialização para *Professores*, *Alunos* e *Avaliadores*.
3.  **Produção Acadêmica:** Controle de *Edições* do evento, *Projetos* (classificados em *Full Papers* e *Short Papers*) e registros de *Avaliações*.

O script DDL (*Data Definition Language*) implementa todas as chaves primárias, chaves estrangeiras e índices necessários para a consistência do modelo.

## 4. Funcionalidades do Sistema

Em conformidade com os requisitos especificados para o Trabalho Final, a aplicação oferece:

### 4.1. Gestão de Dados e Operações DML
O sistema implementa um módulo principal que permite a execução de operações de manipulação de dados (*Data Manipulation Language* - DML):
* **Inicialização (Seed):** Funcionalidade para criação automática da estrutura do banco e povoamento com dados iniciais, permitindo a validação imediata das regras de negócio.
* **Reinicialização do Ambiente:** Opção para exclusão total das tabelas (*Drop Tables*) para testes de integridade.
* **CRUD Transacional:** Interfaces para Inserção, Atualização e Exclusão de registros em todas as tabelas do modelo, com tratamento de dependências.

### 4.2. Relatórios Gerenciais e Visualização Gráfica
Foram desenvolvidas consultas SQL complexas, utilizando junções (*JOINs*) entre múltiplas tabelas e funções de agregação (*SUM, AVG, COUNT*). As análises disponíveis incluem:

1.  **Distribuição Temática:** Quantitativo de projetos submetidos por Área Temática e Edição do evento.
2.  **Desempenho de Orientação:** Média de pontuação dos projetos agrupada por Professor Orientador.
3.  **Origem das Submissões:** Volume de trabalhos submetidos segregado por Instituição.
4.  **Tipologia de Projetos:** Comparativo quantitativo entre as categorias *Full Papers* e *Short Papers*.

Para cada consulta, o sistema apresenta o resultado tabular (SQL) e gera automaticamente a representação gráfica correspondente via `Matplotlib`.

### 4.3. Módulo de Inteligência Artificial Generativa
O sistema demonstra a integração com conceitos de IA Generativa para:
* Realizar a leitura contextual dos dados armazenados no banco.
* Gerar relatórios técnicos automatizados.
* Fornecer análises de tendências e recomendações baseadas nos dados do evento.

## 5. Instruções de Instalação e Execução

Para a correta execução da aplicação, siga os passos abaixo:

### 5.1. Pré-requisitos
* Python 3.x instalado.
* Servidor MySQL 8.0 em execução.

### 5.2. Instalação das Dependências
Execute o comando abaixo no terminal para instalar as bibliotecas necessárias:

```bash
pip install mysql-connector-python matplotlib python-dotenv openai google-generativeai pypandoc
```

### 5.3. Configuração de Ambiente (.env)
Crie um arquivo .env na raiz do projeto contendo as credenciais de acesso ao banco e as chaves de API para os serviços de IA:

```bash
OPENAI_API_KEY=sua_chave_openai
GOOGLE_API_KEY=sua_chave_gemini
GPT_MODEL=gpt-4o-mini
GEMINI_MODEL=gemini-2.5-flash
DB_USER=seu_usuario_mysql
DB_PASS=sua_senha_mysql
```

### 5.4. Configurar Banco de Dados MySQL
Criar o banco:
```bash
CREATE DATABASE eventos_academicos;
```

### 5.5. Execução da Aplicação
Para iniciar o sistema, execute o arquivo principal:

```bash
python main.py
```