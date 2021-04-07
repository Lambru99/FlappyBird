import pygame
import random

# Serve per poter utilizzare la libreria pygame

pygame.init()

# Variabili contenenti immagini e tutto cio che ritorna utile per costruire la scena

sfondo = pygame.image.load('immagini/sfondo.png')
uccello = pygame.image.load('immagini/uccello.png')
base = pygame.image.load('immagini/base.png')
gameover = pygame.image.load('immagini/gameover.png')
tubo_giu = pygame.image.load('immagini/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)
schermo =pygame.display.set_mode((288, 512))

# Variabili che permettono di settare FPS, la velocita di avanzamento del gioco e il font della scritta del punteggio

FPS = 50
Vel_Avanzamento = 3
Font = pygame.font.SysFont('Comic Sans MS', 50, bold=False)

# Classe per creare i tubi

class tubi_classe:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75,150)
    def avanza_e_disegna(self):
        self.x -= Vel_Avanzamento
        schermo.blit(tubo_giu, (self.x,self.y+220))
        schermo.blit(tubo_su, (self.x,self.y-220))
    def collisione(self, uccello, uccellox, uccelloy):
        tolleranza = 5
        uccello_lato_dx = uccellox+uccello.get_width()-tolleranza
        uccello_lato_sx = uccellox+tolleranza
        tubi_lato_dx = self.x+tubo_giu.get_width()
        tubi_lato_sx=self.x
        uccello_lato_su=uccelloy+tolleranza
        uccello_lato_giu= uccelloy+uccello.get_height()-tolleranza
        tubo_lato_su = self.y+100
        tubo_lato_giu=self.y+220
        if (uccello_lato_dx > tubi_lato_sx) and (uccello_lato_sx < tubi_lato_dx):
            if uccello_lato_su < tubo_lato_su or uccello_lato_giu > tubo_lato_giu:
                hai_perso()
    def fra_i_tubi(self, uccello, uccellox):
        tolleranza = 5
        uccello_lato_dx = uccellox + uccello.get_width() - tolleranza
        uccello_lato_sx = uccellox + tolleranza
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        if (uccello_lato_dx > tubi_lato_sx) and (uccello_lato_sx < tubi_lato_dx):
            return True

# Funzione utilizzata per aggiornare la scena

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

# Funzione che viene avviata all'inizio

def inizializza():
    global uccellox, uccelloy, uccello_vely, basex
    global tubi
    global punti
    global fra_tubi
    uccellox, uccelloy,= 60, 150
    uccello_vely = 0
    basex=0
    punti=0
    tubi = []
    tubi.append(tubi_classe())
    fra_tubi = False

inizializza()


# Funzione per disegnare oggetti nello schermo

def disegna_oggetti():
    schermo.blit(sfondo, (0,0))
    for t in tubi:
       t.avanza_e_disegna()
    schermo.blit(uccello, (uccellox, uccelloy))
    schermo.blit(base, (basex,400))
    punti_render = Font.render(str(punti),1,(255,255,255))
    schermo.blit(punti_render, (144,0))

# Funzione per fermare il gioco se si perde

def hai_perso():
    schermo.blit(gameover, (50,180))
    aggiorna()
    ricominciare = False
    while not ricominciare:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                inizializza()
                ricominciare = True
            if event.type == pygame.QUIT:
                pygame.quit()

# Ciclo che permette il perpetuo funzionamento del gioco

while True:
    basex -= Vel_Avanzamento
    uccello_vely +=1
    uccelloy += uccello_vely
    if basex < -45:
        basex = 0
    for event in pygame.event.get():
        if ( event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            uccello_vely = -10
        if event.type == pygame.QUIT:
            pygame.quit()

    if tubi[-1].x < 150:
        tubi.append(tubi_classe())


    for tubo in tubi:
        tubo.collisione(uccello,uccellox,uccelloy)

    if not fra_tubi:
        for t in tubi:
           if t.fra_i_tubi(uccello,uccellox):
               fra_tubi= True

    if punti == 0:
        Vel_Avanzamento = 3

    if punti == 10:
        Vel_Avanzamento = 4

    if punti == 15:
        Vel_Avanzamento = 5

    if punti == 35:
        Vel_Avanzamento = 6

    if punti == 45:
        Vel_Avanzamento = 7

    if fra_tubi:
        fra_tubi=False
        for t in tubi:
           if t.fra_i_tubi(uccello,uccellox):
               fra_tubi= True
        if not fra_tubi:
            punti += 1
    if uccelloy > 380:
        hai_perso()
    disegna_oggetti()
    aggiorna()


