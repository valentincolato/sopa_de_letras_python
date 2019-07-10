#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from matriz import Matriz
from sonido import Sonido
from temperatura import Temperatura

# Conexión de los sensores en sus respectivos pines
# Matriz --> vcc: 2, gnd: 6, din: 19, cs: 24, clk: 23
# Sonido --> a0: 7, gnd: 9, vc: 3, d0: 15
# Temperatura --> vcc: 1, sda: 11, clk: 14

# Activamos los sensores que vamos a usar
# matriz = Matriz(numero_matrices=2, ancho=16)
matriz = Matriz()
sonido = Sonido()
temperatura = Temperatura()

def acciones():
    """"Obtiene los datos del sensor y lo muestra en la matriz"""

    #obtiene datos del sensor
    temp_data = temperatura.datos_sensor()
    #la escribe con un formato
    temp_formateada = 'Temperatura = {0:0.1f}°0C  Humedad = {1:0.1f}%'.format(temp_data['temperatura'], temp_data['humedad'])

    #muestra el mensaje en la matriz
    matriz.mostrar_mensaje(temp_formateada, delay=0.08, font=2)
            
if __name__ == "__main__":
    while True:
        if(sonido.evento_detectado()):
            acciones()
