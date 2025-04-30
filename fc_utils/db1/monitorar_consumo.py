from datetime import datetime
from zoneinfo import ZoneInfo
from fc_utils.db1.inserir_consumo import inserir_consumo

def monitorar_consumo(dados):
    if "ConsumoAr" in dados or "ConsumoEnergia" in dados:
        consumo_ar = dados.get("ConsumoAr", 0.0)
        consumo_energia = dados.get("ConsumoEnergia", 0.0)
        horario = datetime.now(ZoneInfo("America/Sao_Paulo"))

        # Verificação extra para garantir timezone
        if horario.tzinfo is None:
            horario = horario.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))

        print(f"\n💨 Monitorando consumo:")
        print(f"   • Consumo de Ar: {consumo_ar}")
        print(f"   • Consumo de Energia: {consumo_energia}")
        print(f"   • Horário: {horario}")

        inserir_consumo(consumo_ar, consumo_energia, horario)
