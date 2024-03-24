import cv2, time, pandas
import numpy as np
import client
import serial
import time
import threading


num_diff_frames = 2
threshold_value = 30
static_back = None
diff_frames = []
  
ser= serial.Serial('COM5',9600,timeout=1)

def send_angles(x_angle,y_angle):
    ser.write(bytes([x_angle,y_angle]))

df = pandas.DataFrame(columns = ["Start", "End"])
  

video = cv2.VideoCapture(0)


def create_circular_mask(h, w, center=None, radius=None):

    if center is None: 
        center = (int(w/2), int(h/2))
    if radius is None: 
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    mask = np.array(mask, dtype = np.uint8)
    return mask
    

kernel = create_circular_mask(45,45)
kernel_laser = create_circular_mask(53,53)
 
while True:
        
        check, frame = video.read()

      
       
        blurred = cv2.GaussianBlur(frame, (21, 21), 1)
      
        
        if static_back is None:
            static_back = blurred
            continue
      
        
        static_back_copy_non_red = static_back.copy()
        static_back_copy_non_red[:,:,2] = 0
        blurred_copy_non_red = blurred.copy()
        blurred_copy_non_red[:,:,2] = 0
        diff_frame_non_red = cv2.absdiff(static_back_copy_non_red, blurred_copy_non_red)
        
        blurred_copy_red = blurred.copy()
        blurred_copy_red[:,:,:2] = 0
        blurred_copy_red = cv2.threshold(blurred_copy_red, 150, 255, cv2.THRESH_BINARY)[1]
        blurred_copy_red = cv2.dilate(blurred_copy_red, kernel_laser, iterations = 1)
        blurred_copy_red[:,:,0] = blurred_copy_red[:,:,2]
        blurred_copy_red[:,:,1] = blurred_copy_red[:,:,2]
        
        diff_frame = (diff_frame_non_red.astype(np.int32) * (blurred_copy_red==0)).clip(0, 255).astype(np.uint8)
        
        diff_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY) 
        
        
        diff_frames.append(diff_frame)
        if len(diff_frames)>num_diff_frames:
            diff_frames.pop(0)
        
        diff_frame = np.zeros((480,640),dtype = np.uint8)
        
        for i in range(0,len(diff_frames)):
            diff_frame += diff_frames[i]
        
      

        thresh_frame = cv2.threshold(diff_frame, threshold_value, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, kernel, iterations = 2)
      
        
        cnts,_ = cv2.findContours(thresh_frame.copy(), 
                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      
        frame_cnt = np.array(frame)
        
        biggest = None
        biggest_size = None
        for contour in cnts:
            
            
      
            (x, y, w, h) = cv2.boundingRect(contour)
            if biggest is None or w*h>biggest_size:
                biggest = contour
                biggest_size = w*h
            
            cv2.rectangle(frame_cnt, (x, y), (x + w, y + h), (0, 255, 0), 3)
            x=(x+x+w)/2
            y=(y+y+h)/2
            angle_x=((180 - (x / (640 / 180)))/3)+75
            angle_y=((180 - (y / (480 / 180)))/3)+70
            angle_x=round(angle_x)
            angle_y=round(angle_y)
            
            send_angles(angle_x,angle_y)
            time.sleep(0.01)
      
        
        cv2.imshow("Color Frame (1)", frame)
      
        
        cv2.imshow("Non Red Difference (2)", diff_frame_non_red)
      
       
        cv2.imshow("Red Laser Filter (3)", blurred_copy_red.astype(np.uint8))
      
       
        cv2.imshow("Difference Frame (4)", diff_frame)
      
        
        cv2.imshow("Threshold Frame (5)", thresh_frame)
      
       
        cv2.imshow("Contour Frame (6)", frame_cnt)
      
        key = cv2.waitKey(1)
        
        
        
            
        static_back = blurred 
video.release()
cv2.destroyAllWindows()
