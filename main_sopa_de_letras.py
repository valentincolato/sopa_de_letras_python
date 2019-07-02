import PySimpleGUI as sg
import sopa_de_letras_v2_0
import configurar

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
    '''Centro de Control. Menu principal cuyo propósito es seleccionar la funcion que se desea ejecutar. Entre las cuales se encuentra:
    Ajustar la configuración del juego, Jugar, o terminar la ejecución del programa'''
    layout = [
        [sg.Text(text = 'SOPA DE LETRAS ', justification = 'center')],
        [sg.Button("JUGAR", button_color=('white', 'blue')), sg.Button("CONFIGURAR", button_color=('white', 'blue')),
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
