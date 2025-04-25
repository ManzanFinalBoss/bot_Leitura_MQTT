import tkinter as tk
from tkinter import messagebox
import json
import paho.mqtt.publish as publish
from config import MQTT_CONFIG

def enviar_json():
    try:
        # Coleta os dados do formulário
        payload = {
            "InicioProd": var_inicio_prod.get(),
            "FimProd": var_fim_prod.get(),
            "InicioFalha": var_inicio_falha.get(),
            "FimFalha": var_fim_falha.get(),
            "InicioCiclo": var_inicio_ciclo.get(),
            "FimCiclo": var_fim_ciclo.get(),
            "ControleQualidade": int(entry_qualidade.get()) if entry_qualidade.get() else "",
            "ConsumoAr": float(entry_consumo_ar.get()) if entry_consumo_ar.get() else "",
            "ConsumoEnergia": float(entry_consumo_energia.get()) if entry_consumo_energia.get() else ""
        }

        mensagem = json.dumps(payload)

        publish.single(
            topic=MQTT_CONFIG["topics"][0],
            payload=mensagem,
            hostname=MQTT_CONFIG["broker"],
            port=MQTT_CONFIG["port"]
        )

        messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar: {e}")

# GUI
root = tk.Tk()
root.title("Envio Tópico 1")

# Variáveis booleanas
var_inicio_prod = tk.BooleanVar()
var_fim_prod = tk.BooleanVar()
var_inicio_falha = tk.BooleanVar()
var_fim_falha = tk.BooleanVar()
var_inicio_ciclo = tk.BooleanVar()
var_fim_ciclo = tk.BooleanVar()

# Checkboxes (ordem solicitada)
tk.Checkbutton(root, text="InicioProd", variable=var_inicio_prod).grid(row=0, column=0, sticky="w")
tk.Checkbutton(root, text="FimProd", variable=var_fim_prod).grid(row=1, column=0, sticky="w")
tk.Checkbutton(root, text="InicioFalha", variable=var_inicio_falha).grid(row=2, column=0, sticky="w")
tk.Checkbutton(root, text="FimFalha", variable=var_fim_falha).grid(row=3, column=0, sticky="w")
tk.Checkbutton(root, text="InicioCiclo", variable=var_inicio_ciclo).grid(row=4, column=0, sticky="w")
tk.Checkbutton(root, text="FimCiclo", variable=var_fim_ciclo).grid(row=5, column=0, sticky="w")

# Entradas numéricas
tk.Label(root, text="ControleQualidade (0 ou 1):").grid(row=6, column=0, sticky="w")
entry_qualidade = tk.Entry(root)
entry_qualidade.grid(row=6, column=1)

tk.Label(root, text="ConsumoAr (ex: 12.34):").grid(row=7, column=0, sticky="w")
entry_consumo_ar = tk.Entry(root)
entry_consumo_ar.grid(row=7, column=1)

tk.Label(root, text="ConsumoEnergia (ex: 45.67):").grid(row=8, column=0, sticky="w")
entry_consumo_energia = tk.Entry(root)
entry_consumo_energia.grid(row=8, column=1)

# Botão de envio
tk.Button(root, text="Enviar", command=enviar_json).grid(row=9, column=0, columnspan=2, pady=10)

root.mainloop()
