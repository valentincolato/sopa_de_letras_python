# -*- coding: utf-8 -*-
#import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
#from luma.core.render import canvas
#from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class Matriz:
    def __init__(self, numero_matrices=1, orientacion=0, rotacion=0, ancho=8, alto=8):
        """Inicializador de la clase matriz"""

        #fuentes que se pueden elegir
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        #Inicializar la matriz: identificar el puerto
        self.serial = spi(port=0, device=0, gpio=noop())
        #Crear un objeto matriz
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)
    
    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        """Muestra mensaje en la matriz"""
        show_message(self.device, msg, fill="white",
                     font=proportional(self.font[font]),
                     scroll_delay=delay)

