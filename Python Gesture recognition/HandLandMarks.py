#Class file that detects the hand landmarks using the MediaPipe library.

import cv2
import numpy as np 

class mpHands:
    import mediapipe as mp 
    def __init__(self, max_num_hands = 2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_hands = self.mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, 
                                         min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    def Lmarks(self, frame):
        myHands = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results =  self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for HandLandMarks in results.multi_hand_landmarks:
                myHand = []
                for landmark in HandLandMarks.landmark:
                    myHand.append((int(landmark.x * width), int(landmark.y * height)))
                myHands.append(myHand)
        return myHands
    
width = 1280
height = 720
