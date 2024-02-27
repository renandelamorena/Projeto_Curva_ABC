#python -m venv 
#./venv/Scripts/activate

# https://projeto-curva-abc.streamlit.app/

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os

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

situacao_final = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx')).set_index('Ordem')
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

    numero_modulos = st.number_input('Número de modulos:', step=1, min_value=1, value=6, max_value=6)

    total_enderecos_molulos = numero_modulos * total_enderecos_mosdulo
    total_enderecos_aa = numero_modulos * AA
    total_enderecos_ab = numero_modulos * AB
    total_enderecos_ac = numero_modulos * AC
    total_enderecos_am = numero_modulos * AM
    total_enderecos_xpe = numero_modulos * XPE

## Tabelas

### Tabelas - Apanha Caixa

sem_apanha_caixa = ((situacao_final['Ender.Cx.Fechada'].isna()) &\
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
#itens de 'apanha_b' no local errado
maiores_ressupr_frac = situacao_final.sort_values(by='Ativ.Ressupr.Frac', ascending=False)

selecao_curvas_b_maiores_ressupr_frac = (maiores_ressupr_frac['Curva Frac'] == 'B') & \
                                        (maiores_ressupr_frac['local'] != 'fd') & \
                                        (maiores_ressupr_frac['local'] != 'controlado') & \
                                        (maiores_ressupr_frac['Tipo'] != 'Ponta De G')

curvas_b_maiores_ressupr_frac = maiores_ressupr_frac[selecao_curvas_b_maiores_ressupr_frac][:300]

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
selecao_local_apanha_c_mudar = ((df_local_not_na['Curva Frac'] == 'C') & \
                             (df_local_not_na['local'] != 'controlado') & \
                             (df_local_not_na['local'] != 'fd') & \
                             (df_local_not_na['local'] != 'antibiotico') & \
                             (df_local_not_na['local'] != 'pet') & \
                             (df_local_not_na['local'] != 'apanha_c') & \
                             (df_local_not_na['local'] != 'alimento')
                             )

mudar_para_apanha_c = df_local_not_na[selecao_local_apanha_c_mudar]

#No local de 'apanha_c', os itens certos e errados
local_apanha_c = situacao_local(['apanha_c'], 'C|-')

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

#### Seleção e tabela de itens errados (curva A no flowrack - mudar para a prateleira [itens cuja ordem é mair o do que a quantidade de endereços do flowrack])

#Itens de curva A, que são medicamentos normais
selecao_med_normal = (~situacao_final['Descrição'].str.contains('xpe|susp|sol|elixir', case=False)) & \
                     (~situacao_final['Descrição'].str.contains('SPRAYZIIN|escova|ABS|DENTAL|TOALHAS|AG ABSORVENTE|COMPRESSA|AG MULTIFRAL|AG PANTS|FITA|MASCARA|ATADURA|CERA ORTODONTICA|ESPARADRAPO', case=False)) & \
                     (situacao_final['Ender.Fracionado'] > 12.999) & \
                     (situacao_final['Curva Frac'] == 'A')

somente_med_A = situacao_final[selecao_med_normal]
total_somente_med_A = somente_med_A.shape[0]

num_linhas_a_excluir = total_somente_med_A - total_enderecos_molulos

if total_somente_med_A > total_enderecos_molulos:
    num_total_linhas = len(somente_med_A)
    produtos_para_flowrack = somente_med_A.drop(somente_med_A.tail(num_linhas_a_excluir).index)
    linhas_excluidas = somente_med_A.tail(num_linhas_a_excluir)
else:
    produtos_para_flowrack = somente_med_A
    linhas_excluidas = []

total_produtos_para_flowrack = produtos_para_flowrack.shape[0]

#Medicamentos curva A normais que estão na prateleira e devem ir para o flowrack
selecao_curva_a_normal_prateleira_para_flowrack = (situacao_final['Tipo'] == 'Prateleira').isin(produtos_para_flowrack)

curva_a_normal_prateleira_para_flowrack = situacao_final[selecao_curva_a_normal_prateleira_para_flowrack]

total_curva_a_normal_prateleira_para_flowrack = curva_a_normal_prateleira_para_flowrack.shape[0]

#Medicamentos curva A normais que estão no flowrack e devem ir para a prateleira
selecao_curva_a_normal_flowrack_para_prateleira = (situacao_final['Tipo'] == 'Flowrack').isin(linhas_excluidas)

curva_a_normal_flowrack_para_prateleira = situacao_final[selecao_curva_a_normal_flowrack_para_prateleira]

total_curva_a_normal_prateleira_para_flowrack = curva_a_normal_flowrack_para_prateleira.shape[0]

#### Tabela saída por modulo (Unidade)

selecao_somente_flowrack = (situacao_final['Tipo'] == 'Flowrack') & \
                           (situacao_final['Ender.Fracionado'] != 9010.000)

somente_flowrack = situacao_final[selecao_somente_flowrack]

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

somente_flowrack['Ender.Fracionado'] = somente_flowrack['Ender.Fracionado'].astype(str)

#Df vazio
tabela_saida_modulo = pd.DataFrame()

for corredor in corredores:

    corredor_atual = somente_flowrack['Ender.Fracionado'].str.startswith(str(corredor))

    saida_corredor_atual = somente_flowrack[somente_flowrack['Ender.Fracionado'].str.startswith(str(corredor))]['Qtde Venda Frac'].sum()

    qnt_item_corredor_atual = somente_flowrack[somente_flowrack['Ender.Fracionado'].str.startswith(str(corredor))]['Qtde Venda Frac'].shape[0]

    nova_linha = pd.Series({'Modulo': corredor_x_modulos[corredor],
                            'Corredor': corredor,
                            'Saída': saida_corredor_atual,
                            'Quanidade itens' : qnt_item_corredor_atual
                            })

    tabela_saida_modulo = pd.concat([tabela_saida_modulo, nova_linha.to_frame().T], ignore_index=True)

#### Seleção e tabela de produtos com endereço de caixa fechada sem endereço de fracionado

com_apanha_caixa_sem_apanha_frac = ((situacao_final['Ender.Cx.Fechada'].notna()) & \
                                    (situacao_final['Ender.Fracionado'].isna())
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

fig_saida_por_modulo = px.bar(tabela_saida_modulo,
                              x='Modulo',
                              y='Saída', 
                              text_auto=True,
                              title='Saída X Modulo'
                              )

fig_saida_por_corredor = px.bar(tabela_saida_modulo,
                              x='Corredor',
                              y='Saída', 
                              text_auto=True,
                              title='Saída X Corredor'
                              )


## Vizualização

aba1, aba2, aba3 = st.tabs(['Métricas', 'Apanha Fracionado', 'Apanha Caixa'])

#Métricas
with aba1:

    coluna1_aba1, coluna2_aba1 = st.columns(2)

    with coluna1_aba1:
        st.write('## Fracionado - Endereços:')

        st.write('Utilizaveis (XPE não): ', total_enderecos_molulos)
        st.write('Classe AA é: ', total_enderecos_aa)
        st.write('Classe AB é: ', total_enderecos_ab)
        st.write('Endereços classe AC é: ', total_enderecos_ac)
        st.write('Liberados para antibióticos é: ', total_enderecos_am)
        st.write('Destinados para XAROPE é: ', total_enderecos_xpe)

    with coluna2_aba1:
            with st.expander('Fracionado'):
                st.metric('Produtos com endereço de fracionado ineficinente:', formata_numero(total_curva_bc_flowrack + total_curva_a_normal_prateleira_para_flowrack + total_curva_a_normal_prateleira_para_flowrack))
                st.metric('Curva A "medicamento"', formata_numero(somente_med_A.shape[0]))

                coluna1, coluna2 = st.columns(2)
                with coluna1:
                    st.metric('Produtos sem endereço de fracionado:', enderecar_frac.shape[0])
                with coluna2:
                    botao_donwload(enderecar_frac, 'Download produtos para endereçar', 'enderecar_frac.xlsx')

            with st.expander('Caixa Fechada'):
                st.metric('Produtos com endereço de caixa fechada ineficinente:', 1)

                coluna1, coluna2 = st.columns(2)
                with coluna1:
                    st.metric('Produtos sem endereço de caixa fechada:', enderecar_caixa.shape[0])
                with coluna2:
                    botao_donwload(enderecar_caixa, 'Download produtos para endereçar', 'enderecar_caixa.xlsx')

#Apanha Fracionado
with aba2:

    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Curvas B e C no Flowrack:', total_curva_bc_flowrack)
        botao_donwload(curva_bc_flowrack, 'Download B e C - Flowrack', 'curva_bc_flowrack_mudar_para_prateleira.xlsx')
    with coluna2:
        st.metric('Curvas A da prateleira (No flowrack)', total_curva_a_normal_prateleira_para_flowrack)
        botao_donwload(curva_a_normal_flowrack_para_prateleira,'Donwload A - Flowrack', 'curva_a_flowrack_mudar_para_prateleira.xlsx')
    with coluna3:
        st.metric('Curvas A do Flowrack (Na prateleira)', total_curva_a_normal_prateleira_para_flowrack)
        botao_donwload(curva_a_normal_prateleira_para_flowrack,'Donwload A - Prateleira', 'curva_a_prateleira_mudar_para_flowrack.xlsx')

    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(fig_saida_por_modulo, use_container_width=True)

        st.markdown('# Filtrar Saída pela Classe')

        #Filtro por modulo
        modulos_escolhidos = st.multiselect('Selecione os modulos:', modulos_escolhidos, default = modulos_escolhidos)

        #Filtro por local
        classes_frac = ['AA', 'AB', 'AC', 'XPE']
        selecao_locais = st.selectbox('Selecione os locais:', classes_frac)

        #Tabela de saido por local/classe
        produto_flowrack = somente_flowrack[['Ender.Fracionado', 'Código', 'Qtde Venda Frac']]
        local_frac['Ender.Fracionado'] = local_frac['Ender.Fracionado'].astype(str)
        saida_por_local_frac = pd.merge(local_frac, produto_flowrack, on='Ender.Fracionado',  how = 'left')

        #Selecionar o(s) modulo(s)
        selecao_modulo = saida_por_local_frac['modulo'].isin(modulos_escolhidos)
        saida_por_local_frac_modulo = saida_por_local_frac[selecao_modulo]

        #Selecionar o(s) local(is)
        selecao_local = saida_por_local_frac_modulo['local'] == selecao_locais
        tabela_saida_por_local = saida_por_local_frac_modulo[selecao_local]    

        fig_saida_por_classe = px.bar(tabela_saida_por_local,
                               x='modulo',
                               y='Qtde Venda Frac',
                               text_auto=True,
                               title='Saída X Classe'
                               )
        
    with coluna2:
        st.plotly_chart(fig_saida_por_corredor, use_container_width=True)

        st.plotly_chart(fig_saida_por_classe, use_container_width=True)

#Apanha Caixa

with aba3:
    locais = ['Ponta', 'Prateleira', 'Apanha A', 'Apanha B', 'Apanha C', 'Apanha AM']

    dfs_locais_valores = {'Ponta' : [local_ponta_total_certo, local_ponta_total_errado],
                        'Prateleira' : [local_prateleira[1], local_prateleira[2]],
                        'Apanha A' : [local_fechada_a[1], local_fechada_a[2]],
                        'Apanha B' : [local_apanha_b_total_certo, local_apanha_b_total_errado],
                        'Apanha C' : [local_apanha_c[1], local_apanha_c[2]],
                        'Apanha AM' : [local_total_certo_am, local_total_errado_am],
                        }
    dfs_locais_tabelas = {'Ponta' : [local_ponta_certo, local_ponta_errado],
                        'Prateleira' : [local_prateleira[3], local_prateleira[4]],
                        'Apanha A' : [local_fechada_a[3], local_fechada_a[4]],
                        'Apanha B' : [certo_apanha_b, errado_apanha_b],
                        'Apanha C' : [local_apanha_c[3], local_apanha_c[4]],
                        'Apanha AM' : [local_certo_am, local_errado_am],
                        }

    st.write('## Situação por local')

    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.session_state.horizontal = False
        opcao_local_grafico = st.radio('Selecione o local:', locais,
                                    horizontal = st.session_state.horizontal)

        botao_donwload(dfs_locais_tabelas[opcao_local_grafico][0], 'Baixar "Itens Certos"', f'itens_certos_local_{opcao_local_grafico}.xlsx')
        botao_donwload(dfs_locais_tabelas[opcao_local_grafico][1], 'Baixar "Itens Errados"', f'itens_errados_local_{opcao_local_grafico}.xlsx')

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
                                horizontal = st.session_state.horizontal)
        
        df_selec = dfs_locais_errados[local_selec]
        total_trocar = df_selec.shape[0]

        st.metric('Total:', total_trocar)
        botao_donwload(df_selec, 'Baixar tabela', f'trocal_local_para_{local_selec}.xlsx')
        
        st.dataframe(df_selec)

#Ideia - Mapa de calor com a saida por endereço do flowrack
