# python -m venv venv
# ./venv/Scripts/activate

import streamlit as st
# import requests
import pandas as pd
import plotly.express as px
import time
import xlsxwriter
from io import BytesIO

st.set_page_config(layout='wide')

## Func

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor} milhões'

def botao_donwload(tabela_excel, nome_do_botao, nome_do_arquivo):
    # Criar um DataFrame
    df = pd.DataFrame(tabela_excel)

    # Criar um buffer de bytes para armazenar o Excel em memória
    output = BytesIO()

    # Criar um objeto Excel a partir do DataFrame
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Configurar o buffer para leitura
    output.seek(0)

    # Adicionar o botão de download
    st.download_button(label = nome_do_botao,
                        data = output.getvalue(),
                        file_name = nome_do_arquivo,
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

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

    AC = 20
    AB = 32
    AA = 27
    AM = 8
    XPE = 9

    total_enderecos_mosdulo = AC + AB + AA

    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna2:
        st.metric('Total de Curvas B e C no Flowrack:', total_curva_bc_flowrack)
        botao_donwload(curva_bc_flowrack, 'Download B e C - Flowrack', 'curva_bc_flowrack_mudar_para_prateleira.xlsx')
    with coluna1:
        number = st.number_input('Número de modulos:', step=1, min_value=1, value=6, max_value=6)
        st.write('Total de endereços utilizaveis (XPE não): ', number * total_enderecos_mosdulo)
        st.write('Total de endereços classe AA é: ', number * AA)
        st.write('Total de endereços classe AB é: ', number * AB)
        st.write('Total de endereços classe AC é: ', number * AC)
        st.write('Total de endereços liberados para antibióticos é: ', number * AM)
        st.write('Total de endereços destinados para XAROPE é: ', number * XPE)

    st.plotly_chart(fig_total_curva_frac, use_container_width=True)

st.dataframe(situacao_final)