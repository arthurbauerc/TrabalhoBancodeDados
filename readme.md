# Sistema de Gerenciamento de Eventos Acadêmicos

Este projeto implementa um sistema completo de gerenciamento de eventos
acadêmicos com integração a banco de dados MySQL, consultas SQL
avançadas, geração de gráficos estatísticos e uso de Inteligência
Artificial Generativa para análise automática dos dados.

## 1. Objetivo Geral

Desenvolver uma aplicação acadêmica robusta que: - Gerencie entidades
como usuários, instituições, professores, alunos, edições, projetos e
avaliações. - Execute operações CRUD completas. - Gere gráficos
analíticos baseados nos dados do evento. - Utilize IA para sintetizar
relatórios inteligentes a partir do banco de dados.

## 2. Tecnologias Utilizadas

-   **Python 3**
-   **MySQL 8**
-   **mysql-connector-python** para integração com o banco
-   **Matplotlib** para geração de gráficos
-   **python-dotenv** para carregamento seguro de variáveis de ambiente
-   **OpenAI API (GPT-4o-mini)** para análise avançada com IA
-   **Pypandoc** para conversão e geração do arquivo README

## 3. Estrutura do Banco de Dados

A aplicação cria automaticamente tabelas estruturadas para: -
Instituições - Usuários - Professores, Alunos, Avaliadores - Edições de
eventos - Áreas temáticas - Projetos (Full Papers, Short Papers) -
Avaliações - Relações entre entidades

Todas as tabelas incluem chaves primárias, estrangeiras, índices e
regras de integridade referencial.

## 4. Funcionalidades Principais

### 4.1 CRUD Completo

O sistema implementa: - Criação estruturada de todas as tabelas -
Inserção de dados fictícios bem construídos - Atualizações automáticas e
manuais com validação - Remoção automática e manual com segurança - Drop
completo do banco para reinicialização

### 4.2 Consultas SQL Avançadas

Inclui consultas para: - Quantidade de projetos por área temática e
edição - Média de pontuação dos projetos por professor - Distribuição
institucional de submissões - Comparação entre Full Papers e Short
Papers

Todas acompanhadas por **gráficos profissionais** gerados via
Matplotlib.

### 4.3 Inteligência Artificial

O sistema integra IA generativa para: - Ler dados do banco - Produzir
relatórios acadêmicos técnicos e detalhados - Analisar tendências,
padrões e recomendações

### 4.4 Segurança e Boas Práticas

-   Uso de `.env` para armazenar API Key
-   Validação robusta nas operações manuais (inserção, atualização,
    remoção)
-   Prevenção de SQL Injection no uso interativo

## 5. Execução do Projeto

### 5.1 Instalar Dependências

    pip install mysql-connector-python matplotlib python-dotenv openai pypandoc

### 5.2 Configurar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

    OPENAI_API_KEY=sua_chave

### 5.3 Configurar Banco de Dados MySQL

Criar o banco:

    CREATE DATABASE eventos_academicos;

### 5.4 Executar o Sistema

    python ResgateAnimais.py

## 6. Navegação pelo Menu

O sistema oferece:

-   CRUD completo
-   Inserção manual segura
-   Remoção manual segura
-   Atualização segura
-   Consultas SQL (4 opções)
-   Geração de gráficos analíticos
-   Relatório por IA
-   Visualização de tabelas

## 7. Resultados Esperados

O projeto proporciona: - Organização eficiente de informações
acadêmicas - Análises estatísticas úteis para comitês científicos -
Relatórios inteligentes gerados automaticamente - Visualização clara e
objetiva dos dados

## 8. Conclusão

Este sistema atende aos requisitos acadêmicos e demonstra o uso
integrado de bancos relacionais, análise de dados, visualização gráfica
e inteligência artificial --- oferecendo uma plataforma abrangente e
moderna para gestão de eventos científicos.
