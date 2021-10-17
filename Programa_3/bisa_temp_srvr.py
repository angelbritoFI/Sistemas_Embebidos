#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.5
# Date: 17/10/2021
# Description: Leer temperatura del sensor LM35 a través del ADC del Arduino
#	Este convertidor analógico-digital está conectado como esclavo I2C

# ## ###############################################
# Fundamentos de Sistemas Embebidos, Semestre 2022-1
# -*- coding: utf-8 -*-
# Autor: Mauricio Matamoros
# License: MIT
# ## ###############################################

import smbus2 #Lectura del puerto serial I2C
import struct #Conversión de datos binarios a objetos que puede leer Python
# Importación de la función sleep del módulo time para control mediante tiempos de espera
from time import sleep, strftime
# Importación de la función argv del módulo sys para recibir parámetros desde línea de comandos
from sys import argv

# Inicialización de placa virtual (comentar si es implementación en hardware)
from virtualboards import run_temperature_board

# Dirección del dispositivo I2C
SLAVE_ADDR = 0x0A # Dirección I2C del Arduino

# Archivo en el cual se mantiene una bitácora de temperaturas
LOG_FILE = './temp_history.py'
# Archivo en el cual se muestra ayuda al usuario como ejecutar el programa
HELP_FILE = './bisa_ayuda.txt'

# Inicializar el bus I2C instanciando al objeto SMBus
# Como parámetro se indica el número de dispositivo a controlar
i2c = smbus2.SMBus(1)

# Lectura de los bytes de temperatura registrada por Arduino via I2C
def readTemperature(Varef, resolucion):
	if resolucion:
		#Resolución de 8 bits
		num_bytes = 1
		lectura = '<B'
		volt_celsius = 2.56
	else:
		#Resolución de 10 bits
		num_bytes = 2
		lectura = '<H'
		volt_celsius = 10.24
	try:
		#Generación del mensaje I2C de tipo lectura
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, num_bytes) #Número de bytes que se leerán del esclavo
		i2c.i2c_rdwr(msg) #En este caso lectura en I2C (escritura en el canal SDA)		
		data = list(msg)
		""" Función unpack:
		Recibe un bytearray y un especificador de formato (interpreta los bytes en el arreglo
			para generar tupla de n elementos)
		Tiene 2 tipos de lectura:
			- 1 byte (ADC de 8 bits): '<B'
			- 2 bytes (ADC de 10 bits): '<H' -unsigned half int-
		Hace la codificación por defecto en I2C:
			little endian: codifica los bytes con el LSB a la izquierda
		"""
		temp = struct.unpack(lectura, msg.buf)[0]
		temp = temp * (Varef/volt_celsius) #Conversión de valores discretos a °C
		print('Temperatura registrada por el ADC: {:0.2f}°C'.format(temp))
		return temp
	except:
		return None

# Escritura de la bitácora de temperaturas en archivo externo
def log_temp(temperature):
	try:
		with open(LOG_FILE, 'a') as fp:
			fp.write('{} {:0.2f}°C\n'.format(strftime("%d/%m/%Y %H:%M:%S"),temperature))
	except:
		return

def ayuda():
	try:
		archivo = open(HELP_FILE, 'r')
		print(archivo.read())
	except:
		print("ERROR: No se pudo abrir el archivo: ", HELP_FILE)
	finally:
		archivo.close()
	exit() #Salir inmediatamente del programa

#Valores de resistencia para el divisor de voltaje
def resistencias(valores):
	bandera = True
	res = valores.split(",")
	res_dv = []
	if len(res) < 2:
		print("ERROR: Falta especificar el valor de la resitencia 2.")
		ayuda()
	else:
		#Se llena el arreglo de resistencias dadas en línea de comandos
		for r in res:
			try:
				res_dv.append(float(r[3:]))
			except:
				print("ERROR: No se introdujo un valor numérico a la resistencia.")
				ayuda()
	#Se corroborán que los valores sean los adecuados
	for R in res_dv:
		if (R < 1.0 or R > 100000.0):
			print("ERROR: Resistencia de ",R," kilo Ohms no es posible en el ADC.", sep="")
			ayuda()
	return bandera, res_dv[0], res_dv[1]

#Resolución de bits del ADC
def resolucion_bits(formato):
	bandera = True
	try:
		bits = int(formato.strip("b="))
	except:
		print("ERROR: No se introdujo un valor entero a la resolución.")
		ayuda()
	if bits == 8:
		ADC8bits = True
	elif bits == 10:
		ADC8bits = False
	else:
		print("ERROR: Resolución de ",bits," bits no es posible en el ADC.", sep="")
		ayuda()
	return bandera, ADC8bits

#Frecuencia de operación del ADC
def frecuenciaADC(valor):
	bandera = True
	try:
		f_hertz = float(valor.strip("f="))
	except:
		print("ERROR: No se introdujo un valor numérico a la frecuencia.")
		ayuda()
	if (f_hertz < 1.0 or f_hertz > 100.0):
		print("ERROR: Frecuencia de ",f_hertz," Hertz no es posible en el ADC.", sep="")
		ayuda()
	return bandera, f_hertz

#Función para recibir los parámetros opcionales del programa
def procesa_parametros(num_parametros):
	# Banderas de apoyo para parámetros opcionales
	p_resistencias = False
	p_resolucion = False
	p_frecuencia = False
	# Valores de resistencias comerciales que permite el rango de 0 a 150 °C
	R1 = 10
	R2 = 3.9
	res_8bits = False #Resolución del convertidor a 10 bits
	frecuencia = 3 #Frecuencia en Hertz
	if(1 < num_parametros < 5):
		for i in range(1,num_parametros):
			if argv[i].find("R1=") != -1:
				if p_resistencias == False:
					p_resistencias, R1, R2 = resistencias(argv[i])
				else:
					print("ERROR: No es posible más de cuatro valores de resistencias.")
					ayuda()
			elif argv[i].find("b=") != -1:
				if p_resolucion == False:
					p_resolucion, res_8bits = resolucion_bits(argv[i])
				else:
					print("ERROR: No es posible más de dos valores de resolución.")
					ayuda()
			elif argv[i].find("f=") != -1:
				if p_frecuencia == False:
					p_frecuencia, frecuencia = frecuenciaADC(argv[i])
				else:
					print("ERROR: No es posible más de dos valores de frecuencia.")
					ayuda()
			else:
				print("ERROR: Parámetro '", argv[i], "' incorrecto.", sep="")
				ayuda()
	elif num_parametros > 4:
		print("ERROR: Exceso de parámetros opcionales.")
		ayuda()
	return R1, R2, res_8bits, frecuencia

def main():
	temperaturas_celsius = [] #Almacenar todas las temperaturas registradas
	param = len(argv) #Número de parámetros recibidos por línea de comandos
	r1, r2, resADC8bits, frec = procesa_parametros(param)
	"""
	Simulación de un sensor de temperatura LM35 en configuración básica acoplado 
	a un circuito ADC con un divisor de voltaje en Vref+ y Vref− a tierra
	Parámetros:
		- Resistencias para la alimentación del Vref+:
			r1 (por defecto 1 kOhm)
			r2 (por defecto 1 MOhm)
		- p8bits: valor booleano que configura el módulo ADC para operar a una 
				precisión de 8 bits (True) o 10 bits (False, valor por defecto)
	"""
	#Comentar si es una implementación de hardware
	run_temperature_board(r1, r2, resADC8bits, frec)
	Vref = 5 * r2/(r2+r1) #Voltaje de referencia del ADC de acuerdo al divisor de voltaje
	sleep(1) #Esperar 1 segundo

	# Ciclo infinito para lectura de temperaturas
	while True:
		try:
			sumatoriaTemp = 0
			temperaturas_celsius.append(readTemperature(Vref,resADC8bits))
			# Obteniendo la temperatura promedio registrada por el sensor
			for t in temperaturas_celsius:
				sumatoriaTemp = sumatoriaTemp + t
			temp_promedio = sumatoriaTemp/len(temperaturas_celsius)
			log_temp(temp_promedio)
			sleep(1) #Lecturas cada segundo
		except:
			print("\tPrograma terminado")
			return

if __name__ == '__main__':
	main()
