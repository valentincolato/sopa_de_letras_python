#################################################################
# Author: Colato Valentin, Piñeyro Daniela                          
# License: Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# License URL: https://creativecommons.org/licenses/by-sa/4.0/
#################################################################

import PySimpleGUI as sg
from pattern.web import Wiktionary
from pattern.es import parse
import os
import json


def reporte1(palabra):
    '''Genera el Archivo de Reporte cuando la palabra no es encontrada ni en Wikionary, ni Pattern'''
    if (os.path.exists('datos/reporte1.txt')):
        file = open("datos/reporte1.txt", "a")

    else:
        file = open("datos/reporte1.txt", "w")
        file.writelines(" ERRORES CUANDO LA PALABRA NO ES ENCONTRADA \n")

    file.writelines(" Error con la palabra \'" + palabra + "\'. No se encuentra en Pattern ni en Wiktionary.\n")


def BuscadorWIKI(palabra):
    '''Busca la palabra y su defincion en Wiktionary'''
    w = Wiktionary(language='es')
    article = w.search(palabra)
    tipo = '9999'
    definicion = ''
    encontro = False
    try:
        for elem in article.sections:
            if 'verbo' in elem.title.lower():
                tipo = 'verbo'
                encontro = True
            elif 'sustantivo' in elem.title.lower():
                tipo = 'sustantivo'
                encontro = True
            elif 'adjetivo' in elem.title.lower():
                tipo = 'adjetivo'
                encontro = True
            if encontro == True:
                definicion = elem.content.split('1')[1].split('.2')[0].split('*')[0]
                break

    except AttributeError:
        sg.Popup('Palabra ingresada no encontrada en wiki')

    return (tipo, definicion)


def BuscadorPAT(palabra):
    '''Busca la clasificacion de la palabra en Pattern'''
    s = parse(palabra, relations=True, lemmata=True).split("/")[1]
    tipopattern = '9999'
    if s == 'VB':
        tipopattern = 'verbo'
    elif s == 'JJ':
        tipopattern = 'adjetivo'
    elif s == 'NN':
        tipopattern = 'sustantivo'
    else:
        sg.Popup('No encontrada en pattern')

    return tipopattern


def actualizarJSON(d):
    '''Actualiza/Crea un archivo JSON con las palabras ingresadas por la docente'''
    file = open("datos/palabras.json", "w")
    json.dump(d, file, indent=4)
    file.close()


def agregarPalabra(palabra):
    '''Funcion encargada de verificar si es una palabra valida, en caso de no hallar una defincion para dicha palabra, se le solicitara
    al Usuario el ingreso de una. Ademas, se encargara de la generacion de reportes de acuerdo a dos casos:
        1) No coinciden las clasificaciones dadas por Pattern y Wiktionary
        2) No se encuentra la palabra en Pattern ni en Wiktionary
    '''
    # el tipo a agregar por defecto es el de wiki
    tipoAAgregar, definicion = BuscadorWIKI(palabra)
    tipopattern = BuscadorPAT(palabra)
    # si encontro el tipo pero no la definicion le pido que lo ingrese
    if tipoAAgregar != '9999' or tipopattern != '9999' and definicion == '':

        while definicion == '':
            definicion = sg.PopupGetText('Definicion no encontrada, por favor ingrese definicion de la palabra ',
                                         palabra)
        if definicion == None:
            tipoAAgregar = '9999'
        else:

            # si tipo wiki es distinto de 9999 significa que encontro el tipo en wiktcionary
            # comparo si son iguales
            if (tipoAAgregar != '9999'):
                if (tipopattern != tipoAAgregar and tipopattern != '9999'):

                    sg.Popup('No coinciden los valores de pattern con wikcionary')

                    if (os.path.exists('datos/reporte.txt')):
                        file = open("datos/reporte.txt", "a")

                    else:
                        file = open("datos/reporte.txt", "w")
                        file.writelines('ERRORES CUANDO NO COINCIDEN\n')

                    file.writelines("Error con la palabra \'" + palabra + "\' no coinciden los tipos\n")
                    file.writelines("PATTERN:  " + tipopattern + "\n")
                    file.writelines("WIKTONARY: " + tipoAAgregar + "\n\n")

                    file.close()
            else:
                # pregunto si se encontro en pattern
                tipoAAgregar = tipopattern
    else:
        sg.Popup('Palabra no valida')
        reporte1(palabra)

    return (tipoAAgregar, definicion)


def cargarD():
    '''Funcion encargada de devolver desde un Archivo formato JSON, un Diccionario con las palabras a utilizar en la Sopa De Letras.
        En caso de no existir dicho archivo, se inicializará el Diccionario vacío'''
    if (os.path.exists('datos/palabras.json')):
        file = open("datos/palabras.json", "r")
        d = json.load(file)
        file.close()
    else:
        d = {'adjetivo': {},
             'sustantivo': {},
             'verbo': {}}

    return d


def cargarOficinas():
    '''Funcion encargada de devolver desde un Archivo formato JSON, un Diccionario con las temperaturas de las oficinas
        En caso de no existir dicho archivo, se inicializará oficina por defecto'''
    existe = True
    if (os.path.exists('raspberry/arch/datos-oficina.json')):
        file = open("raspberry/arch/datos-oficina.json", "r")
        d = json.load(file)
        file.close()
    else:
        d= {"":None}
        existe = False

    return (d,existe)


def cargarConfiguraciones():
    '''Funcion encargada de devolver desde un Archivo formato JSON, un Diccionario con las configuraciones a utilizar en la Sopa De Letras'''
    if (os.path.exists('datos/configuracion.json')):
        file = open("datos/configuracion.json", "r")
        config = json.load(file)
        file.close()
    else:
        config = {"Cantidad_Verbos": 0, "Cantidad_Adjetivos": 0,
                  "Cantidad_Sustantivos": 0,
                  "Color_ADJETIVO": '', "Color_VERBO": '',
                  "Color_SUSTANTIVO": '', "Ayuda": '', "Oficina": "", "Mayuscula": '',
                  "Tipo_Orientacion": ''}
    return config


def cargarConfig(values):
    '''Funcion que verifica si el Usuario ingreso valores correctos a la configuracion. De no ser asi, se corrigen los posibles errores.
        Luego se carga la configuracion a un archivo JSON'''
    ok = False
    if values['colorAd'] == '':
        values['colorAd'] = '#5727B1'
    if values['colorSus'] == '':
        values['colorSus'] = '#F15A69'
    if values['colorVerb'] == '':
        values['colorVerb'] = '#E28769'
    if values['cantad'] == '0' and values['cantverb'] == '0' and values['cantsus'] == '0' or (values['colorSus'] == values['colorVerb']
       or values['colorSus'] == values['colorAd'] or values['colorAd'] == values['colorVerb']):

        sg.Popup("Valores Invalidos, vuelva  a ingresar")
    else:
        ok = True

        config = {"Cantidad_Verbos": values['cantverb'], "Cantidad_Adjetivos": values['cantad'],
                  "Cantidad_Sustantivos": values['cantsus'],
                  "Color_ADJETIVO": values['colorAd'], "Color_VERBO": values['colorVerb'],
                  "Color_SUSTANTIVO": values['colorSus'], "Ayuda": values['ayuda'], "Oficina": values['office'],
                  "Mayuscula": values['mayus'],
                  "Tipo_Orientacion": values['orientacion']}
        file = open("datos/configuracion.json", "w")
        json.dump(config, file, indent=4)
        file.close()
    return ok


def actualizar_text(window):
    '''Actualiza a vacio el campo donde se ingresan las palabras'''
    elemento = window.FindElement('palabra')
    elemento.Update('')


def leerReporte(arch):
    '''Funcion que abre el archivo de texto y lo devuelve en forma de lista'''
    file = open(arch, 'r')
    txt = file.readlines()
    file.close()
    return txt


def mostrarReporte(arch, titulo, texto):
    '''Funcion que lee el reporte, y lo muestra en una nueva ventana'''
    try:
        txt = leerReporte(arch)
        layout = [
            [sg.Text(txt[0], font=titulo)],
            [sg.Listbox(txt[1:], size=(70, 10), font=texto)],
            [sg.Button('VOLVER')]
        ]
        window = sg.Window('Reporte', auto_size_text=True, default_element_size=(20, 1)).Layout(layout)

        while True:
            event = window.Read()
            if event[0] == 'VOLVER' or event[0] is None:
                window.Close()
                break
    except FileNotFoundError:
        sg.Popup('No se encontro el archivo')


def config_main():
    '''Funcion central donde se inicializa el Layout, se invocan los procesos necesarios '''
    # cargo el diccionario#
    d = cargarD()

    config = cargarConfiguraciones()

    ofi,existeOficina = cargarOficinas()

    layout = [
        [sg.Image(filename='img/menu_header.png')],
        [sg.Text('Ingrese palabras para usar en la sopa de letras '), sg.InputText(key='palabra'), sg.Button('Agregar'),
         sg.Button('Eliminar')],
        [sg.Text('Orientacion del juego'),
         sg.InputCombo(['Vertical', 'Horizontal'], size=(40, 20), key='orientacion', readonly=True,
                       default_value=config['Tipo_Orientacion'])],
        [sg.Text('Letras en '), sg.InputCombo(['mayuscula', 'minuscula'], size=(40, 20), key='mayus', readonly=True,
                                              default_value=config['Mayuscula'])],
        [sg.Text('Palabras Agregadas', justification='center'), sg.Listbox(values=list(
            ['  Sustantivos: '] + list(d['sustantivo'].keys()) + ['  Adjetivos: '] + list(d['adjetivo'].keys()) + [
                '  Verbos: '] + list(d['verbo'].keys())
            ), key='listbox', size=(30, 5))],
        [sg.Text('Cantidad de Palabras', justification='center', font=('Helvetica', 11))],
        [sg.Text('Sustantivos:', justification='center'),
         sg.InputCombo(list(range(len(list(d['sustantivo'].keys())) + 1)), key='cantsus', size=(5, 5), readonly=True,
                       default_value=int(config['Cantidad_Sustantivos'])),
         sg.Button(key='colorSus', button_text='color', button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
        [sg.Text('Adjetivos:    ', justification='center'),
         sg.InputCombo(list(range(len(list(d['adjetivo'].keys())) + 1)), key='cantad', size=(5, 5), readonly=True,
                       default_value=int(config['Cantidad_Adjetivos'])),
         sg.Button(key='colorAd', button_text='color', button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
        [sg.Text('Verbo:         ', justification='center'),
         sg.InputCombo(list(range(len(list(d['verbo'].keys())) + 1)), key='cantverb', size=(5, 5), readonly=True,
                       default_value=int(config['Cantidad_Verbos'])),
         sg.Button(key='colorVerb', button_text='color', button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
        [sg.Text('Ayuda', justification='center'),
         sg.InputCombo(['Si', 'No'], key='ayuda', size=(5, 5), readonly=True, default_value=config['Ayuda'])],
        [sg.Text('Seleccione Oficina', justification='center'),
         sg.InputCombo(list(ofi.keys()), key='office', size=(10, 5), readonly=True,disabled= not(existeOficina), default_value=config['Oficina'])],
        [sg.Text('Seleccione Tipografia ', size=(40, 1), font=("Helvetica", 13), justification='center')],
        [sg.Text('Tipografia del Título'),
         sg.InputCombo(['Arial', 'Helvetica', 'Calibri'], size=(40, 20), key='font1', readonly=True)],
        [sg.Text('Tipografia del Texto'),
         sg.InputCombo(['Arial', 'Helvetica', 'Calibri'], size=(40, 20), key='font2', readonly=True)],
        [sg.Button("Guardar configuracion", button_color=('white', 'green')),
         sg.Button("Salir", button_color=('white', 'red')), sg.Button('Reporte 1'), sg.Button('Reporte 2')]]

    window = sg.Window('Configuracion', auto_size_text=True, default_element_size=(40, 1)).Layout(layout)

    listbox = window.FindElement('listbox')

    sus = window.FindElement('cantsus')
    adj = window.FindElement('cantad')
    verb = window.FindElement('cantverb')
    while True:
        event, values = window.Read()
        if event == 'Guardar configuracion':
            opcion = sg.PopupYesNo('¿Seguro que desea guardar? ')
            if opcion == 'Yes':
                ok = cargarConfig(values)
                if (ok):
                    window.Close()
                    break



        elif event == 'Agregar':

            p = values['palabra']
            actualizar_text(window)
            ok = False
            for dic in list(d.values()):
                if p in dic:
                    ok = True
            if p.isalpha() and not (ok) and p != '':
                tipo, definicion = agregarPalabra(p)
                if tipo != '9999':
                    d[tipo][p] = definicion
                    # creo listas de la cantidad de sustantivo, adjetivos y verbos
                    sus.Update(values=list(range(len(list(d['sustantivo'].keys())) + 1)))
                    adj.Update(values=list(range(len(list(d['adjetivo'].keys())) + 1)))
                    verb.Update(values=list(range(len(list(d['verbo'].keys())) + 1)))
                    listbox.Update(['   Sustantivos: '] + list(d['sustantivo'].keys()) + ['  Adjetivos: '] + list(
                        d['adjetivo'].keys()) + ['  Verbos: '] + list(d['verbo'].keys()))

                    actualizarJSON(d)
            else:
                sg.Popup('ERROR. Palabra incorrecta, o ya definida. Ingrese otra!')
        elif event == 'Eliminar':

            p = values['palabra']  # Obtiene la palabra a borrar
            actualizar_text(window)
            ok = False
            for dic in list(d.values()):
                if p in dic:
                    ok = True
                    del dic[p]
            if ok:
                actualizarJSON(d)
                listbox.Update(
                    ['   Sustantivos: '] + list(d['sustantivo'].keys()) + ['  Adjetivos: '] + list(
                        d['adjetivo'].keys()) + [
                        '  Verbos: '] + list(d['verbo'].keys()))
                sus.Update(values=list(range(len(list(d['sustantivo'].keys())) + 1)))
                adj.Update(values=list(range(len(list(d['adjetivo'].keys())) + 1)))
                verb.Update(values=list(range(len(list(d['verbo'].keys())) + 1)))
        elif event == 'Reporte 1':
            window.Hide()
            mostrarReporte('datos/reporte.txt', values['font1'], values['font2'])
            window.Show()
        elif event == 'Reporte 2':
            window.Hide()
            mostrarReporte('datos/reporte1.txt', values['font1'], values['font2'])
            window.Show()
        elif event == 'Salir' or event == None:
            window.Close()
            break


if __name__ == '__main__':
    import sys

    sys.exit(config_main())
