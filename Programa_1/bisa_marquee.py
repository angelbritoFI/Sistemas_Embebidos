#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.0
# Date: 14/09/2021
# Description: Parpadear un led mediante tiempos de espera
# Físicamente, el led está conectado al pin 32 de la Raspberry Pi mediante un Array Darlington ULN2003

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

# Habilitar los pines con LED como de salida y en bajo
for p in pin:
	GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)

i = 0 #Inicializar contador para arreglo de pines

# Ciclo infinito para parpadear un led
while True:
	sleep(0.5)                 		# Esperar 500ms
	GPIO.output(pin[i], GPIO.HIGH)	# Prender led
	sleep(0.5)                 		# Esperar 500ms
	GPIO.output(pin[i], GPIO.LOW)	# Apagar led
	if i < 7:
		i = i + 1
	else:
		i = 0
