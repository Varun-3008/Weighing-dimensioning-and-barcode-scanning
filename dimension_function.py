import threading
from pymodbus.client.sync import ModbusSerialClient
import psycopg2


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
    boxvolume = length*width*height
    if volume/boxvolume >0.9:
        isbox = True
    return boxvolume, volume, length, width, height, isbox

def dimension_data(ip, port, dimension_socket,conn,cursor,uuid_val):
    serveradd = (ip,port)
    # Create a TCP/IP socket
    try: 
        dimension_socket.connect_ex(serveradd)
        dimension_socket.sendall(bytes("20|01|0001",'utf-8'))
        dim_data = dimension_socket.recv(1024)
        dimensions = dim_data.decode('utf-8')
        #dimensions = "volume=4402043.000000, length=273.372162, width=150.322479, height=118.000000, center.x=-26.884029, center.y=7.321197, center.z=1190.816406"
        boxvolume, volume, length, width, height, isbox = dimmension_calculations(str(dimensions))
        
        if volume:
            try: 
                cursor.execute("UPDATE profiling SET length_mm = %s, width_mm = %s, height_mm = %s, realvolume1 = %s, boxvolume1 = %s, isbox = %s WHERE id = %s", (length, width, height, volume, boxvolume, isbox,uuid_val))
                conn.commit()
                print("Dimension data sucessfully inserted.")
                return boxvolume, volume, length, width, height, isbox
            except Exception as e:
                conn.rollback()
                print("Errr inserting dimensions into database:", e)
                      
    except Exception as e:
        print("Error:", e)


