#python -m venv 
#./venv/Scripts/activate

# https://projeto-curva-abc.streamlit.app/

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os
from itertools import combinations
from decimal import Decimal

st.set_page_config(
    page_title='Projeto Curva ABC',
    layout='wide',
    page_icon=':bar-chart:'
    )

## Func

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor} milhões'

def botao_download(tabela_excel, nome_do_botao, nome_do_arquivo):
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

def criar_grafico_pizza(valores):
    df = pd.DataFrame({'Situação' : ['Certo', 'Errado'],
                       'Quantidade' : valores})
    
    fig = px.pie(df, values='Quantidade', names='Situação', color='Situação', 
                 color_discrete_map={'Certo':'mediumblue',
                                    'Errado':'lightgrey'})

    fig.update_traces(textposition='outside', textinfo='percent+label')
    return fig

def situacao_local(lista_locais, curva):

    selecao = df_local_not_na['local'].isin(lista_locais)
    df_local = df_local_not_na[selecao]

    #Certo
    selecao_local_certo = ((df_local['Curva Frac'].str.contains(curva))
                            )
    local_certo = df_local[selecao_local_certo]
    local_total_certo = local_certo.shape[0]

    #Errado
    selecao_local_errado = (~(df_local['Curva Frac'].str.contains(curva))
                                   )
    local_errado = df_local[selecao_local_errado]
    local_total_errado = local_errado.shape[0]

    #Total
    local_total = local_total_certo + local_total_errado

    return local_total, local_total_certo, local_total_errado, local_certo, local_errado

st.title('Dashbord - Projeto Curva ABC') #Titulo

def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

situacao_final = pd.read_csv(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/csv/situacao_final.csv'))
local_frac = pd.read_excel(caminho_absoluto('data/analise_curva_abc/local/datasets/local_apanha_frac.xlsx'))

## Barra lateral com filtros

with st.sidebar:

    st.write('# Filtros')

    AC = 20
    AB = 32
    AA = 27
    AM = 8
    XPE = 9

    total_enderecos_mosdulo = AC + AB + AA

    numero_modulos = st.number_input('Número de modulos:', step=1, min_value=1, value=5, max_value=6)

    total_enderecos_molulos = numero_modulos * total_enderecos_mosdulo
    total_enderecos_aa = numero_modulos * AA
    total_enderecos_ab = numero_modulos * AB
    total_enderecos_ac = numero_modulos * AC
    total_enderecos_am = numero_modulos * AM
    total_enderecos_xpe = numero_modulos * XPE

    st.write('## Fracionado - Endereços:')

    st.write('Utilizaveis (XPE não): ', total_enderecos_molulos)
    st.write('Classe AA é: ', total_enderecos_aa)
    st.write('Classe AB é: ', total_enderecos_ab)
    st.write('Endereços classe AC é: ', total_enderecos_ac)
    st.write('Liberados para antibióticos é: ', total_enderecos_am)
    st.write('Destinados para XAROPE é: ', total_enderecos_xpe)

## Tabelas

### Tabelas - Apanha Caixa

sem_apanha_caixa = ((situacao_final['Ender.Cx.Fech.'].isna()) &\
                    (situacao_final['Curva Frac'].notna()))
enderecar_caixa = situacao_final[sem_apanha_caixa]

df_local_not_na = situacao_final[~situacao_final['local'].isna()]
df_local_not_na.fillna('-',inplace=True)

#itens de 'ponta' no local errado
selecao_local_ponta_mudar = ((df_local_not_na['Tipo'] == 'Ponta De G') & \
                             (df_local_not_na['local'] != 'controlado') & \
                             (df_local_not_na['local'] != 'ponta') & \
                             (df_local_not_na['local'] != 'pet') & \
                             (df_local_not_na['local'] != 'pallet')
                             )
mudar_para_ponta = df_local_not_na[selecao_local_ponta_mudar]
#itens de 'ponta' no local errado
#Certo
selecao_ok_ponta_no_local_de_ponta = ((situacao_final['local'] == 'ponta') & \
                              (situacao_final['Tipo'] == 'Ponta De G')
                             )

selecao_ok_prateleira_no_local_de_ponta = ((situacao_final['local'] == 'ponta') & \
                              (situacao_final['Tipo'] == 'Prateleira') & \
                              (situacao_final['Curva Frac'] == 'A')
                             )

selecao_local_ponta_certo = selecao_ok_ponta_no_local_de_ponta | selecao_ok_prateleira_no_local_de_ponta

local_ponta_certo = situacao_final[selecao_local_ponta_certo]
local_ponta_total_certo = local_ponta_certo.shape[0]

#Errado
selecao_todos_intes_no_local_ponta = situacao_final['local'] == 'ponta'
todos_intes_no_local_ponta = situacao_final[selecao_todos_intes_no_local_ponta]

selecao_itens_errados_no_local_ponta = ~todos_intes_no_local_ponta.index.isin(local_ponta_certo.index)

local_ponta_errado = todos_intes_no_local_ponta[selecao_itens_errados_no_local_ponta]
local_ponta_total_errado = local_ponta_errado.shape[0]

#Total
local_ponta_total = local_ponta_total_certo + local_ponta_total_errado

#itens de 'prateleira' no local errado
selecao_local_prateleira_mudar = ((df_local_not_na['Curva Frac'] == 'A') & \
                                  (~df_local_not_na['Descrição'].str.contains('\(AM\)')) & \
                                  (df_local_not_na['Tipo'] == 'Prateleira') & \
                                  (df_local_not_na['local'] != 'controlado') & \
                                  (df_local_not_na['local'] != 'prateleira') & \
                                  (df_local_not_na['local'] != 'ponta') & \
                                  (df_local_not_na['local'] != 'fd') & \
                                  (df_local_not_na['local'] != 'alimento')
                                 )
mudar_para_prateleira = df_local_not_na[selecao_local_prateleira_mudar]

#No local de 'prateleira', os itens certos e errados
local_prateleira = situacao_local(['prateleira'], 'A')

#itens de 'apanha_a' no local errado
selecao_local_apanha_a_mudar = ((df_local_not_na['Curva Frac'] == 'A') & \
                             (df_local_not_na['Tipo'] == 'Flowrack') & \
                             (df_local_not_na['local'] != 'controlado') & \
                             (df_local_not_na['local'] != 'apanha_a') & \
                             (df_local_not_na['local'] != 'antibiotico') & \
                             (df_local_not_na['local'] != 'pallet') & \
                             (df_local_not_na['local'] != 'amostra') & \
                             (df_local_not_na['local'] != 'flowrack')
                             )
mudar_para_apanha_a = df_local_not_na[selecao_local_apanha_a_mudar]

#No local de 'apanha_a', os itens certos e errados
local_fechada_a = situacao_local(['pallet', 'apanha_a'], 'A')

#itens de 'apanha_b' no local errado
maiores_ressupr_frac = situacao_final.sort_values(by='Ativ.Ressupr.Frac', ascending=False)
maiores_ressupr_frac['Curva Frac'].fillna('-',inplace=True)

selecao_curvas_b_maiores_ressupr_frac = (maiores_ressupr_frac['Curva Frac'] == 'B') & \
                                        (~maiores_ressupr_frac['Descrição'].str.contains('\(AM\)')) & \
                                        (maiores_ressupr_frac['local'] != 'fd') & \
                                        (maiores_ressupr_frac['local'] != 'controlado') & \
                                        (maiores_ressupr_frac['local'] != 'pet') & \
                                        (maiores_ressupr_frac['local'] != 'alimento') & \
                                        (maiores_ressupr_frac['local'] != 'amostra') & \
                                        (maiores_ressupr_frac['Tipo'] != 'Ponta De G') & \
                                        (~maiores_ressupr_frac['local'].isna())

curvas_b_maiores_ressupr_frac = maiores_ressupr_frac[selecao_curvas_b_maiores_ressupr_frac][:400]
mudar_para_apanha_b = curvas_b_maiores_ressupr_frac[curvas_b_maiores_ressupr_frac['local'] != 'apanha_b']

#No local de 'apanha_b', os itens certos e errados
local_apanha_b = situacao_final[situacao_final['local'] == 'apanha_b']

# Certo
certo_apanha_b = local_apanha_b[local_apanha_b['Código'].isin(curvas_b_maiores_ressupr_frac['Código'])]
local_apanha_b_total_certo = certo_apanha_b.shape[0]

# Errado
errado_apanha_b = local_apanha_b[~local_apanha_b['Código'].isin(curvas_b_maiores_ressupr_frac['Código'])]
local_apanha_b_total_errado = errado_apanha_b.shape[0]

# Total
local_apanha_b_total = local_apanha_b_total_certo + local_apanha_b_total_errado

#itens de 'apanha_c' no local errado
selecao_local_apanha_c_mudar = ((maiores_ressupr_frac['Curva Frac'].str.contains('C|-')) & \
                                (~maiores_ressupr_frac['local'].isna()) & \
                                (maiores_ressupr_frac['local'] != 'controlado') & \
                                (maiores_ressupr_frac['local'] != 'fd') & \
                                (maiores_ressupr_frac['local'] != 'antibiotico') & \
                                (maiores_ressupr_frac['local'] != 'pet') & \
                                (maiores_ressupr_frac['local'] != 'amostra') & \
                                (maiores_ressupr_frac['local'] != 'alimento')
                               )

curvas_b_maiores_ressupr_frac_apos_400 = maiores_ressupr_frac[selecao_curvas_b_maiores_ressupr_frac][400:]
produtos_para_apanha_c = pd.concat([curvas_b_maiores_ressupr_frac_apos_400, maiores_ressupr_frac[selecao_local_apanha_c_mudar]])

mudar_para_apanha_c = produtos_para_apanha_c[produtos_para_apanha_c['local'] != 'apanha_c']

#No local de 'apanha_c', os itens certos e errados
local_apanha_c = situacao_final[situacao_final['local'] == 'apanha_c']

# Certo
certo_apanha_c = local_apanha_c[local_apanha_c['Código'].isin(produtos_para_apanha_c['Código'])]
local_apanha_c_total_certo = certo_apanha_c.shape[0]

# Errado
errado_apanha_c = local_apanha_c[~local_apanha_c['Código'].isin(produtos_para_apanha_c['Código'])]
local_apanha_c_total_errado = errado_apanha_c.shape[0]

# Total
local_apanha_c_total = local_apanha_c_total_certo + local_apanha_c_total_errado

#itens de 'antibiotico' no local errado
selecao_local_am_mudar = ((df_local_not_na['Descrição'].str.contains('\(AM\)')) & \
                          (df_local_not_na['local'] != 'antibiotico')
                          )
mudar_para_am = df_local_not_na[selecao_local_am_mudar]

#No local de 'antibiotico', os itens certos e errados
#Certo
selecao_local_certo_am = ((df_local_not_na['Descrição'].str.contains('\(AM\)')) & \
                          (df_local_not_na['local'] == 'antibiotico')
                          )
local_certo_am = df_local_not_na[selecao_local_certo_am]
local_total_certo_am = local_certo_am.shape[0]
#Errado
selecao_local_errado_am = (~(df_local_not_na['Descrição'].str.contains('\(AM\)')) & \
                          (df_local_not_na['local'] == 'antibiotico')
                          )
local_errado_am = df_local_not_na[selecao_local_errado_am]
local_total_errado_am = local_errado_am.shape[0]

#Total
local_total = local_total_certo_am + local_total_errado_am

### Tabelas - Apanha Fracionado

total_curva_frac = pd.DataFrame(situacao_final['Curva Frac'].value_counts()).reset_index().rename(columns={'Curva Frac':'Curva', 'count':'Total'})

#### Seleção e tabela de itens errados com o fracionado errado:

#Medicamentos curva b e c no flowrack que devem ir para a prateleira
selecao_curva_bc_frac_errado = (situacao_final['Tipo'] == 'Flowrack') & \
                               (situacao_final['Curva Frac'].isin(['B', 'C'])) & \
                               (situacao_final['Ender.Frac.'] > 18.000) & \
                               (situacao_final['Ender.Frac.'] != 9010.000)

curva_bc_flowrack = situacao_final[selecao_curva_bc_frac_errado]
curva_bc_flowrack = curva_bc_flowrack[['Código',
                                        'Descrição',
                                        'Curva Frac',
                                        'Qtde Venda Frac',
                                        'Dias Pedido Frac',
                                        'Ativ.Ressupr.Frac',
                                        'Estoque Frac',
                                        'Embal.',
                                        'Ender.Cx.Fech.',
                                        'Ender.Frac.',
                                        ]]
total_curva_bc_flowrack = curva_bc_flowrack.shape[0]

#### Seleção e tabela de itens errados (curva A no flowrack - mudar para a prateleira [itens cuja ordem é mair o do que a quantidade de endereços do flowrack])

#Itens de curva A, que são medicamentos normais
selecao_med_normal = (~situacao_final['Descrição'].str.contains('xpe|susp|sol|elixir', case=False)) & \
                     (~situacao_final['Descrição'].str.contains('SPRAYZIIN|escova|ABS|DENTAL|TOALHAS|AG ABSORVENTE|COMPRESSA|AG MULTIFRAL|AG PANTS|FITA|MASCARA|ATADURA|CERA ORTODONTICA|ESPARADRAPO', case=False)) & \
                     (situacao_final['Ender.Frac.'] > 12.999) & \
                     (situacao_final['Curva Frac'] == 'A') & \
                     (situacao_final['local'] != 'alimento')

somente_med_A = situacao_final[selecao_med_normal]
total_somente_med_A = somente_med_A.shape[0]

num_linhas_a_excluir = total_somente_med_A - total_enderecos_molulos

if total_somente_med_A > total_enderecos_molulos:
    num_total_linhas = len(somente_med_A)
    produtos_para_flowrack = somente_med_A.drop(somente_med_A.tail(num_linhas_a_excluir).index)
    linhas_excluidas = somente_med_A.tail(num_linhas_a_excluir)
else:
    produtos_para_flowrack = somente_med_A
    linhas_excluidas = somente_med_A[somente_med_A['Código'] == 0]

total_produtos_para_flowrack = produtos_para_flowrack.shape[0]

#Medicamentos curva A normais que estão na prateleira e devem ir para o flowrack
produtos_na_prateleira = situacao_final[situacao_final['Tipo'] == 'Prateleira']
selecao_curva_a_normal_prateleira_para_flowrack = (produtos_na_prateleira['Código']).isin(produtos_para_flowrack['Código'])

curva_a_normal_prateleira_para_flowrack = produtos_na_prateleira[selecao_curva_a_normal_prateleira_para_flowrack]

total_curva_a_normal_prateleira_para_flowrack = curva_a_normal_prateleira_para_flowrack.shape[0]

#Medicamentos curva A normais que estão no flowrack e devem ir para a prateleira
produtos_no_flowrack = situacao_final[situacao_final['Tipo'] == 'Flowrack']
selecao_curva_a_normal_flowrack_para_prateleira = (produtos_no_flowrack['Código']).isin(linhas_excluidas['Código'])

curva_a_normal_flowrack_para_prateleira = produtos_no_flowrack[selecao_curva_a_normal_flowrack_para_prateleira]

total_curva_a_normal_flowrack_para_prateleira = curva_a_normal_flowrack_para_prateleira.shape[0]

#### Tabela saída por modulo (Unidade)

#df somente flowrack
selecao_somente_flowrack = (situacao_final['Tipo'] == 'Flowrack') & \
                           (situacao_final['Ender.Frac.'] != 9010.000)

somente_flowrack = situacao_final[selecao_somente_flowrack]

#df somente prateira
selecao_somente_prateleira = (situacao_final['Tipo'] == 'Prateleira')

somente_prateleira = situacao_final[selecao_somente_prateleira]

# df somente ponta de gondola
selecao_somente_ponta_de_gondola = (situacao_final['Tipo'] == 'Ponta De G')

somente_ponta_de_gondola = situacao_final[selecao_somente_ponta_de_gondola]

modulos = {1:[29, 28],
           2:[27, 26],
           3:[25, 24],
           4:[23, 22],
           5:[21, 20],
           6:[19, 18],
           }

lista_modulos = [1, 2, 3, 4, 5, 6]

modulos_escolhidos = lista_modulos[:numero_modulos] #Input

corredores = []

for modulo in modulos_escolhidos:

    corredores_modulo_atual = modulos[modulo]

    corredores = corredores + corredores_modulo_atual

#Modulos dos corredores
corredor_x_modulos = {  29 : 1,
                        28 : 1,
                        27 : 2,
                        26 : 2,
                        25 : 3,
                        24 : 3,
                        23 : 4,
                        22 : 4,
                        21 : 5,
                        20 : 5,
                        19 : 6,
                        18 : 6,
                        }

#### Seleção e tabela de produtos com endereço de caixa fechada sem endereço de fracionado

com_apanha_caixa_sem_apanha_frac = ((situacao_final['Ender.Cx.Fech.'].notna()) & \
                                    (situacao_final['Ender.Frac.'].isna())
                                    )

enderecar_frac = situacao_final[com_apanha_caixa_sem_apanha_frac]

## Graficos

### Graficos - Apanha Caixa

### Graficos - Apanha Fracionado

fig_total_curva_frac = px.bar(total_curva_frac,
                              x='Curva',
                              y='Total', 
                              text_auto=True,
                              title='Total de curvas (Fraciondo)'
                              )

## Vizualização

aba1, aba2, aba3 = st.tabs(['Métricas', 'Apanha Fracionado', 'Apanha Caixa'])

#Métricas
with aba1:

    coluna1_aba1, coluna2_aba1 = st.columns(2)

    with coluna1_aba1:
        st.metric('Produtos com endereço de fracionado ineficinente:', formata_numero(total_curva_bc_flowrack + total_curva_a_normal_prateleira_para_flowrack + total_curva_a_normal_prateleira_para_flowrack))
        st.metric('Curva A "medicamento"', formata_numero(somente_med_A.shape[0]))

        coluna1, coluna2 = st.columns(2)
        with coluna1:
            st.metric('Produtos sem endereço de fracionado:', enderecar_frac.shape[0])
        with coluna2:
            botao_download(enderecar_frac, 'Download produtos para endereçar', 'enderecar_frac.xlsx')

    with coluna2_aba1:
        st.metric('Produtos com endereço de caixa fechada ineficinente:', 1)

        coluna1, coluna2 = st.columns(2)
        with coluna1:
            st.metric('Produtos sem endereço de caixa fechada:', enderecar_caixa.shape[0])
        with coluna2:
            botao_download(enderecar_caixa, 'Download produtos para endereçar', 'enderecar_caixa.xlsx')

#Apanha Fracionado
with aba2:
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Curvas B e C no Flowrack:', total_curva_bc_flowrack)
        botao_download(curva_bc_flowrack, 'Download B e C - Flowrack', 'curva_bc_flowrack_mudar_para_prateleira.xlsx')
    with coluna2:
        st.metric('Curvas A da prateleira (No flowrack)', total_curva_a_normal_flowrack_para_prateleira)
        botao_download(curva_a_normal_flowrack_para_prateleira,'Download A - Flowrack', 'curva_a_flowrack_mudar_para_prateleira.xlsx')
    with coluna3:
        st.metric('Curvas A do Flowrack (Na prateleira)', total_curva_a_normal_prateleira_para_flowrack)
        botao_download(curva_a_normal_prateleira_para_flowrack,'Download A - Prateleira', 'curva_a_prateleira_mudar_para_flowrack.xlsx')
        
    st.markdown('# Comparação das Saídas Fracionadas')
        
    selec_tipo_end_saida = st.radio('Selecione o tipo de endereço fracionado', ['Flowrack', 'Prateleira', 'Ponta De Gôndola'])
       
    somente_flowrack['Ender.Frac.'] = somente_flowrack['Ender.Frac.'].astype(str)
    somente_prateleira['Ender.Frac.'] = somente_prateleira['Ender.Frac.'].astype(str)
    somente_ponta_de_gondola['Ender.Frac.'] = somente_ponta_de_gondola['Ender.Frac.'].astype(str)

    if selec_tipo_end_saida == 'Flowrack':
        df = somente_flowrack
        
    elif selec_tipo_end_saida == 'Prateleira':
        df = somente_prateleira
        
    elif selec_tipo_end_saida == 'Ponta De Gôndola':
        df = somente_ponta_de_gondola

    #Df vazio
    tabela_saida = pd.DataFrame()

    for corredor in corredores:

        saida_corredor_atual = df[df['Ender.Frac.'].str.startswith(str(corredor))]['Qtde Venda Frac'].sum()

        qnt_item_corredor_atual = df[df['Ender.Frac.'].str.startswith(str(corredor))]['Qtde Venda Frac'].shape[0]

        nova_linha = pd.Series({'Modulo': corredor_x_modulos[corredor],
                                'Corredor': corredor,
                                'Saída': saida_corredor_atual,
                                'Quanidade itens' : qnt_item_corredor_atual
                                })

        tabela_saida = pd.concat([tabela_saida, nova_linha.to_frame().T], ignore_index=True)
        
    col1, col2 = st.columns(2)
    
    with col1:

        st.markdown('### Comparação de Saída por Módulo')  
        
        fig_saida_por_modulo = px.bar(tabela_saida,
                              x='Modulo',
                              y='Saída', 
                              text_auto=True,
                              title='Saída X Modulo'
                              )
        
        st.plotly_chart(fig_saida_por_modulo, use_container_width=True)
             
    with col2:
    
        st.markdown('### Comparação de Saída por Corredor')
           
        fig_saida_por_corredor = px.bar(tabela_saida,
                                    x='Corredor',
                                    y='Saída', 
                                    text_auto=True,
                                    title='Saída X Corredor'
                                    )
        
        st.plotly_chart(fig_saida_por_corredor, use_container_width=True)
    
    st.markdown('# Divisão das Saídas Fracionadas')

    with st.expander('Flowrack'):
        coluna1, coluna2 = st.columns(2)
        with coluna1:

            st.markdown('# Filtrar Saída pela classe')

            #Filtro por local
            classes_frac = ['AA', 'AB', 'AC', 'XPE']
            selecao_locais = st.selectbox('Selecione o local:', classes_frac)

            #Tabela de saida por classe
            produto_flowrack = somente_flowrack[['Ender.Frac.', 'Código', 'Qtde Venda Frac']]
            local_flowrack = local_frac
            local_flowrack['Ender.Frac.'] = local_flowrack['Ender.Frac.'].astype(str)
            saida_por_local_flowrack = pd.merge(local_flowrack, produto_flowrack, on='Ender.Frac.',  how = 'left')

            #Selecionar o(s) modulo(s)
            selecao_modulo = saida_por_local_flowrack['modulo'].isin(modulos_escolhidos)
            saida_por_local_flowrack_modulo = saida_por_local_flowrack[selecao_modulo]

            #Selecionar o(s) local(is)
            selecao_local = saida_por_local_flowrack_modulo['local'] == selecao_locais
            tabela_saida_por_local = saida_por_local_flowrack_modulo[selecao_local]    

            fig_saida_por_classe = px.bar(tabela_saida_por_local,
                                x='modulo',
                                y='Qtde Venda Frac',
                                text_auto=True,
                                title='Saída X Local'
                                )
            
            # print(tabela_saida_por_local[['Código', 'modulo', 'Qtde Venda Frac']])
            
            st.plotly_chart(fig_saida_por_classe, use_container_width=True)
            
        with coluna2:

            selecao_local_flowrack = (local_frac['local'] == selecao_locais)
            local_flowrakc_selecionado = local_frac[selecao_local_flowrack]
            enderecos_local_flowrack_selecionado = local_flowrakc_selecionado['Ender.Frac.'].astype(float)

            def saida_flowrack_no_modulo_pela_classe(corredores):

                selecao_flowrack_corredordes = ((situacao_final['Tipo'] == 'Flowrack') & \
                                                (situacao_final['Ender.Frac.'].astype(str).str.startswith(str(corredores[0])) | \
                                                situacao_final['Ender.Frac.'].astype(str).str.startswith(str(corredores[1]))
                                                )
                                                )
                
                flowrack_do_modulo = situacao_final[selecao_flowrack_corredordes]

                selecao_flowrack_modulo_X_classe = flowrack_do_modulo['Ender.Frac.'].isin(enderecos_local_flowrack_selecionado)

                flowrack_modulo_X_classe = flowrack_do_modulo[selecao_flowrack_modulo_X_classe]

                saida_flowrack_modulo_classe = flowrack_modulo_X_classe['Qtde Venda Frac'].tolist()

                return saida_flowrack_modulo_classe, flowrack_modulo_X_classe
            
            saida_dos_modulos = [saida_flowrack_no_modulo_pela_classe(modulos[1])[0],
                                saida_flowrack_no_modulo_pela_classe(modulos[2])[0],
                                saida_flowrack_no_modulo_pela_classe(modulos[3])[0],
                                saida_flowrack_no_modulo_pela_classe(modulos[4])[0],
                                saida_flowrack_no_modulo_pela_classe(modulos[5])[0],
                                saida_flowrack_no_modulo_pela_classe(modulos[6])[0],
                                ]

            saida_dos_modulos = saida_dos_modulos[:numero_modulos]

            soma_total = 0
            for lista in saida_dos_modulos:
                for valor in lista:
                    soma_total += valor
                    
            media_saida_modulo = round(soma_total / len(saida_dos_modulos), 1)

            saidas_list = []
            for i in range(len(saida_dos_modulos)):
                sum_lista_i = round(sum(saida_dos_modulos[i]), 1)
                saida_dif_sum_lista_i = round((sum_lista_i - media_saida_modulo), 1)
                saidas_list.append(Decimal(str(saida_dif_sum_lista_i)))
            
            st.markdown('# Situação da classe')
            
            st.write(f' #### Média definida para cada módulo: {formata_numero(round(media_saida_modulo))}')
                       
            with st.container(border=True):
                st.metric('1° Módulo', formata_numero(sum(saida_dos_modulos[0])), (str(saidas_list[0])))
                st.metric('2° Módulo', formata_numero(sum(saida_dos_modulos[1])), str(saidas_list[1]))
                st.metric('3° Módulo', formata_numero(sum(saida_dos_modulos[2])), str(saidas_list[2]))
                st.metric('4° Módulo', formata_numero(sum(saida_dos_modulos[3])), str(saidas_list[3]))
                st.metric('5° Módulo', formata_numero(sum(saida_dos_modulos[4])), str(saidas_list[4]))
                
        def encontrar_combinacao(lista, alvo):
            for i in range(1, len(lista) + 1):
                for comb in combinations(lista, i):
                    if sum(comb) == alvo:
                        return list(comb)
            return None
        
        st.write('# Realocar produtos')

        # Lista de números
        modulo_escolhido = st.selectbox('Selecione o modulo:', tuple(lista_modulos))
        modulo = saida_dos_modulos[modulo_escolhido - 1]

        # Número alvo
        total_saida = st.number_input('Insira o total de saída que deseja realocar:', value=0, step=1)
        total_de_saida_desejada = total_saida

        if total_de_saida_desejada != 0:
            # Encontrar combinação
            comb = encontrar_combinacao(modulo, total_de_saida_desejada)

            modulo_e_classe_selc = saida_flowrack_no_modulo_pela_classe(modulos[modulo_escolhido])[1]

            if comb:
                st.write('Itens para realocamento:')
                i = modulo_e_classe_selc[modulo_e_classe_selc['Qtde Venda Frac'].isin(comb)]['Qtde Venda Frac'].drop_duplicates().index
                realocar = modulo_e_classe_selc[modulo_e_classe_selc.index.isin(i)]
                st.dataframe(realocar)
                
            else:
                st.write("Não foi possível encontrar uma combinação.")

        st.write('# Realocar Classes - Flowrack')

        produtos_para_classe_AA = produtos_para_flowrack[0 : (total_enderecos_aa)]
        produtos_para_classe_AB = produtos_para_flowrack[total_enderecos_aa: (total_enderecos_aa + total_enderecos_ab)]
        produtos_para_classe_AC = produtos_para_flowrack[(total_enderecos_aa + total_enderecos_ab) : (total_enderecos_aa + total_enderecos_ab + total_enderecos_ac)]

        def produtos_para_realocar_de_classe(local, produtos_destinados_para_local):

            selecao_do_local = local_frac['local'] == local

            endereco_local_selec = local_frac[selecao_do_local]['Ender.Frac.']

            selecao_produtos_enderecado_no_local_selec = produtos_destinados_para_local['Ender.Frac.'].astype(str).isin(endereco_local_selec)

            produtos_enderecado_no_local_selec_errado = produtos_destinados_para_local[~selecao_produtos_enderecado_no_local_selec]

            return produtos_enderecado_no_local_selec_errado

        colocar_local_AA = produtos_para_realocar_de_classe('AA', produtos_para_classe_AA)
        total_colocar_local_AA = len(colocar_local_AA)

        colocar_local_AB = produtos_para_realocar_de_classe('AB', produtos_para_classe_AB)
        total_colocar_local_AB = len(colocar_local_AB)

        colocar_local_AC = produtos_para_realocar_de_classe('AC', produtos_para_classe_AC)
        total_colocar_local_AC = len(colocar_local_AC)

        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            st.metric('Realocar para Classe AA no Flowrack', total_colocar_local_AA)
            botao_download(colocar_local_AA, 'Download Realocar no Flowrack - AA', 'realocar_para_classe_AA.xlsx')
        with coluna2:
            st.metric('Realocar para Classe AB no Flowrack', total_colocar_local_AB)
            botao_download(colocar_local_AB, 'Download Realocar no Flowrack - AB', 'realocar_para_classe_AB.xlsx')
        with coluna3:
            st.metric('Realocar para Classe AC no Flowrack', total_colocar_local_AC)
            botao_download(colocar_local_AC, 'Download Realocar no Flowrack - AC', 'realocar_para_classe_AC.xlsx')
            
    with st.expander('Prateleiras'):
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('# Filtrar Saída por Pratelerias')

            #Filtro por tipo das prateleiras
            final_modulo = ['21', '22', '25', '26']
            comeco_modulo = ['20', '23', '24', '27']
            
            tipo_das_prateleiras = st.radio('Seleciona e tipo da prateleira:', ['Final dos Módulos', 'Começo dos Módulos'])
            
            if tipo_das_prateleiras == 'Final dos Módulos':
                tipo_prateleira_selec = final_modulo
            else:
                tipo_prateleira_selec = comeco_modulo

            #Tabela de saida por prateleira(final/comeco)
            produto_ponta = somente_prateleira[['Ender.Frac.', 'Código', 'Qtde Venda Frac']]
                        
            selecao_do_tipo_de_prateleira = produto_ponta['Ender.Frac.'].apply(lambda x: any(x.startswith(item) for item in tipo_prateleira_selec))
            saida_por_pratileira_selecionada = produto_ponta[selecao_do_tipo_de_prateleira]
            
            def encontrar_modulo(endereco):
                
                dois_primeiros_digitos = int(str(endereco)[:2])
                
                for modulo, numeros in modulos.items():
                    if dois_primeiros_digitos in numeros:
                        return modulo
                return "Erro"

            saida_por_pratileira_selecionada['modulo'] = saida_por_pratileira_selecionada['Ender.Frac.'].apply(encontrar_modulo)
                
            #Selecionar o(s) modulo(s)
            selecao_modulo = saida_por_pratileira_selecionada['modulo'].isin(modulos_escolhidos)
            saida_por_pratileira_selecionada_modulo = saida_por_pratileira_selecionada[selecao_modulo]
                        
            fig_saida_por_classe = px.bar(saida_por_pratileira_selecionada_modulo,
                    x='modulo',
                    y='Qtde Venda Frac',
                    text_auto=True,
                    title='Saída X Modulo das prateleiras Selecionadas'
                    )
            
            st.plotly_chart(fig_saida_por_classe, use_container_width=True)
        
        with col2:
            st.markdown('# Situação das Prateleiras')
                        
            saida_da_prateleira = saida_por_pratileira_selecionada_modulo['Qtde Venda Frac']
            
            media_saida_prateleira_por_modulo = round(saida_da_prateleira.sum() / 4)
            
            dif_modulos_prateleiras = [saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 2].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 3].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 4].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 5].sum() - media_saida_prateleira_por_modulo]
            
            st.write(f'#### Média definida para cada módulo: {formata_numero(media_saida_prateleira_por_modulo)}')
                       
            with st.container(border=True):
                st.metric('2° Módulo', formata_numero(saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 2].sum()), dif_modulos_prateleiras[0])
                st.metric('3° Módulo', formata_numero(saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 3].sum()), dif_modulos_prateleiras[1])
                st.metric('4° Módulo', formata_numero(saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 4].sum()), dif_modulos_prateleiras[2])
                st.metric('5° Módulo', formata_numero(saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == 5].sum()), dif_modulos_prateleiras[3])
                
        st.write('# Realocar produtos')
        
        # Lista de números
        modulo_escolhido = st.selectbox('Selecione o modulo:', (2, 3, 4, 5))
        modulo = saida_da_prateleira[saida_por_pratileira_selecionada_modulo['modulo'] == modulo_escolhido]

        # Número alvo
        total_saida_prateleira = st.number_input('Insira o total de saída que deseja realocar nas prateleiras:', value=0, step=1)
        total_de_saida_desejada = total_saida_prateleira

        if total_de_saida_desejada != 0:
            # Encontrar combinação
            comb = encontrar_combinacao(modulo, total_de_saida_desejada)

            if comb:
                st.write('Itens para realocamento:')
                i = saida_por_pratileira_selecionada_modulo[saida_por_pratileira_selecionada_modulo['Qtde Venda Frac'].isin(comb)]['Qtde Venda Frac'].drop_duplicates().index
                realocar = saida_por_pratileira_selecionada_modulo[saida_por_pratileira_selecionada_modulo.index.isin(i)]
                st.dataframe(realocar)
                
            else:
                st.write("Não foi possível encontrar uma combinação.")

        selecao_dividir = ((situacao_final['Tipo'] == 'Prateleira') & \
                        (situacao_final['Ender.Frac.'] > 20) & \
                        (situacao_final['Ender.Frac.'] < 28)
                        )

        prateleira_para_dividir = situacao_final[selecao_dividir]

        selecao_nao_e_end_do_meio = ~((prateleira_para_dividir['Ender.Frac.'] > 21.580) & \
                                    (prateleira_para_dividir['Ender.Frac.'] < 22) | \
                                    (prateleira_para_dividir['Ender.Frac.'] > 22.580) & \
                                    (prateleira_para_dividir['Ender.Frac.'] < 23)
                                    )

        prateleira_para_dividir = prateleira_para_dividir[selecao_nao_e_end_do_meio]

        def comeca_com(df, corredor):
            return df['Ender.Frac.'].astype(str).str.startswith(corredor)

        # Mais saida
        ir_para_final_modulo = prateleira_para_dividir[0:720]

        selecao_trocar_para_o_final = ((comeca_com(ir_para_final_modulo, '20')) | \
                                    (comeca_com(ir_para_final_modulo, '23')) | \
                                    (comeca_com(ir_para_final_modulo, '24')) | \
                                    (comeca_com(ir_para_final_modulo, '27'))
                                    )

        colocar_nos_corredores_21_22_25_26 = ir_para_final_modulo[selecao_trocar_para_o_final]

        ir_para_comeco_modulo = prateleira_para_dividir[720:]

        selecao_trocar_para_o_comeco = ((comeca_com(ir_para_comeco_modulo, '21')) | \
                                        (comeca_com(ir_para_comeco_modulo, '22')) | \
                                        (comeca_com(ir_para_comeco_modulo, '25')) | \
                                        (comeca_com(ir_para_comeco_modulo, '26'))
                                        )

        colocar_nos_corredores_20_23_24_27 = ir_para_comeco_modulo[selecao_trocar_para_o_comeco]

        st.write('# Realocar Prateleiras')

        col1, col2 = st.columns(2)

        with col1:
            st.metric('Realocar para os corredores 20, 23, 24, 27 (Menor saída).', len(colocar_nos_corredores_20_23_24_27))
            botao_download(colocar_nos_corredores_20_23_24_27, '⬇️ Excel', 'colocar_nos_corredores_20_23_24_27.xlsx')

        with col2:
            st.metric('Realocar para os corredores 21, 22, 25, 26 (Maior saída).', len(colocar_nos_corredores_21_22_25_26))
            botao_download(colocar_nos_corredores_21_22_25_26, '⬇️ Excel', 'colocar_nos_corredores_21_22_25_26.xlsx')
        
    with st.expander('Ponta de Gôndola'):
                
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('# Saída por Ponta De Gôndola')

            #Tabela de saida por prateleira(final/comeco)
            produto_ponta = somente_ponta_de_gondola[['Ender.Frac.', 'Código', 'Qtde Venda Frac']]
            
            modulos_ponta = {1:[29],
                            2:[28, 27],
                            3:[26, 25],
                            4:[23, 22],
                            5:[21],
                            6:[20, 19],
                            }
            
            def encontrar_modulo(endereco):
                
                dois_primeiros_digitos = int(str(endereco)[:2])
                
                for modulo, numeros in modulos_ponta.items():
                    if dois_primeiros_digitos in numeros:
                        return modulo
                return "Erro"

            produto_ponta['modulo'] = produto_ponta['Ender.Frac.'].apply(encontrar_modulo)
                
            #Selecionar o(s) modulo(s)
            selecao_modulo = produto_ponta['modulo'].isin(modulos_escolhidos)
            produto_ponta_modulo = produto_ponta[selecao_modulo]
                        
            fig_saida_por_classe = px.bar(produto_ponta_modulo,
                    x='modulo',
                    y='Qtde Venda Frac',
                    text_auto=True,
                    title='Saída X Modulo das prateleiras Selecionadas'
                    )
            
            st.plotly_chart(fig_saida_por_classe, use_container_width=True)
        
        with col2:
            st.markdown('# Situação das Pontas De Gôndola')
                        
            saida_da_prateleira = produto_ponta_modulo['Qtde Venda Frac']
            
            media_saida_prateleira_por_modulo = round(saida_da_prateleira.sum() / 5)
            
            dif_modulos_prateleiras = [saida_da_prateleira[produto_ponta_modulo['modulo'] == 1].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[produto_ponta_modulo['modulo'] == 2].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[produto_ponta_modulo['modulo'] == 3].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[produto_ponta_modulo['modulo'] == 4].sum() - media_saida_prateleira_por_modulo,
                                        saida_da_prateleira[produto_ponta_modulo['modulo'] == 5].sum() - media_saida_prateleira_por_modulo]
            
            st.write(f'#### Média definida para cada módulo: {formata_numero(media_saida_prateleira_por_modulo)}')
                       
            with st.container(border=True):
                st.metric('1° Módulo', formata_numero(saida_da_prateleira[produto_ponta_modulo['modulo'] == 1].sum()), dif_modulos_prateleiras[0])
                st.metric('2° Módulo', formata_numero(saida_da_prateleira[produto_ponta_modulo['modulo'] == 2].sum()), dif_modulos_prateleiras[1])
                st.metric('3° Módulo', formata_numero(saida_da_prateleira[produto_ponta_modulo['modulo'] == 3].sum()), dif_modulos_prateleiras[2])
                st.metric('4° Módulo', formata_numero(saida_da_prateleira[produto_ponta_modulo['modulo'] == 4].sum()), dif_modulos_prateleiras[3])
                st.metric('5° Módulo', formata_numero(saida_da_prateleira[produto_ponta_modulo['modulo'] == 5].sum()), dif_modulos_prateleiras[4])
                
        st.write('# Realocar produtos')
        
        # Lista de números
        modulo_escolhido = st.selectbox('Selecione o modulo para as pontas:', (1, 2, 3, 4, 5))
        modulo = saida_da_prateleira[produto_ponta_modulo['modulo'] == modulo_escolhido]

        # Número alvo
        total_saida_prateleira = st.number_input('Insira o total de saída que deseja realocar nas pontas:', value=0, step=1)
        total_de_saida_desejada = total_saida_prateleira

        if total_de_saida_desejada != 0:
            # Encontrar combinação
            comb = encontrar_combinacao(modulo, total_de_saida_desejada)

            if comb:
                st.write('Itens para realocamento:')
                i = produto_ponta_modulo[produto_ponta_modulo['Qtde Venda Frac'].isin(comb)]['Qtde Venda Frac'].drop_duplicates().index
                realocar = produto_ponta_modulo[produto_ponta_modulo.index.isin(i)]
                st.dataframe(realocar)
                
            else:
                st.write("Não foi possível encontrar uma combinação.")

    st.write('---')

    with st.expander('Rowa'):

        st.write('# Realocar Rowa')

        col1, col2, col3 = st.columns(3)

        with col1:
            selecao_curva_A_e_B_no_robo = ((situacao_final['Curva Frac'].str.contains('A|B')) & \
                               (situacao_final['Ender.Frac.'] == 9010)
                               )

            itens_para_retirar_do_robo = situacao_final[selecao_curva_A_e_B_no_robo][['Código', 'Descrição']]

            st.metric('Itens para retirar do Rowa (Maior saída).', len(itens_para_retirar_do_robo))

            botao_download(itens_para_retirar_do_robo, '⬇️ Excel', 'itens_para_retirar_do_robo.xlsx')

        with col3:

            itens_verificados = st.text_area('Códigos de itens verificados:')

            if itens_verificados != '':
                lines = itens_verificados.split('\n')

                numbers = [float(line.replace('.', '').replace(',', '.')) for line in lines]

                itens_verificados = pd.DataFrame(numbers, columns=['Código'])

                st.dataframe(itens_verificados, hide_index=True)

            else:
                itens_verificados = pd.DataFrame(columns=['Código'])

        with col2:

            descricao_nao_cabe = 'FD|WHEY|ESCOVA|ML|ESPARADRAPO|ZIIN ZIIN|CRISP BAR|DARK BAR|DIET WEEK|KIT|AGUA|VO2|FITA|1KG|900G|EVORA|APARELHO|PRESERVATIVO|MIX|CHUPETA|PACK|AGULHA|INALADOR'
            codigos_que_nao_cabem_robo = pd.read_excel(caminho_absoluto('codigos_que_nao_cabem_robo.xlsx'))
            codigos_que_nao_cabem_robo = codigos_que_nao_cabem_robo['Código'].astype(int)

            selecao_curva_C_fora_do_robo = ((situacao_final['Curva Frac'].str.contains('C')) & \
                                            (situacao_final['Ender.Frac.'] != 9010) & \
                                            (situacao_final['Ender.Frac.'] > 20) & \
                                            (situacao_final['Estoque Frac'] > 0) & \
                                            (~situacao_final['Descrição'].str.contains(descricao_nao_cabe, case=True)) & \
                                            (~situacao_final['Código'].isin(codigos_que_nao_cabem_robo)) & \
                                            (~situacao_final['Código'].isin(itens_verificados['Código']))
                                            )

            itens_para_verificar_se_cabem_no_robo = situacao_final[selecao_curva_C_fora_do_robo]
            itens_para_verificar_se_cabem_no_robo = itens_para_verificar_se_cabem_no_robo[['Código', 'Descrição', 'Ender.Frac.']]

            st.metric('Itens para verificar se cabem no Rowa (Menor saída).', len(itens_para_verificar_se_cabem_no_robo))
            botao_download(itens_para_verificar_se_cabem_no_robo, '⬇️ Excel', 'itens_para_verificar_se_cabem_no_robo.xlsx')
            st.dataframe(itens_para_verificar_se_cabem_no_robo, hide_index=True)
            
#Apanha Caixa

with aba3:
    locais = ['Ponta', 'Prateleira', 'Apanha A', 'Apanha B', 'Apanha C', 'Apanha AM']

    dfs_locais_valores = {'Ponta' : [local_ponta_total_certo, local_ponta_total_errado],
                        'Prateleira' : [local_prateleira[1], local_prateleira[2]],
                        'Apanha A' : [local_fechada_a[1], local_fechada_a[2]],
                        'Apanha B' : [local_apanha_b_total_certo, local_apanha_b_total_errado],
                        'Apanha C' : [local_apanha_c_total_certo, local_apanha_c_total_errado],
                        'Apanha AM' : [local_total_certo_am, local_total_errado_am],
                        }
    dfs_locais_tabelas = {'Ponta' : [local_ponta_certo, local_ponta_errado],
                        'Prateleira' : [local_prateleira[3], local_prateleira[4]],
                        'Apanha A' : [local_fechada_a[3], local_fechada_a[4]],
                        'Apanha B' : [certo_apanha_b, errado_apanha_b],
                        'Apanha C' : [certo_apanha_c, errado_apanha_c],
                        'Apanha AM' : [local_certo_am, local_errado_am],
                        }

    st.write('## Situação por local')

    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.session_state.horizontal = False
        opcao_local_grafico = st.radio('Selecione o local:', locais)

        with st.popover(f'Itens CERTOS no local de {opcao_local_grafico}'):

            df_local_selec_certo = dfs_locais_tabelas[opcao_local_grafico][0][['Código', 'Descrição', 'Curva Frac', 'Qtde Venda Frac', 'Ender.Cx.Fech.']].sort_values(by='Ender.Cx.Fech.')

            botao_download(df_local_selec_certo, 'Baixar "Itens Certos"', f'itens_certos_local_{opcao_local_grafico}.xlsx')
            st.dataframe(df_local_selec_certo, use_container_width=True, hide_index=True)

        with st.popover(f'Itens ERRADOS no local de {opcao_local_grafico}'):

            df_local_selec_errado = dfs_locais_tabelas[opcao_local_grafico][1][['Código', 'Descrição', 'Curva Frac', 'Qtde Venda Frac', 'Ender.Cx.Fech.']].sort_values(by='Ender.Cx.Fech.')

            botao_download(df_local_selec_errado, 'Baixar "Itens Errados"', f'itens_errados_local_{opcao_local_grafico}.xlsx')
            st.dataframe(df_local_selec_errado, use_container_width=True, hide_index=True)

    with coluna2:
        chart = criar_grafico_pizza(dfs_locais_valores[opcao_local_grafico])
        st.plotly_chart(chart, use_container_width=True)

    #Itens nos locais errados
    with st.expander('Itens para colocar no local:'):
        #Selecionar o df
        dfs_locais_errados = {'Ponta' : mudar_para_ponta,
                              'Prateleira' : mudar_para_prateleira,
                              'Apanha A' : mudar_para_apanha_a,
                              'Apanha B' : mudar_para_apanha_b,
                              'Apanha C' : mudar_para_apanha_c,
                              'Apanha AM' : mudar_para_am
                              }

        st.session_state.horizontal = True
        local_selec = st.radio('Selecione o local:', locais,
                                horizontal = True)
        
        df_selec = dfs_locais_errados[local_selec]
        total_trocar = df_selec.shape[0]

        st.metric('Total:', total_trocar)

        df_selec = df_selec[['Código', 'Descrição', 'Curva Frac', 'Qtde Venda Frac', 'Ender.Cx.Fech.']].sort_values(by='Ender.Cx.Fech.')

        botao_download(df_selec, 'Baixar tabela', f'trocal_local_para_{local_selec}.xlsx')
        st.dataframe(df_selec, use_container_width=False, hide_index=True)
        
with aba2:
        
    st.write('# Realocar Fracionado por saídas')

    on = st.toggle('Realocar')

    if on:

        tipo_divisao = st.selectbox('Selecione o por onde deseja realocar:', 
                                    ('Flowrack na classe selecionada acima',
                                    'Prateleiras da orientação do módulo selecionado acima',
                                    ))

        if tipo_divisao == 'Flowrack na classe selecionada acima':
            df = tabela_saida_por_local
        else:
            df = saida_por_pratileira_selecionada_modulo

        # Calculando a média de saída desejada
        media_saida = df['Qtde Venda Frac'].sum() / df['modulo'].nunique()

        # Calculando a variação permitida de 2% para mais ou para menos
        variação_permitida = media_saida * 0.02

        # Calculando a soma de saída por módulo
        soma_saida_por_modulo = df.groupby('modulo')['Qtde Venda Frac'].sum()

        # Identificando os módulos que estão fora da faixa de tolerância
        fora_da_faixa = soma_saida_por_modulo[(soma_saida_por_modulo < media_saida - variação_permitida) | 
                                            (soma_saida_por_modulo > media_saida + variação_permitida)]

        # media_saida, variação_permitida, soma_saida_por_modulo, fora_da_faixa

        def ajustar_saidas_modulos(df):
            trocas = []
            while True:
                media_saida = df['Qtde Venda Frac'].sum() / df['modulo'].nunique()
                variação_permitida = media_saida * 0.02
                soma_saida_por_modulo = df.groupby('modulo')['Qtde Venda Frac'].sum()
                
                # Definindo módulos acima e abaixo da média
                modulos_abaixo = soma_saida_por_modulo[soma_saida_por_modulo < (media_saida - variação_permitida)].index.tolist()
                modulos_acima = soma_saida_por_modulo[soma_saida_por_modulo > (media_saida + variação_permitida)].index.tolist()
                
                # Verificando se ainda há módulos fora da faixa de tolerância
                if not modulos_acima and not modulos_abaixo:
                    break  # Todos os módulos estão dentro da tolerância
                
                # Realizando trocas
                for modulo_abaixo in modulos_abaixo:
                    for modulo_acima in modulos_acima:
                        # Produto com menor saída no módulo abaixo da média
                        produto_min = df[df['modulo'] == modulo_abaixo].nsmallest(1, 'Qtde Venda Frac')
                        diferenca_para_media = media_saida - soma_saida_por_modulo[modulo_abaixo]
                        
                        # Produto no módulo acima da média que melhor ajusta a diferença
                        df_modulo_acima = df[df['modulo'] == modulo_acima]
                        produto_troca = df_modulo_acima.iloc[(df_modulo_acima['Qtde Venda Frac'] - (diferenca_para_media + produto_min['Qtde Venda Frac'].values[0])).abs().argsort()[:1]]
                        
                        # Realizando a troca
                        if not produto_troca.empty and not produto_min.empty:
                            df.loc[produto_min.index, 'modulo'] = modulo_acima
                            df.loc[produto_troca.index, 'modulo'] = modulo_abaixo
                            trocas.append((produto_min['Código'].values[0], modulo_acima, produto_troca['Código'].values[0], modulo_abaixo))
                            break  # Realizar uma troca por iteração
                    
                # Recalcular as somas após a troca
                soma_saida_por_modulo = df.groupby('modulo')['Qtde Venda Frac'].sum()

            return df, trocas

        df_ajustado, lista_trocas = ajustar_saidas_modulos(df.copy())
        trocas = pd.DataFrame(lista_trocas)
        trocas

        botao_download(trocas, 'Download tabela para realocar', 'Cadas linha é uma troca a ser feita.xlsx')