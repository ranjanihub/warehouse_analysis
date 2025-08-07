import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('fulfillment_model.pkl')

# Streamlit App Title
st.title("Fulfillment Rate Predictor")

# User Input Fields
st.header("Enter Product & Inventory Details:")

units_sold = st.number_input("Units Sold", min_value=0)
demand_forecast = st.number_input("Demand Forecast", min_value=0)
inventory_level = st.number_input("Inventory Level", min_value=0)
unit_price = st.number_input("Unit Price", min_value=0.0)
promotion_flag = st.selectbox("Promotion Active?", ['No', 'Yes'])
warehouse_id = st.selectbox("Warehouse", ['wh_1', 'wh_2', 'wh_3', 'wh_4', 'wh_5'])
region = st.selectbox("Region", ['north', 'south', 'east', 'west'])
perishable_flag = st.selectbox("Perishable Item?", ['No', 'Yes'])

# Encode inputs
data = pd.DataFrame({
    'Units_Sold': [units_sold],
    'Demand_Forecast': [demand_forecast],
    'Inventory_Level': [inventory_level],
    'Promotion_Flag': [1 if promotion_flag == 'Yes' else 0],
    'Perishable_Flag': [1 if perishable_flag == 'Yes' else 0],
    'Unit_Price': [unit_price],
    'Warehouse_ID_wh_2': [1 if warehouse_id == 'wh_2' else 0],
    'Warehouse_ID_wh_3': [1 if warehouse_id == 'wh_3' else 0],
    'Warehouse_ID_wh_4': [1 if warehouse_id == 'wh_4' else 0],
    'Warehouse_ID_wh_5': [1 if warehouse_id == 'wh_5' else 0],
    'Region_east': [1 if region == 'east' else 0],
    'Region_north': [1 if region == 'north' else 0],
    'Region_south': [1 if region == 'south' else 0],
    'Region_west': [1 if region == 'west' else 0]
})

# Fill any missing one-hot columns with 0
all_columns = model.feature_names_in_
for col in all_columns:
    if col not in data.columns:
        data[col] = 0
data = data[all_columns]

# Predict
if st.button("Predict Fulfillment Rate"):
    prediction = model.predict(data)[0]
    st.success(f"Predicted Fulfillment Rate: {prediction:.2%}")

    if prediction < 0.9:
        st.warning("At risk of under-fulfillment. Consider restocking.")
    else:
        st.info("Fulfillment rate looks good.")
