#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.2
# Date: 03/10/2021
# Description: Controlar los leds de la GPIO

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

# Configurar pines 36, 38, 40 y 37 como salida y habilitar en bajo (para el display de 7 segmentos)
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""
def leds(num):	
	for i in range(len(pin)):
		if (i == num):
			GPIO.output(pin[i], GPIO.HIGH) #Prender led
		else:
			GPIO.output(pin[i], GPIO.LOW) #Apagar led

""" Activa el modo marquesina
	type toma tres valores: left, right y pingpong
	(To be developed by the student)
"""
def marquee(type='pingpong'):
	switcher = {
		'left'     : _marquee_left,
		'right'    : _marquee_right,
		'pingpong' : _marquee_pingpong
	}
	func = switcher.get(type, None)
	if func:
		func()

"""	Despliega en número proporcionado en el display de siete segmentos.
	(To be developed by the student)
"""
def bcd(num):
	# Conversión de entero a bits
	bit = []
	i = 0x00000001
	while i <= 0x00000008: #Solo repetir 4 veces para los bits
		bit.append(num & i)
		i = i * 2
	# Enviar bits al decodificador BCD
	GPIO.output(36, GPIO.HIGH if bit[0] > 0 else GPIO.LOW )
	GPIO.output(38, GPIO.HIGH if bit[1] > 0 else GPIO.LOW )
	GPIO.output(40, GPIO.HIGH if bit[2] > 0 else GPIO.LOW )
	GPIO.output(37, GPIO.HIGH if bit[3] > 0 else GPIO.LOW )

""" Activa el modo marquesina continua a la izquierda"""
def _marquee_left():
	i = 7 #Contador auxiliar
	while i >= 0:
		GPIO.output(pin[i], GPIO.HIGH) #Prender led
		sleep(0.5) #Esperar 500ms
		GPIO.output(pin[i], GPIO.LOW) #Apagar led
		i = i - 1

""" Activa el modo marquesina continua a la derecha"""
def _marquee_right():
	i = 0 #Contador auxiliar
	while i < 8:
		GPIO.output(pin[i], GPIO.HIGH) #Prender led
		sleep(0.5) #Esperar 500ms
		GPIO.output(pin[i], GPIO.LOW) #Apagar led
		i = i + 1
		
""" Activa el modo marquesina ping-pong"""
def _marquee_pingpong():
	# Llamando funciones creadas anteriormente
	_marquee_right()
	_marquee_left()	

