import streamlit as st
from functions import *


def main():

    st.set_page_config(
        page_title="Rotate Data Challenge",
        page_icon="✈️",
    )

    st.title("Rotate Data Challenge")

    st.markdown(
        """<style> div.stButton > button:first-child { width: 100% ; } </style>""", unsafe_allow_html=True)

    with st.form("Main"):
        col1, col2 = st.columns(2)

        origin_input = col1.text_input(
            "Input origin here :", placeholder="eg. KMEM").upper()
        destination_input = col2.text_input(
            "Input destination here :", placeholder="eg. PHNL").upper()

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


if __name__ == "__main__":
    main()
