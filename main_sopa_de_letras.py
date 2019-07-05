import PySimpleGUI as sg
import sopa_de_letras_v2_0
import configurar
import json
import os

def promedioTemperatura():
    '''Funcion encargada de devolver desde un Archivo formato JSON, un Diccionario con las temperaturas registradas.'''
    tempPromedio = 21
    if (os.path.exists('datos/datos-oficina.json')):
        file = open("datos/datos-oficina.json", "r")
        d = json.load(file)
        file.close()
        temp = 0
        cantTemp = 0
        for lista in list(d.values()):
            for dic in lista:
                cantTemp = cantTemp + 1
                temp = temp + dic['temp']

        tempPromedio = temp / cantTemp

    if tempPromedio <= 19:
        color = 'BluePurple'
	
    elif tempPromedio >= 20 and tempPromedio <= 27:
        color = 'NeutralBlue'
    else:
        color = 'SandyBeach'
    return color

def barraDeProgreso():
    '''Proceso que contiene un loop que normalmente haria algo util, su funcion es estetica'''
    ok = True
    layout = [[sg.Text('Ajustando el juego :)')],
              [sg.ProgressBar(5000, orientation='h', size=(20, 20), key='progressbar')],
              [sg.Cancel()]]

    window = sg.Window('Cargando configuraciones').Layout(layout)
    progress_bar = window.FindElement('progressbar')

    for i in range(5000):
        event, values = window.Read(timeout=0)
        if event == 'Cancel' or event is None:
            ok = False
            break
        progress_bar.UpdateBar(i + 1)

    window.Close()
    return ok

def main_sopa():
    color = promedioTemperatura()
    sg.ChangeLookAndFeel(color)
    '''Centro de Control. Menu principal cuyo propósito es seleccionar la funcion que se desea ejecutar. Entre las cuales se encuentra:
    Ajustar la configuración del juego, Jugar, o terminar la ejecución del programa'''
    layout = [
        [sg.Image(filename='img/header.png')],	
        [sg.Text("\t",justification = "center"), sg.Button("JUGAR"), sg.Button("CONFIGURAR"),
         sg.Button("SALIR", button_color=('white', 'red'))]


    ]
    window = sg.Window('Sopa de Letras', auto_size_text=True, default_element_size=(20, 1)).Layout(layout)

    while True:
        event, values = window.Read()
        if event == 'JUGAR':

            if (barraDeProgreso()):
                sopa_de_letras_v2_0.main()


        elif event == 'CONFIGURAR':
            configurar.config_main()
        elif event == 'SALIR' or event == None:
            sys.exit()
            break



if __name__ == '__main__':
    import sys
    sys.exit(main_sopa())
