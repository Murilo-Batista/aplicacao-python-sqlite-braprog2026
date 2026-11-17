
from database import conectar


class Categorias:

    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria.strip().capitalize()

    def insert(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO categorias (nome_categoria) VALUES (?)",
            (self.nome_categoria,)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def select():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM categorias")
        resultado = cursor.fetchall()

        conn.close()
        return resultado

    @staticmethod
    def update(id_categoria, nome):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE categorias
            SET nome_categoria = ?
            WHERE id = ?
            """,
            (nome.strip().capitalize(), id_categoria)
        )

        conn.commit()
        alterados = cursor.rowcount
        conn.close()

        return alterados

    @staticmethod
    def delete(id_categoria):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM categorias WHERE id = ?",
            (id_categoria,)
        )

        conn.commit()
        excluidos = cursor.rowcount
        conn.close()

        return excluidos
