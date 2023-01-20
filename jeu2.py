# JEU 2 (version E)
# H. Poupon et E. Verplanken
# 15/01/2023 : ajout du son "bye bye" en sortie

import os
import machine
import utime
from pico_i2c_lcd import I2cLcd
from machine import I2C, Timer
from wavePlayer import wavePlayer

player = wavePlayer()

i2c = I2C(id=0,scl=machine.Pin(1),sda=machine.Pin(0),freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16) # LCD 16x2

led_g = machine.Pin(17, machine.Pin.OUT)
led_d = machine.Pin(14, machine.Pin.OUT)
left_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
right_button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

g_d = None
pressedG = False
pressedD = False

def temps_droite(u):
    global pressedD
    if not pressedD:
        pressedD=True
        global D
        D = utime.ticks_diff(utime.ticks_ms(), timer_start)
        right_button.irq(handler=None)
           
def temps_gauche(t):
    global pressedG
    if not pressedG:
        pressedG=True
        global G
        G = utime.ticks_diff(utime.ticks_ms(), timer_start)
        left_button.irq(handler=None)

def fin_jeu(Source):
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("P E R D U")
    lcd.move_to(1,1)
    lcd.putstr("trop attendu !")
    player.play('/sounds/wrong-answer-buzzer-08-converted.wav')
    utime.sleep(3)

def arret():
    lcd.clear()
    lcd.putstr("   A R R E T   ")
    lcd.move_to(0,1)
    lcd.putstr("==> Eteindre")
    player.play('/sounds/bye-bye-1-converted.wav')
    utime.sleep(1)
    with open("menu.py", encoding="utf-8") as f:
        transfer = f.read()
    with open("main.py", "w") as file:
        file.write(transfer)
    utime.sleep(0.2)
    machine.deepsleep()

#### DEBUT DU JEU ####
Fin_Timer = machine.Timer(period=60000, mode=Timer.ONE_SHOT, callback=fin_jeu) # fin automatique si on ne fait rien après 60 sec.
lcd.clear()
lcd.putstr('  JEU COMPTER')
lcd.move_to(2,1)
lcd.putstr('10 secondes')
utime.sleep(3)
lcd.clear()
lcd.putstr("Appuyez a 10 sec")
compteur = 0
timer_start = utime.ticks_ms() # début de la mesure du temps

for i in range(1,6):
   compteur = compteur + 1
   lcd.move_to(4,1)
   lcd.putstr("==> " + str(compteur))
   utime.sleep(1)
lcd.clear()

# déclenchement mesure du temps lors de l'appui des boutons
left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=temps_gauche)
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=temps_droite)

while utime.ticks_diff(utime.ticks_ms(), timer_start) < 16000:
    if pressedG == True:
        lcd.move_to(0,0)
        lcd.putstr('Gauche: '+str(G)+' ms')
    if pressedD == True:
        lcd.move_to(0,1)
        lcd.putstr('Droite: '+str(D)+' ms')

#### GESTION FIN DE JEU #### (réutilisable pour les futurs jeux)
        
def relance_jeu(pin):
    global g_d
    g_d = pin

left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=relance_jeu)
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=relance_jeu)

i = 0
while g_d is None:
    i += 1
    lcd.clear()
    lcd.putstr("  On rejoue ?")
    lcd.move_to(0,1)
    lcd.putstr("<= NON    OUI =>")
    utime.sleep(1)
    if i >= 10:
        arret()

if g_d is left_button:
    arret()

elif g_d is right_button:
    lcd.clear()
    lcd.putstr('<== MEME JEU')
    lcd.move_to(3,1)
    lcd.putstr('AUTRE JEU ==>')
    while True:
#         utime.sleep(0.2)   
        if left_button.value() == False:
            utime.sleep(0.2)
            machine.reset()
        if right_button.value() == False:
            with open("menu.py", encoding="utf-8") as f:
                transfer = f.read()
            with open("main.py", "w") as file:
                file.write(transfer)
            utime.sleep(0.2)
            machine.reset()
  

