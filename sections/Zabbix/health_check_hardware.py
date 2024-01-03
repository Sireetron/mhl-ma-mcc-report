# %%
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os
from docxtpl import DocxTemplate,InlineImage

# writing data in each table
doc = DocxTemplate
# Define the directory to save the figures
save_dir = "./sections/Zabbix/Image"

# Ensure the directory exists, create it if necessary
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# %% [markdown]
# # import data from GG Sheet

# %%
## original data https://docs.google.com/spreadsheets/d/14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A/edit?pli=1#gid=0

# %%
from datetime import datetime

# Original date string
original_date_string = "2024-01"

# Convert to datetime object
original_date = datetime.strptime(original_date_string, "%Y-%m")

# Format the datetime object into a new string
sheet_name = original_date.strftime("%b%y")

# Display the result
print(sheet_name)

# %%
## sheet สถานภาพเครื่องแม่ข่าย_และอุปกรณ์ต่อพ่วง_PoPNix owner P'Pooooo

sheet_id = '14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A'
sheet_name = 'Jan67'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df = pd.read_csv(url)
df # print(df.head())

# %%
lst_serial = df['Serial Number']
lst_serial

# %%
lst_device = df['List Devices']
lst_device

# %%
lst_health = df['Health Check']
lst_health

# %%
lst_clean = df['Clean Check']
lst_clean

# %%
lst_clean[1]

# %%
status = df['Health Check'][1]
status

# %% [markdown]
# # Print figure for Health Check

# %%
# Replace 'path/to/your/image.jpg' with the actual path to your image file
# image_pass =  './sections/Zabbix/Image/pass.png'
# image_not_pass =  './sections/Zabbix/Image/not_pass.png'
image_pass =  'C:/Users/Admins/Documents/GitHub/mhl-ma-report/sections/Zabbix/Image/pass.png'
image_not_pass =  'C:/Users/Admins/Documents/GitHub/mhl-ma-report/sections/Zabbix/Image/not_pass.png'

# Open the image using Pillow
img_pass = Image.open(image_pass)
img_not_pass = Image.open(image_not_pass)

def show_img(status):
    if status == True:
        img = img_pass
    else: img = img_not_pass
    return img

health_check = []


# Display  figures using a for loop
for i in range(len(lst_health)):  # Display at most 10 figures
    img_health = show_img(lst_health[i])
    
    # Print lst_device and lst_serial for each device
    # print(f"Device: {lst_device[i]}, Serial: {lst_serial[i]}")
    device_name = lst_device[i]
    serial_number = lst_serial[i]
    plt.figure()  # Create a new figure
    plt.imshow(img_health)
    plt.axis('off')  # Turn off axis labels

     # Save the plot
    image_health_check = f'health_check_{device_name}.png'
    plt.savefig(os.path.join(save_dir,image_health_check))

    img_clean = show_img(lst_clean[i])
    plt.figure()  # Create a new figure
    plt.imshow(img_clean)
    plt.axis('off')  # Turn off axis labels
    image_clean_check = f'clean_check_{device_name}.png'
    plt.savefig(os.path.join(save_dir,image_clean_check))

    plt.close()  # Close the plot to avoid overlapping when iterating over multiple datasets

     # Append the values to disk_space list
    health_check.append({
        'device_name' : device_name,
        'serial_number': serial_number, 
        'image_health_check': InlineImage(doc,f"{image_health_check}"),
        'image_clean_check': InlineImage(doc,f"{image_clean_check}")
    })

# # Show all figures
# plt.show()

# %%
health_check[1]


context = {
         'health_check': health_check
        }


def health_check_hardware() :
    # print(context)
    return context