
# Aquí se definen las clases tren, estacion y persona
# Relaciones: el tren tiene una lista de personas, el metro tiene estaciones y trenes

# tomar en consideracion: este programa solo funciona si hay a lo menos dos estaciones. Sino el while 
# de elegir el destino de la persona no termina nunca

import random

class Metro():
    def __init__(self, linea: list, lista_trenes: list):
        self.tiempo = 0
        #lista de ceros y unos
        self.linea = linea
        #ista de instancias estacion
        self.estaciones = []
        #lista de clases de tipo Tren
        self.trenes = []
        #los siguientes dos parámetros son para calcular el tiempo de espera promedio
        self.tiempo_total = 0
        self.personas_atendidas = 0
        #inicializar instancias de clases (trenes y estaciones)
        contador = 0
        for i in linea:
            if i == 1:
                nueva_estacion = Estacion(posicion= contador)
                self.estaciones.append(nueva_estacion)
            contador += 1
        contador = 0
        for i in lista_trenes:
            nuevo_tren = Tren(id= contador, posicion_partida= i[0], direccion= i[1])
            if linea[nuevo_tren.estacion_actual] == 1:
                nuevo_tren.pasajeros_en_movimiento = True
            self.trenes.append(nuevo_tren)
            contador += 1
        # me falta poner la modalidad de tiempo y visualizacion de la simulación
    
    def retornar_tiempo(self):
        return self.tiempo

    def avanzar(self):
        # primero llegan personas a las estaciones
        for i in self.estaciones:
            # esta sintaxis incluye al 0 y al 10
            personas_llegando = random.randint(0, 10)
            for p in range(personas_llegando):
                destino_persona = random.choice(self.estaciones)
                # seria mas eficiente eliminar la opcion de la lista
                while destino_persona.posicion == i.posicion:
                    destino_persona = random.choice(self.estaciones)
                nueva_persona = Persona(posicion_inicio= i.posicion, destino= destino_persona.posicion, tiempo_inicio= self.tiempo)
                i.personas.append(nueva_persona)
        for t in self.trenes:
            # si el tren no esta parado en una estación
            if not t.pasajeros_en_movimiento:
                # si el tren va hacia la derecha
                if t.direccion == "d":
                    # si el tren está en la última estación
                    if t.estacion_actual == len(self.linea) - 1:
                        t.direccion = "i"
                        t.estacion_actual -= 1
                    else:
                        t.estacion_actual += 1
                # si el tren va hacia la izquierda
                else:
                    # si el tren está en la primera estación
                    if t.estacion_actual == 0:
                        t.direccion = "d"
                        t.estacion_actual += 1
                    else:
                        t.estacion_actual -= 1
                #revisar si ha caido recien en una estacion
                if self.linea[t.estacion_actual] == 1:
                    t.pasajeros_en_movimiento = True
            else:
                # si el tren está parado en una estación
                # personas que se bajan
                for p in t.pasajeros:
                    if p.destino == t.estacion_actual:
                        t.dejar_pasajero(p)
                        # t.pasajeros.remove(p) se hace en funcion
                        self.personas_atendidas += 1
                        self.tiempo_total += self.tiempo - p.tiempo_inicio
                # personas que se suben
                #esto de aca es un poco ineficiente
                for estacion in self.estaciones:
                    if estacion.posicion == t.estacion_actual:
                        for p in estacion.personas:
                            if p.direccion_viaje == t.direccion:
                                t.agregar_pasajero(p)
                                #t.pasajeros.append(p) se hace en funcion
                                estacion.personas.remove(p)
                t.pasajeros_en_movimiento = False
        self.tiempo += 1

    def imprimir_estado(self):
        print(f'TIEMPO {self.tiempo}')
        print("ESTADO DE LOS TRENES")
        for i in range(len(self.trenes)):
            print(f'El tren {i} está en la estación {self.trenes[i].estacion_actual} y se dirige hacia la {self.trenes[i].direccion} llevando a {len(self.trenes[i].pasajeros)} personas')
            #print("las estaciones a las que se dirigen son")
            lista_auxiliar = []
            #for j in range(len(self.linea)):
            #    lista_auxiliar.append(0)
            #for p in self.trenes[i].pasajeros:
            #    lista_auxiliar[p.destino] += 1
            #print(lista_auxiliar)
        print("\n")
        print("ESTADO DE LAS ESTACIONES")
        for i in range(len(self.estaciones)):
            print(f'La estación {self.estaciones[i].posicion} tiene {len(self.estaciones[i].personas)} personas esperando')
            contador_derecha = 0
            contador_izquierda = 0
            for  p in self.estaciones[i].personas:
                if p.direccion_viaje == "d":
                    contador_derecha += 1
                else:
                    contador_izquierda += 1
            #print(f'    {contador_derecha} personas esperando hacia la derecha y {contador_izquierda} personas esperando hacia la izquierda')
        
        print("\n")
        print("\n")
    
    def imprimir_tiempo_espera(self):
        # manejar el caso de cero personas atendidas
        if self.personas_atendidas == 0:
            print('No se atendió a ninguna persona')
        else:
            print(f'El tiempo promedio de espera es de {self.tiempo_total / self.personas_atendidas} segundos')


# hacer variable de clase
class Persona():
    def __init__(self, posicion_inicio: int, destino: int, tiempo_inicio: int):
        self.destino = destino
        self.tiempo_inicio = tiempo_inicio
        #incializar direccion viaje correctamente
        self.direccion_viaje = ""
        if destino > posicion_inicio:
            self.direccion_viaje = "d" 
        else:
            self.direccion_viaje = "i"
    
class Tren():
    def __init__(self, id: int, posicion_partida: int, direccion: str):
        # pasajeros en mov (cuando el tren llega a una estacion esto se vuelve true, en el siguiente avance
        # scuando esta true en el siguiente avance no avanzara, los pasajeros bajan y suben, y se vuelve false)
        self.pasajeros_en_movimiento = False
        # sera true si esque parte en posicion partida, esto se maneja al inicializar desde metro
        self.id = id
        # lista de personas
        self.pasajeros = []
        self.estacion_actual = posicion_partida
        self.direccion = direccion

    def agregar_pasajero(self, persona: Persona):
        #print(f'Una persona ha entrado al tren {self.id}')
        self.pasajeros.append(persona)

    def dejar_pasajero(self, persona: Persona):
        #print(f'Una persona ha salido al tren {self.id}')
        self.pasajeros.remove(persona)

class Estacion():
    def __init__(self, posicion):
        self.posicion = posicion
        #lista de personas
        self.personas = []