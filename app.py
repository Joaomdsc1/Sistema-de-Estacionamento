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

    for numero_vaga in range(1, 101):  # Número de vagas ajustado para 100
        cursor.execute("INSERT INTO Vagas (numero_vaga, ocupada) VALUES (?, ?)", (numero_vaga, 0))

    conn.commit()
    conn.close()

@app.route('/cadastrar_placa', methods=['POST'])
def cadastrar_placa():
    data = request.json
    placa = data.get('placa')

    if not placa:
        return jsonify({'message': 'Placa não pode ser vazia!'}), 400

    placa = placa.upper()  # Converte a placa para maiúsculas para padronização
    formato_placa = "^[A-Z]{3}-\d{4}$"
    if not re.match(formato_placa, placa):
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


@app.route('/vagas_disponiveis', methods=['GET'])
def vagas_disponiveis():
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Vagas WHERE ocupada = 0")
    vagas_disponiveis = cursor.fetchone()[0]
    conn.close()
    return jsonify(vagas_disponiveis)

@app.route('/tempo_e_saldo', methods=['GET'])
@app.route('/tempo_e_saldo/<placa>', methods=['GET'])
def tempo_e_saldo(placa=None):
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()

    if placa:
        # Converte a placa para maiúsculas para padronização
        placa = placa.upper()
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
    else:
        # Se nenhuma placa for passada, retorna todos os registros
        cursor.execute("SELECT placa, data_entrada FROM Placas")
        placas = cursor.fetchall()
        registros = []
        for placa, data_entrada in placas:
            data_saida = datetime.now()
            tempo_permanencia = data_saida - datetime.strptime(data_entrada, '%Y-%m-%d %H:%M:%S')
            saldo = calcular_saldo(tempo_permanencia)
            registros.append({
                'placa': placa,
                'data_entrada': data_entrada,
                'data_saida': data_saida.strftime('%Y-%m-%d %H:%M:%S'),
                'saldo': saldo
            })
        return jsonify(registros), 200

def calcular_saldo(tempo_permanencia):
    total_minutos = tempo_permanencia.total_seconds() / 60

    if total_minutos <= 15:
        return 0
    elif total_minutos <= 30:
        return 10
    elif total_minutos <= 45:
        return 15
    elif total_minutos <= 60:
        return 22
    else:
        minutos_adicionais = total_minutos - 60
        intervalos_adicionais = (minutos_adicionais // 15) + (1 if minutos_adicionais % 15 > 0 else 0)
        return 22 + intervalos_adicionais * 10

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

@app.route('/dar_baixa', methods=['POST'])
def dar_baixa():
    data = request.json
    placa = data.get('placa')

    if not placa:
        return jsonify({'message': 'Placa não pode ser vazia!'}), 400

    placa = placa.upper()  # Padroniza a placa em maiúsculas
    conn = sqlite3.connect('estacionamento.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Placas WHERE placa = ?", (placa,))
    resultado = cursor.fetchone()

    if resultado:
        try:
            # Deleta a placa da tabela
            cursor.execute("DELETE FROM Placas WHERE placa = ?", (placa,))

            # Libera uma vaga associada
            cursor.execute("""
                UPDATE Vagas
                SET ocupada = 0
                WHERE id = (SELECT id FROM Vagas WHERE ocupada = 1 LIMIT 1)
            """)

            conn.commit()
            return jsonify({'message': 'Carro removido com sucesso e vaga liberada!'}), 200
        except Exception as e:
            return jsonify({'message': f'Erro ao dar baixa: {str(e)}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Placa não encontrada!'}), 404
