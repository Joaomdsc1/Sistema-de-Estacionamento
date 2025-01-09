import sqlite3

conn = sqlite3.connect('estacionamento.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Placas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL UNIQUE,
        data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_saida TIMESTAMP DEFAULT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vagas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_vaga INTEGER NOT NULL UNIQUE,
        ocupada BOOLEAN DEFAULT 0
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Planos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        desconto REAL
    )
''')

conn.commit()
conn.close()
