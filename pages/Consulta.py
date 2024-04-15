import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os

st.set_page_config(
    page_title='Consulta',
    layout='wide',
    page_icon=':bar-chart:'
    )

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
    
def consultar_valor_situacao_final(nome_coluna):
    linha_codigo = situacao_final.loc[situacao_final['Código'] == codigo]
    coluna = linha_codigo[nome_coluna].values[0]
    return coluna

def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

situacao_final = pd.read_csv(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/csv/situacao_final.csv'))

st.title('Consultas')

coluna_1, coluna_2 = st.columns([1, 4])

with coluna_1:
    codigo = st.number_input('Código Produto:', value=None, placeholder='Escreva o Código...', step=0)
with coluna_2:

    if codigo != None and situacao_final['Código'].isin([codigo]).any():
        linha_codigo = situacao_final.loc[situacao_final['Código'] == codigo]

        descricao = linha_codigo['Descrição'].values[0]

        end_frac = linha_codigo['Ender.Fracionado'].values[0]
        end_cx = linha_codigo['Ender.Cx.Fechada'].values[0]

        flag = linha_codigo['Permite Frac.'].values[0]
        emb = linha_codigo['Embal.'].values[0]

        local_frac = 'Em teste'
        local_cx_fech = linha_codigo['local'].values[0]

    else:
        ne = 'Não encontrado'
        descricao = ne

        end_frac = ne
        end_cx = ne

        flag = ne
        emb = ne

        local_frac = 'Teste'
        local_cx_fech = ne

    st.metric('Descrição:', descricao)

coluna_1, coluna_2, coluna_3 = st.columns([5, 4, 3])

with coluna_1:    
    st.metric('End. Fracionado:', end_frac)
    st.metric('End. Cx. Fech:', end_cx)

with coluna_2:
    st.metric('Permite Frac:', flag)
    st.metric('Embalagem:', emb)

with coluna_3:
    st.metric('Local Frac:', local_frac)
    st.metric('Local Cx:', local_cx_fech)

with st.expander('Saída e Atividade'):
    
    selec = st.radio('Selecionar Tipo da Curva:', 
                        ['Frac', 'Cx', 'Geral'], 
                        index=0, 
                        horizontal=True)
    
    if codigo != None and situacao_final['Código'].isin([codigo]).any():

        if consultar_valor_situacao_final(f'Curva {selec}') != 'nan':
    
            col1, col2, col3, col4 = st.columns(4)

            col1.metric('Curva', consultar_valor_situacao_final(f'Curva {selec}'))
            col2.metric('Venda', int(consultar_valor_situacao_final(f'Qtde Venda {selec}')))
            col3.metric('Dias pedidos', int(consultar_valor_situacao_final(f'Dias Pedido {selec}')))
            col4.metric('Atv Ressup.', int(consultar_valor_situacao_final(f'Ativ.Ressupr.{selec}')))
        
        else:
            st.info(f'Sem saída {selec}')

        saida_frac = int(consultar_valor_situacao_final(f'Qtde Venda Frac'))
        saida_und_cx = int(consultar_valor_situacao_final(f'Qtde Venda Cx')) * emb

        if saida_frac != 'nan' & saida_und_cx != 'nan':

            df = pd.DataFrame({'Situação' : ['Fracionado', 'Caixa'],
                        'Quantidade' : [saida_frac, saida_und_cx]})

            fig = px.pie(df, values='Quantidade', names='Situação', color='Situação', title='Comparação do tipo de Saída em unidades', 
                    color_discrete_map={'Fracionado':'mediumblue',
                                    'Caixa':'lightgrey'})

            fig.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    else:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric('Curva', ne)
        col2.metric('Venda', ne)
        col3.metric('Dias pedidos', ne)
        col4.metric('Atv Ressup.', ne)