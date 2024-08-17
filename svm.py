import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE


# Load the data
data = pd.read_csv('gesture_data.csv')

# Separate features and labels
feat_X = data.iloc[:, :-1].values  # All columns except the last one
feat_y = data.iloc[:, -1].values   # The last column is the label

# Encode the labels as integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(feat_y)

# Create a mapping dictionary (gesture_mapping) for later use
gesture_mapping = {index: label for index, label in enumerate(label_encoder.classes_)}

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(feat_X, y_encoded, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the SVM model
svm_model = SVC(kernel='rbf')

# Perform cross-validation
score = cross_val_score(svm_model, feat_X, y_encoded, cv=10)
print("Cross-validation scores:", score)

# Dimensionality reduction for visualization
tsne = TSNE()
X_embed = tsne.fit_transform(feat_X)

# Use the integer labels for hue in the scatterplot
markers = [gesture_mapping[label_encoder.transform([label])[0]] for label in feat_y]

# Plot the t-SNE embedding
sns.set(rc={'figure.figsize': (10, 8)})
palette = sns.color_palette('bright', len(gesture_mapping))  # Ensure palette length matches the number of unique labels
sns.scatterplot(x=X_embed[:, 0], y=X_embed[:, 1], hue=markers, legend="full", palette=palette)
plt.show()

# Fit the model
svm_model.fit(X_train_scaled, y_train)

# Save the model and scaler
joblib.dump(svm_model, 'svm_gesture_model.pkl')
joblib.dump(scaler, 'scaler.pkl')




