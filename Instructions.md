# Rock Paper Scissors Gesture Recognition Game

These instructions will guide you on how to run this project, with or without Arduino integration.
For a detailed overview of the project structure, please refer to "[README.md](./README.md)" file.   

## How to Run

### I. Requirements
Ensure you have the following libraries installed: 
OpenCV, Numpy, Mediapipe, Pandas, scikit-learn, joblib, and serial. (required for Arduino usage)

### II. Data Collection
You can use the provided dataset, but it’s recommended to collect your own data for rock, paper, and scissors gestures by running the `data.py` script. 
If you do so, either remove the existing `gesture_data.csv` file or save your data with a different filename to avoid conflicts.

### III. Model creation 
Create the SVM model by running the `svm.py` script. This will generate the model and scaler files needed for the game.

### IV. Game flow
After completing the previous steps, you’re ready to play the game. If you’ve connected the servos and LEDs to an Arduino, run `FullGame.py` file.
If you’re not using Arduino, comment out or remove the following lines:

Line 11: arduino = serial.Serial(port='COM3', baudrate=115200),

Servo and LED control functions,

Line 173: control_servos(computer_gesture),

and Line 188: control_leds(result).

### V. Hybrid and Gesture Recognition testing
The `hybrid.py` file is for testing a hybrid approach that combines the SVM model with a distance-based method. The `gesture_recno.py`
file tests the distance-based method independently. You can run these files if you want to explore or test these methods.
