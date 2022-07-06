# -*- coding: utf-8 -*-
"""
@author: Alejandro Garcia

reconocimiento
"""

import cv2
import os
import numpy as np
from tkinter import *

def obtenerEmocion:
    emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    emotion_recognizer.read("C:/Users/Alejandro Garcia/Downloads/modeloLBPH.xml")
    # --------------------------------------------------------------------------------
    
    dataPath = 'C:/Users/Alejandro Garcia/Desktop/PROYECTO PDI/DATA'
    imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)
    emociones = ['ENOJO', 'FELICIDAD', 'SORPRESA', 'TRISTEZA']
    
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    
    while True:
    
        ret,frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
    
        nFrame = cv2.hconcat([frame, np.zeros((480,300,3),dtype=np.uint8)])
    
        faces = faceClassif.detectMultiScale(gray,1.3,5)
    
        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = emotion_recognizer.predict(rostro)
    
            cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
    
            if result[1] < 150:
                cv2.putText(frame,'{}'.format(emociones[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                print(emociones[result[0]])
            else:
                cv2.putText(frame,'No identificado',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                nFrame = cv2.hconcat([frame,np.zeros((480,300,3),dtype=np.uint8)])
    
        cv2.imshow('nFrame',nFrame)
        k = cv2.waitKey(1)
        if k == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()


root = Tk()
root.geometry("200x100")
exit_button = Button(root, text="Exit", command=obtenerEmocion)
exit_button.pack(pady=20)
root.mainloop()