#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.0
# Date: 13/09/2021
# Description: Controlar un display mediante el decodificador BCD a 7 segmentos (driver 74LS47)

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

# Configurar la librería para usar el número de pin
GPIO.setmode(GPIO.BOARD)

# Configurar pines 36, 38, 40 y 37 como salida y habilitar en bajo
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

# Función que mapea bits a los pines de la GPIO
def bcd7(num):
	GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW )
	GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW )
	GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW )
	GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW )

# Request a number and send it to the display
flag = True
while flag:
	try:
		# Solicitar un número y enviarlo al display de 7 segmentos
		num = int(input("Ingresa un número entero entre 0 y 15: "))
		bcd7(num)
	# Detener con el shortcut CTRL+C o excepción
	except:
		flag = False
		print("Valor no permitido :( \nPrograma terminado")

# Reiniciar todos los puertos para que estén en su estado por defecto (entradas)
GPIO.cleanup()
