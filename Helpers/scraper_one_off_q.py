import Helpers.scraper_gemini_prices as sgp
import streamlit as st
import google.generativeai as genai
import sys
import google.generativeai.types as genai_errors

def gemini_chat(chat,prompt):
    try:
          response = chat.send_message(prompt)
          return response
    except genai_errors.StopCandidateException as e:
        print(e)
        st.error(f"""Gemini returned and error: {e}""")
        sys.exit()

def call_gemini_one_off(target_html):
    print("Calling Gemini")

    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    response = gemini_chat(chat,[st.session_state["one_off_prompt"],target_html])
    print(response.text)
    return response.text

def scraper_prices_one_off(url):
        # Fetch content from URL
        st.session_state['target_html'] = sgp.fetch_url_content(url)
        # Capture screenshot
        #st.session_state['target_screenshot'] = capture_screenshot(url)
        with st.expander("See payload"):
        #st.image(st.session_state['target_screenshot'])
            st.text(st.session_state['target_html'])

        with st.spinner("Calling Gemini"):
            response = call_gemini_one_off(st.session_state['target_html'])
            st.text(response)