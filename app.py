import numpy as np
import pickle
import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Tariff Recommender System", layout="wide")

# Hide the Streamlit main menu
st.set_option('showMenu', False)

# Apply custom CSS to set the background to white and hide the footer
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .viewerBadge_container__1QSob {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Important Functions ---
def load_url(url):
    r = requests.get(url)       # to access the animation link
    if r.status_code != 200:
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
        c1, c2 = st.columns((1, 2))
        with c1:
            st.title("Tariff Recommender")
            st.write("Let's find you the best tariff:")
            
            # -- Time to take user input --
            # Our model takes 7 parameters so we need 7 input fields
            n = st.number_input("Number of bedrooms", min_value=0, max_value=100)
            p = st.radio("Do you have a SMART meter?", ("No", "Yes"))
            ev_solar = st.radio("Do you have an electric vehicle or solar panel installed?", ("No", "Yes"))
            # Change this part to capture EV and Solar Panel selection
            if ev_solar == "Yes":
                ev_solar_options = st.multiselect("Select all that apply:", ["EV customer", "Solar panel customer", "Both - EV and Solar"])
                ev_customer = 1 if "EV customer" in ev_solar_options or "Both - EV and Solar" in ev_solar_options else 0
                solar_panel_customer = 1 if "Solar panel customer" in ev_solar_options or "Both - EV and Solar" in ev_solar_options else 0
            else:
                ev_customer = 0
                solar_panel_customer = 0
            k = st.radio("Do you have a strong preference for 100% green electricity?", ("No", "Yes"))
            temperature = st.number_input("What is your monthly consumption?", min_value=0, max_value=100)
            humidity = st.radio("Are you an existing BG customer?", ("No", "Yes"))
            # Additional question for existing BG customers
            if humidity == "Yes":
                bg_customer_reference = st.text_input("Please enter your BG account number:")
            
            ph_value_options = ["None","Homecare 100", "EV charging", "HAMZAH WILL BE GREAT ONE DAY"]
            ph_value = st.selectbox("What bundle offers would interest you?", ph_value_options)
            
            rainfall = st.radio("Would you like to save half-price every Sunday by join BG Peaksave Sunday?*", ("No", "Yes"))

            # --- Code for recommendation ---
            crop_output = ""
            
            # --- Creating a button ---
            if st.button("Find The Best Tariff"):
                # Map the radio button values back to numeric values (0 for No, 1 for Yes)
                p_numeric = 1 if p == "Yes" else 0
                k_numeric = 1 if k == "Yes" else 0
                r_numeric = 1 if r == "Yes" else 0
                humidity_numeric = 1 if humidity == "Yes" else 0
                rainfall_numeric = 1 if rainfall == "Yes" else 0

                # Include the BG customer reference in the input data if provided
                input_data = [n, p_numeric, k_numeric, temperature, humidity_numeric, rainfall_numeric]
                if humidity == "Yes":
                    input_data.append(bg_customer_reference)
                input_data.extend([ph_value, rainfall_numeric])
                
                crop_output = crs_output(input_data)
                st.success(crop_output)  # Executes after successful button press
        
        with c2:
            # Place both animations in a separate container to avoid duplication
            with st.container():
                st_lottie(farmer, height=650, width=1300, key="farmer")  # Adjust the width here

if __name__ == '__main__':
    main()
