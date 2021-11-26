# Nastavitve programa (potem vse ostalo sam izračuna)
# Tukaj nastavimo število točk in omejitve za x in y
## Koda je sicer pisana v sage-u, vendar zaradi tehničnih težav, nama še ni uspelo naložiti sage dokumenta, zato je koda (začasno) kar v pythonu.
n = 60
x_min = 0
x_max = 10
y_min = 0
y_max = 10

if n <= 0:
    print("Napaka: število kvadratov mora biti pozitivno")
elif x_min >= x_max or y_min >= y_max:
    print("Napaka: napačno nastavljeni parametri")
else:
    print("Uspešno nastavljene nastavitve")

import random
from matplotlib.pyplot import plot, axis, show,axes
import matplotlib.pyplot as plt

def nakljucne_tocke(x_min, x_max, y_min, y_max, n):
    #nam da seznam n točk v koordinatnem sistemu na intervalu [x_min,x_max]x[y_min,y_max]
    rangeX = (x_min, x_max-1)
    rangeY = (y_min, y_max-1)
    points = []
    i = 0
    while i<n:
        x = random.uniform(*rangeX) 
        y = random.uniform(*rangeY)
        points.append([x,y])
        i += 1
    return points


seznam_tock = nakljucne_tocke(x_min, x_max, y_min, y_max, n)

def generiranje_kvadrata(tocka): # tocka je seznam [ , ]
    #generira še druge tri vogale kvadrata in jih poveze, da to nariše potrebujem za ukazom plt.show()
    x0 = tocka[0]
    y0 = tocka[1]
    x1 = x0 + 1
    x2 = x1
    x3 = x0
    y1 = y0
    y2 = y0 + 1
    y3 = y2
    return plot([x0, x1, x2, x3, x0], [y0, y1, y2, y3, y0])

seznam_slik = []
for i in range(0,len(seznam_tock)):
    tocka = seznam_tock[i]
    seznam_slik.append(generiranje_kvadrata(tocka))

for slika in seznam_slik:    #to pokaže koncno sliko vseh mojih enotskih kvadratov
     plt.plot()
plt.show()

def koordinate_kvadrata(tocka):
    x0 = tocka[0]
    y0 = tocka[1]
    x1 = x0 + 1
    x2 = x1
    x3 = x0
    y1 = y0
    y2 = y0 + 1
    y3 = y2
    return [[x0,y0], [x1,y1], [x2,y2], [x3,y3]]

seznam_kvadratov = []   #seznam kvadratov oz. tock, ki generirajo prej narisane kvadrate
for i in seznam_tock:
    seznam_kvadratov.append(koordinate_kvadrata(i))


def najvecje_dotikanje(seznam_tock): # kot vhod dobita seznam spodnjih levih oglišč
    n = len(seznam_tock)
    x_min = min(x for x, y in seznam_tock)
    x_max = max(x for x, y in seznam_tock)
    y_min = min(y for x, y in seznam_tock)
    y_max = max(y for x, y in seznam_tock)

    p = MixedIntegerLinearProgram(maximization=True) # iščeta točko, ki se dotika največ kvadratov
    z = p.new_variable(binary=True) #z_i = 1 če tocka (x,y) v kvadratu i
    p.set_objective(sum(z[i] for i in range(n))) # številčenje naj gre kar od 0 do n-1
    for i, (x_i, y_i) in enumerate(seznam_tock): # za realni spremenljivki x, y indeksiramo kar p
        p.add_constraint(p['x'] + (1-z[i])*(x_max - x_min) >= x_i)
        p.add_constraint(p['x'] - (1-z[i])*(x_max - x_min) <= x_i + 1)
        p.add_constraint(p['y'] + (1-z[i])*(y_max - y_min) >= y_i)
        p.add_constraint(p['y'] - (1-z[i])*(y_max - y_min) <= y_i + 1)

    stevilo = p.solve()
    x, y = p.get_values(p['x']), p.get_values(p['y'])
    kvadrati = [k for k, v in p.get_values(z).items() if v == 1]
    return [stevilo, (x, y), kvadrati] # vrnemo število dotikanj, koordinato točke in seznam indeksov kvadratov, ki se jih dotika

najvecje_dotikanje(seznam_tock)

#seznam_kvadratov
#kvadrati = najvecje_dotikanje(seznam_tock)[2]
#for i in kvadrati:
#    print(seznam_kvadratov[i])

import time
#kako se spreminja čas izvajanja v odvisnosti od n (to je število izbranih točk oz kvadratov)
def cas_izvajanja_od_n(x_min, x_max, y_min, y_max ,n):
    seznam_tock = nakljucne_tocke(x_min, x_max, y_min, y_max, n)
    casi = []
    for i in range(1,n+1):
        zacetek = time.time()
        najvecje_dotikanje(seznam_tock)
        konec = time.time() - zacetek
        casi.append((konec))
    return casi
cas_izvajanja_od_n(0,10,0,10,60)
cas_izvajanja_od_n(0,10,0,50,60)
cas_izvajanja_od_n(0,10,0,10,100)

def p_max(x_min, x_max, y_min, y_max):
    seznam = []
    for k in range(-1000, y_max + 1001):
        for m in range(-1000, y_max + 1001):
            y = k*(x_max + 1) + m
            seznam.append(y)
    return max(seznam)
p_max = p_max(x_min, x_max, y_min, y_max)

def najvecje_dotikanjepremica(seznam_tock, p_max): # kot vhod dobita seznam spodnjih levih oglišč
    n = len(seznam_tock)
    x_min = min(x for x, y in seznam_tock)
    x_max = max(x for x, y in seznam_tock)
    y_min = min(y for x, y in seznam_tock)
    y_max = max(y for x, y in seznam_tock)
    #seznam = []
    #for k in range(-Integer(1000), y_max + Integer(1001)):
    #    for m in range(-Integer(1000), y_max + Integer(1001)):
    #        y = k*(x_max + Integer(1)) + m
    #        seznam.append(y)
    #p_max = max(seznam)
    #p_max = p_max(x_min, x_max, y_min, y_max)
    
    p = MixedIntegerLinearProgram(maximization=True) # iščeta točko, ki se dotika največ kvadratov
    z = p.new_variable(binary=True) #z_i = 1 če tocka (x,y) v kvadratu i
    u = p.new_variable(binary=True)
    v = p.new_variable(binary=True)
    p.set_objective(sum(z[i] for i in range(n))) # številčenje naj gre kar od 0 do n-1
    for i, (x_i, y_i) in enumerate(seznam_tock): # za realni spremenljivki x, y indeksiramo kar p
        p.add_constraint(z[i] <= u[i]+v[i])
        p.add_constraint(p['k']*(x_i+1) + p['m'] + (1-u[i])*(p_max - y_min) >= y_i)
        p.add_constraint(p['k']*x_i + p['m'] - (1-u[i])*(p_max - y_min) <= y_i + 1)
        p.add_constraint(p['k']*x_i + p['m'] + (1-v[i])*(p_max - y_min) >= y_i)
        p.add_constraint(p['k']*(x_i+1) + p['m'] - (1-v[i])*(p_max - y_min) <= y_i + 1)

    stevilo = p.solve()
    k, m = p.get_values(p['k']), p.get_values(p['m'])
    kvadrati = [k for k, v in p.get_values(z).items() if v == 1]
    return [stevilo, (k, m), kvadrati] # vrnemo število dotikanj, koordinato točke in seznam indeksov kvadratov, ki se jih dotika

najvecje_dotikanjepremica(seznam_tock,p_max)