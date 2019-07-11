#!/usr/bin/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

"""
A0  --> pin 7
VCC --> pin 2
GND --> pin 6
D0  --> pin 15 (BCM22)
"""

class Sonido:
    
    def __init__(self, canal=22):
        """Inicializador  de la clase sonido """
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)
        
    def evento_detectado(self):
        """Proceso que devuelve cuando un sonido es detectado """
        sonido = False
        if GPIO.event_detected(self._canal):
            sonido = True

        return sonido


