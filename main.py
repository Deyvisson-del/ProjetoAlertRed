import pywhatkit as kit
import datetime
import time

def enviar_mensagem(numero, mensagem, minutos_espera=1):
    hora = datetime.datetime.now().hour
    minuto = datetime.datetime.now().minute + minutos_espera
    kit.sendwhatmsg(numero, mensagem, hora, minuto)
    # Espera alguns segundos para evitar conflito de abas
    time.sleep(15)  # Ajuste conforme o tempo que o WhatsApp Web demora para abrir

mensagem = "Estou criando um aviso via whatsapp afim de automatizar e notificar os horários de remédios de Tio Josias \nFavor não responder"

numeros = ["+5581994810999", "+5581985027060"]

for numero in numeros:
    # Repetir 5 vezes para cada número
    for i in range(5):
        enviar_mensagem(numero, mensagem, minutos_espera=(i+1)*1)  # espaça 1 minuto cada envio
