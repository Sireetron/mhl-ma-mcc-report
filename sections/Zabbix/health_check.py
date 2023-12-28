#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import os

# Define the directory to save the figures
save_dir = "C:/Users/jdpsk/OneDrive/Desktop/ST/report_water/Image/"

# Ensure the directory exists, create it if necessary
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# # import data from GG Sheet

# In[9]:


## original data https://docs.google.com/spreadsheets/d/14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A/edit?pli=1#gid=0


# In[10]:

## sheet สถานภาพเครื่องแม่ข่าย_และอุปกรณ์ต่อพ่วง_PoPNix owner P'Pooooo

SHEET_ID = '14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A'
SHEET_NAME = 'status'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
df # print(df.head())

# In[11]:


lst_health = df['Health Check']
lst_health


# In[12]:


lst_clean = df['Clean Check']
lst_clean


# In[13]:


status = df['Health Check'][1]
status


# # Print figure for Health Check

# In[14]:


# Replace 'path/to/your/image.jpg' with the actual path to your image file
# image_pass =  './sections/Zabbix/Image/pass.png'
# image_not_pass =  './sections/Zabbix/Image/not_pass.png'
image_pass = 'C:/Users/jdpsk/OneDrive/Desktop/ST/report_water/Image/pass.png'
image_not_pass = 'C:/Users/jdpsk/OneDrive/Desktop/ST/report_water/Image/not_pass.png'

# Open the image using Pillow
img_pass = Image.open(image_pass)
img_not_pass = Image.open(image_not_pass)

def show_img(status):
    if status == True:
        img = img_pass
    else: img = img_not_pass
    return img

# Display 10 figures using a for loop
for index, value in enumerate(lst_health):
    img = show_img(value)
    plt.figure()  # Create a new figure
    plt.imshow(img)
    plt.axis('off')  # Turn off axis labels
    plt.savefig(os.path.join(save_dir, f'health_check_{index+1}.png'))
    # plt.savefig(f'health_check_{index+1}.png')
    # plt.savefig(f'health_check_{index+1}.png')
    plt.close()  # Close the plot to avoid overlapping when iterating over multiple datasets

# # # Show all figures
plt.show()


# # Print Figure for Clean check

# In[15]:


# Replace 'path/to/your/image.jpg' with the actual path to your image file
# image_pass =  './sections/Zabbix/Image/pass.png'
# image_not_pass =  './sections/Zabbix/Image/not_pass.png'
image_pass = 'C:/Users/jdpsk/OneDrive/Desktop/ST/report_water/Image/pass.png'
image_not_pass = 'C:/Users/jdpsk/OneDrive/Desktop/ST/report_water/Image/not_pass.png'

# Open the image using Pillow
img_pass = Image.open(image_pass)
img_not_pass = Image.open(image_not_pass)

def show_img(status):
    if status == True:
        img = img_pass
    else: img = img_not_pass
    return img

# Display 10 figures using a for loop
for index, value in enumerate(lst_clean):
    img = show_img(value)
    plt.figure()  # Create a new figure
    plt.imshow(img)
    plt.axis('off')  # Turn off axis labels
    plt.savefig(os.path.join(save_dir, f'clean_check_{index+1}.png'))
    # plt.savefig(f'clean_check_{index+1}.png')
    plt.close()  # Close the plot to avoid overlapping when iterating over multiple datasets

# # # Show all figures
plt.show()

# # Print only one figure

# In[16]:


def show_img(status):
    if status == True:
        img = img_pass
    else: img = img_not_pass
    
    return img

result = show_img(lst_clean[1])
plt.figure()  # Create a new figure
plt.imshow(result)
plt.axis('off')  # Turn off axis labels

# # # Show all figures
plt.show()


# # In[17]:



# .ipynb -> .py
# get_ipython().system('jupyter nbconvert --to script health_check.ipynb')

from docxtpl import DocxTemplate,InlineImage
# writing data in each table
doc = DocxTemplate
context = {
    #################################### health check
    'Private_Cloud_1_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_1.png'),
    'Private_Cloud_2_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_2.png'),
    'Private_Cloud_3_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_3.png'),
    'Big_data_Data_node_1_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_4.png'),
    'Big_data_Data_node_2_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_5.png'),
    'Big_data_Data_node_3_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_6.png'),
    'Frontend_server_1_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_7.png'),
    'Frontend_server_2_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_8.png'),
    'Backup_server_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_9.png'),
    'Network_L3_Switch_1_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_10.png'),
    'Network_L3_Switch_2_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_11.png'),
    'Network_L2_Switch_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_12.png'),
    'Deep_Learning_Server_1_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_13.png'),
    'Deep_Learning_Server_2_health_check': InlineImage(doc,f'./sections/Zabbix/Image/health_check_14.png'),
    
    #################################### Clean check
    'Private_Cloud_1_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_1.png'),
    'Private_Cloud_2_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_2.png'),
    'Private_Cloud_3_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_3.png'),
    'Big_data_Data_node_1_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_4.png'),
    'Big_data_Data_node_2_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_5.png'),
    'Big_data_Data_node_3_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_6.png'),
    'Frontend_server_1_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_7.png'),
    'Frontend_server_2_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_8.png'),
    'Backup_server_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_9.png'),
    'Network_L3_Switch_1_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_10.png'),
    'Network_L3_Switch_2_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_11.png'),
    'Network_L2_Switch_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_12.png'),
    'Deep_Learning_Server_1_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_13.png'),
    'Deep_Learning_Server_2_clean_check': InlineImage(doc,f'./sections/Zabbix/Image/clean_check_14.png')
    }


# # doc.render(context)
# # doc.save(f'./Docxfile/{month}_{year}/Audittrail_edit.docx')


def auditrail() :
    # print(context)
    return context