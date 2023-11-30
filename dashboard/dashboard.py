#python -m venv venv
#./venv/Scripts/activate

import streamlit as st
import pandas as pd
import plotly.express as px
import time
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

st.title('Dashbord - Projeto Curva ABC') #Titulo

situacao_final = pd.read_excel(r'..\tratamento_curva_abc\dados_tratados\situacao_final.xlsx').set_index('Ordem')
local_frac = pd.read_excel(r'..\analise_curva_abc\local\datasets\local_apanha_frac.xlsx')

## Barra lateral com filtros

with st.sidebar:

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

    st.write('Endereços utilizaveis (XPE não): ', total_enderecos_molulos)
    st.write('Endereços classe AA é: ', total_enderecos_aa)
    st.write('Endereços classe AB é: ', total_enderecos_ab)
    st.write('Endereços classe AC é: ', total_enderecos_ac)
    st.write('Endereços liberados para antibióticos é: ', total_enderecos_am)
    st.write('Endereços destinados para XAROPE é: ', total_enderecos_xpe)

## Tabelas

### Tabelas - Apanha Caixa

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



    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Produtos com endereço de fracionado ineficinente:', formata_numero(total_curva_bc_flowrack + total_curva_a_normal_prateleira_para_flowrack + total_curva_a_normal_prateleira_para_flowrack))
        with st.expander('Fracionado'):
            coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.metric('Curva A "medicamento"', formata_numero(somente_med_A.shape[0]))

    with coluna2:
        st.metric('Produtos com endereço de caixa fechada ineficinente:', 1)


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

        st.markdown('# Filtar Saída pela Classe')

        #Filtro por modulo
        modulos_escolhidos = st.multiselect('Selecione os modulos:', modulos_escolhidos, default = modulos_escolhidos)

        #Filtro por local
        locais = ['AA', 'AB', 'AC', 'XPE']
        selecao_locais = st.selectbox('Selecione os locais:', locais)

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

#Ideia - Mapa de calor com a saida por endereço do flowrack

#Apanha Caixa
# with aba3: