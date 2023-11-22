# python -m venv venv
# ./venv/Scripts/activate

import streamlit as st
# import requests
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout='wide')

## Func

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor} milhões' 

st.title('Dashbord - Projeto Curva ABC') ##Titulo

situacao_final = pd.read_excel(r'..\tratamento_curva_abc\dados_tratados\situacao_final.xlsx').set_index('Ordem')

## Tabelas

### Tabelas - Métricas

total_curva_frac = pd.DataFrame(situacao_final['Curva Frac'].value_counts()).reset_index().rename(columns={'Curva Frac':'Curva', 'count':'Total'})

### Tabelas - Apanha Caixa

### Tabelas - Apanha Fracionado
selecao_curva_bc_frac_errado = (situacao_final['Tipo'] == 'Flowrack') & \
                               (situacao_final['Curva Frac'].isin(['B', 'C'])) & \
                               (situacao_final['Ender.Fracionado'] > 18.000) & \
                               (situacao_final['Ender.Fracionado'] != 9010.000)
                       
curva_bc_flowrack = situacao_final[selecao_curva_bc_frac_errado]
curva_bc_flowrack = curva_bc_flowrack[['Código',
                                        'Descrição',
                                        'Curva Frac',
                                        'Qtde Venda Frac',
                                        'Dias Pedido Frac',
                                        'Ativ.Ressupr.Frac',
                                        'Estoque Frac',
                                        'Embal.',
                                        'Ender.Cx.Fechada',
                                        'Ender.Fracionado',
                                        ]]

total_curva_bc_flowrack = curva_bc_flowrack.shape[0]

## Graficos

### Graficos - Métrica

### Graficos - Apanha Caixa

### Graficos - Apanha Fracionado

fig_total_curva_frac = px.bar(total_curva_frac,
                              x='Curva',
                              y='Total', 
                              text_auto=True,
                              title='Total de curvas (Fraciondo)'
                              )

## Vizualização

aba1, aba2, aba3 = st.tabs(['Métricas', 'Apanha Caixa', 'Apanha Fracionado'])

# Métricas
with aba1:
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Total de Curvas A (Fracionado):', formata_numero(situacao_final[situacao_final['Curva Frac'] == 'A'].shape[0]))
    with coluna2:
        st.metric('Total de itens cadastrados:', formata_numero(situacao_final['Código'].shape[0]))
    with coluna3:
        st.metric('Total de Curvas B (Fracionado):', formata_numero(situacao_final[situacao_final['Curva Frac'] == 'B'].shape[0]))

#Apanha Caixa
# with aba2:


#Apanha Fracionado
with aba3:

    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Total de Curvas B e C no Flowrack:', total_curva_bc_flowrack)

    st.plotly_chart(fig_total_curva_frac, use_container_width=True)

st.dataframe(situacao_final)