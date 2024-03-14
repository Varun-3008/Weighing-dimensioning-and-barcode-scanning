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
import json

# Define constants
baudrate = 9600
z1comport = 'COM7'
usbport = 'COM8'
timeout = 1
dimCamIP = '192.168.1.20'
dimCamPort = 3000
serveradd = (dimCamIP, dimCamPort)
registeradd = 0
unit = 1
camera_url = "rtsp://admin:Nido@123@192.168.1.64/Streaming/channels/1/"
save_folder = "C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Images"
overlay_save_folder = "C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Images\\Overlay"
UI_save_folder = "C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Static"
db = {"barcode" : 0, "uuid": "0", "weight_gms" : 0, "weight_kgs": 0, "boxvolume" : 0, "volume" : 0, "length" : 0, "width" : 0, "height" : 0, "isbox" : False }
HOST = '127.0.0.1'  # Use '0.0.0.0' to listen on all available interfaces
PORT = 5001        # Choose a port number (e.g., 12345)

def create_socket_host(HOST, PORT, db):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode()
        
        if data == "ping":
            # Convert the dictionary to a JSON string
            data_to_send = json.dumps(db)
            
            # Send the JSON string to the client
            client_socket.send(data_to_send.encode())
            client_socket.close()

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
    start_new_thread(create_socket_host, (HOST, PORT, db))

    while True:
        # Your barcode scanning and other processing logic here
        barcode = Barcode_scanning_functions.scan_barcode(ser)
        if barcode:  # If a barcode is scanned
            uuid_val = UUID_functions.generate_and_insert_uuid(conn, cursor)
            start_new_thread(Barcode_scanning_functions.insert_barcode_data,(barcode,conn,cursor,uuid_val,db))
            start_new_thread(Weighing_function.read_weight,(client,registeradd,unit,conn,cursor,uuid_val,db))
            start_new_thread(dimension_function.dimension_data,(dimCamIP, dimCamPort, dimension_socket,conn,cursor,uuid_val,db))
            start_new_thread(Image_capturing_functions.get_img,(camera_url,save_folder,cursor,conn,uuid_val,overlay_save_folder,db,UI_save_folder))
cursor.close()
conn.close()
