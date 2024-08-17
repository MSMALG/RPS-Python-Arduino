#Main File that contains the hybrid system and implementing it into the game 

import csv
import HandLandMarks as HM
import cv2
import numpy as np
import math
import joblib
import random
import serial  


arduino = serial.Serial(port='COM3', baudrate=115200)  

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

def show_countdown(frame):
    height, width, _ = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 3
    color = (0, 255, 0)
    
    for i in range(3, 0, -1):
        frame_copy = np.zeros_like(frame)  #Creating a blank frame
        text = f'Get ready! {i}'
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        cv2.putText(frame_copy, text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)
        cv2.imshow("Gesture Recognition", frame_copy)
        cv2.waitKey(1000)
    
    frame_copy = np.zeros_like(frame) 
    text = 'Shoot!'
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    cv2.putText(frame_copy, text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)
    cv2.imshow("Gesture Recognition", frame_copy)
    cv2.waitKey(1000)

def control_servos(computer_move):
    #Sending a command to the Arduino to move the servos based on the computer's move.
    
    if computer_move == 'rock':
        arduino.write(b'Computer: Rock\r')
    elif computer_move == 'paper':
        arduino.write(b'Computer: Paper\r')
    elif computer_move == 'scissors':
        arduino.write(b'Computer: Scissors\r')
    else:
        arduino.write(b'Computer: Unknown\r')

def control_leds(result):
    #Sending a command to the Arduino to move the LEDs based on the game result.

    if result == 'Player: Won':
        arduino.write(b'Player: Won\r')
    elif result == 'Player: Lost':
        arduino.write(b'Player: Lost\r')
    elif result == 'It\'s a Tie':
        arduino.write(b'It\'s a Tie\r')
    else:
        arduino.write(b'Unknown\r')


svm_model = joblib.load('svm_gesture_model.pkl')
scaler = joblib.load('scaler.pkl')

known_gestures = []
labels = []
with open('gesture_data.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        landmarks = list(map(float, row[:-1])) 
        label = row[-1]  
        landmarks = np.array(landmarks).reshape(-1, 2)
        known_gestures.append(calc_distance(landmarks))  
        labels.append(label)

#A mapping dictionary for labels
label_mapping = {i: label for i, label in enumerate(labels)}

KeyPoints = [0, 4, 8, 12, 16, 20, 5, 9, 13, 17]

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


FindHands = HM.mpHands(1)

player_gesture = None
computer_gesture = None
countdown_done = False

while True:
    ignore, frame = cam.read()

    if not countdown_done:  #Showing countdown at the beginning of the game
        show_countdown(frame)
        countdown_done = True
        player_gesture = "Unknown"
        computer_gesture = None
        continue

    HandsLm = FindHands.Lmarks(frame)
    
    if HandsLm:
        for hand in HandsLm:
            #Distance based method prediction
            unknown_gesture = calc_distance(hand)
            gesture_dist = gesture_identifier(known_gestures, unknown_gesture, KeyPoints, labels, tolerance=10)

            if gesture_dist == "Unknown":
                #SVM model prediction
                raw_features = np.array(hand).flatten()  
                scaled_features = scaler.transform([raw_features])
                svm_prediction = svm_model.predict(scaled_features)[0]
                final_gesture = "Unknown"  
            else:
                final_gesture = gesture_dist

            #Check if the gesture has changed
            if player_gesture != final_gesture:
                player_gesture = final_gesture
                computer_gesture = None  #Reset computer gesture

            #Generate computer's gesture if it's not set
            if computer_gesture is None:
                if player_gesture == "Unknown":
                    computer_gesture = "Unknown"
                else:
                    computer_gesture = random.choice(labels)

                #Sending the computer's gesture to the arduino to move the servos and display it
                control_servos(computer_gesture)

            #Determinig the result
            if player_gesture == "Unknown" or computer_gesture == "Unknown":
                result = "Unknown"
            elif player_gesture == computer_gesture:
                result = "It's a Tie"
            elif (player_gesture == "rock" and computer_gesture == "scissors") or \
                 (player_gesture == "scissors" and computer_gesture == "paper") or \
                 (player_gesture == "paper" and computer_gesture == "rock"):
                result = "Player: Won"
            else:
                result = "Player: Lost"

            #Controlling LEDs based on the result
            control_leds(result)

            cv2.putText(frame, f'Player Gesture: {player_gesture}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Computer Gesture: {computer_gesture}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, result, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Gesture Recognition", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('7'):      #Restart the game if 7 was pressed
        player_gesture = None 
        computer_gesture = None
        countdown_done = False  

    elif key == ord('q'):  
        break

cam.release()
cv2.destroyAllWindows()
