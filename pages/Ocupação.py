import streamlit as st
import pandas as pd
import plotly.express as px
import os

def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

situacao_final = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx')).set_index('Ordem')

st.title('Ocupação do estoque')

aba1, aba2, aba3 = st.tabs(['Caixa Fechada', 'Fracionado', 'Prateleira'])

with aba1:
    'a'
    
with aba2:
    'a'
    
with aba3:
    'a'