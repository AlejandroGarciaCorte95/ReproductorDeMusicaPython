# -*- coding: utf-8 -*-
"""
Reproductor de musica SmartPlayer

"""

from tkinter import *
from tkinter import ttk
import tkinter as tk

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
from pydub.playback import play
from pydub import *
import eyed3

from mutagen.easyid3 import EasyID3

from tflite_runtime.interpreter import Interpreter 
from PIL import Image, ImageTk
import numpy as np
import time
import cv2 as cv
import imutils
import random
import os

import mutagen
from mutagen.wave import WAVE


#-----------CLASES------------#

class Button(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self['background']
        self.bind('<Enter>', self.onEnter)
        self.bind('<Leave>', self.onLeave)
        self['relief'] = 'flat'

    def onEnter(self, e):
        self['background'] = self['activebackground']

    def onLeave(self, e):
        self['background'] = self.defaultBackground
        
class ButtonTrack(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self['background']
        self.defaultHeight = self['height']
        self.bind('<Enter>', self.onEnter)
        self.bind('<Leave>', self.onLeave)
        self['relief'] = 'flat'

    def onEnter(self, e):
        self['background'] = self['activebackground']
        self['height']  = (self.defaultHeight + 4)

    def onLeave(self, e):
        self['background'] = self.defaultBackground
        self['height'] = self.defaultHeight
        

#----------VARIABLES----------#

tipoDeLetra = 'arial'
cursorCruz = 'tcross'
cursorBotonMano = 'hand2'

flagTipoReproduccion = 0
trackActualIndex = -1
emocion = 'happy'
tracks = {}

#----------FUNCIONES----------#

#Abrir imagenes:
def abrirImagen(rutaImagen, ancho, alto):
    imagen = Image.open(rutaImagen)
    imagen = imagen.resize((ancho, alto), Image.ANTIALIAS)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen
    
def reproducirAudio(comienzo_ms=0, audiofile=""):
    global playing
    print('reproduciendo: ' + audiofile + '------------' + tracks[trackActualIndex][1])
    try:
        playing.stop()
        print('deteniendo audio')
    except:
        pass
    
    print("./MUSICA/"+audiofile)
    sound = AudioSegment.from_file("./MUSICA/"+audiofile, "wav", start_second=50)
    # sound = AudioSegment.from_file("./MUSICA/Pista1.wav", "wav", start_second=10)
    print(sound.duration_seconds)
    
    splice = sound[comienzo_ms:]
    playing = _play_with_simpleaudio(sound)
    
def forzarIndex(num):
    global trackActualIndex
    trackActualIndex = num
    print('el nuevo index es ' + str(trackActualIndex))
    
    reproducirAudio(audiofile=tracks[trackActualIndex][0])

def elegirPistaSiguiente():
    global trackActualIndex
    tempListaEmocion = []
    
    if flagTipoReproduccion == 0: #de corrido
        if trackActualIndex >= len(tracks) -1:
            trackActualIndex = 0
        elif trackActualIndex < 0:
            trackActualIndex = 0
        else:
            trackActualIndex += 1
        
    elif flagTipoReproduccion == 1: #aleatorio
        trackActualIndex += random.randint(0, len(tracks) -1)
        
    elif flagTipoReproduccion == 2: #reconocimiento emociones
        for key, value in tracks.items():
         if emocion == value[3]:
             tempListaEmocion.append(key)
        trackActualIndex = random.shuffle(tempListaEmocion)[0]
             
    reproducirAudio(audiofile=tracks[trackActualIndex][0])
        

def mostrarTracks():
    global tracks
    def a(name):
        print (name)
        
    archivosDeDirectorio = os.listdir('./MUSICA/')
    i = 0
    for archivo in archivosDeDirectorio:
        # audio = EasyID3("./MUSICA/" + archivo)  
        if '.wav' in archivo:
            tracks.setdefault(i, [archivo, "Nombre pista: Pista " + str(i), "Interprete: Desconocido", "happy"])
            i += 1
    
    print(tracks)

    row = 1
    
    # for name in tracks:
    #     user_button = Button(frame_Playlist,text=tracks[name][0].capitalize() + '\nAutor: ' + tracks[name][1].capitalize(), anchor="w", width=50,command=lambda name=name:a(name))
    #     user_button.grid(row = row, column = 0)
    #     row+=1
    
    cTableContainer = tk.Canvas(frame_Playlist,bg='purple')
    fTable = tk.Frame(cTableContainer)
    fTable.config(bg='cyan')
    # sbHorizontalScrollBar = tk.Scrollbar(frame_Playlist)
    sbVerticalScrollBar = tk.Scrollbar(frame_Playlist)

    # Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
    def updateScrollRegion():
    	cTableContainer.update_idletasks()
    	cTableContainer.config(scrollregion=fTable.bbox())

    # Sets up the Canvas, Frame, and scrollbars for scrolling
    def createScrollableContainer():
    	cTableContainer.config(yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    	# sbHorizontalScrollBar.config(orient=tk.HORIZONTAL, command=cTableContainer.xview)
    	sbVerticalScrollBar.config(orient=tk.VERTICAL, command=cTableContainer.yview)

    	# sbHorizontalScrollBar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
    	sbVerticalScrollBar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    	cTableContainer.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
    	cTableContainer.create_window(0, 0, window=fTable, anchor=tk.NW)

    # Adds labels diagonally across the screen to demonstrate the scrollbar adapting to the increasing size

    createScrollableContainer()
    for name in tracks:
        user_button = ButtonTrack(fTable,text=tracks[name][1].capitalize() + '\nAutor: ' + tracks[name][1].capitalize(), anchor="w", width=50, activebackground = 'red',command=lambda name=name:[forzarIndex(name)])
        user_button.grid(row = row, column = 0)
        row+=1
        
        updateScrollRegion()
    
def abrirCamara():
    def iniciar():
        global cap
        cap = cv.VideoCapture(1, cv.CAP_DSHOW)
        visualizar()
        
    def visualizar():
        global cap
        global frame
        if cap is not None:
            ret, frame = cap.read()
            if ret == True:
                frame = imutils.resize(frame, width=500, height=500, inter=cv.INTER_CUBIC)
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                # zoom =1
                # frame = cv.resize(frame, (1, 0), fx=zoom+1, fy=zoom)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                lblVideo.configure(image=img)
                lblVideo.image = img
                lblVideo.after(10, visualizar)
            else:
                lblVideo.image = ""
                cap.release()
                
    def finalizar():
        global cap
        cap.release()
        
    def capturarImagen():
        cv.imwrite("./TEMP/test.png", cv.cvtColor(frame, cv.COLOR_BGR2GRAY))
        
        time.sleep(400/1000)
        finalizar()
        
    cap = None
    ventanaCamara = Toplevel(ventanaMenu)
    ventanaCamara.title('Camara')
    ventanaCamara.resizable(width = False, height = False)
    ventanaCamara.focus_set()
    ventanaCamara.grab_set()
    ventanaCamara.transient(master=ventanaMenu)
    btnFoto = Button(ventanaCamara, text="Capturar emocion", width=70, activebackground='sky blue', command=capturarImagen)
    btnFoto.grid(column=0, row=1, padx=5, pady=5)
    lblVideo = Label(ventanaCamara)
    lblVideo.grid(column=0, row=0, columnspan=2)

    iniciar()

    identificarEmocion()
    ventanaCamara.mainloop()
    
    
def identificarEmocion():
    def load_labels(path): # Read the labels from the text file as a Python list.
      with open(path, 'r') as f:
        return [line.strip() for i, line in enumerate(f.readlines())]

    def set_input_tensor(interpreter, image):
      tensor_index = interpreter.get_input_details()[0]['index']
      input_tensor = interpreter.tensor(tensor_index)()[0]
      input_tensor[:, :] = image

    def classify_image(interpreter, image, top_k=1):
      set_input_tensor(interpreter, image)
      interpreter.invoke()

      output_details = interpreter.get_output_details()[0]
      output = np.squeeze(interpreter.get_tensor(output_details['index']))
      
      scale, zero_point = output_details['quantization']
      output = scale * (output - zero_point)
      ordered = np.argpartition(-output, 1)
      return [(i, output[i]) for i in ordered[:top_k]][0]

    data_folder = "./MODELO/"
    testImg = "./TEMP/test.png"

    model_path = data_folder + "model.tflite"
    label_path = data_folder + "labels.txt"

    interpreter = Interpreter(model_path)
    print("Model Loaded Successfully.")

    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    print("Image Shape (", width, ",", height, ")")

    # Load an image to be classified.
    image = Image.open(testImg).convert('RGB').resize((width, height))

    # Classify the image.
    time1 = time.time()
    label_id, prob = classify_image(interpreter, image)
    time2 = time.time()
    classification_time = np.round(time2-time1, 3)
    print("Classificaiton Time =", classification_time, "seconds.")

    # Read class labels.
    labels = load_labels(label_path)

    # Return the classification label of the image.
    classification_label = labels[label_id]
    print("Image Label is :", classification_label, ", with Accuracy :", np.round(prob*100, 2), "%.")

    img = cv.imread(testImg)
    texto = ('{}, {} {}').format(classification_label, np.round(prob*100, 2), '%')
    cv.putText(img, texto, (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

    
#--------------------------------------------

ventanaMenu = Tk()
ventanaMenu.title('Smart Music')
ventanaMenu.minsize(height=400, width=900)
#ventanaMenu.config(bg = 'white')
#ventanaMenu.wm_attributes('-alpha', 0.97)
#ventanaMenu.attributes('-fullscreen', True)
ventanaMenu.after(1, lambda: ventanaMenu.focus_force())
# bit99 = ventanaMenu.iconbitmap('SmartMusicIcono.ico')
#ventanaMenu.iconphoto(True, tk.PhotoImage(file='SmartMusicIcono.png'))

frame_Izquierdo = Frame(ventanaMenu, width=200, height=200, relief='groove') 
frame_Izquierdo.pack(fill='y', side='left')
frame_Izquierdo.config(bg = 'black')

frame_Playlist = Frame(frame_Izquierdo, width=200, height=200, relief='groove') 
frame_Playlist.pack(fill='y', side='left')
frame_Playlist.config(bg = 'orange')

frame_Reproductor = Frame(ventanaMenu, relief='groove') 
frame_Reproductor.pack(fill='both', side='right', expand=1)
frame_Reproductor.config(bg = 'red')

frame_Controles = Frame(frame_Reproductor, height=100, relief='groove') 
frame_Controles.pack(fill='x',  side='bottom', expand=0)
frame_Controles.config(bg = 'blue')

frame_BarraTiempo = Frame(frame_Controles, height=10, relief='groove') 
frame_BarraTiempo.pack(fill='both', side='right', expand=1)
frame_BarraTiempo.config(bg = 'pink')

frame_Barra = Frame(frame_BarraTiempo, height=10, relief='groove') 
#frame_Barra.pack(fill='both', side='top', expand=1)
frame_Barra.config(bg = 'purple')

frame_Directorio = Frame(frame_Reproductor, height=20, relief='groove') 
frame_Directorio.pack(fill='both',  anchor='center', expand=0)
frame_Directorio.config(bg = 'yellow')

frame_Pista = Frame(frame_Reproductor, height=10, relief='groove') 
frame_Pista.pack(fill='both',  side='top', expand=1)
frame_Pista.config(bg = 'green')

frame_Disco = Frame(frame_Pista, width=300, height=300, relief='groove') 
frame_Disco.pack(anchor='nw', expand=0)
frame_Disco.config(bg = 'sky blue')

mostrarTracks()


frameCnt = 45
frames = [PhotoImage(file="./IMAGENES/DISCO/discoOptimizado.gif",format = 'gif -index %i' %(i)).zoom(1) for i in range(frameCnt)]
def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    frame_Disco.after(20, update, ind)
label = Label(frame_Disco, bg='sky blue')
label.pack()
frame_Disco.after(0, update, 0)

lblInicio = Label(frame_BarraTiempo, text='00:00', bg='green')
# lblInicio.pack()
# lblInicio.grid(row=1,column=0)
lblInicio.pack(side = LEFT, expand = False, fill = BOTH)

def show_values():
    print(str(sliderBarraProgreso.get()))

btnPlayPausa = Button(frame_Controles, text=' ▶ ',font = (tipoDeLetra, 20), activebackground='blue')
btnPlayPausa.pack()

sliderBarraProgreso = Scale(frame_Barra, from_=0, to=1000, orient=HORIZONTAL, bg='red', relief='flat', bd=0, showvalue=0, sliderlength=10, width=10, activebackground='blue', command=lambda _:show_values())
sliderBarraProgreso.set(23)
sliderBarraProgreso.pack(fill='both',anchor='e', expand=1)

# frame_Barra.pack(fill='both', side='top')
# frame_Barra.grid(row=1,column=1,sticky='we')
frame_Barra.pack(side = LEFT, expand = True, fill = BOTH)

lblFin = Label(frame_BarraTiempo, text='99:59', bg='green')
lblFin.pack(side = LEFT, expand = False, fill = BOTH)

btnDeteccionEmociones = Button(frame_Reproductor, text='Como me siento', command=abrirCamara)
btnDeteccionEmociones.pack()

btnSiguiente = Button(frame_Reproductor, text='siguiente', command=elegirPistaSiguiente)
btnSiguiente.pack()

ventanaMenu.mainloop()
