import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os

st.set_page_config(layout='wide')

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
    
def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

# Streamlit

st.title('Dados brutos')

situacao_final = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx')).set_index('Ordem')

with st.sidebar:
    st.markdown('# Filtros')

    with st.expander('Curvas'):
        frac_toggle = st.toggle('Fracionado', value=True)
        cx_toggle = st.toggle('Caixa Fechada', value=True)
        geral_toggle = st.toggle('Geral', value=True)
    
    with st.expander('Colunas'):
        itens_permite_frac = situacao_final['Permite Frac.'].unique()
        opcoes_permite_frac = st.multiselect('Permite fracionado na caixa fechada:', itens_permite_frac, itens_permite_frac)
        
        itens_tipo = situacao_final['Tipo'].unique()
        opcoes_tipo = st.multiselect('Tipo de endereço fracionado:', itens_tipo, itens_tipo)
        
        itens_local = situacao_final['local'].unique()
        opcoes_local = st.multiselect('Tipo de local de caixa fechada:', itens_local, itens_local)
   
#Seleção curva por tipo
if frac_toggle == False:
    
    situacao_final.drop(['Curva Frac', 'Qtde Venda Frac', 'Dias Pedido Frac', 'Ativ.Ressupr.Frac', 'Média por dia frac'], axis='columns', inplace=True)

if cx_toggle == False:
    
    situacao_final.drop(['Curva Cx', 'Qtde Venda Cx', 'Dias Pedido Cx', 'Ativ.Ressupr.Cx', 'Média por dia cx'], axis='columns', inplace=True)

if geral_toggle == False:
    
    situacao_final.drop(['Curva Geral', 'Qtde Venda Geral', 'Dias Pedido Geral', 'Ativ.Ressupr.Geral', 'Média por dia geral'], axis='columns', inplace=True)

#Seleção coluna de permite fracionado na caixa fechada
selec_permite_frac = situacao_final['Permite Frac.'].isin(opcoes_permite_frac)
situacao_final = situacao_final[selec_permite_frac]

selec_tipo = situacao_final['Tipo'].isin(opcoes_tipo)
situacao_final = situacao_final[selec_tipo]

selec_local = situacao_final['local'].isin(opcoes_local)
situacao_final = situacao_final[selec_local]

st.dataframe(situacao_final)