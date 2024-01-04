# %%
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os
from docxtpl import DocxTemplate,InlineImage
from colorama import Fore, Style

from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal
import calendar

# writing data in each table
doc = DocxTemplate
# Define the directory to save the figures
save_dir = "./result"

# Ensure the directory exists, create it if necessary
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# %%
## original data https://docs.google.com/spreadsheets/d/14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A/edit?pli=1#gid=0

# %% [markdown]
# ## deal with date

# %%
from datetime import datetime, timedelta

# Get the current date
current_date = datetime.now()

# Convert the current date to the Thai Buddhist calendar year (add 543 years)
buddhist_year = (current_date.year + 543) % 100

# Get the first three characters of the month name
month_name = current_date.strftime('%b')

# Combine the month abbreviation and last two digits of the Buddhist year
sheet_name = f"{month_name}{buddhist_year:02}"

print(sheet_name)


# %%
# Mapping dictionary for English to Thai month names
english_to_thai_month = {
    'January': 'มกราคม',
    'February': 'กุมภาพันธ์',
    'March': 'มีนาคม',
    'April': 'เมษายน',
    'May': 'พฤษภาคม',
    'June': 'มิถุนายน',
    'July': 'กรกฎาคม',
    'August': 'สิงหาคม',
    'September': 'กันยายน',
    'October': 'ตุลาคม',
    'November': 'พฤศจิกายน',
    'December': 'ธันวาคม'
}

# Function to get the end of the month
def end_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return datetime(year, month, last_day)

# Example usage
current_date = datetime.now()

# Get the end of the current month
end_of_current_month = end_of_month(current_date.year, current_date.month)

# Convert to Thai Buddhist calendar
buddhist_calendar_date = end_of_current_month + relativedelta(years=543)

# Get the Thai month name
english_month = buddhist_calendar_date.strftime("%B")
thai_month = english_to_thai_month.get(english_month, english_month)

# Format the result
report_date = buddhist_calendar_date.strftime("%d ") + thai_month + buddhist_calendar_date.strftime(" %Y").replace("พ.ศ.", "พ.ศ.")

print("End of the current month:", end_of_current_month)
print("Converted date:", report_date)


# %% [markdown]
# # import data from GG Sheet

# %%
## sheet สถานภาพเครื่องแม่ข่าย_และอุปกรณ์ต่อพ่วง_PoPNix owner P'Pooooo

sheet_id = '14GmNx-6YkTfOSYfjQqGw-wC6h9VPqB3frw-ovtMTN5A'
sheet_name = 'Jan67'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df = pd.read_csv(url)
# df = df.sort_values(by='List Devices') # print(df.head())
df

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

# %% [markdown]
# # ผลการวิเคราะห์ Analysis Result

# %%
topic_text = f"การตรวจสอบสถานภาพพื้นฐานระบบภายในอุปกรณ์ ณ วันที่ {report_date} "
full_capacity = f"อุปกรณ์ทั้งหมดอยู่ในสถานะพร้อมใช้งาน สามารถรองรับการทำงานได้อย่างเต็มประสิทธิภาพ"

all_true_health = lst_health.all()
all_true_clean = lst_clean.all()

lst_problem = []

if all_true_health and all_true_clean:
    lst_problem.append(topic_text + full_capacity)

else:
    # Find the indices where lst_health is False
    false_indices_health = lst_health.index[~lst_health].tolist()
    server_problems_health = lst_device.iloc[false_indices_health]
    problem_num_health = len(server_problems_health)
    problem_num_txt_health = f"พบ {problem_num_health} รายการที่มีปัญหา คือ"
    # Convert the pandas Series to a list
    server_health = server_problems_health.tolist()
    # Join the list of strings
    server_problems_txt_health = f" {', '.join(map(str, server_health))} มีปัญหาเกี่ยวกับ"
  

    # Find the indices where lst_clean is False
    false_indices_clean = lst_clean.index[~lst_clean].tolist()
    server_problems_clean = lst_device.iloc[false_indices_clean]
    problem_num_clean = len(server_problems_clean)
    # Convert the pandas Series to a list
    server_clean = server_problems_clean.tolist()
    # Join the list of strings
    server_problems_txt_clean = f" และ {', '.join(map(str, server_clean))} "


    if all_true_health and not all_true_clean:
        lst_problem.append(topic_text + full_capacity)

    if problem_num_health == 1:
        print(topic_text + problem_num_txt_health + server_problems_txt_health)
    if problem_num_health > 1:
        lst_problem.append(topic_text + problem_num_txt_health)
        for problem in server_problems_health:
            lst_problem.append(f" - {problem} มีปัญหาเกี่ยวกับ")

    # if not all_true_clean:
    # print(problem_num_clean) 
    if all_true_health and problem_num_clean == 1:
        lst_problem.append(f"ยกเว้น {', '.join(map(str, server_clean))} ")

    if not all_true_health and problem_num_clean == 1:
        lst_problem.append(f"และ {', '.join(map(str, server_clean))} ")

    if all_true_health and  problem_num_clean > 1:
        lst_problem.append("ยกเว้น")
        for problem in server_problems_clean:
            lst_problem.append(f" - {problem}")

    if not all_true_health and  problem_num_clean > 1:
        lst_problem.append("และ")
        for problem in server_problems_clean:
            lst_problem.append(f" - {problem}")

    # Print the collected problems
for problem in lst_problem:
    print(problem)

# %%
context = {
         'health_check': health_check,
         'lst_problem' : lst_problem
        }

def health_check_hardware() :
    # print(context)
    return context


