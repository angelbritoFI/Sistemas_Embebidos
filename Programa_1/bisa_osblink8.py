#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 3.2
# Date: 15/09/2021
# Description: Parpadear 8 leds del simulador en línea mediante tiempos de espera

# Importación de la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importación de la función sleep del módulo time para control mediante tiempos de espera
from time import sleep

# Desactiviar advertencias
GPIO.setwarnings(False)

#Configuraciones de la librería Rpi.GPIO
GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

# Declaración de arreglo para mejor control de pines
pin = [8, 10, 12, 16, 18, 22, 24, 26]

# Habilitar los pines con LED como de salida y en bajo
for p in pin:
	GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)

# Ciclo infinito para parpadear los leds
while True:
	sleep(0.5) #Esperar 500ms
	for p in pin:
		GPIO.output(p, GPIO.HIGH) #Prender led
	sleep(0.5) #Esperar 500ms
	for p in pin:
		GPIO.output(p, GPIO.LOW) #Apagar led
