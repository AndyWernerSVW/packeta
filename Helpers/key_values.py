import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def generate_data():

    # Number of companies
    n_companies = 100

    # Generate company names
    customers = ['Company_' + str(i) for i in range(1, n_companies + 1)]

    # Generate metrics following a Pareto distribution
    # We use the Pareto distribution as a proxy for the 80-20 rule
    # The scale (b) is arbitrarily chosen; you might need to adjust it based on your specific needs
    pareto_shape = 1.16  # This shape parameter gives a roughly 80-20 distribution
    pieces = np.random.pareto(a=pareto_shape, size=n_companies)*1_000_000 + 1  # adding 1 to shift from 0 to minimum 1
    aov = np.random.normal(loc=1500, scale=1000, size=n_companies)
    costperdelivery = np.random.normal(loc=20, scale=10, size=n_companies)
    absolute_profit =  np.random.pareto(a=pareto_shape, size=n_companies)*1_000_0000 + 1  # adding 1 to shift from 0 to minimum 1

    # Create the DataFrame
    df = pd.DataFrame({
        'Customer': customers,
        'Pieces': pieces,
        "AOV": aov,
        "Packeta Cost per delivery": costperdelivery,
        "Absolute profit": absolute_profit

    })

    return(df)

def minibar(df, highlight, metric, xlabel='Customer', ylabel='Metric', title='Metric Values by Customer'):
    # Sort the DataFrame by 'Metric' in descending order for better visualization
    df_sorted = df.sort_values(by=metric, ascending=False).reset_index(drop=True)

    # Setup figure and axes for Matplotlib
    fig, ax = plt.subplots(figsize=(2,1))

    # Plotting using axes
    bars = ax.bar(df_sorted['Customer'], df_sorted[metric], color='#f0f3f9')  # default color

    # Find the index of the highlighted customer in the sorted DataFrame
    try:
        highlight_index = df_sorted[df_sorted['Customer'] == highlight].index[0]
        bars[highlight_index].set_color('#88294e')  # Change color of the specific bar
    except IndexError:
        print(f"Warning: '{highlight}' not found in DataFrame.")

    # Ensure layout is clean and remove borders
    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Remove x-axis and y-axis completely
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    return fig

def one_row(company_name, metric,df,unit):
    metric_value =df.loc[df['Customer'] == company_name, metric].values[0]

    col1, col2 = st.columns(2,vertical_alignment = "center")
    with col1:
            st.metric(label = metric, value = f"{metric_value:,.0f} {unit}")
            st.markdown(""">Source: Strategy 1.0""")
    with col2:
            fig = minibar(df,company_name,metric )
            st.pyplot(fig,use_container_width=False)

def key_ratios():
    df = generate_data()
    company = "Company_20"
    one_row(company,"Pieces",df,"pcs")
    one_row(company,"AOV",df,"CZK")
    one_row(company,"Packeta Cost per delivery",df,"CZK")
    one_row(company,"Absolute profit",df,"CZK")
