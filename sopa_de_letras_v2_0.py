import PySimpleGUI as sg
import os
import string
import random
import sys
import json
from main_sopa_de_letras import main_sopa

def largoMax(palabras):
    '''Funcion encargada de obtener la longitud de la palabra mas larga de las seleccionadas'''
    max = -1
    for elem in palabras:
        if (len(elem[0]) > max):
            max = len(elem[0])
    return max

def cargarD():
    '''Funcion encargada de devolver desde un Archivo formato JSON, un Diccionario con las palabras a utilizar en la Sopa De Letras'''

    file = open("datos/palabras.json", "r")
    d = json.load(file)
    file.close()
    return d

def cargarConfiguraciones():
    '''Funcion encargada de devolver desde un Archivo formato JSON, un Diccionario con las configuraciones a utilizar en la Sopa De Letras'''
    file = open("datos/configuracion.json", "r")
    d = json.load(file)
    file.close()
    return d


def ArmarPorClasificacion(lista, cantidad,tipo):
    '''Selecciona aleatoriamente las palabras de un determinado tipo, segun la cantidad indicada en la configuracion'''
    l = []
    for vez in range(int(cantidad)):
        palabra = random.choice(lista)
        l.append((palabra, tipo))
        lista.remove(palabra)

    return l

def armarPalabras(d,config):
    '''Devuelve una lista con la cantidad final de palabras a utilizar'''
    return ArmarPorClasificacion(list(d['sustantivo'].keys()), config['Cantidad_Sustantivos'],'SUSTANTIVO') + \
           ArmarPorClasificacion(list(d['adjetivo'].keys()),config['Cantidad_Adjetivos'],'ADJETIVO' ) + \
           ArmarPorClasificacion(list(d['verbo'].keys()),config['Cantidad_Verbos'],'VERBO' )

def randomLetra(mayus):
    '''Devuelve una letra al azar, mayuscula o minuscula dependiendo de la configuracion de usuario'''
    letra = random.choice(string.ascii_lowercase)
    if(mayus == 'mayuscula'):
        letra = letra.upper()

    return letra

def rotar_matriz(m, cant=3):
    '''Funcion encargada de rotar la matriz, para modificar la orientacion de las palabras en la Sopa de Letras'''
    new=m
    for x in range(cant):
        new = [[new[j][i] for j in range(len(new))] for i in range(len(new[0]) -1, -1, -1)]

    return new


def ArmarMatriz(palabras,config):
    '''Funcion encargada de crear las matrices necesarias para el funcionamiento correcto del Juego.
    Cada matriz tendra un proposito particular:
        La matriz JUEGO, contiene la Sopa de Letras
        La matriz RESPUESTAS, contiene en sus posiciones un valor que indica si en esa misma existe una letra valida (o no)
        La matriz DE USUARIO contendra los valores ingresados por el Usuario'''
    max = largoMax(palabras)


    numero_columnas = len(palabras)
    numero_filas = max + 5

    #matriz donde va aparecer la sopa de letras
    matriz_juego =  [[None] * numero_filas for i in range(numero_columnas)]
    #matriz donde va a  aparecer la entrada del usuario
    matriz_usuario = [[None] * numero_filas for i in range(numero_columnas)]
    #matriz donde va a estar las respuestas
    matriz_respuestas = [[None] * numero_filas for i in range(numero_columnas)]

    for x in range(numero_columnas):
        palabra, tipo = random.choice(palabras)
        palabras.remove((palabra, tipo))

        pos = random.randint(0, numero_filas - len(palabra))
        num = 0
        l = []
        for y in range(numero_filas):

            if (y < pos or y >= (pos + len(palabra))):
                letra = randomLetra(config['Mayuscula'])

            else:
                letra = palabra[num]
                if config['Mayuscula'] == 'mayuscula':
                    letra = letra.upper()
                else:
                    letra = letra.lower()
                num = num + 1
                matriz_respuestas[x][y] = tipo


            matriz_juego[x][y] = letra




    if config['Tipo_Orientacion'] == 'Horizontal':
        matriz_juego = rotar_matriz(matriz_juego)
        matriz_respuestas = rotar_matriz(matriz_respuestas)
        matriz_usuario = rotar_matriz(matriz_usuario)

    return (matriz_juego,matriz_usuario,matriz_respuestas)

def cargarLayout(matriz_juego):
    '''Procedimiento que devuelve la plantilla, a partir de los valores de la Matriz JUEGO'''
    layout = []
    largo = len(matriz_juego)
    alto = len(matriz_juego[0])

    for y in range(alto):
        l = []
        for x in range(largo):

            l.append(sg.Text(key=(x, y), auto_size_text=True, enable_events=True, text=matriz_juego[x][y],
                                 text_color='black', font='Ubuntu', background_color='white', size=(5, 1),
                                 justification='center', pad = (0,0)))
        layout.append(l)
    return layout



def termine(matriz_juego,matriz_usuario,matriz_respuestas):
    '''El proceso termine creara una nueva ventana, indicando los errores o aciertos del Usuario
        Naranja: Falta seleccionar una letra en la palabra / Palabras nunca seleccionadas
        Rojo: Cuando se selecciona una letra/palabra no definida
        Verde: Acierto
        Blanco: No tiene relevancia

        Se indican, con distintos colores, cual es el tipo correcto de la palabra, en caso de que el usuario se equivoque
        '''
    layout = [[sg.Frame('Correción Sopa de Letras', font =('Ubuntu',10), title_location= 'n', layout = [
                  [sg.Text(text='Te equivocaste de tipo', text_color='black', font=('Ubuntu',10),
                          justification='center')],
                 [sg.Text("\t"), sg.Text(text='', background_color='blue', size=(1, 1)),
                  sg.Text(text='Es un Sustantivo ', text_color='black',
                          justification='center')],
                [sg.Text("\t"), sg.Text(text='', background_color='pink', size=(1, 1)),
                 sg.Text(text='Es un Adjetivo ', text_color='black',
                         justification='center')],
                [sg.Text("\t"), sg.Text(text='', background_color='purple', size=(1, 1)),
                 sg.Text(text='Es un Verbo ', text_color='black',
                         justification='center')],
                 [sg.Text(text='', background_color="red", size=(1, 1)),
                  sg.Text(text='No existe </3', text_color='black', font=('Ubuntu',10),
                          justification='center')],

                 [sg.Text(text='', background_color='green', size=(1, 1)),
                  sg.Text(text='Acertaste', text_color='black',
                          justification='center')],
                 [sg.Text(text='', background_color="orange", size=(1, 1)), sg.Text(text='Te falto seleccionar',
                                                                                    text_color='black',
                                                                                    justification='center')]])]
    ]

    largo = len(matriz_juego)
    alto = len(matriz_juego[0])
    for y in range(alto):
        l = []
        for x in range(largo):
            if matriz_usuario[x][y] == None and matriz_respuestas[x][y] == None:
                color = "white"
            elif matriz_usuario[x][y] == matriz_respuestas[x][y]:
                color = 'green'
            elif matriz_usuario[x][y] == None and matriz_respuestas[x][y] != None:
                color = 'orange'
            elif matriz_usuario[x][y] != None and matriz_respuestas[x][y] == None:
                color = 'red'

            else:
                if matriz_respuestas[x][y] == 'SUSTANTIVO':
                    color = 'blue'
                elif matriz_respuestas[x][y] == 'ADJETIVO':
                    color = 'pink'
                elif matriz_respuestas[x][y] == 'VERBO':
                    color = 'purple'

            l.append(sg.Text(key=(x, y), auto_size_text=True, enable_events=False, text=matriz_juego[x][y],
                             text_color='black', font='Ubuntu', background_color=color, size=(5, 1),
                             justification='center', pad=(0, 0)))
        layout.append(l)


    layout.append([sg.Button("Volver a jugar", button_color=('white', 'blue')),sg.Button("SALIR", button_color=('white', 'red'))])

    window = sg.Window('Resultado de la sopa de letras', auto_size_text=True, default_element_size=(10, 10)).Layout(layout)

    while True:
        event,value = window.Read()
        if event == 'Volver a jugar':
            window.Close()
            break
        elif event == 'SALIR' or event == None:
            os._exit(1)


def devolverDefiniciones(dicpalabra, palabras):
    '''Funcion que por cada palabra de la lista de palabras, busca en el diccionario su definicion y lo retorna en una lista'''
    listadef = []

    for palabra in palabras:
        for clave in dicpalabra:
            if palabra[0] in dicpalabra[clave]:
                listadef.append('-'+str(dicpalabra[clave][palabra[0]]))


    return listadef

def main():
    '''Procedimiento central encargado de generar y mostrar la Sopa de Letras al Usuario, dependiendo de la configuracion de la misma,
    y su correccion. '''


    try:
        dicpalabra = cargarD()
        config = cargarConfiguraciones()
        palabras = armarPalabras(dicpalabra,config)
        matriz_juego,matriz_usuario,matriz_respuestas = ArmarMatriz(palabras.copy(),config)
        layout = cargarLayout(matriz_juego)
        layout.append([sg.Button("SUSTANTIVO", button_color=('white', config["Color_SUSTANTIVO"])),
                       sg.Button("VERBO", button_color=('white', config["Color_VERBO"])),
                       sg.Button("ADJETIVO", button_color=('white', config['Color_ADJETIVO']))])


        if config['Ayuda'] == 'Si':
            listadef = devolverDefiniciones(dicpalabra,palabras)
            layout.append([sg.Text('Ayuda', justification='left'), sg.Listbox(values=listadef, size=(70, 5), auto_size_text= True)])
        else:
            layout.append([sg.Text('Cantidad de sustantivos ' + str(config['Cantidad_Sustantivos'])),
                          sg.Text('Cantidad de verbos ' + str(config['Cantidad_Verbos'])),
                          sg.Text('Cantidad de adjetivos ' + str(config['Cantidad_Adjetivos']))])
        layout.append(
            [sg.Button("TERMINE", button_color=('white', 'green')), sg.Button("SALIR", button_color=('white', 'red'))])

        window = sg.Window('sopa de letras', auto_size_text=True, default_element_size=(20, 1)).Layout(layout)
        #valor de tipo por default
        tipo = 'SUSTANTIVO'
        while True:
            event, values = window.Read()

            if event == 'TERMINE':
                window.Close()
                termine(matriz_juego,matriz_usuario,matriz_respuestas)
                break
            elif event == 'SUSTANTIVO':
                tipo = 'SUSTANTIVO'

            elif event == 'ADJETIVO':
                tipo = 'ADJETIVO'

            elif event == 'VERBO':
                tipo = 'VERBO'

            elif event == 'SALIR' or event == None:
                window.Close()
                break
            else:
                elemento = window.FindElement(event)

                # si la matriz del usuario en esa posicion es None significa que nunca fue seleccionada
                if(matriz_usuario[event[0]][event[1]] == None):
                    matriz_usuario[event[0]][event[1]] = tipo
                    elemento.Update(background_color=config['Color_'+ tipo])
                else:
                    matriz_usuario[event[0]][event[1]]  = None
                    elemento.Update(background_color='white')

    except FileNotFoundError:
        sg.PopupError('Error faltan archivos')







if __name__ == '__main__':
    import sys
    sys.exit(main())
