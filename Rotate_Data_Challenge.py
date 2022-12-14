import streamlit as st
from functions import *


def main():

    st.set_page_config(
        page_title="Rotate Data Challenge",
        page_icon="✈️",
    )

    st.title("Rotate Data Challenge")

    st.write("Input an origin and destination airport using the ICAO format. Then click 'Run' and the app will then give you the expected daily volume and weight of cargo that one can expect to transit, alongside the current average number of daily flights on this route.")

    st.markdown(
        """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

    with st.form("Main"):
        col1, col2 = st.columns(2)

        origin_input = col1.text_input(
            "Input origin airport here :", placeholder="eg. KMEM").upper()
        destination_input = col2.text_input(
            "Input destination airport here :", placeholder="eg. PHNL").upper()

        button = st.form_submit_button("Run")

        if button:
            result = route_daily_capacity(origin_input, destination_input)
            empty_col, col1_bis, col2_bis, col3_bis = st.columns([
                                                                 0.8, 2, 2, 2])

            col1_bis.metric("Daily Capacity Weight [kg]", np.round(
                result["Daily Capacity Weight [kg]"], 2))
            col2_bis.metric("Daily Capacity Volume [m3]", np.round(
                result["Daily Capacity Volume [m3]"], 2))
            col3_bis.metric("Daily Flights [-]",
                            np.round(result["Daily Flights"], 2))

    # st.dataframe(gather_flight_data())


if __name__ == "__main__":
    main()
