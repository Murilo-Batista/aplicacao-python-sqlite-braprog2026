from database import conectar

class Familias:

    def __init__(self, nome_familia, descricao=""):
        self.nome_familia = nome_familia.strip().capitalize()
        self.descricao = descricao.strip()

    def insert(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO familias (nome_familia, descricao)
            VALUES (?, ?)
            """,
            (self.nome_familia, self.descricao)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def select():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM familias")
        resultado = cursor.fetchall()

        conn.close()
        return resultado

    @staticmethod
    def update(id_familia, nome, descricao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE familias
            SET nome_familia = ?, descricao = ?
            WHERE id = ?
            """,
            (nome.strip().capitalize(), descricao.strip(), id_familia)
        )

        conn.commit()
        alterados = cursor.rowcount
        conn.close()

        return alterados

    @staticmethod
    def delete(id_familia):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM familias WHERE id = ?",
            (id_familia,)
        )

        conn.commit()
        excluidos = cursor.rowcount
        conn.close()

        return excluidos
