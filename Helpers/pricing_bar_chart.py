def pricing_bar(df):

    import matplotlib.pyplot as plt
    import pandas as pd



    # Color mapping for carriers
    color_dict = {
        'PPL': '#f0f3f9',  # Light Grey
        'DPD': '#dcc1cd',  # Very Light Pink
        'Zásilkovna': '#88294e',  # Dark Maroon
        'Česká pošta': '#000000'  # Black
    }
    default_color = '#808080'  # Grey

    # Assign colors to services based on the carrier
    df['Color'] = df['internal_carrier_name'].apply(lambda x: color_dict.get(x, default_color))

    # Sort the DataFrame based on 'Delivery Type' and then 'Price'
    df_sorted = df.sort_values(by=['internal_delivery_type', 'price'], ascending=[True, False])

    print(df)

    # Create a figure and an axes object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data using the axes object
    bars = []  # to keep track of bar objects for the legend
    for i, row in df_sorted.iterrows():
        bar = ax.bar(row['name'], row['price'], color=row['Color'])
        ax.text(row['name'], row['price'], f'{row["price"]}', ha='center', va='bottom')
        bars.append(bar)

    # Set labels and title using the axes object
    ax.set_ylabel('Price (CZK)')
    ax.set_xticklabels(df_sorted['name'], rotation=45, ha="right")



    # Adjust layout to ensure everything fits without clipping
    plt.tight_layout()

    # Remove borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add legend to the right of the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Show the plot
    return plt
