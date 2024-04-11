import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("Dataset.csv")

# Function to preprocess data and train model
def train_model(data):
    label_encoder = LabelEncoder()
    data['BMI Range'] = label_encoder.fit_transform(data['BMI Range'])

    X = data.drop("Meal Plan", axis=1)
    y = data["Meal Plan"]
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

model = train_model(data)

# Function to predict meal plan based on BMI value
def predict_meal_plan(bmi_value):
    bmi_range = [[bmi_value]]
    predicted_meal_plan = model.predict(bmi_range)
    return predicted_meal_plan[0]
