import logging
import threading
from _thread import start_new_thread
from pymodbus.client.sync import ModbusSerialClient
import socket
import psycopg2
import time
import Barcode_scanning_functions
import Weighing_function
import dimension_function
import UUID_functions
import Image_capturing_functions



# Define constants
baudrate = 9600
z1comport = 'COM7'
usbport = 'COM8'
timeout = 1
dimCamIP = '192.168.1.20'
dimCamPort = 3000
serveradd = (dimCamIP,dimCamPort)
registeradd = 0
unit = 1
camera_url = "rtsp://admin:Nido@123@192.168.1.64/Streaming/channels/1/"
save_folder = "C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Images"
overlay_save_folder = "C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Images\\Overlay"

def setup_logging():
    Barcode_scanning_functions.setup_loggingbarcode()
    Weighing_function.setup_loggingweight()
    
    
ser = Barcode_scanning_functions.open_serial_port(z1comport, baudrate, timeout)
client = Weighing_function.open_modbus_serial_port(usbport, baudrate)
dimension_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dimension_socket.connect_ex(serveradd)

conn = psycopg2.connect(
        dbname="Capella test",
        user="postgres",
        password="1234",
        host="127.0.0.1",
        port="5432"
    )
cursor = conn.cursor()

print("Connected to dimensioning server at {}:{}".format(dimCamIP, dimCamPort))

if ser and client:
    setup_logging()
    while True:
        barcode = Barcode_scanning_functions.scan_barcode(ser)
        if barcode:  # If a barcode is scanned
            uuid_val = UUID_functions.generate_and_insert_uuid(conn, cursor)
            time.sleep(0.5)
            start_new_thread(Barcode_scanning_functions.insert_barcode_data,(barcode,conn,cursor,uuid_val))
            weight_gms, weight_kg = start_new_thread(Weighing_function.read_weight,(client,registeradd,unit,conn,cursor,uuid_val))
            start_new_thread(dimension_function.dimension_data,(dimCamIP, dimCamPort, dimension_socket,conn,cursor,uuid_val))
            start_new_thread(Image_capturing_functions.get_img,(camera_url,save_folder,cursor,conn,uuid_val))



    #weight_gms, weight_kg = 
    #boxvolume, volume, length, width, height, isbox = 
    cursor.close()
    conn.close()