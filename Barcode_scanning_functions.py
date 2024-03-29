import serial
import logging
import psycopg2

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
def insert_barcode_data(barcode,conn,cursor,uuid_value,db):
    try:
        cursor.execute("UPDATE profiling SET barcode = %s WHERE id = %s", (barcode, uuid_value))
        conn.commit()
        db['barcode']  = barcode
        db['uuid'] = uuid_value
        print("Barcode data sucessfully inserted.")
    except Exception as e:
        conn.rollback()
        print("Errr inserting Barcode into database:", e)
