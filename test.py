import pywhatkit as kit
import datetime
import time

# ----- CONFIGURAÇÃO -----
# Lista de destinos: números +55XXXXXXXXXXX ou IDs de grupos '1234567890-123456@g.us'
destinos = [
    "+5581994810999",      # contato 1 (exemplo)
    "+5581985027060",      # contato 2 (exemplo) # grupo (exemplo)
]

mensagem = "💊 Lembrete: tomar o remédio agora."
repeticoes_por_destino = 5    # quantas vezes quer enviar para cada destino
intervalo_minutos_entre_reps = 1  # intervalo (em minutos) entre repetições da mesma mensagem
intervalo_segundos_entre_envios = 10  # pausa entre agendamentos para o navegador "respirar"

# Quanto tempo a partir de agora (em minutos) começar a agendar os envios
# pywhatkit precisa do horário no futuro (recomendo ao menos 1-2 minutos)
atraso_minutos_para_inicio = 1
# -------------------------

def add_minutes_to_datetime(dt: datetime.datetime, minutes: int) -> datetime.datetime:
    return dt + datetime.timedelta(minutes=minutes)

def agendar_envio(destino: str, texto: str, when: datetime.datetime):
    """Usa pywhatkit para agendar o envio. Se for grupo, usa função para grupo."""
    h = when.hour
    m = when.minute
    # pywhatkit exige hora e minuto inteiros
    try:
        if destino.endswith("@g.us"):
            # função para grupos (o ID do grupo deve estar correto)
            kit.sendwhatmsg_to_group(destino, texto, h, m)
        else:
            kit.sendwhatmsg(destino, texto, h, m)
        print(f"[OK] Agendado para {destino} às {h:02d}:{m:02d}")
    except Exception as e:
        print(f"[ERRO] Falha ao agendar para {destino} às {h:02d}:{m:02d} -> {e}")

def main():
    agora = datetime.datetime.now()
    base_time = add_minutes_to_datetime(agora, atraso_minutos_para_inicio)

    # contador para espaçar envios entre destinos também (evita colisões de minuto)
    offset_minutos_global = 0

    print("Iniciando agendamento...")
    print(f"Agora: {agora.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Primeiro agendamento começará a partir de: {base_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    for destino in destinos:
        for rep in range(repeticoes_por_destino):
            # calcular horário para essa repetição
            minutos_adicionais = offset_minutos_global + rep * intervalo_minutos_entre_reps
            when = add_minutes_to_datetime(base_time, minutos_adicionais)

            # agendar
            agendar_envio(destino, mensagem, when)

            # pausa curta entre chamadas para evitar problemas no navegador
            time.sleep(intervalo_segundos_entre_envios)

        # depois de terminar as repetições de um destino, aumentamos o offset global
        # para que o próximo destino não gere colisão no mesmo minuto.
        offset_minutos_global += repeticoes_por_destino * intervalo_minutos_entre_reps

    print("\nAgendamentos concluídos. Deixe o navegador aberto e logado no WhatsApp Web.")
    print("Aguarde os envios conforme os horários acima.")

if __name__ == "__main__":
    main()
