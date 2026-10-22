
import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕")

st.title("☕ Starbucks Calorie Predictor")
st.write("Explore the calories in your favorite Starbucks drinks.")

# Load the Starbucks dataset
@st.cache_data
def load_data():
    df = pd.read_csv("starbucks.csv", encoding="latin1")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Check required columns
    if not {"Beverage", "Calories"}.issubset(df.columns):
        st.error("The dataset must contain Beverage and Calories columns.")
        st.stop()

    df["Calories"] = pd.to_numeric(df["Calories"], errors="coerce")
    df = df.dropna(subset=["Beverage", "Calories"])

    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("starbucks.csv was not found. Upload it to your GitHub repository.")
    st.stop()
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

# Let the user select a drink
drinks = sorted(df["Beverage"].astype(str).unique())
selected_drink = st.selectbox("Choose a Starbucks drink:", drinks)

drink_data = df[df["Beverage"].astype(str) == selected_drink]

# If the dataset includes preparation types, allow a selection
if "Beverage_prep" in df.columns:
    preparations = sorted(drink_data["Beverage_prep"].dropna().astype(str).unique())

    if preparations:
        selected_prep = st.selectbox("Choose preparation:", preparations)
        drink_data = drink_data[
            drink_data["Beverage_prep"].astype(str) == selected_prep
        ]

if not drink_data.empty:
    calories = drink_data["Calories"].iloc[0]
    st.metric("Calories", f"{calories:g} kcal")
    st.caption("Calories shown are from the dataset, not a new model prediction.")
