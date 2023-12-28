import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import numpy as np

# Define your custom colors
airflow_colors = [
    '#F23000',
    '#E65C00',
    '#D98200',
    '#CCA300',
    '#C0C000',
    '#8FB300',
    '#64A600',
    '#3D9900',
    '#1C8D00',
    '#008000',
]

airflow_colors_rgba = [
    (1.0, 0.137, 0.0, 1.0),  # RGBA for #F23000
    (0.90196, 0.36078, 0.0, 1.0),  # RGBA for #E65C00
    (0.85098, 0.50588, 0.0, 1.0),  # RGBA for #D98200
    (0.8, 0.63922, 0.0, 1.0),  # RGBA for #CCA300
    (0.75294, 0.75294, 0.0, 1.0),  # RGBA for #C0C000
    (0.56078, 0.70196, 0.0, 1.0),  # RGBA for #8FB300
    (0.39216, 0.65098, 0.0, 1.0),  # RGBA for #64A600
    (0.23922, 0.6, 0.0, 1.0),  # RGBA for #3D9900
    (0.1098, 0.55294, 0.0, 1.0),  # RGBA for #1C8D00
    (0.0, 0.50196, 0.0, 1.0),  # RGBA for #008000
]

# Function to convert hex color codes to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

# Convert hex colors to RGB
rgb_colors = [hex_to_rgb(color) for color in airflow_colors]
# Create a custom colormap from the colors
# airflow_cmap = ListedColormap(colors)
# airflow_cmap = LinearSegmentedColormap.from_list('airflow', rgb_colors )
airflow_cmap = ListedColormap(airflow_colors_rgba)

# airflow_cmap = mcolors.LinearSegmentedColormap.from_list("custom_colormap", airflow_colors, N=len(airflow_colors))
if __name__ == '__main__':
    print(rgb_colors)
    airflow_cmap
    data = np.random.rand(10, 10)
    plt.imshow(data, cmap=airflow_cmap)
    plt.show()
