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

def insertDB(palabra, intentos, tiempo_total):
    conn = sqlite3.connect('palabras.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO palabras (palabra, intentos, tiempo_total)
        VALUES (?, ?, ?)
        ''', (palabra, intentos, tiempo_total))
    conn.commit()
    conn.close()

def generar_aleatorio(largo):
    """Genera una cadena aleatoria del largo dado (incluyendo letras y espacios)."""
    return ''.join(random.choices(string.ascii_letters + " ", k=largo))

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
        print(f"{random.choice(colores)}{generado}{Style.RESET_ALL}", end="\r")

        if generado == objetivo:  # Comparación estricta, distingue mayúsculas y minúsculas
            # Registrar el tiempo de finalización
            tiempo_fin = time.time()
            tiempo_total = tiempo_fin - tiempo_inicio  # Calcular la duración total
            print(f"{Fore.GREEN}Palabra formada: {generado} en {intentos_totales} intentos en {tiempo_total:.2f} segundos.{Style.RESET_ALL}")
            insertDB(objetivo, intentos_totales, tiempo_total)  # Guardar en la base de datos
            break  # Termina el ciclo inmediatamente después de encontrar la palabra

if __name__ == "__main__":
    createDB()
    palabra_objetivo = input(str("Ingrese que palabra quiere formar: "))  # Cambia por la palabra que desees formar
    formar_palabra(palabra_objetivo)
