import random, json

STEVILO_DOVOLJENIH_NAPAK = 10 

ZACETEK = 'Z'

#Konstante za rezultate ugibanj
PRAVILNA_CRKA = '+'
PONOVLJENA_CRKA = 'o'
NAPACNA_CRKA = '-'

ZMAGA = 'W'
PORAZ = 'X'

DATOTEKA_S_STANJEM = 'stanje_iger.json'
#preberemo vse besede iz te datoteke in jih preuredimo v male črke
bazen_besed = []
with open('besede.txt') as datoteka_bazena:
    for beseda in datoteka_bazena:
        bazen_besed.append(beseda.strip().lower())

class Igra:
    #definiramo si igro ki sestoji iz gesla ki ga more nekdo ugotovit in ugibanih crk
    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if crke == None:
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
                delni += ' _ '
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




class Vislice:
    '''
    Skrbi za trenutno stanje VEČ iger (imel bo več objektov tipa Igra)
    '''
    def __init__(self):
        #Slovar, ki ID-ju priredi igro
        self.igre = {}   #   init  --> (Igra, stanje)

    def prost_id_igre(self):
        '''Vrne nek id, ki ga ne uporablja se nobena igra.'''
    
        if len(self.igre) == 0:
            return 0
        else:
          return max(self.igre.keys()) + 1 #tako vemo, da nebomo nikoli dobili istega idja kot ze obstaja v tem slovarju (problem je eko brišemo)
    
    def nova_igra(self):
        self.preberi_iz_datoteke()
        #dobimo svež id

        nov_id = self.prost_id_igre()
        #naredimo novo igro

        sveza_igra = nova_igra()
        #vse to shranimo v self.igre

        self.igre[nov_id] = (sveza_igra, ZACETEK)

        self.shrani_v_datoteko()
        #Vrnemo id igre
        return nov_id

    def ugibaj(self, id_igre, crka):
        #Dobimo staro igro ven
        self.preberi_iz_datoteke()
        trenutna_igra, _ = self.igre[id_igre]

        #Ugibamo crko
        novo_stanje = trenutna_igra.ugibaj(crka)

        #Zapišemo novo stanje in igro nazaj v 'BAZO'
        self.igre[id_igre] = (trenutna_igra, novo_stanje)

        self.shrani_v_datoteko()

    def shrani_v_datoteko(self):
        igre = {}
        for id_igre, (igra,stanje) in self.igre.items(): #id_igre, (Igra, stanje)
            igre[id_igre] = ((igra.geslo, igra.crke), stanje)

        with open(DATOTEKA_S_STANJEM, 'w') as out_file:
            json.dump(igre, out_file)

    def preberi_iz_datoteke(self):
        with open(DATOTEKA_S_STANJEM) as in_file:
            igre = json.load(in_file)  #igre iz diska 
        
        self.igre = {}
        for id_igre, ((geslo, crke), stanje) in igre.items():
            self.igre[int(id_igre)] = Igra(geslo, crke), stanje
