from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.shared import Inches
import requests
import pandas as pd
import datetime
from datetime import datetime
# Import date class from datetime module
from datetime import date
import plotly.graph_objects as go
import plotly.io as pio


def slc(month, year, day, doc, InlineImage):

    # get data from api
    token = 'aw33unoyu47lxu2n3uhr7cupm'
    response = requests.get('https://ticket-api.maholan.co.th/tickets/report',headers={'token': f'{token}', 'Origin': '0.0.0.0'})
    typeticket = requests.get('https://ticket-api.maholan.co.th/tickets/types',headers={'token': f'{token}', 'Origin': '0.0.0.0'})
    typeticket = typeticket.json()
    typeticket = pd.DataFrame(typeticket)
    data = response.json()



    # Dataframe and filter other issue out
    df = pd.DataFrame(data)
    df_with_start = df.rename(columns={"created_at": "created_date"})
    _TH_FULL_MONTHS = [
        "มกราคม",
        "กุมภาพันธ์",
        "มีนาคม",
        "เมษายน",
        "พฤษภาคม",
        "มิถุนายน",
        "กรกฎาคม",
        "สิงหาคม",
        "กันยายน",
        "ตุลาคม",
        "พฤศจิกายน",
        "ธันวาคม",
    ]
    _TH_FULL_MONTHS[month-1]






    # Flat Data to Get comment in json child
    dataprep = pd.json_normalize(data, 'comments', ['ticket_type_id', 'title', 'last_activity_at', 'status', 'assigned_to', 'closed_at', 'label'])
    dataprep['create_at_month'] = pd.to_datetime(dataprep['created_at']).dt.month
    dataprep['create_at_year'] = pd.to_datetime(dataprep['created_at']).dt.year
    dataprep_fil = dataprep.merge(df_with_start, left_on='title', right_on='title')
    datafil = dataprep_fil[['label_x', 'id_y', 'created_at', 'description', 'ticket_type_id_x', 'title','last_activity_at_x', 'status_x', 'assigned_to_x', 'create_at_month', 'create_at_year', 'closed_at_x', 'created_date']]
    datafil = datafil.loc[datafil['label_x'].isnull()]






    # Get ticket at focused comment
    datafil.loc[datafil['status_x'] == 'open' ].groupby('title').first()
    ticket_fil = pd.concat([datafil.loc[datafil['status_x'] == 'closed' ].groupby('title', group_keys=False).last(),datafil.loc[datafil['status_x'] == 'open' ].groupby('title', group_keys=False).first()]).reset_index()
    data_inmonth = (ticket_fil.loc[((ticket_fil['create_at_month'] == month) & (ticket_fil['create_at_year']== year)) | ((ticket_fil['status_x'] == 'open') & (ticket_fil['create_at_month'] < month) & (ticket_fil['create_at_year']== year)) ]) #filter





    # Chage str to date time for calculating work duration
    data_inmonth['created_date_ex'] = data_inmonth['created_date'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M"))
    data_inmonth['last_activity_at_x_ex'] = data_inmonth['last_activity_at_x'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M"))
    data_inmonth['created_date_ex'] = data_inmonth['created_date_ex'].apply(lambda x: x.replace(year=year))
    data_inmonth['last_activity_at_x_ex'] = data_inmonth['last_activity_at_x_ex'].apply(lambda x: x.replace(year=year))
    data_inmonth['duration'] = data_inmonth['last_activity_at_x_ex'] - data_inmonth['created_date_ex']
    # Lookup typeticket
    data_inmonth_fil = data_inmonth.merge(typeticket, left_on='ticket_type_id_x', right_on='id')



    # Summarize data to table 1
    allticket = data_inmonth_fil.groupby(['title_y'])['title_y'].count().reset_index(name='counts')  # งานทั้งหมดรายticket
    #####
    ticketsucc = data_inmonth_fil.loc[data_inmonth_fil['status_x'] == 'closed'].groupby(['title_y'])['title_y'].count().astype(str).reset_index(name='success')  # งานที่เสร็จสิ้นรายticket
    #####
    ticketop = data_inmonth_fil.loc[data_inmonth_fil['status_x'] == 'open'].groupby(['title_y'])['title_y'].count().astype(str).reset_index(name='open')  # งานที่กำลังทำรายticket
    #####
    tickeduration = data_inmonth_fil.loc[data_inmonth_fil['status_x'] == 'closed'].groupby(['title_y'])['duration'].mean().reset_index()  # AvgdurationbyTicket
    # Merge and Recalculate working duration
    dataallticket = allticket.merge(ticketsucc, how='left').merge(ticketop, how='left').merge(tickeduration, how='left')
    dataallticket['success'] = dataallticket['success'].astype(str).replace('nan', '0')
    dataallticket['open'] = dataallticket['open'].astype(str).replace('nan', '0')
    dataallticket['duration'] = dataallticket['duration'].astype(str).replace('NaT', '0')
    dataallticket['duration'] = dataallticket['duration'].astype(str).apply(lambda x: x.replace('days', 'วัน'))





    # Summarize data to table2
    datasuccess = data_inmonth_fil.loc[data_inmonth_fil['status_x'] == 'closed'].sort_values('id_y').reset_index()
    datasuccess['duration'] = datasuccess['duration'].astype(str).apply(lambda x: x.replace('days', 'วัน'))
    # Filter and Edit Showed Data
    dataop = data_inmonth_fil.loc[data_inmonth_fil['status_x'] == 'open'].sort_values('id_y').reset_index()
    dataop['duration'] = dataop['duration'].astype(str).apply(lambda x: x.replace('days', 'วัน'))
    dataop['remain'] = 90 - dataop['duration'].apply(lambda x: x.split()[0].replace('วัน', '')).astype(int)





    # Get Report date to table header
    thaiyear = int(year)+543
    alldate = _TH_FULL_MONTHS[month-1] + " "+str(thaiyear)
    alldateandday = str(day) + " " + _TH_FULL_MONTHS[month-1] + " "+str(datetime.now().year +543)





    # Get Data to Card Summary  (amount of allticket in month)
    # get amount of ticket by status
    total_success = datasuccess['id_y'].count()
    total_op = dataop['id_y'].count()
    total_slc = data_inmonth_fil['id_y'].count()


    datasuccesslast = datasuccess.loc[datasuccess['created_date_ex'].dt.month < month]['id_y'].count()
    dataoplast = dataop.loc[dataop['created_date_ex'].dt.month < month]['id_y'].count()
    # creating chart for done work
    labels = ['success', 'operate']
    values = [total_slc-total_success, total_success]
    # Use `hole` to create a donut-like pie chart
    card_2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)]
                       )
    card_2.update_traces(
        marker=dict(colors=['#ECECEC', '#6CEE8D']), showlegend=False, textinfo='none')

    card_2.update_layout(
        autosize=False,
        margin={'l': 60, 'r': 60, 't': 20, 'b': 70},
        paper_bgcolor="#ecf7e1",
        width=400,
        height=400,
        annotations=[dict(text=total_success.astype(str)+' งาน', x=0.50, y=0.52, font_size=70, showarrow=False),
                     dict(text=(((total_success*100)/total_slc).astype(int)).astype(str)+'%', x=0.50, y=0.3, font_size=30,
                          showarrow=False),  dict(text='งานที่เสร็จสิ้น',  x=0.50, y=-0.12, showarrow=False, font_size=30),
                     dict(text=f'(งานจากเดือนที่ผ่านมา {datasuccesslast} งาน)',
                          x=0.50, y=-0.2, showarrow=False, font_size=20)
                     ],
    )
    pio.write_image(card_2, f'./sections/SLC/Image/success.png', format='png')






    # creating chart for in-progress work
    labels = ['success', 'operate']
    values = [total_slc-total_op, total_op]
    card_3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)]
                       )
    card_3.update_traces(
        marker=dict(colors=['#ECECEC', '#FFCC0D']), showlegend=False, textinfo='none')
    card_3.update_layout(
        autosize=False,
        margin={'l': 60, 'r': 60, 't': 20, 'b': 70},
        paper_bgcolor="#faedc2",
        width=400,
        height=400,
        annotations=[dict(text=total_op.astype(str)+' งาน', x=0.50, y=0.52, font_size=70, showarrow=False),
                     dict(text=(((total_op*100)/total_slc).astype(int)).astype(str) +
                          '%', x=0.50, y=0.3, font_size=30, showarrow=False),
                     dict(text='งานที่กำลังดำเนินการ',  x=0.50,
                          y=-0.12, showarrow=False, font_size=30),
                     dict(text=f'(งานจากเดือนที่ผ่านมา {dataoplast} งาน)',
                          x=0.50, y=-0.2, showarrow=False, font_size=20)
                     ],
    )
    # card_3.show()
    # card_3.write_image("./Image")/Users/mh-air/Desktop/fhon/python/mhl-ma-report/sections/SLC/Image
    pio.write_image(
        card_3, f'./sections/SLC/Image/inprogress.png', format='png')






    # writing data in each table
    deps = dataallticket['title_y'].unique()
    base_jsonall = dataallticket.to_dict('records')
    base_jsonsuccess = datasuccess.to_dict('records')
    base_jsonop = dataop.to_dict('records')
    context = {
        'project_manager': 'ณัฐพร นุตยสกุล',
        'project_status': 'MA',
        'report_month': alldate,
        'report_date': alldateandday,
        'slc_table1': base_jsonall,
        'slc_image1': InlineImage(doc, f"./sections/SLC/Image/success.png", width=Cm(5)),
        'slc_image2': InlineImage(doc, f"./sections/SLC/Image/inprogress.png", width=Cm(5)),
        'slc_table2': base_jsonsuccess,
        'slc_table3': base_jsonop,
        'slc_table3_have_no_data': len(base_jsonop) == 0,
        'slc_table2_have_no_data': len(base_jsonsuccess) == 0,
        'slc_table1_have_no_data': len(base_jsonall) == 0,
        'allticket': f'{total_slc}  งาน'

    }
    print('**********SLC Section Sucessful*****************')

    return context
