#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.0
# Date: 13/09/2021
# Description: Parpadear un led mediante tiempos de espera
# Físicamente, el led está conectado al GPIO 32 de la Raspberry Pi

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

# Configurar la librería Rpi.GPIO para usar el número físico de pin
GPIO.setmode(GPIO.BOARD)

# Configurar el pin 32 como salida y habilitar en bajo
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)

# Ciclo infinito para parpadear un led
while True:
	sleep(0.5)                 # Esperar 500ms
	GPIO.output(32, GPIO.HIGH) # Prender led
	sleep(0.5)                 # Esperar 500ms
	GPIO.output(32, GPIO.LOW)  # Apagar led
