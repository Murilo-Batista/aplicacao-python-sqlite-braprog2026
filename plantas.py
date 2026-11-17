
from database import conectar


class Plantas:

    def __init__(self, nome_cientifico, nomes_populares, descricao):
        self.nome_cientifico = nome_cientifico.strip().upper()
        self.nomes_populares = nomes_populares.strip().capitalize()
        self.descricao = descricao.strip()

    def insert(self, id_familia):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO plantas
            (nome_cientifico, nomes_populares, descricao, id_familia)
            VALUES (?, ?, ?, ?)
            """,
            (
                self.nome_cientifico,
                self.nomes_populares,
                self.descricao,
                id_familia
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def select():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT plantas.id,
                   plantas.nome_cientifico,
                   plantas.nomes_populares,
                   plantas.descricao,
                   familias.nome_familia
            FROM plantas
            INNER JOIN familias
            ON plantas.id_familia = familias.id
            ORDER BY plantas.id
        """)

        resultado = cursor.fetchall()
        conn.close()

        return resultado

    @staticmethod
    def update(id_planta, nome, populares, descricao, id_familia):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE plantas
            SET nome_cientifico = ?,
                nomes_populares = ?,
                descricao = ?,
                id_familia = ?
            WHERE id = ?
            """,
            (
                nome.strip().upper(),
                populares.strip().capitalize(),
                descricao.strip(),
                id_familia,
                id_planta
            )
        )

        conn.commit()
        alterados = cursor.rowcount
        conn.close()

        return alterados

    @staticmethod
    def delete(id_planta):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM plantas WHERE id = ?",
            (id_planta,)
        )

        conn.commit()
        excluidos = cursor.rowcount
        conn.close()

        return excluidos

    @staticmethod
    def vincular_categoria(id_planta, id_categoria):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO planta_categorias
            (id_planta, id_categoria)
            VALUES (?, ?)
            """,
            (id_planta, id_categoria)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def vincular_regiao(id_planta, id_regiao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO planta_regioes
            (id_planta, id_regiao)
            VALUES (?, ?)
            """,
            (id_planta, id_regiao)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def consultar_relacionamentos(id_planta):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT categorias.nome_categoria
            FROM planta_categorias
            INNER JOIN categorias
            ON planta_categorias.id_categoria = categorias.id
            WHERE planta_categorias.id_planta = ?
        """, (id_planta,))

        categorias = cursor.fetchall()

        cursor.execute("""
            SELECT regioes.nome_regiao
            FROM planta_regioes
            INNER JOIN regioes
            ON planta_regioes.id_regiao = regioes.id
            WHERE planta_regioes.id_planta = ?
        """, (id_planta,))

        regioes = cursor.fetchall()

        conn.close()

        return categorias, regioes
