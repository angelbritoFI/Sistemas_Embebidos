#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 4.2
# Date: 15/09/2021
# Description: Marquesina de izquierda a derecha para prender los 8 leds en una fila del simulador en línea

# Importación de la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importación de la función sleep del módulo time para control mediante tiempos de espera
from time import sleep

# Desactiviar advertencias
GPIO.setwarnings(False)

#Configuraciones de la librería Rpi.GPIO
GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

# Declaración de arreglo para mejor control de pines
pin = [21, 23, 27, 29, 31, 33, 35, 37]

# Inicialización del arreglo para control por PWM
pwm = []

# Habilitar los pines con LED como de salida, en bajo e inicializar PWM a una frecuencia de 2 Hz
for p in pin:
	GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)
	pwm.append(GPIO.PWM(p, 2))

i = 0 #Inicializar contador para arreglo de pines

# Ciclo infinito para marquesina de 
while True:		
	pwm[i].start(50) #Establecer el ciclo de trabajo inicial
	sleep(1) #Esperar 1 s
	# Apagar LED
	pwm[i].ChangeDutyCycle(0)
	pwm[i].stop()		
	if i < 7:
		i = i + 1
	else:
		i = 0
