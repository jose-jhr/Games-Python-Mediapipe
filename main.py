import threading

import cv2
import mediapipe as mp

import PointsDetect
#importamos pygame
import pygame

#importamos el personaje
import Personaje


#importamos hilos con el fin de ejecutar la pantalla por un lado y
#mediapipe por otro lado



'''
  Configuracion de pygame
  '''
pygame.init()
anchoPantalla = 600
altoPantalla = 600
screen = pygame.display.set_mode((anchoPantalla, altoPantalla))

clock = pygame.time.Clock()
RUNNING = True
#tamano de cada punto de la imagen, es general y puede ser modificado
tamanoPoint = 50


'''
Conexiones del personaje
'''
personaje = Personaje.Personaje()


'''
Configuracion de video
'''
# Open webcam or video file
cap = cv2.VideoCapture(0)  # Use 0 for webcam or provide a video file path
#inicializamos el modelo que obtiene los puntos
pointsDetect = PointsDetect.PointsDetect()
mp_pose = mp.solutions.pose
mp_pose
mp_drawing = mp.solutions.drawing_utils

img = cv2.imread("src/men.png")




while cap.isOpened():
    ret, frame = cap.read()
    #if not ret:
    #    break
    #flip al frame


    # Convert the frame to RGB
    rgb_frame = frame

    #rgb_frame = img
    #llamamos al modelo para la deteccion del cuerpo humano
    results = pointsDetect.recognized(frame=frame)

    #rgb_frame = cv2.flip(rgb_frame, 1)
    # Display the frame
    cv2.imshow('Pose Detection', rgb_frame)


    '''
    ScreenDraw pygma
    '''
    #limpiamos la pantalla anteriormente dibujada
    screen.fill((0,0,0))

    #dibujamos el personaje
    personaje.drawPersonaje(screen,results,tamanoPoint,screen.get_width(),screen.get_height())


    #Actualizamos el screen de pygame
    pygame.display.flip()

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
