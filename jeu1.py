# reaction_2players_8.py
# Eric Verplanken 
# 15/01/2023 : ajout du son "bye bye" en sortie et "wrong answer" en cas de réponse trop rapide

import os
import machine
import utime
import urandom
from pico_i2c_lcd import I2cLcd
from machine import I2C
from wavePlayer import wavePlayer

player = wavePlayer()

i2c = I2C(id=0,scl=machine.Pin(1),sda=machine.Pin(0),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16) # LCD 16x2

led_g = machine.Pin(17, machine.Pin.OUT)
led_d = machine.Pin(14, machine.Pin.OUT)
left_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
right_button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
fastest_button = None
g_d = None
bouton = None
timer_reaction = 0
pressed = False
pressed1 = False
pressed2 = False
appui = False

def trop_vite(pin):
    global appui
    if not appui:
        appui=True
        global bouton_rapide
        bouton_rapide = pin
        lcd.clear()
        lcd.putstr("  TROP VITE !!")
        player.play('/sounds/wrong-answer-buzzer-08-converted.wav')
        utime.sleep(1)
        if bouton_rapide is left_button:
            lcd.move_to(0,1)
            lcd.putstr('Gauche a perdu !')
#            utime.sleep(3)
        elif bouton_rapide is right_button:
            lcd.move_to(0,1)
            lcd.putstr('Droite a perdu !')
        utime.sleep(3)
        lcd.clear()
        lcd.putstr('ON RECOMMENCE !')
        utime.sleep(1)
        lcd.clear()
        machine.reset()

def button_handler(pin):
    global pressed
    if not pressed:
        pressed=True
        global timer_reaction
        timer_reaction = utime.ticks_diff(utime.ticks_ms(), timer_start)
        global fastest_button
        fastest_button = pin

def relance_jeu(pin):
    global g_d
    g_d = pin

# def run_script_jeu1(filename):
#     left_button.irq(handler=None)
#     right_button.irq(handler=None)
#     utime.sleep(0.2)
#     exec(open(filename).read())

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

### DEBUT DU JEU ####

lcd.clear()
lcd.putstr('     JEU DE     ')
lcd.move_to(0,1)
lcd.putstr('   REACTIVITE   ')
utime.sleep(2)

lcd.clear()
lcd.putstr("   Attention   ")
lcd.move_to(0,1)
lcd.putstr(" C'est parti ! ")
utime.sleep(2)
lcd.clear()
lcd.putstr(" Soyez prets ! ")
led_g.value(1)
led_d.value(1)
left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=trop_vite)
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=trop_vite)

utime.sleep(urandom.uniform(2, 5))
led_g.value(0)
led_d.value(0)
timer_start = utime.ticks_ms()
left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
lcd.clear()
lcd.putstr(" MAINTENANT !!!")

while fastest_button is None:
    utime.sleep(0.1)
lcd.clear()
if fastest_button is left_button:
    lcd.putstr(' Gauche gagne !')
elif fastest_button is right_button:
    lcd.putstr(' Droite gagne !')

lcd.move_to(0,1)
lcd.putstr("Temps : " + str(timer_reaction) + " ms")
utime.sleep(5)
lcd.clear()

#### GESTION FIN DE JEU #### (réutilisable pour les futurs jeux)

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
            with open("menu_chat_gpt.py", encoding="utf-8") as f:
                transfer = f.read()
            with open("main.py", "w") as file:
                file.write(transfer)
            utime.sleep(0.2)
            machine.reset()
     


  