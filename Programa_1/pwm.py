#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.0
# Date: 13/09/2021
# Description: Papadear un led utilizando PWM por hardware (incorporado por Raspberry Pi)
# Físicamente, el led está conectado al pin 32

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
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW) # Habilitar pin 32: como de salida y en bajo
pwm = GPIO.PWM(32, 1) # Inicializar pin 32 como PWM a una frecuencia de 1 Hz

print("Iniciando PWM")
pwm.start(50) # Establecer ciclo de trabajo al 50% para que parpadee cada 500 ms
print("PWM iniciado")
flag = True

# Ciclo infinito para parpadear un led hasta que ocurra una excepción
while flag:
	try:
		dutyCycle = int(input("Ingrese ciclo de trabajo: "))
		pwm.ChangeDutyCycle(dutyCycle)
	# Detener con el shortcut CTRL+C o excepción
	except:
		flag = False
		print("Valor no permitido :(")
		pwm.ChangeDutyCycle(0)
		print("Ciclo de trabajo: 0")

# Detener PWM
pwm.stop()

# Reiniciar todos los puertos para que estén en su estado por defecto (entradas)
GPIO.cleanup()
