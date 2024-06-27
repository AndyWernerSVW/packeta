from Helpers.sel_screenshot import capture_screenshot
import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd
import json
import html
from PIL import Image
import Helpers.pricing_bar_chart as pbc
import google.generativeai.types as genai_errors
import sys



genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


def to_df(response):
    decoded_string = html.unescape(response)
    json_data = json.loads(decoded_string)
    try:
        df = pd.DataFrame(json_data)
    except: AttributeError

        
    return df



def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return str(e)
def gemini_chat(chat,prompt):
    try:
          response = chat.send_message(prompt)
          return response
    except genai_errors.StopCandidateException as e:
        print(e)
        st.error(f"""Gemini returned and error: {e}""")
        sys.exit()
        

def call_gemini(target_html):
    print("Calling Gemini")

    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    response = gemini_chat(chat,[st.session_state["Initial_prompt"],target_html])
    print(response.text)
    response = gemini_chat(chat,match_cariers_prompt)
    print(response.text)
    response = gemini_chat(chat,match_delivery_types)
    print(response.text)
    #json_data = """[{"name": "Doprava u partnerského prodeje", "price": "Způsob a cena doručení závisí na partnerovi Při rozdělení objednávky do více zásilek, platíte jen za jedno doručení", "internal_category": "missing"}, {"name": "Osobní odběr na pobočkách WE|DO Point", "price": "Zdarma se / 59 Kč", "internal_category": "A"}, {"name": "Osobní odběr WE|DO OX Box", "price": "Zdarma se / 49 Kč", "internal_category": "B"}, {"name": "Osobní odběr WE|DO AlzaBox", "price": "Zdarma se / 49 Kč", "internal_category": "B"}, {"name": "Osobní odběr na pobočkách Zásilkovny", "price": "Zdarma se / 59 Kč", "internal_category": "A"}, {"name": "Balík na poštu", "price": "Zdarma se / 79 Kč", "internal_category": "E"}, {"name": "Doručení ve vámi vybraný den", "price": "od 99 Kč", "internal_category": "missing"}, {"name": "Doručení o víkendu", "price": "od 189 Kč", "internal_category": "missing"}, {"name": "Doručení v den objednání", "price": "od 159 Kč", "internal_category": "missing"}, {"name": "Doručení ve vámi určený čas", "price": "40 Kč", "internal_category": "missing"}, {"name": "MALL Comfort - Komplet", "price": "349 Kč", "internal_category": "missing"}, {"name": "MALL Comfort - Výnos do patra", "price": "249 Kč", "internal_category": "missing"}, {"name": "MALL Comfort - Odvoz starého spotřebiče", "price": "Zdarma", "internal_category": "missing"}, {"name": "Odborná instalace spotřebiče", "price": "1 599 Kč", "internal_category": "missing"}, {"name": "Instalace dvou spotřebičů s mezikusem(jen se službou Komplet)", "price": "199 Kč", "internal_category": "missing"}, {"name": "Můžu sledovat stav mojí objednávky?", "price": null, "internal_category": "missing"}, {"name": "Problémy s doručováním", "price": null, "internal_category": "missing"}]"""
    prices_df = to_df(response.text)
    return prices_df

initial_prompt = """I am sending you a page from an czech e-shop, that informs customer about delivery options.
    I will load data into Python Dataframe: so I need a list like this.[{name,price},{name,price}].
    Give me only the list, do not write anything else, otherwise my script will fail and I will lose my job.
    The price is number only. Do not add "Kč" or "CZK"
    Also remove all control characters (for example new lines) that would prevent loading the data into DataFrame
    Use double quotes to enclose property name and value
    """

match_cariers_prompt = """ Now match the delivery types to one of these internal carrier names:
        "Zásilkovna"                           
        "DPD"
        "PPL"
        "Česká pošta" - Also known as Balíkovna, or Balík do ruky.
        "WE|DO"
        "Other"
    If you cannot find proper match for given internal carrier names, do not add guess. Say "missing"
    So now, the JSON would look like this: {name,price,internal_carrier_name,}
    Use double quotes to enclose property name and value
    """
match_delivery_types = """Now match the delivery types to these internal categories:
"Home" - delivered to an address
"Box" - delivered to parcel box
"Pickup point" - delivered to a pickup point
"Not delivery" - other service that is not delivery.
If you cannot find proper match for given internal carrier names, do not add guess. Say "missing"
So now, the JSON would look like this: {name,price,internal_carrier_name,internal_delivery_type}
Use double quotes to enclose property name and value
"""

def scraper_prices(url):
            # Fetch content from URL
        st.session_state['target_html'] = fetch_url_content(url)
        # Capture screenshot
        #st.session_state['target_screenshot'] = capture_screenshot(url)
        with st.expander("See content"):
        #st.image(st.session_state['target_screenshot'])
            st.text(st.session_state['target_html'])

        with st.spinner("Calling Gemini"):
            prices_df = call_gemini(st.session_state['target_html'])
            #data = """[{"name": "PPL", "price": 114, "internal_carrier_name": "PPL", "internal_delivery_type": "Home"}, {"name": "DPD", "price": 120, "internal_carrier_name": "DPD", "internal_delivery_type": "Home"}, {"name": "Zásilkovna do 5 kg", "price": 59, "internal_carrier_name": "Zásilkovna", "internal_delivery_type": "Pickup point"}, {"name": "Zásilkovna nad 5 kg", "price": 79, "internal_carrier_name": "Zásilkovna", "internal_delivery_type": "Pickup point"}, {"name": "Balíkovna", "price": 45, "internal_carrier_name": "missing", "internal_delivery_type": "missing"}, {"name": "Balík do ruky", "price": 79, "internal_carrier_name": "missing", "internal_delivery_type": "Home"}] """
            #prices_df = to_df(data)
            st.subheader('Overview of Services and Prices')
            st.pyplot(pbc.pricing_bar(prices_df))
            st.table(prices_df)