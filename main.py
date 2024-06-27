import streamlit as st
import Helpers.margin_pool as mp
import Helpers.depot_utilisation as dp
import Helpers.key_values as kv
import Helpers.scraper_main as sm
import pandas as pd


st.title('Great customer A')
tab1, tab2 = st.tabs(["Scraper","Dashboard"])
with tab1:
    st.header('Delivery option Scraper and Analyzer')
    with st.expander("Worth trying"):
        st.code("""https://bionebio.cz/doprava-zbozi
    https://www.datart.cz/napoveda/vsechny-druhy-doprav
    https://gymbeam.cz/doruceni-platba
    https://www.mall.cz/zpusoby-doruceni
        """)

    section1 = st.empty()
    sm.scraper_main(section1)


with tab2:
    # Display Margin Pool chart
    st.subheader("Margin Pool")

    margin_pool_data  = pd.read_csv('SampleData/inputs.csv')

    st.pyplot(mp.margin_pool_chart(margin_pool_data))
    with st.expander("Notes"):
        st.markdown(mp.mp_notes)

    st.subheader("Depot Utilization")
    depot_names = [
        "Nučice u Rudné u Prahy", "Praha-Štěrboholy", "Nehvizdy u Prahy",
        "Holubice u Brna", "Ostrava", "Ústí nad Labem", "Břeclav",
        "Plzeň", "České Budějovice 'Minidepo'", "Hradec Králové", "Zlín",
        "Jihlava", "Olomouc", "Šumperk", "Liberec", "Karlovy Vary 'Minidepo'", "Svitavy"]
    depot_util = dp.plot_depot_utilization(depot_names)
    st.pyplot(depot_util)
    with st.expander("Notes"):
        st.markdown(dp.data_needed)

    st.subheader("Key Values and Benchmarking")
    kv.key_ratios()