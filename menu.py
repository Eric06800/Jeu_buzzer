# menu pour 2 jeux
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


def arret(a):
    lcd.clear()
    lcd.putstr("   A R R E T   ")
    lcd.move_to(0,1)
    lcd.putstr("==> Eteindre")
    player.play('/sounds/bye-bye-1-converted.wav')
    utime.sleep(1)
    machine.deepsleep()

def show_menu():
    lcd.clear()
    lcd.putstr('<== JEU 1')
    lcd.move_to(7,1)
    lcd.putstr('JEU 2 ==>')

# Fin_Timer = machine.Timer(period=30000, mode=Timer.ONE_SHOT, callback=arret) # fin automatique si on ne fait rien après 60 sec.
show_menu()

while True:
    utime.sleep(0.2)
    led_g.toggle()
    led_d.toggle()
    if left_button.value() == False:
        with open("jeu1.py", encoding="utf-8") as f:
            transfer = f.read()
        with open("main.py", "w") as file:
            file.write(transfer)
        utime.sleep(0.2)
        machine.reset()
    if right_button.value() == False:
        with open("jeu2.py", encoding="utf-8") as f:
            transfer = f.read()
        with open("main.py", "w") as file:
            file.write(transfer)
        utime.sleep(0.2)
        machine.reset()
        