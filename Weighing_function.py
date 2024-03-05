import logging
import keyboard
import threading
from pymodbus.client.sync import ModbusSerialClient


baudrate = 9600
z1comport = 'COM7'
usbport = 'COM8'

weight_gms = 0
weight_kg = 0  
def weight_calculations(weight):
    global weight_kg, weight_gms
    if isinstance(weight, list) and len(weight) >= 2:
        weight_value = weight[1]
        weightgms = float(weight_value) * 10
        weightkg = float(weight_value) * 0.01

        weight_gms = "{:.2f}".format(weightgms)
        weight_kg = "{:.2f}".format(weightkg)
        logging.info("Weight for- GUID: %s, Weight in grams: %s, Weight in Kg: %s", weight_gms, weight_kg)
    else:
        logging.error("Invalid weight data format")
        
        
def setup_logging():
    # Configure logging to log to both file and console
    logging.basicConfig(filename='data.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def open_modbus_serial_port(port= usbport , baudrate=baudrate ):
    try:
        client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, timeout=1)
        if client.connect():
            logging.info("Modbus serial port connection established successfully.")
            return client
        else:
            logging.error("Failed to connect to Modbus serial port.")
            return None
    except Exception as e:
        logging.error(f"Failed to open Modbus serial port: {e}")
        return None

def close_modbus_serial_port(client):
    if client:
        client.close()
        logging.info("Modbus serial port connection closed.")

def read_weight(client, register_address=0, unit = 1):
    try:
        # Read holding register to get weight data
        response = client.read_holding_registers(address=register_address, count=10 , unit=unit)
        if response.isError():
            logging.error("Failed to read weight data from Modbus device.")
            return None
        else:     
            weight = weight_calculations(response.registers)
            logging.info(f"Weight read successfully: {weight}")
            return weight_gms, weight_kg
    except Exception as e:
        logging.error(f"Error reading weight data from Modbus device: {e}")
        return None

def on_space_pressed():
    client = open_modbus_serial_port()
    if client:
        weight = read_weight(client)
        close_modbus_serial_port(client)
        if weight is not None:
            # Process weight data as needed
            print("Weight:", weight)

def main():
    setup_logging()
    logging.info("Press space to read weight...")
    keyboard.add_hotkey('space', on_space_pressed)
    keyboard.wait('esc')

if __name__ == "__main__":
    main()
 