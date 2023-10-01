import numpy as np
import pandas as pd
import pickle
import streamlit as st
import json
import math
import base64

result = None
try :
    with open("ban_house.pickle", 'rb') as f:
        __model = pickle.load(f)

except Exception as e:
    st.error("Error loading the model. Please check if the model file 'ban_house.pickle' is available.")
    st.stop()  # Stop the app if model loading fails


with open("data_columns.json", 'r') as obj:
    __data_columns = json.load(obj)["data_columns"]
    #__area_types = __data_columns[4:8]
    __locations = __data_columns[3:]


def get_predicted_price(location, sqft, bathroom, BHK):
    try:
        #area_index = __data_columns.index(area_type.lower())
        loc_index = __data_columns.index(location.lower())
    except ValueError as e:
        area_index = -1
        loc_index = -1

    lis = np.zeros(len(__data_columns))
    lis[0] = sqft
    lis[1] = bathroom
    lis[2] = BHK

    if loc_index >= 0:
        #lis[area_index] = 1
        lis[loc_index] = 1

    price = round(__model.predict([lis])[0], 2)
    strp = ' lakhs'

    if math.log10(price) >= 2:
        price = price / 100
        price = round(price, 2)
        strp = " crores"

    return str(price) + strp


def main():
    global result
    st.title("Bangalore House Price Predictor")


    #st.markdown(html_temp, unsafe_allow_html=True)
    total_sqft = st.text_input("Total_sqft")
    #balcony = st.text_input("Number of Balconies")
    bathroom = st.text_input("Number of Bathrooms")
    BHK = st.text_input("BHK")
    #area_type = st.selectbox("Area Type", __area_types)
    location = st.selectbox("Location", __locations)

    if st.button("Predict"):
        result = get_predicted_price(location, total_sqft, bathroom, BHK)

    st.success(f"Price = {result}")


if __name__ == "__main__":
    main()

