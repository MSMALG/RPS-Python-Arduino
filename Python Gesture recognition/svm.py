#SVM model

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE



data = pd.read_csv('gesture_data.csv')

#Separating features and labels
feat_X = data.iloc[:, :-1].values  #All columns except the last one
feat_y = data.iloc[:, -1].values   #The last column is the label

#Encode the labels as integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(feat_y)


#Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(feat_X, y_encoded, test_size=0.2, random_state=42)

#Scaling the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#Training the SVM model
svm_model = SVC(kernel='rbf')

#Performing cross-validation
score = cross_val_score(svm_model, feat_X, y_encoded, cv=10)
print("Cross-validation scores:", score)

#Fit the model
svm_model.fit(X_train_scaled, y_train)

#Saving the model and scaler
joblib.dump(svm_model, 'svm_gesture_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
