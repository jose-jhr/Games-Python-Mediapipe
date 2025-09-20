import math
import random
import pygame.image
from Config import Config
from games.meteorito.interfaces.InterfacePuntajeMet import InterfacePuntajeMet


class Meteoritos:

    def __init__(self,obj_b:InterfacePuntajeMet):
        #inicializamos la interface para la respuesta de puntaje
        self.interfacePuntajeMet = obj_b
        self.anchoPantalla = Config().anchoPantalla
        self.altoPantalla= Config().altoPantalla
        print("ancho pantalla",self.anchoPantalla)

        #Movimiento del meteorito
        self.movMeteorito = 10
        self.metorito = pygame.image.load("./src/meteorito.png")
        #tamano aleatorio imagen, entre
        self.sizeMeteorito = (40,40)
        #tamano del meteorito, izquierda pequeno valor derecha grande valor
        size = random.randint(self.sizeMeteorito[0],self.sizeMeteorito[1])
        self.metorito = pygame.transform.scale(self.metorito,(size,size))
        self.rectMeteorito = self.metorito.get_rect()
        self.posx = 0
        self.posy = 0
        #iniciamos los valores random
        self.randomPosx()
        self.randomPosY()
        #rectangulo del meteorito
        self.rectMeteorito.x = self.posx
        self.rectMeteorito.y = self.posy
        #variable que sera usada para la reduccion de la escala
        self.limiteReduScale = 10
        #limite inferior de y para su generación aleatoria
        self.limitY = -30
        #puntaje
        self.puntos = 0

    #cambiamos la posicion de inicio del meteorito
    def randomPosx(self):
        #self.randomSize()
        self.posx = random.randint(0, self.anchoPantalla - self.metorito.get_width())

    def randomPosY(self):
        self.posy = random.randint(0,10)

    def randomSize(self):
        #size = random.randint(self.widthMeteorito[0],self.widthMeteorito[1])
        self.metorito = pygame.transform.scale(self.metorito, (self.sizeMeteorito[0], self.sizeMeteorito[1]))

    def reinitMeteorito(self):
        # obtenemos una posicion aleatoria de la nueva posicion en y
        self.randomPosY()
        self.rectMeteorito.y = self.posy
        # cambiamos la posicion del meteorito
        self.randomPosx()
        self.rectMeteorito.x = self.posx

    def update(self,screen):
        self.rectMeteorito.y += self.movMeteorito
        screen.blit(self.metorito,(self.posx,self.rectMeteorito.y))
        if(self.rectMeteorito.y>self.altoPantalla):
            self.reinitMeteorito()

    def positionMeteorito(self):
        return self.rectMeteorito.x,self.rectMeteorito.y

    def colision(self, A, B, C):
        #calculamos la distancia sobre la que pasa el laser....
        #distancia = abs((A*x+B*y+C)/(math.sqrt(pow(A,2)+pow(B,2))))
        distancia = (A*self.rectMeteorito.x+B*self.rectMeteorito.y+C)/(math.sqrt(pow(A,2)+pow(B,2)))
        if -40<distancia<0:
            self.puntos +=1
            self.interfacePuntajeMet.responsePuntaje(self.puntos)
            self.reinitMeteorito()




        '''
        print(f"Valores: A = {A} - B = {B} -> {xfinalRecta} - {p3x} "
              f"C = {C} - xMet = {self.rectMeteorito.x} -"
              f" yMet = {self.rectMeteorito.y}"
              f" Distancia = {distancia} - "
              f" xfinal = {xfinalRecta} p3x = {p3x}  p3y = {p3y}"
              )
        '''

