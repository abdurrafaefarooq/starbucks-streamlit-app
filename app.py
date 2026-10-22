
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Starbucks Calories Predictor",
    page_icon="☕"
)

st.title("☕ Starbucks Calories Explorer")
st.write(
    "Select a Starbucks drink to view its calories "
    "and nutritional information."
)

# Load the dataset
DATA_PATH = Path(__file__).parent / "starbucks.csv"

try:
    df = pd.read_csv(DATA_PATH)
except Exception as error:
    st.error("Could not load starbucks.csv.")
    st.write(str(error))
    st.stop()

# Clean column names and calorie values
df.columns = df.columns.str.strip()

if "Beverage" not in df.columns or "Calories" not in df.columns:
    st.error("The dataset must contain Beverage and Calories columns.")
    st.stop()

df["Calories"] = pd.to_numeric(df["Calories"], errors="coerce")
df = df.dropna(subset=["Beverage", "Calories"]).copy()

# Make each drink preparation selectable
if "Beverage_prep" in df.columns:
    df["Drink_Option"] = (
        df["Beverage"].astype(str)
        + " — "
        + df["Beverage_prep"].fillna("Standard").astype(str)
    )
else:
    df["Drink_Option"] = df["Beverage"].astype(str)

drink_options = sorted(df["Drink_Option"].unique())

selected_drink = st.selectbox(
    "Choose a Starbucks drink",
    drink_options
)

# Get the selected drink's dataset row
drink_data = df[df["Drink_Option"] == selected_drink]

# If there are multiple matching rows, show the first one
drink = drink_data.iloc[0]

st.subheader("Nutrition Information")

st.metric(
    label="Calories",
    value=f"{drink['Calories']:g} kcal"
)

if "Beverage_category" in df.columns:
    st.write("**Beverage Category:**", drink["Beverage_category"])

st.write("**Selected Drink:**", selected_drink)

nutrition_columns = [
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

available_columns = [
    col for col in nutrition_columns if col in df.columns
]

if available_columns:
    st.subheader("Other Nutrition Details")

    nutrition_data = pd.DataFrame({
        "Nutrient": available_columns,
        "Value": [drink[col] for col in available_columns]
    })

    st.dataframe(nutrition_data, hide_index=True)

st.caption(
    "Values are taken from the uploaded Starbucks dataset "
    "and may vary by drink preparation or serving size."
)
