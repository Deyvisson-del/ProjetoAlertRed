import pywhatkit as kit
import datetime
import time

destinos = [
    "+5581994810999",      
    "+5581985027060",      
]

mensagem = "💊 Lembrete: tomar o remédio agora."
repeticoes_por_destino = 5    
intervalo_minutos_entre_reps = 1  
intervalo_segundos_entre_envios = 10  

atraso_minutos_para_inicio = 1

def add_minutes_to_datetime(dt: datetime.datetime, minutes: int) -> datetime.datetime:
    return dt + datetime.timedelta(minutes=minutes)

def agendar_envio(destino: str, texto: str, when: datetime.datetime):
    """Usa pywhatkit para agendar o envio. Se for grupo, usa função para grupo."""
    h = when.hour
    m = when.minute
   
    try:
        if destino.endswith("@g.us"):
            kit.sendwhatmsg_to_group(destino, texto, h, m)
        else:
            kit.sendwhatmsg(destino, texto, h, m)
        print(f"[OK] Agendado para {destino} às {h:02d}:{m:02d}")
    except Exception as e:
        print(f"[ERRO] Falha ao agendar para {destino} às {h:02d}:{m:02d} -> {e}")

def main():
    agora = datetime.datetime.now()
    base_time = add_minutes_to_datetime(agora, atraso_minutos_para_inicio)

    
    offset_minutos_global = 0

    print("Iniciando agendamento...")
    print(f"Agora: {agora.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Primeiro agendamento começará a partir de: {base_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    for destino in destinos:
        for rep in range(repeticoes_por_destino):
            
            minutos_adicionais = offset_minutos_global + rep * intervalo_minutos_entre_reps
            when = add_minutes_to_datetime(base_time, minutos_adicionais)

           
            agendar_envio(destino, mensagem, when)

           
            time.sleep(intervalo_segundos_entre_envios)

        offset_minutos_global += repeticoes_por_destino * intervalo_minutos_entre_reps

    print("\nAgendamentos concluídos. Deixe o navegador aberto e logado no WhatsApp Web.")
    print("Aguarde os envios conforme os horários acima.")

if __name__ == "__main__":
    main()
