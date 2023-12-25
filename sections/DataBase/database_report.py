#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup


# ## Queries

# In[2]:


import os

os.system("pip install python-dotenv")


# In[3]:


import sys
sys.path.append(os.path.abspath('../'))
from dotenv import load_dotenv
load_dotenv()


# In[4]:


# from urllib.request import urlopen

# file_queries = os.getenv('file_queries')

# # Open the file using urlopen
# with urlopen(file_queries) as file:
#     # Read the HTML content from the file
#     html_content = file.read().decode('utf-8')

# # Parse the HTML using BeautifulSoup
# queries_ = BeautifulSoup(html_content, 'html.parser')

# # Print the prettified HTML
# print(queries_.prettify())


# In[5]:


file_queries = os.getenv('REPORT_SERVICE')+"database/report/2311"
print(file_queries)


# In[6]:


from urllib.request import urlopen

# Open the file using urlopen
with urlopen(file_queries) as file:
    # Read the HTML content from the file
    html_content = file.read().decode('utf-8')

# Parse the HTML using BeautifulSoup
queries_ = BeautifulSoup(html_content, 'html.parser')

# Print the prettified HTML
print(queries_.prettify())


# In[7]:


tabbable = queries_.find('div', {'class': 'tabbable'})
tabbable


# In[8]:


tab_content1 = tabbable.find('div', {'class': 'tab-content'})
tab_content1


# In[9]:


element = tab_content1.find('div', {'class': 'tab-pane active', 'id': 'tab-queries'})

# type(element)
element = '"""'+ str(element) + '"""'
element


# In[10]:


# Parse the HTML content
soup = BeautifulSoup(element, 'html.parser')

# Get the text content
text_content = soup.get_text(strip=True, separator='\n')

print(text_content)


# In[11]:


# Parse the HTML content
soup = BeautifulSoup(element, 'html.parser')

# Get the text content
text_content = soup.get_text(strip=True, separator='\n')

# Split the text content into a list of lines
lines = text_content.split('\n')

# Create variables to store the values
num_unique_queries = int(lines[1].replace(',', ''))
num_queries = int(lines[3].replace(',', ''))
total_query_duration = lines[5]
first_query = lines[7]
last_query = lines[9]
queries_per_second = lines[11]

# Print or use the variables as needed
print("Number of unique normalized queries:", num_unique_queries)
print("Number of queries:", num_queries)
print("Total query duration:", total_query_duration)
print("First query:", first_query)
print("Last query:", last_query)
print("Queries per second:", queries_per_second)


# ## Queries by type

# In[12]:


file_type = os.getenv('REPORT_SERVICE')+"database/report/2311#queries-by-type"
print(file_type)


# In[13]:


# Open the file using urlopen
with urlopen(file_type) as file:
    # Read the HTML content from the file
    html = file.read().decode('utf-8')

# Parse the HTML using BeautifulSoup
type = BeautifulSoup(html, 'html.parser')

# Print the prettified HTML
print(type.prettify())


# In[14]:


# from urllib.request import urlopen

# # Specify the file path
# file_type = 'file:///D:/maholan/mwa/out.html#queries-by-type'

# # Open the file using urlopen
# with urlopen(file_type) as file:
#     # Read the HTML content from the file
#     html = file.read().decode('utf-8')

# # Parse the HTML using BeautifulSoup
# type = BeautifulSoup(html, 'html.parser')

# # Print the prettified HTML
# print(type.prettify())


# In[15]:


analy = type.find('div', {'class': 'analysis-item row', 'id': 'queries-by-type'})
analy


# In[16]:


tab_content2 = analy.find('div', {'class': 'tab-content'})
tab_content2


# In[17]:


element2 = tab_content2.find('script', {'type': 'text/javascript'})
element2

# type(element2)
element2 = '"""'+ str(element2) + '"""'
element2


# In[18]:


import re
import ast

match = re.search(r'var data_26 = \[\s*(\[.*\])\s*\];', element2)

if match:
    extracted_list_str = match.group(1)
    print(extracted_list_str)
    print(type(extracted_list_str))
    my_list_of_lists = ast.literal_eval(f"[{extracted_list_str}]")


# In[19]:


my_list_of_lists


# In[20]:


import matplotlib.pyplot as plt

# Extract labels and values from the data
labels, values = zip(*my_list_of_lists)

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Type of Queries')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the pie chart
plt.show()


# In[21]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from cycler import cycler

# Create a DataFrame
df_queries_by_type = pd.DataFrame(my_list_of_lists, columns=['Type', 'Count'])

# Calculate percentage
df_queries_by_type['Percentage'] = df_queries_by_type['Count'] / df_queries_by_type['Count'].sum() * 100

# Plotting the pie chart
labels = df_queries_by_type['Type'].to_list()
sizes = df_queries_by_type['Percentage'].to_list()
explode = tuple([0.05] * len(sizes))
num = len(sizes)

# Set up colors
cmap = get_cmap('tab10')
inner_colors = cmap(np.arange(num))

# Plot the pie chart
fig, ax = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode,
                                  colors=inner_colors, textprops={'fontsize': 9, 'weight': 'bold'})

# Add a circle at the center to make it a donut chart
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Add legend
ax.legend(wedges, labels, title="Queries by Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Add title
plt.title('Queries by Type', loc='left', fontsize=20, weight='bold', color="#9B9B9B")

# # Save the figure
# plt.tight_layout()
# fig.savefig('Queries_by_type.png')

plt.show()


# In[22]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from cycler import cycler

# Create a DataFrame
df_queries_by_type = pd.DataFrame(my_list_of_lists, columns=['Type', 'Count'])

# Calculate percentage
df_queries_by_type['Percentage'] = df_queries_by_type['Count'] / df_queries_by_type['Count'].sum() * 100

# Plotting the pie chart
labels = df_queries_by_type['Type'].to_list()
sizes = df_queries_by_type['Percentage'].to_list()
explode = tuple([0.05] * len(sizes))
num = len(sizes)

# Set up colors with a blue colormap
cmap = get_cmap('Blues')
inner_colors = cmap(np.linspace(0.2, 1, num))

# Plot the pie chart
fig, ax = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode,
                                  colors=inner_colors, textprops={'fontsize': 9, 'weight': 'bold'})

# Add a circle at the center to make it a donut chart
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that the pie is drawn as a circle
ax.axis('equal')

# Add legend
ax.legend(wedges, labels, title="Queries by Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Add title
plt.title('Queries by Type', loc='left', fontsize=20, weight='bold', color="#9B9B9B")

# Save the figure
plt.tight_layout()

# Save the plot
fig.savefig('queries_by_type_image.png')

plt.show()


# ## Disk Space

# In[23]:


file_disk_space= os.getenv('REPORT_SERVICE')+"database/size"
print(file_disk_space)


# In[24]:


import json

# Open the file using urlopen
with urlopen(file_disk_space) as file:
    # Read the JSON content from the file
    json_data = json.load(file)

json_data


# ## Disk Space Leakage

# In[25]:


# Extract the first item from the array
df_disk_space_leakage = json_data[0]
df_disk_space_leakage


# In[26]:


# Access individual values and assign them to variables
db_name_space_leakage = df_disk_space_leakage['db_name']
desc_space_leakage = df_disk_space_leakage['desc']
data_space_leakage = df_disk_space_leakage['data']

# Access values within the 'data' dictionary
database_name_space_leakage = data_space_leakage['database_name']
total_database_size_space_leakage = data_space_leakage['total_database_size']
total_table_size_space_leakage = data_space_leakage['total_table_size']
total_index_size_space_leakage = data_space_leakage['total_index_size']

# Print or use the variables as needed
print("db_name:", db_name_space_leakage)
print("desc:", desc_space_leakage)
print("database_name:", database_name_space_leakage)
print("total_database_size:", total_database_size_space_leakage)
print("total_table_size:", total_table_size_space_leakage)
print("total_index_size:", total_index_size_space_leakage)


# In[27]:


# Convert to Megabyte
total_database_size_space_leakage_mb = round(total_database_size_space_leakage / (1024 * 1024), 4)

print("total database size in MB:", total_database_size_space_leakage_mb)


# In[28]:


# Assuming you have calculated these percentages
percent_table_size_space_leakage = (total_table_size_space_leakage / total_database_size_space_leakage) * 100
percent_index_size_space_leakage = (total_index_size_space_leakage / total_database_size_space_leakage) * 100
percent_other_space_leakage = 100 - percent_table_size_space_leakage - percent_index_size_space_leakage

# Pie chart
labels = ['Data Size', 'Index Size', 'Other']
sizes = [percent_table_size_space_leakage, percent_index_size_space_leakage, percent_other_space_leakage]
explode = tuple([0.05] * len(sizes))
inner_colors = ['#018CDF', '#F7AF41', '#E5E7E9']

plt.pie(sizes, colors=inner_colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode, textprops={'fontsize': 12, 'weight': 'bold'})
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.tight_layout()
plt.legend(labels=labels, title="Type:", loc='right', bbox_to_anchor=(1.2, 0.5))
plt.title('Disk Space', loc='left', fontsize=20, weight='bold', color="#9B9B9B")
fig.set_size_inches(6, 7)

plt.show()

# Save the plot
fig.savefig('disk_space_leakage_chart_image.png', bbox_inches='tight')


# ##  Disk Space Salinity

# In[29]:


# Extract the second item from the array
df_disk_space_salinity = json_data[1]
df_disk_space_salinity


# In[30]:


# Access individual values and assign them to variables
db_name_space_salinity = df_disk_space_salinity['db_name']
desc_space_salinity = df_disk_space_salinity['desc']
data_space_salinity = df_disk_space_salinity['data']

# Access values within the 'data' dictionary
database_name_space_salinity = data_space_salinity['database_name']
total_database_size_space_salinity = data_space_salinity['total_database_size']
total_table_size_space_salinity = data_space_salinity['total_table_size']
total_index_size_space_salinity = data_space_salinity['total_index_size']

# Print or use the variables as needed
print("db_name:", db_name_space_salinity)
print("desc:", desc_space_salinity)
print("database_name:", database_name_space_salinity)
print("total_database_size:", total_database_size_space_salinity)
print("total_table_size:", total_table_size_space_salinity)
print("total_index_size:", total_index_size_space_salinity)


# In[ ]:


# Convert to Megabyte
total_database_size_space_salinity_mb = round(total_database_size_space_salinity / (1024 * 1024), 4)

print("total database size in MB:", total_database_size_space_salinity_mb)


# In[32]:


# Assuming you have calculated these percentages
percent_table_size_space_salinity = (total_table_size_space_salinity / total_database_size_space_salinity) * 100
percent_index_size_space_salinity = (total_index_size_space_salinity / total_database_size_space_salinity) * 100
percent_other_space_salinity = 100 - percent_table_size_space_salinity - percent_index_size_space_salinity

# Pie chart
labels = ['Data Size', 'Index Size', 'Other']
sizes = [percent_table_size_space_salinity, percent_index_size_space_salinity, percent_other_space_salinity]
explode = tuple([0.05] * len(sizes))
inner_colors = ['#018CDF', '#F7AF41', '#E5E7E9']

plt.pie(sizes, colors=inner_colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode, textprops={'fontsize': 12, 'weight': 'bold'})
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.tight_layout()
plt.legend(labels=labels, title="Type:", loc='right', bbox_to_anchor=(1.2, 0.5))
plt.title('Disk Space', loc='left', fontsize=20, weight='bold', color="#9B9B9B")
fig.set_size_inches(6, 7)

plt.show()

# Save the plot
fig.savefig('disk_space_salinity_chart_image.png', bbox_inches='tight')


# writing data in each table
# doc = DocxTemplate
context = {
    'num_unique_queries': num_unique_queries,
    'num_queries': num_queries,
    'queries_per_second': queries_per_second,
    'total_database_size_space_leakage_mb': total_database_size_space_leakage_mb,
    'total_database_size_space_salinity_mb': total_database_size_space_salinity_mb,
    'queries_by_type_image.png': 'queries_by_type_image.png',
    'disk_space_leakage_chart_image.png': 'disk_space_leakage_chart_image.png',
    'disk_space_salinity_chart_image.png': 'disk_space_salinity_chart_image.png'
    }


def auditrail() :
    # print(context)
    return context