import cv2
import numpy as np
import HandLandMarks as HM
import csv

# Set up camera dimensions
width = 1280
height = 720

# Initialize the webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Check if the webcam is opened correctly
if not cam.isOpened():
    print("Error: Could not open webcam.")
    exit()

FindHands = HM.mpHands(1)

# Define the key points and CSV file
KeyPoints = [0, 4, 8, 12, 16, 20, 5, 9, 13, 17]
csv_file = 'gesture_data.csv'

# Open CSV file to save landmarks and labels
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    header = [f'landmark_{i}_x' for i in range(21)] + [f'landmark_{i}_y' for i in range(21)] + ['label']
    writer.writerow(header)

    # Data collection loop
    print("Press 'r' for Rock, 'p' for Paper, 's' for Scissors, 'q' to quit")
    while True:
        ignore, frame = cam.read()

        # Check if frame was captured
        if not ignore:
            print("Error: Could not read frame.")
            break

        HandsLm = FindHands.Lmarks(frame)

        # Draw landmarks if hands are detected
        if HandsLm:
            for hand in HandsLm:
                for idx in KeyPoints:
                    cv2.circle(frame, hand[idx], 5, (0, 0, 255), 2)  # Draw the landmark points

            # Save landmarks to CSV if a gesture is detected
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
                # Save landmarks and label to CSV
                writer.writerow(landmarks + [label])
                print(f"Saved {label} gesture")

        # Show the frame with landmarks
        cv2.imshow("My WebCam", frame)

# Release the camera and close any OpenCV windows
cam.release()
cv2.destroyAllWindows()
