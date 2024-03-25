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

armazenagens = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/datasets/armazenagens.xlsx'))
armazenagens_estoque = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/datasets/armazenagens_estoque.xlsx'))
armazenagens_estoque.fillna('-', inplace=True)

fracionado = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/datasets/fracionado.xlsx'))

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

with aba1:
    with st.expander('Fracionado'):

        st.write('# Situação apanha fracionado')
        
        corredores_frac = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27','28', '29',]
        
        selec_corredores = st.multiselect('Selecione os corredores:', corredores_frac,
                                ['20', '21', '22', '23', '24', '25', '26', '27','28', '29'])
        
        fracionado['Motivo Bloqueio'].fillna('-', inplace=True)

        selecao_fracinados = (fracionado['Situação'] != 'Inativo') & \
                            (~fracionado['Motivo Bloqueio'].str.contains('NÃO EXISTE', case=False)) & \
                            (~fracionado['Motivo Bloqueio'].str.contains('AGREGADO', case=False))

        fracionado_selec = fracionado[selecao_fracinados]
        fracionado_selec['Apelido'] = fracionado_selec['Apelido'].astype(str)

        condicao = False
        for corredor in selec_corredores:
            condicao |= fracionado_selec['Apelido'].str.startswith(corredor)

        fracionado_selec = fracionado_selec[condicao]

        total_fracionado_selec = len(fracionado_selec)

        selecao_fracionado_bloq = (fracionado_selec['Situação'] == 'Bloqueado')

        fracionado_bloq = fracionado_selec[selecao_fracionado_bloq]
        
        motivos_bloq_frac = fracionado_bloq['Motivo Bloqueio'].value_counts()
        motivos_bloq_frac = pd.DataFrame(motivos_bloq_frac).reset_index()
        motivos_bloq_frac['Motivo Bloqueio'] = motivos_bloq_frac['Motivo Bloqueio'].str.lstrip('.')
        motivos_bloq_frac.rename(columns={'count':'N° Armazenagens'}, inplace=True)

        total_fracionado_bloq = len(fracionado_bloq)

        selecao_fracionado_livre = (fracionado_selec['Situação'] == 'Liberado') | \
                                   (fracionado_selec['Situação'] == 'Bloq.Invent.')

        fracionado_livre = fracionado_selec[selecao_fracionado_livre]

        total_fracionado_livre = len(fracionado_livre)

        total_fracionado_livre_sem_cadastro = len(fracionado_livre[fracionado_livre['Função'] == 'Apanha Frac.'])

        total_fracionado_livre_cadastro = len(fracionado_livre[fracionado_livre['Função'] == 'Apanha'])

        total_fracionado_uso = len(fracionado_selec[fracionado_selec['Situação'] == 'Uso'])

        total_fracionado_utilizavel = total_fracionado_uso + total_fracionado_livre_cadastro + total_fracionado_livre_sem_cadastro

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric('Total de endereços', total_fracionado_selec)

        with col2:
            st.metric('Total de endereços bloqueados', total_fracionado_bloq)

        with col3:
            st.metric('Total de endereços utilizáveis', total_fracionado_utilizavel)
            
        col1, col2 = st.columns(2)

        with col1:
            st.write('#### Motivo do bloqueio')
            
            st.dataframe(motivos_bloq_frac)
            
        with col2:
            st.write('#### Situação das apanhas utilizáveis')
            
            frac_uso = pd.DataFrame({'Situação' : ['Liberado e castrado', 'Liberado sem cadastro', 'Em uso'],
                        'Quantidade' : [total_fracionado_livre_cadastro, total_fracionado_livre_sem_cadastro, total_fracionado_uso]})

            fig = px.pie(frac_uso, values='Quantidade', names='Situação', color='Situação', 
                        color_discrete_map={'Em uso':'lightgrey',
                                            'Liberado e castrado':'lightblue',
                                            'Liberado sem cadastro' : 'mediumblue'})

            situacao_frac_utilizaveis_graf_pizza = fig.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(situacao_frac_utilizaveis_graf_pizza, use_container_width=True)            

    with st.expander('Armazenagem'):
        
        st.write('# Situação armazenagem')

        ruas_selec = st.multiselect('Selecione as ruas:',
                                    ['010', '012', '014', '015', '016', '017', '018', '100'],
                                    ['010', '012', '014', '015', '016', '017', '018'])
        
        colunas = ['Dep.',
                    'Apelido',
                    'Situação',
                    'Motivo Bloqueio',
                    ]
        
        todas_armazenagens = armazenagens[colunas]
        todas_armazenagens['Motivo Bloqueio'].fillna('-', inplace=True)

        condicao = False
        for rua in ruas_selec:
            condicao |= todas_armazenagens['Apelido'].str.startswith(rua)

        todas_armazenagens = todas_armazenagens[condicao]
        
        selecao_porta_pallets = (todas_armazenagens['Dep.'] == 1) & \
                            (todas_armazenagens['Situação'] != 'Inativo') & \
                            (~todas_armazenagens['Motivo Bloqueio'].str.contains('NÃO EXISTE', case=False)) & \
                            (~todas_armazenagens['Motivo Bloqueio'].str.contains('AGREGADO', case=False))

        porta_pallets = todas_armazenagens[selecao_porta_pallets]
        total_porta_pallets = len(porta_pallets)
        
        selecao_porta_pallets_bloq = (porta_pallets['Situação'] == 'Bloqueado')

        porta_pallets_bloq = porta_pallets[selecao_porta_pallets_bloq]

        total_porta_pallets_bloq = len(porta_pallets_bloq)

        motivos_bloq = porta_pallets_bloq['Motivo Bloqueio'].value_counts()
        motivos_bloq = pd.DataFrame(motivos_bloq).reset_index()
        motivos_bloq['Motivo Bloqueio'] = motivos_bloq['Motivo Bloqueio'].str.lstrip('.')
        motivos_bloq.rename(columns={'count':'N° Armazenagens'}, inplace=True)
        
        selecao_porta_pallet_dif_bloq = ~porta_pallets['Apelido'].isin(porta_pallets_bloq['Apelido'])

        porta_pallet_dif_bloq = porta_pallets[selecao_porta_pallet_dif_bloq]

        total_porta_pallet_dif_bloq = len(porta_pallet_dif_bloq)
        
        situacao_utilizaveis = porta_pallet_dif_bloq['Situação'].value_counts()
        situacao_utilizaveis = pd.DataFrame(situacao_utilizaveis).reset_index()
        situacao_utilizaveis['Situação'] = situacao_utilizaveis['Situação'].str.lstrip('.')
        situacao_utilizaveis.rename(columns={'count':'Quantidade'}, inplace=True)
        
        valores_situacao_utilizaveis = situacao_utilizaveis['Situação'].values

        if 'Uso' in valores_situacao_utilizaveis:
            total_uso = situacao_utilizaveis['Quantidade'][situacao_utilizaveis['Situação'] == 'Uso'].iloc[0]
        else:
            total_uso = 0

        if 'Bloq.Invent.' in valores_situacao_utilizaveis:
            total_inv = situacao_utilizaveis['Quantidade'][situacao_utilizaveis['Situação'] == 'Bloq.Invent.'].iloc[0]
        else:
            total_inv = 0
        
        if 'lib' in valores_situacao_utilizaveis:
            total_lib = situacao_utilizaveis['Quantidade'][situacao_utilizaveis['Situação'] == 'Liberado'].iloc[0]
        else:
            total_lib = 0

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric('Total de porta-pallets', total_porta_pallets)

        with col2:

            st.metric('Total de armazenagens bloqueadas', total_porta_pallets_bloq)

        with col3:

            st.metric('Total de armazenagens utilizáveis', total_porta_pallet_dif_bloq)
                    
        with col1:
            st.write('#### Motivo do bloqueio')
            st.dataframe(motivos_bloq)

        with col2:
            st.write('#### Situação dos porta-pallets utilizáveis')
            
            arm_uso = pd.DataFrame({'Situação' : ['Liberado', 'Em uso'],
                    'Quantidade' : [(total_inv + total_lib), (total_uso)]})

            fig = px.pie(arm_uso, values='Quantidade', names='Situação', color='Situação', 
                         color_discrete_map={'Em uso':'lightgrey',
                                             'Liberado':'mediumblue'})

            situacao_utilizaveis_graf_pizza = fig.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(situacao_utilizaveis_graf_pizza, use_container_width=True)

        with col3:
            st.write('#### Situação dos porta-pallets em uso')
            
            condicao = False
            for rua in ruas_selec:
                condicao |= armazenagens_estoque['Endereço'].str.startswith(rua)

            arm_selec = armazenagens_estoque['Endereço'][condicao]

            df = pd.DataFrame()

            for endereco in armazenagens_estoque['Endereço']:
                
                if endereco in arm_selec.values:
                                        
                    i_linha_atual = armazenagens_estoque['Endereço'][armazenagens_estoque['Endereço'] == endereco].index
                
                    e_fd = armazenagens_estoque['Motivo Bloq.Ender.'].iloc[i_linha_atual[0] + 2].startswith('FD')
                
                    if e_fd:
                        tipo = 'FD'
                    else:
                        tipo = 'Outros'
                
                    linha = pd.DataFrame({'End' : [endereco], 'Tipo': [tipo]})
                    df = pd.concat([df, linha], ignore_index=True)
                                
            relacao_em_uso = pd.DataFrame(df['Tipo'].value_counts()).reset_index().rename(columns={'count' : 'Quantidade'})

            fig = px.pie(relacao_em_uso, values='Quantidade', names='Tipo', color='Tipo', 
                        color_discrete_map={'FD':'lightgrey',
                                            'Outros':'mediumblue'})

            situacao_em_uso_graf_pizza = fig.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(situacao_em_uso_graf_pizza, use_container_width=True)
    
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
        corredor = st.selectbox('Selecione o corredor do flowrack:', corredores_frac)

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
        corredor = st.selectbox('Selecione o corredor das prateleiras:', corredores_frac)

        chart = criar_mapa_de_calor_saida('Ender.Fracionado', 'Qtde Venda Frac', mapa_prateleira[f'{corredor}'], f'Mapa de calor de saída do corredor {corredor}')

        st.plotly_chart(chart, use_container_width=True)
