#Data collection file code 

import cv2
import numpy as np
import HandLandMarks as HM
import csv

#Setting up camera dimensions
width = 1280
height = 720

#Initializing the webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#Calling the class that finds the hand landmarks 
FindHands = HM.mpHands(1)

#Defining the key points and CSV file
KeyPoints = [0, 4, 8, 12, 16, 20, 5, 9, 13, 17]
csv_file = 'gesture_data.csv'

#Opening the CSV file to save landmarks and labels
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    header = [f'landmark_{i}_x' for i in range(21)] + [f'landmark_{i}_y' for i in range(21)] + ['label']
    writer.writerow(header)

    #Data collection loop
    print("Press 'r' for Rock, 'p' for Paper, 's' for Scissors, 'q' to quit")
    while True:
        ignore, frame = cam.read()

        #Checking if frame was captured
        if not ignore:
            print("Error: Could not read frame.")
            break

        HandsLm = FindHands.Lmarks(frame)

        if HandsLm:
            for hand in HandsLm:
                for idx in KeyPoints:
                    cv2.circle(frame, hand[idx], 5, (0, 0, 255), 2)  #Drawing the landmark points

            #Saving the landmarks to the CSV file if a gesture is detected
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                label = 'rock'
            elif key == ord('p'):
                label = 'paper'
            elif key == ord('s'):
                label = 'scissors'
            elif key == ord('q'):
                break
            else:
                label = None

            if label:
                landmarks = [coord for point in hand for coord in point]
                #Save landmarks and label to CSV
                writer.writerow(landmarks + [label])
                print(f"Saved {label} gesture")

        cv2.imshow("My WebCam", frame)

cam.release()
cv2.destroyAllWindows()
