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
recommender = pickle.load(open('CropRecommender.sav','rb'))

# --- Function that performs prediction ---

def crs_output(input_data):
    input_array = np.array(input_data)
    final_input = input_array.reshape(1,-1)
    prediction = recommender.predict(final_input)
    output = prediction[0]
    return (f'Field conditions are most suitable for {output}')


def main():

    with st.container():
        c1, c2 = st.columns((1,1.5))
        with c1:
            st.title("Tariff Recommender")
            st.write('Let's find you the best tariff: 



        with c2:
            st_lottie(farmer, height = 650, key="farmer")


    with st.container():
        col1, col2 = st.columns((1,1))
        with col1:
            
            st.header("Have Fun :smile:")
            #-- Time to take user input --
            # our model takes 7 parameters so we need 7 input fields

            n = st.number_input("Number of bedrooms", min_value=0.0, max_value=100.0)
            p = st.number_input("Do you have a SMART meter?", min_value= 0.0, max_value= 100.0)
            k =st.number_input("Do you have a strong preference for 100% green electricity?", min_value=0.0, max_value=100.0)
            temperature =st.number_input("What is your monthly consumption?", min_value=0.0, max_value=100.0)
            humidity =st.number_input("Are you an exisiting BG customer?", min_value=0.0, max_value=100.0)
            ph_value =st.number_input("What bundle offers would interest you?", min_value=0.0, max_value=15.0)
            rainfall =st.number_input("Would you want to join BG Peaksave Sunday",  min_value=0.0)

            # --- Code for reommendation ---
            crop_output = ""
            # --- creating a button ---
            if st.button("Find The Best Tariff"):
                crop_output = crs_output([n, p, k, temperature, humidity, ph_value, rainfall])
                with col2:
                    st_lottie(plant, height = 800, key="plant")
    
                st.success(crop_output) # executes after successful button press 


    



#if __name__ == '__main__':
main()
