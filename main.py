import random
import string
import sqlite3
import time
from colorama import Fore, Style, init

init(autoreset=True)

def createDB():
    conn = sqlite3.connect('palabras.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS palabras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra TEXT NOT NULL,
        intentos INTEGER NOT NULL,
        tiempo_total REAL NOT NULL
        )
        ''')
    conn.commit()
    conn.close()

def createCasiDB():
    conn = sqlite3.connect('casiConcidencias.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS casiConcidencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra_objetivo TEXT NOT NULL,
        palabra_encontrada TEXT NOT NULL,
        intentos INTEGER NOT NULL
        )
        ''')
    conn.commit()
    conn.close()

def insertDB(palabra, intentos, tiempo_total):
    conn = sqlite3.connect('palabras.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO palabras (palabra, intentos, tiempo_total)
        VALUES (?, ?, ?)
        ''', (palabra, intentos, tiempo_total))
    conn.commit()
    conn.close()

def insertCasiDB(palabra_objetivo, palabra_encontrada, intentos):
    conn = sqlite3.connect('casiConcidencias.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO casiConcidencias (palabra_objetivo, palabra_encontrada, intentos)
        VALUES (?, ?, ?)
        ''', (palabra_objetivo, palabra_encontrada, intentos))
    conn.commit()
    conn.close()

def generar_aleatorio(largo):
    """Genera una cadena aleatoria del largo dado (solo letras)."""
    return ''.join(random.choices(string.ascii_letters, k=largo))

def formar_palabra(objetivo):
    """Intenta formar la palabra objetivo de manera aleatoria y cuenta los intentos."""
    intentos_totales = 0
    colores = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.WHITE]
    print("Generando aleatoriamente, espere... ")

    # Registrar el tiempo de inicio
    tiempo_inicio = time.time()

    while True:
        intentos_totales += 1
        generado = generar_aleatorio(len(objetivo))

        if intentos_totales % 50000000 == 0:  # Imprimir cada 1 millón de intentos
            print(f"{random.choice(colores)}Intento {intentos_totales}: {generado}{Style.RESET_ALL}")

        if generado.lower() == objetivo.lower() and generado != objetivo:  # Coincidencia casi exacta
            print(f"{Fore.YELLOW}Casi coincidencia: {generado} encontrada en {intentos_totales} intentos.{Style.RESET_ALL}")
            insertCasiDB(objetivo, generado, intentos_totales)  # Guardar en la base de datos de casi coincidencias

        if generado == objetivo:  # Coincidencia exacta
            # Registrar el tiempo de finalización
            tiempo_fin = time.time()
            tiempo_total = tiempo_fin - tiempo_inicio  # Calcular la duración total
            print(f"{Fore.GREEN}Palabra formada: {generado} en {intentos_totales} intentos en {tiempo_total:.2f} segundos.{Style.RESET_ALL}")
            insertDB(objetivo, intentos_totales, tiempo_total)  # Guardar en la base de datos de coincidencias exactas
            break  # Termina el ciclo inmediatamente después de encontrar la palabra

if __name__ == "__main__":
    createDB()
    createCasiDB()
    palabra_objetivo = input(str("Ingrese que palabra quiere formar: "))  # Cambia por la palabra que desees formar
    formar_palabra(palabra_objetivo)
