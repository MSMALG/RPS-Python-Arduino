# Hand Gesture Recognition 

This project implements a hand gesture recognition system using the MediaPipe library, distance-based gesture recognition, and an SVM model. The system recognizes gestures such as Rock, Paper, and Scissors, and can be integrated with a robotic hand via Arduino to play a Rock-Paper-Scissors game. 
For instruction on how to run this project please reference [Instructions.md](./Instructions.md)

## Project Structure

### 1. HandLandMarks.py
This file defines a class for detecting hand landmarks using the MediaPipe library.

- **Class: `mpHands`**
  - **`__init__`**: Initializes the hand detection model with configurable parameters.
  - **`Lmarks`**: Processes a video frame and returns detected hand landmarks.

### 2. Data Collection
This script collects gesture data using a webcam and saves it to a CSV file for training models.

- **File: `data.py`**
  - Captures hand landmarks and saves them with associated labels (Rock, Paper, Scissors) to `gesture_data.csv`.

### 3. Gesture Recognition (Distance-Based Method)
This script uses a distance matrix approach to recognize hand gestures based on known patterns.

- **File: `gesture_reco.py`**
  - Recognizes gestures by comparing the distance matrix of detected landmarks against pre-stored gestures.

### 4. SVM Model Training
This script trains an SVM model for gesture recognition using the collected data.

- **File: `svm.py`**
  - Trains an SVM model using the collected gesture data and saves the trained model and scaler for future use.

### 5. Gesture Recognition (Hybrid System)
This script combines both distance-based and SVM-based methods to improve gesture recognition accuracy.

- **File: `hybrid.py`**
  - First attempts to recognize gestures using the distance-based method. If unsuccessful, it uses the SVM model.

### 6. Rock-Paper-Scissors Game with Arduino Integration
This script integrates gesture recognition with Arduino to control a robotic hand and play Rock-Paper-Scissors.

- **File: `FullGame.py`**
  - Recognizes gestures in real-time, communicates with Arduino via serial port to control the robotic hand, and determines game outcomes using LEDs.

### 7. Arduino Implementation
This script controls five servos representing the fingers of a robotic hand, executing Rock, Paper, and Scissors gestures based on commands received over the serial port.

- **File: `hand.py`**
  - The Rock, Paper, and Scissors functions control the movement of the servos to perform each gesture.
  - LEDs indicate whether the player won, lost, or if the game resulted in a tie.
  - The system prevents executing the same command repeatedly, ensuring smoother gameplay.
