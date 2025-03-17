import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Step 1: Load the dataset
dataset_path = "assets/Data/Crop_recommendation.csv"  # Update with your dataset file path
df = pd.read_csv(dataset_path)

# Features and Target
X = df.iloc[:, :-1]  # All columns except the last one
y = df.iloc[:, -1]   # Last column (Crop Name)

# Encode Crop Names
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  # Convert crop names to numeric values

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train Decision Tree Model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Model Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save Model and Label Encoder
with open("models/classifier.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("models/label_encoder.pkl", "wb") as encoder_file:
    pickle.dump(label_encoder, encoder_file)

print("Model and Label Encoder saved successfully!")