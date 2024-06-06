import streamlit as st
import pandas as pd
from io import BytesIO
import os

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
                        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
    
def caminho_absoluto(caminho_relativo_com_barras_normais):

    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

def tratar_codigos(df):
            
    df['Código'] = df['Código'].astype(str)

    df['Código'] = df['Código'].str.slice(start=2)
    df['Código'] = df['Código'].str.lstrip('0')
        
st.title('Tratar Virtual')

# Caixa de upload de arquivos
uploaded_file = st.file_uploader('Escolha o arquivo "997.xlsx" para upload', type='xlsx', accept_multiple_files=False)

virtual_tratado = pd.DataFrame()
tratado = False

# Se houver upload
if uploaded_file != None:
    # Tratar virtual
    virtual = pd.read_excel(uploaded_file)
    situacao_final = pd.read_csv(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/csv/situacao_final.csv'))

    # retirar primeira coluna
    virtual = virtual.drop(['Endereço'], axis = 'columns')

    # torar a primeira linha os nomes das colanas
    virtual.columns = virtual.loc[1]

    # retirar primeira linha
    virtual = virtual.drop([0, 1], axis = 'rows')

    # tratando os codigos
    virtual.rename(columns = {'Cód.Produto' : 'Código'}, inplace = True)
    tratar_codigos(virtual)

    colunas_irrelevantes = ['Dias Venc.', 
                            'Lote Bloq.', 
                            'Res.Apanha', 
                            'Ress.Entrada', 
                            'Ress.Saída', 
                            'Ajuste Saída', 
                            'Saldo']

    virtual.drop(colunas_irrelevantes, axis = 'columns', inplace = True)

    virtual['Código'] = pd.to_numeric(virtual['Código'], downcast='float')

    produtos = situacao_final[['Código', 'Ender.Frac.', 'Ender.Cx.Fech.']].astype(str)

    todos_produtos = pd.to_numeric(produtos['Código'], downcast='float')

    produtos_virtual = pd.to_numeric(virtual['Código'], downcast='float')

    selecao = todos_produtos.isin(produtos_virtual)

    produtos = produtos[selecao]

    produtos['Código'] = pd.to_numeric(produtos['Código'], downcast='float')

    virtual = pd.merge(virtual, produtos, on = 'Código')
    virtual.sort_values(by = 'Ender.Frac.', inplace = True)

    virtual['Data Validade'] = pd.to_datetime(virtual['Data Validade'])
    virtual['Data Validade'] = virtual['Data Validade'].dt.strftime('%d/%m/%Y')

    virtual_tratado = virtual

    tratado = True

if tratado:

    st.write('### Virtual tratado:')

    st.dataframe(virtual_tratado, hide_index=True)

    botao_donwload(virtual_tratado, '⬇️ Excel', 'virtual_tratado.xlsx')
