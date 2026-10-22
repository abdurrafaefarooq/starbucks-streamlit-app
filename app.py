
import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="Starbucks Drink Predictor",
    page_icon="☕",
    layout="centered"
)

st.title("☕ Starbucks Calories Predictor")

st.write(
    "Enter the calories and nutrition details "
    "of a Starbucks drink to predict its beverage category."
)

# Load the trained model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "starbucks_decision_tree.pkl"
)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(
        "Model could not be loaded. "
        "Please check that the PKL file is in the repository."
    )
    st.stop()

# Input features — keep the same order as training
features = [
    "Calories",
    "Total Fat (g)",
    "Trans Fat (g)",
    "Saturated Fat (g)",
    "Sodium (mg)",
    "Total Carbohydrates (g)",
    "Cholesterol (mg)",
    "Dietary Fibre (g)",
    "Sugars (g)",
    "Protein (g)",
    "Vitamin A (% DV)",
    "Vitamin C (% DV)",
    "Calcium (% DV)",
    "Iron (% DV)",
    "Caffeine (mg)"
]

st.subheader("Enter Drink Nutrition")

with st.form("drink_form"):
    values = {}

    for feature in features:
        values[feature] = st.number_input(
            feature,
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    submitted = st.form_submit_button("Predict Category")

if submitted:
    input_data = pd.DataFrame(
        [[values[f] for f in features]],
        columns=features
    )

    prediction = model.predict(input_data)

    st.success("Prediction completed!")
    st.subheader("Predicted Beverage Category")
    st.write(str(prediction[0]))
