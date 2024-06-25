import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import textwrap

# Load data
margin_pool_data  = pd.read_csv('inputs.csv')

# Columns to use
required_columns = ['Category', 'E-shop margin', 'Alternative Take', 'Packeta profit', 'Packeta costs', 'Units Sold']
margin_pool_data = margin_pool_data[required_columns]

# Data for plotting
categories = margin_pool_data['Category']
units_sold = margin_pool_data['Units Sold']

# Normalize widths
total_width = sum(units_sold)
normalized_widths = [unit / total_width for unit in units_sold]

# Calculate cumulative sums of the widths
cumulative_widths = np.cumsum(normalized_widths)

# Calculate starting positions of each bar by shifting the cumulative sums
# The starting position of the first bar is 0
width_positions = np.concatenate(([0], cumulative_widths[:-1]))

# Color dictionary for each label
color_dict = {
    'Packeta costs': '#f0f3f9',  # Light Grey
    'Packeta profit': '#dcc1cd',  # Very Light Pink
    'E-shop margin': '#88294e',  # Dark Maroon
    'Alternative Take': '#000000'  # Black
}

# Wrap the labels
wrapped_categories = [textwrap.fill(label, 10) for label in categories]

# Use Roboto font if installed, otherwise default to Arial
plt.rcParams['font.family'] = 'Roboto' if 'Roboto' in plt.rcParams['font.family'] else 'Arial'

# Create figure and axis
fig, ax = plt.subplots()

# Create stacked bar chart with relative widths
for i, category in enumerate(categories):
    bottom = 0
    for value, label in zip(
        [margin_pool_data.loc[i, 'Packeta profit'], margin_pool_data.loc[i, 'Packeta costs'],
         margin_pool_data.loc[i, 'Alternative Take'], margin_pool_data.loc[i, 'E-shop margin']],
        ['Packeta profit', 'Packeta costs', 'Alternative Take', 'E-shop margin']):
        ax.bar(width_positions[i], value, width=normalized_widths[i], bottom=bottom, color=color_dict[label], label=label if i == 0 else "")
        bottom += value

# Adjust the x-axis to have the correct category labels
ax.set_xticks(width_positions + np.array(normalized_widths) / 2)  # set xticks at the center of bars
ax.set_xticklabels(wrapped_categories)

# Draw a horizontal line at the average E-shop margin
average_margin = margin_pool_data['E-shop margin'].mean()
ax.axhline(y=average_margin, color='r', linestyle='--', linewidth=2, label='Average E-shop Margin')

# Add labels, title, and legend
ax.set_xlabel('Categories')
ax.set_ylabel('Amount')
ax.set_title('Stacked Bar Chart with Relative Widths')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

# Enhance aesthetics
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(True)

# Display chart in Streamlit
st.title('Relative Width Stacked Bar Chart')
st.pyplot(fig)
