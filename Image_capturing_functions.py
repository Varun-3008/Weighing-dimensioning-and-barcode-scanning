import cv2 as cv
import os
import psycopg2
from datetime import datetime

image_path = None
# Open a connection to the camera
def get_img(camera_url,save_folder,cursor,conn,uuid):
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
    image_name = f"captured_image_{timestamp}.jpg"
    image_path = os.path.join(save_folder, image_name)
    cv.imwrite(image_path, frame)
    cursor.execute("UPDATE profiling SET timestamp = %s WHERE id = %s", (timestamp,uuid))
    conn.commit()
    # Release the camera
    overlay_img = cv.imread(image_path)
    overlay_img = cv.resize(overlay_img,(1600,900))
    if overlay_img is not None:
        # Display the image
        while True:
            cv.imshow("Image", overlay_img)
            if cv.waitKey(10) & 0xFF==ord(' '):
                break
            cv.waitKey(0)  # Wait for a key press
            cv.destroyAllWindows()  # Close the window when a key is pressed
    cap.release()
    print("Image captured successfully and saved to:", image_path)
    

    
