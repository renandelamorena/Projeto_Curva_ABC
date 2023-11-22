# python -m venv venv
# ./venv/Scripts/activate



import streamlit as st
# import requests
import pandas as pd
import plotly.express as px

# Func

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor} milhões' 

st.title('Dashbord - Projeto Curva ABC')

situacao_final = pd.read_excel(r'..\tratamento_curva_abc\dados_tratados\situacao_final.xlsx').set_index('Ordem')

coluna1, coluna2 = st.columns(2)

with coluna1:
    st.metric('Total de Curvas A (Fracionado):', formata_numero(situacao_final[situacao_final['Curva Frac'] == 'A'].shape[0]))
with coluna2:
    st.metric('Total de itens cadastrados:', formata_numero(situacao_final['Código'].shape[0]))

st.dataframe(situacao_final)