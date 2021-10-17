#!/usr/bin/env python3
# Author: Brito Segura Angel
# Version 1.0
# Date: 16/10/2021
# Description: Leer temperatura del sensor LM35 a través del ADC del Arduino
#	Este convertidor analógico-digital está conectado como esclavo I2C

# ## ###############################################
# Fundamentos de Sistemas Embebidos, Semestre 2022-1
# -*- coding: utf-8 -*-
# Autor: Mauricio Matamoros
# License: MIT
# ## ###############################################

import smbus2
import struct
import time

# Initializes virtual board (comment out for hardware deploy)
from virtualboards import run_temperature_board

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino

# Name of the file in which the log is kept
LOG_FILE = './temp.log'

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def readTemperature():
	"""Reads a temperature bytes from the Arduino via I2C"""
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 1)
		i2c.i2c_rdwr(msg)
		data = list(msg)
		temp = struct.unpack('<B', msg.buf)[0]
		print('Received ADC temp value: {} = {:0.2f}'.format(data, temp))
		return temp
	except:
		return None
#end def

def log_temp(temperature):
	try:
		with open(LOG_FILE, 'a') as fp:
			fp.write('{} {:0.2f}C\n'.format(
				time.strftime("%Y.%m.%d %H:%M:%S"),
				temperature
			))
	except:
		return
#end def

def main():
	"""
	Simulación de un sensor de temperatura LM35 en configuración básica acoplado 
	a un circuito ADC con un divisor de voltaje en Vref+ y Vref− a tierra
	Parámetros:
		- Resistencias para la alimentación del Vref+:
			r1 (por defecto 1 kOhm)
			r2 (por defecto 1 MOhm)
		- p8bits: valor booleano que configura el módulo ADC para operar a una 
				precisión de 8 bits (True) o 10 bits (False)
	"""
	run_temperature_board() #Comentar si es una implementación de hardware
	time.sleep(1)

	while True:
		try:
			cTemp = readTemperature()
			log_temp(cTemp)
			time.sleep(1)
		except KeyboardInterrupt:
			return

if __name__ == '__main__':
	main()
