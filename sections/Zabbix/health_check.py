#!/usr/bin/env python
# coding: utf-8

# In[103]:


import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os

# Define the directory to save the figures
save_dir = "C:/Users/Admins/Documents/GitHub/mhl-ma-report/sections/Zabbix/Image"

# Ensure the directory exists, create it if necessary
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# # import data from GG Sheet

# In[104]:


## original data https://docs.google.com/spreadsheets/d/14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A/edit?pli=1#gid=0


# In[105]:


## sheet สถานภาพเครื่องแม่ข่าย_และอุปกรณ์ต่อพ่วง_PoPNix owner P'Pooooo

SHEET_ID = '14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A'
SHEET_NAME = 'status'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
df # print(df.head())


# In[106]:


lst_serial = df['List Devices']
lst_serial


# In[107]:


lst_device = df['List Devices']
lst_device


# In[108]:


lst_health = df['Health Check']
lst_health


# In[109]:


lst_clean = df['Clean Check']
lst_clean


# In[110]:


lst_clean[1]


# In[111]:


status = df['Health Check'][1]
status


# # Print figure for Health Check

# In[128]:


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
        'image_health_check': image_health_check,
        'image_clean_check': image_clean_check
    })

# # Show all figures
# plt.show()


# In[129]:


health_check


# In[130]:


# .ipynb -> .py
get_ipython().system('jupyter nbconvert --to script health_check.ipynb')

