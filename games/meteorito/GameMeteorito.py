import math
from enum import Enum
import pygame
from games.meteorito import Meteoritos
from games.meteorito.interfaces.InterfacePuntajeMet import InterfacePuntajeMet


# Selecciona el brazo que esta disparando
class DisparoSelector(Enum):
    IZQUIERDA = 1
    DERECHA = 2


class GameMeteorito(InterfacePuntajeMet):

    def __init__(self):
        # posiciones iniciales del personaje
        self.perPosX = 0
        self.perPosY = 0
        # variable que permite saber si ya disparo o no
        # en el caso que este el brazo extendido se mantiene la variable en false.
        # hasta que vuelva a poner en linea recta la posicion de los dos puntos
        self.disparoI = False
        self.disparoD = False
        # tiempo de duracion de disparo
        self.duraDisparo = 5
        # Tiempo duracion de linea.
        self.contTimeDisparoI = self.duraDisparo
        self.contTimeDisparoD = self.duraDisparo
        # sonido laser
        # inicializamos el modulo mixer
        pygame.mixer.init()
        # cargamos el sonido
        self.laserSound = pygame.mixer.Sound("./src/laser.mp3")
        self.explosionSound = pygame.mixer.Sound("./src/explosion.mp3")
        # emitio sonido
        self.isSonido = False
        self.colorLaser = (0, 0, 255)
        #screen general
        self.screen = None
        #puntaje de nivel
        self.puntajeGame = 0


        #objeto meteoritos
        self.objMeteoritos = [
            Meteoritos.Meteoritos(self),
            Meteoritos.Meteoritos(self),
            Meteoritos.Meteoritos(self)
        ]
        self.my_font = pygame.font.SysFont('Comic Sans MS', 10)


    #response interfaz puntaje from meteorito
    def responsePuntaje(self,puntaje) ->str:
        self.explosionSound.play()
        self.puntajeGame += 1


    def viewPuntuacion(self):
        text_surface = self.my_font.render(
            f"Puntaje {self.puntajeGame}", False, (255, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        print(f"Puntaje {self.puntajeGame}")



        '''
           Params.
           screen: Pantalla sobre la cual se quiere dibujar
           p1x, coordenada brazo
           p1y, coordenada brazo
           p2x, coordenada antebrazo
           p2y, coordenada antebrazo

           '''
    def calculaGrado(self, screen, p1, p2, p3, tamanoPoint, disparoSelector,callbackEcuGeneral):

        numerador1 = p2.y - p1.y
        denominador1 = p2.x - p1.x

        numerador2 = p3.y - p2.y
        denominador2 = p3.x - p2.x
        # calculamos la pendiente del antebrazo con el fin de determinar
        # a donde llegara nuestro laser mas adelante
        pendienteAntebrazo = (numerador2 / denominador2)
        # lo mismo con la pendiente del brazo
        pendienteBrazo = (numerador1 / denominador1)

        # calculamos el angulo y obtenemos los grados.
        angulo1 = math.atan(pendienteBrazo) * 180 / math.pi
        angulo2 = math.atan(pendienteAntebrazo) * 180 / math.pi

        # Segun sea la posicion de los puntos sera el cuadrante
        cuadrante = 0
        if p3.x > p2.x and p3.y < p2.y:
            cuadrante = 1
        if p3.x < p2.x and p3.y < p2.y:
            cuadrante = 2
        if p3.x < p2.x and p3.y > p2.y:
            cuadrante = 3
        if p3.x > p2.x and p3.y > p2.y:
            cuadrante = 4

        # realizamos los ajustes necesarios para la visualizacion de los angulos segun el
        # plano cartesiano.
        if angulo1 < 0 and cuadrante == 1:
            angulo2 = angulo2 * -1
            angulo1 = angulo1 * -1
        if angulo1 > 0 and cuadrante == 2:
            angulo2 = 180 - angulo2
            angulo1 = 180 - angulo1
        if angulo1 < 0 and cuadrante == 3:
            angulo1 = 180 - angulo1
            angulo2 = 180 - angulo2
        if angulo1 > 0 and cuadrante == 4:
            angulo1 = 360 - angulo1
            angulo2 = 360 - angulo2


        # disparo?
        disparo = False
        if (abs(angulo1 - angulo2) <= 20) and 0 < angulo1 < 180:
            xFinalRecta = 0
            # usamos el angulo del antebrazo con el arreglo de los cuadrantes para obtener un valor real
            # angulo 2 es el angulo del antebrazo
            if angulo2 != 90 and angulo1 != 90:
                # calculamos la pendiente con el angulo haciendo uso de tangente
                pendienteConAngulo = math.tan(angulo2 * math.pi / 180)
                # calculamos el punto que tendra x cuando y = 0 haciendo uso de la ecuación de la recta.
                xFinalRecta = (abs(p3.x * tamanoPoint) + self.perPosX + (abs(p3.y * tamanoPoint) + self.perPosY) / (
                    pendienteConAngulo))
            else:
                xFinalRecta = p3.x * tamanoPoint + self.perPosX
                # calculamos a donde estara x cuando y = 0 para que el laser llegue al final de la pantalla
                # y = m*(x-x1)+y1
                print("angulo ", angulo2)

            if disparoSelector == DisparoSelector.IZQUIERDA and not self.disparoI:
                # procuramos emitir el sonido una sola vez al disparar

                if self.contTimeDisparoI == self.duraDisparo - 1:
                    self.laserSound.play()
                # Cambiamos el valor de disparoI, ya que tiene que volver a la misma posicion si quiere disparar.
                # es decir para volver a disparar tiene que volver a poner en linea recta los brezos.
                # reducimos el tiempo que tiene que durar el disparo
                self.contTimeDisparoI -= 1
                if self.contTimeDisparoI <= 0:
                    self.disparoI = True
                    self.contTimeDisparoI = self.duraDisparo  # sonido de disparo

                # dibujamos la linea.
                pygame.draw.line(screen, self.colorLaser,
                                     (p3.x * tamanoPoint + self.perPosX, p3.y * tamanoPoint + self.perPosY),
                                     (xFinalRecta, 0), 5)


                pygame.draw.circle(screen,self.colorLaser,(p3.x*tamanoPoint+self.perPosX
                                                               ,p3.y*tamanoPoint+self.perPosY),20,5)

                # Ahora calculamos los valores de A,B,C con el fin de determinar la ecuacion general de la recta
                # A = y2 -y1
                A = p3.y * tamanoPoint + self.perPosY
                # B = x1 - x2
                B = xFinalRecta - (p3.x * tamanoPoint + self.perPosX)
                # C = x2*y1 - y2*x1
                C = -(p3.y * tamanoPoint + self.perPosY) * xFinalRecta
                # llamamos a la funcion con el fin de pasar los parametros de los valores para la ecuacion general
                callbackEcuGeneral(A, B, C)

            if disparoSelector == DisparoSelector.DERECHA and not self.disparoD:

                # procuramos emitir el sonido una sola vez al disparar
                if self.contTimeDisparoD == self.duraDisparo:
                    print("Dispara")
                    self.laserSound.play()
                    # Cambiamos el valor de disparoI, ya que tiene que volver a la misma posicion si quiere disparar.
                    # es decir para volver a disparar tiene que volver a poner en linea recta los brezos.
                    # reducimos el tiempo que tiene que durar el disparo
                self.contTimeDisparoD -= 1
                if self.contTimeDisparoD <= 0:
                    self.disparoD = True
                    self.contTimeDisparoD = self.duraDisparo

                # dibujamos la linea.
                pygame.draw.line(screen, self.colorLaser,
                                     (p3.x * tamanoPoint + self.perPosX, p3.y * tamanoPoint + self.perPosY),
                                     (xFinalRecta, 0), 5)

                pygame.draw.circle(screen, self.colorLaser, (p3.x * tamanoPoint + self.perPosX
                                                                 , p3.y * tamanoPoint + self.perPosY), 20, 5)

                # Ahora calculamos los valores de A,B,C con el fin de determinar la ecuacion general de la recta
                # A = y2 -y1
                A = p3.y * tamanoPoint + self.perPosY
                # B = x1 - x2
                B = xFinalRecta - (p3.x * tamanoPoint + self.perPosX)
                # C = x2*y1 - y2*x1
                C = -(p3.y * tamanoPoint + self.perPosY) * xFinalRecta
                # llamamos a la funcion con el fin de pasar los parametros de los valores para la ecuacion general
                callbackEcuGeneral(A, B, C)

        else:
        # En caso de que los puntos no esten en linea recta entonces vamos a reiniciar el poder disparar
            if (abs(angulo1 - angulo2)) > 20:
                if (disparoSelector == DisparoSelector.IZQUIERDA):
                    self.disparoI = False
                    self.contTimeDisparoI = self.duraDisparo
                if (disparoSelector == DisparoSelector.DERECHA):
                    self.disparoD = False
                    self.contTimeDisparoD = self.duraDisparo



    def colisionEvalue(self,A,B,C):
        for meteoritos in self.objMeteoritos:
            meteoritos.colision(A,B,C)


    def jugar(self,screen,points,tamanoPoint,perPosX,perposY):

        #screen init
        if self.screen is None:
            self.screen = screen

        self.perPosX = perPosX
        self.perPosY = perposY

        self.calculaGrado(screen, points.landmark[11],
                              points.landmark[13],
                              points.landmark[15],
                              tamanoPoint,DisparoSelector.DERECHA,
                              self.colisionEvalue)
        self.calculaGrado(screen, points.landmark[12],
                                    points.landmark[14],
                                    points.landmark[16],
                                    tamanoPoint,DisparoSelector.IZQUIERDA,
                                    self.colisionEvalue)

        #quedamos en la adicion de la colision
        for data in self.objMeteoritos:
            data.update(screen)

        #visualizamos la puntuacion
        self.viewPuntuacion()
        #Visualizar los puntajes
        #self.objMeteoritos[0].puntaje(screen)


