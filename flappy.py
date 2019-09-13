import pygame
import neat
import time
import os
import random
pygame.font.init()

SIRINA = 500    # naše igralno okno
VISINA = 800

PTIC_SLIKE = [pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bird3.png")))]
CEV_SLIKA = pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "pipe.png")))
OZADJE_SLIKA = pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "bg.png")))
TLA_SLIKA = pygame.transform.scale2x(pygame.image.load(os.path.join("slike", "base.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

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

        # displacement - fizika, ki pove kam gre ptič
        d = self.hitrost * self.tick_count + 1.5 * self.tick_count ** 2
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

    # za trčenja
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
        self.vrh = self.visina - self.CEV_VRH.get_height()
        self.dno = self.visina + self.RAZMIK

    def premik(self):
        self.x -= self.HITROST

    def narisi(self, okno):
        okno.blit(self.CEV_VRH, (self.x, self.vrh))
        okno.blit(self.CEV_DNO, (self.x, self.dno))

    def trci(self, ptic):
        ptic_maska = ptic.dobi_masko()  
        vrh_maska = pygame.mask.from_surface(self.CEV_VRH)  
        dno_maska = pygame.mask.from_surface(self.CEV_DNO)

        vrh_odmik = (self.x - ptic.x, self.vrh - round(ptic.y))
        dno_odmik = (self.x - ptic.x, self.dno - round(ptic.y))

        dno_tocka = ptic_maska.overlap(dno_maska, dno_odmik)
        vrh_tocka = ptic_maska.overlap(vrh_maska, vrh_odmik)

        if vrh_tocka or dno_tocka:
            return True
        
        return False


class Tla:
    HITROST = 5
    SIRINA = TLA_SLIKA.get_width()
    SLIKA = TLA_SLIKA

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.SIRINA

    def premik(self):
        self.x1 -= self.HITROST
        self.x2 -= self.HITROST

        if self.x1 + self.SIRINA < 0:
            self.x1 = self.x2 + self.SIRINA

        if self.x2 + self.SIRINA < 0:
            self.x2 = self.x1 + self.SIRINA

    def narisi(self, okno):
        okno.blit(self.SLIKA, (self.x1, self.y))
        okno.blit(self.SLIKA, (self.x2, self.y))


def narisi_okno(okno, ptic, cevi, tla, score):
    okno.blit(OZADJE_SLIKA, (0, 0))
    for cev in cevi:
        cev.narisi(okno)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    okno.blit(text, (SIRINA - 10 - text.get_width(), 10))

    tla.narisi(okno)

    ptic.narisi(okno)
    pygame.display.update()

def main():
        ptic = Ptic(230, 350)
        tla = Tla(730)
        cevi = [Cev(700)]
        okno = pygame.display.set_mode((SIRINA, VISINA))
        clock = pygame.time.Clock()

        score = 0

        run = True
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #ptic.premik()
            dodaj_cev = False
            odstrani = []
            for cev in cevi:
                if cev.trci(ptic):
                    pass

                if cev.x + cev.CEV_VRH.get_width() < 0:
                    odstrani.append(cev)

                if not cev.mimo and cev.x < ptic.x:
                    cev.mimo = True
                    dodaj_cev = True

                cev.premik()

            if dodaj_cev:
                score += 1
                cevi.append(Cev(600))

            for cev in odstrani:
                cevi.remove(cev)

            if ptic.y + ptic.slika.get_height() >= 730:
                pass

            tla.premik()
            narisi_okno(okno, ptic, cevi, tla, score)
        
        pygame.quit()

main()