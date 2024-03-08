from clases import Metro, Persona, Tren
import parametros
import time
import random

# inicializacion de variables

tiempo_final = 600

# inicializacion de clases

metro = Metro(linea= parametros.E, lista_trenes= parametros.Trenes)

# Inicio

print("----------------Bienvenido al sistema de simulación de metro----------------")


while metro.retornar_tiempo() < tiempo_final:
    metro.avanzar()
    metro.imprimir_estado()
    input("presione enter para avanzar")

# se contabilizan las personas para el cálculo cuando estas se BAJAN.
metro.imprimir_tiempo_espera()
