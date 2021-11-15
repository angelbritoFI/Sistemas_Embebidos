#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.6
# Date: 15/11/2021
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

def powerf2ms(pw, frec):
	if frec == 60:
		t_disparo = {100: 0, 95: 1.196, 90: 1.707, 85: 2.11, 80: 2.46, 75: 2.778, 70: 3.075,
		65: 3.3582, 60: 3.6328, 55: 3.901, 50: 4.1666, 45: 4.4322, 40: 4.701, 35: 4.975, 
		30: 5.258, 25: 5.5555, 20: 5.8739, 15: 6.2235, 10: 6.626, 5: 7.137, 0: 8.33}
	else:
		t_disparo = {100: 0, 95: 1.435, 90: 2.048, 85: 2.532, 80: 2.952, 75: 3.333, 70: 3.69,
		65: 4.03, 60: 4.359, 55: 4.681, 50: 5, 45: 5.319, 40: 5.641, 35: 5.97, 
		30: 6.31, 25: 6.667, 20: 7.048, 15: 7.468, 10: 7.952, 5: 8.564, 0: 10}
	for i in range(0, 105, 5):
		if (i <= pw <= (i+5)):
			pw = t_disparo[i] + (((t_disparo[i+5] - t_disparo[i])/5)*(pw-i))
			break
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

#Función para recibir los parámetros opcionales del programa
def procesa_parametros(num_parametros):
	if num_parametros > 1:
		if num_parametros == 2:
			try:
				frecuencia = int(argv[1].strip("Hz"))
			except:
				print("ERROR: No se introdujo un valor entero a la frecuencia.")
				ayuda()
			if not ((frecuencia == 50) or (frecuencia == 60)):				
				print("ERROR: Frecuencia promedio de ",frecuencia,"Hz no es posible.", sep="")
				ayuda()
		else:
			print("ERROR: Se recibieron", num_parametros, "parámetros.")
			ayuda()
	else: #Valor predeterminado
		frecuencia = 60 #Frecuencia en Hertz
	return frecuencia

def main():
	param = len(argv) #Número de parámetros recibidos por línea de comandos
	frecuencia = procesa_parametros(param)
	#Comentar si es una implementación de hardware
	run_dimmer_board(freq=frecuencia)
	# Apagando lámpara
	sleep(1) #Esperar un segundo
	writePhase(1000/60)
	factor_potencia = 0 #Se inicia en 0%
	while True:
		try:
			entrada = input("Introducir factor de potencia (y tiempo de transición): ")
			valor = entrada.split()
			num_in = len(valor)
			if (num_in > 2):
				print("ERROR: Se introdujeron más de 2 valores a la entrada, vuelva a intentarlo.\n")
			else:
				pf = float(valor[0])
				if num_in > 1:
					t = int(valor[1])
					if t == 0:
						writePhase(powerf2ms(pf, frecuencia))
					elif (0 < t < 11):
						diferencia = (pf - factor_potencia)/t
						for i in range(0,t):
							sleep(1) #Esperar un segundo
							factor_potencia = factor_potencia + diferencia
							writePhase(powerf2ms(factor_potencia, frecuencia))
					else:
						print("ERROR: El tiempo de transición es entre 0 y 10 segundos, vuelva a introducir valores.\n")
				else: #Valor predeterminado de 0 segundos
					writePhase(powerf2ms(pf, frecuencia))
				factor_potencia = pf
		except KeyboardInterrupt:
			return
		except:
			print("ERROR: No se introdujeron valores correctos, vuelva a introducirlos.\n")
			continue

if __name__ == '__main__':
	main()
