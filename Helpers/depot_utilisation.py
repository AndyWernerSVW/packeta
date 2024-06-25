import matplotlib.pyplot as plt
import numpy as np

def plot_depot_utilization(depot_names, depot_utilisation=None, number_of_parcels=None,
                           special_depot_utilisation=None, special_number_of_parcels=None,
                           cost_per_unit=None):
    if depot_utilisation is None or number_of_parcels is None:
        np.random.seed(0)  # For reproducibility
        depot_utilisation = np.random.uniform(30, 60, len(depot_names) - 2)
        number_of_parcels = np.random.uniform(0.5, 3.0, len(depot_names) - 2)

    if special_depot_utilisation is None or special_number_of_parcels is None:
        special_depot_utilisation = np.array([30, 35])
        special_number_of_parcels = np.array([5.5, 4.2])

    if cost_per_unit is None:
        cost_per_unit = np.random.uniform(2.3, 4.1, len(depot_names))  # Random cost per unit handled

    # Combine regular and special depots
    full_depot_utilisation = np.append(depot_utilisation, special_depot_utilisation)
    full_number_of_parcels = np.append(number_of_parcels, special_number_of_parcels)

    # Calculate point sizes, normalized based on cost_per_unit
    point_sizes = (cost_per_unit - cost_per_unit.min()) / (cost_per_unit.max() - cost_per_unit.min()) * 100 + 10  # Normalize and scale

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(full_depot_utilisation, full_number_of_parcels, s=point_sizes, c='#88294e', label='Depots', alpha=0.6)
    for i, txt in enumerate(depot_names):
        ax.annotate(txt, (full_depot_utilisation[i], full_number_of_parcels[i]))

    # Labels and Title
    ax.set_xlabel('Depot Utilisation in %')
    ax.set_ylabel('Number of Parcels in Millions')
    ax.set_title('Scatter Plot of Depot Utilization vs. Number of Parcels')

    # Customize frame
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Setting grid color to light grey
    ax.grid(True, color='lightgrey', linestyle='-', linewidth=0.5)


    return plt

# List of depot names
depot_names = [
    "Nučice u Rudné u Prahy", "Praha-Štěrboholy", "Nehvizdy u Prahy",
    "Holubice u Brna", "Ostrava", "Ústí nad Labem", "Břeclav",
    "Plzeň", "České Budějovice 'Minidepo'", "Hradec Králové", "Zlín",
    "Jihlava", "Olomouc", "Šumperk", "Liberec", "Karlovy Vary 'Minidepo'", "Svitavy"
]

# Example of calling the function
# plot_depot_utilization(depot_names)

data_needed = """#### Data Needed
- Overall Depot Utilisation
- Number of Parcels by cusotmer
- Cost per parcel per depot: would be good to split into variable and fixed. 
"""