import numpy as np
import pickle
import streamlit as st
import requests
from streamlit_lottie import st_lottie


st.set_page_config(page_title="Crop Recommender System", layout="wide")

# --- Important Functions ---
def load_url(url):
    r = requests.get(url)       # to access the animation link
    if r.status_code !=200:
        return None
    return r.json()

# Animation Assests
plant = load_url("https://lottie.host/317802e0-e0a9-4715-9eaf-6ef6511ea52d/vvXUHRFJ2L.json")
farmer = load_url("https://lottie.host/317802e0-e0a9-4715-9eaf-6ef6511ea52d/vvXUHRFJ2L.json")


# --- Load The Model ---
recommender = pickle.load(open('CropRecommender.sav', 'rb'))

# --- Function that performs prediction ---

def crs_output(input_data):
    input_array = np.array(input_data)
    final_input = input_array.reshape(1, -1)
    prediction = recommender.predict(final_input)
    output = prediction[0]
    return f'Field conditions are most suitable for {output}'

def main():
    with st.container():
        c1, c2 = st.columns((2, 1))
        with c1:
            st.title("Tariff Recommender")
            st.write("Let's find you the best tariff:")
            
            # -- Time to take user input --
            # Our model takes 7 parameters so we need 7 input fields

            n = st.number_input("Number of bedrooms", min_value=0, max_value=100)
            p = st.radio("Do you have a SMART meter?", ("No", "Yes"))
            k = st.radio("Do you have a strong preference for 100% green electricity?", ("No", "Yes"))
            temperature = st.number_input("What is your monthly consumption?", min_value=0, max_value=100)
            humidity = st.radio("Are you an existing BG customer?", ("No", "Yes"))
            
            # Additional question for existing BG customers
            if humidity == "Yes":
                bg_customer_reference = st.text_input("Please enter your BG customer reference:")
            
            ph_value = st.number_input("What bundle offers would interest you?", min_value=0, max_value=15)
            rainfall = st.radio("Would you want to join BG Peaksave Sunday?", ("No", "Yes"))

            # --- Code for recommendation ---
            crop_output = ""
            # --- Creating a button ---
            if st.button("Find The Best Tariff"):
                # Map the radio button values back to numeric values (0 for No, 1 for Yes)
                p_numeric = 1 if p == "Yes" else 0
                k_numeric = 1 if k == "Yes" else 0
                humidity_numeric = 1 if humidity == "Yes" else 0
                rainfall_numeric = 1 if rainfall == "Yes" else 0

                # Include the BG customer reference in the input data if provided
                input_data = [n, p_numeric, k_numeric, temperature, humidity_numeric, ph_value, rainfall_numeric]
                if humidity == "Yes":
                    input_data.append(bg_customer_reference)

                crop_output = crs_output(input_data)
                st.success(crop_output)  # Executes after successful button press
        
        with c2:
            st_lottie(farmer, height=650, width=1300, key="farmer")  # Adjust the width here
            st_lottie(plant, height=800, key="plant")

# if __name__ == '__main__':
main()
