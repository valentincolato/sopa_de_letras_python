#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import time
from temperatura import Temperatura

temperatura = Temperatura()


def leer_temp():
    """"Devuelve un diccionario con los datos del sensor, invocando los metodos correspondientes
     de la clase temperatura y le agrega la fecha actual al diccionario"""
    info_temperatura = temperatura.datos_sensor()
    info_temperatura.update({"fecha": time.asctime(time.localtime(time.time()))})
    return info_temperatura
 
def guardar_temp(info , oficina = 'oficina1'):
    """Proceso encargado de guardar lo leido por el sensor, en el archivo json """
    if(os.path.exists("arch/datos-oficina.json")):
        with open("arch/datos-oficina.json", "r") as log_file:
            dic_de_temperaturas = json.load(log_file)
    else:
        dic_de_temperaturas = {}

    #guardamos la nueva temperatura en el diccionario
    try :
        dic_de_temperaturas[oficina].append(info)
    except KeyError:
        #si la oficina no estaba en el diccionario se agrega
        dic_de_temperaturas[oficina] = [info]

    ##guardamos en el archivo el diccionario actualizado
    with open ("arch/datos-oficina.json", "w") as log_file:
        json.dump(dic_de_temperaturas, log_file, indent=4)

if __name__ == "__main__":
    while True:
        time.sleep(60) # Espera 1 min antes de la proxima lectura
        temp = leer_temp()
        guardar_temp(temp)


