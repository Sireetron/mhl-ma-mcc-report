import requests
import pandas as pd
import numpy as np
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.shared import Inches
from datetime import datetime
# Import date class from datetime module
from datetime import date
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from docxtpl import DocxTemplate,InlineImage

#getdata
response = requests.get('https://bigdata.mwa.co.th/360-api/apis/audittrail')
data = response.json()
dataframe = pd.DataFrame(data)

#flatdata
df = pd.json_normalize(data,meta=['user',['title','username']])
pd.set_option('display.max_columns', 500)
df = df.loc[df['user.lastName'] != 'for_python']


#dataaselectedmonth and field
month = datetime.now().month -1
year = datetime.now().year
df['createdAt'] = pd.to_datetime(df['createdAt'], format='ISO8601')
filtered_df = df.loc[(df['createdAt'].dt.month == month) & (df['createdAt'].dt.year == year)]
dataselected= filtered_df[['ip_address','source','system.system_id','system.system_name','user.title.objectId','createdAt','note','user.objectId']]
dataselected.loc[dataselected['system.system_name']=='Water Salinity']
#replaceword
dataselected['system.system_name'] = dataselected['system.system_name'].astype(str).replace('Water Salinity','Water-Eyes')
dataselected['system.system_name'] = dataselected['system.system_name'].astype(str).replace('nan','Data Service')
dataselected['system.system_name'] = dataselected['system.system_name'].astype(str).replace('Worksite Management','CIA')
dataselected['system.system_name'] = dataselected['system.system_name'].astype(str).replace('Water Leakage','Leak Detective')

#ip
datauniq=dataselected .drop_duplicates(subset='ip_address')
datauniqdfil = datauniq.query("source == 'desktop'")
dataipdesk = datauniqdfil.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]#.note.transform('count')
datauniqdfil_phone = datauniq.query("source == 'phone'")
datauniqdfil_phonefil = datauniqdfil_phone.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
dataiptab = datauniq.query("source == 'tablet'").groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
print("IP")

#Login
datalogindesk = dataselected.loc[(dataselected['source'] == 'desktop')]
dataloginphone = dataselected.loc[(dataselected['source'] == 'phone')]
datalogintablet = dataselected.loc[(dataselected['source'] == 'tablet')]
datalogin_desktop = datalogindesk.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
datalogin_phone = dataloginphone.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
datalogin_tablet = datalogintablet.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
print("login")

#๊USER
data_desktop = dataselected.query("source == 'desktop'")
data_phone = dataselected.query("source == 'phone'")
data_desktop_fil = data_desktop.drop_duplicates(subset='user.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.objectId']]
data_phone_fil = data_phone.drop_duplicates(subset='user.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.objectId']]
datatab_fil  =  dataselected.query("source == 'tablet'").drop_duplicates(subset='user.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.objectId']]
print("USER")



data_desktop = dataselected.query("source == 'desktop'")
data_phone = dataselected.query("source == 'phone'")
data_desktop_fil = data_desktop.drop_duplicates(subset='user.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.objectId']]
data_phone_fil = data_phone.drop_duplicates(subset='user.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.objectId']]


# Create traces for Login
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
# Create traces for Login
trace11 = go.Bar(
    y=datalogin_desktop['system.system_name'],
    x=datalogin_desktop['ip_address'],
    text=datalogin_desktop['ip_address'], 
    textposition='auto',
    name='Desktop2',
    orientation='h',
    marker=dict(
        color='rgba(24, 78, 139, 0.6)',
        # line=dict(color='rgba(24, 78, 139, 1.0)', width=3)
    )
)
trace12 = go.Bar(
    y=datalogin_phone['system.system_name'],
    x=datalogin_phone['ip_address'],
    text=datalogin_phone['ip_address'], 
    textposition='auto',
    name='Phone2',
    orientation='h',
    marker=dict(
        color='rgba(584, 71, 80, 0.6)',
        # line=dict(color='rgba(584, 71, 80, 1.0)', width=3)
    )
    
)
trace13 = go.Bar(
    y=datalogin_tablet['system.system_name'],
    x=datalogin_tablet['ip_address'],
    text=datalogin_tablet['ip_address'], 
    textposition='auto',
    name='Tablet',
    orientation='h',
    marker=dict(
        color='rgba(255, 160, 122, 1 )',
        # line=dict(color='rgba(255, 160, 122, 1 )', width=3)
    )
    
)

# Create traces for IPS
trace21 = go.Bar(
    y=dataipdesk['system.system_name'],
    x=dataipdesk['ip_address'],
    text=dataipdesk['ip_address'], 
    textposition='auto',
    name='Desktop3',
    orientation='h',
    marker=dict(
        color='rgba(24, 78, 139, 0.6)',
        # line=dict(color='rgba(24, 78, 139, 1.0)', width=3)
    )
)
trace22 = go.Bar(
    y=datauniqdfil_phonefil['system.system_name'],
    x=datauniqdfil_phonefil['ip_address'],
    text=datauniqdfil_phonefil['ip_address'], 
    name='Phone3',
    textposition='auto',
    orientation='h',
    marker=dict(
        color='rgba(584, 71, 80, 0.6)',
        # line=dict(color='rgba(584, 71, 80, 1.0)', width=3)
    )
)

trace23 = go.Bar(
    y=dataiptab['system.system_name'],
    x=dataiptab['ip_address'],
    text=dataiptab['ip_address'], 
    name='Tablet2',
    textposition='auto',
    orientation='h',
     marker=dict(
        color='rgba(255, 160, 122, 1 )',
        # line=dict(color='rgba(255, 160, 122, 1 )', width=3)
    )
)
# Create traces for USER
trace31 = go.Bar(
    y=data_desktop_fil['system.system_name'],
    x=data_desktop_fil['user.objectId'],
    text=data_desktop_fil['user.objectId'], 
    name='Desktop',
    textposition='auto',
    orientation='h',
      marker=dict(
        color='rgba(24, 78, 139, 0.6)',
        # line=dict(color='rgba(24, 78, 139, 1.0)', width=3)
    )
)

trace32 = go.Bar(
    y=data_phone_fil['system.system_name'],
    x=data_phone_fil['user.objectId'],
    text=data_phone_fil['user.objectId'], 
    textposition='auto',
    name='Phone',
    orientation='h',
    marker=dict(
        color='rgba(584, 71, 80, 0.6)',
        # line=dict(color='rgba(584, 71, 80, 1.0)', width=3)
    )
)

trace33 = go.Bar(
    y=datatab_fil['system.system_name'],
    x=datatab_fil['user.objectId'],
    text=datatab_fil['user.objectId'], 
    textposition='auto',
    name='Tablet3',
    orientation='h',
    marker=dict(
        color='rgba(255, 160, 122, 1 )',
        # line=dict(color='rgba(255, 160, 122, 1 )', width=3)
    )
)

# Create subplots
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, subplot_titles=('การเข้าใช้ (ครั้ง)', 'IP เข้าใช้ (IPs)','ผู้เข้าใช้ (ราย)'))


# Add traces to subplots
fig.add_trace(trace11, row=1, col=1)
fig.add_trace(trace12, row=1, col=1)
fig.add_trace(trace13, row=1, col=1)
fig.add_trace(trace21, row=1, col=2)
fig.add_trace(trace22, row=1, col=2)
fig.add_trace(trace23, row=1, col=2)
fig.add_trace(trace31, row=1, col=3)
fig.add_trace(trace32, row=1, col=3)
fig.add_trace(trace33, row=1, col=3)

# Hide the legend for specific traces ('y1' and 'y3' in this example)
fig.update_traces(showlegend=False, selector=dict(name='Phone2'))
fig.update_traces(showlegend=False, selector=dict(name='Desktop2'))
fig.update_traces(showlegend=False, selector=dict(name='Tablet2'))
fig.update_traces(showlegend=False, selector=dict(name='Phone3'))
fig.update_traces(showlegend=False, selector=dict(name='Desktop3'))
fig.update_traces(showlegend=False, selector=dict(name='Tablet3'))


# Update layout
fig.update_layout(barmode='stack' )

# Customize the legend
fig.update_layout(
    legend=dict(
        title='อุปกรณ์',
        x=0.9,  # Adjust the x-position of the legend
        y=1.3,  # Adjust the y-position of the legend
        traceorder='normal',  # Set the order of legend items
        orientation='v',  # Set the legend orientation (horizontal)
        bgcolor='rgba(255, 255, 255, 0.5)',  # Set the legend background color with alpha
        # bordercolor='black',  # Set the legend border color
        # borderwidth=2  # Set the legend border width
    )
)

# Show figure
# fig.show()
fig.write_image(f"./sections/Audittrail/Image/image.png")

dataip=datauniq['ip_address'].count()
datalogin= dataselected['user.title.objectId'].count()
datauser = dataselected.drop_duplicates(subset='user.objectId')['user.objectId'].count()


#writing data in each table
# doc = DocxTemplate("./Template/Audittrail_template.docx")
context = {
    'login': datalogin,
    'ip': dataip,
    'user': datauser,
    # 'audittail-image':InlineImage(doc,f"./Audittrail/Image/{month}_{year}_image.png",width=Cm(16)),

    }
# doc.render(context)
# doc.save(f'./Docxfile/{month}_{year}/Audittrail_edit.docx')

def auditrail() :
    # print(context)
    return context