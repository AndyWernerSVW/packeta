from Helpers.sel_screenshot import capture_screenshot
import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd
import json
import html
from PIL import Image
import Helpers.pricing_bar_chart as pbc


genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


def to_df(response):
    decoded_string = html.unescape(response)
    json_data = json.loads(decoded_string)
    df = pd.DataFrame(json_data)
    return df



def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return str(e)

def call_gemini(target_html):
    print("Calling Gemini")

    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    response = chat.send_message([st.session_state["Initial_prompt"],target_html] )
    print(response.text)
    st.session_state['Gemini Status'] = "Asking Question 2"
    response = chat.send_message(match_cariers_prompt)
    print(response.text)
    response = chat.send_message(match_delivery_types)
    #json_data = """[{"name": "Doprava u partnerského prodeje", "price": "Způsob a cena doručení závisí na partnerovi Při rozdělení objednávky do více zásilek, platíte jen za jedno doručení", "internal_category": "missing"}, {"name": "Osobní odběr na pobočkách WE|DO Point", "price": "Zdarma se / 59 Kč", "internal_category": "A"}, {"name": "Osobní odběr WE|DO OX Box", "price": "Zdarma se / 49 Kč", "internal_category": "B"}, {"name": "Osobní odběr WE|DO AlzaBox", "price": "Zdarma se / 49 Kč", "internal_category": "B"}, {"name": "Osobní odběr na pobočkách Zásilkovny", "price": "Zdarma se / 59 Kč", "internal_category": "A"}, {"name": "Balík na poštu", "price": "Zdarma se / 79 Kč", "internal_category": "E"}, {"name": "Doručení ve vámi vybraný den", "price": "od 99 Kč", "internal_category": "missing"}, {"name": "Doručení o víkendu", "price": "od 189 Kč", "internal_category": "missing"}, {"name": "Doručení v den objednání", "price": "od 159 Kč", "internal_category": "missing"}, {"name": "Doručení ve vámi určený čas", "price": "40 Kč", "internal_category": "missing"}, {"name": "MALL Comfort - Komplet", "price": "349 Kč", "internal_category": "missing"}, {"name": "MALL Comfort - Výnos do patra", "price": "249 Kč", "internal_category": "missing"}, {"name": "MALL Comfort - Odvoz starého spotřebiče", "price": "Zdarma", "internal_category": "missing"}, {"name": "Odborná instalace spotřebiče", "price": "1 599 Kč", "internal_category": "missing"}, {"name": "Instalace dvou spotřebičů s mezikusem(jen se službou Komplet)", "price": "199 Kč", "internal_category": "missing"}, {"name": "Můžu sledovat stav mojí objednávky?", "price": null, "internal_category": "missing"}, {"name": "Problémy s doručováním", "price": null, "internal_category": "missing"}]"""
    prices_df = to_df(response.text)
    return prices_df

initial_prompt = """I am sending you a page from an czech e-shop, that informs customer about delivery options.
    I will load data into Python Dataframe: so I need a list like this.[{name,price},{name,price}].
    Give me only the list, do not write anything else, otherwise my script will fail and I will lose my job.
    The price is number only. Do not add "Kč" or "CZK"
    Also remove all control characters (for example new lines) that would prevent loading the data into DataFrame
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
    """
match_delivery_types = """Now match the delivery types to these internal categories:
"Home" - delivered to an address
"Box" - delivered to parcel box
"Pickup point" - delivered to a pickup point
"Not delivery" - other service that is not delivery.
If you cannot find proper match for given internal carrier names, do not add guess. Say "missing"
So now, the JSON would look like this: {name,price,internal_carrier_name,internal_delivery_type}
"""

def scraper():
    with st.expander("Worth trying"):
        st.code("""https://bionebio.cz/doprava-zbozi
    https://www.datart.cz/napoveda/vsechny-druhy-doprav
    https://gymbeam.cz/doruceni-platba
    https://www.mall.cz/zpusoby-doruceni
        """)
    if 'content' not in st.session_state:
            st.session_state['target_screenshot'] = ""
            st.session_state['target_html'] = ""
            st.session_state["Initial_prompt"] = ""
            st.session_state["match_cariers_prompt"] = ""
            st.session_state["match_delivery_types"] = ""


    with st.form('url_form'):
        url = st.text_input('Enter the URL', value = "https://bionebio.cz/doprava-zbozi")
        with st.expander("Prompts"):
            st.session_state["Initial_prompt"] = st.text_area("Initial Prompt", value = initial_prompt, height = 200)
            st.session_state["match_cariers_prompt"] = st.text_area("Match Carriers Prompt", value = match_cariers_prompt, height = 200)
            st.session_state["match_delivery_types"] = st.text_area("Match Delivery Types Prompt", value = match_delivery_types, height = 200)
            st.caption("""How this work: There are three calls to the Gemini. First one send the .html of the given site above together with initial prompt.
                       then there are follow up calls that allow you to work with the reply. Make sure you requset reply in this format, otherwise the prices chart will not render:{name,price,internal_carrier_name,internal_delivery_type}
                       Also you can get an error, then try to laod again """)
        
        submit_button = st.form_submit_button('Fetch and Analyze')

    if submit_button and url:
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
            st.header('Overview of Services and Prices')
            st.pyplot(pbc.pricing_bar(prices_df))
            st.table(prices_df)