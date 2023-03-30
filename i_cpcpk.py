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


st.set_page_config(page_title='Capability Analysis')
st.title('_i_-Capability Analysis')
st.write(":blue[version : 00-00.CA.0323]")

#Upload XLSX File
uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    st.markdown('---')

    st.write("Select Columns to Analysis:")
    data_columns = st.multiselect("Columns", list(df.columns))

    usl = st.number_input('Input USL :')
    lsl = st.number_input('Input LSL :')

    a_lsl = lsl - 3.0
    a_usl = usl + 3.0


    for i in range(len(data_columns)):
        st.write(data_columns[i])
        chart_data = pd.DataFrame({ 'x' : np.arange(30), 
                               'y' : df[data_columns[i]]})
        c = alt.Chart(chart_data).mark_line(point=True).encode(
        x='x',
        y=alt.Y('y',scale=alt.Scale(domain=[a_lsl , a_usl]))
        )
        st.altair_chart(c, theme='streamlit', use_container_width=True)
  

    for i in range(len(data_columns)):
        x = df[data_columns[i]]
        st.write("**Cp-Cpk**", data_columns[i])
        st.write("**CP :**",Cp(x, usl, lsl))
        st.write("**CPK :**",Cpk(x, usl, lsl))
        fig = sns.displot(x, kde=True)
        st.pyplot(fig)
