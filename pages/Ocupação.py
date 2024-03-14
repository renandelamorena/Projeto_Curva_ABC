import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title='Ocupação',
    layout='wide',
    page_icon=':bar-chart:'
    )

def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

def refatorar_indece(df, nome_index):
    
    qnt_linha = df.shape[0] + 1

    index = [i for i in range(1, qnt_linha)]

    df.set_index(pd.Index(index), inplace=True)

    df.index.name = nome_index
    
    return df

situacao_final = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx')).set_index('Ordem')
mapa = pd.read_excel(caminho_absoluto('mapa_estoque/mapa_orientacao.xlsx')).fillna('-').astype(str)
mapa_prateleira = pd.read_excel(caminho_absoluto('mapa_estoque/mapa_prateleira_orientacao.xlsx'), sheet_name=None)
mapa_flowrack = pd.read_excel(caminho_absoluto('mapa_estoque/mapa_flowrack_orientacao.xlsx'), sheet_name=None)

def criar_mapa_de_calor_saida(coluna_endereco, coluna_saida, mapa, nome_do_grafico):
    
    if len(mapa.index) * 20 < 500:
        altura = 500
    else:
        altura = len(mapa.index) * 20

    # Agrupar por endereço e somar os dados da coluna
    coluna_x_endereço = situacao_final[[coluna_endereco, coluna_saida]].groupby([coluna_endereco]).sum().reset_index()

    # Cria um serie com os valores, para transformar em um dicionario
    coluna_x_endereço = pd.Series(coluna_x_endereço[coluna_saida].values, index = coluna_x_endereço[coluna_endereco]).to_dict()

    # Mapeia as informações da coluna com os indereços
    coluna_por_enderco = mapa.replace(coluna_x_endereço)

    # Criar o mapa de calor
    fig = go.Figure(data=go.Heatmap(
                  z=coluna_por_enderco.values, # Valores para a cor
                  x=coluna_por_enderco.columns, # Eixos X
                  y=coluna_por_enderco.index, # Eixo Y
                  colorbar_title='Saída',
                  colorscale=['LightBlue', 'DarkBlue'],
                  text=mapa,
                  texttemplate='%{text}',
                  textfont={'size':10}
                  ))

    # Ajustes finais no layout
    fig.update_layout(title_text=nome_do_grafico,
                    yaxis=dict(autorange='reversed'),
                    xaxis_showgrid=False, yaxis_showgrid=False,
                    xaxis_zeroline=False, yaxis_zeroline=False,
                    autosize=False,
                    width=7000,
                    height=altura,
                    )

    fig.update_xaxes(side='top')
    return fig

def criar_mapa_de_calor_cadastro(nome_do_grafico):
    ## Ocupação (Cadastro)

    coluna_x_endereço = situacao_final[['Ender.Cx.Fechada', 'Código']]

    if opcao_coluna == 'Produtos com estoque':
        selecao_armazenado = situacao_final['Estoque Cx'] != '0'
        qnt_com_estoque_x_endereco = coluna_x_endereço[selecao_armazenado].groupby(['Ender.Cx.Fechada']).count().reset_index()
        # Cria um serie com os valores, para transformar em um dicionario
        tipo_da_ocupacao = pd.Series(qnt_com_estoque_x_endereco['Código'].values, index = qnt_com_estoque_x_endereco['Ender.Cx.Fechada']).to_dict()

    else:
        qnt_enderecado_x_endereco = coluna_x_endereço.groupby(['Ender.Cx.Fechada']).count().reset_index()
        # Cria um serie com os valores, para transformar em um dicionario
        tipo_da_ocupacao = pd.Series(qnt_enderecado_x_endereco['Código'].values, index = qnt_enderecado_x_endereco['Ender.Cx.Fechada']).to_dict()

    # Mapeia as informações da coluna com os indereços
    coluna_por_enderco = mapa.replace(tipo_da_ocupacao)
    
    # Criar o mapa de calor
    fig = go.Figure(data=go.Heatmap(
                z=coluna_por_enderco.values, # Valores para a cor
                x=coluna_por_enderco.columns, # Eixos X
                y=coluna_por_enderco.index, # Eixo Y
                colorbar_title='Saída',
                colorscale=['LightBlue', 'DarkBlue'],
                text=mapa,
                texttemplate='%{text}',
                textfont={'size':10}
                ))

    # Ajustes finais no layout
    fig.update_layout(title_text=nome_do_grafico,
                    yaxis=dict(autorange='reversed'),
                    xaxis_showgrid=False, yaxis_showgrid=False,
                    xaxis_zeroline=False, yaxis_zeroline=False,
                    autosize=False,
                    width=2000,
                    height=1200,
                    )

    fig.update_xaxes(side='top')
    return fig

st.title('Ocupação do estoque')

aba1, aba2, aba3, aba4 = st.tabs(['Métricas', 'Caixa Fechada', 'Flowrack', 'Prateleira'])

corredores_frac = ('10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27','28', '29',)

with aba1:
    # Fracionado
    st.write('# Situação apanha fracionado')

    corredores = st.multiselect('Selecione os corredores:', list(corredores_frac),
                               ['20', '21', '22', '23', '24', '25', '26', '27','28', '29'])

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric('Total de endereços', '?')

    with col2:

        st.metric('Total de endereços bloqueados', '?')

    with col3:

        st.metric('Total de endereços utilizáveis', '?')

    # Armazenagem
    st.write('# Situação armazenagem')
    rua = st.multiselect('Selecione as ruas:', ['10', '12', '14', '15', '16', '17', '18', '100'],
                        ['10', '12', '14', '15', '16', '17', '18'])

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric('Total de porta pallets', '?')

    with col2:

        st.metric('Total de armazenagens bloqueadas', '?')

    with col3:

        st.metric('Total de armazenagens utilizáveis', '?')

with aba2:

    tipo_de_visualizacao = st.radio('Selecione o tipo de vizualização:',
                                    ['Cadastro', 'Saída'],
                                    captions=['Produtos com estoque ou vinculados por endereços', 'Saídas por atividades e vendas'])

    if tipo_de_visualizacao == 'Cadastro':
        colunas = ['Produtos vinculados',
                   'Produtos com estoque'
                   ]
        
    else:
        colunas = ['Ativ.Ressupr.Frac',
                   'Ativ.Ressupr.Cx',
                   'Ativ.Ressupr.Geral',
                   'Qtde Venda Frac',
                   'Qtde Venda Cx',
                   'Qtde Venda Geral',
                   'Dias Pedido Frac',
                   'Dias Pedido Cx',
                   'Dias Pedido Geral',
                   'Média por dia frac',
                   'Média por dia cx',
                   'Média por dia geral',
                   ]

    opcao_coluna = st.selectbox('Selecione o tipo de saída:', colunas)

    if tipo_de_visualizacao == 'Cadastro':
        chart = criar_mapa_de_calor_cadastro(f'{opcao_coluna} por Endereço de Caixa Fechada')

    else:
        chart = criar_mapa_de_calor_saida('Ender.Cx.Fechada', opcao_coluna, mapa, f'{opcao_coluna} por Endereço de Caixa Fechada')

    st.plotly_chart(chart, use_container_width=True)
    
with aba3:
    mapa_geral_flowrack = pd.concat(mapa_flowrack.values(), axis=1)

    radio_selecao_visao_flowrack = st.radio('Selecione o tipo de vizualização do flowrack:', ['Por corredor', 'Geral'])

    if radio_selecao_visao_flowrack == 'Geral':
        chart = criar_mapa_de_calor_saida('Ender.Fracionado', 'Qtde Venda Frac', mapa_geral_flowrack, 'Mapa de calor geral do flowrack')

        st.plotly_chart(chart, use_container_width=False)

    else:
        corredor = st.selectbox('Selecione o Corredor:', ('10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27','28', '29',))

        chart = criar_mapa_de_calor_saida('Ender.Fracionado', 'Qtde Venda Frac', mapa_flowrack[f'{corredor}'], f'Mapa de calor de saída do corredor {corredor}')

        st.plotly_chart(chart, use_container_width=True)
    
with aba4:
    mapa_geral_plateleiras = pd.concat(mapa_prateleira)
    refatorar_indece(mapa_geral_plateleiras, None)

    radio_selecao_visao_prateleiras = st.radio('Selecione o tipo de vizualização das prateleiras:', ['Por corredor', 'Geral'])

    if radio_selecao_visao_prateleiras == 'Geral':

        chart = criar_mapa_de_calor_saida('Ender.Fracionado', 'Qtde Venda Frac', mapa_geral_plateleiras, 'Mapa de calor geral das prateleiras')

        st.plotly_chart(chart, use_container_width=True)

    else:
        corredor = st.selectbox('Selecion o Corredor:', ('10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27','28', '29',))

        chart = criar_mapa_de_calor_saida('Ender.Fracionado', 'Qtde Venda Frac', mapa_prateleira[f'{corredor}'], f'Mapa de calor de saída do corredor {corredor}')

        st.plotly_chart(chart, use_container_width=True)
