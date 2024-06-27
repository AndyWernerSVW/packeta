import streamlit as st
import Helpers.scraper_gemini_prices as sgp
import Helpers.scraper_one_off_q as so

def scraper_main(section):
    if 'content' not in st.session_state:
        st.session_state['target_screenshot'] = ""
        st.session_state['target_html'] = ""
        st.session_state["Initial_prompt"] = ""
        st.session_state["match_cariers_prompt"] = ""
        st.session_state["match_delivery_types"] = ""
    tab1, tab2 = section.tabs(["Extract Prices", "Ask Gemini"])
    with tab1:
        with st.form('url_form'):
            url = st.text_input('Enter the URL', value = "https://bionebio.cz/doprava-zbozi")
            with st.expander("Prompts"):
                st.session_state["Initial_prompt"] = st.text_area("Initial Prompt", value = sgp.initial_prompt, height = 200)
                st.session_state["match_cariers_prompt"] = st.text_area("Match Carriers Prompt", value = sgp.match_cariers_prompt, height = 200)
                st.session_state["match_delivery_types"] = st.text_area("Match Delivery Types Prompt", value = sgp.match_delivery_types, height = 200)
                st.caption("""How this work: There are three calls to the Gemini. First one send the .html of the given site above together with initial prompt.
                        then there are follow up calls that allow you to work with the reply. Make sure you requset reply in this format, otherwise the prices chart will not render:{name,price,internal_carrier_name,internal_delivery_type}
                        Also you can get an error, then try to laod again """)
            
            submit_button_prices = st.form_submit_button('Extract Prices')

        if submit_button_prices and url:
            sgp.scraper_prices(url)

    with tab2:
        with st.form('ask_one_off'):
            url = st.text_input('Enter the URL', value = "https://bionebio.cz/doprava-zbozi")
            st.session_state["one_off_prompt"] = st.text_area("Initial Prompt", value = "Tell me about shipping options", height = 200)
            submit_button_one_off = st.form_submit_button('Query Gemini')
        
        if submit_button_one_off and url:
            so.scraper_prices_one_off(url)