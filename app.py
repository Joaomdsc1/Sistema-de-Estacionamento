from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)

def inicializar_vagas():
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Placas")
    cursor.execute("DELETE FROM Vagas")

    for numero_vaga in range(1, 1001):
        cursor.execute("INSERT INTO Vagas (numero_vaga, ocupada) VALUES (?, ?)", (numero_vaga, 0))

    conn.commit()
    conn.close()

# Rota para cadastrar uma nova placa
@app.route('/cadastrar_placa', methods=['POST'])
def cadastrar_placa():
    data = request.json
    placa = data.get('placa')

    formato_placa = "^[A-Z]{3}-\d{4}$"
    if not placa or not re.match(formato_placa, placa):
        return jsonify({'message': 'Placa inválida! Formato esperado: ABC-1234'}), 400

    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Vagas WHERE ocupada = 0")
    vagas_disponiveis = cursor.fetchone()[0]

    if vagas_disponiveis > 0:
        try:
            data_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO Placas (placa, data_entrada) VALUES (?, ?)", (placa, data_entrada))

            cursor.execute(""" 
                UPDATE Vagas 
                SET ocupada = 1 
                WHERE id = (SELECT id FROM Vagas WHERE ocupada = 0 LIMIT 1)
            """)
            conn.commit()
            return jsonify({'message': 'Placa cadastrada com sucesso!'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Placa já cadastrada!'}), 409
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Não há vagas disponíveis!'}), 400

# Rota para verificar vagas não ocupadas
@app.route('/vagas_disponiveis', methods=['GET'])
def vagas_disponiveis():
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Vagas WHERE ocupada = 0")
    vagas_disponiveis = cursor.fetchone()[0]
    conn.close()
    return jsonify(vagas_disponiveis)

# Rota para consultar tempo de permanência e saldo
@app.route('/tempo_e_saldo/<placa>', methods=['GET'])
def tempo_e_saldo(placa):
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT data_entrada FROM Placas WHERE placa = ?", (placa,))
    resultado = cursor.fetchone()
    
    if resultado:
        data_entrada = resultado[0]
        data_saida = datetime.now()
        tempo_permanencia = data_saida - datetime.strptime(data_entrada, '%Y-%m-%d %H:%M:%S')
        saldo = calcular_saldo(tempo_permanencia)

        return jsonify({
            'data_entrada': data_entrada,
            'data_saida': data_saida.strftime('%Y-%m-%d %H:%M:%S'),
            'saldo': saldo
        }), 200
    else:
        return jsonify({'message': 'Placa não encontrada!'}), 404

def calcular_saldo(tempo_permanencia):
    return tempo_permanencia.total_seconds() / 3600 * 5

# Rota para consultar planos de fidelidade
@app.route('/planos', methods=['GET'])
def planos():
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Planos")
    planos = cursor.fetchall()
    conn.close()
    return jsonify(planos)

# Rota para consultar todas as placas
@app.route('/placas', methods=['GET'])
def consultar_placas():
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()
    cursor.execute("SELECT placa FROM Placas")
    placas = cursor.fetchall()
    conn.close()
    return jsonify([placa[0] for placa in placas])

if __name__ == '__main__':
    inicializar_vagas()
    app.run(debug=True)
