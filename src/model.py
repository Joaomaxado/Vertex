from prophet import Prophet
from src.cleaning import cleaning
import pandas as pd
import streamlit as st  

def predicao_faturamento (df):
    df = cleaning()
    df['DATA_DIA'] = pd.to_datetime(df['DATA E HORA DO PEDIDO']).dt.date
    df_diario = df.groupby('DATA E HORA DO PEDIDO')['TOTAL PAGO PELO CLIENTE (R$)'].sum().reset_index()
    df_diario = df_diario.rename(columns={'DATA_DIA': 'ds', 'TOTAL PAGO PELO CLIENTE (R$)': 'y'})

    model = Prophet()
    model.fit(df_diario)

    future = model.make_future_dataframe(periods=7) 
    forecast = model.predict(future)

    st.subheader('Previsão dos próximos 7 dias')
    fig1 = model.plot(forecast)
    st.pyplot(fig1)

    st.subheader('Componentes da previsão')
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)
    return forecast


