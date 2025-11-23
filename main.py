#pip install mysql-connector-python
#pip install matplotlib
#pip install openai
#pip install python-dotenv
#pip install google-generativeai

import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from openai import OpenAI
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
genai.configure(api_key=GEMINI_API_KEY)


# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {
    'INSTITUICAO': (
        """CREATE TABLE `Instituicao` (
            `id_instituicao` INTEGER PRIMARY KEY NOT NULL,
            `nome` VARCHAR(100) NOT NULL,
            `endereco` VARCHAR(100)
        ) ENGINE=InnoDB"""
    ),
    'USUARIO': (
        """CREATE TABLE `Usuario` (
            `id_usuario` INTEGER PRIMARY KEY NOT NULL,
            `nome` VARCHAR(100) NOT NULL,
            `email` VARCHAR(100) UNIQUE NOT NULL,
            `senha` VARCHAR(100) NOT NULL,
            `fk_id_instituicao` INTEGER,
            FOREIGN KEY (`fk_id_instituicao`) REFERENCES `Instituicao`(`id_instituicao`)
        ) ENGINE=InnoDB"""
    ),
    'ALUNO': (
        """CREATE TABLE `Aluno` (
            `id_aluno` INTEGER PRIMARY KEY NOT NULL,
            FOREIGN KEY (`id_aluno`) REFERENCES `Usuario`(`id_usuario`) ON DELETE CASCADE
        ) ENGINE=InnoDB"""
    ),
    'PROFESSOR': (
        """CREATE TABLE `Professor` (
            `id_professor` INTEGER PRIMARY KEY NOT NULL,
            FOREIGN KEY (`id_professor`) REFERENCES `Usuario`(`id_usuario`) ON DELETE CASCADE
        ) ENGINE=InnoDB"""
    ),
    'AVALIADOR': (
        """CREATE TABLE `Avaliador` (
            `id_avaliador` INTEGER PRIMARY KEY NOT NULL,
            FOREIGN KEY (`id_avaliador`) REFERENCES `Usuario`(`id_usuario`) ON DELETE CASCADE
        ) ENGINE=InnoDB"""
    ),
    'EDICAO': (
        """CREATE TABLE `Edicao` (
            `id_edicao` INTEGER PRIMARY KEY NOT NULL,
            `nome` VARCHAR(100),
            `data_inicio` TIMESTAMP,
            `data_fim` TIMESTAMP,
            `data_limite_submissao` TIMESTAMP,
            `local` VARCHAR(100),
            `status_edicao` VARCHAR(50)
        ) ENGINE=InnoDB"""
    ),
    'AREA_TEMATICA': (
        """CREATE TABLE `Area_Tematica` (
            `id_area_tematica` INTEGER PRIMARY KEY NOT NULL,
            `descricao` VARCHAR(100) NOT NULL,
            `fk_id_edicao` INTEGER NOT NULL,
            FOREIGN KEY (`fk_id_edicao`) REFERENCES `Edicao`(`id_edicao`)
        ) ENGINE=InnoDB"""
    ),
    'PROJETO': (
        """CREATE TABLE `Projeto` (
            `id_projeto` INTEGER PRIMARY KEY NOT NULL,
            `titulo` VARCHAR(200),
            `resumo` TEXT,
            `status` VARCHAR(50),
            `data_submissao` TIMESTAMP,
            `caminho_arquivo` TEXT,
            `descricao` TEXT,
            `fk_id_professor` INTEGER NOT NULL,
            `fk_id_area_tematica` INTEGER NOT NULL,
            `fk_id_edicao` INTEGER NOT NULL,
            FOREIGN KEY (`fk_id_professor`) REFERENCES `Professor`(`id_professor`),
            FOREIGN KEY (`fk_id_area_tematica`) REFERENCES `Area_Tematica`(`id_area_tematica`),
            FOREIGN KEY (`fk_id_edicao`) REFERENCES `Edicao`(`id_edicao`)
        ) ENGINE=InnoDB"""
    ),
    'FULL_PAPER': (
        """CREATE TABLE `Full_Paper` (
            `id_projeto` INTEGER PRIMARY KEY NOT NULL,
            FOREIGN KEY (`id_projeto`) REFERENCES `Projeto`(`id_projeto`) ON DELETE CASCADE
        ) ENGINE=InnoDB"""
    ),
    'SHORT_PAPER': (
        """CREATE TABLE `Short_Paper` (
            `id_projeto` INTEGER PRIMARY KEY NOT NULL,
            FOREIGN KEY (`id_projeto`) REFERENCES `Projeto`(`id_projeto`) ON DELETE CASCADE
        ) ENGINE=InnoDB"""
    ),
    'ALUNO_PROJETO': (
        """CREATE TABLE `Aluno_Projeto` (
            `id_aluno` INTEGER NOT NULL,
            `id_projeto` INTEGER NOT NULL,
            PRIMARY KEY (`id_aluno`, `id_projeto`),
            FOREIGN KEY (`id_aluno`) REFERENCES `Aluno`(`id_aluno`),
            FOREIGN KEY (`id_projeto`) REFERENCES `Projeto`(`id_projeto`)
        ) ENGINE=InnoDB"""
    ),
    'USUARIO_EDICAO': (
        """CREATE TABLE `Usuario_Edicao` (
            `id_usuario` INTEGER NOT NULL,
            `id_edicao` INTEGER NOT NULL,
            PRIMARY KEY (`id_usuario`, `id_edicao`),
            FOREIGN KEY (`id_usuario`) REFERENCES `Usuario`(`id_usuario`),
            FOREIGN KEY (`id_edicao`) REFERENCES `Edicao`(`id_edicao`)
        ) ENGINE=InnoDB"""
    ),
    'AVALIACAO': (
        """CREATE TABLE `Avaliacao` (
            `id_avaliador` INTEGER NOT NULL,
            `id_projeto` INTEGER NOT NULL,
            `comentarios_correcao` TEXT,
            `parecer_final` TEXT,
            `data_avaliacao` TIMESTAMP,
            `pontuacao` INTEGER,
            PRIMARY KEY (`id_avaliador`, `id_projeto`),
            FOREIGN KEY (`id_avaliador`) REFERENCES `Avaliador`(`id_avaliador`),
            FOREIGN KEY (`id_projeto`) REFERENCES `Projeto`(`id_projeto`)
        ) ENGINE=InnoDB"""
    ),
}

# Valores para serem inseridos no Banco de Dados
inserts = {
    'INSTITUICAO': (
        """INSERT INTO Instituicao (id_instituicao, nome, endereco) VALUES
        (1, 'UFSC - Campus Araranguá', 'Araranguá - SC'),
        (2, 'IFSC - Campus Araranguá', 'Araranguá - SC')"""
    ),
    'USUARIO': (
        """INSERT INTO Usuario (id_usuario, nome, email, senha, fk_id_instituicao) VALUES
        (1, 'Alice Aluna', 'alice@ufsc.br', '123456', 1),
        (2, 'Bruno Aluno', 'bruno@ufsc.br', '123456', 1),
        (3, 'Carlos Professor', 'carlos.prof@ufsc.br', '123456', 1),
        (4, 'Daniela Professora', 'daniela.prof@ifsc.edu.br', '123456', 2),
        (5, 'Eduardo Avaliador', 'eduardo.av@ufsc.br', '123456', 1),
        (6, 'Fernanda Avaliadora', 'fernanda.av@ifsc.edu.br', '123456', 2)"""
    ),
    'ALUNO': (
        """INSERT INTO Aluno (id_aluno) VALUES
        (1),
        (2)"""
    ),
    'PROFESSOR': (
        """INSERT INTO Professor (id_professor) VALUES
        (3),
        (4)"""
    ),
    'AVALIADOR': (
        """INSERT INTO Avaliador (id_avaliador) VALUES
        (5),
        (6)"""
    ),
    'EDICAO': (
        """INSERT INTO Edicao (id_edicao, nome, data_inicio, data_fim, data_limite_submissao, local, status_edicao) VALUES
        (1, 'SEPEI 2025', '2025-06-10 00:00:00', '2025-06-12 23:59:59', '2025-05-10 23:59:59', 'Araranguá', 'Submissões encerradas'),
        (2, 'Mostra Integrada 2025', '2025-10-01 00:00:00', '2025-10-03 23:59:59', '2025-09-10 23:59:59', 'Araranguá', 'Em submissão')"""
    ),
    'AREA_TEMATICA': (
        """INSERT INTO Area_Tematica (id_area_tematica, descricao, fk_id_edicao) VALUES
        (1, 'Engenharia de Software', 1),
        (2, 'Inteligência Artificial', 1),
        (3, 'Educação em Computação', 2)"""
    ),
    'PROJETO': (
        """INSERT INTO Projeto (id_projeto, titulo, resumo, status, data_submissao, caminho_arquivo, descricao,
                                fk_id_professor, fk_id_area_tematica, fk_id_edicao) VALUES
        (1, 'Plataforma Mentorar', 'Sistema web para mentoria acadêmica.', 'Submetido',
         '2025-04-20 10:00:00', '/uploads/mentorar.pdf', 'Projeto de apoio à permanência estudantil.',
         3, 1, 1),
        (2, 'Análise de Dados de Evasão', 'Estudo de evasão em cursos de TIC.', 'Aprovado',
         '2025-04-25 14:30:00', '/uploads/evasao.pdf', 'Projeto com foco em mineração de dados educacionais.',
         3, 2, 1),
        (3, 'Gamificação no Ensino de BD', 'Uso de jogos na disciplina de Banco de Dados.', 'Submetido',
         '2025-09-01 09:15:00', '/uploads/gamificacao.pdf', 'Projeto com recursos lúdicos em sala de aula.',
         4, 3, 2)"""
    ),
    'FULL_PAPER': (
        """INSERT INTO Full_Paper (id_projeto) VALUES
        (1),
        (2)"""
    ),
    'SHORT_PAPER': (
        """INSERT INTO Short_Paper (id_projeto) VALUES
        (3)"""
    ),
    'ALUNO_PROJETO': (
        """INSERT INTO Aluno_Projeto (id_aluno, id_projeto) VALUES
        (1, 1),
        (2, 1),
        (1, 2),
        (2, 3)"""
    ),
    'USUARIO_EDICAO': (
        """INSERT INTO Usuario_Edicao (id_usuario, id_edicao) VALUES
        (1, 1),
        (2, 1),
        (3, 1),
        (5, 1),
        (1, 2),
        (4, 2),
        (6, 2)"""
    ),
    'AVALIACAO': (
        """INSERT INTO Avaliacao (id_avaliador, id_projeto, comentarios_correcao, parecer_final, data_avaliacao, pontuacao) VALUES
        (5, 1, 'Bom escopo e boa escrita.', 'Aprovado com ajustes.', '2025-05-20 15:00:00', 9),
        (6, 1, 'Metodologia clara, mas faltam detalhes.', 'Aprovado.', '2025-05-21 10:30:00', 8),
        (5, 2, 'Resultados relevantes.', 'Aprovado.', '2025-05-22 16:45:00', 8),
        (6, 2, 'Boa fundamentação teórica.', 'Aprovado.', '2025-05-23 11:10:00', 7),
        (5, 3, 'Ideia inovadora para ensino de BD.', 'Recomendado para apresentação.', '2025-10-01 09:00:00', 9)"""
    ),
}

# Valores para deletar as tabelas
drop = {
    'AVALIACAO': "DROP TABLE Avaliacao",
    'USUARIO_EDICAO': "DROP TABLE Usuario_Edicao",
    'ALUNO_PROJETO': "DROP TABLE Aluno_Projeto",
    'SHORT_PAPER': "DROP TABLE Short_Paper",
    'FULL_PAPER': "DROP TABLE Full_Paper",
    'PROJETO': "DROP TABLE Projeto",
    'AREA_TEMATICA': "DROP TABLE Area_Tematica",
    'EDICAO': "DROP TABLE Edicao",
    'AVALIADOR': "DROP TABLE Avaliador",
    'PROFESSOR': "DROP TABLE Professor",
    'ALUNO': "DROP TABLE Aluno",
    'USUARIO': "DROP TABLE Usuario",
    'INSTITUICAO': "DROP TABLE Instituicao",
}

# Valores para teste de update
update = {
    'USUARIO': (
        """UPDATE Usuario
           SET nome = 'Alice A. Cardoso'
           WHERE id_usuario = 1"""
    ),
    'PROJETO': (
        """UPDATE Projeto
           SET status = 'Avaliado'
           WHERE id_projeto = 3"""
    ),
    'AVALIACAO': (
        """UPDATE Avaliacao
           SET pontuacao = 10
           WHERE id_avaliador = 5 AND id_projeto = 3"""
    ),
}

# Valores para teste de delete
delete = {
    'AVALIACAO': (
        """DELETE FROM Avaliacao
           WHERE id_avaliador = 6 AND id_projeto = 2"""
    ),
    'USUARIO_EDICAO': (
        """DELETE FROM Usuario_Edicao
           WHERE id_usuario = 2 AND id_edicao = 1"""
    ),
}


def connect_sistemaEventos():
    cnx = mysql.connector.connect(
        host='localhost',
        database='eventos_academicos',
        user='root',
        password='Awds0705@'
    )
    if cnx.is_connected():
        db_info = cnx.server_info
        print("Conectado ao servidor MySQL versão", db_info)
        cursor = cnx.cursor()
        cursor.execute("SELECT DATABASE();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados", linha)
        cursor.close()
    return cnx


def drop_all_tables(connect):
    print("\n---DROP DB---")
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Drop {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome:", table_name)
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar: ")).upper()
        if name not in tables:
            print("Tabela inválida.")
            cursor.close()
            return
        real_name = name.title().replace("_", "_")
        select = "SELECT * FROM " + real_name
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA", real_name)
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()


def update_value(connect):
    print("\n--- ATUALIZAÇÃO SEGURA ---")
    cursor = connect.cursor()

    # Mostrar as tabelas disponíveis
    print("Tabelas disponíveis:")
    for table_name in tables:
        print(" -", table_name)

    name = input("\nDigite o nome da tabela para atualizar: ").upper()

    if name not in tables:
        print("Erro: tabela inválida.")
        cursor.close()
        return

    real_name = name.title().replace("_", "_")

    # Buscar colunas da tabela
    cursor.execute(f"SHOW COLUMNS FROM {real_name}")
    columns = [col[0] for col in cursor.fetchall()]

    print("\nColunas disponíveis na tabela:")
    for col in columns:
        print(" -", col)

    atributo = input("\nDigite o atributo a ser alterado: ")

    if atributo not in columns:
        print("Erro: coluna inválida.")
        cursor.close()
        return

    valor = input("Digite o novo valor (use aspas para texto): ")

    chave = input("Digite a coluna da condição (WHERE): ")

    if chave not in columns:
        print("Erro: coluna da condição inválida.")
        cursor.close()
        return

    valor_chave = input("Digite o valor da condição (use aspas para texto): ")

    if valor_chave.strip() == "":
        print("Erro: valor da condição vazio. Atualização cancelada.")
        cursor.close()
        return

    sql = f"""
        UPDATE {real_name}
        SET {atributo} = {valor}
        WHERE {chave} = {valor_chave}
    """

    confirm = input(f"\nCONFIRMAR UPDATE? (s/n)\n{sql}\n> ").lower()
    if confirm != "s":
        print("Operação cancelada.")
        cursor.close()
        return

    try:
        cursor.execute(sql)
        connect.commit()
        print("Registro atualizado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro MySQL:", err.msg)

    cursor.close()



def insert_test(connect):
    print("\n---INSERT TEST---")
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def update_test(connect):
    print("\n---UPDATE TEST---")
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
            cursor.execute(update_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def delete_test(connect):
    print("\n---DELETE TEST---")
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print("Teste de exclusão de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def insert_manual(connect):
    print("\n--- INSERÇÃO MANUAL SEGURA ---")
    cursor = connect.cursor()

    print("\nTabelas disponíveis:")
    for table_name in tables:
        print(" -", table_name)

    name = input("\nDigite o nome da tabela onde deseja inserir: ").upper()

    if name not in tables:
        print("Erro: tabela inválida.")
        cursor.close()
        return

    real_name = name.title().replace("_", "_")

    cursor.execute(f"SHOW COLUMNS FROM {real_name}")
    columns_data = cursor.fetchall()
    columns = [c[0] for c in columns_data]

    print("\nColunas da tabela:")
    for col in columns_data:
        col_name = col[0]
        not_null = "NOT NULL" if col[2] == "NO" else "NULL"
        print(f" - {col_name} ({not_null})")

    print("\nDigite os valores para cada coluna (deixe vazio para NULL se permitido).")

    values = {}
    for col in columns_data:
        nome_coluna = col[0]
        nulo_permitido = (col[2] == "YES")
        valor = input(f"{nome_coluna}: ")

        if valor.strip() == "" and nulo_permitido:
            values[nome_coluna] = "NULL"
        elif valor.strip() == "" and not nulo_permitido:
            print(f"Erro: a coluna {nome_coluna} é NOT NULL. Inserção cancelada.")
            cursor.close()
            return
        else:
            if valor.replace(".", "", 1).isdigit():
                values[nome_coluna] = valor
            else:
                values[nome_coluna] = f"'{valor}'"

    colunas_sql = ", ".join(values.keys())
    valores_sql = ", ".join(values.values())

    sql = f"INSERT INTO {real_name} ({colunas_sql}) VALUES ({valores_sql})"

    print("\nSQL gerado:")
    print(sql)

    confirm = input("Confirmar inserção? (s/n): ").lower()
    if confirm != "s":
        print("Operação cancelada.")
        cursor.close()
        return

    try:
        cursor.execute(sql)
        connect.commit()
        print("Registro inserido com sucesso!")
    except mysql.connector.Error as err:
        print("Erro MySQL:", err.msg)

    cursor.close()

def delete_manual(connect):
    print("\n--- DELETE MANUAL SEGURO ---")
    cursor = connect.cursor()

    print("Tabelas disponíveis:")
    for table_name in tables:
        print(" -", table_name)

    name = input("\nDigite o nome da tabela onde deseja deletar: ").upper()

    if name not in tables:
        print("Erro: tabela inválida.")
        cursor.close()
        return

    real_name = name.title().replace("_", "_")

    cursor.execute(f"SHOW COLUMNS FROM {real_name}")
    columns = [col[0] for col in cursor.fetchall()]

    print("\nColunas disponíveis para filtro:")
    for col in columns:
        print(" -", col)

    coluna = input("\nDigite o nome da coluna da condição (WHERE): ")

    if coluna not in columns:
        print("Erro: coluna inválida.")
        cursor.close()
        return

    valor = input("Digite o valor da condição (use aspas se for texto): ").strip()

    if valor == "":
        print("Erro: valor da condição vazio. Operação cancelada.")
        cursor.close()
        return

    sql = f"DELETE FROM {real_name} WHERE {coluna} = {valor}"

    print("\nSQL gerado:")
    print(sql)

    confirm = input("Confirmar exclusão? (s/n): ").lower()
    if confirm != "s":
        print("Operação cancelada.")
        cursor.close()
        return

    try:
        cursor.execute(sql)
        connect.commit()
        print("Registro deletado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro MySQL:", err.msg)

    cursor.close()

def consulta1(connect):
    select_query = """
    SELECT
        e.nome AS edicao,
        a.descricao AS area_tematica,
        COUNT(p.id_projeto) AS total_projetos
    FROM Edicao e
    INNER JOIN Area_Tematica a ON a.fk_id_edicao = e.id_edicao
    INNER JOIN Projeto p ON p.fk_id_area_tematica = a.id_area_tematica
    GROUP BY e.nome, a.descricao
    ORDER BY e.nome, a.descricao
    """

    print("\nConsulta 01: Quantidade de projetos por área temática em cada edição.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    rows = cursor.fetchall()

    print("Edição | Área Temática | Total de Projetos")
    for r in rows:
        print(r)

    edicoes = [f"{r[0]} - {r[1]}" for r in rows]
    totais = [r[2] for r in rows]

    plt.figure(figsize=(12, 5))
    plt.bar(edicoes, totais)
    plt.xticks(rotation=45, ha='right')
    plt.title("Projetos por Área Temática / Edição")
    plt.xlabel("Área Temática por Edição")
    plt.ylabel("Total de Projetos")

    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

    cursor.close()



def consulta2(connect):
    select_query = """
    SELECT
        p.id_projeto,
        p.titulo,
        u.nome AS professor,
        AVG(av.pontuacao) AS media_pontuacao
    FROM Projeto p
    INNER JOIN Professor pr ON p.fk_id_professor = pr.id_professor
    INNER JOIN Usuario u ON pr.id_professor = u.id_usuario
    INNER JOIN Avaliacao av ON av.id_projeto = p.id_projeto
    GROUP BY p.id_projeto, p.titulo, u.nome
    ORDER BY media_pontuacao DESC
    """

    print("\nConsulta 02: Média das pontuações dos projetos por professor orientador.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    rows = cursor.fetchall()

    print("ID Projeto | Título | Professor | Média de Pontuação")
    for r in rows:
        print(r)

    projetos = [f"{r[0]} - {r[1]}" for r in rows]
    medias = [float(r[3]) for r in rows]

    plt.figure(figsize=(12, 5))
    plt.barh(projetos, medias)
    plt.title("Média das Avaliações por Projeto")
    plt.xlabel("Média da Pontuação")
    plt.ylabel("Projetos")

    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

    cursor.close()


def consulta3(connect):
    select_query = """
    SELECT
        i.nome AS instituicao,
        COUNT(p.id_projeto) AS total_projetos
    FROM Instituicao i
    INNER JOIN Usuario u ON u.fk_id_instituicao = i.id_instituicao
    INNER JOIN Professor pr ON pr.id_professor = u.id_usuario
    INNER JOIN Projeto p ON p.fk_id_professor = pr.id_professor
    GROUP BY i.nome
    ORDER BY total_projetos DESC
    """

    print("\nConsulta 03: Total de projetos submetidos por instituição do professor orientador.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    rows = cursor.fetchall()

    print("Instituição | Total de Projetos")
    for r in rows:
        print(r)

    instituicoes = [r[0] for r in rows]
    totais = [int(r[1]) for r in rows]  # Garantir inteiros

    plt.figure(figsize=(8, 8))
    plt.pie(totais, labels=instituicoes, autopct='%1.1f%%')
    plt.title("Distribuição de Projetos por Instituição")
    plt.tight_layout()
    plt.show()

    cursor.close()



def consulta_extra(connect):
    select_query = """
    SELECT
        sub.edicao,
        sub.tipo,
        SUM(sub.total) AS total_submissoes
    FROM (
        SELECT
            e.nome AS edicao,
            'Full Paper' AS tipo,
            COUNT(fp.id_projeto) AS total
        FROM Edicao e
        INNER JOIN Projeto p ON p.fk_id_edicao = e.id_edicao
        INNER JOIN Full_Paper fp ON fp.id_projeto = p.id_projeto
        GROUP BY e.nome

        UNION ALL

        SELECT
            e.nome AS edicao,
            'Short Paper' AS tipo,
            COUNT(sp.id_projeto) AS total
        FROM Edicao e
        INNER JOIN Projeto p ON p.fk_id_edicao = e.id_edicao
        INNER JOIN Short_Paper sp ON sp.id_projeto = p.id_projeto
        GROUP BY e.nome
    ) AS sub
    GROUP BY sub.edicao, sub.tipo
    ORDER BY sub.edicao, sub.tipo
    """

    print("\nConsulta Extra: Distribuição de Full Papers e Short Papers por edição.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    rows = cursor.fetchall()

    print("Edição | Tipo | Total de Submissões")
    for r in rows:
        print(r)

    edicoes = sorted(list(set([r[0] for r in rows])))
    tipos = ["Full Paper", "Short Paper"]

    dados = {tipo: [] for tipo in tipos}

    for ed in edicoes:
        for tipo in tipos:
            valor = next((r[2] for r in rows if r[0] == ed and r[1] == tipo), 0)
            dados[tipo].append(int(valor))

    x = range(len(edicoes))

    plt.figure(figsize=(12, 6))
    width = 0.4

    plt.bar([i - width/2 for i in x], dados["Full Paper"], width=width, label="Full Paper")
    plt.bar([i + width/2 for i in x], dados["Short Paper"], width=width, label="Short Paper")

    plt.xticks(x, edicoes, rotation=45)
    plt.title("Submissões por Tipo de Artigo")
    plt.xlabel("Edição")
    plt.ylabel("Total de Submissões")
    plt.legend()

    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

    cursor.close()

def gerar_relatorio_ia(texto, modelo):
    if modelo == "chatgpt":
        resposta = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": texto}]
        )
        return resposta.choices[0].message.content

    elif modelo == "gemini":
        model = genai.GenerativeModel(GEMINI_MODEL)
        resposta = model.generate_content(texto)
        return resposta.text

    else:
        return "Modelo inválido."


def ia_relatorio(connect):
    print("\n--- RELATÓRIO INTELIGENTE COM IA ---")

    print("\nEscolha o modelo de IA:")
    print("1. ChatGPT (OpenAI)")
    print("2. Gemini (Google AI)\n")

    opcao = input("Opção desejada: ")

    if opcao == "1":
        modelo = "chatgpt"
    elif opcao == "2":
        modelo = "gemini"
    else:
        print("Opção inválida.")
        return

    cursor = connect.cursor()

    cursor.execute("""
        SELECT p.titulo, u.nome AS professor, a.descricao AS area, e.nome AS edicao
        FROM Projeto p
        INNER JOIN Professor pr ON p.fk_id_professor = pr.id_professor
        INNER JOIN Usuario u ON pr.id_professor = u.id_usuario
        INNER JOIN Area_Tematica a ON p.fk_id_area_tematica = a.id_area_tematica
        INNER JOIN Edicao e ON p.fk_id_edicao = e.id_edicao
    """)
    projetos = cursor.fetchall()

    cursor.execute("""
        SELECT u.nome AS avaliador, p.titulo, av.pontuacao
        FROM Avaliacao av
        INNER JOIN Avaliador a ON a.id_avaliador = av.id_avaliador
        INNER JOIN Usuario u ON u.id_usuario = a.id_avaliador
        INNER JOIN Projeto p ON p.id_projeto = av.id_projeto
    """)
    avaliacoes = cursor.fetchall()

    texto_projetos = "\n".join([f"- {p[0]} (Prof: {p[1]}, Área: {p[2]}, Edição: {p[3]})" for p in projetos])
    texto_avaliacoes = "\n".join([f"- {a[0]} avaliou '{a[1]}' com nota {a[2]}" for a in avaliacoes])

    prompt = f"""
    Gere um relatório técnico, coerente e analítico sobre um evento acadêmico usando os dados abaixo:

    PROJETOS:
    {texto_projetos}

    AVALIAÇÕES:
    {texto_avaliacoes}

    Produza um texto contínuo, formal e acadêmico, com interpretação, 
    insights e recomendações.
    """

    try:
        resposta = gerar_relatorio_ia(prompt, modelo)
        print("\n--- RELATÓRIO GERADO ---\n")
        print(resposta)
        print("\n--- FIM DO RELATÓRIO ---\n")

    except Exception as e:
        print("Erro ao executar IA:", e)

    cursor.close()


def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão com o banco de dados foi encerrada!")


def crud_sistemaEventos(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)


try:
    con = connect_sistemaEventos()

    while True:
        print("""
    --- MENU ---
    1. CRUD COMPLETO (Drop, Create, Insert, Consultas, Update e Delete de teste)
    2. Criar tabelas
    3. Inserir dados
    4. Atualizar (automático - testes)
    5. Remover (automático - testes)
    6. Consulta 01 (Projetos por área temática e edição)
    7. Consulta 02 (Média das avaliações por projeto/professor)
    8. Consulta 03 (Projetos por instituição)
    9. Consulta Extra (Full x Short por edição)
    10. Mostrar tabela
    11. Atualizar manual
    12. Inserir manual
    13. Deletar manual
    14. Drop All
    15. Análise inteligente (IA)
    0. Sair
    """)

        choice = int(input("Opção: "))

        match choice:
            case 0:
                exit_db(con)
                break
            case 1:
                crud_sistemaEventos(con)
            case 2:
                create_all_tables(con)
            case 3:
                insert_test(con)
            case 4:
                update_test(con)
            case 5:
                delete_test(con)
            case 6:
                consulta1(con)
            case 7:
                consulta2(con)
            case 8:
                consulta3(con)
            case 9:
                consulta_extra(con)
            case 10:
                show_table(con)
            case 11:
                update_value(con)
            case 12:
                insert_manual(con)
            case 13:
                delete_manual(con)
            case 14:
                drop_all_tables(con)
            case 15:
                ia_relatorio(con)
            case _:
                print("Opção inválida.")

except mysql.connector.Error as err:
    print("Erro na conexão!", err.msg)
