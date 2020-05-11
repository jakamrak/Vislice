import random

STEVILO_DOVOLJENIH_NAPAK = 10 

PRAVILNA_CRKA = '+'
PONOVLJENA_CRKA = 'o'
NAPACNA_CRKA = '-'

ZMAGA = 'W'
PORAZ = 'X'

#preberemo vse besede iz te datoteke in jih preuredimo v male črke
bazen_besed = []
with open('besede.txt') as datoteka_bazena:
    for beseda in datoteka_bazena:
        bazen_besed.append(beseda.strip().lower())

class Igra:
    #definiramo si igro ki sestoji iz gesla ki ga more nekdo ugotovit in ugibanih crk
    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if self.crke == None:
            self.crke = []
        else:
            self.crke = [c.lower() for c in crke]

#seznam napacnih crk
    def napacne_crke(self):
        napacne = []
        for crka in self.crke:
            if crka not in self.geslo:
                napacne.append(crka)
        return napacne

    def pravilne_crke(self):
        pravilne = []
        for crka in self.crke:
            if crka in self.geslo:
                pravilne.append(crka)
        return pravilne

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def zmaga(self):
        for crka in self.geslo:
            if crka not in self.crke:
                return False
        return True

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def pravilni_del_gesla(self):
        delni = ''
        for crka in self.geslo:
            if crka in self.crke:
                delni += crka
            else:
                delni += '_'
        return delni

    def nepravilni_ugibi(self):
        return ' '.join(self.napacne_crke())

    def ugibaj(self, ugibana_crka):
        ugibana_crka = ugibana_crka.lower()
        if ugibana_crka in self.crke:
            return PONOVLJENA_CRKA
        
        self.crke.append(ugibana_crka)
        #PRAVILNA, NAPAČNA, ZMAGA, PORAZ
        #zdruzimo pravilna, zmaga in napacna, poraz

        if ugibana_crka in self.geslo: #uganu je
            if self.zmaga():
                return ZMAGA
            else:
                return PRAVILNA_CRKA
        else:
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA

def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)
    