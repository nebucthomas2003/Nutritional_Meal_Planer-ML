from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the datasets
dataset_paths = {
    "Underweight": "underweight_meal_plan.csv",
    "Normal weight": "normal_weight_meal_plan.csv",
    "Overweight": "overweight_meal_plan.csv",
    "Obese": "obese_meal_plan.csv"
}

# Function to calculate BMI
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    return bmi

# Function to determine BMI category
def categorize_bmi(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 25:
        return "Normal weight"
    elif 25 <= bmi_value < 30:
        return "Overweight"
    else:
        return "Obese"

# Route to handle weight and height input and display meal plan
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        weight_input = request.form["weight"]
        height_input = request.form["height"]

        # Check if weight and height inputs are numeric and non-zero
        try:
            weight = float(weight_input)
            height_cm = float(height_input)
            if weight <= 0 or height_cm <= 0:
                raise ValueError
        except ValueError:
            return render_template("invalid_input.html")

        bmi = calculate_bmi(weight, height_cm)
        bmi_category = categorize_bmi(bmi)

        # Load the appropriate dataset based on BMI category
        meal_plan_data = pd.read_csv(dataset_paths[bmi_category])

        # Extract the meal plan
        meal_plan = meal_plan_data["Meal Plan"].values[0]

        return render_template("result.html", weight=weight, height_cm=height_cm, bmi=bmi,
                               bmi_category=bmi_category, meal_plan=meal_plan)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)