import logging
import threading
from pymodbus.client.sync import ModbusSerialClient
import Barcode_scanning_functions
import Weighing_function
import socket 
import sys

CamIP = '192.168.1.20'
CamPort = 3000

def dimmension_calculations(dimensions):
    # Find the substring containing the dimensions
    start_index = dimensions.find("volume=")
    if start_index == -1:
        return None, None, None, None
    end_index = dimensions.find(", center")
    if end_index == -1:
        return None, None, None, None

    dimensions_string = dimensions[start_index:end_index]

    # Split the dimensions substring by commas to separate key-value pairs
    pairs = dimensions_string.split(', ')
    
    # Initialize variables to store extracted values
    volume = None
    length = None
    width = None
    height = None
    
    # Iterate over key-value pairs
    for pair in pairs:
        # Split each pair into key and value
        key, value = pair.split('=')
        # Check key and assign value to corresponding variable
        if key == 'volume':
            volume = float(value)
        elif key == 'length':
            length = float(value)
        elif key == 'width':
            width = float(value)
        elif key == 'height':
            height = float(value)
    
    # Return extracted values as a tuple
    return volume, length, width, height

def dimension_data(ip, port, dimension_socket):
    serveradd = (CamIP,CamPort)
    # Create a TCP/IP socket
    try: 
        dimension_socket.connect_ex(serveradd)
        while True:
            dimension_socket.sendall(bytes("20|01|0001",'utf-8'))
            dim_data = dimension_socket.recv(1024)
            dimensions = dim_data.decode('utf-8')
            #dimensions = "volume=4402043.000000, length=273.372162, width=150.322479, height=118.000000, center.x=-26.884029, center.y=7.321197, center.z=1190.816406"
            volume, length, width, height = dimmension_calculations(str(dimensions))
            return volume, length, width, height 
                    
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        dimension_socket.close()
        


def main():

    # Start receiving dimensioning data in a separate thread
    dimension_thread = threading.Thread(target=dimension_data, args=(CamIP, CamPort))
    dimension_thread.start()

    # Add your other main functionality here
    # For example, you can start barcode scanning and weighing processes in separate threads

if __name__ == "__main__":
    main()

