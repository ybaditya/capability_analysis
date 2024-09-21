import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


def Cp(x, usl, lsl):
    sigma = x.std()
    Cp = (usl - lsl) / (6*sigma)
    return Cp

def Cpk(x, usl, lsl):
    sigma = x.std()
    m = x.mean()
    Cpu = (usl - m) / (3*sigma)
    Cpl = (m - lsl) / (3*sigma)
    Cpk = np.min([Cpu, Cpl] )
    return Cpk


st.set_page_config(page_title='Capability Analysis Apps')
st.title('Capability Analysis Apps')
st.write(":blue[Created by : YB Aditya]")
st.markdown("---")

st.caption(
    """Capability analysis is a statistical tool used to assess the ability of a process to produce outputs that meet specified requirements or specifications. 
    A Cp or Cpk value greater than 1.33 is generally considered acceptable for a capable process. Values below 1 indicate that the process is not capable of meeting specification"""
)


#Upload XLSX File
uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    st.markdown('---')

    st.write("Select Columns to Analysis:")
    data_columns = st.multiselect("Columns", list(df.columns))


st.sidebar.link_button("Link to Multi Apps & Tools", "https://multiappsandtools.web.app/")
st.sidebar.markdown("---")

st.sidebar.header('Input Capability Parameters :')

cp_ok = st.sidebar.number_input('Input Cp Standard:',value=1.33)
cpk_ok = st.sidebar.number_input('Input Cpk Standard:',value=1.33)

st.sidebar.markdown("---")

usl = st.sidebar.number_input('Input USL :')
lsl = st.sidebar.number_input('Input LSL :')

st.sidebar.markdown("---")

cs = (usl + lsl) / 2
a_lsl = lsl - 3
a_usl = usl + 3

Analyze = st.sidebar.button('Analyze')

if Analyze:
    for i in range(len(data_columns)):
        st.markdown('---')
        st.write("Graph for",data_columns[i])
        st.write("**LSL :**",lsl,"**| CS :**",cs,"**| USL :**",usl,)
        chart_data = pd.DataFrame({ 'x' : np.arange(30),'y' : df[data_columns[i]], 'usl' : np.repeat(usl, 30), 'lsl' : np.repeat(lsl, 30)})

        line_data = alt.Chart(chart_data).mark_line(color='green',point=True).encode(
            x='x',
            y=alt.Y('y',scale=alt.Scale(domain=[a_lsl , a_usl]))
        )
        line_usl = alt.Chart(chart_data).mark_line(color='red',point=True).encode(
            x='x',
            y=alt.Y('usl',scale=alt.Scale(domain=[a_lsl , a_usl])),
        )
        line_lsl = alt.Chart(chart_data).mark_line(color='red',point=True).encode(
            x='x',
            y=alt.Y('lsl',scale=alt.Scale(domain=[a_lsl , a_usl])),
        )
        c = alt.layer(line_data, line_usl, line_lsl)
        st.altair_chart(c, theme='streamlit', use_container_width=True)

        st.markdown('---')
        x = df[data_columns[i]]
        st.write("**Capability from:**", data_columns[i])
        st.write("**Cp Result :**",Cp(x, usl, lsl))
        st.write("**Cpk Result :**",Cpk(x, usl, lsl))
        if Cp(x, usl, lsl) > cp_ok :
            st.write(":green[**Cp Status :** OK]")
        else:
            st.write(":red[**Cp Status :** NG]")
        
        if Cpk(x, usl, lsl) > cpk_ok :
            st.write(":green[**Cpk Status :** OK]")
        else:
            st.write(":red[**Cpk Status :** NG]")
        st.markdown('---')
        fig = sns.displot(x, kde=True)
        st.pyplot(fig)
