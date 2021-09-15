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

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import Raspberry Pi's GPIO control library
import RPi.GPIO as GPIO
# Imports sleep functon
from time import sleep
# Initializes virtual board (comment out for hardware deploy)
import virtualboard

# Disable warnings
# GPIO.setwarnings(False)
# Set up Rpi.GPIO library to use physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Set up pin no. 32 as output and default it to low
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)

# Blink the led
while True: # Forever
	sleep(0.5)                 # Wait 500ms
	GPIO.output(32, GPIO.HIGH) # Turn led on
	sleep(0.5)                 # Espera 500ms
	GPIO.output(32, GPIO.LOW)  # Turn led off
