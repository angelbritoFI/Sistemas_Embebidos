#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.1
# Date: 15/09/2021
# Description: Marquesina de izquierda a derecha para prender los 8 leds

# ## ###############################################
# Fundamentos de Sistemas Embebidos, Semestre 2022-1
# -*- coding: utf-8 -*-
# Autor: Mauricio Matamoros
# License: MIT
# ## ###############################################

# Importación de future (para compatibilidad con Python 2.7)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Importación de la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importación de la función sleep del módulo time para control mediante tiempos de espera
from time import sleep

# Inicialización de placa virtual (comentar si es implementación en hardware)
import virtualboard
# Desactiviar advertencias (descomentar si es implementación en hardware)
# GPIO.setwarnings(False)

#Configuraciones de la librería Rpi.GPIO
GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

# Declaración de arreglo para mejor control de pines
pin = [10, 12, 16, 18, 22, 24, 26, 32]
pwm = []

# Habilitar los pines con LED como de salida, en bajo e inicializar PWM a una frecuencia de 1 Hz
for p in pin:
	GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)
	pwm.append(GPIO.PWM(p, 1))

i = 0 #Inicializar contador para arreglo de pines

# Ciclo infinito para marquesina de 
while True:		
	pwm[i].start(30) #Establecer el ciclo de trabajo inicial
	sleep(0.5) #Esperar 500ms
	# Apagar LED
	pwm[i].ChangeDutyCycle(0)
	pwm[i].stop()		
	if i < 7:
		i = i + 1
	else:
		i = 0
