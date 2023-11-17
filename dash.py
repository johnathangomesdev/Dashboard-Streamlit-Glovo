import numpy as np
import pandas as pd
import streamlit as st
import plotly_express as px

st.set_page_config(layout = "wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header("Dashboard dos ganhos trabalhando com a Glovo")
st.markdown("""---""")
#Lê o dataframe
df = pd.read_csv('dados_glovo.csv')
#Retira € dos valores
df["Km"] = df["Km"].str.lstrip("€ ")
#Subistitue "," por "."
df["Km"] = df["Km"].str.replace(',', '.')
#Troca o tipo de dado para float
df["Km"] = df["Km"].astype(float)
#Retira € dos valores
df["Total"] = df["Total"].str.lstrip("€ ")
#Subistitue "," por "."
df["Total"] = df["Total"].str.replace(',', '.')
#Troca o tipo de dado para float
df["Total"] = df["Total"].astype(float)
#Retira € dos valores
df["Gorjeta"] = df["Gorjeta"].str.lstrip("€ ")
#Subistitue "," por "."
df["Gorjeta"] = df["Gorjeta"].str.replace(',', '.')
#Troca o tipo de dado para float
df["Gorjeta"] = df["Gorjeta"].astype(float)
#Troca o tipo de dado para datetime
df["Date"] = pd.to_datetime(df["Dia"], dayfirst=True)
#Ordena os dados pelo "Dia"
df = df.sort_values("Date")
#Agrupa o dia aos mes
df["Dia"] = df["Date"].apply(lambda x: str(x.month) + "-" + str(x.day))
#Agrupa o mes ao ano
df["Mes"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
#Caixa de seleção
option = st.sidebar.selectbox("Como deseja filtrar os dados?",("Dias", "Meses"), index=1)
if option == "Dias":
    #Cria uma side bar com os dias como opção
    day = st.sidebar.selectbox("Dias", df["Dia"].unique())
    #Cria um dataframe filtrado pelos dias
    df_filtered = df[df["Dia"] == day]
    tempo = "Hora"
elif option == "Meses":
    #Cria uma side bar com os meses como opção
    month = st.sidebar.selectbox("Meses", df["Mes"].unique())
    #Cria um dataframe filtrado pelos dias
    df_filtered = df[df["Mes"] == month]
    tempo = "Dia"

#Separa a tela em colunas
col1, col2, col3, col4, col5 = st.columns(5)
col6 = st.columns(1)
col7, col8, col9 = st.columns(3)
#Agrupa os dias com os totais e somar
df_total = df_filtered.groupby([tempo,"Local"])[["Total"]].sum().reset_index()
#Cria um grafico o total ganho por dia
fig_total_day = px.bar(df_total, x = tempo,
                                 y = "Total",
                                 color = "Local")
#Cria um grafico com os Locais de recolha
fig_local_day = px.pie(df_filtered, values = "Total",
                                    names = "Local")
#Agrupa os dias com os totais e conta as corridas
df_call_day = df_filtered.groupby(tempo)[["Total"]].value_counts().reset_index()
#Agrupa os dias com os corridas e soma
df_call_day = df_call_day.groupby(tempo)[["count"]].sum().reset_index()
#Cria um grafico com os Locais de recolha
fig_calls_day = px.line(df_call_day, x = tempo,
                                    y = "count")
#Cria uma indicação com a soma dos valores ganhos no dia
col1.metric(label="Ganhos Totais", value= round(df_filtered["Total"].sum(),2), delta=None)
#Cria uma indicação media de ganho
col2.metric(label="Media de Ganhos", value= round(df_filtered["Total"].mean(),2), delta=None)
#Cria uma indicação com o maior ganho
col3.metric(label="Melhor Entrega", value= round(df_filtered["Total"].max(),2), delta=None)
#Cria uma indicação com o total de kms
col4.metric(label="KM Totais", value= round(df_filtered["Km"].sum(),2), delta=None)
#Cria uma indicação com o total gorjetas
col5.metric(label="Gorjetas", value= round(df_filtered["Gorjeta"].sum(),2), delta=None)
#Plota o grafico na tela
col7.markdown("""# Ganhos""")
col7.plotly_chart(fig_total_day, use_container_width = True)
col8.markdown("""# Entregas""")
col8.plotly_chart(fig_calls_day, use_container_width = True)
col9.markdown("""# Restaurantes""")
col9.plotly_chart(fig_local_day, use_container_width = True)
