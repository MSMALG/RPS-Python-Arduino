# gesture_recno.py
import csv
import HandLandMarks as HM
import cv2
import numpy as np
import math

def calc_distance(landmarksData):
    dMatrix = np.zeros([len(landmarksData), len(landmarksData)], dtype="float")
    palmSize = math.sqrt((landmarksData[0][0] - landmarksData[9][0])**2 +
                         (landmarksData[0][1] - landmarksData[9][1])**2)

    for from_pt in range(len(landmarksData)):
        for to_pt in range(len(landmarksData)):
            dMatrix[from_pt][to_pt] = (math.sqrt((landmarksData[from_pt][0] - landmarksData[to_pt][0])**2 + 
                                                (landmarksData[from_pt][1] - landmarksData[to_pt][1])**2)) / palmSize      
    return dMatrix

def calc_error(knownGesture, unknownGesture, keyPts):
    ErrorSignal = 0
    for from_pnt in keyPts:
        for to_pnt in keyPts:
            ErrorSignal += abs(knownGesture[from_pnt][to_pnt] - unknownGesture[from_pnt][to_pnt])
    return ErrorSignal

def gesture_identifier(knownGestures, unknownGesture, keypts, GestNames, tolerance):
    errorArray = []
    for i in range(len(GestNames)):
        error = calc_error(knownGestures[i], unknownGesture, keypts)
        errorArray.append(error)

    MinimumError = errorArray[0]
    minimumIndex = 0

    for j in range(len(errorArray)):
        if errorArray[j] < MinimumError:
            MinimumError = errorArray[j]
            minimumIndex = j
    if MinimumError < tolerance:
        gesture = GestNames[minimumIndex]
    else:
        gesture = "Unknown"

    return gesture

# Loading known gestures and labels
known_gestures = []
labels = []

with open('gesture_data.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        landmarks = list(map(float, row[:-1]))  # All but the last column
        label = row[-1]  # Last column is the label
        landmarks = np.array(landmarks).reshape(-1, 2)
        known_gestures.append(calc_distance(landmarks))  # Store distance matrices
        labels.append(label)

KeyPoints = [0, 4, 8, 12, 16, 20, 5, 9, 13, 17]

# Set up camera dimensions
width = 1280
height = 720
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Initialize the hand landmarks detection
FindHands = HM.mpHands(1)

# Main loop for gesture recognition
while True:
    ignore, frame = cam.read()

    # Check if frame was captured
    if not ignore:
        print("Error: Could not read frame.")
        break

    HandsLm = FindHands.Lmarks(frame)

    if HandsLm:
        for hand in HandsLm:
            # Calculate the distance matrix for the current hand
            unknown_gesture = calc_distance(hand)

            # Identify the gesture
            gesture = gesture_identifier(known_gestures, unknown_gesture, KeyPoints, labels, tolerance=10)
            cv2.putText(frame, f'Gesture: {gesture}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Draw landmarks
            for idx in KeyPoints:
                cv2.circle(frame, hand[idx], 5, (0, 0, 255), 2)  # Draw the landmark points

    # Show the frame with gesture recognition
    cv2.imshow("Gesture Recognition", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any OpenCV windows
cam.release()
cv2.destroyAllWindows()
