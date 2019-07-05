#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import time
from temperatura import Temperatura

temperatura = Temperatura()


def leer_temp():
    info_temperatura = temperatura.datos_sensor()
    info_temperatura.update({"fecha": time.asctime(time.localtime(time.time()))})
    return info_temperatura
 
def guardar_temp(info , oficina = 'oficina1'):
    with open ("arch/datos-oficina.json", "r") as log_file:
        try:
            dic_de_temperaturas = json.load(log_file)
        except Exception:
            # En caso de que el json no sea una lista
            dic_de_temperaturas = {}
        try :
            dic_de_temperaturas[oficina].append(info)
        except KeyError:
            dic_de_temperaturas[oficina] = [info]
    with open ("arch/datos-oficina.json", "w") as log_file:
        json.dump(dic_de_temperaturas, log_file, indent=4)

if __name__ == "__main__":
    while True:
        time.sleep(60) # Espera 1r min antes de la proxima lectura
        temp = leer_temp()
        guardar_temp(temp)


