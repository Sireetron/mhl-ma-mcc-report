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


response = requests.get('https://bigdata.mwa.co.th/360-api/apis/audittrail')
data = response.json()

dataframe = pd.DataFrame(data)

df = pd.json_normalize(data,meta=['user',['title','username']])
pd.set_option('display.max_columns', 500)

unique = set(df['system.system_id'])

month = datetime.now().month -1

df['createdAt'] = pd.to_datetime(df['createdAt'], format='ISO8601')
filtered_df = df.loc[(df['createdAt'].dt.month == month)]
dataselected= filtered_df[['ip_address','source','system.system_id','system.system_name','user.title.objectId','createdAt','note']]


datauniq=dataselected .drop_duplicates(subset='ip_address')
datauniqdfil = datauniq.query("source == 'desktop'")
dataipdesk = datauniqdfil.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]#.system.system_name.transform('count')
datauniqdfil_phone = datauniq.query("source == 'phone'")
datauniqdfil_phonefil = datauniqdfil_phone.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]

dataselected.loc[(dataselected['note'] == 'login')& (dataselected['source'] == 'desktop')]
datalogindesk = dataselected.loc[(dataselected['note'] == 'login')& (dataselected['source'] == 'desktop')]
dataloginphone = dataselected.loc[(dataselected['note'] == 'login')& (dataselected['source'] == 'phone')]
datalogin_desktop = datalogindesk.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
datalogin_phone = dataloginphone.groupby('system.system_name').count().reset_index()[['system.system_name','ip_address']]
datalogin_desktop,datalogin_phone

categorical = ['IoT Platform','Admin','Water Leakage','Water Salinity','Worksite Management','Main Service']
datalogin_desktop['system.system_name'] = pd.Categorical(datalogin_desktop["system.system_name"], categories=categorical, ordered=True)
datalogin_desktop = datalogin_desktop.sort_values('system.system_name')

data_desktop = dataselected.query("source == 'desktop'")
data_phone = dataselected.query("source == 'phone'")
data_desktop_fil = data_desktop.drop_duplicates(subset='user.title.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.title.objectId']]
data_phone_fil = data_phone.drop_duplicates(subset='user.title.objectId').groupby('system.system_name').count().reset_index()[['system.system_name','user.title.objectId']]
data_desktop_fil

# # Create traces for Login
trace11 = go.Bar(
    y=datalogin_desktop['system.system_name'],
    x=datalogin_desktop['ip_address'],
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
    name='Phone2',
    orientation='h',
    marker=dict(
        color='rgba(584, 71, 80, 0.6)',
        # line=dict(color='rgba(584, 71, 80, 1.0)', width=3)
    )
    
)

# Create traces for IPS
trace21 = go.Bar(
    y=dataipdesk['system.system_name'],
    x=dataipdesk['ip_address'],
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
    name='Phone3',
    orientation='h',
    marker=dict(
        color='rgba(584, 71, 80, 0.6)',
        # line=dict(color='rgba(584, 71, 80, 1.0)', width=3)
    )
)
# Create traces for USER
trace31 = go.Bar(
    y=dataselected['system.system_name'],
    x=data_desktop_fil['user.title.objectId'],
    name='Desktop',
    orientation='h',
    marker=dict(
        color='rgba(24, 78, 139, 0.6)',
        # line=dict(color='rgba(24, 78, 139, 1.0)', width=3)
    )
)

trace32 = go.Bar(
    y=data_phone_fil['system.system_name'],
    x=data_phone_fil['user.title.objectId'],
    name='Phone',
    orientation='h',
    marker=dict(
        color='rgba(584, 71, 80, 0.6)',
        # line=dict(color='rgba(584, 71, 80, 1.0)', width=3)
    )
)

# Create subplots
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, subplot_titles=('การเข้าใช้ (ครั้ง)', 'IP เข้าใช้ (ครั้ง)','ผู้เข้าใช้ (ราย)'),)


# Add traces to subplots
fig.add_trace(trace11, row=1, col=1)
fig.add_trace(trace12, row=1, col=1)
fig.add_trace(trace21, row=1, col=2)
fig.add_trace(trace22, row=1, col=2)
fig.add_trace(trace31, row=1, col=3)
fig.add_trace(trace32, row=1, col=3)

# Hide the legend for specific traces ('y1' and 'y3' in this example)
fig.update_traces(showlegend=False, selector=dict(name='Phone2'))
fig.update_traces(showlegend=False, selector=dict(name='Desktop2'))
fig.update_traces(showlegend=False, selector=dict(name='Phone3'))
fig.update_traces(showlegend=False, selector=dict(name='Desktop3'))
# fig.update_traces(showlegend=False, selector=dict(name='Line 3'))


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
fig.write_image("./Audittrail/Image/image.png")

dataip=datauniq['ip_address'].count()
datalogin= dataselected.loc[(dataselected['note'] == 'login')]['user.title.objectId'].count()
datauser = dataselected.drop_duplicates(subset='user.title.objectId')['user.title.objectId'].count()


#writing data in each table
doc = DocxTemplate("./Audittrail/Audittrail_template.docx")
context = {
    'login': datalogin,
    'ip': dataip,
    'user': datauser,
    'image':InlineImage(doc,"./Audittrail/Image/image.png",width=Cm(16)),

    }
doc.render(context)
doc.save('./Allpart/Audittrail_edit.docx')