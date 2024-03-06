import logging
import threading
import _thread
from pymodbus.client.sync import ModbusSerialClient
import Barcode_scanning_functions
import Weighing_function
import dimension_function
import socket
import uuid
import psycopg2

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
            # Start threads for reading weight and dimension data
            weight_thread = threading.Thread(target=Weighing_function.read_weight, args=(client,))
            dimension_thread = threading.Thread(target=dimension_function.dimension_data, args=(dimCamIP, dimCamPort, dimension_socket))
            
            weight_thread.start()
            dimension_thread.start()
            
            # Wait for both threads to finish before continuing
            weight_thread.join()
            dimension_thread.join()
            
            print(f"Barcode: {barcode}")

           # print(f"Barcode: {barcode}, Weight: {weight_gms} g, {weight_kg} kg, volume = {volume :.0f}, length = {length :.2f}, width = {width :.2f}, height = {height :.2f}")
