import cv2 as cv
import os
import psycopg2
from datetime import datetime
from _thread import start_new_thread

image_path = None
# Open a connection to the camera
def get_img(camera_url,save_folder,cursor,conn,uuid,overlay_save_folder,db,UI_save_folder):
    cap = cv.VideoCapture(camera_url)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        exit()
    # Save the captured frame as an image in the specified folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_name = f"{uuid}captured_image_{timestamp}.jpg"
    image_path = os.path.join(save_folder, image_name)
    cv.imwrite(image_path, frame)
    get_overlay_image(uuid,overlay_save_folder,timestamp,db,UI_save_folder)
    cursor.execute("UPDATE profiling SET timestamp = %s WHERE id = %s", (timestamp,uuid))
    conn.commit()

    # Release the camera

    cap.release()
    print("Image captured successfully and saved to:", image_path)
    
def get_overlay_image(uuid_val,overlay_save_folder,timestamp,db,UI_save_folder):
    # Get a list of all files in the current directory
    files = os.listdir("C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Images")
    
    # Search for the file with the UUID prefix
    image_filename = None
    for filename in files:
        if filename.startswith(uuid_val):
            image_filename = f"C:\\Users\\varun\\OneDrive\\Desktop\\Python\\Weighing-dimensioning-and-barcode-scanning\\Images\\{filename}" 
            break
    
    # Check if the file exist
    if image_filename is not None:
        # Read the image
        image = cv.imread(image_filename)
        start_new_thread(cv.putText,(image,f"barcode = {db['barcode']}", (10,30), cv.FONT_HERSHEY_COMPLEX, 0.75, (0,255,0), 2))
        start_new_thread(cv.putText,(image,f"uuid = {db['uuid']}",(10,60),cv.FONT_HERSHEY_COMPLEX,0.75,(0,255,0),2))
        start_new_thread(cv.putText,(image,f"weight_gms = {db['uuid']}, weight_kgs = {db['weight_kgs']}",(10,90),cv.FONT_HERSHEY_COMPLEX,0.75,(0,255,0),2))
        start_new_thread(cv.putText,(image,f"length = {db['length']}, width = {db['width']}, height = {db['height']}",(10,120),cv.FONT_HERSHEY_COMPLEX,0.75,(0,255,0),2))
        start_new_thread(cv.putText,(image,f"volume = {db['volume']}, box_volume = {db['boxvolume']}",(10,150),cv.FONT_HERSHEY_COMPLEX,0.75,(0,255,0),2))
        overlay_image_name =  f"{uuid_val}Overlayed_image_{timestamp}.jpg"
        save_location = os.path.join(overlay_save_folder,overlay_image_name)
        UI_save_location = os.path.join(UI_save_folder,overlay_image_name)
        cv.imwrite(save_location, image)
        cv.imwrite(UI_save_location,image)
    else:
        print(f"Error: Image file starting with '{uuid_val}' not found.")