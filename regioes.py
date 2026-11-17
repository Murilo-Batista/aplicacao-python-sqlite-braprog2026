
from database import conectar


class Regioes:

    def __init__(self, nome_regiao):
        self.nome_regiao = nome_regiao.strip().capitalize()

    def insert(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO regioes (nome_regiao) VALUES (?)",
            (self.nome_regiao,)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def select():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM regioes")
        resultado = cursor.fetchall()

        conn.close()
        return resultado

    @staticmethod
    def update(id_regiao, nome):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE regioes
            SET nome_regiao = ?
            WHERE id = ?
            """,
            (nome.strip().capitalize(), id_regiao)
        )

        conn.commit()
        alterados = cursor.rowcount
        conn.close()

        return alterados

    @staticmethod
    def delete(id_regiao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM regioes WHERE id = ?",
            (id_regiao,)
        )

        conn.commit()
        excluidos = cursor.rowcount
        conn.close()

        return excluidos
