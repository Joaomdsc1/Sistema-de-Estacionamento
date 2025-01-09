import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
import re

# Funções auxiliares
def exibir_mensagem(mensagem):
    tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado_text.insert(tk.END, f"{tempo} - {mensagem}\n")
    resultado_text.see(tk.END)

# Funções de consulta e cadastro
def consultar_placas():
    try:
        response = requests.get("http://127.0.0.1:5000/placas")
        if response.status_code == 200:
            placas = response.json()
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem("Placas cadastradas:")
            for placa in placas:
                exibir_mensagem(placa)
        else:
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem("Erro: Não foi possível buscar as placas.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        exibir_mensagem(f"Erro de Conexão: {str(e)}")

def cadastrar_placa(placa):
    formato_placa = "^[A-Z]{3}-\\d{4}$"
    if not re.match(formato_placa, placa):
        resultado_text.delete(1.0, tk.END)
        exibir_mensagem("Placa inválida! Formato esperado: ABC-1234")
        return

    try:
        response = requests.post("http://127.0.0.1:5000/cadastrar_placa", json={"placa": placa})
        if response.status_code == 201:
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem("Placa cadastrada com sucesso!")
        elif response.status_code == 400:
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem(response.json().get('message', 'Erro desconhecido.'))
        else:
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem("Erro: Não foi possível cadastrar a placa.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        exibir_mensagem(f"Erro de Conexão: {str(e)}")

def consultar_vagas_disponiveis():
    try:
        response = requests.get("http://127.0.0.1:5000/vagas_disponiveis")
        if response.status_code == 200:
            vagas = response.json()
            vagas_ocupadas = 100 - vagas
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem(f'Vagas Disponíveis: {vagas}')
            exibir_mensagem(f"Vagas Ocupadas: {vagas_ocupadas}")
        else:
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem("Erro: Não foi possível buscar as vagas.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        exibir_mensagem(f"Erro de Conexão: {str(e)}")

def consultar_permanencia_saldo(placa):
    try:
        response = requests.get(f"http://127.0.0.1:5000/tempo_e_saldo/{placa}")
        if response.status_code == 200:
            dados = response.json()
            permanencia = dados.get("data_entrada")
            permanencia1 = dados.get("data_saida")
            saldo = dados.get("saldo")
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem(f"Hora de Entrada: {permanencia}")
            exibir_mensagem(f"Hora de saída: {permanencia1}")
            exibir_mensagem(f"Saldo: {saldo}")
        else:
            resultado_text.delete(1.0, tk.END)
            exibir_mensagem("Erro: Não foi possível buscar os dados.")
    except Exception as e:
        resultado_text.delete(1.0, tk.END)
        exibir_mensagem(f"Erro de Conexão: {str(e)}")

def consultar_planos_fidelidade():
    planos = [
        {"nome": "Estacionamento na Veia - Forte e vingador", "beneficios": "Acesso ilimitado, estacionamento reservado, descontos exclusivos", "requisitos": "Pagamento mensal de R$ 200,00"},
        {"nome": "Estacionamento na Veia - Preto", "beneficios": "Acesso a vagas preferenciais, descontos em estacionamentos parceiros", "requisitos": "Pagamento mensal de R$ 120,00"},
        {"nome": "Estacionamento na Veia - Prata", "beneficios": "Descontos em estacionamentos parceiros", "requisitos": "Pagamento mensal de R$ 60,00"}
    ]
    
    planos_info = "\n\n".join([f"Plano: {p['nome']}\nBenefícios: {p['beneficios']}\nRequisitos: {p['requisitos']}" for p in planos])

    resultado_text.delete(1.0, tk.END)
    exibir_mensagem(planos_info)

# Configuração da interface principal com abas
root = tk.Tk()
root.title("Gerenciador do Estacionamento")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")

# Título
header_frame = ttk.Frame(root)
header_frame.pack(fill="x", pady=10)
header_label = ttk.Label(header_frame, text="Bem-vindo ao Gerenciador do Estacionamento", font=("Helvetica", 16, "bold"), anchor="center")
header_label.pack(pady=10)

description_label = ttk.Label(header_frame, text="Gerencie vagas, consulte placas e aproveite nossos planos de fidelidade!", font=("Helvetica", 12), anchor="center")
description_label.pack()

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Aba para Consulta e Cadastro de Placas
frame_placas = ttk.Frame(notebook)
notebook.add(frame_placas, text="Consulta e Cadastro de Placas")

btn_consultar_placas = ttk.Button(frame_placas, text="Consultar Placas", command=consultar_placas)
btn_consultar_placas.pack(pady=10)

tk.Label(frame_placas, text="Nova Placa:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
entry_nova_placa = ttk.Entry(frame_placas, font=("Helvetica", 12))
entry_nova_placa.pack(pady=5)
btn_cadastrar_placa = ttk.Button(frame_placas, text="Cadastrar Placa", command=lambda: cadastrar_placa(entry_nova_placa.get()))
btn_cadastrar_placa.pack(pady=10)

# Aba para Consulta de Vagas
frame_vagas = ttk.Frame(notebook)
notebook.add(frame_vagas, text="Consulta de Vagas")
btn_consultar_vagas = ttk.Button(frame_vagas, text="Consultar Vagas Disponíveis", command=consultar_vagas_disponiveis)
btn_consultar_vagas.pack(pady=10)

# Aba para Consulta de Tempo de Permanência e Saldo
frame_permanencia = ttk.Frame(notebook)
notebook.add(frame_permanencia, text="Consulta de Permanência")

ttk.Label(frame_permanencia, text="Número da Placa:").pack(pady=5)
entry_placa = ttk.Entry(frame_permanencia, font=("Helvetica", 12))
entry_placa.pack(pady=5)
btn_consultar_permanencia = ttk.Button(frame_permanencia, text="Consultar Permanência e Saldo", command=lambda: consultar_permanencia_saldo(entry_placa.get()))
btn_consultar_permanencia.pack(pady=10)

# Aba para Consulta de Planos de Fidelidade
frame_planos = ttk.Frame(notebook)
notebook.add(frame_planos, text="Consulta de Planos")
btn_consultar_planos = ttk.Button(frame_planos, text="Consultar Planos de Fidelidade", command=consultar_planos_fidelidade)
btn_consultar_planos.pack(pady=10)

# Widget de texto com rolagem para exibir resultados
resultado_text_frame = ttk.Frame(root)
resultado_text_frame.pack(fill="both", expand=True, padx=10, pady=10)

resultado_text = tk.Text(resultado_text_frame, wrap=tk.WORD, height=10, font=("Helvetica", 12))
resultado_text.pack(expand=True, fill="both", padx=5, pady=5)

scrollbar = ttk.Scrollbar(resultado_text_frame, command=resultado_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
resultado_text.config(yscrollcommand=scrollbar.set)

root.mainloop()