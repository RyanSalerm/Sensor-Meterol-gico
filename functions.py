import serial


def ler_arduino():
    ser = serial.Serial('COM3', 9600)  # Certifique-se de ajustar a porta correta

    # Agora vamos ler os dados
    line = ser.readline().decode('latin-1').strip()

    # Formatar os dados
    dados_formatados = f'{line}'

    return dados_formatados
"""
import serial
import datetime


def ler_arduino():
    ser = serial.Serial('COM3', 9600)  # Certifique-se de ajustar a porta correta

    # Obter a data atual
    data_atual = datetime.date.today()
    dia = data_atual.day
    mes = data_atual.month

    # Agora vamos ler os dados
    line = ser.readline().decode('latin-1').strip()

    # Formatar os dados
    dados_formatados = f'{dia}/{mes},{line}'

    return dados_formatados
"""
