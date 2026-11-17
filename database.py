
import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "plantas.db")

def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar_banco():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS familias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_familia TEXT NOT NULL UNIQUE,
            descricao TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS plantas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cientifico TEXT NOT NULL UNIQUE,
            nomes_populares TEXT NOT NULL,
            descricao TEXT,
            id_familia INTEGER NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_familia)
                REFERENCES familias (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_categoria TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS regioes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_regiao TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS planta_categorias (
            id_planta INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            PRIMARY KEY (id_planta, id_categoria),
            FOREIGN KEY (id_planta)
                REFERENCES plantas (id) ON DELETE CASCADE,
            FOREIGN KEY (id_categoria)
                REFERENCES categorias (id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS planta_regioes (
            id_planta INTEGER NOT NULL,
            id_regiao INTEGER NOT NULL,
            PRIMARY KEY (id_planta, id_regiao),
            FOREIGN KEY (id_planta)
                REFERENCES plantas (id) ON DELETE CASCADE,
            FOREIGN KEY (id_regiao)
                REFERENCES regioes (id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()