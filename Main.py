import logging
import threading
from _thread import start_new_thread
from pymodbus.client.sync import ModbusSerialClient
import Barcode_scanning_functions
import Weighing_function
import dimension_function
import socket

# Define constants
baudrate = 9600
z1comport = 'COM7'
usbport = 'COM8'
timeout = 1
dimCamIP = '192.168.1.20'
dimCamPort = 3000
serveradd = (dimCamIP,dimCamPort)


def setup_logging():
    Barcode_scanning_functions.setup_loggingbarcode()
    Weighing_function.setup_loggingweight()
    
ser = Barcode_scanning_functions.open_serial_port(z1comport, baudrate, timeout)
client = Weighing_function.open_modbus_serial_port(usbport, baudrate)
dimension_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dimension_socket.connect_ex(serveradd)

print("Connected to dimensioning server at {}:{}".format(dimCamIP, dimCamPort))

if ser and client:
    setup_logging()
    while True:
        barcode = Barcode_scanning_functions.scan_barcode(ser)
        if barcode:  # If a barcode is scanned
            weight_gms, weight_kg = Weighing_function.read_weight(client)
            volume, length, width, height = dimension_function.dimension_data(dimCamIP, dimCamPort, dimension_socket)
            print(f"Barcode: {barcode}, Weight: {weight_gms} g, {weight_kg} kg, volume = {volume}, length = {length}, width = {width}, height = {height}")
