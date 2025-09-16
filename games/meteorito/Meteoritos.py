import math
import random
import pygame.image
from Config import Config


class Meteoritos:

    def __init__(self):
        self.anchoPantalla = Config().anchoPantalla
        self.altoPantalla= Config().altoPantalla
        print("ancho pantalla",self.anchoPantalla)

        #Movimiento del meteorito
        self.movMeteorito = 10
        self.metorito = pygame.image.load("./src/meteorito.png")
        #tamano aleatorio imagen
        self.widthMeteorito = (40,100)
        #tamano del meteorito, izquierda pequeno valor derecha grande valor
        size = random.randint(self.widthMeteorito[0],self.widthMeteorito[1])
        self.metorito = pygame.transform.scale(self.metorito,(size,size))
        self.rectMeteorito = self.metorito.get_rect()
        self.posx = 0
        self.posy = -2
        #rectangulo del meteorito
        self.rectMeteorito.x = self.posx
        self.rectMeteorito.y = self.posy
        #ponemos aleatoriamente la posicion de la piedra inicial
        self.randomPosx()

    def randomPosx(self):
        self.posx = random.randint(0, self.anchoPantalla - self.metorito.get_width())
        self.randomSize()

    def randomSize(self):
        size = random.randint(self.widthMeteorito[0],self.widthMeteorito[1])
        print("tamano aleatorio ",size)
        self.metorito = pygame.transform.scale(self.metorito, (size, size))

    def update(self,screen):
        self.rectMeteorito.y += self.movMeteorito
        screen.blit(self.metorito,(self.posx,self.rectMeteorito.y))
        if(self.rectMeteorito.y>self.altoPantalla):
            self.rectMeteorito.y = self.posy
            #cambiamos la posicion del meteorito
            self.randomPosx()
