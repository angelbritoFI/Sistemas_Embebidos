#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.1
# Date: 14/11/2021
# Description: Control de atenuación de luz de una lámpara incandecente

# ## ###############################################
# Fundamentos de Sistemas Embebidos, Semestre 2022-1
# -*- coding: utf-8 -*-
# Autor: Mauricio Matamoros
# License: MIT
# ## ###############################################

import smbus2 #Lectura del puerto serial I2C
import struct #Conversión de datos binarios a objetos que puede leer Python
#Importación de la función sleep y strftime del módulo time para control de tiempos
from time import sleep
#Importación de la función argv del módulo sys para recibir parámetros desde línea de comandos
from sys import argv
#Inicialización de placa virtual (comentar si es implementación en hardware)
from virtualboards import run_dimmer_board

# Dirección del dispositivo I2C
SLAVE_ADDR = 0x0A # Dirección I2C del Arduino

# Inicializar el bus I2C instanciando al objeto SMBus
# Como parámetro se indica el número de dispositivo a controlar
i2c = smbus2.SMBus(1)

# Archivo en el cual se muestra ayuda al usuario como ejecutar el programa
HELP_FILE = './bisa_ayuda_dimm.txt'

#Escribir el retraso de fase (en ms) en Arduino via I2C
def writePhase(delay):
	try:
		""" Función pack:
		Recibe un bytearray y un especificador de formato para poder generar su tupla
		Se empaqueta el tiempo de fase recibido (en milisegundos) como un valor flotante (f)
		Hace la codificación por defecto en I2C (<):
			little endian: codifica los bytes con el LSB a la izquierda
		"""
		data = struct.pack('<f', delay/1000.0) 
		#Generación del mensaje I2C de tipo lectura
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data) #Número de bytes que se leerán del esclavo
		i2c.i2c_rdwr(msg) #En este caso lectura en I2C (escritura en el canal SDA)
		print('Escribiendo retraso de fase: {:0.5f} ({:0.1f}ms)'.format(delay/1000.0, delay))
	except Exception as ex:
		raise ex

def powerf2ms(pw):
	# Student's code here
	return pw

#Función para desplegar ayuda al usuario
def ayuda():
	try:
		archivo = open(HELP_FILE, 'r')
		print(archivo.read())
	except:
		print("ERROR: No se pudo abrir el archivo: ", HELP_FILE)
	finally:
		archivo.close()
	exit() #Salir inmediatamente del programa

def main():
	#Comentar si es una implementación de hardware
	run_dimmer_board(freq=60)
	# Apagando lámpara
	sleep(1)
	writePhase(1000/60)

	while True:
		try:
			entrada = input("Introducir factor de potencia (y tiempo de transición): ")
			valores = entrada.split()
			num_in = len(valores)
			if (num_in > 2):
				print("ERROR: Se introdujeron más de 2 valores a la entrada, volver a intentarlo.\n")
			else:
				print(valores)
			#writePhase(powerf2ms(pf))
		except KeyboardInterrupt:
			return
		except:
			print("ERROR: No se introdujo valores correctos, vuelva a introducirlos")
			continue

if __name__ == '__main__':
	main()
