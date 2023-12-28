# %% [markdown]
# ##ETL_Calendar

# %%
from docxtpl import DocxTemplate,InlineImage
from docx.shared import Cm
import requests
import pandas as pd
import matplotlib.pyplot as plt
from utils import airflow_colors
import psycopg2
import os
import plotly.express as px
import plotly.graph_objects as go
from croniter import croniter
import numpy as np
from matplotlib.colors import Normalize,to_rgba
from matplotlib.cm import ScalarMappable
import datetime
import croniter
from datetime import datetime
from datetime import datetime, timedelta
from utils import airflow_cmap
import numpy as np
import july
from july.utils import date_range
from matplotlib.colors import LinearSegmentedColormap
import calendar
from dotenv import load_dotenv
import july


file_queries = os.getenv('REPORT_SERVICE')


# Load environment variables from the .env file
load_dotenv()

plt.rcParams['font.family'] = 'Tahoma'
# Assume 'API_URL_GET_JOB_CALENDAR' and 'AUTH_TOKEN' are defined in your .env file
api_url_get_job_calendar = os.getenv('REPORT_SERVICE')+"get_job_calendar"
api_params = {'month': '12', 'year': '2023'}  # Replace with your desired month and year
auth_token = os.getenv('AUTH_TOKEN')

try:
    # Fetch data from the API with authentication
    headers = {'Authorization': f'Bearer {auth_token}'}
    api_response = requests.get(api_url_get_job_calendar, params=api_params, headers=headers)

    if api_response.status_code == 200:
        api_data = api_response.json()

        if 'get_job_calendar' in api_data:
            df = pd.DataFrame(api_data['get_job_calendar']['data'])
            # Convert 'Execution Date' to datetime format
            df['Execution Date'] = pd.to_datetime(df['Execution Date'])
            print(df)
            # Continue with the rest of your code (e.g., plotting) using the 'df' DataFrame
            # ...

        else:
            print("No 'get_job_calendar' key found in the API response.")
            print("Response content:", api_response.content.decode('utf-8'))

    else:
        print(f"Error fetching data from API. Status code: {api_response.status_code}")

except Exception as error:
    print("Error:", error)

# %%

# %%


# Assuming df is your DataFrame
dates = date_range('2023-10-01', '2023-10-31')
data = df[df['Execution Date'].dt.month == 10]["Percent Success"]
print(data)

# Check if dates and data are not empty
if len(dates) > 0 and len(data) > 0:
    # Generate a custom colormap
    colors = [
        (0, 'green'),
        (0.25, 'green'),
        (0.4, 'green'),
        (0.5, 'green'),
        (0.6, 'green'),
        (0.75, 'green'),
        (1.0, 'green')
    ]
    
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)
    
    # Create a month plot with the custom colormap
    fig, ax = plt.subplots(figsize=(10, 6))
    cax = july.month_plot(dates, data, month=10, cmap=custom_cmap, ax=ax)
    
    # Generate and set the title with the month name
    month_name = calendar.month_name[10]
    ax.set_title(month_name)
    
    ax.set_yticks([])  # Optionally remove y-axis ticks
    
    # Create ScalarMappable for colorbar
    sm = plt.cm.ScalarMappable(cmap=custom_cmap)
    sm.set_array([])

    # Add colorbar
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label('Percent Success')

    img_path = 'Monthly_work__process_summary_image'
    plt.savefig(img_path,bbox_inches='tight')
    # Show or save the plot as needed
    
else:
    print("Error Something")

# %%
import july
import matplotlib.pyplot as plt

# Assuming 'Execution Date' is a datetime column in your DataFrame
ax = july.calendar_plot(
    df['Execution Date'],  # Replace with your actual datetime column
    df['Percent Success'],  # Replace with your actual success percentage column
    cmap=airflow_cmap,
    title="Data Pipelines Health"
)

plt.suptitle("Data Pipelines Health")


# %%

# Load environment variables from the .env file
load_dotenv()

# %%
def query_api_for_job_scheduler(API_URL_JOB_SCHEDULER, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(API_URL_JOB_SCHEDULER, headers=headers)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["data"])
        return df
    else:
        print(f"Error fetching data from API. Status code: {response.status_code}")
        return None

# Example API URL and token
API_URL_JOB_SCHEDULER = os.getenv('REPORT_SERVICE')+"job_scheduler"

auth_token = os.getenv('AUTH_TOKEN')
headers = {'Authorization': f'Bearer {auth_token}'}
# Fetch data from the API
df_af = query_api_for_job_scheduler(API_URL_JOB_SCHEDULER, auth_token)

# Display the DataFrame
if df_af is not None:
    print(df_af)

# %%
df = df_af

# %%
df['grand_avg']=df['avg_count_dag_id'].mean()

# %%
df[df['avg_count_dag_id']==df['avg_count_dag_id'].max()]


# %%
df[df['avg_count_dag_id']==df['avg_count_dag_id'].min()]

# %%


# Assuming you have your DataFrame stored in a variable called df

# Extract the time values and average count values from the DataFrame
df['formatted_min_time_1'] = pd.to_datetime(df['formatted_min_time'], format='%H:%M')

theta = np.linspace(0, 360, len(df), endpoint=False)
theta_adjusted = np.where((theta >= 105), theta - 105, np.where(theta < 105, theta + 255, theta))

# Create a new DataFrame with polar coordinates
polar_df = pd.DataFrame({
    'theta': theta_adjusted,
    'count_dag': df["avg_count_dag_id"],
    'formatted_min_time': df['formatted_min_time_1'],
    'time': df['formatted_min_time'],
    'grand_avg': df['grand_avg']

})

# Specify the color range based on the min and max of avg_count_dag_id
color_min = polar_df['count_dag'].min()
color_max = polar_df['count_dag'].max()

# Create a polar scatter plot using Plotly Express
fig2=px.line_polar(polar_df, r='grand_avg', theta='theta',
               color="grand_avg", line_close=True,
                    
                 )
fig = px.bar_polar(polar_df, r='count_dag', theta='theta',
                   color='count_dag',
                    #color_continuous_scale='Blues',
                    color_continuous_scale=['#edeff2','#e6e8ed','#2c6dde'],
                   title="Jobs Schedule Occurrences Per 5 Minutes of the Day",
                   
                   )
#                    start_angle= 90)
#                    range_r=[color_min, color_max])

# Customize the radial axis
fig3 = go.Figure(
    data=fig.data
      )

fig3.update_polars(radialaxis_showticklabels=False)
fig3.update_traces(marker=dict(line=dict(color="red", width=0)))
fig3.update_traces(
    marker_coloraxis=None
)
fig3.update_layout(
   legend=dict( 
      
        # title_font_family="Times New Roman", 
        # font=dict( 
        #     family="Courier", 
        #     size=12, 
        #     color="black"
        # ), 
        bgcolor="LightBlue", 
        bordercolor="black", 
        borderwidth=1
    ) 
)

# Set custom tick labels for angular axis
fig.update_layout(
    polar=dict(
        # angularaxis_nticks=20,
        angularaxis_dtick=1,
        angularaxis_layer="above traces",

        angularaxis=dict(
            tickvals=theta,
                                # tickvals=[12*(x+1) for x in range( 0,30)],

            ticktext=[t.strftime('%H:%M') if t.strftime('%H:%M')[-2:]=='00' else '' for t in polar_df['formatted_min_time']],
            tickfont=dict(size=15),
            ticks='outside',
            # ticklen=50,
            # gridwidth=1
            # gridcolor='black'#['red' if t.strftime('%H:%M')[-2:]=='00' else 'yellow' for t in polar_df['formatted_min_time']],
        ),
        radialaxis = dict(
            range=[0, 35], 
            showticklabels=True,
              ticks='',
            tickfont=dict(
                family='Arial, sans-serif',  # Specify the font family
                color='black',              # Specify the text color
                size=12,                    # Specify the text size
            )
            
              ),
  
    )
)



# Add a colorbar to show the color scale
# fig3.update_coloraxes(colorbar_title='Number of jobs')
fig.update_layout(
    width=950,  # Adjust the width as needed
    height=800,
    template='plotly_white'
)


img_path = 'job_scheldule_cycle_image'
plt.savefig(img_path,bbox_inches='tight')
# Show the plot
# fig.show()




# %%

other_threshold = 5
plt.rcParams['font.family'] = 'Tahoma'

# %%
def query_dag_system():
    # Set the API URL and header
    API_URL_JOB_SYSTEM= os.getenv('REPORT_SERVICE')+"job_system"
    auth_token = os.getenv('AUTH_TOKEN')

    try:
        # Make the API request
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.get(API_URL_JOB_SYSTEM, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Convert the JSON response to a DataFrame
        api_data = response.json()
        df_af = pd.DataFrame(api_data["data"])
        return df_af

    except requests.exceptions.RequestException as e:
        # Print an error message if the request was not successful
        print(f"API request failed: {e}")
        return None

# Call the function to get the DataFrame
df_result = query_dag_system()

# Print or further process the resulting DataFrame
if df_result is not None:
    print(df_result)

# %%
raw_df = query_dag_system()

# %%
other_count = raw_df[raw_df['count']<other_threshold].sum().values[1]
other_df = pd.DataFrame([['others',other_count]],columns=list(raw_df.columns))

# %%
named_df = raw_df[raw_df['count']>=other_threshold]
df = pd.concat([named_df,other_df],axis=0)

# %%
other_threshold = 10  # Replace this with your desired threshold
named_df = raw_df[raw_df['count'] >= other_threshold]

# Concatenate `named_df` and `other_df` along the rows (axis=0)
df = pd.concat([named_df, other_df], axis=0)

# %%
other_threshold = 5

# Calculate the sum of 'count' for items below the threshold and add it as 'others'
other_count = raw_df[raw_df['count'] < other_threshold]['count'].sum()
other_df = pd.DataFrame([['others', other_count]], columns=raw_df.columns)

# Filter and concatenate DataFrames
named_df = raw_df[raw_df['count'] >= other_threshold]
df = pd.concat([named_df, other_df], axis=0)

# Set the index and calculate percentages
df.index = df['name']
df['percent'] = df['count'] / df['count'].sum()

# Sort by 'count' in descending order (max to min)
df = df.sort_values(by='count', ascending=False)

# Create a bar plot with wider bars
fig, ax = plt.subplots()
ax.bar(df.index, df['count'], color='#0BAFEC', width=0.9)  # Adjust the width as needed
ax.set_xlabel('หมวดหมู่')
ax.set_ylabel('จำนวน')
ax.set_title('')

# Rotate x-axis labels for readability
plt.xticks(rotation=45, ha='right')

img_path = 'job_overall_status_image'
plt.savefig(img_path,bbox_inches='tight')



# %% [markdown]
# ##TOP5 ETL

# %%


# Load environment variables from the .env file
load_dotenv()

# Define the API endpoint and parameters
API_URL_TOP5_ETL_FAIL = os.getenv('REPORT_SERVICE')+"top5_etl_fail"
api_params = {'month': '9', 'year': '2023'}  # Update with the desired month and year or use current_month and current_year
auth_token = os.getenv('AUTH_TOKEN')

# Include your authentication token in the headers
headers = {'Authorization': f'Bearer {auth_token}'}  # Replace 'POPPOPNIX' with your actual token

try:
    # Fetch data from the API with authentication
    response = requests.get(API_URL_TOP5_ETL_FAIL, params=api_params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'top5_etl_fail' in data:
            df_api = pd.DataFrame(data["top5_etl_fail"]["data"])

            # Display the top 5 cron expressions and their counts in a bar chart
            plt.figure(figsize=(10, 6))
            plt.barh(df_api['dag_id'][:5], df_api['total_success'][:5] + df_api['total_failures'][:5],
                     color=airflow_colors[0])
            plt.barh(df_api['dag_id'][:5], df_api['total_success'][:5], color=airflow_colors[-1])
            plt.rc('axes', axisbelow=True)
            plt.grid()

            plt.xlabel('Total Runs')
            plt.ylabel('DAG Names')
            plt.title('Top 5 DAGs by Total Runs')
            plt.gca().invert_yaxis()  # Invert the y-axis to display the highest count at the top
            

        else:
            print("No 'top5_etl_fail' key found in the API response.")
            print("Response content:", response.content.decode('utf-8'))

    else:
        print(f"Error fetching data from API. Status code: {response.status_code}")

except Exception as error:
    print("Error:", error)

# %%
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Tahoma'

# Sort the DataFrame in descending order by 'percent_fail'
fail_df = df_api.sort_values('percent_fail', ascending=False)

# Select the top 5 failed DAGs
top_5_fail_df = fail_df.head(5)

fig, ax = plt.subplots(figsize=(10, 6))

hbars = ax.barh(top_5_fail_df['dag_id'], top_5_fail_df['total_success'] + top_5_fail_df['total_failures'], color=airflow_colors[0])
ax.barh(top_5_fail_df['dag_id'], top_5_fail_df['total_success'], color=airflow_colors[-1])
ax.set_axisbelow(True)
ax.grid(color='#DDD', linestyle='dashed')
ax.set_xlabel('จำนวนการทำงานทั้งหมด')
ax.set_ylabel('ชื่อ DAGS')
ax.set_title('')
ax.bar_label(hbars, labels=[f'{e:.2f}%' for e in top_5_fail_df['percent_success']],
             padding=8, color='g', fontsize=14)
ax.bar_label(hbars, labels=[f'/{e:.2f}%' for e in top_5_fail_df['percent_fail']],
             padding=61, color='r', fontsize=14)
ax.set_xlim(right=max(top_5_fail_df['total_runs']) + 500)

# Invert the y-axis to display the highest count at the top
ax.invert_yaxis()

img_path = 'job_detail_image'
plt.savefig(img_path,bbox_inches='tight')



# %% [markdown]
# ##Sum_etl

# %%


# Load environment variables from the .env file
load_dotenv()

# API endpoint and parameters

API_URL_SUM_ETL = os.getenv('REPORT_SERVICE')+"sum_etl"
api_params = {'month': '08', 'year': '2023'}

# Include your authentication token in the headers
auth_token = os.getenv('AUTH_TOKEN')
 # Replace 'POPPOPNIX' with your actual token
headers = {'Authorization': f'Bearer {auth_token}'}

try:
    # Fetch data from the API with authentication
    response = requests.get(API_URL_SUM_ETL, params=api_params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Extract data from the response
        if 'sum_etl' in data and 'data' in data['sum_etl']:
            df_api = pd.DataFrame(data['sum_etl']['data'])

            # Display the DataFrame
            print(df_api)

        else:
            print("No 'data' key found in the 'sum_etl' API response.")
            print("Response content:", data)

    else:
        print(f"Error fetching data from API. Status code: {response.status_code}")

except Exception as error:
    print("Error:", error)

# %% [markdown]
# ##Total_run

# %%


# Load environment variables from the .env file
load_dotenv()

plt.rcParams['font.family'] = 'Tahoma'

# API endpoint and parameters
api_url_total_run = os.getenv('REPORT_SERVICE')+"total_run"
api_params_total_run = {'month': '10', 'year': '2023'}
auth_token = os.getenv('AUTH_TOKEN')

# Include your authentication token in the headers
headers = {'Authorization': f'Bearer {auth_token}'}   # Replace 'POPPOPNIX' with your actual token

try:
    # Fetch data from the 'total_run' API with authentication
    response_total_run = requests.get(api_url_total_run, params=api_params_total_run, headers=headers)

    if response_total_run.status_code == 200:
        data_total_run = response_total_run.json()
        
        # Check if 'data' key is present in the API response
        if 'data' in data_total_run.get('total_runs', {}):
            # Extract relevant data from the API response
            total_runs_data = data_total_run['total_runs']['data'][0]
            
            # Create a DataFrame from the API data
            df_total_runs = pd.DataFrame([total_runs_data])

            # Calculate success and failure rates in percentage
            df_total_runs['success_rate'] = (df_total_runs['total_success'] / df_total_runs['total_runs']) * 100
            df_total_runs['failure_rate'] = (df_total_runs['total_failures'] / df_total_runs['total_runs']) * 100
            
            # Display the DataFrame
            print("Total Runs Metrics:")
            print(df_total_runs)

            # Plot a bar chart
            df_total_runs[['total_success', 'total_failures']].plot(kind='bar', stacked=True, color=['green', 'red'])
            plt.xlabel('')
            plt.ylabel('จำนวนครั้ง')
            plt.title('')
            plt.xticks(rotation=0)
            plt.legend(['Success', 'Failures'])
            
            


        else:
            print("No 'data' key found in the 'total_run' API response.")
            print("Response content:", response_total_run.content.decode('utf-8'))

    else:
        print(f"Error fetching data from 'total_run' API. Status code: {response_total_run.status_code}")

except Exception as error:
    print("Error:", error)



# Load environment variables from the .env file
load_dotenv()

plt.rcParams['font.family'] = 'Tahoma'

# API endpoint and parameters
api_url_total_run = os.getenv('REPORT_SERVICE')+"total_run"
api_params_total_run = {'month': '10', 'year': '2023'}
auth_token = os.getenv('AUTH_TOKEN')

# Include your authentication token in the headers
headers = {'Authorization': f'Bearer {auth_token}'}   # Replace 'POPPOPNIX' with your actual token

try:
    # Fetch data from the 'total_run' API with authentication
    response_total_run = requests.get(api_url_total_run, params=api_params_total_run, headers=headers)

    if response_total_run.status_code == 200:
        data_total_run = response_total_run.json()
        
        # Check if 'data' key is present in the API response
        if 'data' in data_total_run.get('total_runs', {}):
            # Extract relevant data from the API response
            total_runs_data = data_total_run['total_runs']['data'][0]
            
            # Create a DataFrame from the API data
            df_total_runs = pd.DataFrame([total_runs_data])

            # Calculate success and failure rates in percentage
            df_total_runs['success_rate'] = (df_total_runs['total_success'] / df_total_runs['total_runs']) * 100
            df_total_runs['failure_rate'] = (df_total_runs['total_failures'] / df_total_runs['total_runs']) * 100
            
            # Calculate total_auto_run
            df_total_runs['total_auto_run'] = df_total_runs['total_runs'] - df_total_runs['total_manual_runs']

            # Reorder columns
            columns_order = ['total_runs', 'total_auto_run', 'total_manual_runs', 'total_success', 'total_failures', 'success_rate']
            df_total_runs = df_total_runs[columns_order]

            # Display the DataFrame
            print("Total Runs Metrics:")
            print(df_total_runs)

        else:
            print("No 'data' key found in the 'total_run' API response.")
            print("Response content:", response_total_run.content.decode('utf-8'))

    else:
        print(f"Error fetching data from 'total_run' API. Status code: {response_total_run.status_code}")

except Exception as error:
    print("Error:", error)

# %%

# Load environment variables from the .env file
load_dotenv()



# API endpoint and parameters
API_URL_DAG = os.getenv('REPORT_SERVICE')+"get_dag"
auth_token = os.getenv('AUTH_TOKEN')
headers = {'Authorization': f'Bearer {auth_token}'}  
payload = {}
response = requests.request("GET", API_URL_DAG, headers=headers, data=payload)

print(response.text)


# %%


# Load environment variables from the .env file
load_dotenv()

# API endpoint and parameters
API_URL_DAG = os.getenv('REPORT_SERVICE')+"get_dag"
auth_token = os.getenv('AUTH_TOKEN')
headers = {'Authorization': f'Bearer {auth_token}'}
payload = {}

# Make the GET request
response = requests.get(API_URL_DAG, headers=headers, data=payload)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract 'data' from the JSON response
    api_data = response.json()['data']
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(api_data)
    
    # Add a new column 'dag_is_python'
    df['dag_is_python'] = df['dag_is_active'] - df['dag_is_talend']
    
    # Add a new column 'job_inactive'
    df['job_inactive'] = df['dag_all'] - df['dag_is_active']
    
    # Reorder columns
    df = df[['dag_all', 'dag_is_active', 'job_inactive', 'dag_is_talend', 'dag_is_python']]
    
    # Now you can work with the DataFrame (e.g., print it, analyze it, plot it)
else:
    print(f"Error: {response.status_code}")
    print(response.text)


# %%

# writing data in each table
doc = DocxTemplate
context = {

    'dag_all': df['dag_all'][0], ##from dag_all.py
    'dag_is_active': df['dag_is_active'][0], ##from dag_all.py
    'job_inactive': df['job_inactive'][0], ##from dag_all.py
    'dag_is_talend': df['dag_is_talend'][0], ##from dag_all.py
    'dag_is_python': df['dag_is_python'][0], ##from dag_all.py
    'normal_count': df_api['normal_count'][0], ##from sum_etl.py
    'warning_count': df_api['warning_count'][0], ##from sum_etl.py
    'critical_count': df_api['critical_count'][0], ##from sum_etl.py
    'total_runs': df_total_runs['total_runs'][0], #from total_run.py
    'total_auto_run': df_total_runs['total_auto_run'][0], #from total_run.py
    'total_manual_runs': df_total_runs['total_manual_runs'][0], #from total_run.py
    'total_success': df_total_runs['total_success'][0], #from total_run.py
    'total_failures': df_total_runs['total_failures'][0], #from total_run.py
    'success_rate': df_total_runs['success_rate'][0], #from total_run.py
    'Monthly_work__process_summary_image':InlineImage(doc,"./DataBase/Monthly_work__process_summary_image.png",width=Cm(16)),
    'job_scheldule_cycle_image':InlineImage(doc,"./DataBase/job_scheldule_cycle_image.png",width=Cm(16)),
    'job_overall_status_image':InlineImage(doc,"./DataBase/job_overall_status_image.png",width=Cm(16)),
    'job_detail_image':InlineImage(doc,"./DataBase/job_detail_image.png",width=Cm(16))
    
    
    }

def get_auditrail() :
    # print(context)
    return context


