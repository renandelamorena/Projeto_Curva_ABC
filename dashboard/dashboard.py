# python -m venv venv
# ./venv/Scripts/activate

import streamlit as st
# import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

## Func

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor} milhões' 

st.title('Dashbord - Projeto Curva ABC') #Titulo

situacao_final = pd.read_excel(r'..\tratamento_curva_abc\dados_tratados\situacao_final.xlsx').set_index('Ordem')

## Tabelas

total_curva_frac = pd.DataFrame(situacao_final['Curva Frac'].value_counts()).reset_index().rename(columns={'Curva Frac':'Curva', 'count':'Total'})

## Graficos

fig_total_curva_frac = px.bar(total_curva_frac,
                              x='Curva',
                              y='Total', 
                              text_auto=True,
                              title='Total de curvas (Frac)'
                              )

## Vizualização

aba1, aba2, aba3 = st.tabs(['aba1', 'aba2', 'aba3'])

with aba1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Total de Curvas A (Fracionado):', formata_numero(situacao_final[situacao_final['Curva Frac'] == 'A'].shape[0]))
        st.plotly_chart(fig_total_curva_frac, use_container_width=True)
    with coluna2:
        st.metric('Total de itens cadastrados:', formata_numero(situacao_final['Código'].shape[0]))

st.dataframe(situacao_final)