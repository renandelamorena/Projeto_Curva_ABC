import streamlit as st
import pandas as pd
import plotly.express as px
import time
from io import BytesIO

def botao_donwload(tabela_excel, nome_do_botao, nome_do_arquivo):
    #Criar um DataFrame
    df = pd.DataFrame(tabela_excel)

    #Criar um buffer de bytes para armazenar o Excel em memória
    output = BytesIO()

    #Criar um objeto Excel a partir do DataFrame
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    #Configurar o buffer para leitura
    output.seek(0)

    #Adicionar o botão de download
    st.download_button(label = nome_do_botao,
                        data = output.getvalue(),
                        file_name = nome_do_arquivo,
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

st.set_page_config(layout='wide')

st.title('Dados brutos')

situacao_final = pd.read_excel(r'..\tratamento_curva_abc\dados_tratados\situacao_final.xlsx').set_index('Ordem')

with st.sidebar:
    st.markdown('# Filtros')

st.dataframe(situacao_final)

