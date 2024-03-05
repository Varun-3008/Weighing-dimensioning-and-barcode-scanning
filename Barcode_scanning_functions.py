import serial
import logging

# Define constants
baudrate = 9600
z1comport = 'COM7'
usbport = 'COM8'

def setup_loggingbarcode():
    # Configure logging to log to both file and console
    logging.basicConfig(filename='barcodedata.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def open_serial_port(port=z1comport, baudrate=baudrate, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        logging.info("Serial port connection established successfully.")
        return ser
    except serial.SerialException as e:
        logging.error(f"Failed to open serial port: {e}")
        return None

def close_serial_port(ser):
    if ser:
        ser.close()
        logging.info("Serial port connection closed.")

def scan_barcode(ser):
    try:
        while True:
            # Read data from serial port
            barcode_data = ser.readline().strip().decode('utf-8')
            
            if barcode_data:
                logging.info("Scanned Barcode: %s", barcode_data)
                return barcode_data  # Return scanned barcode data
            
            # Process the barcode data as needed
            
    except KeyboardInterrupt:
        close_serial_port(ser)

def main():
    setup_loggingbarcode()
    ser = open_serial_port()
    if ser:
        scan_barcode(ser)

if __name__ == "__main__":
    main()
