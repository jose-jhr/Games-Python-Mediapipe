import mediapipe as mp
import pygame
from enum import Enum
from games.meteorito import GameMeteorito


#Selecciona el brazo que esta disparando
class DisparoSelector(Enum):
    IZQUIERDA = 1
    DERECHA = 2




class Personaje:

    def __init__(self):
        self.anchoPersonaje = 0
        self.altoPersonaje = 0
        self.mp_pose = mp.solutions.pose

        #los datos menores para el dibujo
        self.menorX = float('inf')
        self.mayorX = float('inf')
        self.menorY = float('inf')
        self.mayorY = float('inf')
        self.endFor = False
        #posiciones iniciales del personaje
        self.perPosX = 0
        self.perPosY = 0
        #self color personaje
        self.colorLineas = (255,255,255)
        self.colorLaser = (0, 255, 0)
        self.colorCirculos = (180,180,180)
        #pantalla
        self.anchoPantalla = 0
        self.altoPantalla = 0
        #juego de meteoritos
        self.gameMetorito = GameMeteorito.GameMeteorito()


    """
        Dibujamos la cabeza del personaje
        Arg:
        screen pantalla sobre la que se dibuja
        tamanoPoint: Dimension sobre la que se ajustan los valores
         
    """
    def drawHead(self,screen,landmark,tamanoPoint):
        #calculamos el radio de la cabeza como referncia los puntos extremos de la cabeza
        radioHead = abs(landmark[7].x - landmark[8].x)*tamanoPoint*1.5
        #centro de la circunferencia o punto inicial sera la nariz.
        center_circle = self.perPosX+landmark[0].x* tamanoPoint,self.perPosY+landmark[0].y*tamanoPoint
        #dibujamos circunferencia
        pygame.draw.circle(screen,self.colorCirculos,center_circle,radioHead)
        #dibujamos el ojo izquiedo
        pygame.draw.circle(screen,(255,0,0),(self.perPosX+landmark[5].x*tamanoPoint,self.perPosY+landmark[5].y*tamanoPoint),1)
        pygame.draw.circle(screen,(255,0,0),(self.perPosX+landmark[2].x*tamanoPoint,self.perPosY+landmark[2].y*tamanoPoint),1)
        #dibujamos boca
        pygame.draw.aalines(screen,(255,0,0),False,([(self.perPosX+landmark[10].x*tamanoPoint,self.perPosY+landmark[10].y*tamanoPoint),
                                                     (self.perPosX+landmark[9].x*tamanoPoint,self.perPosY+landmark[9].y*tamanoPoint)]),3)


    def drawBody(self,screen,landmark,tamanoPoint):
        #capturamos el centro de la parte de abajo del cuerpo pos 24 y 23
        minX = min(landmark[23].x ,landmark[24].x, landmark[12].x,landmark[11].x)
        maxX = max(landmark[23].x ,landmark[24].x, landmark[12].x,landmark[11].x)
        minY = min(landmark[23].y ,landmark[24].y, landmark[12].y,landmark[11].y)
        maxY = max(landmark[23].y ,landmark[24].y, landmark[12].y,landmark[11].y)
        anchoPersonaje = (abs(maxX - minX))*tamanoPoint
        altoPersonaje = (abs(maxY - minY))*tamanoPoint
        pygame.draw.rect(screen,self.colorLineas,(self.perPosX+minX*tamanoPoint,self.perPosY+minY*tamanoPoint,anchoPersonaje,altoPersonaje))


        #capturamos el centro de la parte de abajo del cuerpo pos 12 y 11

    def drawLines(self, screen, landmarkX, landmarkY, tamanoPoint):
        # Extraemos las coordenadas de los puntos
        x1 = landmarkX.x
        y1 = landmarkX.y
        x2 = landmarkY.x
        y2 = landmarkY.y

        # Calcular las posiciones ajustadas con los factores de escala
        pos_x1 = x1 * tamanoPoint + self.perPosX
        pos_y1 = y1 * tamanoPoint + self.perPosY
        pos_x2 = x2 * tamanoPoint + self.perPosX
        pos_y2 = y2 * tamanoPoint + self.perPosY

        # Dibujar la línea con suavizado (antialiasing)
        pygame.draw.aalines(screen, self.colorLineas, False, [(pos_x1, pos_y1), (pos_x2, pos_y2)], 3)  # 3 es el grosor

        # Dibujar círculos en los extremos para simular los bordes redondeados
        radio = 5  # Radio de los círculos
        pygame.draw.circle(screen, self.colorCirculos, (pos_x1, pos_y1), radio)  # Extremo izquierdo
        pygame.draw.circle(screen, self.colorCirculos, (pos_x2, pos_y2), radio)  # Extremo derecho



    def drawPersonaje(self,screen,results,tamanoPoint,ancho,alto):

        #tamaño de pantalla
        self.anchoPantalla = ancho
        self.altoPantalla = alto

        # recorremos los puntos que se obtuvieron del modelo
        # Dibuja las conexiones y puntos en Pygame
        if results.pose_landmarks:
            # posicion inicial del personaje
            self.perPosX = ancho / 2
            self.perPosY = alto - results.pose_landmarks.landmark[31].y * tamanoPoint

            # dibujamos el piso
            pygame.draw.line(screen, (0, 255, 0), (0, alto), (ancho, alto), 10)
            #dibujamos la cabeza
            self.drawHead(screen,results.pose_landmarks.landmark,tamanoPoint)
            #dibujamos el cuerpo
            self.drawBody(screen,results.pose_landmarks.landmark,tamanoPoint)
            #brazo 1
            self.drawLines(screen,results.pose_landmarks.landmark[11],results.pose_landmarks.landmark[13],tamanoPoint)
            #brazo 2
            self.drawLines(screen,results.pose_landmarks.landmark[12],results.pose_landmarks.landmark[14],tamanoPoint)
            #antebrazo 1
            self.drawLines(screen, results.pose_landmarks.landmark[13], results.pose_landmarks.landmark[15],
                            tamanoPoint)
            #antebrazo 2
            self.drawLines(screen, results.pose_landmarks.landmark[14], results.pose_landmarks.landmark[16],
                            tamanoPoint)
            #muslo 2
            self.drawLines(screen, results.pose_landmarks.landmark[24], results.pose_landmarks.landmark[26],
                            tamanoPoint)
            #pantorrila 2
            self.drawLines(screen, results.pose_landmarks.landmark[26], results.pose_landmarks.landmark[28],
                            tamanoPoint)
            #muslo 1
            self.drawLines(screen, results.pose_landmarks.landmark[23], results.pose_landmarks.landmark[25],
                            tamanoPoint)
            #muslo 2
            self.drawLines(screen, results.pose_landmarks.landmark[25], results.pose_landmarks.landmark[27],
                            tamanoPoint)



            '''
            Caso 1 Juego de disparos con las manos derriba meteoritos...
            '''
            self.gameMetorito.jugar(screen,results.pose_landmarks,tamanoPoint,self.perPosX,self.perPosY)





