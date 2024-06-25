import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import textwrap
from matplotlib.ticker import FixedLocator


def margin_pool_chart(margin_pool_data):


    required_columns = ['Category', 'E-shop margin', 'Alternative Take', 'Packeta profit', 'Packeta costs']
    for column in required_columns:   
        categories = margin_pool_data['Category']
        e_shop_margin = margin_pool_data['E-shop margin']
        alternative_take = margin_pool_data['Alternative Take']
        packeta_profit = margin_pool_data['Packeta profit']
        packeta_costs = margin_pool_data['Packeta costs']
        units_sold = (margin_pool_data['Units Sold'])


    total_width = sum(units_sold)
    normalized_widths = np.array([unit / total_width for unit in units_sold])

    # Calculate cumulative sums of the widths
    cumulative_widths = np.cumsum(normalized_widths)

    # Calculate starting positions of each bar by shifting the cumulative sums
    # The starting position of the first bar is 0
    width_positions = np.concatenate(([0], cumulative_widths[:-1]))
    mid_points = width_positions + normalized_widths

    # Color dictionary for each label
    color_dict = {
        'Packeta costs': '#f0f3f9',  # Light Grey: (240, 243, 249)
        'Packeta profit': '#dcc1cd',  # Very Light pink ()
        'E-shop margin': '#88294e',  # Dark Maroon: (136, 41, 78)
        'Alternative Take': '#000000'  # Black: (0, 0, 0)
    }

    # Wrap the labels
    wrapped_categories = [textwrap.fill(label, 10) for label in categories]


    # Use Roboto font
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # Create figure and axis
    fig, ax = plt.subplots(figsize = (12,6))

    # Create stacked bar chart with different widths
    for i in range(len(categories)):
        bottom = 0
        for value, label in zip(
            [ packeta_profit[i],packeta_costs[i], alternative_take[i], e_shop_margin[i]],
            ['Packeta profit','Packeta costs', 'Alternative Take','E-shop margin']
        ):
            ax.bar(cumulative_widths[i], value, width=normalized_widths[i], bottom=bottom, color=color_dict[label], label=label if i == 0 else "",align = 'center')
            bottom += value


   
    # Set the x-tick locations and labels
    ax.set_xticks(cumulative_widths)
    #ax.xaxis.set_major_locator(FixedLocator(width_positions))
    ax.set_xticklabels(wrapped_categories, ha='center')


    # Draw a horizontal line at the average E-shop margin
    ax.axhline(y=28, color='r', linestyle='--', linewidth=2, label='Average Price to Shop')
    ax.axhline(y=35, color='g', linestyle='--', linewidth=2, label='Average Price to Consumer')



    # Adding labels and title

    ax.set_ylabel('CZK/parcel')
    #ax.set_title('Margin Pool', loc = "left", fontsize = 25)
    # Place the legend below the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    ax.set_xlim([0, 1.2])

    # Remove frame
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    return(fig)

mp_notes = """
##### Data Explanation and Data Acquisition Strategies
**E-Shop Margin = Price to Consumer - Price to Shop**
* Price to Consumer:
    * Strategy 0.1: Manual Page visit
    * Strategy 1.0: AI augmented Scraper, Human reviewed, one-off
    * Strategy 2.0: HTML scraper, regular visits
* Price to Shop Packeta:
    * We know
* Price to Shop Alternatives:
    * Strategy 0.1: Assume our prices
    * Strategy 1.0: Ask Customer

**Packeta Profit = Price to shop - Packeta Costs**
* Packeta Costs
    * Strategy 0.1:
    * Strategy 1.0: Split fixed vs variable, split by types of operations
    * Strategy 2.0: Split by routes, depots

**Volumes**
* Packeta Total
    * We know
* Shop Total
    * Strategy 0.1: Ask
    * Strategy 0.2: triangulate from: Estimate (ask for) AOV, financial records, newspaper articles
    * Strategy 1.0: Implement API in exchange for something
* Alternatives split
    *Strategy 0.1: Ask, apply overall marketshares
* Share of Free Shipping (Packeta and Alternatives)
    * Strategy 0.1: Ask shop, Use break-even point, use knowledge from other shops
    * Strategy 1.0: Exchange for something
    * Strategy 2.0: Participate on some UX improvement project

**Benchmarks**
* Average price to shop, to consumer
    * Strategy 0.1: Structured collection

"""