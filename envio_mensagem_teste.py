import tkinter as tk
from tkinter import messagebox
import json
import paho.mqtt.publish as publish
from config import MQTT_CONFIG

def enviar_dados():
    try:
        payload_dict = {}

        # Enviar JSON se houver dados preenchidos
        if entry_consumo_energia.get():
            payload_dict["ConsumoEnergia (mWh)"] = float(entry_consumo_energia.get())
        if entry_consumo_ar.get():
            payload_dict["ConsumoAr"] = float(entry_consumo_ar.get())

        if payload_dict:
            mensagem_json = json.dumps(payload_dict)
            publish.single(
                topic=MQTT_CONFIG["topics"][0],
                payload=mensagem_json,
                hostname=MQTT_CONFIG["broker"],
                port=MQTT_CONFIG["port"]
            )
            print(f"✅ JSON enviado:\n{mensagem_json}")

        # Flags booleanas enviadas como STRING
        flags = []

        if var_bproducao_true.get():
            flags.append("{bProducao: TRUE}")
        elif var_bproducao_false.get():
            flags.append("{bProducao: FALSE}")

        if var_bciclo_true.get():
            flags.append("{bCiclo: TRUE}")
        elif var_bciclo_false.get():
            flags.append("{bCiclo: FALSE}")

        if var_bpecas_defeito_true.get():
            flags.append("{bPecasDefeito: TRUE}")
        elif var_bpecas_defeito_false.get():
            flags.append("{bPecasDefeito: FALSE}")

        if var_bdetec_vazamento_true.get():
            flags.append("{bDetecVazamento: TRUE}")
        elif var_bdetec_vazamento_false.get():
            flags.append("{bDetecVazamento: FALSE}")

        # Enviar uma a uma
        for flag in flags:
            publish.single(
                topic=MQTT_CONFIG["topics"][0],
                payload=flag,
                hostname=MQTT_CONFIG["broker"],
                port=MQTT_CONFIG["port"]
            )
            print(f"✅ String enviada: {flag}")

        if not payload_dict and not flags:
            messagebox.showwarning("Atenção", "Nenhum dado preenchido ou selecionado para envio!")
        else:
            messagebox.showinfo("Sucesso", "Todos os dados enviados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar: {e}")

# GUI
root = tk.Tk()
root.title("Envio de Dados (JSON + String com TRUE/FALSE)")

# Entradas para JSON
tk.Label(root, text="ConsumoEnergia (mWh):").grid(row=0, column=0, sticky="w")
entry_consumo_energia = tk.Entry(root)
entry_consumo_energia.grid(row=0, column=1)

tk.Label(root, text="ConsumoAr:").grid(row=1, column=0, sticky="w")
entry_consumo_ar = tk.Entry(root)
entry_consumo_ar.grid(row=1, column=1)

# Cabeçalho para flags booleanas
tk.Label(root, text="Sinal").grid(row=2, column=0, pady=(10, 0))
tk.Label(root, text="TRUE").grid(row=2, column=1, pady=(10, 0))
tk.Label(root, text="FALSE").grid(row=2, column=2, pady=(10, 0))

# Função para criar linha de checkboxes TRUE/FALSE por flag
def criar_linha(nome, linha, var_true, var_false):
    tk.Label(root, text=nome).grid(row=linha, column=0, sticky="w")
    tk.Checkbutton(root, variable=var_true).grid(row=linha, column=1)
    tk.Checkbutton(root, variable=var_false).grid(row=linha, column=2)

# Variáveis para cada flag
var_bproducao_true = tk.BooleanVar()
var_bproducao_false = tk.BooleanVar()
criar_linha("bProducao", 3, var_bproducao_true, var_bproducao_false)

var_bciclo_true = tk.BooleanVar()
var_bciclo_false = tk.BooleanVar()
criar_linha("bCiclo", 4, var_bciclo_true, var_bciclo_false)

var_bpecas_defeito_true = tk.BooleanVar()
var_bpecas_defeito_false = tk.BooleanVar()
criar_linha("bPecasDefeito", 5, var_bpecas_defeito_true, var_bpecas_defeito_false)

var_bdetec_vazamento_true = tk.BooleanVar()
var_bdetec_vazamento_false = tk.BooleanVar()
criar_linha("bDetecVazamento", 6, var_bdetec_vazamento_true, var_bdetec_vazamento_false)

# Botão de envio
tk.Button(root, text="Enviar", command=enviar_dados).grid(row=7, column=0, columnspan=3, pady=15)

root.mainloop()
