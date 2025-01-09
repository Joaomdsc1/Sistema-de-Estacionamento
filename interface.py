import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

# Funções de consulta e cadastro
#Define a Função de Consultar Placas
def consultar_placas():
    try:
        response = requests.get("http://127.0.0.1:5000/placas")  # Verifique a rota correta na API
        if response.status_code == 200:
            placas = response.json()
            resultado_text.delete(1.0, tk.END)  # Limpa o conteúdo do Text antes de adicionar novos resultados
            resultado_text.insert(tk.END, "\n".join(placas))  # Insere as placas no Text
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, "Erro: Não foi possível buscar as placas.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Erro de Conexão: {str(e)}")
        
#Define a Função de Cadastrar Placas
def cadastrar_placa(placa):
    tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    try:
        response = requests.post("http://127.0.0.1:5000/cadastrar_placa", json={"placa": placa})
        if response.status_code == 201:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, f"{tempo} - Placa cadastrada com sucesso!")
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, "Erro: Não foi possível cadastrar a placa.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Erro de Conexão: {str(e)}")
        
#Define a Função de Consultar Vagas
def consultar_vagas_disponiveis():
    try:
        response = requests.get("http://127.0.0.1:5000/vagas_disponiveis")
        if response.status_code == 200:
            vagas = response.json()
            vagas_ocupadas = 1000 - vagas
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, f'Vagas Disponíveis: {vagas}')
            resultado_text.insert(tk.END, f"\nVagas Ocupadas: {vagas_ocupadas}")
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, "Erro: Não foi possível buscar as vagas.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Erro de Conexão: {str(e)}")
        
#Define a Função de Consultar Saldo
def consultar_permanencia_saldo(placa):
    try:
        response = requests.get(f"http://127.0.0.1:5000/tempo_e_saldo/{placa}")
        if response.status_code == 200:
            dados = response.json()
            permanencia = dados.get("data_entrada")
            permanencia1 = dados.get("data_saida")
            saldo = dados.get("saldo")
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, f"Hora de Entrada: {permanencia}\n Hora de saida: {permanencia1}\nSaldo: {saldo}")
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, "Erro: Não foi possível buscar os dados.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Erro de Conexão: {str(e)}")
        
#Define a Função de Consultar Planos
def consultar_planos_fidelidade():
    planos = [
        {"nome": "Estacionamento na Veia - Forte e vingador", "beneficios": "Acesso ilimitado, estacionamento reservado, descontos exclusivos", "requisitos": "Pagamento mensal de R$ 200,00"},
        {"nome": "Estacionamento na Veia - Preto", "beneficios": "Acesso a vagas preferenciais, descontos em estacionamentos parceiros", "requisitos": "Pagamento mensal de R$ 120,00"},
        {"nome": "Estacionamento na Veia - Prata", "beneficios": "Descontos em estacionamentos parceiros", "requisitos": "Pagamento mensal de R$ 60,00"}
    ]
    
    # Adiciona uma linha em branco entre cada plano
    planos_info = "\n\n".join([f"Plano: {p['nome']} - Benefícios: {p['beneficios']} - Requisitos: {p['requisitos']}" for p in planos])

    
    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, planos_info)

# Configuração da interface principal com abas
root = tk.Tk()
root.title("Gerenciador do Estacionamento")
root.geometry("800x600")  # Tamanho da janela ajustado

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Aba para Consulta e Cadastro de Placas (História 1)
frame_placas = ttk.Frame(notebook)
notebook.add(frame_placas, text="Consulta e Cadastro de Placas")

btn_consultar_placas = tk.Button(frame_placas, text="Consultar Placas", command=consultar_placas)
btn_consultar_placas.pack(pady=10)

tk.Label(frame_placas, text="Nova Placa:").pack(pady=5)
entry_nova_placa = tk.Entry(frame_placas)
entry_nova_placa.pack(pady=5)
btn_cadastrar_placa = tk.Button(frame_placas, text="Cadastrar Placa", command=lambda: cadastrar_placa(entry_nova_placa.get()))
btn_cadastrar_placa.pack(pady=10)

# Aba para Consulta de Vagas Disponíveis (História 2)
frame_vagas = ttk.Frame(notebook)
notebook.add(frame_vagas, text="Consulta de Vagas")
btn_consultar_vagas = tk.Button(frame_vagas, text="Consultar Vagas Disponíveis", command=consultar_vagas_disponiveis)
btn_consultar_vagas.pack(pady=10)

# Aba para Consulta de Tempo de Permanência e Saldo (História 3)
frame_permanencia = ttk.Frame(notebook)
notebook.add(frame_permanencia, text="Consulta de Permanência")
lbl_placa = tk.Label(frame_permanencia, text="Número da Placa:")
lbl_placa.pack(pady=5)
entry_placa = tk.Entry(frame_permanencia)
entry_placa.pack(pady=5)
btn_consultar_permanencia = tk.Button(frame_permanencia, text="Consultar Permanência e Saldo", command=lambda: consultar_permanencia_saldo(entry_placa.get()))
btn_consultar_permanencia.pack(pady=10)

# Aba para Consulta de Planos de Fidelidade (História 4)
frame_planos = ttk.Frame(notebook)
notebook.add(frame_planos, text="Consulta de Planos")
btn_consultar_planos = tk.Button(frame_planos, text="Consultar Planos de Fidelidade", command=consultar_planos_fidelidade)
btn_consultar_planos.pack(pady=10)

# Widget de texto com rolagem para exibir resultados
resultado_text_frame = ttk.Frame(root)
resultado_text_frame.pack(fill="both", expand=True, padx=10, pady=10)

resultado_text = tk.Text(resultado_text_frame, wrap=tk.WORD, height=10)
resultado_text.pack(expand=True, fill="both", padx=5, pady=5)

scrollbar = tk.Scrollbar(resultado_text_frame, command=resultado_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
resultado_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
