# %%
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import json 
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.abspath('../'))
from dotenv import load_dotenv
from docxtpl import DocxTemplate,InlineImage
load_dotenv()

# %% [markdown]
# ## Import Data

# %%
file_queries = os.getenv('REPORT_SERVICE')+ 'server/server-info'
print(file_queries)

# %%
from urllib.request import urlopen

# Open the URL using urlopen
with urlopen(file_queries) as response:
    file_contents = response.read().decode('utf-8')
    # print(file_contents)

# %%
encryp = {
    "key" : os.environ.get('ENCRYPTION_KEY'),
    "iv" : os.environ.get('ENCRYPTION_IV')
}
print(encryp)

# %%
def decrypt(encrypted_text):
        # try:
        # print(encrypted_text)
        encrypted_bytes = b64decode(encrypted_text)
        cipher = AES.new(bytes(encryp['key'], 'utf-8'), AES.MODE_CBC, bytes(encryp['iv'],'utf-8'))
        decrypted = cipher.decrypt(encrypted_bytes)
        unpadded = unpad(decrypted, AES.block_size)
        return unpadded 

# %%
server_info = decrypt(file_contents).decode()
server_info_json = json.loads(server_info)
print(server_info_json)

# %%
# Extract the 'data' list from the dictionary
data_list = server_info_json['data']

# Convert the list of dictionaries to a DataFrame
df_server = pd.DataFrame(data_list)

# # Display the DataFrame
# print(df_server)
# df_server

# %%
# Add a new column 'Run_Number' with consecutive numbers starting from 1
df_server['Run_Number'] =  np.arange(1, len(df_server) + 1)

df_server =  df_server[['Run_Number', 'server_name', 'services_software', 'hostname', 'ip_address']]
df_server  = df_server.rename(columns={"Run_Number": "No", "server_name": "Name","services_software":"Service", "hostname":"Hostname","ip_address":"Private IP"})

# Display the DataFrame with the new column
# print(df_server)
df_server

# %%
all_server = df_server.to_dict()
all_server


context = {
         'all_server': all_server
        }


def server_all() :
    # print(context)
    return context