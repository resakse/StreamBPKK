import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Statistik Radiologi Kesihatan", page_icon=':bar_chart:', layout='wide')
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility:hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
st.session_state['language']='ms'
fl = st.sidebar.file_uploader(':file_folder: Upload fail reten', type=(['xlsx','xls']))
if fl is not None:
    filename = fl.name
    # st.write(filename)
    nama_fail = fl
else:
    nama_fail = 'selangor-2023.xlsx'

@st.cache_data()
def get_data(namafile):
    df = pd.read_excel(io=namafile,
                       sheet_name='JAN-DIS 2023',
                       skiprows=5,
                       usecols='B:BT',
                       nrows=409,
                       engine='openpyxl'
                       )
    df.rename(columns={'Unnamed: 1': 'Negeri', 'Unnamed: 2': 'Daerah', 'Unnamed: 3': 'Klinik', 'Unnamed: 4': 'Kod PIK',
                       'Human.1': 'Over Exposure','Unnamed: 46':'Under Exposure','Unnamed: 47':'Double Exposure','Unnamed: 48':'Wrong Technique',
                       'Unnamed: 49': 'Wrong Patient', 'Unnamed: 50': 'Marker', 'Unnamed: 51': 'Collimation', 'Unnamed: 52': 'Pt. Movement',
                       'Unnamed: 53': 'Artifact', 'Unnamed: 54': 'R_Human', 'Equipment.1': 'Tube/Grid/Bucky', 'Unnamed: 56': 'Detector/Plate',
                       'Unnamed: 57': 'Equipment Artifact', 'Unnamed: 58': 'Processing','Unnamed: 59': 'R_Equip', 'Others.1': 'Lain-lain',
                       'Human': 'Over Expose (Filem)', 'Unnamed: 23': 'Under Expose (Filem)','Unnamed: 24': 'Double Exposure (Filem)',
                       'Unnamed: 25': 'Wrong Technique (Filem)','Unnamed: 26': 'Wrong Patient (Filem)', 'Unnamed: 27': 'Marker (Filem)',
                       'Unnamed: 28': 'Collimation (Filem)', 'Unnamed: 29': 'Pt. Movement (Filem)', 'Unnamed: 30':'Artifact (Filem)',
                       'Equipment': 'Equipment Artifact (Filem)','Unnamed: 33': 'Cassete/Screen','Prosessing': 'Darkroom',
                       'Unnamed: 36': 'Film Artifact','Unnamed: 37': 'Film Fogged','Unnamed: 38': 'Processor'}, inplace=True)
    df = df.dropna(subset=['Klinik'])
    return df

df = get_data(nama_fail)
# sidebar
st.sidebar.header('Filter')
negeri = st.sidebar.multiselect(
    'Pilih Negeri',
    options=df['Negeri'].unique(),
    # default='Selangor'
)
if not negeri:
    df2 = df.copy()
    df_selection = df.query(
        'Klinik.notna()'
    )
else:
    df2 = df[df['Negeri'].isin(negeri)]
    daerah = st.sidebar.multiselect(
        'Pilih Daerah',
        options=df2['Daerah'].unique(),
        default=df2['Daerah'].unique()
    )
    df_selection = df.query(
        'Negeri == @negeri & Daerah == @daerah & Klinik.notna()'
        )

# if not daerah:
#     df3 = df2.copy()
# else:
#     df3 = df2[df2['Daerah'].isin(daerah)]
#
# klinik = st.sidebar.multiselect(
#     'Pilih Klinik',
#     options=df3['Klinik'].unique(),
#     default=df3['Klinik'].unique(),
# )



st.title(':bar_chart: Statistik Radiologi Kesihatan Awam')
st.markdown('##')

jumlah_daerah = int(df_selection['Daerah'].nunique())
jumlah_klinik = int(df_selection['Klinik'].count())
jumlah_kes = int(df_selection['Jumlah'].sum())
jumlah_film = int(df_selection['Jumlah Filem Digunakan'].sum())
jumlah_filmrejek = int(df_selection['Jumlah Filem Di Rejek'].sum())
jumlah_filmtotal = jumlah_film+jumlah_filmrejek
jumlah_imej = int(df_selection['Jumlah Imej Digital/CR '].sum())
# jumlah_imej=20
jumlah_imejrejek = int(df_selection['Jumlah Imej Di Rejek'].sum())
jumlah_imejtotal = jumlah_imejrejek+jumlah_imej
# jumlah_pesakit =
kiri, tengah, kanan = st.columns(3)
kiri.metric("Jumlah Daerah", f'{jumlah_daerah} PKD')
tengah.metric("Jumlah Klinik", f'{jumlah_klinik} Klinik')
kanan.metric("Jumlah Kes", f'{jumlah_kes} Kes')

st.markdown('---')

## Graf
jkes = (
    df_selection.groupby(by=['Klinik']).sum()['Jumlah']
)
# jimej = (
#     df_selection.groupby(by=['Klinik']).sum()['Jumlah Imej Digital/CR']
# )
# jreject = (
#     df_selection.groupby(by=['Klinik']).sum()['Jumlah Imej Di Rejek']
# )

# @st.cache(hash_funcs={dict: lambda _: None}) # hash_funcs because dict can't be hashed
# def get_dic_of_fig():
#     kesbar = px.bar(jkes,
#                     x='Jumlah',
#                     y=jkes.index,
#                     title='<b>Jumlah Kes Mengikut Klinik</b>',
#                     # color_discrete_sequence=["#0083B8"] * len(jkes),
#                     template='plotly_white'
#                     )
#     kesbar.update_layout(
#         xaxis=dict(tickmode='linear')
#     )
#     return kesbar
#
# dico_of_fig = get_dic_of_fig() # this dic is cached
#
# st.plotly_chart(dico_of_fig, use_container_width=True)
if not negeri:
    tn = df_selection[['Negeri','Jumlah']].groupby(by='Negeri').sum().reset_index()
    fig = px.bar(tn, x='Negeri', y='Jumlah', text='Jumlah', template='seaborn',color='Negeri')
else:
    fig = px.bar(df_selection, x='Klinik', y='Jumlah', text= ['{:,.0f}'.format(x) for x in df_selection['Jumlah']], template='seaborn',color='Daerah')
st.plotly_chart(fig, use_container_width=True)
with st.expander('DataFrame'):
    st.dataframe(df_selection)
st.subheader('Pemeriksaan')

ex1, ex2 = st.columns((2,1))

exams = df_selection[['Dada','Abdomen','Extremiti','Rangka Kepala','Spina Vertebra','Pelvis','Skeletal Survey','Dexa','OPG']].sum()
jexams = exams.reset_index().rename(columns={'index': 'Kategori',0:'Jumlah'})
figexam = px.pie(jexams, values='Jumlah', names='Kategori', hole=0.5)
figexam.add_annotation(x=0.5, y=0.5,showarrow=False, font_size=22, text=f'{int(sum(figexam.data[0].values))} Kes')

figexam.update_traces(text=jexams['Kategori'], textposition='outside')
with ex1:
    st.plotly_chart(figexam, use_container_width=True)
with ex2:
    st.dataframe(jexams, use_container_width=True)
st.markdown('---')

#reject
st.subheader('Analisa Penolakan')
rejek_film = df_selection[['Over Expose (Filem)','Under Expose (Filem)','Double Exposure (Filem)','Wrong Technique (Filem)','Wrong Patient (Filem)',
                           'Marker (Filem)','Collimation (Filem)','Pt. Movement (Filem)','Artifact (Filem)','Equipment Artifact (Filem)','Cassete/Screen','Darkroom','Film Artifact','Film Fogged','Processor','Others']].sum()
rejek_full = df_selection[['Over Exposure','Under Exposure','Double Exposure','Wrong Technique','Wrong Patient','Marker','Collimation','Pt. Movement','Artifact',
                           'Tube/Grid/Bucky','Detector/Plate','Equipment Artifact','Processing']].sum()

fig_film = rejek_film.reset_index().rename(columns={'index': 'Kategori',0:'Jumlah'})
fig_rejek = rejek_full.reset_index().rename(columns={'index': 'Kategori',0:'Jumlah'})
fig_rejek['Jenis']='Digital'
fig_film['Jenis']='Filem'
adafilm=True
adacr=True
if fig_film.sum()['Jumlah'] == 0:
    df_reject = fig_rejek
    adafilm=False
elif fig_rejek.sum()['Jumlah'] == 0:
    df_reject = fig_film
    adacr=False
else:
    df_reject = pd.concat([fig_film, fig_rejek], axis=0)
figkatrejek = px.bar(df_reject,y='Kategori',x='Jumlah',orientation='h',text='Jumlah',color='Jenis', barmode='group')
figkatrejek.update_traces(textangle=0, textposition='outside',textfont_size=14, width=0.7,cliponaxis=False)
figkatrejek.update_yaxes(tickfont=dict(size=12))
figkatrejek.update_xaxes(tickfont=dict(size=12))
figkatrejek.update_layout(height=800)

rej1, rej2 = st.columns(2)

with rej1:
    st.plotly_chart(figkatrejek, height=800,use_container_width=True)
with rej2:
    if adacr:
        dlabels = ['Imej','Rejek']
        dvalues = [jumlah_imej,jumlah_imejrejek]
        figim = go.Figure(data=go.Pie(labels=dlabels, values=dvalues, hole=.7))
        figim.add_annotation(x=0.5, y=0.5, showarrow=False, font_size=22, text=f'{int(sum(figim.data[0].values))} Imej')
        figim.update_traces(text=dlabels, textposition='outside',marker_colors=['red','yellow'])
        if adafilm:
            figim.update_layout(height=370)
        else:
            figim.update_layout(height=600)
        st.plotly_chart(figim, use_container_width=True)
    if adafilm:
        flabels = ['Filem','Rejek']
        fvalue = [jumlah_film,jumlah_filmrejek]
        fig = go.Figure(data=go.Pie(labels=flabels, values=fvalue, hole=.7))
        fig.add_annotation(x=0.5, y=0.5, showarrow=False, font_size=22, text=f'{int(sum(fig.data[0].values))} Filem')
        fig.update_traces(text=flabels, textposition='outside')
        if adacr:
            fig.update_layout(height=370)
        st.plotly_chart(fig, use_container_width=True)