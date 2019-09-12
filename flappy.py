import pygame
import neat
import time
import os
import random

SIRINA = 500    # naše igralno okno
VISINA = 800

PTIC_SLIKE = [pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bird3.png")))]
CEV_SLIKA = pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "pipe.png")))
OZADJE_SLIKA = pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bg.png")))
TLA_SLIKA = pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "base.png")))

class Ptic:
    SLIKE = PTIC_SLIKE
    ROTACIJA = 25    # največja rotacija
    ROT_HITROST = 20
    ANIMACIJA_CAS = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0    # naša nagnjenost
        self.tick_count = 0    # kdaj smo nazadnje skočili
        self.hitrost = 0
        self.visina = self.y
        self.katera_slika = 0
        self.slika = self.SLIKE[0]

    def skok(self):
        self.hitrost = -10.5
        self.tick_count = 0
        self.visina = self.y

    def premik(self):
        self.tick_count += 1

        d = self.hitrost * self.tick_count + 1.5 * self.tick_count ** 2    # displacement - fizika, ki pove kam gre ptič
        if d >= 16:    # to je terminal velocity
            d = 16
        if d < 0:
            d -= 2    # polepša gibanje

        self.y += d

        if d < 0 or self.y < self.visina + 50:    # pogledamo, kako visoko je ptič - za tilt
            if self.tilt < self.ROTACIJA:    # premikanje gor
                self.tilt = self.ROTACIJA
        else:
            if self.tilt > -90:    # premikanje dol
                self.tilt -= self.ROT_HITROST

    def narisi(self, okno):
        self.katera_slika += 1

        # to je za animacijo ptiča
        if self.katera_slika < self.ANIMACIJA_CAS:    
            self.slika = self.SLIKE[0]
        elif self.katera_slika < self.ANIMACIJA_CAS * 2:
            self.slika = self.SLIKE[1]
        elif self.katera_slika < self.ANIMACIJA_CAS * 3:
            self.slika = self.SLIKE[2]
        elif self.katera_slika < self.ANIMACIJA_CAS * 4:
            self.slika = self.SLIKE[1]
        elif self.katera_slika == self.ANIMACIJA_CAS * 4 + 1:
            self.slika = self.SLIKE[0]
            self.katera_slika = 0

        if self.tilt <= -80:    # če padamo hitro
            self.slika = self.SLIKE[1]
            self.katera_slika = self.ANIMACIJA_CAS * 2

        # rotacija slike okoli centra
        rotirna_slika = pygame.transform.rotate(self.slika, self.tilt)    
        nova_sredina = rotirna_slika.get_rect(center=self.slika.get_rect(topleft = (self.x, self.y)).center)
        okno.blit(rotirna_slika, nova_sredina.topleft)

    def dobi_masko(self):
        return pygame.mask.from_surface(self.slika)
        

class Cev:
    HITROST = 5

    def __init__(self, x):
        self.x = x
        self.visina = 0
        self.RAZMIK = 100

        self.vrh = 0
        self.dno = 0
        self.CEV_VRH = pygame.transform.flip(CEV_SLIKA, False, True)
        self.CEV_DNO = CEV_SLIKA

        self.mimo = False
        self.nastavi_visino()

    def nastavi_visino(self):
        self.visina = random.randrange(50, 450)
        self.vrh = self.visina - self.CEV_VRH.pridobi_visino()
        self.dno = self.visina + self.RAZMIK


def narisi_okno(okno, ptic):
    okno.blit(OZADJE_SLIKA, (0, 0))
    ptic.narisi(okno)
    pygame.display.update()

def main():
        ptic = Ptic(200, 200)
        okno = pygame.display.set_mode((SIRINA, VISINA))
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #ptic.premik()
            narisi_okno(okno, ptic)
        
        pygame.quit()

main()