import PySimpleGUI as sg
import json

def cargarConfiguraciones():

    file = open("datos/configuracion.json", "r")
    config = json.load(file)
    file.close()
    return config

def main():
    config = cargarConfiguraciones()
    f_titulo = config['font_title']
    f_texto = config['font_text']

    plantilla = [
        [sg.Text('TITULO', font=config['font_title'],)],
        [sg.PopupScrolled(config, size=(120, None))]
    ]

    window = sg.Window('Reportes', auto_size_text=True, default_element_size=(20, 1)).Layout(plantilla)